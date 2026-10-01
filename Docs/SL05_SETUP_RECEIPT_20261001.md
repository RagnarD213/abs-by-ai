# SL-05 Stop Deadlifting shorts: setup receipt (2026-10-01)

Handoff `Handoffs/handoff-20261001-sl05-shorts-video-setup.md`, run by Claude Opus 5.5 on Dan's instruction.

## Checks before any write
- All five masters re-hashed: SHA-256 prefixes match the handoff (b67c57cc, 4e47fc96, 51c89fab, 44a35a16, 4381f541).
- Covers: round 2 option A (dark gym, red X) from `Short-form video content/covers/approved-sl05-for-Claude/`; all ten SHA-256 match `Docs/SL05_COVER_FINALS_20261001.md`.
- Classification: all five ORGANIC. Closing words from `/Volumes/Extreme/_edit_work/sl05/build/gate/S*_asr_clean.json`: "This is how most people end up quitting.", "actually build more muscle with the safer exercise.", "that are better for making you look better.", "slow and you're going to build those lats", "then periodically getting injured and getting set back." No "tap the button".
- ad_guard `--scan` CLEAN before (137 posts) and after (157 posts).
- **Parent is NOT public yet.** "Why I Stopped Deadlifting at 40" is still scheduled in Blotato for Sun Oct 11 9 AM CT (`4976695` FB / `4976700` IG / `4976709` TikTok / `4976708` YouTube). The handoff said to run after it posts; Dan fired the setup on Oct 1, so the shorts were scheduled for dates after the parent (first one six days later). If the parent fails to post on Oct 11, hold or move these 20 posts.

## No YouTube holding upload
Blotato creates each public YouTube Short at release (Dan, 2026-10-01).

## Schedules (9 AM CDT = 14:00Z, keyword TRAIN, campaign `stop-deadlifting`)

| order | short | date | AI flag | FB | IG @danrosefit | TikTok | YouTube |
|---|---|---|---|---|---|---|---|
| 1 | short 1 "Deadlifts Cause More Injuries Than Every Other Lift" | Sat Oct 17 | on | 5053506 | 5053507 | 5053509 | 5053510 |
| 2 | short 4 "2 Back Exercises To Do Instead Of Deadlifts" | Tue Oct 20 | on | 5053515 | 5053516 | 5053517 | 5053518 |
| 3 | short 2 "Safer Lifts Build MORE Muscle Long Term" | Thu Oct 22 | on | 5053520 | 5053522 | 5053523 | 5053524 |
| 4 | short 5 "Train Legs Without Deadlifts" | Sat Oct 24 | off | 5053527 | 5053528 | 5053529 | 5053530 |
| 5 | short 3 "Deadlifts Build A Powerlifter Body, Not An Aesthetic One" | Tue Oct 27 | on | 5053535 | 5053536 | 5053538 | 5053539 |

- Configs: `scripts/blotato/configs/sl05-short{1..5}-*.json`. Queue 137 -> 157 of 200.
- Read back by `organic_short_queue.py` after each write: text, media and targets identical to the plan on all 20.
- Uploads: all 20 files (master, TikTok copy, Instagram cover, YouTube cover per short) download MD5-identical from Blotato.
- TikTok: `tiktok_cover.build()` cover as frame 0, `videoCoverTimestamp: 0`; frames +1, audio packets unchanged, cover PSNR 48.3-49.5 dB. Copies in `/Volumes/Extreme/_edit_work/sl05/setup/`.
- YouTube thumbnails: the YouTube-layout PNGs (1.5-1.7 MB, under the 2 MB limit). IG covers: the Instagram-layout PNGs.
- Oct 27 also has the first $17 Ab Wheel short at 5 PM CT on FB, IG and TikTok; different time, no clash.
- YouTube descriptions name the full video by title (no link: it has no public id until Oct 11).

## Copies
- Extreme: `/Volumes/Extreme/Short-form video content/stop-deadlifting SL-05/` (5 masters MD5-matched + 10 covers).
- Google Drive: `Short-form video content/stop-deadlifting SL-05/`, anyone with the link.

## After release
- Captions are burned in; no SRT to upload.
