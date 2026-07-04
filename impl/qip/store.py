"""Qdrant + embedding store. Fail-closed ingest contract enforcement (ops/ingest-contract.md)."""
import datetime
import json
import urllib.error
import urllib.request
import uuid

from . import config, constitution

REQUIRED_FIELDS = [
    "source", "topic", "type", "tier", "project", "timestamp",
    "embedding_model", "embedding_status", "content_preview", "full_text",
    "agent_id", "status", "parent_ids",
]

VALID_TYPES = {
    "decision", "insight", "research_finding", "code_pattern", "user_preference",
    "protocol_change", "operational_rule", "failed_assumption", "accepted_architecture",
    "task", "lesson", "principle", "execution_trace", "inversion_result",
    "hypothesis_result", "validation", "agent_registration",
}


def _request(url, body=None, headers=None, method=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        detail = e.read().decode()[:400]
        raise RuntimeError(f"HTTP {e.code} on {method or 'POST'} {url.split('?')[0]}: {detail}") from None


def qdrant(method, path, body=None):
    return _request(config.QDRANT_URL + path, body,
                    {"Content-Type": "application/json", "api-key": config.QDRANT_KEY}, method)


def embed(text):
    """Canonical embedding. Anything but a real 1536-dim vector is a hard failure (I2)."""
    if not text or not text.strip():
        raise SystemExit("[store] refusing to embed empty text (preview-only writes are forbidden)")
    res = _request("https://api.openai.com/v1/embeddings",
                   {"model": config.CANONICAL_MODEL, "input": text},
                   {"Content-Type": "application/json",
                    "Authorization": "Bearer " + config.OPENAI_KEY}, "POST")
    vec = res["data"][0]["embedding"]
    if len(vec) != config.VECTOR_SIZE:
        raise SystemExit(f"[store] embedding dims {len(vec)} != {config.VECTOR_SIZE}; write refused")
    return vec


def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def normalize_payload(pl):
    """Read-side compatibility with qip_capture_v1 drift (ingest contract, legacy section)."""
    out = dict(pl)
    out.setdefault("topic", pl.get("summary"))
    out.setdefault("tier", pl.get("memory_tier") or pl.get("decay_class"))
    out.setdefault("type", pl.get("knowledge_type") or pl.get("content_type"))
    out.setdefault("full_text", pl.get("content"))
    out.setdefault("status", "active")   # legacy points predate quarantine; treated as active
    out.setdefault("parent_ids", [])
    return out


def capture(collection, *, topic, type_, tier, full_text, project=None, source=None,
            parent_ids=None, extra=None, signature=None, status="active", trust=None):
    """The only write path. Validates, redacts, embeds, upserts, returns point id."""
    if type_ not in VALID_TYPES:
        raise SystemExit(f"[store] unknown type '{type_}'")
    if tier not in config.TIERS:
        raise SystemExit(f"[store] unknown tier '{tier}'")
    if collection not in config.ALL_COLLECTIONS:
        raise SystemExit(f"[store] unknown collection '{collection}'")

    full_text = constitution.redact(full_text.strip())
    payload = {
        "source": source or f"qip-cli:{config.AGENT_ID}",
        "topic": topic, "type": type_, "tier": tier,
        "project": project or config.PROJECT,
        "timestamp": now_iso(),
        "embedding_model": config.CANONICAL_MODEL,
        "embedding_status": "embedded",
        "content_preview": full_text[:200],
        "full_text": full_text,
        "agent_id": config.AGENT_ID,
        "status": status,
        "parent_ids": parent_ids or [],
        "access_count": 0,
        "schema_version": "qip_v2",
    }
    if trust is not None:
        payload["trust"] = trust
    if signature is not None:
        payload["signature"] = signature
    if extra:
        payload.update(extra)
    for f in REQUIRED_FIELDS:
        if f not in payload or payload[f] in (None, ""):
            raise SystemExit(f"[store] contract violation: missing field '{f}'; write refused")
    constitution.assert_write_ok(payload)

    pid = str(uuid.uuid4())
    vec = embed(full_text)
    res = qdrant("PUT", f"/collections/{collection}/points?wait=true",
                 {"points": [{"id": pid, "vector": vec, "payload": payload}]})
    if res.get("status") != "ok":
        raise SystemExit(f"[store] upsert not ok: {res}")
    return pid


def scroll(collection, flt=None, limit=200, with_payload=True):
    pts, offset = [], None
    while True:
        body = {"limit": min(limit - len(pts), 200), "with_payload": with_payload, "with_vector": False}
        if flt:
            body["filter"] = flt
        if offset:
            body["offset"] = offset
        res = qdrant("POST", f"/collections/{collection}/points/scroll", body)["result"]
        pts += res["points"]
        offset = res.get("next_page_offset")
        if not offset or len(pts) >= limit:
            return pts


def search(collection, query_text, limit=8, flt=None):
    body = {"vector": embed(query_text), "limit": limit, "with_payload": True}
    if flt:
        body["filter"] = flt
    return qdrant("POST", f"/collections/{collection}/points/search", body)["result"]


def get_points(collection, ids):
    return qdrant("POST", f"/collections/{collection}/points",
                  {"ids": ids, "with_payload": True, "with_vector": False})["result"]


def set_payload(collection, ids, payload):
    return qdrant("POST", f"/collections/{collection}/points/payload?wait=true",
                  {"payload": payload, "points": ids})


def ensure_setup():
    """`qip init`: create missing collections, ensure payload indexes (canonical-state rule)."""
    existing = [c["name"] for c in qdrant("GET", "/collections")["result"]["collections"]]
    for name in config.ALL_COLLECTIONS:
        if name not in existing:
            qdrant("PUT", f"/collections/{name}",
                   {"vectors": {"size": config.VECTOR_SIZE, "distance": config.DISTANCE}})
            print(f"[init] created collection {name}")
    for name in config.ALL_COLLECTIONS:
        for field in config.INDEXED_FIELDS:
            try:
                qdrant("PUT", f"/collections/{name}/index?wait=true",
                       {"field_name": field, "field_schema": "keyword"})
                print(f"[init] index {name}.{field} ok")
            except RuntimeError as e:
                if "already exists" in str(e).lower() or "400" in str(e):
                    print(f"[init] index {name}.{field} exists")
                else:
                    raise


def audit(collection="qip_knowledge", strict=False):
    """Vector-integrity audit; the fail-closed gate. Returns True on pass."""
    pts = scroll(collection, limit=100000)
    bad_model, bad_status, missing_full = [], [], []
    for p in pts:
        pl = p["payload"]
        if pl.get("embedding_model") != config.CANONICAL_MODEL:
            bad_model.append(p["id"])
        if pl.get("embedding_status") != "embedded":
            bad_status.append(p["id"])
        if strict and not (pl.get("full_text") or pl.get("content")):
            missing_full.append(p["id"])
    print(f"[audit] {collection}: {len(pts)} points | canonical model: "
          f"{len(pts) - len(bad_model)}/{len(pts)} | embedded: {len(pts) - len(bad_status)}/{len(pts)}")
    if strict:
        print(f"[audit:strict] missing full_text: {len(missing_full)} (remediation backlog, see MAP.md)")
    ok = not bad_model and not bad_status
    print("[audit] PASS" if ok else f"[audit] FAIL model={bad_model[:5]} status={bad_status[:5]}")
    return ok
