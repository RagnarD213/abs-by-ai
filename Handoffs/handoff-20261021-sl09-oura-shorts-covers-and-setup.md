CONTENT | SL-09 | Oura Ring Review SFL Setup

# SL-09 Oura Ring Review shorts (5): covers, then upload and schedule

Written 2026-10-21 by Claude (Opus 5.5). Five Shorts (`SFL`) cut from Zeeshan's finished long-form "My Honest Oura Ring Review
After 1.5 Years" (Video 4). One Claude handoff covers both halves (Dan's rule, 2026-10-01). **Recommended: Claude Opus 5.5,
high effort** (cover design is editorial work; the video was edited on Claude; memory `model-routing-plan`). **Use the Codex
subscription to generate the images.**

Dan finalized all five: shorts 1-3 on 2026-10-20 (*"Short one looks good. This is finalized... That's finalized. Short 3
looks good. This is finalized."*), shorts 4-5 on 2026-10-21 (*"finalized"*, after round 5 trimmed short 4's AI opener to
0:02.8). Queue: SL-09 `finalized`. Edit history and recipe: `.claude/skills/shorts/reference/softblue-sl09/`.

## Read first
1. `.claude/skills/_shared/VIDEO-RULES.md` in full (the five cover choices made by Codex; Blotato only for organic YouTube;
   AI label rule; Speedo crop; frowning photos; cover text never over his face or hair).
2. `.claude/skills/_shared/IMAGE-GENERATION.md` and `/coverimage` (locked cover type, grid-safe crop).
3. `/video-setup`: "Shorts", "YouTube Shorts cover verification", "Covers on all platforms" (cover_audit preflight,
   Facebook cover registry), "Blotato full?" (waiting list). Closest worked example:
   `Handoffs/handoff-20261018-sl07-belly-fat-shorts-covers-and-setup.md` and its receipt `Docs/SL07_SETUP_RECEIPT_20261018.md`.
4. `Short-form video content/oura-SHORTS.md` (the batch card: titles, film ranges, AI flags).

## 1. The five files (final; never re-render or re-edit)

Folder `Short-form video content/`, 1080x1920, 29.97 fps, captions burned in (no `.srt`), Zeeshan's mix cut only, with
`.audio_gate.json` and `.deliver_gate.json` (PASS 39/39, gate 2.6.1) beside each. Re-hash before any upload; a mismatch
means the file changed after approval: stop and tell Dan.

| # | file | length | on-screen title (eyebrow) | AI flag | sha256 (first 8) |
|---|---|---|---|---|---|
| 1 | `oura-short1_train-harder-after-a-bad-nights-sleep.mp4` | 57.0 s | Train Harder After A Bad Night's Sleep | false | `0b5b7018` |
| 2 | `oura-short2_your-sleep-score-shows-whos-toxic.mp4` | 55.1 s | Your Sleep Score Shows Who's Toxic In Your Life | false | `5c8fa50f` |
| 3 | `oura-short3_cut-the-adrenaline-before-bed.mp4` | 55.9 s | Cut The Adrenaline Before Bed | true (Zeeshan's AI Tesla clip, 0:36-0:41) | `351d88c7` |
| 4 | `oura-short4_youre-not-sleeping-as-well-as-you-think.mp4` | 42.5 s | You're Not Sleeping As Well As You Think | true (AI opener, 0:00-0:02.8) | `6f532eba` |
| 5 | `oura-short5_oura-ring-or-whoop-which-one-to-buy.mp4` | 45.6 s | Oura Ring Or WHOOP? Which One To Buy | true (AI ring 0:00-0:03.7, ring and WHOOP 0:16.3-0:20.6) | `51fa0c50` |

**Release slots.** `Docs/SHORTS_RELEASE_CALENDAR.md` gives short 1 Fri Nov 13, 9 AM Chicago (two days after the parent);
shorts 2 to 5 take the next free Mon/Tue/Fri/Sat 9 AM slots after it in 2026 (every edited Short releases in 2026), never
before the parent is public. The parent is on `Docs/LONGFORM_RELEASE_CALENDAR.md` for **Wed Nov 11** (an older board line
says Sun Nov 8): read the live Blotato YouTube queue for its actual slot first and move the shorts with it.

**All five are ORGANIC.** Closing words: 1 "...low risk workouts so that way you don't get injured."; 2 "...certain people in your
life either need to change your behavior or they need to go."; 3 "...as a result of cutting out that fast driving."; 4 "...you gotta buy a sleep tracker,
even if it is not the Oura Ring."; 5 "...there's no subscription and the cost is low." No "tap the button". Run the
classification step and `python3 scripts/blotato/ad_guard.py --scan` before and after every Blotato write. Organic videos may
name Zepbound and other drugs; these name only Oura, WHOOP, Apple Watch and Fitbit.

## 2. Covers (first half; stop for Dan's picks)

Five choices per short, each in both layouts (Instagram grid and YouTube Shorts), which count as one choice:
1. one real pool-shoot photo of Dan; 2. one real studio-shoot photo of Dan; 3. one AI-enhanced or AI-generated image of Dan
in the short's subject; 4. and 5. two more AI images of Codex's choice (Dan or not). Five unique designs per short: write
one line per option naming its layout, type, colour and composition before building, and check no two share them.

- Codex makes all of them: `.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high`. No other model. Real
  photos are never redrawn (Codex makes the background; his cutout from `photos/finalized social media photos/_cutouts/` and
  the type are layered in code). For option 3 give Codex a real photo as reference, "lean and shredded, not bulky", and
  check the face reads as him.
- Copy: the short's title (same on all five). No claims or numbers as results, no AbsByAI.com, no "Real picture" label,
  text clear of his face and every part of his hair. Title case.
- Photos: defined abs, no frowning photos, Speedo crop at the waistband, ten or more different photos across the set, none
  already on the grid (`Short-form video content/covers/posted covers/`). Masculine palettes (memory `thumbnail-masculine-colours`).
- Topic images for the AI designs: the Oura ring and the sleep score (1, 4, 5), a heavy barbell vs a light dumbbell (1), a
  couple arguing or a crashing sleep graph (2), fast night driving and a phone sleep chart (3), a ring vs a WHOOP strap side
  by side (5). The AI frames already made for this batch (`/Volumes/Extreme/_edit_work/sl09/round2/aiframes/`: J1 ring on
  sheets, J2w ring and WHOOP, K1 thumbs-up man) are approved pictures Codex may use as references.
- Measure every cover before showing it (person mask: text clear of face and hair, abs uncovered; Instagram inside the
  grid-safe centre; YouTube JPEG 1080x1920 under 2 MB). A Codex background with warped objects or garbled text is redone.
- One review sheet of all 25 (grouped by short), `SendUserFile`, **stop for Dan's picks**. Export picks to
  `Short-form video content/covers/approved-sl09/` as `Instagram_<file slug>_cover-<letter>.png` and
  `YouTube_<file slug>_cover-<letter>.jpg`.

## 3. Upload and schedule (second half, after the picks)

1. Board: one ACTIVE line. Copies: Extreme `/Volumes/Extreme/Short-form video content/oura SL-09/` and Google Drive
   `Short-form video content/oura SL-09/` (masters + covers, md5-matched, Drive folder anyone-with-link). Check Extreme free
   space first.
2. Per short: `tiktok_cover.build()` (absolute paths) with the Instagram cover as frame 0; upload master, TikTok copy,
   Instagram PNG and YouTube JPEG with `blotato_create_presigned_upload_url` and hash-check each download; write
   `scripts/blotato/configs/sl09-short<N>-<slug>.json` (copy an `sl07-short*` config; `content_type` organic, `source`,
   the keyword the parent Oura long-form uses, `utm_content=sl09-short<N>`, `ai_generated` per the table, `"pinned_comment"`
   through `dan-voice-writer`, YouTube description naming the full video by title). Register each Facebook cover in
   `scripts/blotato/fb_reel_covers.json` and the live installer.
3. `python3 scripts/blotato/cover_audit.py`, then `python3 scripts/blotato/organic_short_queue.py <config>` dry run, then
   `--apply`; read back all four posts per short. If Blotato is full, finish everything else and add each short to
   `scripts/blotato/video_waitlist.json` (kind `short`); the daily routine queues it. Never create a one-video task.
4. Close: `BLOTATO_QUEUE_PROGRESS.md` section, receipt `Docs/SL09_SETUP_RECEIPT_<date>.md` (schedule ids, cover hashes,
   pinned comments, "articles: written by the routine after release"), `queue.py set SL-09 uploaded` + Edit Queue artifact
   (`jobs/SL-09` was version 9 on 2026-10-21; pin `if_version`) + `mark-synced`, board one-liner, commit and push.

## Starter prompt

> Name this task "Oura Ring Review SFL Setup". This is CONTENT. Read `Handoffs/handoff-20261021-sl09-oura-shorts-covers-and-setup.md` and execute it: make five cover choices for each of the five Oura Ring Review shorts, show me one review sheet and stop for my picks, then upload and schedule all five on every platform through Blotato on the shorts calendar dates. Use the Codex subscription to generate the images.
