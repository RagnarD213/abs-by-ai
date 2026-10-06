---
name: handoffs-not-auto-added-to-dashboard
description: Dan's rule 2026-09-08 — never add a dashboard row for a new handoff doc unless he explicitly asks; the queue is the coordination file's HANDOFFS section + Handoffs/README.md
metadata:
  type: feedback
---

On 2026-09-08 Dan retired the "every handoff doc gets a Key dashboard task" rule. New handoff docs are
listed in the HANDOFFS section of `AI_COORDINATION.md` and the Open table of `Handoffs/README.md`,
and get a dashboard row ONLY when Dan explicitly asks for one.

**Why:** the money column had filled with executed and superseded "Execute handoff:" rows (two sweeps
were needed, 09-01 and 09-08) until the real top priorities were invisible. He wants the dashboard to
show only what actually needs doing.

Later the same day he had the board hard-reset to 11 rows (4 open handoffs + 7 he named; `scripts/dashboard/cleanup_20260908_reset.py`). **He wants the dashboard minimal: only things that genuinely need doing.** Review-this / decide-this / blocked-on-Dan items belong in the coordination file and the morning brief, not on the board.

**How to apply:** after writing a handoff, add it to the two lists, give the starter prompt in chat, and
stop. If he says "put it on the board", use the `/dashboard-tasks` skill. A session that executes a
handoff removes it from both lists. The separate "Handoffs to fire" card (stored list `handoffs`, cap 7, status chip + copy-prompt button, delete when run, 14-day stale flag) was BUILT the same day at his request — mechanics in the `/dashboard-tasks` skill. See [[bias-toward-action]] for the general rule and
[[handoff-starter-prompt-rule]] for how handoffs are delivered.
