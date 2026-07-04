"""Compounding metrics and the falsifiability gate (spec/12)."""
import datetime

from . import config, store

BUSINESS = config.COLLECTIONS["business"]
SESSION = config.COLLECTIONS["session"]


def _cutoff(window):
    n, unit = int(window[:-1]), window[-1]
    days = n * 7 if unit == "w" else n
    return (datetime.datetime.now(datetime.timezone.utc)
            - datetime.timedelta(days=days)).isoformat()


def compute(window="30d"):
    since = _cutoff(window)
    biz = [store.normalize_payload(p["payload"]) | {"_id": p["id"]}
           for p in store.scroll(BUSINESS, limit=100000)]
    ses = [p["payload"] for p in store.scroll(SESSION, limit=100000)]

    in_window = [p for p in biz if (p.get("timestamp") or "") >= since]
    lessons = [p for p in in_window if p.get("type") in ("lesson", "insight", "research_finding")]
    principles_all = [p for p in biz if p.get("type") == "principle"]
    principles_new = [p for p in principles_all if (p.get("timestamp") or "") >= since]

    adoptions = sum(len(p.get("adopted_by") or []) for p in principles_all)
    cross = sum(1 for p in principles_all
                for a in (p.get("adopted_by") or []) if a != p.get("agent_id"))
    reuse_events = sum(int(p.get("access_count") or 0) for p in biz)
    rejected = [p for p in principles_all if p.get("status") == "deprecated"]
    quarantined = [p for p in principles_all if p.get("status") == "quarantined"]

    tasks = [p for p in ses if p.get("type") == "task" and (p.get("timestamp") or "") >= since]
    done = [t for t in tasks if t.get("task_status") == "done"]
    routed = [t for t in tasks if t.get("route")]
    fast_share = (sum(1 for t in routed if t.get("route") == "fast") / len(routed)) if routed else None
    reversals = [p for p in in_window if p.get("type") == "decision" and p.get("reversed")]
    repaid = _repaid_lessons(biz)

    new_lessons = max(len(lessons), 1)
    cc = round((reuse_events + adoptions) / new_lessons, 2)

    print(f"QIP COMPOUNDING METRICS  window={window}  computed={store.now_iso()}")
    print(f"  compounding coefficient (CC)   {cc}   "
          f"[{'compounding' if cc > 1 else 'linear' if cc == 1 else 'archive, not intelligence'}]")
    print(f"  lessons stored (window)        {len(lessons)}")
    print(f"  principles: total/new/active   {len(principles_all)}/{len(principles_new)}/"
          f"{sum(1 for p in principles_all if p.get('status') == 'active')}")
    print(f"  adoption events (all time)     {adoptions}  cross-identity: {cross}")
    print(f"  reuse events (access_count Σ)  {reuse_events}")
    print(f"  tasks: created/done (window)   {len(tasks)}/{len(done)}")
    print(f"  fast-path share                {f'{fast_share:.0%}' if fast_share is not None else 'n/a (no routed tasks yet)'}")
    print(f"  quarantine: pending/rejected   {len(quarantined)}/{len(rejected)}"
          + ("   ⚠ zero rejections ever recorded: review may be theater" if not rejected else ""))
    print(f"  decision reversals (window)    {len(reversals)}")
    print(f"  re-paid lessons                {repaid}"
          + ("   ⚠ same failure captured twice: compounding leak" if repaid else ""))
    print("  honesty: numbers include only integrity-passing points; "
          "external claims must reproduce from this output (spec/12)")
    return {"cc": cc, "lessons": len(lessons), "adoptions": adoptions,
            "fast_share": fast_share, "rejected": len(rejected), "repaid": repaid}


def _repaid_lessons(biz):
    seen, repaid = {}, 0
    for p in biz:
        if p.get("type") == "failed_assumption":
            key = (p.get("topic") or "")[:80]
            if key in seen:
                repaid += 1
            seen[key] = True
    return repaid
