# SL-18 I'm 41. I Wasted My Life. shorts: setup receipt (2026-10-22)

Task `I'm 41 Wasted Life SFL Setup`, Claude Opus 5.5. Handoff `Handoffs/handoff-20261022-sl18-wasted-my-life-shorts-covers-and-setup.md` (executed; removed from the OPEN list).

## Checks before any write
- Masters re-hashed: SHA-256 prefixes match the handoff (130d3c14, bbd9d0cb). Not re-edited. (Two older iCloud duplicates named `... 2.mp4` in `Short-form video content/` have other hashes and were not used.)
- Classification: both ORGANIC, from `/Volumes/Expansion/_edit_work/SL-18/build/{B,D}/delivered_asr.json`. Closing words: 1 "...the long-term effects get so bad that you have to quit."; 2 "...you'll be able to attract far better women than you can today." No "tap the button". `ad_guard.py --scan` CLEAN before (150 posts) and after (158).
- Parent RO-25 public (oEmbed of https://www.youtube.com/watch?v=xyi-B_5tccw reads "I'm 41. I Wasted My Life.").

## Covers
Five choices per short (A pool photo-71 / photo-289, B studio-white-32 / studio-blue-80 on Codex scenes, C AI image of Dan, D and E Codex designs), 9 Codex GPT-6.1 Sol high images on the subscription (one redo: Short 2 E first showed two different men in a before/after, rejected before Dan saw it). Builder and checks: `scripts/covers/sl18-20261022/` (20 of 20 PASS). Dan's picks 2026-10-22: Short 1 C; Short 2 D revised per his note ("I want to have the girl crossed out with a red X ... Make the text larger"): red X drawn in code over the woman, eyebrow DATING IN YOUR 20S kept, title "Stop Dating Until You Are Ripped And Rich" (cover only; the post title stays "Build Your Value Before You Date"). Exports: `Short-form video content/covers/approved-sl18/` (`picks.json` holds full hashes).

## Scheduled (Blotato, read back)
| short | title | slot | cover | AI flag | Blotato ids (FB, IG, TT, YT) | master / TikTok | IG PNG / YT JPG | config |
|---|---|---|---|---|---|---|---|---|
| 1 | Why ADHD Meds Backfire Long Term | Mon 2026-10-26 14:00Z (9 AM CDT) | C | yes | 5909596, 5909597, 5909598, 5909600 | `130d3c14` / `9f616ab4` | `77cde648` / `8fb7b6ef` | `sl18-short1-why-adhd-meds-backfire-long-term.json` |
| 2 | Build Your Value Before You Date | Sat 2026-12-12 15:00Z (9 AM CST) | D (revised) | yes | 5909603, 5909604, 5909605, 5909607 | `bbd9d0cb` / `f31fc16e` | `c0f40f60` / `84b90464` | `sl18-short2-build-your-value-before-you-date.json` |

- All 8 uploads and the 8 media URLs Blotato saved on the posts downloaded back and SHA-256 matched. YouTube titles, covers and `containsSyntheticMedia` true read back; TikTok `isAiGenerated` true, cover timestamp 0.
- TikTok copies: `tiktok_cover.build()` with the Instagram cover as frame 0 (video +1 frame, audio packets identical, frame-0 PSNR 35.2 / 37.1 dB), in `/Volumes/Expansion/_edit_work/sl18-publish/`.
- Facebook covers (YouTube JPEG) registered in `scripts/blotato/fb_reel_covers.json` and the live installer `~/.absbyai/fb-reel-covers/`. `cover_audit.py`: 158 posts, no issues. (The main folder's copy of the registry was union-resolved from both merge sides to clear stale conflict markers that broke the guard; backup `tmp/fb_reel_covers.conflict-backup-20261022.json` in the main folder.)
- Keyword ABS, campaign `wasted-my-life`, `utm_content=sl18-short<N>`. YouTube descriptions name the full video "I'm 41. I Wasted My Life." with its watch link and the AI line. Captions by `dan-voice-writer`.

## Pinned comments (dan-voice-writer)
- Short 1: "I took Vyvanse, Adderall and Adderall XR for about five years. Have you ever taken an ADHD drug?" Posts and pins after release (routine youtube-pinned-comment-daily).
- Short 2: "Dating is always going to be a struggle until you're ripped and rich. Which one are you working on first, ripped or rich?" Posts and pins after release.

## Copies
- Extreme: `/Volumes/Extreme/Short-form video content/wastedlife SL-18/` (masters, covers, picks.json; md5-matched).
- Google Drive: `Short-form video content/wastedlife SL-18/`, anyone with the link: https://drive.google.com/open?id=1zKrokHlEYhiSAoB5Q7lVLttOa265D2nq (rclone check: 7 matching files).

## After release
- Captions are burned in; no SRT. Articles: written by sixpackabs-article-gap-daily after release.
- After each YouTube release, check the public Shorts tile shows the approved cover (`/video-setup`, "YouTube Shorts cover verification").
- Edit Queue: SL-18 `uploaded` (rev 6), mirrored to the page (version 5), synced. No third Short: the Tue Dec 15 "Wasted My Life 3" slot goes to another video Dan picks.

## Short 2 cover revision R2 (2026-10-22, later)
Dan revised cover D: drop the DATING IN YOUR 20S eyebrow; "STOP DATING" huge, red, all caps across the full width; "Until You Are / Ripped And Rich" white, larger. Shown to him first (new rule: a revised cover waits for his approval, VIDEO-RULES and memory `approve-revised-cover-before-install`); he replied "Approved, install it".
- New files: Instagram PNG `a278e3bd`, YouTube JPEG `90c945ce`, TikTok cover-first copy `336241ce` (frame-0 PSNR 36.1 dB, audio packets identical). R1 files kept in `approved-sl18/superseded-r1/`.
- Swapped on Instagram 5909604 (coverImageUrl), YouTube 5909607 (thumbnailUrl) and TikTok 5909605 (media), read back: captions, title, flags and time unchanged; all hashes match. Facebook 5909603: live installer cover file replaced in place (same path).
- Extreme and Drive copies refreshed (md5 / rclone matched). `cover_audit.py`: 182 posts, 0 issues; `ad_guard.py --scan` CLEAN.
