# SL-07 If I Had Belly Fat shorts: setup receipt (2026-10-18)

Task `If I Had Belly Fat SFC Setup`, Claude Opus 5.5. Handoff `Handoffs/handoff-20261018-sl07-belly-fat-shorts-covers-and-setup.md`.

## Checks before any write
- Masters re-hashed: SHA-256 prefixes match the handoff (b55cf957, 1ebf30e5, eedadc47, 088b3898, 4a971479). Not re-edited.
- Classification: all five ORGANIC. Closing words: 1 "everything else would have to fit around that."; 2 "hope the scale is going to move."; 3 "that's the reason why."; 4 "Losing 30 pounds is 90 days of sacrifice."; 5 "you'll be shocked at how much faster you start losing fat." No "tap the button". `ad_guard.py --scan` CLEAN (198 posts) before and after.
- Parent RO-16 YouTube schedule `5090110` is Sun Dec 20 2026 15:00Z (read live 2026-10-18), so the shorts follow it.

## Covers
Five choices per short (A pool, B studio on a Codex scene, C AI image of Dan, D and E Codex designs), all Codex GPT-6.1 Sol high on the subscription (20 images). Builder, prompts and measured checks: `scripts/covers/sl07-20261018/` (person mask + face boxes on each cover's picture layer; 50 of 50 PASS, one checked waiver on 5D). Review page: http://127.0.0.1:8893/. Dan's picks 2026-10-18: "1. C 2. C 3. A 4. C 5. C". Exports: `Short-form video content/covers/approved-sl07/` (`picks.json` holds full hashes).

## Status: WAITING for Blotato room (queue 198 of 200)
Everything is uploaded and configured; the five shorts are on `scripts/blotato/video_waitlist.json` (kind `short`). The daily routine `social-queue-daily-refresh` queues them on their saved slots (dry run 2026-10-18 confirmed Dec 21, 22, 26, 28, 29 at 9 AM Central). Dry runs: no slot clash on any of the four accounts; refused only on the cap.

| short | title | slot | cover | AI flag | master / TikTok sha256 | IG PNG / YT JPG sha256 | config |
|---|---|---|---|---|---|---|---|
| 1 | Stop Trying To Lose 1 Pound A Week | 2026-12-21 15:00Z | C | no | `b55cf957` / `fe58c9f6` | `90c15973` / `d05fd112` | `sl07-short1-stop-trying-to-lose-1-pound-a-week.json` |
| 2 | Weigh Yourself Every Morning | 2026-12-22 15:00Z | C | yes | `1ebf30e5` / `5b71d1ef` | `c4d3e5e9` / `274787e7` | `sl07-short2-weigh-yourself-every-morning.json` |
| 3 | Work Out Every Morning, Not 3 Times A Week | 2026-12-26 15:00Z | A | yes | `eedadc47` / `f7328fd2` | `42feefe5` / `8685fe8d` | `sl07-short3-work-out-every-morning.json` |
| 4 | The 3-Pound Rule That Keeps Belly Fat Off | 2026-12-28 15:00Z | C | yes | `088b3898` / `1800ff63` | `16aee806` / `5c80f459` | `sl07-short4-the-3-pound-rule.json` |
| 5 | Track Your Calories With A Photo | 2026-12-29 15:00Z | C | yes | `4a971479` / `695f91f7` | `7aa84425` / `9c363e7a` | `sl07-short5-track-your-calories-with-a-photo.json` |

- All 20 uploads (5 masters, 5 TikTok cover-first copies, 5 Instagram PNGs, 5 YouTube JPEGs, all under 2 MB) downloaded back from their public URLs and SHA-256 matched.
- TikTok copies: `tiktok_cover.build()` with the Instagram cover as frame 0 (cover PSNR 47 dB, video +1 frame, audio packets identical, no decode errors). In `/Volumes/Extreme/_edit_work/sl07-publish/`.
- Facebook covers (YouTube layout JPEG) registered in `scripts/blotato/fb_reel_covers.json` and the live installer `~/.absbyai/fb-reel-covers/`, matched on each caption's first line. `cover_audit.py`: no issues.
- Keyword FOOD (as RO-16), campaign `belly-fat-90-days`, `utm_content=sl07-short<N>`. YouTube descriptions name the full video by title.

## Pinned comments (dan-voice-writer)
- Short 1: Losing 1 pound a week means 7 months for 30 pounds, and almost nobody stays motivated that long. Would you go all in for 90 days?
- Short 2: Weigh yourself every morning after the bathroom, before you eat, and judge your 7 day average against last week's. Do you weigh every day, or do you avoid the scale?
- Short 3: A 10 to 15 minute workout every morning beats 2 or 3 long sessions a week, because first thing in the morning nobody needs you yet. What time do you usually work out?
- Short 4: Keep weighing every day after you reach your goal, and if you're more than 3 pounds over, go right back to cutting. Do you still weigh yourself after you hit a goal?
- Short 5: The old way of weighing your food was too much work. Now you take a picture and AI gives you the calories and protein. Do you track your calories right now, and how?

## Copies
- Extreme: `/Volumes/Extreme/Short-form video content/belly-fat SL-07/` (five masters md5-matched, ten covers).
- Google Drive: `Short-form video content/belly-fat SL-07/`, anyone with the link: https://drive.google.com/open?id=1-R-6Gl6O4tsPsknt1dRuNTNl0hZWsy53 (md5-matched).

## After release
- Captions are burned in; no SRT. Articles: written by the routine after release.
- After each YouTube release, check the public Shorts tile shows the approved cover (`/video-setup`, "YouTube Shorts cover verification"); the cover monitor checks all four platforms.
