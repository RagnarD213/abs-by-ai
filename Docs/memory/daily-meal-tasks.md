---
name: daily-meal-tasks
description: "Dan's three daily meal-timing health tasks, and the stale-write bug that kept deleting them"
metadata: 
  node_type: memory
  type: project
  originSessionId: a53d9967-0126-408e-b6e9-6a492955dc23
  modified: 2026-08-10T20:18:32.901Z
---

Dan wants three meal-timing tasks on the dashboard **every day**: `Salad by 2:00 PM`, `Large meal by 6:00 PM`, `Small meal by 9:00 PM`. They live in the `health` list with `recurring: true`. This fits [[dan-daily-habits]] (eat earlier, last meal done by ~9 PM, for sleep).

**Why:** they vanished repeatedly and he had to ask several times. **An earlier version of this memory blamed that on the tasks never having been created — that was wrong.** They WERE created, on 2026-08-05 and again on 2026-08-07, and both times something deleted them. Traced 2026-08-10 in `todos.json` git history: a whole-file `POST /api/todos` writes back whatever the caller holds, so any client with a stale copy silently deleted every task added since. Commit `7e4c573d` (2026-08-10 08:07:40) is the clean example — it removed all three meal tasks plus two business tasks in one write. Same class of write hit them on 08-06 and 08-07.

**Fixed 2026-08-10** (commit `f83533b`): `POST /api/todos` now diffs against a fresh read — a missing `recurring: true` task is restored unless the caller names it in `allowDeletes`, and a write dropping 3+ other tasks is refused with a 409. The dashboard's `addedAt` backfill also no longer saves on load, which had made every page view rewrite the whole file.

**How to apply:** "Daily" here means ONE permanent entry with `recurring: true` — `dashboard.html` `isDone()` counts a recurring task as done only when `taskLog[id]` holds today's date, so it re-appears unchecked each morning by itself. Never add a task per day. When editing the lists by hand, GET and POST back to back, send all four lists (`business`/`health`/`personal`/`assistant` — an omitted list is deleted), and on a 409 re-read rather than retrying the same body. Renaming changes the check id (`<displayKey>::<exact text>`), so migrate today's completion or the streak looks broken.
