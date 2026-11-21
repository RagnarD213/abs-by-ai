# SL-05 Stop Deadlifting shorts: covers for all five shorts (Codex half)

**Written 2026-10-01 by Claude (Opus 5.5) for Codex.** Standing split (Dan, 2026-09-25 and 2026-09-30): **Codex makes the
covers in its own task, Claude uploads and sets up.** This task is covers only. Do not upload, schedule, post or touch
YouTube, Blotato or any social account. Dan hands the finalized cover paths to the Claude setup task
(`Handoffs/handoff-20261001-sl05-shorts-video-setup.md`) himself.

## 1. The shorts (all five FINALIZED by Dan, 2026-10-01: "Both are finalized", after "Everything else is looking good")
Folder: `Short-form video content/`. Notes, topics and the posting order: `Short-form video content/stop-deadlifting-SHORTS.md`.
Parent: Zeeshan's "Stop Deadlifting" long-form,
`Zeeshan Content Videos/stop deadlifting - video 3/stop deadlifting | zeeshan | 16x9 | video 3.mp4` (approved; public Sun Oct 11).

| # | file | length | on-screen small line / headline | suggested post title | sha256 (first 16) |
|---|---|---|---|---|---|
| 1 | `stop-deadlifting-short1_deadlifts-cause-more-injuries.mp4` | 56.9 s | STOP DOING DEADLIFTS / MORE INJURIES THAN EVERY OTHER LIFT | Deadlifts Cause More Injuries Than Every Other Lift | `b67c57ccdc6852c5` |
| 2 | `stop-deadlifting-short2_safer-lifts-build-more-muscle.mp4` | 50.2 s | BUILD MORE MUSCLE / SAFER LIFTS WIN LONG TERM | Safer Lifts Build MORE Muscle Long Term | `4e47fc961a08f59d` |
| 3 | `stop-deadlifting-short3_deadlifts-build-a-powerlifter-body.mp4` | 50.9 s | WANT AN AESTHETIC BODY? / DEADLIFTS BUILD A POWERLIFTER BODY | Deadlifts Build A Powerlifter Body, Not An Aesthetic One | `51c89fab6871185f` |
| 4 | `stop-deadlifting-short4_two-back-exercises-instead-of-deadlifts.mp4` | 59.1 s | SKIP THE DEADLIFT / 2 BACK EXERCISES TO DO INSTEAD | 2 Back Exercises To Do Instead Of Deadlifts | `44a35a16779c29e7` |
| 5 | `stop-deadlifting-short5_train-legs-without-deadlifts.mp4` | 38.3 s | SKIP THE DEADLIFT / TRAIN LEGS WITHOUT DEADLIFTS | Train Legs Without Deadlifts | `4381f541c459fc36` |

All five need a cover. Cover copy: start from the on-screen headline of each short (Dan saw these titles and asked for no
change). Keep the copy the same across a short's five options.

## 2. Rules (read these first)
- `.claude/skills/coverimage/SKILL.md` in full: most ripped source image, grid-safe crop, the two outputs per short
  (`posted covers/` for Instagram/Facebook/TikTok and `posted covers/youtube/` for the YouTube Short, 1080x1920 canvas).
- `.claude/skills/_shared/VIDEO-RULES.md`, "Five cover and thumbnail choices per video". **Five visual options per short:**
  1. one pool-shoot photo;
  2. and 3. two different real studio photos, each on a bold topic-specific background in the Jelly Beans cover family
     (reference `Short-form video content/covers/review/jelly-bean-refresh/B3-jelly-beans-beat-soda-tight.png`);
  4. one enhanced screenshot from the approved finished parent video (keep Dan's identity, physique and the exercise);
  5. one designer choice.
  Each option has an Instagram layout and a YouTube layout; the pair counts as one option.
- Same file, cover rules: text never on Dan's face, hair or abs (measure with a person mask on the rendered cover); never a
  frowning photo (`photos/finalized social media photos/Frowning Photos/`); Speedo photos cropped at the waistband; no
  "Real picture of me" label and no AbsByAI.com on covers; abs visible, never soft or undefined.
- The closest precedent is SL-04 (same editor, same kind of batch): `Handoffs/handoff-20260930-sl04-shorts-covers-codex.md`,
  build folder `Short-form video content/covers/review/sl04-covers-20260930/round2-five-options/`, finals in
  `Docs/SL04_COVER_FINALS_20260930.md`. Dan picked the enhanced screenshot (option D) for all four there: "Love what you
  did with the screenshots." Make that option strong here too, but still show all five.
- Screenshot sources in the parent (16:9, seconds): short 1 talking 117-140 and 193-224; short 2 talking 241-288; short 3
  talking 296-298, 321-338, 350-363; short 4 Dan's lat demonstration 402-411 (he raises each arm and points at his lat, a
  good cover frame) and talking 393-402; short 5 talking 428-466. Zeeshan's AI clips and stock in the parent are not Dan:
  do not use them as the cover subject.
- Graphic set note (Dan, 2026-10-01): SL-05's in-video graphics are the last in the old olive set. Covers follow the cover
  rules above, not the in-video graphics. Do not carry the olive bar onto a cover.

## 3. Deliver
1. Work in `Short-form video content/covers/review/sl05-covers-20261001/` (recipe, assets, prompts, outputs, `quality-checks.json`).
2. QC every cover on the rendered file: person-mask clearance of all text, abs visible where the photo shows them, grid-safe
   at Instagram's profile-grid crop, legible at feed size.
3. Show five options per short (letters A pool, B and C studio, D enhanced screenshot, E designer choice), Instagram and
   YouTube layouts, on two review sheets (`REVIEW_sl05_five-options_instagram.jpg`, `REVIEW_sl05_five-options_youtube.jpg`)
   and a local paired gallery. **Stop for Dan's five picks.**
4. After the picks: export each chosen cover to
   `Short-form video content/covers/posted covers/stop-deadlifting-short<N>_<slug>_cover-<letter>.png` and its
   `posted covers/youtube/` twin, copy all ten into `Short-form video content/covers/approved-sl05-for-Claude/`, write
   `Docs/SL05_COVER_FINALS_<date>.md` with paths and hashes, and give Dan the exact paths. No upload or scheduling.
5. Update `Handoffs/README.md` (this row) and the board's HANDOFFS line; commit and push only your files (docs and scripts,
   never media: the repo is public). The shared checkout has other sessions' uncommitted work: never `git stash -u`.
6. Spend: built-in image generation as in SL-04; any metered generation stays inside the standing $25 per session.

## 4. Model and starter prompt
Codex (GPT-6 Astra), effort medium (image work per `model-routing-plan`; a known recipe with a precedent).

> Read `Handoffs/handoff-20261001-sl05-shorts-covers-codex.md` in full and do only what it asks: build five visual options each for the five SL-05 Stop Deadlifting shorts (one pool photo, two studio photos on Jelly Beans style backgrounds, one enhanced video screenshot, one designer choice), in Instagram and YouTube layouts, send me the review sheets and stop for my picks, then export the finals and give me the paths. Do not upload or schedule anything.
