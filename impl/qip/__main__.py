"""QIP v2.0 CLI. Every subcommand is a station of the loop or a governance surface."""
import argparse
import sys


def main():
    ap = argparse.ArgumentParser(prog="qip", description="Quantum Intelligence Protocol v2.0")
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init", help="create missing collections + payload indexes")

    p = sub.add_parser("audit", help="fail-closed vector integrity audit")
    p.add_argument("--collection", default="qip_knowledge")
    p.add_argument("--strict", action="store_true")
    p.add_argument("--all", action="store_true", help="audit every collection")

    p = sub.add_parser("task", help="create a task (station 1)")
    p.add_argument("text")
    p.add_argument("--project")
    p.add_argument("--frequency", default="mid", choices=["high", "mid", "low", "ultra-low"])
    p.add_argument("--collapse-deadline")

    p = sub.add_parser("heartbeat", help="pick up open tasks, emit execution briefs (station 2)")
    p.add_argument("--max", type=int, default=3)

    p = sub.add_parser("lesson", help="store lesson, close task (station 4)")
    p.add_argument("task_id")
    p.add_argument("text")
    p.add_argument("--type", default="lesson", dest="type_")
    p.add_argument("--principle", help="transferable principle to broadcast via the Mesh")
    p.add_argument("--principle-topic")

    p = sub.add_parser("retrieve", help="tiered retrieval: mind_pin, L3-active, semantic")
    p.add_argument("query")
    p.add_argument("--collection", default="qip_knowledge")
    p.add_argument("--limit", type=int, default=8)

    p = sub.add_parser("capture", help="direct durable capture under the ingest contract")
    p.add_argument("text")
    p.add_argument("--topic", required=True)
    p.add_argument("--type", required=True, dest="type_")
    p.add_argument("--tier", default="L3-active")
    p.add_argument("--project")
    p.add_argument("--collection", default="qip_knowledge")

    p = sub.add_parser("broadcast", help="sign + quarantine a principle into the Mesh")
    p.add_argument("text")
    p.add_argument("--topic", required=True)
    p.add_argument("--scope", default="general")
    p.add_argument("--confidence", type=float, default=0.5)
    p.add_argument("--parents", nargs="*", default=[])

    sub.add_parser("review", help="Guardian queue: quarantined principles")

    p = sub.add_parser("promote", help="Guardian: quarantined -> active")
    p.add_argument("point_id")
    p.add_argument("--trust", type=float)

    p = sub.add_parser("deprecate", help="Guardian: demote + blast-radius recall")
    p.add_argument("point_id")
    p.add_argument("--reason", required=True)

    p = sub.add_parser("adopt", help="adopt an active, trusted principle")
    p.add_argument("point_id")

    p = sub.add_parser("route", help="novelty routing preview for a task text")
    p.add_argument("text")

    p = sub.add_parser("metrics", help="compounding metrics, the falsifiability gate")
    p.add_argument("--window", default="30d")

    sub.add_parser("conformance", help="print the spec/14 checklist with live checks")

    a = ap.parse_args()
    from . import config, loop, memory, mesh, metrics, routing, store

    if a.cmd == "init":
        store.ensure_setup()
    elif a.cmd == "audit":
        cols = config.ALL_COLLECTIONS if a.all else [a.collection]
        ok = all(store.audit(c, strict=a.strict) for c in cols)
        sys.exit(0 if ok else 1)
    elif a.cmd == "task":
        loop.create_task(a.text, project=a.project, frequency=a.frequency,
                         collapse_deadline=a.collapse_deadline)
    elif a.cmd == "heartbeat":
        loop.heartbeat(max_tasks=a.max)
    elif a.cmd == "lesson":
        loop.lesson(a.task_id, a.text, type_=a.type_, principle=a.principle,
                    principle_topic=a.principle_topic)
    elif a.cmd == "retrieve":
        for r in memory.retrieve(a.query, a.collection, a.limit):
            score = f" {r['score']:.3f}" if r.get("score") else ""
            print(f"[{r['via']}{score}] ({r['tier']}/{r['type']}) {r['topic']}\n    {r['preview'][:150]}")
    elif a.cmd == "capture":
        pid = store.capture(a.collection, topic=a.topic, type_=a.type_, tier=a.tier,
                            full_text=a.text, project=a.project)
        print(f"[capture] {pid} written to {a.collection}; running audit")
        sys.exit(0 if store.audit(a.collection) else 1)
    elif a.cmd == "broadcast":
        mesh.broadcast(a.text, a.topic, scope=a.scope, confidence=a.confidence,
                       parent_ids=a.parents)
    elif a.cmd == "review":
        mesh.review_queue()
    elif a.cmd == "promote":
        mesh.promote(a.point_id, trust=a.trust)
    elif a.cmd == "deprecate":
        mesh.deprecate(a.point_id, a.reason)
    elif a.cmd == "adopt":
        mesh.adopt(a.point_id)
    elif a.cmd == "route":
        import json
        print(json.dumps(routing.route(a.text), indent=2))
    elif a.cmd == "metrics":
        metrics.compute(a.window)
    elif a.cmd == "conformance":
        _conformance()


def _conformance():
    from . import config, store
    checks = []
    try:
        names = [c["name"] for c in store.qdrant("GET", "/collections")["result"]["collections"]]
        checks.append(("collections present", all(c in names for c in config.ALL_COLLECTIONS)))
    except Exception:
        checks.append(("collections present", False))
    try:
        checks.append(("audit passes (qip_knowledge)", store.audit("qip_knowledge")))
    except Exception:
        checks.append(("audit passes (qip_knowledge)", False))
    checks.append(("agent key configured (signing)", bool(config.AGENT_KEY)))
    print("\nQIP-Core mechanical checks:")
    for name, ok in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print("Manual items: see spec/14-conformance.md (mechanical passes are necessary, never sufficient)")


if __name__ == "__main__":
    main()
