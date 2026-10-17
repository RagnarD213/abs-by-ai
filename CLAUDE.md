# Claude Code Instructions

@AGENTS.md
@AI_COORDINATION.md

**Long-form releases (Dan, 2026-10-17):** Two a week, Sunday and Wednesday 9 AM America/Chicago, one per day, per the dated calendar in `Docs/LONGFORM_RELEASE_CALENDAR.md` and the rule in `AGENTS.md`. Never another weekday. YouTube publishes first; Facebook, Instagram and TikTok follow the next day (Monday 9 AM, or Thursday noon after a Wednesday release) once the YouTube post is verified public.

**Memory entries are in `Docs/memory/` (index: `Docs/memory/MEMORY.md`).** When a skill or rule says "memory `name`", read `Docs/memory/name.md`. Local sessions also have the same entries in the auto-memory folder; the repo copy is the cloud copy. A name with no file there is private on purpose: do not guess its content.
After writing or changing a memory entry locally, run `scripts/sync-memory-to-repo.sh`, then push `Docs/memory`. In a cloud session, write the entry straight into `Docs/memory/` and add its index line.

## Bias toward action (Dan's standing instruction, 2026-08-06)

Do not ask permission for anything reversible. Dan explicitly prefers aggressive autonomous action with occasional fixable mistakes over being asked to approve things.

- The test is **reversibility**, not confidence. Code changes, deploys, config edits, dashboard writes, test batches within the $10/session spend cap, and anything under a standing authorization in `AGENTS.md`: do it, verify it, then report what was done. Never end a turn with "Shall I…?" for work in this category.
- Ambiguous detail mid-task? Pick the sensible default, note the choice, keep moving.
- Give one recommendation and execute it — not a menu of options.
- Still ask first ONLY for: irreversible/destructive actions (deleting user data, DNS record deletions, canceling subscriptions), spend beyond the standing caps, sending email to customers or the list, formal Apple/Google certifications (Dan's personal declarations), and credentials (a hard platform restriction on Claude, not Dan's preference — Claude cannot type passwords/payment details, so Dan has to enter them; do not frame this as Dan's rule).

### Exception: brainstorming / prioritization sessions (Dan's instruction, 2026-08-11)

When Dan asks a "what should we work on" / "what should I use my limit for" / "help me prioritize" type of question, the deliverable is the **prioritized recommendation itself — do NOT start executing the recommended work in that session.** Dan executes handoffs and recommended tasks in separate sessions on purpose, to save tokens and keep each execution session's context window clean. In a brainstorming session: read whatever is needed to ground the recommendation (board, coordination file, handoffs), give the priorities with reasoning, and stop. Bias toward action still applies fully once a session IS the execution session.

## End every task with the two wrap-up boxes (Dan, 2026-10-16)

The `task-wrapup` mod (`~/.claude/mods/task-wrapup`, on for every session on this Mac) adds this rule; it is written here too for sessions that do not load it (cloud sessions, a session opened before a mod change). Whenever a reply finishes a task, finishes a work phase, or stops to wait for Dan, end it with these two boxes, last, nothing after them:

> **What was done**
> One or two short plain-language sentences. No file paths, no jargon.

> **Your next steps**
> 1. Each thing Dan must do, starting with a verb, with the clickable link (review page, thumbnail page, Doc, Drive folder), saying whether he has reviewed it yet.

At most 4 steps. Video edit: the first step is the review page link; setup task: the thumbnail choices. A handoff step says fire now or after review, with its starter prompt above the boxes. Nothing to do: the only step is "Nothing. This is done." Skip the boxes only for a quick question-and-answer reply. Dan: *"make all tasks going forward use that modification."*

**Enforcement (2026-10-16):** the prompt rule alone was skipped in long or older sessions, so a Stop hook (`~/.claude/hooks/wrapup-check.py`, registered in `~/.claude/settings.json`) now sends Claude back to add the boxes when a turn that used tools ends without them. Takes effect in sessions opened after this date.

## Suggested-task chips: plain language only (Dan, 2026-10-16)

When you flag a side task with `spawn_task`, Dan sees a card with a title and a short description (the `tldr` field), and the full `prompt` only on hover. He cannot read the technical version and was asking in chat "what is this?" every time.

- **`title`:** plain words a non-coder understands (e.g. "Fix a check that wrongly fails very short ads"), never function names, file names or flags.
- **`tldr`:** two short sentences, no jargon, no file paths, no code, no numbers like "0.9 s" unless he would recognize them. Sentence 1: what went wrong or what you noticed, in everyday words. Sentence 2: what the new session will do and why it matters to him. If a technical term is unavoidable, translate it in the same sentence.
- **`prompt`:** stays full and technical (paths, functions, rules, tests). It is for the next Claude, not for Dan.
- Test before sending: would a smart friend who does not code understand the card without asking anything? If not, rewrite it.
- Example: title "Fix a check that wrongly fails very short ads". tldr "While finishing the RA-12 ad, the automatic quality check said the AI label was missing on a very short card, but the label was there. The new session will fix the check so it stops raising false alarms."

## Shared-workflow requirements

- Before doing project work, inspect the current Git state. `AI_COORDINATION.md` is already loaded above.
- **`AI_COORDINATION.md` is a STATUS BOARD, not a log — keep it short.** It is loaded into every message in this project, so every line costs context in every session. Record only what is open: the task, who is blocked, and the exact next action, in a few factual sentences. Never a transcript.
- **Size budget: `AI_COORDINATION.md` stays under 2,500 words.** Each bold-titled entry is at most 80 words and dated. Run `scripts/board-check.sh` after editing the board; compress before finishing if it fails. The hook fails only the session that edited the board; trim your own entry, never another session's.
- **The board holds open coordination only (Dan, 2026-10-16).** Decisions only Dan can make go in `Docs/DAN_DECISIONS.md`; unexecuted handoffs are listed only in the OPEN section of `Handoffs/README.md`. Neither goes on the board.
- Report finished work in chat and the morning brief, never as FYI on the board. Follow `Docs/BOARD_MORNING_MAINTENANCE.md` for aging and weekly cleanup.
- **A finished, approved task's entry gets DELETED, not marked complete.** Before deleting it, put anything durable where it belongs: techniques and traps go in the relevant skill, code history in git, unexecuted work in `Handoffs/` + `Handoffs/README.md`, Dan's open decisions in `Docs/DAN_DECISIONS.md`, lasting facts in memory, standing rules in `AGENTS.md`. The table at the top of `AI_COORDINATION.md` is the routing guide.
- **Re-read `AI_COORDINATION.md` from disk before finishing a task, not just before starting one.** The copy in context is a snapshot from session start and a concurrent session may have written to it; edit only your own entry. This is how the dashboard check-off rule got missed on 2026-07-29, and how an entry got clobbered on 2026-09-01.
- Only one session owns implementation of a task at a time. Don't continue or overwrite another session's unfinished work without an explicit handoff or a review request.
- Follow the delivery, deployment, security, and communication requirements imported from `AGENTS.md`.
- **Shared files (Dan, 2026-10-05):** push a shared file with `safe-push.sh` the moment you edit it. If `safe-push.sh` stops on files older than 2 hours, re-run it with `--adopt-stale`; if a file is newer, its owner is live, so post the board note and retry at the end of the task. Full rule: `AGENTS.md`, "Delivery and deployment".

## Check the task off on the Victory Dashboard when you finish it

**PAUSED 2026-10-05 (Dan): do not read, write or check off anything on the Victory Dashboard.** Dan called it unusable and is rebuilding it with Codex. Until he says the new one is ready, skip every dashboard step below and report finished work in chat only.

Finishing a task means checking it off at `absbyai.com/dashboard` in the same session: Dan should not have to click it himself; an unchecked task reads as unfinished work. Do this after the change is committed, pushed, deployed and verified, as the last step of the task. **Do NOT add a dashboard row for a new handoff doc unless Dan explicitly asks for one** (Dan's rule, 2026-09-08: the board had drowned in executed handoffs). Record an unexecuted handoff only in the OPEN section of `Handoffs/README.md` (the board just points there). When Dan says to fire one, it goes on the dashboard's **Handoffs to fire** list (the `handoffs` list, cap 7, delete when run: mechanics in `/dashboard-tasks`), never as a Money Key task. **Invoke the `/dashboard-tasks` skill for the mechanics** (gated endpoints, `X-Dash-Key` auth, the id format and the `money`-vs-`business` trap); do not work these endpoints from memory.

## Secrets and env vars — NEVER ask Dan to fetch these (Dan's instruction, 2026-08-18)

Get them yourself: `~/.npm-global/bin/railway variables --service abs-by-ai --kv` (CLI authenticated, project linked; `--service` is required — without it you read the Postgres service). Local cache: `~/.absbyai-secrets.env` (0600, outside the repo) — grep/source it, refresh from the CLI when a key looks stale. `DATABASE_URL` is in there (direct prod Postgres; reversible row updates fall under bias-toward-action, destructive deletions of real user data still require asking). Never commit the file or paste key values into chat, artifacts, or the coordination file. Only ask Dan for a secret that genuinely doesn't exist anywhere yet.

## Voice input (Wispr Flow)

Most of Dan's prompts are dictated through Wispr Flow, not typed. If an instruction contains a word or phrase that doesn't quite make sense in context, consider whether it's a mis-transcription of a phonetically similar word or product/technical term before acting on it literally. If a misheard reading would change what you do in a meaningful or risky way, ask for clarification rather than guessing.
