# SL-04 Arms & Shoulders shorts: setup receipt (2026-09-30)

Handoff `Handoffs/handoff-20260930-sl04-shorts-video-setup.md`, run by Claude Opus 5.5.

## Checks before any write
- All five masters re-hashed: SHA-256 prefixes match the handoff (952f3596..., 8dc39f0e..., 2931ce4f..., f052cd54..., d5e9f096...).
- Covers: short 2 `cover-B` (approved earlier); shorts 1, 3, 4, 5 `cover-D` from `Short-form video content/covers/approved-sl04-D-for-Claude/`, MD5-identical to `posted covers/` and `posted covers/youtube/`.
- Classification: all five ORGANIC. Closing words from `/Volumes/Extreme/_edit_work/sl04/build/gate/*_asr_clean.json`: "like this at the top", "do three or four rounds", "whichever way works the best for you is perfectly valid", "just make sure there's no rocking", "no swinging, no rocking, no momentum". No "tap the button".
- Parent "Arms & Shoulders Home Workout" is public: YouTube `ZxsFnsv7mLo`, FB reel and TikTok posted 2026-09-27. Its IG @danrosefit post (`739230`) reads **failed** ("internal server error"); not re-checked on Instagram.
- Content ID on the parent: claim "Heavy Metal Thunder" (Birthday PAPA, claimant Elite Alliance Music), 8:25-9:57, the live-round song. Studio says no impact on reach or channel, only potential earnings. Shorts 1 and 2 end on this track; queued anyway and flagged to Dan (first one posts Oct 6).
- ad_guard `--scan` CLEAN before and after.

## No YouTube holding upload
Per VIDEO-RULES (Dan, 2026-10-01: organic = Blotato only), no Private upload was made; Blotato creates the public YouTube Short at release.

## Schedules (9 AM CDT = 14:00Z, keyword TRAIN, ai_generated false)

| order | short | date | FB | IG @danrosefit | TikTok | YouTube |
|---|---|---|---|---|---|---|
| 1 | short 2 "Do This 2 Minute Arm Pump Before You Take Your Shirt Off" | Tue Oct 6 | 5019222 | 5019223 | 5019224 | 5019225 |
| 2 | short 1 "Make Your Waist Look Smaller With Side Lateral Raises" | Thu Oct 8 | 5019226 | 5019227 | 5019228 | 5019229 |
| 3 | short 5 "How To Do Bicep Curls: One Arm or Both Arms?" | Sat Oct 10 | 5019232 | 5019233 | 5019234 | 5019235 |
| 4 | short 3 "Side Lateral Raise Mistake: Raise Your Elbows, Not Your Hands" | Tue Oct 13 | 5019237 | 5019238 | 5019240 | 5019241 |
| 5 | short 4 "Stop Swinging Your Bicep Curls" | Thu Oct 15 | 5019247 | 5019250 | 5019251 | 5019252 |

- Configs: `scripts/blotato/configs/sl04-short{1..5}-*.json`. Queue 113 -> 133 of 200.
- Fresh pull: text and targets identical to the plan on all 20; Blotato rehosted every media URL, and each rehosted file downloads MD5-identical to the master (TikTok: to the cover-first copy).
- TikTok: `tiktok_cover.build()` cover as frame 0, `videoCoverTimestamp: 0`; frames +1, audio packets unchanged, cover PSNR 47.4-51.1 dB.
- YouTube thumbnails: the YouTube-layout covers as JPEG q92 (445-620 KB; the PNGs were over YouTube's 2 MB limit). IG covers: the Instagram-layout PNGs.
- `organic_short_queue.py` TikTok line changed from an em dash to a comma ("Free Abs By AI preview, link in bio").

## Copies
- Extreme: `/Volumes/Extreme/Short-form video content/arms-shoulders SL-04/` (5 masters MD5-matched + 5 covers).
- Google Drive: `Short-form video content/arms-shoulders SL-04/`, anyone with the link.

## After release
- Captions are burned in; no SRT to upload.
