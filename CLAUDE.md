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

- Before doing project work, inspect the current Git state. `AI_COORDINATION.md` is already loaded above.
- **`AI_COORDINATION.md` is a STATUS BOARD, not a log — keep it short.** It is loaded into every message in this project, so every line costs context in every session. Record only what is open: the task, who is blocked, and the exact next action, in a few factual sentences. Never a transcript.
- **A finished, approved task's entry gets DELETED, not marked complete.** Before deleting it, put anything durable where it belongs: techniques and traps go in the relevant skill, code history in git, unexecuted work in `Handoffs/`, lasting facts in memory, standing rules in `AGENTS.md`. The table at the top of `AI_COORDINATION.md` is the routing guide.
- **Re-read `AI_COORDINATION.md` from disk before finishing a task, not just before starting one.** The copy in context is a snapshot from session start and a concurrent session may have written to it; edit only your own entry. This is how the dashboard check-off rule got missed on 2026-07-29, and how an entry got clobbered on 2026-09-01.
- Only one session owns implementation of a task at a time. Don't continue or overwrite another session's unfinished work without an explicit handoff or a review request.
- Follow the delivery, deployment, security, and communication requirements imported from `AGENTS.md`.

## Check the task off on the Victory Dashboard when you finish it

Finishing a task means checking it off at `absbyai.com/dashboard` in the same session — Dan should not have to click it himself; an unchecked task reads as unfinished work. Do this after the change is committed, pushed, deployed and verified, as the last step of the task. Same rule for adding a Rule-8 Key task whenever a handoff doc is created. **Invoke the `/dashboard-tasks` skill for the mechanics** (gated endpoints, `X-Dash-Key` auth, the id format and the `money`-vs-`business` trap) — do not work these endpoints from memory.

## Secrets and env vars — NEVER ask Dan to fetch these (Dan's instruction, 2026-08-18)

Get them yourself: `~/.npm-global/bin/railway variables --service abs-by-ai --kv` (CLI authenticated, project linked; `--service` is required — without it you read the Postgres service). Local cache: `~/.absbyai-secrets.env` (0600, outside the repo) — grep/source it, refresh from the CLI when a key looks stale. `DATABASE_URL` is in there (direct prod Postgres; reversible row updates fall under bias-toward-action, destructive deletions of real user data still require asking). Never commit the file or paste key values into chat, artifacts, or the coordination file. Only ask Dan for a secret that genuinely doesn't exist anywhere yet.

## Voice input (Wispr Flow)

Most of Dan's prompts are dictated through Wispr Flow, not typed. If an instruction contains a word or phrase that doesn't quite make sense in context, consider whether it's a mis-transcription of a phonetically similar word or product/technical term before acting on it literally. If a misheard reading would change what you do in a meaningful or risky way, ask for clarification rather than guessing.
