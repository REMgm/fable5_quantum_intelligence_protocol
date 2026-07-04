"""Scalable EI novelty routing: Fast/Smart/Deep (spec/07). Hybrid metric, pluggable."""
from . import store
from .memory import NOT_QUARANTINED

FAST_MAX = 0.35   # novelty below this: apply cached pattern
SMART_MAX = 0.65  # below this: standard reasoning; above: Einstein Gateway mandatory


def novelty(task_text, collection="qip_knowledge"):
    """Hybrid: distance to nearest active patterns, tempered by neighborhood density.

    Returns (score 0..1, evidence list). Master Coordination's open decision
    (novelty vs surprise vs hybrid) resolved as hybrid-by-default; replace this
    function to change the metric, nothing else needs to move.
    """
    hits = store.search(collection, task_text, limit=5, flt=NOT_QUARANTINED)
    if not hits:
        return 1.0, []
    top = hits[0].get("score") or 0.0            # cosine similarity
    mean3 = sum(h.get("score") or 0.0 for h in hits[:3]) / min(3, len(hits))
    score = 0.7 * (1.0 - top) + 0.3 * (1.0 - mean3)
    return round(min(max(score, 0.0), 1.0), 3), hits


def route(task_text, collection="qip_knowledge"):
    score, hits = novelty(task_text, collection)
    if score < FAST_MAX:
        path = "fast"
        directive = "Pattern hit. Apply the cached pattern; log reuse via memory.touch()."
    elif score < SMART_MAX:
        path = "smart"
        directive = "Partial precedent. Standard reasoning informed by pattern layer."
    else:
        path = "deep"
        directive = ("No precedent. Einstein Gateway MANDATORY: three bold hypotheses "
                     "on record before further retrieval (spec/01).")
    return {"path": path, "novelty": score, "directive": directive,
            "nearest": [{"id": h["id"], "score": round(h.get("score") or 0, 3),
                         "topic": store.normalize_payload(h["payload"]).get("topic")}
                        for h in hits[:3]]}
