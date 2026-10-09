# SL-03 Daily Salad shorts: setup receipt (2026-10-08)

Task `Daily Salad SFC Setup`, Claude Sonnet 5.5. Handoff `Handoffs/handoff-20261008-sl03-daily-salad-shorts-covers-and-setup.md`. Covers and picks: `Docs/SL03_COVER_FINALS_20261008.md`.

## Checks before any write
- All six masters re-hashed: SHA-256 prefixes match the handoff (6b423816, d8c3d4fb, c270c157, e4848c5f, 8f7fd9cf, b824dd8f). Not re-edited.
- Classification: all six ORGANIC. Closing words: "start doing what I'm doing right here" (1, 2), "sealed glass containers" (3), "Too little and it's going to be dry" (4), "one meal prep thing alone" (5), "almost near accurate for taking pictures" (6). No "tap the button". `ad_guard.py --scan` CLEAN before (186 posts) and after (198 posts).
- Parent "How I Make My Daily Salad" is NOT public yet: still scheduled, YouTube Sun Oct 18 (5014534), Facebook / Instagram / TikTok Mon Oct 19 (5014529, 5014531, 5014533), none failed. Dan said to install now, so the shorts were scheduled for dates 10 or more days AFTER the parent. If the parent fails to post, hold or move shorts 1, 4, 5.

## Capacity
Queue was 186 of 200. Each short is 4 posts, so only three shorts fit (198 of 200). Shorts 2, 3 and 6 are not queued yet; their configs and uploads are ready (see below).

## Schedules (9 AM Central, keyword FOOD, campaign `daily-salad`, AI flag off)

| order | short | when | FB | IG @danrosefit | TikTok | YouTube |
|---|---|---|---|---|---|---|
| 1 | 1 "Break Your Fast With This" | Thu Oct 29 14:00Z (CDT) | 5329617 | 5329619 | 5329622 | 5329624 |
| 2 | 4 "Stop Buying Salad Dressing" | Sat Oct 31 14:00Z (CDT) | 5329625 | 5329626 | 5329628 | 5329629 |
| 3 | 5 "Track A Week Of Meals From 1 Photo" | Tue Nov 3 15:00Z (CST) | 5329631 | 5329632 | 5329633 | 5329634 |
| 4 | 2 "The $20 Salad You Can Make For $4" | Thu Nov 5 15:00Z | 5361331 | 5361332 | 5361333 | 5361334 |
| 5 | 3 "Keep Your Salads Fresh For 7 Days" | Sat Nov 7 15:00Z | owed | owed | owed | owed |
| 6 | 6 "Make AI Calorie Tracking Accurate" | Tue Nov 10 15:00Z | owed | owed | owed | owed |

Dan's constraints hold: shorts 5 and 6 are 7 days apart; shorts 1 and 2 are not back to back. No same-minute clash on the four accounts. The Ab Wheel shorts post the same days at 5 PM Central (different time, as with SL-05). Clocks go back Nov 1, so slots from Nov 3 are 15:00Z.

## Verification (fresh pull of the schedule list)
- Every post is the config's text, target and slot; TikTok `videoCoverTimestamp` 0 and `isAiGenerated` false; YouTube `privacyStatus` public with the approved JPEG as `thumbnailUrl`; Instagram `coverImageUrl` is the approved PNG.
- Blotato re-hosts media when a schedule is created. Downloaded from the hosted URLs, all 18 files (3 masters used by FB/IG/YouTube, 3 TikTok copies, 3 Instagram PNGs, 3 YouTube JPEGs) are byte-identical (SHA-256) to the local files.
- TikTok copies: `tiktok_cover.build()` with the Instagram PNG as frame 0, video frames +1, audio untouched, no decode errors. Copies in `/Volumes/Extreme/_edit_work/sl03-publish/`.
- All 24 uploads (six shorts) were hash-checked after upload. Configs: `scripts/blotato/configs/sl03-short{1..6}-*.json`.

## Copies
- Extreme: `/Volumes/Extreme/Short-form video content/daily-salad SL-03/` (six masters MD5-matched, 12 covers).
- Google Drive: `Short-form video content/daily-salad SL-03/`, anyone with the link: https://drive.google.com/open?id=1F9qvzozSy07XDy6JsusjZhkeW7aXYILs

## After release
- Captions are burned in; no SRT.
- After each YouTube release, check the public Shorts tile shows the approved cover (skill `/video-setup`, "YouTube Shorts cover verification"); fix in desktop Studio if it shows a frame.
- Short 6's post title is "Make AI Calorie Tracking Accurate"; the burned-in band in the video still says "The One Line That Makes It Accurate".
- YouTube descriptions name the full video by title (no link until it has a public id after Oct 18).
- Remaining: `Handoffs/handoff-20261008-sl03-queue-shorts-2-3-6.md`.

## Automation (2026-10-08)
Scheduled task `sl03-queue-shorts-2-3-6` (daily about 8:30 AM, Claude app must be open) queues shorts 2, 3 and 6 once the Blotato queue has room, then disables itself. Queue was 198 of 200; expect room after the Oct 10 posts (about 184).

## Short 2 queued (2026-10-09, scheduled task)
- Queue was 195 of 200, room for one short only. Short 2 queued for Thu Nov 5 15:00Z: Facebook 5361331, Instagram @danrosefit 5361332, TikTok 5361333, YouTube 5361334. Queue now 199 of 200.
- `ad_guard.py --scan` CLEAN (195 posts). Parent still scheduled, none failed (5014534 Oct 18; 5014529, 5014531, 5014533 Oct 19).
- Fresh pull: text, targets and slot match the config; TikTok `videoCoverTimestamp` 0, `isAiGenerated` false; YouTube public, synthetic off. Hosted media downloaded and SHA-256 matched to local files: master d8c3d4fb (FB, IG, YouTube), TikTok copy e629949e, Instagram PNG 060b9e0d, YouTube JPEG 755843f8.
- Still owed: short 3 (Sat Nov 7) and short 6 (Tue Nov 10). The task retries daily.
