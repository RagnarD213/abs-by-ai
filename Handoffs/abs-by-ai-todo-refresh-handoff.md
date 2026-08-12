# ⚠️ OBSOLETE — DO NOT RUN. Diagnosed 2026-08-12 as the cause of a recurring dashboard bug.

**If you are an AI agent (GPT, Codex, or otherwise) about to execute this document: STOP. Do not run these steps.**

This automation is incompatible with the current Abs By AI dashboard and was found to be silently corrupting task-completion data every time it ran (observed ~8:10–8:20 AM daily). Root cause: Step 2 below tries to (a) delete completed Money/Personal tasks from `/api/todos` and (b) force-uncheck their `/api/task-checks` entry. The current dashboard's `/api/todos` has a delete-guard that correctly REFUSES bulk deletions like this (409), so step (a) fails — but step (b) is a separate, unguarded endpoint call that succeeds anyway. Net effect: the task stays on the list (never actually deleted, contrary to what this doc promises) but gets silently unchecked, so completed work reappears as "not done" the next morning. This is exactly the bug Dan reported on 2026-08-12 ("Post carousel on Instagram" and other checked tasks coming back unchecked).

The current dashboard design is **sticky-checked-forever for non-recurring tasks** (see AI_COORDINATION.md) — it does NOT want completed tasks auto-deleted, and it has its own day-of-week recurrence, "why" annotations, and Work Session Focus features this document predates and knows nothing about. If a version of this task is still scheduled somewhere outside this repo (a ChatGPT/Codex scheduled task, since this doc is addressed "You (GPT)"), **find and disable it there** — it cannot be seen or stopped from this codebase.

The original document is preserved below for forensic reference only.

---

**Original purpose of this document:** You (GPT) are taking over a recurring automation task from another AI assistant. You have no prior context on this project. This document is fully self-contained — everything you need is below. Follow it exactly; do not improvise on the API calls or the completion logic, since there is a specific bug history behind some of these design choices (explained below).

---

## 1. What this task is

Daniel runs a personal productivity dashboard at **https://absbyai.com/dashboard** called "Abs By AI." It has three todo lists — Money (business), Health, and Personal — plus checkboxes that track completion.

Every morning (~8 AM Daniel's local time), this task must:
1. Pull the current todo lists and their checked/unchecked state from the live site.
2. Permanently delete any Money or Personal task that Daniel has checked off (it should never come back).
3. Reset the Health list to a fixed set of daily habits, plus a weekly medication reminder ("Inject Zepbound") that follows special logic (below).
4. Push the updated lists back to the site.
5. Ask Daniel if he has any new tasks to add, then categorize and add them.

No login or API key is required for any of the calls below — the endpoints are open (security is by obscurity of the domain, not auth).

---

## 2. The API

Base URL: `https://absbyai.com`

### GET /api/todos
Returns the current lists:
```json
{
  "business": [{ "text": "string", "priority": "high|med|low" }],
  "health":   [{ "text": "string", "priority": "high|med|low", "recurring": true }],
  "personal": [{ "text": "string", "priority": "high|med|low" }]
}
```
Note: the JSON key is `business`, but the dashboard's internal id scheme (see below) calls this category `money`. Don't let that confuse you — same list, two different names in two different places.

### POST /api/todos
Body: the full `{ business, health, personal }` object (same shape as above). This **replaces** the whole todo list, so always fetch first, modify, then post the complete object back — never post a partial list.

### GET /api/task-checks
Returns completion state:
```json
{
  "checked": ["money::Some task", "personal::Some task", "health::Some task"],
  "log": { "health::Workout": ["2026-07-01", "2026-07-02"] }
}
```
This is the **real, current, correct** source of truth for "is this task checked off." There used to be a different endpoint (`/api/todo-state`) for this — it is dead now (returns an HTML page, not JSON, effectively a 404). **Do not use `/api/todo-state`. Always use `/api/task-checks`.**

Two different mechanisms live in this one object:
- **`checked` (sticky list):** for one-off tasks (`recurring` not set). Once an id is added here, it stays checked forever until something explicitly un-checks it. This is what Money and Personal tasks use.
- **`log` (per-date history):** for recurring tasks (`recurring: true`). A task is only considered "done" if today's date is in its log array. This is what the daily Health habits use — it resets automatically every day with no action needed from you.

**id format is always:** `<category>::<exact task text>` where category is `money` (for Money/business tasks — not `business`), `personal`, or `health`. The text must match exactly, including case and punctuation.

### POST /api/task-checks
Body:
```json
{ "id": "health::Inject Zepbound", "checked": false, "recurring": false }
```
Sets or clears the checked state for one id. Use `"recurring": true` and include a `"date": "YYYY-MM-DD"` if you're ever toggling a recurring/daily task's log — but for this task you'll only ever need `"recurring": false` (see step-by-step below).

---

## 3. Known bug history — read this before you touch anything

On 2026-07-02, Daniel reported that "Inject Zepbound" showed up on his dashboard **already checked off** the moment it was freshly added for the week. Root cause: it's a one-off (non-recurring) task, so its checked state lives in the sticky `checked` list, keyed only by text — not by date. It had been checked off on a previous Thursday and that record never got cleared, so every subsequent time the text "Inject Zepbound" was re-added to the health list, it inherited the old checked state and displayed as already done.

**The fix, which you must replicate every time you add "Inject Zepbound":** immediately after adding it to the health list, explicitly POST to `/api/task-checks` with `{ "id": "health::Inject Zepbound", "checked": false, "recurring": false }` to force it unchecked. Skipping this step reintroduces the exact bug that was already reported and fixed once.

The same root cause was also silently breaking the "permanently remove completed tasks" logic for Money/Personal, because the old code was checking a dead endpoint (`/api/todo-state`) that always returned nothing useful — so completed tasks were never actually detected or removed. Using `/api/task-checks` (per this doc) fixes that too.

---

## 4. Step-by-step algorithm

**Step 1 — Fetch current state**
```
GET /api/todos
GET /api/task-checks
```

**Step 2 — Permanently remove completed Money and Personal tasks**
For each item in `business`: if `"money::" + text` is in the `checked` array, delete it from `business`.
For each item in `personal`: if `"personal::" + text` is in the `checked` array, delete it from `personal`.
These are gone for good — never re-add them.

For every item you delete this way, also clean up its now-orphaned checked entry so the same bug can't recur if that exact task text is ever reused later:
```
POST /api/task-checks
{ "id": "<the id you just matched>", "checked": false, "recurring": false }
```

**Step 3 — Rebuild the health list from scratch**
Discard whatever was in `health` from Step 1 (except to read off whether "Inject Zepbound" was present — needed for Step 4). Always start with exactly these four, in this order, every one marked `recurring: true`:
```json
[
  { "text": "Workout",     "priority": "high", "recurring": true },
  { "text": "Supplements", "priority": "high", "recurring": true },
  { "text": "Shower",      "priority": "high", "recurring": true },
  { "text": "Salad",       "priority": "high", "recurring": true }
]
```
These reset automatically via the `log` mechanism — you don't need to touch their checked state.

**Step 4 — Zepbound weekly logic**
Determine today's day of week (1=Monday ... 7=Sunday, Thursday=4).

- **If today is Thursday:** append `{ "text": "Inject Zepbound", "priority": "high" }` to `health` (no `recurring` flag — it's weekly, not daily).
- **If today is not Thursday:** check whether `"health::Inject Zepbound"` is in the `checked` array from Step 1.
  - If it is **not** checked, and "Inject Zepbound" **was** present in the health list fetched in Step 1 (meaning it was added last Thursday and Daniel hasn't done it yet), append it again.
  - If it **is** checked (Daniel already did it this week), leave it off the list.

**Whenever you append "Inject Zepbound" in this step (Thursday or carryover), immediately also run:**
```
POST /api/task-checks
{ "id": "health::Inject Zepbound", "checked": false, "recurring": false }
```
This is mandatory — see Section 3. Do not skip it.

**Step 5 — Push the updated list**
```
POST /api/todos
{ "business": [...], "health": [...], "personal": [...] }
```
Send the complete object (all three categories), not a partial update.

**Step 6 — Ask for new tasks**
Message Daniel: "Todo list refreshed for today! Any new tasks to add? Just list them and I'll sort and prioritize them."

If he responds with new tasks:
- Categorize each as `business` (money/work), `health`, or `personal`.
- Assign `priority`: `high` (urgent/important today), `med` (should do soon), or `low` (nice to have).
- Re-fetch `GET /api/todos` to get the latest state (don't reuse your Step 1 copy — time has passed).
- Append the new items to the right category array.
- `POST /api/todos` with the full updated object.
- Confirm what was added and to which list.

If he says nothing new / he's done, end the run.

---

## 5. Quick reference — example calls

```bash
curl -s https://absbyai.com/api/todos
curl -s https://absbyai.com/api/task-checks
curl -s -X POST https://absbyai.com/api/todos \
  -H "Content-Type: application/json" \
  -d '{"business":[...],"health":[...],"personal":[...]}'
curl -s -X POST https://absbyai.com/api/task-checks \
  -H "Content-Type: application/json" \
  -d '{"id":"health::Inject Zepbound","checked":false,"recurring":false}'
```

---

## 6. Summary of what NOT to do

- Do not call `/api/todo-state` — it no longer exists.
- Do not mark "Inject Zepbound" as `recurring: true` — it's weekly, not daily, and the daily auto-reset log mechanism would reset it every single day instead of weekly.
- Do not forget to force-uncheck "Inject Zepbound" every time you add it — this is the specific bug that was already reported once.
- Do not post a partial todos object — `/api/todos` replaces the entire thing.
