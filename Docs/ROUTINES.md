# Routines

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
