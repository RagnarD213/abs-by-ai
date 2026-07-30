# Claude Code Instructions

@AGENTS.md
@AI_COORDINATION.md

## Shared-workflow requirements

- Before doing project work, read `AI_COORDINATION.md` and inspect the current Git state.
- If starting a new task, fill in the active-task section and set **Owner** to `Claude Code`.
- If the active task is owned by Codex, do not make overlapping implementation changes unless the user asks you to review the work or the document records a handoff to Claude Code.
- Keep the coordination document concise and factual. Record results, decisions needed, verification, and the exact next action—not the conversation transcript.
- Before stopping or handing work to Codex, update `AI_COORDINATION.md` so Codex can continue without needing access to the Claude conversation.
- **Re-read `AI_COORDINATION.md` from disk before finishing a task, not just before starting one.** The copy in context is a snapshot from session start; the other assistant may have added a working rule since. This is how the dashboard check-off rule got missed on 2026-07-29.
- Follow the delivery, deployment, security, and communication requirements imported from `AGENTS.md`.

## Check the task off on the Victory Dashboard when you finish it

Finishing a task means checking it off at `absbyai.com/dashboard` in the same session. Dan should not have to click it himself — an unchecked task reads as unfinished work. Do this after the change is committed, pushed, deployed and verified, as the last step of the task.

```bash
# 1. Find the task's exact text.  Stored lists are business / health / personal.
curl -s https://absbyai.com/api/todos | python3 -m json.tool
# 2. Check it off.  The id is "<displayKey>::<exact text>" — see the mapping note below.
curl -s -X POST https://absbyai.com/api/task-checks -H 'Content-Type: application/json' \
  -d '{"id":"money::Execute handoff: Close locked-image leak on paywall","checked":true}'
```

Three things that are easy to get wrong here, all verified on 2026-07-29:

- **Done state lives in `/api/task-checks`, not in `todos.json`.** Setting a `done` field on the todo object does nothing — no surface reads it. `POST /api/task-checks` with `{ id, checked: true }` is the only mechanism.
- **The `business` list is displayed as `money`, and check ids use the DISPLAY key.** `dashboard.html` merges the stored `business` list into `todosState.money` (line ~1615) and writes it back as `business` (~2111), while `taskCheckId()` builds `<displayKey>::<text>`. So a money-column task is `money::…`, never `business::…`. `health` and `personal` are the same in both.
- **The text must match exactly**, including punctuation — the id is the raw text. Fetch it, don't retype it.

For a recurring task, `POST` also needs `{ recurring: true, date: "YYYY-MM-DD" }`. Then reload the dashboard and confirm the row is struck through — a 200 from the endpoint is not proof the right id was used. If no matching task exists, say so rather than inventing one.

## Voice input (Wispr Flow)

Most of Dan's prompts are dictated through Wispr Flow, not typed. If an instruction contains a word or phrase that doesn't quite make sense in context, consider whether it's a mis-transcription of a phonetically similar word or product/technical term before acting on it literally. If a misheard reading would change what you do in a meaningful or risky way, ask for clarification rather than guessing.
