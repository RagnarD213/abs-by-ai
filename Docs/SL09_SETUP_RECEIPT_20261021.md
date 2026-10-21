# SL-09 Oura Ring Review shorts: setup receipt (2026-10-21)

Task `Oura Ring Review SFL Setup`, Claude Opus 5.5. Handoff `Handoffs/handoff-20261021-sl09-oura-shorts-covers-and-setup.md`.

## Checks before any write
- Masters re-hashed: SHA-256 prefixes match the handoff (0b5b7018, 5c8fa50f, 351d88c7, 6f532eba, 51fa0c50). Not re-edited.
- Classification: all five ORGANIC. Closing words: 1 "low risk workouts so that way you don't get injured."; 2 "they need to go."; 3 "as a result of cutting out that fast driving."; 4 "even if it is not the Oura Ring."; 5 "there's no subscription and the cost is low." No "tap the button". `ad_guard.py --scan` CLEAN before (170 posts) and after (190).
- Parent "My Honest Oura Ring Review After 1.5 Years" YouTube schedule `5095442` is Wed Nov 11 2026 15:00Z (read live 2026-10-21); socials Thu Nov 12 noon. Every short follows it.

## Covers
Round 1: five per short (A pool, B studio on a Codex scene, C AI image of Dan, D and E Codex designs), 20 Codex GPT-6.1 Sol high images on the subscription, 50/50 measured checks. Dan picked 2 C and 5 D, asked for new AI zombie designs for 1 and 4 and a new bottom picture on 3 E. Round 2: 7 more Codex images (two short 1 G retakes rejected by Claude: too wide, then cut at the waist), 62/62 checks (short 1 G body row waived by eye: type over his legs in shadow). Dan, round 2: "Let's go with F for short one, and E looks good for short two. Go ahead and install these." Read as short 1 F and short 3 E (the second row on the sheet); **short 4 had no letter, so F (yellow band, as short 1) was used: swap before Nov 23 if Dan names G or H.** Builder, prompts, checks: `scripts/covers/sl09-20261021/`. Exports and full hashes: `Short-form video content/covers/approved-sl09/picks.json`. Review page: http://127.0.0.1:8909/.

## Queued (Blotato, 9 AM Central, all four platforms)
Order of ids: Facebook / Instagram / TikTok / YouTube.

| short | title | slot | cover | AI flag | master / TikTok sha256 | IG PNG / YT JPG sha256 | schedule ids | config |
|---|---|---|---|---|---|---|---|---|
| 1 | Train Harder After A Bad Night's Sleep | Fri Nov 13 9 AM (2026-11-13T15:00Z) | F | no | `0b5b7018` / `772fef18` | `91b18f49` / `8f7eb3e3` | 5867678 / 5867679 / 5867680 / 5867682 | `sl09-short1-train-harder-after-a-bad-nights-sleep.json` |
| 2 | Your Sleep Score Shows Who's Toxic In Your Life | Mon Nov 16 9 AM (2026-11-16T15:00Z) | C | no | `5c8fa50f` / `8177cf32` | `f1b15c7c` / `760df510` | 5867684 / 5867685 / 5867687 / 5867688 | `sl09-short2-your-sleep-score-shows-whos-toxic.json` |
| 3 | Cut The Adrenaline Before Bed | Fri Nov 20 9 AM (2026-11-20T15:00Z) | E | yes | `351d88c7` / `17461c6a` | `12cb1d4a` / `e32080ae` | 5867691 / 5867694 / 5867698 / 5867701 | `sl09-short3-cut-the-adrenaline-before-bed.json` |
| 4 | You're Not Sleeping As Well As You Think | Mon Nov 23 9 AM (2026-11-23T15:00Z) | F | yes | `6f532eba` / `b79e3de8` | `a2227d3f` / `ff0b0080` | 5867702 / 5867703 / 5867704 / 5867706 | `sl09-short4-youre-not-sleeping-as-well-as-you-think.json` |
| 5 | Oura Ring Or WHOOP? Which One To Buy | Fri Nov 27 9 AM (2026-11-27T15:00Z) | D | yes | `51fa0c50` / `1fbdd815` | `3a1ab00c` / `a48e96cf` | 5867711 / 5867713 / 5867715 / 5867716 | `sl09-short5-oura-ring-or-whoop-which-one-to-buy.json` |

- All 20 uploads downloaded back from their public URLs and SHA-256 matched; after queueing, all 20 Blotato-hosted videos downloaded again and matched (Blotato re-hosts under new URLs).
- Read back: times, Instagram and YouTube cover URLs, YouTube title and AI flag, TikTok `videoCoverTimestamp: 0` and AI flag all as configured.
- TikTok copies: `tiktok_cover.build()` with the Instagram cover as frame 0 (video +1 frame, audio packets identical, frame 0 PSNR 34.7 to 38.1 dB, checked side by side). In `/Volumes/Expansion/_edit_work/sl09-publish/`.
- Facebook covers (YouTube layout JPEG) registered in `scripts/blotato/fb_reel_covers.json` and the live installer `~/.absbyai/fb-reel-covers/`, matched on each caption's first line. `cover_audit.py`: no issues.
- Keyword SLEEP (as the parent), campaign `oura-ring-review`, `utm_content=sl09-short<N>`. YouTube descriptions name the full video by title; shorts 3 to 5 carry the AI-clips line.
- Slots: Fri Nov 13 per the calendar; 2 to 5 took the next free Mon/Fri slots, keeping the Zepbound Tips Saturdays. `Docs/SHORTS_RELEASE_CALENDAR.md` updated (four not-yet-edited Shorts moved later).

## Pinned comments (dan-voice-writer)
- Short 1: After a bad night of sleep, do you go harder in the gym or take the day easy?
- Short 2: Has a person in your life ever wrecked your sleep? Ex, boss or family?
- Short 3: What's the last thing you do before bed: phone, TV, or something else?
- Short 4: How many hours of sleep do you think you get on a normal night?
- Short 5: Oura Ring or WHOOP: which one are you wearing, or are you not tracking your sleep yet?
Posts and pins automatically after release (routine youtube-pinned-comment-daily).

## Copies
- Extreme: `/Volumes/Extreme/Short-form video content/oura SL-09/` (five masters md5-matched, ten covers, picks.json).
- Google Drive: `Short-form video content/oura SL-09/`, anyone with the link: https://drive.google.com/open?id=1lcXYeAeeCAsY4bIYYn5f5ah-WLJN4dGv (five masters md5-matched, ten covers, picks.json)

## After release
- Captions are burned in; no SRT. Articles: written by the routine after release.
- After each YouTube release, check the public Shorts tile shows the approved cover (`/video-setup`, "YouTube Shorts cover verification"); the cover monitor checks all four platforms.
