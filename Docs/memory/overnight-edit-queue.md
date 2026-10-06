---
name: overnight-edit-queue
description: "Unattended video edit dispatcher in scripts/edit-queue/ — LIVE since 09-18 after the Phase 0 proof; shares Dan's 5-hour Claude allowance; by-hand launches count toward the nightly cap; -p text output hides tokens and progress"
metadata: 
  node_type: memory
  type: project
  originSessionId: 38f14912-ad9b-4c0d-9630-39d5d57d805f
  modified: 2026-09-18T09:28:29.570Z
---

Built 2026-09-17: `scripts/edit-queue/` holds the overnight edit queue (dispatcher tick every 15 min via launchd
`com.absbyai.edit-queue`, runner with cross-review, scoreboard, review page at http://127.0.0.1:8830). Everything
about it is in `scripts/edit-queue/README.md`; design in `Handoffs/handoff-20260917-overnight-edit-queue.md`.
Routing (Dan): Codex = RA/RO/DS raw first cuts, Claude = AV/AS/SL secondary cuts ([[video-editing-executor-routing]]).
Models (Dan, 09-17): edits Opus/high + Sol/high — a commit once silently reverted them; check `config.json` first.

**Why:** the Mac mini idles overnight; Dan's review time (4 items) and AI allowance are the scarce resources.

**How to apply:**
- **Phase 0 passed 2026-09-18, queue RESUMED.** AV-01 (Ad 1 9:16 59s) ran 1.03 h unattended on Opus/high, no prompt,
  parked honestly on the approved master's own faults; a by-hand Codex review agreed (`DOES NOT SHIP`). Phase 2
  (AI-clip placeholder flow) is not built. SL-01/SL-02 carry `unattended:false` (they need Dan's segment picks).
- **The queue shares the account's 5-hour Claude window with Dan's day sessions.** A launch after a heavy day dies
  with "hit your monthly spend limit … session limit resets 9pm"; the dispatcher can't see allowance beforehand, so
  the only guard is `usage_limit_patterns` (extended 09-18 to match that wording) + the 2-hour back-off.
- A dead run leaves a half-used work dir the eligibility check reads as "half-built": move it to
  `_edit_work/_queue-failed/<run id>/`, then `queue.py set <ID> ready`.
- `launch-one` runs count toward the nightly cap (3, rolls over at noon). A Claude `-p --output-format text`
  session logs nothing until it ends and exposes no token counts; watch the work dir for progress.
- Headless Codex must run `-s danger-full-access` (Dan's own config default): `workspace-write` denies `/bin/ps`,
  which every edit needs for the two-build cap, and blocks rclone's token refresh.
- The dispatcher keeps out of any job whose ID appears in `AI_COORDINATION.md` ACTIVE or that has a work directory
  with a build in it. Never write a queue job's ID into the queue's own board line.
- The folder contains `queue.py`, which shadows Python's stdlib `queue`; scripts there call `eq.unshadow()` and load
  siblings with `eq.sibling()` (a plain `import runner` fails).
- Artifact `write_db` to the Edit Queue page needs `if_version` for existing job docs (see the edit-queue skill README).
