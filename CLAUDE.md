# Claude Code Instructions

@AGENTS.md
@AI_COORDINATION.md

## Bias toward action (Dan's standing instruction, 2026-08-06)

Do not ask permission for anything reversible. Dan explicitly prefers aggressive autonomous action with occasional fixable mistakes over being asked to approve things.

- The test is **reversibility**, not confidence. Code changes, deploys, config edits, dashboard writes, test batches within the $10/session spend cap, and anything under a standing authorization in `AGENTS.md`: do it, verify it, then report what was done. Never end a turn with "Shall I…?" for work in this category.
- Ambiguous detail mid-task? Pick the sensible default, note the choice, keep moving.
- Give one recommendation and execute it — not a menu of options.
- Still ask first ONLY for: irreversible/destructive actions (deleting user data, DNS record deletions, canceling subscriptions), spend beyond the standing caps, sending email to customers or the list, formal Apple/Google certifications (Dan's personal declarations), and credentials (a hard platform restriction on Claude, not Dan's preference — Claude cannot type passwords/payment details, so Dan has to enter them; do not frame this as Dan's rule).

### Exception: brainstorming / prioritization sessions (Dan's instruction, 2026-08-11)

When Dan asks a "what should we work on" / "what should I use my limit for" / "help me prioritize" type of question, the deliverable is the **prioritized recommendation itself — do NOT start executing the recommended work in that session.** Dan executes handoffs and recommended tasks in separate sessions on purpose, to save tokens and keep each execution session's context window clean. In a brainstorming session: read whatever is needed to ground the recommendation (board, coordination file, handoffs), give the priorities with reasoning, and stop. Bias toward action still applies fully once a session IS the execution session.

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
# 1. Find the task's exact text.  Stored lists are business / health / personal / assistant.
curl -s https://absbyai.com/api/todos | python3 -m json.tool
# 2. Check it off.  The id is "<displayKey>::<exact text>" — see the mapping note below.
curl -s -X POST https://absbyai.com/api/task-checks -H 'Content-Type: application/json' \
  -d '{"id":"money::Execute handoff: Close locked-image leak on paywall","checked":true}'
```

Three things that are easy to get wrong here, all verified on 2026-07-29:

- **Done state lives in `/api/task-checks`, not in `todos.json`.** Setting a `done` field on the todo object does nothing — no surface reads it. `POST /api/task-checks` with `{ id, checked: true }` is the only mechanism.
- **The `business` list is displayed as `money`, and check ids use the DISPLAY key.** `dashboard.html` merges the stored `business` list into `todosState.money` (line ~1615) and writes it back as `business` (~2111), while `taskCheckId()` builds `<displayKey>::<text>`. So a money-column task is `money::…`, never `business::…`. `health`, `personal` and `assistant` are the same in both.

- **`assistant` is delegated work — Dan's personal assistant's list, not Dan's** (added 2026-08-08). It renders as its own "Assistant Tasks" card in the Health column and is mirrored to `absbyai.com/assistant`, an unauthenticated page the assistant uses. It is deliberately excluded from the Work Session Focus band's auto-population, so **do not put agent work orders or Dan's own tasks in it**, and do not add Rule-8 handoff tasks there — those still go in `business`.
- **The text must match exactly**, including punctuation — the id is the raw text. Fetch it, don't retype it.

For a recurring task, `POST` also needs `{ recurring: true, date: "YYYY-MM-DD" }`. Then reload the dashboard and confirm the row is struck through — a 200 from the endpoint is not proof the right id was used. If no matching task exists, say so rather than inventing one.

## Secrets and env vars — NEVER ask Dan to fetch these (added 2026-08-18, Dan's instruction)

Dan explicitly eliminated the "go into Railway, grab the variable, paste it" loop. Get secrets yourself:

1. **Railway CLI is installed and authenticated**: `~/.npm-global/bin/railway` (not on default PATH — use the full path or export `PATH="$HOME/.npm-global/bin:$PATH"`). The project is already linked. `railway variables --kv` prints every production variable; auth auto-refreshes.
2. **Local cache**: `~/.absbyai-secrets.env` (0600, outside the repo) holds a snapshot of all prod variables. Source it or grep it. Refresh it with `railway variables --kv > ~/.absbyai-secrets.env && chmod 600 ~/.absbyai-secrets.env` whenever a key looks stale.
3. **`DATABASE_URL` is in there** — direct production Postgres access. This replaces the old "needs Dan's admin login" blocker for comp/beta grants and data inspection. Reversible row updates (membership_status grants, test-account cleanup) fall under bias-toward-action; destructive deletions of real user data still require asking.
4. Never commit the secrets file or paste full key values into chat, artifacts, or the coordination file.

Only ask Dan for a secret when it genuinely does not exist yet anywhere (a brand-new provider account) — and then have him paste it once so it can be added to Railway and the cache, never per-session.

## Voice input (Wispr Flow)

Most of Dan's prompts are dictated through Wispr Flow, not typed. If an instruction contains a word or phrase that doesn't quite make sense in context, consider whether it's a mis-transcription of a phonetically similar word or product/technical term before acting on it literally. If a misheard reading would change what you do in a meaningful or risky way, ask for clarification rather than guessing.
