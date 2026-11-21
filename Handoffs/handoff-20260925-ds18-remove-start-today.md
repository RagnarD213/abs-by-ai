# Handoff: DS-18 final cut, remove Start Today clip

Prepared September 25, 2026. This handoff is for one final edit in a new task. The current video is approved overall. Do not redesign or reopen any other edit decision.

Recommended model: **GPT-6 Astra, high effort.**

## Goal

Remove the silent kettlebell demonstration labelled `START TODAY` at about 39 seconds. Ripple-close that interval so the final spoken comment CTA follows naturally. Preserve every other approved picture, caption, arrow, crop, label, audio treatment, colour decision and cover exactly.

Dan's final revision request:

> Okay this is looking great overall. Just one revision at 39 seconds: I want you to eliminate that silent clip of me deadlifting where it says "Start Today." I feel like that looks a little awkward and doesn't add to the video. Just make that final cut: cut that clip of me silently deadlifting. "Start Today" is at 39 seconds and the video is set.

## Current approved candidate

- Full master: `/Users/danielrose/Documents/Claude/Projects/Abs By AI/Short-form video content/ds-18_how-to-kettlebell-deadlift.mp4`
- Master SHA256: `da08a6d50d42fc2ae5c8615fabdd9ef6fff082a91a645b5d7de8d0b9612c7444`
- Review copy: `/Volumes/Extreme/_edit_work/ds18-kettlebell-deadlift/review/DS-18-R5-full-video-review.mp4`
- Review SHA256: `9fc751c2d14850c525203d97880b78ce2df10ab9fc7bbe9a213f073b0ccaca45`
- Current format: 1080x1920, H.264, 30000/1001 fps, AAC 48 kHz stereo, 1358 frames, 45.311933 seconds.
- Work directory: `/Volumes/Extreme/_edit_work/ds18-kettlebell-deadlift/`
- Reproducible renderer: `/Volumes/Extreme/_edit_work/ds18-kettlebell-deadlift/recipe/final_r5.py`
- Current manifest: `/Volumes/Extreme/_edit_work/ds18-kettlebell-deadlift/final-r5-manifest.json`
- Approved cover, unchanged: `/Volumes/Extreme/_edit_work/ds18-kettlebell-deadlift/covers/instagram/ds-18_how-to-kettlebell-deadlift_cover-C-video-frame-r5.png`

The independent visual audit passed all 30 required images and all 14 boundaries before this final revision. Its findings are at `/Volumes/Extreme/_edit_work/ds18-kettlebell-deadlift/review/watch-r8/findings.json`.

## Exact edit

The unwanted scene is manifest item `10-start-today`:

- Picture starts at `38.972267` seconds, frame 1168.
- The labelled B-roll itself is 97 frames and ends at about `42.208833` seconds.
- The next spoken word, `Leave`, begins at about `42.36` seconds.
- A clean frame-aligned ripple-delete candidate is `[38.972267, 42.342300)`, frames 1168 through 1268. This removes 101 frames and should produce about 1257 frames or 41.9419 seconds.

Confirm the join by listening and inspecting consecutive frames before locking it. Do not cut the preceding word `home` or the following word `Leave`. The target is a natural pause between those two lines, with no silent deadlift scene and no audio click. If the exact best boundary differs by a frame or two, use the cleanest word-safe and click-free boundary and record it.

The safest method is to modify the existing deterministic recipe and ripple-delete the same interval from picture, audio and caption timing. If cutting the current approved master is materially safer, use one high-quality encode and prove there is no visible quality loss. Do not rebuild or retime unrelated scenes.

## Preserve exactly

- All nine earlier approved B-roll clips, their full vertical framing, trims and labels.
- Correct Form has no arrows.
- The approved red and green arrow treatments on the mistake and correction demonstrations.
- The clean rounded-back repetition with no standing junk footage.
- Demonstration captions in the low clear band, away from the kettlebell and shoes.
- The approved talking-head framing, colour, audio treatment and comment CTA.
- The approved cover image.
- No black bars, no placeholders, no new graphics and no replacement B-roll.

Do not upload, publish or schedule the video.

## Verification and delivery

1. Read `AGENTS.md`, `.claude/skills/_shared/VIDEO-RULES.md`, `Handoffs/video-editing/00-RULES.md`, `$abs-edit-organic`, and `.claude/skills/shorts/SKILL.md` before editing.
2. Check the machine build count before rendering. Never start a third concurrent video process.
3. Render the revised full master and a lightweight review copy.
4. Confirm the Start Today clip and label are completely absent.
5. Inspect the new join as consecutive frames and listen through it with headphones. Confirm `home` flows naturally into `Leave me a comment` with no long silence, clipped word or click.
6. Rerun audio checks, finished-file ASR, the shared delivery gate, the every-frame watch pass and a fresh independent complete-candidate review on the exact delivered hash. Do not change thresholds to force a pass.
7. Deliver the review copy to Dan. Do not upload or publish.
8. Update `WORK_PACKET.json`, the DS-18 queue row, `Handoffs/video-editing/00-MASTER.md` and the DS-18 entry in `AI_COORDINATION.md`. Once Dan approves this final cut, mark DS-18 finalized and remove its active board entry.
9. Commit only DS-18 tracking changes, push `main`, confirm deployment and verify `https://absbyai.com` responds normally.

## Exact next action

Open the existing DS-18 recipe and master, remove only the frame-aligned Start Today interval, render the shortened file, then inspect and listen to the new `home` to `Leave me a comment` join before running the complete final checks.

## Ready-to-paste starter prompt

> Read `Handoffs/handoff-20260925-ds18-remove-start-today.md` and execute it exactly. This is the final DS-18 revision. Remove only the silent `START TODAY` kettlebell clip around 39 seconds, ripple-close the same interval in picture, audio and captions, and preserve every other approved choice. Verify that `home` flows naturally into `Leave me a comment` with no silence, clipped word or click. Rerun all exact-file checks and a fresh independent review, deliver the new review copy, update DS-18 tracking, and do not upload or publish.
