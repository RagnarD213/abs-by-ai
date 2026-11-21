CONTENT | SL-07 | If I Had Belly Fat SFC Setup

# SL-07 If I Had Belly Fat shorts (5): covers, then upload and schedule

Written 2026-10-18 by Claude (Opus 5.5). Five Shorts (`SFC`) cut from the long-form RO-16 "If I Had Belly Fat, Here's How
I'd Lose It In 90 Days". One Claude handoff covers both halves (Dan's rule, 2026-10-01). **Recommended: Claude Opus 5.5,
high effort** (cover design is editorial work; memory `model-routing-plan`). **Use the Codex subscription to generate the images.**

Dan finalized all five on 2026-10-18: *"Okay, everything is finalized and approved. You can now proceed to set up."* That
approves the shorts exactly as delivered in round 3: pickups as shipped (short 2 band-matched, short 3 film voice EQ), every
new clip kept, the four reworded key points kept, no "Today's total" change in short 5, and no vacation clip (the ab wheel
stays in short 3). Queue: SL-07 `finalized`. Supersedes `handoff-20261016-sl07-round4-after-dan-r3-review.md` (not needed).

## Read first
1. `.claude/skills/_shared/VIDEO-RULES.md` in full (the five cover choices, made by Codex; Blotato only for organic YouTube;
   AI label; Speedo crop; frowning photos; cover text never over his face or hair).
2. `.claude/skills/_shared/IMAGE-GENERATION.md` and `/coverimage` (locked cover type, grid-safe crop).
3. `/video-setup`: "Shorts", "YouTube Shorts cover verification", "Covers on all platforms" (cover_audit preflight,
   Facebook cover registry), "Blotato full?" (waiting list). Closest worked examples: `Docs/SL03_SETUP_RECEIPT_20261008.md`,
   `Handoffs/handoff-20261008-sl03-daily-salad-shorts-covers-and-setup.md`.

## 1. The five files (final; never re-render or re-edit)

Folder `Short-form video content/`, 1080x1920, 29.97 fps, captions burned in (no `.srt`), `.audio_gate.json` and
`.deliver_gate.json` (PASS 39/39, gate 2.6.1) beside each. **Ignore the `... 2.mp4` files there: they are old round 2
sync duplicates.** Re-hash before any upload; a mismatch means the file changed after approval: stop and tell Dan.

| # | file | length | on-screen title (eyebrow LOSE YOUR BELLY FAT) | AI flag | sha256 (first 8) | release slot (calendar) |
|---|---|---|---|---|---|---|
| 1 | `belly-fat-90-days-short1_stop-trying-to-lose-1-pound-a-week.mp4` | 52.1 s | Stop Trying To Lose 1 Pound A Week | false | `b55cf957` | Mon Dec 21 |
| 2 | `belly-fat-90-days-short2_weigh-yourself-every-morning.mp4` | 51.4 s | Weigh Yourself Every Morning | true (AI scale and praying clips) | `1ebf30e5` | Tue Dec 22 |
| 3 | `belly-fat-90-days-short3_work-out-every-morning.mp4` | 56.7 s | Work Out Every Morning, Not 3 Times A Week | true (AI stairs clip) | `eedadc47` | Sat Dec 26 |
| 4 | `belly-fat-90-days-short4_the-3-pound-rule.mp4` | 43.0 s | The 3-Pound Rule That Keeps Belly Fat Off | true (AI beer clip) | `088b3898` | Mon Dec 28 |
| 5 | `belly-fat-90-days-short5_track-your-calories-with-a-photo.mp4` | 47.5 s | Track Your Calories With A Photo | true (AI measuring-cups clip) | `4a971479` | Tue Dec 29 |

Slots are from `Docs/SHORTS_RELEASE_CALENDAR.md` (approved 2026-10-17), 9 AM Central. The parent RO-16 releases on YouTube
Sun Dec 20 per `Docs/LONGFORM_RELEASE_CALENDAR.md`: read the live Blotato queue for its actual slot first. No short goes out
before the parent is public; if the parent moved, move the shorts with it.

**All five are ORGANIC.** Closing words: 1 "...and everything else would have to fit around that."; 2 "...and hope the scale
is going to move."; 3 "...and that's the reason why."; 4 "...Losing 30 pounds is 90 days of sacrifice."; 5 "...you'll be
shocked at how much faster you start losing fat." No "tap the button". Short 5 names AbsByAI.com's free macro tracker.
Run the classification step and `python3 scripts/blotato/ad_guard.py --scan` before and after every Blotato write.

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
  text clear of his face and every part of his hair. Title case (VIDEO-RULES 2026-10-16).
- Photos: defined abs, no frowning photos, Speedo crop at the waistband, ten or more different photos across the set, none
  already on the grid (`Short-form video content/covers/posted covers/`).
- Topic images for the AI designs: the bathroom scale (shorts 1, 2, 4), early-morning workout (3), food photo and phone
  calorie tracking (5), a calendar of 90 days (1).
- Measure every cover before showing it (person mask: text clear of face and hair, abs uncovered; Instagram inside the
  grid-safe centre; YouTube JPEG 1080x1920 under 2 MB). A Codex background with warped objects or garbled text is redone.
- One review sheet of all 25 (grouped by short), `SendUserFile`, **stop for Dan's picks**. Export picks to
  `Short-form video content/covers/approved-sl07/` as `Instagram_<file slug>_cover-<letter>.png` and
  `YouTube_<file slug>_cover-<letter>.jpg`.

## 3. Upload and schedule (second half, after the picks)

1. Board: one ACTIVE line. Copies: Extreme `/Volumes/Extreme/Short-form video content/belly-fat SL-07/` and Google Drive
   `Short-form video content/belly-fat SL-07/` (masters + covers, md5-matched, Drive folder anyone-with-link). The Extreme
   drive was full on 10-16: check free space first.
2. Per short: `tiktok_cover.build()` (absolute paths) with the Instagram cover as frame 0; upload master, TikTok copy,
   Instagram PNG and YouTube JPEG with `blotato_create_presigned_upload_url` and hash-check each download; write
   `scripts/blotato/configs/sl07-short<N>-<slug>.json` (copy an `sl03-short*` config; `content_type` organic, `source`,
   keyword `FOOD` as RO-16 used, `utm_content=sl07-short<N>`, `ai_generated` per the table, `"pinned_comment"` through
   `dan-voice-writer`, YouTube description naming the full video by title). Register each Facebook cover in
   `scripts/blotato/fb_reel_covers.json` and the live installer (`/video-setup`, "Covers on all platforms").
3. `python3 scripts/blotato/cover_audit.py`, then `python3 scripts/blotato/organic_short_queue.py <config>` dry run, then
   `--apply`; read back all four posts per short. If Blotato is full, finish everything else and add each short to
   `scripts/blotato/video_waitlist.json` (kind `short`); the daily routine queues it. Never create a one-video task.
4. Close: `BLOTATO_QUEUE_PROGRESS.md` section, receipt `Docs/SL07_SETUP_RECEIPT_<date>.md` (schedule ids, cover hashes,
   pinned comments, "articles: written by the routine after release"), `queue.py set SL-07 uploaded` + Edit Queue artifact
   (`jobs/SL-07` was version 8 on 2026-10-18; pin `if_version`) + `mark-synced`, board one-liner, commit and push.

## Starter prompt

> Name this task "If I Had Belly Fat SFC Setup". This is CONTENT. Read `Handoffs/handoff-20261018-sl07-belly-fat-shorts-covers-and-setup.md` and execute it: make five cover choices for each of the five If I Had Belly Fat shorts, show me one review sheet and stop for my picks, then upload and schedule all five on every platform through Blotato on the shorts calendar dates. Use the Codex subscription to generate the images.
