# SL-04 Arms & Shoulders shorts: covers for shorts 1, 3, 4, 5 (Codex half)

**Written 2026-09-30 by Claude (Opus 5.5) for Codex.** Standing split (Dan, 2026-09-25 and 2026-09-30): **Codex makes the covers
in its own task, Claude uploads and sets up.** This task is covers only. Do not upload, schedule, post or touch YouTube, Blotato
or any social account. Dan hands the finalized cover paths to the Claude setup task
(`Handoffs/handoff-20260930-sl04-shorts-video-setup.md`) himself.

## 1. The shorts (all five FINALIZED by Dan, 2026-09-30)
Folder: `Short-form video content/`. Notes and the approved posting order: `Short-form video content/arms-shoulders-SHORTS.md`.

| # | file | on-screen eyebrow / title | cover needed |
|---|---|---|---|
| 1 | `arms-shoulders-short1_make-your-waist-look-smaller.mp4` (52.0 s) | TRAIN YOUR SHOULDERS / MAKE YOUR WAIST LOOK SMALLER | **yes** |
| 2 | `arms-shoulders-short2_do-this-before-you-take-your-shirt-off.mp4` (56.1 s) | 2-MINUTE HOME ARM WORKOUT / DO THIS BEFORE YOU TAKE YOUR SHIRT OFF | **no: cover B is approved** |
| 3 | `arms-shoulders-short3_raise-your-elbows-not-your-hands.mp4` (30.9 s) | SIDE LATERAL TIP / RAISE YOUR ELBOWS, NOT YOUR HANDS | **yes** |
| 4 | `arms-shoulders-short4_stop-swinging-your-curls.mp4` (28.2 s) | BICEP CURL MISTAKE / STOP SWINGING YOUR CURLS | **yes** |
| 5 | `arms-shoulders-short5_how-to-do-bicep-curls.mp4` (51.6 s) | 2 WAYS TO DO THEM / HOW TO DO BICEP CURLS | **yes** |

- **The in-batch style reference is short 2's approved cover B:**
  `Short-form video content/covers/posted covers/arms-shoulders-short2_do-this-before-you-take-your-shirt-off_cover-B.png` and its
  `posted covers/youtube/` twin. Build 1, 3, 4, 5 to sit beside it on the grid.
- The earlier A/B covers for 1, 3, 4, 5 are in `posted covers/_rejected-sl04/`. **Dan did not keep them; do not resubmit them
  unchanged.** Their builders (`posted covers/_build-covers-sl04.py`, `_build-covers-sl04-youtube.py`) are a starting point for
  sizes and type, not for the photo choices.
- Short 1's ending was re-cut on 09-30 (it now ends on live-round side-lateral reps); its cover topic is unchanged: shoulders
  make your waist look smaller.

## 2. Rules (read these first)
- `.claude/skills/coverimage/SKILL.md` in full: most ripped source image, grid-safe crop, locked J2 type, **five visual options**, and
  the two outputs per short (`posted covers/` for Instagram/Facebook/TikTok, `posted covers/youtube/` for the YouTube Short,
  1080x1920 canvas).
- `.claude/skills/_shared/VIDEO-RULES.md` cover rules: text never on Dan's face, hair or abs (measure with a person mask on the
  rendered cover); never a frowning photo (`photos/finalized social media photos/Frowning Photos/`); Speedo photos cropped at the
  waistband; no "Real picture of me" label and no AbsByAI.com on covers; abs visible, never soft or undefined.
- The latest approved queue-cover design and QC method: `Docs/QUEUE_COVERS_APPROVALS_20260926.json` and
  `Handoffs/handoff-20260926-queue-covers-r4-unfinished-only.md` (platform layouts, grid crops, quality-checks).
- **Updated by Dan, 2026-09-30:** each short gets one pool photo, two different studio photos on topic-specific Jelly Beans style backgrounds, one enhanced screenshot from its approved finished parent video, and one designer choice. Keep the copy consistent. This supersedes the original two-option brief.
- Reference: `Short-form video content/covers/review/jelly-bean-refresh/B3-jelly-beans-beat-soda-tight.png`.
- Follow `.claude/skills/_shared/VIDEO-RULES.md`, "Five cover and thumbnail choices per video". Dan explicitly requested image/design alternatives and screenshot enhancement. Built-in image_gen was used for two scene plates and four screenshot enhancements; it did not report a dollar cost. Studio portraits were composited from existing real cutouts.

## 3. Deliver
1. Round 2 lives in `Short-form video content/covers/review/sl04-covers-20260930/round2-five-options/` (recipe, assets, prompts, outputs and `quality-checks.json`). Original A/B review remains in its parent folder.
2. QC every cover on the rendered file: person-mask clearance of all text, abs visible, grid-safe crop checked at Instagram's
   profile-grid crop, legible at feed size.
3. Show five options per short, each with separate Instagram and YouTube layouts. Letters: A pool, B red-gym studio, C blue-home-gym studio, D enhanced exercise screenshot, E clean editorial. Review sheets: `REVIEW_sl04_five-options_instagram.jpg` and `REVIEW_sl04_five-options_youtube.jpg`, with short 2 approved B beside them. Local paired gallery: `http://127.0.0.1:8798/`. Stop for Dan's four picks.
4. After the picks: export each chosen cover to `posted covers/arms-shoulders-short<N>_<slug>_cover-<A|B|C|D|E>.png` and its `posted covers/youtube/` twin. Use the round-2 source files, because letters B-E differ from the original A/B review. Give Dan exact paths for all four shorts. No upload or scheduling.
5. Update `Handoffs/README.md` (this row: executed, with the final paths) and your board entry; commit and push only your files
   (docs and scripts, never media: the repo is public). The shared checkout has other sessions' uncommitted work: never `git stash -u`.

## Review status, 2026-09-30

Round 2 delivered for picks: 20 visual options, 40 RGB 1080x1920 platform files. Actual-render person-mask checks pass for all 40, minimum text clearance 49px. Instagram grid crops and phone-size layouts checked. Short 2 approved B is unchanged. No chosen finals, uploads or schedules yet.

## 4. Model and starter prompt
Codex (GPT-6 Astra), effort medium (image work per `model-routing-plan`; a known recipe with a style reference).

> Read `Handoffs/handoff-20260930-sl04-shorts-covers-codex.md` in full and do only what it asks: build five visual options each for SL-04 Arms & Shoulders shorts 1, 3, 4 and 5: one pool, two studio photos with Jelly Beans style backgrounds, one enhanced video screenshot and one designer choice, send me the review sheet and stop for my picks, then export the finals (Instagram and YouTube versions) and give me the paths. Do not upload or schedule anything.
