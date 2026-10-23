# SL-17 I'm 41. I'm Top 1%. How I Did It. shorts: setup receipt (2026-10-23)

Task `Top 1 Percent SFL Setup`, Claude Opus 5.5. Handoff `Handoffs/handoff-20261023-sl17-top-1-percent-shorts-covers-and-setup.md` (executed; removed from the OPEN list).

## Checks before any write
- Masters re-hashed: SHA-256 prefixes match the handoff (3dd0eb49, 2443763b, 65748f11). Not re-edited.
- Classification: all ORGANIC, from `/Volumes/Extreme/_edit_work/SL-17/build/{A,B,D}/delivered_asr.json`. Closing words: 1 "It'll make a huge impact on the rest of your life."; 2 "Working out has made my life better in so many ways."; 3 "Training will make you a better man. It'll make your life so much better." No "tap the button". `ad_guard.py --scan` CLEAN before (196 posts) and after (198).
- Parent RO-26 is queued on Blotato YouTube Sun Oct 25, 9 AM, not public yet. Its real title is "I'm 41. I'm Top 1%. How I Did It." (the handoff's "My Life Is Top 1%" was a working name). Descriptions name it by title; no watch URL yet (same as SL-19).

## Covers
Round 1: five choices per short (A pool photo-258 / photo-228 / photo-149, B studio-blue-240 / -188 / -266 on Codex scenes, C AI image of Dan acting the title out, D and E Codex designs); 12 Codex GPT-6.1 Sol high images on the subscription, no redo. Dan's picks 2026-10-23: Short 1 C, Short 2 C; Short 3 "I don't like any of these. Show me three new designs with a real photo of me with a black belt."
Round 2 (Short 3): real black-belt photos found in his Photos library (promotion day 2024-12-14 with his instructor, and 2024-12-21), exported as originals, never redrawn: F yellow band over the promotion photo, G seated cutout on the Codex dojo plate, H photo panel over a type panel. Dan: "Let's go with F. Change the text to 'Why Every Man Should Train In Martial Arts.'" Revised F shown first; Dan: "Okay, this is approved. Go ahead and install this cover." Cover text only; post title stays "Every Man Should Train A Martial Art".
Builder and checks: `scripts/covers/sl17-20261023/` (36 of 36 PASS). Exports `Short-form video content/covers/approved-sl17/` (`picks.json` holds full hashes).

## Scheduled (waiting list, tied to RO-26 by `parent_config`)
Blotato was full (196-198 of 200, 23 videos waiting), so all three wait on `scripts/blotato/video_waitlist.json`, placed ahead of the later-releasing entries; the daily routine `social-queue-daily-refresh` queues each as room opens and never before Oct 26.

| short | title | slot | cover | AI flag | master / TikTok | IG PNG / YT JPG | config |
|---|---|---|---|---|---|---|---|
| 1 | Nutrition Matters More Than Your Workouts | Fri 2026-10-30 14:00Z (9 AM CDT) | C | yes | `3dd0eb49` / `6fa9f6bc` | `64d95dba` / `6a11ff40` | `sl17-short1-nutrition-matters-more-than-your-workouts.json` |
| 2 | Start With 5 Minutes Every Morning | Fri 2026-11-06 15:00Z (9 AM CST) | C | no | `2443763b` / `a285917f` | `14d09fa9` / `382ff727` | `sl17-short2-start-with-5-minutes-every-morning.json` |
| 3 | Every Man Should Train A Martial Art | Mon 2026-11-30 15:00Z (9 AM CST) | F (revised) | no | `65748f11` / `8a84268d` | `a0945406` / `1466ebc7` | `sl17-short3-every-man-should-train-a-martial-art.json` |

- All 12 uploads to Blotato storage downloaded back and SHA-256 matched. `organic_short_queue.py` dry runs clean for each (4 posts: FB 47105, IG 67203, TikTok 58181, YouTube 46963).
- TikTok copies: `tiktok_cover.build()` with the Instagram cover as frame 0 (video +1 frame, audio packets identical, frame-0 PSNR 34.8 / 34.6 / 35.0 dB), in `/Volumes/Expansion/_edit_work/sl17-publish/`.
- Facebook covers (YouTube JPEG) registered in `scripts/blotato/fb_reel_covers.json` and the live installer `~/.absbyai/fb-reel-covers/`. `cover_audit.py`: no issues.
- Keyword ABS, campaign `top-1-percent`, `utm_content=sl17-short<N>`. Captions and pinned comments by `dan-voice-writer`. Short 1 carries the AI line and flag (approved AI salad-bite clip); Shorts 2 and 3 are real or Pexels footage.
- Calendar: `Docs/SHORTS_RELEASE_CALENDAR.md` "Moved 2026-10-23" note (Work Out Every Day 1 and What To Cut 1 move later; Sat Dec 19 open).

## Pinned comments
- Short 1: "I don't eat until about 2 PM, then I start with a big salad. What's the first thing you eat each day?" Posts and pins automatically after release (routine youtube-pinned-comment-daily).
- Short 2: "I still work out first thing in the morning, 7 days a week. What time do you usually work out?" Posts and pins automatically after release (routine youtube-pinned-comment-daily).
- Short 3: "I trained for about 20 years, with private lessons, to earn my black belt. Have you ever trained a martial art?" Posts and pins automatically after release (routine youtube-pinned-comment-daily).

## Copies
- Extreme: `/Volumes/Extreme/Short-form video content/top1 SL-17/` (masters, gate files, covers, picks.json; md5-matched).
- Google Drive: `Short-form video content/top1 SL-17/`, anyone with the link: https://drive.google.com/drive/folders/1Mu3iCisq2jIahFo_rgQ3d6yUlq1Bz1Dw

## After release
- Once each post is queued, read back all four posts (the routine's helper verifies on a fresh pull).
- After RO-26 is public, its watch URL can be added to each YouTube description (optional; title is already named).
- After each YouTube release, check the public Shorts tile shows the approved cover (`/video-setup`, "YouTube Shorts cover verification").
- Captions are burned in; no SRT. Articles: written by sixpackabs-article-gap-daily after release.
- Edit Queue: SL-17 `uploaded` (rev 5), mirrored to the page (version 4), synced.
