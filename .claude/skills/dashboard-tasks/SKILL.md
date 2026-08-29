---
name: dashboard-tasks
description: Read or write the Victory Dashboard task board — check a finished task off, add a Rule-8 Key task for a new handoff, or inspect /api/todos, /api/task-checks and /api/plan. Use at the end of any completed task (committed, pushed, deployed, verified) so its dashboard row gets struck through, and whenever a handoff document is created — even if Dan doesn't mention the dashboard.
---

# Victory Dashboard task mechanics

Finishing a task means checking it off at `absbyai.com/dashboard` in the same session — Dan should not have to click it himself. Do it after the change is committed, pushed, deployed and verified, as the last step of the task.

## Auth — every call needs the key

These endpoints are gated (added 2026-08-19): `/api/todos`, `/api/task-checks`, `/api/plan`, `/api/tasks-state`, `/api/morning-data`, `/api/monarch`. Send `X-Dash-Key: $DASH_SECRET` on every call. The one exception is an `assistant::` check-off, which the public `/assistant` page must be able to make and so needs no key.

```bash
DASH=$(grep '^DASH_SECRET=' ~/.absbyai-secrets.env | cut -d= -f2-)
```

**A 401 means the key is missing or stale, not that the id was wrong** — it is the single most likely reason a check-off silently stops working. Refresh the cache: `~/.npm-global/bin/railway variables --service abs-by-ai --kv > ~/.absbyai-secrets.env && chmod 600 ~/.absbyai-secrets.env`. (Without `--service abs-by-ai`, the CLI reads the linked Postgres service and returns the wrong variables — verified 2026-08-19.)

## Checking a task off

```bash
# 1. Find the task's exact text.  Stored lists are business / health / personal / assistant.
curl -s -H "X-Dash-Key: $DASH" https://absbyai.com/api/todos | python3 -m json.tool
# 2. Check it off.  The id is "<displayKey>::<exact text>".
curl -s -X POST https://absbyai.com/api/task-checks -H "X-Dash-Key: $DASH" \
  -H 'Content-Type: application/json' \
  -d '{"id":"money::Execute handoff: Close locked-image leak on paywall","checked":true}'
```

Four traps, the first three verified on 2026-07-29:

- **Done state lives in `/api/task-checks`, not in `todos.json`.** Setting a `done` field on the todo object does nothing — no surface reads it. `POST /api/task-checks` with `{ id, checked: true }` is the only mechanism.
- **The `business` list is displayed as `money`, and check ids use the DISPLAY key.** `dashboard.html` merges the stored `business` list into `todosState.money` (~line 1615) and writes it back as `business` (~2111), while `taskCheckId()` builds `<displayKey>::<text>`. So a money-column task is `money::…`, never `business::…`. `health`, `personal` and `assistant` are the same in both.
- **The text must match exactly**, including punctuation — the id is the raw text. Fetch it, don't retype it.
- **`assistant` is delegated work — Dan's personal assistant's (Brittany's) list, not Dan's.** It is mirrored to the unauthenticated `absbyai.com/assistant` page and excluded from Work Session Focus auto-population. Do not put agent work orders, Dan's own tasks, or Rule-8 handoff tasks there — handoff tasks go in `business`.

For a recurring task, the `POST` also needs `{ recurring: true, date: "YYYY-MM-DD" }`.

⚠ **READ THE VERIFY RESPONSE CORRECTLY — `/api/task-checks` returns `checked` as an ARRAY, not a
dict of id→bool** (measured 2026-08-28). The payload is
`{"checked": ["money::…", …], "log": {…}, "checkedAt": {"money::…": "YYYY-MM-DD"}}`. A verifier that
does `d.get('checks', d)` and iterates keys finds nothing and reports a perfectly good write as
failed — which cost a needless duplicate POST here. Check membership with
`tgt in d['checked']`, and read `d['checkedAt'][tgt]` for the date. **A re-POST of an
already-checked id is harmless** (it does not duplicate — the array still held exactly one copy), so
a false "not found" leads to a wasted call rather than corruption, but it will also send you hunting
for a text-mismatch that isn't there.

**Verify, don't trust the 200:** reload the dashboard (or re-read `/api/task-checks`) and confirm the row is struck through — a 200 only means the write was accepted, not that the id matched a task. If no matching task exists (it predates the rule, or Dan deleted it), say so rather than inventing one. Note `/api/todos` reads are eventually consistent — re-check after a beat before concluding a write failed.

## Adding a Rule-8 handoff task

Whenever a handoff document is created for work not yet executed, add a Key task so it doesn't get forgotten: fetch `GET /api/todos`, append to the **`business`** list:

```json
{ "text": "Execute handoff: <short description>", "priority": "key", "why": "<filename> — created but not yet run", "addedAt": "YYYY-MM-DD" }
```

then `POST /api/todos` the updated object back and re-read to confirm it persisted. If the handoff gets fully executed in the same session it was created, check it off instead of leaving it dangling.

**`POST /api/todos` replaces the whole file and has server-side guards** (recurring tasks are restored, 3+ deletions are refused with a 409, day-schedules are restored) — always write back the freshly fetched object with your one change, never a stale copy. Intentional deletions need an `allowDeletes` array naming the task.

## Standing authorization

Reading and writing `/api/todos`, `/api/task-checks` and `/api/plan` is covered by a standing authorization in `AGENTS.md` — no per-action confirmation needed. It does not permit deleting tasks Dan created or rewriting task text he wrote.
