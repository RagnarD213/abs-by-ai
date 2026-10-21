# First Step Abs AD setup, October 21, 2026

**AD.** RA-12 "The First Step To Getting Abs Isn't A Workout" R2 9:16, approved by Dan 2026-10-21 ("Okay, everything is finalized and approved. Let's proceed to setup."). Closing words, transcribed from the exact file: "So take the first step. Tap the button below to see yourself with abs." Only the 9:16 exists; no 16:9 film was built.

Master `Claude Ad Videos/the first step to getting abs isnt a workout - RA-12/the first step to getting abs isnt a workout | claude | 9x16 | RA-12.mp4`, SHA-256 `18728d49ab7a8e0f4dd43f0a8aa63554f8edb627362abc1b088e1ab98d94b539`, checked before the upload. Uploaded unchanged; no render. Delivery checks were already done on this file (stamps beside it).

## Thumbnails

Round 1: five designs by Codex (gpt-6.1-sol, high) through `codex-image.sh`, headline THE FIRST STEP / ISN'T A WORKOUT: (1) real pool photo-125 on a golden-hour pool, white band; (2) real studio-blue-11 in front of a cork vision board, handwritten card; (3) AI Dan holding a goal print with its back to the viewer; (4) a different man presenting his phone like a trophy, acid yellow; (5) a giant phone in sprint starting blocks. Dan: "I don't like any of these. I want three new designs with image number 2 and two other similar images. Change the text to 'The key to getting abs' and make three unique designs."

Round 2, planned and plated by Codex: (A) real studio-blue-11 in front of an open vault with a gold key, Arial Black white and gold; (B) real studio-blue-222 inside a glowing cyan frame, Impact on two yellow bands; (C) real studio-blue-145 beside a hanging chrome key in an orange room, Rockwell Bold. Dan: "Let's go with design A, but in the horizontal, I want to move the text up and make the key fully visible beneath the text." His body hid the key's toothed end in the 16:9, so Codex re-made that plate with the key moved left onto open floor (`r2/A2_16x9.png`) and the headline went above it.

Files: `social media graphics/youtube/thumbnails/RA-12 The First Step To Getting Abs/FINAL-APPROVED/` (9:16 installed, 16:9 kept). Every file passed text clearance (face, hair, abs) and the 2 MB limit. No paid image API; Replicate only for the photo-125 cutout and the transcript, cents each.

## YouTube

| YouTube | Thumbnail | Status read back |
|---|---|---|
| [7bsTcr0vu6Y](https://youtu.be/7bsTcr0vu6Y) | Round 2 A, THE KEY TO GETTING ABS vault | unlisted, processing succeeded, embeddable |

Channel `UC236gjadarHAhEhOMYNGJ9g` (Dan Rose Fitness). Title "The First Step To Getting Abs", category 26, not made for kids, synthetic=true (AI lock screen 11.5-12.9 s, AI beginner 14.0-15.5 s, app generation 16.8-21.7 s, analysis card 26.8-33.7 s, AI trainer demo 33.7-39.3 s), tags ab workout, abs by ai, ai fitness, six pack abs, ai goal picture, see yourself with abs. Description has no chapters, links the homepage with `dgen-trial-ra12` UTMs, carries the AI sentence, no em dash. Served thumbnail read back and checked by eye.

## Google Ads

Trial campaign `24316364155`, ad group `202084443740` "RA-12 The First Step To Getting Abs", ENABLED, $40 target CPA (RA-14 reference), Audience `359952376`, US + CA, English. Ad `828687867099`, ENABLED, REVIEW_IN_PROGRESS. Final URL on absbyai.com/start with `utm_content=claude-9x16-vsl`, HTTP 200. validateOnly passed before apply. Budget `15911255930` read $30/day before and after; campaign status untouched. Policy report 10-21: nothing in the campaign disapproved or limited. Recheck 10-22.

A trial (tap-the-button) ad, so not one of the engagement "AT ·" ads that go in all three engagement campaigns.

## Records

Edit queue RA-12 set to `uploaded` after the readback and the Ads entry (Drive status file and artifact db v5). Setup handoff removed from the OPEN index. No organic posting, public upload or pinned comment. Victory Dashboard skipped (paused).

Recipe: `.claude/skills/ad-setup/reference/ra12-setup-20261021/` (build.py round 1, build_r2.py round 2, Codex plans and prompts, QC, generation receipts, policy). Config/result: `scripts/ads/api/dgen-ads/ra12.json`, `ra12.result.json`.
