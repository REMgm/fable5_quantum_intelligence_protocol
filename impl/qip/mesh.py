"""Indra's Mesh with Integrity layer: signed broadcast, quarantine, trust, recall (spec/04, spec/10)."""
import hashlib
import hmac

from . import config, store

BUSINESS = config.COLLECTIONS["business"]


def _sig(topic, full_text, timestamp, agent_id, key):
    msg = "|".join([topic, full_text, timestamp, agent_id]).encode()
    return hmac.new(key.encode(), msg, hashlib.sha256).hexdigest()


def sign_payload(topic, full_text, timestamp):
    if not config.AGENT_KEY:
        raise SystemExit("[mesh] QIP_AGENT_KEY not set; unsigned broadcasts are forbidden (spec/10)")
    return _sig(topic, full_text, timestamp, config.AGENT_ID, config.AGENT_KEY)


def verify(point, key):
    pl = store.normalize_payload(point["payload"])
    expect = _sig(pl.get("topic", ""), pl.get("full_text", ""), pl.get("timestamp", ""),
                  pl.get("agent_id", ""), key)
    return hmac.compare_digest(expect, pl.get("signature", ""))


def broadcast(principle_text, topic, *, scope="general", confidence=0.5,
              parent_ids=None, collection=BUSINESS):
    """Step 1-3 of the Mesh protocol: extract (caller), encode, sign, quarantine."""
    ts = store.now_iso()
    # capture() stamps its own timestamp; sign over full_text+topic+agent, embed ts in extra
    sig = _sig(topic, principle_text.strip(), ts, config.AGENT_ID,
               config.AGENT_KEY or _require_key())
    pid = store.capture(
        collection, topic=topic, type_="principle", tier="L2-mid",
        full_text=principle_text, parent_ids=parent_ids or [],
        status="quarantined", trust=0.30, signature=sig,
        extra={"applicability_scope": scope, "confidence": confidence,
               "signed_at": ts, "adopted_by": [], "validations": []},
    )
    print(f"[mesh] principle {pid} broadcast in QUARANTINE (trust=0.30). Guardian review required.")
    return pid


def _require_key():
    raise SystemExit("[mesh] QIP_AGENT_KEY not set; unsigned broadcasts are forbidden (spec/10)")


def review_queue(collection=BUSINESS):
    flt = {"must": [{"key": "status", "match": {"value": "quarantined"}}]}
    rows = store.scroll(collection, flt, limit=100)
    for p in rows:
        pl = store.normalize_payload(p["payload"])
        print(f"- {p['id']}  [{pl.get('agent_id')}]  {pl.get('topic')}\n"
              f"    {pl.get('content_preview', '')[:160]}")
    if not rows:
        print("[mesh] quarantine queue empty")
    return rows


def promote(point_id, collection=BUSINESS, trust=None):
    """Guardian approval. Inversion pass (spec/06) is part of review; record it separately."""
    store.set_payload(collection, [point_id],
                      {"status": "active", "trust": trust or config.TRUST_THRESHOLD,
                       "promoted_by": config.AGENT_ID, "promoted_at": store.now_iso()})
    print(f"[mesh] {point_id} promoted to ACTIVE (trust={trust or config.TRUST_THRESHOLD})")


def deprecate(point_id, reason, collection=BUSINESS):
    """Demotion with blast-radius recall: flag every adopter-derived pattern (spec/10)."""
    store.set_payload(collection, [point_id],
                      {"status": "deprecated", "deprecated_reason": reason,
                       "deprecated_by": config.AGENT_ID, "deprecated_at": store.now_iso()})
    flagged = 0
    for p in store.scroll(collection, limit=100000):
        pl = store.normalize_payload(p["payload"])
        if point_id in (pl.get("parent_ids") or []):
            store.set_payload(collection, [p["id"]],
                              {"needs_review": True,
                               "review_reason": f"ancestor {point_id} deprecated: {reason}"})
            flagged += 1
    print(f"[mesh] {point_id} DEPRECATED; blast-radius recall flagged {flagged} descendant point(s)")


def adopt(point_id, collection=BUSINESS):
    """Step 4-5: identity-filtered adoption. Enforces status + trust threshold."""
    pts = store.get_points(collection, [point_id])
    if not pts:
        raise SystemExit(f"[mesh] no such point {point_id}")
    pl = store.normalize_payload(pts[0]["payload"])
    if pl.get("status") != "active":
        raise SystemExit(f"[mesh] refusing adoption: status={pl.get('status')} (quarantine wall, I5)")
    if float(pl.get("trust") or 0) < config.TRUST_THRESHOLD:
        raise SystemExit(f"[mesh] refusing adoption: trust {pl.get('trust')} < {config.TRUST_THRESHOLD}")
    adopted = list(pl.get("adopted_by") or [])
    if config.AGENT_ID not in adopted:
        adopted.append(config.AGENT_ID)
    store.set_payload(collection, [point_id],
                      {"adopted_by": adopted,
                       "access_count": int(pl.get("access_count") or 0) + 1,
                       "last_accessed": store.now_iso()})
    print(f"[mesh] adopted {point_id} as {config.AGENT_ID}; adopters={adopted}")
    return pl
