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
- **Size budget: `AI_COORDINATION.md` stays under 2,500 words.** Each bold-titled entry is at most 80 words and dated. Run `scripts/board-check.sh` after editing the board; compress before finishing if it fails.
- Report finished work in chat and the morning brief, never as FYI on the board. Follow `Docs/BOARD_MORNING_MAINTENANCE.md` for aging and weekly cleanup.
- **A finished, approved task's entry gets DELETED, not marked complete.** Before deleting it, put anything durable where it belongs: techniques and traps go in the relevant skill, code history in git, unexecuted work in `Handoffs/`, lasting facts in memory, standing rules in `AGENTS.md`. The table at the top of `AI_COORDINATION.md` is the routing guide.
- **Re-read `AI_COORDINATION.md` from disk before finishing a task, not just before starting one.** The copy in context is a snapshot from session start and a concurrent session may have written to it; edit only your own entry. This is how the dashboard check-off rule got missed on 2026-07-29, and how an entry got clobbered on 2026-09-01.
- Only one session owns implementation of a task at a time. Don't continue or overwrite another session's unfinished work without an explicit handoff or a review request.
- Follow the delivery, deployment, security, and communication requirements imported from `AGENTS.md`.

## Check the task off on the Victory Dashboard when you finish it

Finishing a task means checking it off at `absbyai.com/dashboard` in the same session — Dan should not have to click it himself; an unchecked task reads as unfinished work. Do this after the change is committed, pushed, deployed and verified, as the last step of the task. **Do NOT add a dashboard row for a new handoff doc unless Dan explicitly asks for one** (Dan's rule, 2026-09-08 — the board had drowned in executed handoffs). Record an unexecuted handoff in the HANDOFFS section of `AI_COORDINATION.md` and in `Handoffs/README.md`. When Dan says to fire one, it goes on the dashboard's **Handoffs to fire** list (the `handoffs` list, cap 7, delete when run — mechanics in `/dashboard-tasks`), never as a Money Key task. **Invoke the `/dashboard-tasks` skill for the mechanics** (gated endpoints, `X-Dash-Key` auth, the id format and the `money`-vs-`business` trap) — do not work these endpoints from memory.

## Secrets and env vars — NEVER ask Dan to fetch these (Dan's instruction, 2026-08-18)

Get them yourself: `~/.npm-global/bin/railway variables --service abs-by-ai --kv` (CLI authenticated, project linked; `--service` is required — without it you read the Postgres service). Local cache: `~/.absbyai-secrets.env` (0600, outside the repo) — grep/source it, refresh from the CLI when a key looks stale. `DATABASE_URL` is in there (direct prod Postgres; reversible row updates fall under bias-toward-action, destructive deletions of real user data still require asking). Never commit the file or paste key values into chat, artifacts, or the coordination file. Only ask Dan for a secret that genuinely doesn't exist anywhere yet.

## Voice input (Wispr Flow)

Most of Dan's prompts are dictated through Wispr Flow, not typed. If an instruction contains a word or phrase that doesn't quite make sense in context, consider whether it's a mis-transcription of a phonetically similar word or product/technical term before acting on it literally. If a misheard reading would change what you do in a meaningful or risky way, ask for clarification rather than guessing.

## Video review refinements — C1652 R3 (Dan, 2026-09-17)

- **Clip variety means different visible content, not merely different IDs or trims.** Do not reuse stock from essentially the same scene/shoot with the same actors or actresses, even from a different camera angle. Doctor inserts within one video need distinct casts and settings. Prefer suitable Pexels/known-rights footage; use authorized AI generation if no suitable distinct clip exists.
- **Exercise illustrations must vary the exercise.** For Dan demonstrating daily exercise, use ab wheel plus toe touches or kettlebell deadlifts, not repeated ab-wheel footage. This includes similar excerpts from one source video. Dan remains the same person; the exercise action must differ. Necessary repetitions inside an actual exercise teaching demonstration are a different purpose.
- **No added camera movement in horizontal16:9 presenter footage.** Do not pan, drift, track or recenter just because Dan shifts slightly. Keep a fixed composition within the shot; preserve approved framing sizes and deliberate cuts unless separately rejected. Check rendered footage, not just a fixed-center setting.
- **Requested AI narrative clips require actual motion.** A static frame, start/end montage, slow image pan or brief motion fragment followed by a held endpoint is not a completed clip. Generate and validate the intended motion from approved assets; do not ask again for unchanged approved frames. This does not prohibit real photo displays or specifically approved scientific still illustrations.
- **Three-photo screen template:** use three vertical real studio portraits with distinct poses and consistent presentation proportions; plural disclosure “Real pictures of me — not AI-generated,” clear of faces/abs. Save the tested layout for reuse.
- **Organic graphics:** imitate Muhammad’s actual moving graphics, including lower-thirds and full-screen treatments. Use self-contained titles that name the topic. Specific approvals with limited requested edits take precedence over a general redesign; for C1652's Zepbound/stakes lists, enlarge text as requested and preserve the otherwise approved panel design.

## Horizontal footage stays completely static — Dan, 2026-09-17

- **No added camera movement or recentering on Dan in horizontal/16:9 videos.** No tracking, pan, drift, animated crop or zoom to follow or center him. Choose a fixed composition for each shot and leave it fixed. This supersedes earlier horizontal exceptions for approaching the frame edge; tracking is only for square/vertical layouts when actually needed.
- Ordinary cuts between fixed compositions remain editing cuts, not camera motion. Graphics may animate without moving the presenter picture beneath them. Check actual rendered background landmarks: a fixed-X setting alone does not prove a static picture. If the camera source itself drifts, resolve that in source choice/stabilization rather than silently claiming the delivered picture is static.
- Dan approved C1652 R4 as good enough to ship despite a small remaining movement near1:09. Do not reopen that accepted film to enforce the future rule. Its approved master is SHA256 `eace1bdbb9f7a16fadff8bb2d2e80812ea4e777cf413a1e06575527f95d64f44`.
- C1652’s Zepbound text size is approved. Dan would prefer a third benefit, “Makes you serious about fat loss,” in a future relevant treatment; he accepted the existing two-row graphic in this final film. Do not expand its content without speech/timing context in future work.
