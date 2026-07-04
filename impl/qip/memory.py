"""Identity Core: tiered retrieval and Decision Context construction (spec/02, spec/09)."""
from . import config, store

# Quarantine wall (I5): DC and retrieval never read quarantined/deprecated points.
NOT_QUARANTINED = {"must_not": [{"key": "status", "match": {"any": ["quarantined", "deprecated"]}}]}


def _fmt(p):
    pl = store.normalize_payload(p["payload"])
    return {
        "id": p["id"], "topic": pl.get("topic"), "type": pl.get("type"),
        "tier": pl.get("tier"), "project": pl.get("project"),
        "preview": (pl.get("content_preview") or (pl.get("full_text") or "")[:200]),
        "trust": pl.get("trust"), "score": p.get("score"),
    }


def retrieve(query, collection="qip_knowledge", limit=8):
    """Normative order: mind_pin, then L3-active, then semantic (spec/02)."""
    out, seen = [], set()

    def take(points, label):
        for p in points:
            if p["id"] not in seen:
                seen.add(p["id"])
                row = _fmt(p)
                row["via"] = label
                out.append(row)

    tier_f = lambda t: {"must": [{"key": "tier", "match": {"value": t}}],
                        "must_not": NOT_QUARANTINED["must_not"]}
    take(store.scroll(collection, tier_f("mind_pin"), limit=12), "mind_pin")
    take(store.scroll(collection, tier_f("L3-active"), limit=12), "L3-active")
    take(store.search(collection, query, limit=limit, flt=NOT_QUARANTINED), "semantic")
    return out


def build_decision_context(task_text, collection="qip_knowledge"):
    """DC pipeline: identity -> patterns -> objectives -> environment (spec/09)."""
    identity = [_fmt(p) for p in store.scroll(
        collection, {"must": [{"key": "tier", "match": {"value": "mind_pin"}}]}, limit=8)]
    patterns = [_fmt(p) for p in store.search(collection, task_text, limit=5, flt=NOT_QUARANTINED)]
    objectives = [_fmt(p) for p in store.scroll(
        collection, {"must": [{"key": "tier", "match": {"value": "L3-active"}}],
                     "must_not": NOT_QUARANTINED["must_not"]}, limit=8)]
    dc = {
        "identity": identity,
        "patterns": patterns,
        "objectives": objectives,
        "environment": {"read_at": store.now_iso(),
                        "note": "live scout feeds attach here in multi-agent deployments"},
    }
    dc["summary"] = summarize(dc, task_text)
    return dc


def summarize(dc, task_text):
    lines = [f"DECISION CONTEXT for: {task_text[:120]}"]
    lines.append("- identity: " + "; ".join(i["topic"] or "?" for i in dc["identity"][:5]))
    lines.append("- patterns: " + "; ".join(
        f"{p['topic']}({p['score']:.2f})" if p.get("score") else str(p["topic"])
        for p in dc["patterns"][:5]))
    lines.append("- objectives: " + "; ".join(o["topic"] or "?" for o in dc["objectives"][:5]))
    return "\n".join(lines)


def touch(collection, point_ids):
    """Reuse accounting: increment access_count on points that informed an execution."""
    for pid in point_ids:
        pts = store.get_points(collection, [pid])
        if pts:
            count = int(pts[0]["payload"].get("access_count") or 0) + 1
            store.set_payload(collection, [pid], {"access_count": count,
                                                  "last_accessed": store.now_iso()})
