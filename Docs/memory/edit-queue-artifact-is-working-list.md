---
name: edit-queue-artifact-is-working-list
description: Dan works from the Edit Queue artifact page, not 00-MASTER.md; every queue change must be verified visible on the page
metadata:
  type: feedback
---
The Abs By AI Edit Queue artifact (https://claude.ai/artifact/1r1T8Znf96XH24zHZhybHs) is Dan's working list (2026-09-24). Updating jobs.json / 00-MASTER.md alone is not done.

**Why:** 09-24 I added 18 jobs from the 9/23 shoot; 9 were invisible because the page only renders groups hard-coded in its LISTS array and Dedicated-shorts subs "Talking"/"Workout". Dan couldn't find them.

**How to apply:** after any `queue.py add/set`: (1) `queue.py push` (Drive) and write_db the exported rows (pin `if_version` on existing docs), (2) check every new job's `group` is in the page's LISTS groups and any Dedicated-shorts `sub` is rendered; if not, edit the page (read it, republish same URL), (3) confirm on the page. The in-app browser is signed out, so verify via the page source logic and tell Dan how to spot the rows.

**Row labels (Dan, 2026-10-08):** an in-progress row names who is editing it ("In progress Muhammad", "In progress Codex", "In progress Claude"): set it with `queue.py set <ID> in_progress --by X --editor Name`. A blocked row shows what unblocks it beside the title: `queue.py set <ID> blocked --needs "one short line"` (the tool refuses a blocked job with no `--needs`). In List 2, "ready" displays as "Shorts not cut yet". When a long-form's release date moves, fix the date in its SL row title too.
