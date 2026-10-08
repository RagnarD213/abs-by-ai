# SL-03 Daily Salad: queue shorts 2, 3 and 6 (the Blotato cap blocked them)

**Category: CONTENT, Shorts (`SFC`). Written 2026-10-08 by Claude (Sonnet 5.5). Task name: `Daily Salad SFC Setup 2`.**
Shorts 1, 4 and 5 are queued (Oct 29, Oct 31, Nov 3). The queue was 198 of 200, so shorts 2, 3 and 6 wait for room. Everything else is ready. Full state: `Docs/SL03_SETUP_RECEIPT_20261008.md`.

## What is ready
- Configs `scripts/blotato/configs/sl03-short2-*.json`, `sl03-short3-*.json`, `sl03-short6-*.json` (copy, hash-checked uploads, covers, slots Thu Nov 5, Sat Nov 7, Tue Nov 10 at 15:00Z, keyword FOOD).
- Dan approved all covers and all six shorts. Short 6 is titled "Make AI Calorie Tracking Accurate".

## Steps
1. `python3 scripts/blotato/ad_guard.py --scan` (expect CLEAN). Read the live queue; you need room for 12 posts (queue at 188 or fewer). The cap is 200. If short, queue in order 2, 3, 6 as far as it fits and tell Dan what is left.
2. Confirm "How I Make My Daily Salad" is still scheduled or public on all four (Blotato posts 5014534, 5014529, 5014531, 5014533). If it failed, tell Dan before queuing.
3. For each short in order 2, 3, 6: dry run `python3 scripts/blotato/organic_short_queue.py <config>`, then `--apply`. If a slot now clashes or a config's media URL no longer downloads, stop and tell Dan.
4. Verify on a fresh pull and by downloading each hosted media URL and covers (SHA-256 against `Short-form video content/daily-salad-short<N>_*.mp4`, the TikTok copies in `/Volumes/Extreme/_edit_work/sl03-publish/` and `Short-form video content/covers/approved-sl03/`).
5. When all six are queued: `python3 scripts/edit-queue/queue.py set SL-03 uploaded --by Claude --note "..."`, mirror the row to the Edit Queue artifact (read it first, pin `if_version`), `queue.py mark-synced SL-03`.
6. Append the three schedules to `Docs/SL03_SETUP_RECEIPT_20261008.md`, update `BLOTATO_QUEUE_PROGRESS.md`, delete this handoff's board line and README row, push with `scripts/git/safe-push.sh`.

## Traps
- Never queue an ad organically; these are organic. Never @abs.by.ai.
- 9 AM Central is 14:00Z until Nov 1 and 15:00Z after.
- Shorts 5 and 6 stay at least a week apart; do not move short 6 earlier than Nov 10.

## Starter prompt
> Name this task `Daily Salad SFC Setup 2`. Read `Handoffs/handoff-20261008-sl03-queue-shorts-2-3-6.md` and `Docs/SL03_SETUP_RECEIPT_20261008.md`. Queue Daily Salad shorts 2, 3 and 6 in Blotato as the handoff says, verify every schedule, and report. If anything does not match the receipt, stop and tell me.

Model and effort: Claude Sonnet 5, medium. Fire when the Blotato queue has room for 12 posts (about Oct 12 or later).
