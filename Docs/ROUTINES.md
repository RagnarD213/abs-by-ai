# Routines

## Silent checks and owner handoff in local routines (Dan, 2026-10-28)

Local routines and continuations follow `AGENTS.md` and `.claude/skills/_shared/VIDEO-RULES.md`: enter **Start silent checks** (or `?review_mode=automation`) before testing managed players, verify mute throughout playback/source changes/recovery, then use **Finish checks for owner**. That handoff cancels stale callbacks, pauses and verifies every player before enabling audio, and never starts playback. Preserve the chosen volume and normal controls. A failure stays muted and is reported. Dan's next deliberate Play includes sound; later automated testing must re-enter silent mode. The global local-Codex `~/.codex/AGENTS.md` records the same workflow, and Claude project tasks import project `AGENTS.md` through `CLAUDE.md`.

Use offline decoding, measurements or supported non-speaker model/file inspection; never call a silent/numerical check an audible listen. Playback readiness is not QA or content approval. Do not change Mac/Wispr Flow/microphone/routing/media settings. Existing independent tasks must read/apply the update and open pages must reload; no app-wide preference or automatic prompt update is claimed. External/native players use the same pause-verified handoff where supported.

## Abs By AI morning brief

Status: **local chat schedule enabled October 25, 2026**. Daily at 07:00 America/Chicago, ready target 07:30, using the existing full-access local chat. This replaces cloud execution after its private-folder permission failure. The Mac must be online with the Codex app running. The first automatic publication is unproven until a scheduled run passes independent storage and live-page checks.

Runbook: `Docs/MORNING_BRIEF_LOCAL.md`. Main code runs from `/Users/danielrose/Projects/Claude/Projects/Abs By AI`. Social state is `/Users/danielrose/Projects/Codex/2026-10-08/task-2/private`; brief inputs, signing key and receipts are `/Users/danielrose/Projects/Codex/2026-09-30/task/.private-brief-proof`. No old launcher, cloud child task, Documents or iCloud alias. Victory Dashboard reads remain paused; `collect_local.py` skips them before any request. Trello remains deferred.

The writer collects fresh connected Gmail and Calendar alongside planning, Ads, site metrics and read-only social inventory. It publishes a new dated edition with one grounded first action, explicitly unknown business outcomes, source coverage and the last verified image with its real date. Follow `Docs/MORNING_BRIEF_INPUTS.md` and `Docs/MORNING_BRIEF_PUBLISHING.md`. Only `local-routine-state.json` records current schedule evidence; old cloud state is historical. No mail, campaign or social schedule changes and no daily notification.

Current video cadence is Sunday/Wednesday 9 AM Central, at most one long-form per day; other platforms follow the next day at noon after public YouTube verification. Preserve genuine approval/date/asset conflicts. The complete social inventory is imported in bounded batches without truncation. Verify the whole stored edition, its date and image digest/size, and the owner browser after publishing. Article gaps and failed checks stay explicit, never converted to zero.

## sixpackabs.com article for every new video

| Item | Current state |
| --- | --- |
| Routine | `sixpackabs-article-gap-daily`, a Claude scheduled task (Claude app, Routines) |
| Schedule | Every day, 10:30 AM America/Chicago. The Mac and the Claude app must be open; a missed run fires at next launch |
| Owner | Claude. It is the one routine kept on Claude on purpose: the work is writing in Dan's voice (Opus 5.5 through `dan-voice-writer`) and publishing through the WordPress.com connector, and both live on the Claude side |
| Prompt | `~/.claude/scheduled-tasks/sixpackabs-article-gap-daily/SKILL.md` |
| Detector | `python3 sixpackabs/articles/gap.py` (no AI, no login). Exit 0 none late, 1 a gap older than 24 hours, 2 could not check |
| Cost when idle | One script call and a one-line answer |
| Early warning | Server log line `sixpackabs article gap: ...` after each five-minute feed refresh (`scripts/sixpackabs/article-gaps.js`) |
| Check on the routine | Morning brief input `sources.article_gaps` and `Docs/BOARD_MORNING_MAINTENANCE.md` step 8 |
| Rules | `sixpackabs/articles/README.md`. Receipt: `Docs/SIXPACKABS_ARTICLE_AUTOMATION_RECEIPT_20261010.md` |

A Codex release-check automation that also publishes a long-form's article (for example the December 6 Keep Your Muscle check) does not conflict: whichever runs first publishes, and the other finds `gap.py` clean and the draft already renamed.

## Edit stall watchdog

| Item | Current state |
| --- | --- |
| Routine | `edit-stall-watchdog`, a Claude scheduled task (Claude app, Routines), created 2026-11-05 |
| Schedule | Every 15 minutes. The Mac and the Claude app must be open; runs start in the app's default permission mode |
| Detector | `python3 .claude/skills/_shared/stallwatch/stallwatch.py scan --claim --json` (no AI, no login) |
| Cost when idle | One script call and a one-line answer |
| Does | Finds edit jobs with no live process, logs quiet 20+ min and no DONE marker; messages the Claude session holding the edit slot (2 nudges, 30 min apart), then notifies Dan. Codex-owned stalls go to Dan |
| Prompt | `~/.claude/scheduled-tasks/edit-stall-watchdog/SKILL.md` |
| Rules | `.claude/skills/_shared/stallwatch/README.md`; VIDEO-RULES.md, render queue section, "Chains are watched by their EXIT" |
