# CONTENT (LFC): Arms & Shoulders Workout Only, Round 3

Start now in **Arms Shoulders Workout LFC R3**. Recommended model: **GPT-6 Sol, high effort**, the existing organic editing executor. All creative choices needed for this workout are settled; the work is full assembly and careful verification.

## Dan's authorization, October 20, 2026

> Let's go with color B. Finish the full video.

Use **Round 2 B, Warm Rich Vivid**, not Round 1's rejected warm B. This explicitly authorizes the full film. Preserve the reviewed Round 2 fixed crop and all inherited approved timing, graphics and original audio. No more color options or repeated approval questions. The complete export still needs Dan's final review after it has been built and checked.

Decision record and current verified SHA256s: `Handoffs/video-editing/ro04-round3-plan/decisions.json`. All eight inherited graphics/audio assets were rehashed and match their recorded locks. The new B stills, B moving sample, first minute, overhead sample and reproduction inputs are hashed there. Rehash before reuse. Approval corpus additions are copied beside the decisions and added to the shared corpus.

## Read only what is needed

1. Current `.claude/skills/_shared/VIDEO-RULES.md`, `Handoffs/video-editing/00-RULES.md`, and the installed `$long-form-content-edit` skill.
2. This handoff and the Round 3 decisions above. They supersede older color-pending and no-full-film statements.
3. `Handoffs/handoff-20261015-ro04-round1-review.md` for source/music/timing; `Handoffs/video-editing/ro04-round2-plan/notes-round2.md`, `review-receipt.json` and `panel-repair-20261019.json` for the preview checks and player repair.
4. `Media/video-edits/RO-04/round2/recipe/build.py`, `qa/calibration.json`, `qa/plan.json`, `edit-sheet.json`, `WORK_PACKET.json` and `qa/music-fit.json` if present; the authoritative music-fit evidence also exists in round1/qa.

Claim only this job after checking `AI_COORDINATION.md`, the RO-04 row in `00-MASTER.md` and the edit queue. Preserve other sessions' work and keep the shared two-build cap. Raw rolls stay read-only.

## Exact build

Build in a new `Media/video-edits/RO-04/round3/`; preserve Round 1 and Round 2 media. Copy/adapt the R2 recipe so every output and evidence path points to round3. Do not execute the R2 recipe with old output paths.

- Source: `/Volumes/Extreme/abs by ai 8:3 jeff chagrin shoot/main camera/C1586.MP4`, 1920x1080, 30000/1001 fps, BT.709. Source start **66.6003**. Nine opening frames were ALREADY trimmed. Never trim them again.
- Full camera action ends at output **95.8497**. Ready ends 5.8497; curls end 35.8497; laterals end 65.8497; triceps end 95.8497; rest ends **125.8497**. Keep actual-time equipment changes, complete movement and set durations. Do not accelerate or repeat sets.
- Color B: existing fitted RGB polynomial from R2 calibration, RGB multipliers 1.012, 1.0, 0.99; then saturation **1.48**, contrast **1.075**, brightness `(1-contrast)*0.04`, as implemented by R2 `vf()`. Grade camera before graphics. Never grade approved graphics with the camera.
- Fixed crop **x100,y18,w1776,h1000**, scaled to1920x1080. Same size as the preview, about20.68% less typical standing headroom. No animated camera movement. Protect hair, hands, raised dumbbell and teaching action across all95.85seconds.
- Original stereo audio reference: `Zeeshan Content Videos/arms and shoulders home workout - video 2/arms and shoulders home workout | zeeshan | 16x9 | video 2.mp4`,858396944bytes, MD5 `49c7dfb3d189043dbb2bc4b326e8fd81`. Decode untagged picture as BT.709 if used for comparison. Audio offset431.36425, cut starts497.96455. Copy its AAC unchanged for camera action; no EQ, bass lift, new limiter or mono conversion. Dan has approved this editor mix.
- Use R2 `state()` / `paint()` for the already approved five timer/rest graphics. Preserve copy, layout, timing and motion. The newer HyperFrames rule expressly preserves already approved graphics; do not redesign this job during final assembly.
- Render camera action **0 to95.8497**, then the full rest **95.8497 to125.8497** separately. The source-picture renderer must not run across the rest boundary. It would read past available camera footage. Respect frame-grid rounding and prove the resulting actual timeline.
- Rest music: `/Volumes/Extreme/_edit_work/music-check-20260922/knox-gym-energy-gym-thunder-538872.mp3`. Reference time510 matches music8.7325, gain0.07449345290660858. Preserve music phase through the camera/rest seam and check it in listening context. The earlier isolated rest preview did not prove the final30-second seam.
- Preserve the actual short spoken start phrase and initial countdown in an SRT sidecar. No burned running captions, invented dialogue or song lyrics in subtitles.

## Verification and delivery

The R2 first minute SHA256 is `3c905347a0b51e3468dc78b19f9fd2dde058026d1c71fe4fdc3e985971c29a8f`. It passed audio gate2.0.0 and delivery gate2.6.1 (39passed,0failed,0unmeasured,15declared N/A) at delivery. Those are PREVIEW checks, not full-film stamps. The R2 independent review cleared inspected stills/strips/samples, not continuous full-film playback or new native audio listening.

For the actual new full export: run the shared audio selftest, verbatim audio gate with exact source-mix/timing proof, current consolidated delivery gate, edit-sheet validation, dense hair/action crop checks, native freeze/black/continuity checks and a complete picture/audio review. Use one fresh independent reviewer after editor QA; repair real defects before Dan sees it. Inspect graphics across every set boundary and the final rest. Reuse only exact audio evidence whose hashes/timing prove applicability. The preview gate originally mistook functional timer text for subtitles and original song lyrics for extra speech. Preserve honest evidence of those specific detector limits; do not copy the entire old PASS or blindly waive new full-film findings. No gate thresholds change to fit this export.

Name the native output `Arms Shoulders Workout LFC R3 - full workout.mp4`, and the phone copy with ` - REVIEW 540p.mp4`. Include SRT, audio A/B, exact-file stamps, notes and reproducible recipe. Copy the native full workout to `Videos to Review/` and reveal that folder. Keep old review files until the full film is finalized.

Keep the R2 panel and player repair functional on8974 until the R3 review is ready. Use the maintained managed review server for R3; identify this job's old service before switching its root, never replace another job's port. Preserve the October19 custom seek/play/restart controls in `round2/recipe/page.py`. Re-test all links, HTTP200 and video206 ranges, actual browser playback, seeking and speed silently; leave paused/muted. Do not use a plain HTTP server.

Back up the delivery to a public Round3 sibling folder under `gdrive:Codex Content Videos/Arms Shoulders Workout Only - RO-04/`, parent project Drive folder `1KlxWLcUFccU_bPZA3KyC9TWyfzwAKOoe`. Set anyone-with-link viewer and verify saved files. R2 public backup: https://drive.google.com/drive/folders/1TZp50kIXBGsGNts7FJ_W6SeJ3Ma3Q5Go . rclone single transfer with32M chunks worked. Check free space before the build; Extreme was full in earlier rounds, local ignored Media storage was used.

Deliver the full-film review link first, then exact watch ranges from the new timeline around the opening, 0:35.85/1:05.85 exercise changes, 1:10 -1:26 overhead action,1:35.85 rest seam and final rest. Confirm actual rounded times before reporting them. Mark the queue delivered only after complete review delivery, finalized only after Dan approves the complete film. This edit includes no thumbnails, upload/setup, scheduling or ad-format adaptations. Later content Shorts are a separate job.

## State and costs

This handoff turn recorded B approval and render authorization; it did not render the full film. R1/R2 previews and repaired page remain. R1 provider review estimate under$1, actual billed dollars unavailable; R2 and panel repair paid generation/review-provider spend$0. This handoff spend$0. No AI generation is needed. State an estimate before any paid quality-review batch, obey the existing$5 review limit, and record actual usage when exposed. Exact task-model token totals/context percentage are unavailable in this runtime.

First action: verify locks and source availability, check build capacity/storage, then adapt R2 into the new round3 directory and render the complete workout plus rest. No new creative approval is needed before that render.

## Starter prompt

CONTENT (LFC). Name this chat Arms Shoulders Workout LFC R3. Execute Handoffs/handoff-20261020-ro04-round3-color-b-full-film.md. Dan said: "Let's go with color B. Finish the full video." Use Round2 Warm Rich Vivid B and the reviewed crop. Preserve the approved opening, original stereo audio, real-time sets, timers and rest design. Build the complete workout and30-second rest in a new round3 folder, check the audio seam, run exact-file gates and one independent full-film review, then deliver the full video on the repaired review panel and in Videos to Review. Do not ask for color approval again. No thumbnails, publishing or ad-format versions. Recommended model: GPT-6 Sol, high effort.
