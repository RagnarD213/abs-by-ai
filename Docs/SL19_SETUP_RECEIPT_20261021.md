# SL-19 3 Healthy Foods That Made Me Fat shorts: setup receipt (2026-10-21)

Task `3 Healthy Foods SFL Setup`, Claude Opus 5.5. Handoff `Handoffs/handoff-20261021-sl19-healthy-foods-shorts-covers-and-setup.md` (executed; removed from the OPEN list).

## Checks before any write
- Masters re-hashed: SHA-256 prefixes match the handoff (95643513, 6d98a3fc, 56ec71eb). Not re-edited.
- Classification: all three ORGANIC, from the delivered transcripts (`/Volumes/Extreme/_edit_work/SL-19/build/{C,A,D}/delivered_asr.json`). Closing words: 1 "...these days I stay just as hydrated or better from using a zero-calorie electrolyte powder."; 2 "...eating 700 calories of healthy trail mix at your desk and wondering why you're still fat."; 3 "...I would say that's the best fast food snack out there.". No "tap the button". `ad_guard.py --scan` CLEAN (196 posts) before and after.
- Parent RO-17 is on the waiting list for YouTube Sun Dec 13 (Blotato 196/200), so the shorts wait behind it.

## Covers
Five choices per short (A pool, B studio on a Codex scene, C AI image of Dan acting the title out, D and E Codex designs), 12 Codex GPT-6.1 Sol high images on the subscription. Builder, prompts and checks: `scripts/covers/sl19-20261021/` (person mask + face boxes on each cover's picture layer; 30 of 30 PASS, no waivers). Short 2 pool photo swapped from photo-106 (arms hid the abs) to photo-298 before Dan saw it; Short 3 pool photo-167 cropped at the waistband (Speedo rule). Dan's picks 2026-10-21: "Go with C for all". Exports: `Short-form video content/covers/approved-sl19/` (`picks.json` holds full hashes).

## Status: WAITING behind RO-17 on the waiting list
| short | title | slot | cover | AI flag | master / TikTok sha256 | IG PNG / YT JPG sha256 | config |
|---|---|---|---|---|---|---|---|
| 1 | Coconut Water Is Just Sugar Water | Mon 2026-12-14 15:00Z | C | no | `95643513` / `d04cf65b` | `f2e41477` / `49534a66` | `sl19-short1-coconut-water-is-just-sugar-water.json` |
| 2 | Trail Mix Has More Calories Than A Big Mac | Fri 2026-12-18 15:00Z | C | yes | `6d98a3fc` / `d52b4188` | `aee21d90` / `fb4ff3cf` | `sl19-short2-trail-mix-more-calories-than-a-big-mac.json` |
| 3 | My 4 Go-To High-Protein Snacks | Fri 2026-12-25 15:00Z | C | yes | `56ec71eb` / `0c64ce23` | `5d70df53` / `bf9795a3` | `sl19-short3-my-4-high-protein-snacks.json` |

- Slots: Short 1 per the calendar. Dan's rule (every edited Short releases in 2026) put Shorts 2 and 3 on Fri Dec 18 and Fri Dec 25, slots held for SL-12 and SL-13, which had not started editing (calendar note added). The handoff's 2027 placement predates that check.
- `video_waitlist.json` entries carry `parent_config: ro17-3-healthy-foods.json`; `video_topup.py` now never slots such a Short on or before the parent's day (tested: parent moved to Dec 20 re-slots Short 1 to Dec 25). Dry run with room: RO-17 Dec 13, then SL-19 Dec 14, 18, 25.
- All 12 uploads (3 masters, 3 TikTok cover-first copies, 3 Instagram PNGs, 3 YouTube JPEGs, all under 2 MB) downloaded back from their public URLs and SHA-256 matched.
- TikTok copies: `tiktok_cover.build()` with the Instagram cover as frame 0 (video +1 frame, audio packets identical, frame-0 PSNR 35 dB). In `/Volumes/Expansion/_edit_work/sl19-publish/`.
- Facebook covers (YouTube layout JPEG) registered in `scripts/blotato/fb_reel_covers.json` and the live installer `~/.absbyai/fb-reel-covers/`, matched on each caption's first line. `cover_audit.py`: no issues.
- Keyword FOOD (as RO-17), campaign `3-healthy-foods`, `utm_content=sl19-short<N>`. YouTube descriptions name the full video, "3 Healthy Foods That Made Me Fat", and carry the AI line. Captions written by `dan-voice-writer`.

## Pinned comments (dan-voice-writer)
- Short 1: "A 1 liter carton of coconut water is about 180 calories and 40 grams of sugar. How much coconut water do you drink in a day?" Posts and pins automatically after release (routine youtube-pinned-comment-daily).
- Short 2: "One cup of trail mix is about 700 calories, more than a Big Mac. Do you measure out a serving, or eat it straight from the bag?" Posts and pins automatically after release (routine youtube-pinned-comment-daily).
- Short 3: "Which of these four is your go-to snack: sardines, hard-boiled eggs, rotisserie chicken or the Chipotle protein cup?" Posts and pins automatically after release (routine youtube-pinned-comment-daily).

## Copies
- Extreme: `/Volumes/Extreme/Short-form video content/healthyfoods SL-19/` (three masters and six covers md5-matched, picks.json).
- Google Drive: `Short-form video content/healthyfoods SL-19/`, anyone with the link: https://drive.google.com/open?id=1EpqmVXOiWppFWpBPk-jT4ag4pxsaGHL1 (rclone check: 10 matching files).

## After release
- Captions are burned in; no SRT. Articles: written by sixpackabs-article-gap-daily after release.
- After each YouTube release, check the public Shorts tile shows the approved cover (`/video-setup`, "YouTube Shorts cover verification"); the cover monitor checks all four platforms.
- Edit Queue: SL-19 `uploaded` (as SL-07 while waitlisted), mirrored to the page, synced.
