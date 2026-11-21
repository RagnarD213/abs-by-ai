# RO-05 "How I Make My Daily Salad": YouTube thumbnail options (Codex half)

**Written 2026-09-30 by Claude (Opus 5.5) for Codex.** Standing split for every organic content video (Dan, 2026-09-30):
**Codex makes the thumbnail, Claude uploads and sets up.** This task is the thumbnail only. Do not upload, schedule, post or touch
YouTube, Blotato or any social account. Dan hands the finalized thumbnail to the Claude setup task
(`Handoffs/handoff-20260930-ro05-video-setup.md`) himself.

## 1. The video
- Approved by Dan 2026-09-30 ("this video is approved and good to go"). Organic content video, 14:53.86.
- Master: `claude edited long form content/08 - How I Make My Daily Salad (Fable recut)/How I Make My Daily Salad | claude round 4 | 16x9 | RO-05.mp4`
  (sha256 `23fdcb0c86469cb7...`). Chapters beside it (`...RO-05.chapters.txt`). Ignore the older `| fable |` file (rejected cut).
- What it is: Dan's daily meal-prep salad, built in his kitchen. Seven glass bowls made at once and kept fresh for 7 days; about
  700 calories and about $4 a bowl; arugula, carrots, grape tomatoes, broccolini, English cucumber, red onion, olive oil and vinegar
  dressing, rotisserie chicken, hard-boiled eggs, olives, pico de gallo; he tracks it with the Abs By AI app. In the footage he wears a
  black tank top and blue gloves, so **no frame of the video shows his abs**.
- Good salad frames: the finished salad close-ups at 0:03 to 0:08 (C1550 111.0-113.8, 115.0-119.6 in the raw roll), the layered
  bowls top-down at 1:44 to 1:47, the seven sealed containers at 7:00 to 7:10. Dan holding the sealed glass bowl: about 6:30 to 6:55.

## 2. Rules (read these files first)
- `.claude/skills/video-setup/SKILL.md` Step 2 (the five-variation mix and the working build to copy:
  `social media graphics/youtube/thumbnails/Ab Wheel Workout/_build-2026-09-13/build.py`, $0, reuses existing assets).
- `.claude/skills/youtube-packaging/SKILL.md` (type system, frowning-photos rule, waistline crop, text never on Dan).
- Dan's standing rules, in short: Manrope ExtraBold white caps with the red accent bar `rgb(201,48,45)`, logo recoloured white; never
  a blur; fill the frame with the photo; **abs visible in every variation and text never over them**; never a frowning photo
  (p135 and p138 are frowning); real shoot photos over video frames, never soft or folded posture; Speedo photos cropped at the
  waistband; short big copy (two lines beat three), no claims or result numbers.
- Standing mix: two pool-shoot photos, two studio photos, one video-based variation. **For this video the video-based slot is
  food-forward:** the finished salad close-up (or the seven sealed bowls) as the scene with a real studio or pool cutout of Dan
  (`photos/finalized social media photos/_cutouts/`), so the abs rule still holds. Same headline on all five.
- Headline direction (your call, keep it short): about the daily salad, e.g. `MY DAILY SALAD` or `MY 7-DAY SALAD`. The title is
  written later by the Claude task, so the thumbnail should not repeat a full sentence.
- Rotate photos away from what the last few long-forms used (`social media graphics/youtube/thumbnails/`).
- Cost: $0 expected (existing assets). Any AI generation over $5 needs Dan first.

## 3. Deliver
1. Build in `social media graphics/youtube/thumbnails/How I Make My Daily Salad/_build-2026-09-30/` (recipe + outputs).
2. QC each on the rendered file: person-mask clearance of the text, abs visible, nothing clipped, legible at feed size (320 px wide).
3. One review sheet `REVIEW_ro05_thumbnails.jpg` with the five labelled 1 to 5; send it to Dan and stop for his pick (he may pick two
   for an A/B test).
4. After the pick: export `How I Make My Daily Salad - thumbnail FINAL.jpg` (and `... FINAL B.jpg` if he picks two) in
   `social media graphics/youtube/thumbnails/How I Make My Daily Salad/`: 1280x720, JPEG, under 2 MB. Give Dan the exact path(s);
   he pastes them into the Claude setup task.
5. Update `Handoffs/README.md` (this row: executed, with the final path) and your board entry; commit and push only your files. The
   shared checkout has other sessions' uncommitted work: never `git stash -u`.

## 4. Model and starter prompt
Codex (GPT-6 Astra), effort medium.

> Read `Handoffs/handoff-20260930-ro05-thumbnails-codex.md` in full and do only what it asks: build five YouTube thumbnail options for RO-05 "How I Make My Daily Salad", send me the review sheet and stop for my pick, then export the final 1280x720 JPEG and give me its path. Do not upload or schedule anything.
