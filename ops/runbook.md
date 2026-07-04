# Ops Runbook

## First-time setup

```bash
cp .env.example .env      # fill in cluster URL + keys; .env is gitignored
cd impl
python3 -m qip init       # creates missing collections + payload indexes
python3 -m qip audit      # must pass before anything else runs
```

Key handling: keys live in `.env` (local) or the platform keychain, never in repo files, never in captures (invariant I3 redacts, but do not test it on purpose), never in process names when avoidable.

## Heartbeat scheduling

macOS (launchd) preferred over cron for laptop deployments, it survives sleep better:

```xml
<!-- ~/Library/LaunchAgents/com.qip.heartbeat.plist -->
<plist version="1.0"><dict>
  <key>Label</key><string>com.qip.heartbeat</string>
  <key>ProgramArguments</key><array>
    <string>/bin/zsh</string><string>-lc</string>
    <string>cd /path/to/repo/impl && set -a && source ../.env && python3 -m qip heartbeat >> ~/.qip/heartbeat.log 2>&1</string>
  </array>
  <key>StartInterval</key><integer>1800</integer>
</dict></plist>
```

`launchctl load ~/Library/LaunchAgents/com.qip.heartbeat.plist`. Linux: equivalent cron `*/30 * * * *`. Exact-time jobs (Monday 09:00 strategy cycle) get their own cron entry; heartbeat for drift-tolerant batching, cron for precision (AGENTS.md rule).

## Cadences

| Cadence | Command | Purpose |
|---|---|---|
| 30 min | `qip heartbeat` | Task pickup, execution briefs |
| Daily | `qip audit` | Vector integrity |
| Weekly | `qip review` + `qip metrics --window 7d` | Quarantine queue, compounding check |
| Monthly | `qip metrics --window 30d` + inversion pass | Falsifiability gate, paradigm lock check |

## Incident response

- Audit fails: stop writes, identify offending points, fix or delete, re-audit. Fail-closed means the pipeline stays down until green
- Poisoned/deprecated principle: `qip deprecate <id>` cascades review flags to adopters (blast-radius recall, spec/10); review each derived pattern before re-activation
- Cluster migration: write a superseding `mind_pin` canonical-state capture naming old and new endpoints (2026-06-28 precedent); never edit history
- Schema drift discovered: extend `normalize_payload`, capture a `protocol_change`, remediate on touch

## Remediation backlog (from MAP.md)

404 `qip_research` points lack `full_text` (pre-contract migration). Path: re-chunk source documents in `qip_documents`, re-embed, supersede. Run as a low-frequency background task, not a big-bang rewrite.
