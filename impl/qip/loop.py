"""Compound Autonomy Loop (spec/11): task -> heartbeat -> memory-informed execution -> lesson."""
from . import config, constitution, memory, routing, store

SESSION = config.COLLECTIONS["session"]
BUSINESS = config.COLLECTIONS["business"]


def create_task(text, project=None, frequency="mid", collapse_deadline=None):
    """Station 1: any agent (or the system itself) files work."""
    flags = constitution.screen_task(text)
    extra = {"task_status": "open", "frequency": frequency}
    if collapse_deadline:
        extra["collapse_deadline"] = collapse_deadline
    if flags:
        extra["constitution_flags"] = [f"{i}: {msg}" for i, msg in flags]
    pid = store.capture(SESSION, topic=f"task-{text[:60].lower().replace(' ', '-')}",
                        type_="task", tier="L3-active", full_text=text,
                        project=project, extra=extra)
    print(f"[loop] task {pid} created (status=open, frequency={frequency})")
    for inv, msg in flags:
        print(f"[loop]   ⚠ {inv}: {msg}")
    return pid


def heartbeat(max_tasks=3):
    """Station 2 + 3 setup: wake, pick up open tasks, build DC, emit execution briefs."""
    flt = {"must": [{"key": "type", "match": {"value": "task"}}]}
    open_tasks = [p for p in store.scroll(SESSION, flt, limit=200)
                  if p["payload"].get("task_status") == "open"]
    open_tasks.sort(key=lambda p: p["payload"].get("timestamp", ""))
    if not open_tasks:
        print("HEARTBEAT_OK")
        return []

    briefs = []
    for p in open_tasks[:max_tasks]:
        pl = p["payload"]
        text = pl.get("full_text", "")
        dc = memory.build_decision_context(text, BUSINESS)
        rt = routing.route(text, BUSINESS)
        brief = {
            "task_id": p["id"], "task": text, "project": pl.get("project"),
            "frequency": pl.get("frequency"), "route": rt, "dc": dc["summary"],
            "constitution_flags": pl.get("constitution_flags", []),
            "ei_pre_execution": [
                "Predict: what will this action change in the environment?",
                "Tag: what intelligence will this execution generate?",
            ],
        }
        store.set_payload(SESSION, [p["id"]],
                          {"task_status": "in_progress", "claimed_by": config.AGENT_ID,
                           "claimed_at": store.now_iso(),
                           "dc_summary": dc["summary"], "route": rt["path"],
                           "novelty": rt["novelty"]})
        memory.touch(BUSINESS, [x["id"] for x in dc["patterns"][:3]])
        briefs.append(brief)

        print("=" * 72)
        print(f"TASK {p['id']}  [{rt['path'].upper()} | novelty {rt['novelty']}]  "
              f"project={pl.get('project')}")
        print(text)
        for f in brief["constitution_flags"]:
            print(f"  ⚠ CONSTITUTION {f}")
        print("-" * 72)
        print(dc["summary"])
        print(f"ROUTE: {rt['directive']}")
        print("EI PRE-EXECUTION: " + " | ".join(brief["ei_pre_execution"]))
        print(f"CLOSE WITH: python3 -m qip lesson {p['id']} \"<what was learned>\"")
    return briefs


def lesson(task_id, text, type_="lesson", principle=None, principle_topic=None):
    """Station 4: store the lesson, close the task, optionally hand a principle to the Mesh."""
    pts = store.get_points(SESSION, [task_id])
    if not pts:
        raise SystemExit(f"[loop] no such task {task_id}")
    task_pl = pts[0]["payload"]
    lid = store.capture(BUSINESS, topic=f"lesson-{(task_pl.get('topic') or task_id)[:60]}",
                        type_=type_, tier="L3-active", full_text=text,
                        project=task_pl.get("project"), parent_ids=[task_id],
                        extra={"route_taken": task_pl.get("route"),
                               "dc_summary": task_pl.get("dc_summary", "")[:500]})
    store.set_payload(SESSION, [task_id],
                      {"task_status": "done", "lesson_id": lid,
                       "closed_at": store.now_iso()})
    print(f"[loop] lesson {lid} stored; task {task_id} closed")
    if principle:
        from . import mesh
        mesh.broadcast(principle, principle_topic or f"principle-from-{task_id[:8]}",
                       parent_ids=[lid])
    else:
        print("[loop] no principle extracted. If a transferable generalization exists, "
              "broadcast it: python3 -m qip broadcast \"<principle>\" --topic <topic> "
              f"--parents {lid}")
    return lid
