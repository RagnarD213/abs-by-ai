# SL-15 My First Spray Tan shorts: setup receipt (2026-10-22)

Task `My First Spray Tan SFL Setup`, Claude Opus 5.5. Handoff `Handoffs/handoff-20261021-sl15-spray-tan-shorts-covers-and-setup.md`.

## Checks before any write
- Masters re-hashed: SHA-256 prefixes match the handoff (`ec87695a`, `476b5a6f`). Not re-edited. The iCloud duplicates named `... 2.mp4` / `... 3.mp4` beside them were never touched or uploaded.
- Classification: both ORGANIC. Closing words: 1 "...you'll look much more defined."; 2 "...you're a lot more likely to get that kind of cancer." No "tap the button". `ad_guard.py --scan` CLEAN (192 posts).
- Parent RO-19 "Spray Tanning Guide: How To Looksmax With A Spray Tan" is NOT public: it is on the waiting list, and the 2026-10-22 dry run of `video_topup.py` shows it queued at the next run for YouTube Wed Dec 30 2026, 9 AM Central (queue 192 of 200).

## Covers (six rounds with Dan)
Round 1: five choices per short (A pool, B studio on a Codex scene, C AI image of Dan, D and E Codex designs), Codex GPT-6.1 Sol high on the subscription (8 images plus one retake). Short 2: Dan picked C. Short 1: round 2 added F/G from the film's own pale vs tan pairs; Dan picked F's photos with new copy "How A Spray Tan Makes You Look More Ripped" and asked for designs with less blank space; round 3 H/I/K; Dan picked K (tan photo full frame, pale photo as a tilted print) and three rounds of position edits followed (print clear of his body, measured 0 px overlap; YouTube layout equal to Instagram). Builder and checks: `scripts/covers/sl15-20261021/` (`build.py`, `build_r2.py`, `build_r3.py`, `qc.py`: 30 of 30 PASS). Review page: http://127.0.0.1:9151/. Exports: `Short-form video content/covers/approved-sl15/` (`picks.json` holds full hashes). The cover copy of short 1 differs from its burned-in title; the post title stays "Why You Look Less Ripped In Photos".

## Status: WAITING (parent first)
Both shorts are on `scripts/blotato/video_waitlist.json` (kind `short`) with `"after": "scripts/blotato/configs/ro19-my-first-spray-tan.json"`. New in `video_topup.py` (2026-10-22): a Short with `after` waits until its parent is on Blotato and is always slotted after the parent's YouTube release day. Dry runs: with room, RO-19 Wed Dec 30, short 1 Fri Jan 1 2027, short 2 Sat Jan 2 2027, all 9 AM Central; with RO-19 held, both shorts print "waiting parent". (Dan's 2026-only rule cannot hold: the parent itself releases Dec 30.)

| short | title | slot | cover | AI flag | master / TikTok sha256 | IG PNG / YT JPG sha256 | config |
|---|---|---|---|---|---|---|---|
| 1 | Why You Look Less Ripped In Photos | 2027-01-01 15:00Z | K | no (real photos) | `ec87695a` / `1315e0c4` | `3ff5f562` / `9b99aabc` | `sl15-short1-why-you-look-less-ripped-in-photos.json` |
| 2 | Get A Tan Without Sun Damage | 2027-01-02 15:00Z | C | yes (AI appointment, AI vampire) | `476b5a6f` / `0971e70b` | `83e73141` / `16ee750c` | `sl15-short2-get-a-tan-without-sun-damage.json` |

- All 8 uploads (2 masters, 2 TikTok cover-first copies, 2 Instagram PNGs, 2 YouTube JPEGs under 2 MB) downloaded back from their public URLs and SHA-256 matched. `organic_short_queue.py` dry runs: 4 posts each (FB 47105, IG 67203, TikTok 58181, YouTube 46963).
- TikTok copies: `tiktok_cover.build()` with the Instagram cover as frame 0 (video +1 frame, audio packets identical, cover PSNR 36.9 / 35.2 dB). In `/Volumes/Expansion/_edit_work/sl15-publish/`.
- Facebook covers (YouTube layout JPEG) registered in `scripts/blotato/fb_reel_covers.json` and the live installer `~/.absbyai/fb-reel-covers/`, matched on each caption's first line. `cover_audit.py`: no issues.
- Keyword TRACK (as RO-19), campaign `spray-tanning-guide`, `utm_content=sl15-short<N>`. YouTube descriptions name the full video by title; short 1 says its photos are real, short 2 carries the AI-footage line.

## Pinned comments (dan-voice-writer)
- Short 1: Have you ever looked great in the mirror and then way less defined in a photo? Let me know in the comments.
- Short 2: How do you usually get your tan, from the sun or a spray tan? Let me know below.

## Copies
- Extreme: `/Volumes/Extreme/Short-form video content/spraytan SL-15/` (masters and four covers, md5-matched).
- Google Drive: `Short-form video content/spraytan SL-15/`, anyone with the link: https://drive.google.com/open?id=1Fw0Cc5elo3-6c5CgodQbCuM03p3MYc1W (md5-matched).

## After release
- Captions are burned in; no SRT. Articles: written by the routine after release.
- After each YouTube release, check the public Shorts tile shows the approved cover (`/video-setup`, "YouTube Shorts cover verification"); the cover monitor checks all four platforms.
