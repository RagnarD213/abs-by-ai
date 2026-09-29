# WV-01 final A: create a 1.2x speed variation

Created 2026-09-29. Recommended model: **GPT-6 Sol, Medium effort**.

## Goal and authorization

Dan approved the exact WV-01 version A website video as final, then asked for a handoff to make a 1.2x speed variation in a new task. Make a separate reviewable variant from the finalized master. Do not revise or replace the approved original. This handoff authorizes the speed variation render, not an upload or website installation.

## Locked source and current state

- Final 1080p source: `/Volumes/Extreme/_edit_work/wv01-edit/round17/final/WV-01 FINAL Website VSL A 1080p.mp4`
- Source SHA-256: `acddfb5b3bad7bb6d85f937b74054fafb4be33505f49ae91cd765a8ecac88836`
- Source duration: 753.086 seconds, about 12:33, at 1920x1080 and 30000/1001 fps. The requested uniform 1.2x version should run about 627.57 seconds, or 10:28, subject to frame and audio packet rounding.
- Subtitles: `/Volumes/Extreme/_edit_work/wv01-edit/round17/final/WV-01 FINAL Website VSL A.srt` and matching `.vtt`.
- Finalization record: `/Volumes/Extreme/_edit_work/wv01-edit/round17/final/FINALIZATION.json`. Full prior QA: `/Volumes/Extreme/_edit_work/wv01-edit/round17/review/QA.md`.
- The exact original was approved by Dan on 2026-09-29 and WV-01 is `finalized` in the editing queue. Complete B is deferred. The dispatcher stays paused. Nothing has been uploaded or installed on the site.
- The original website delivery gate reported FAIL. Its recorded findings include C01 garbled AI screen text around 1:47 to 1:53, the accepted R12-B sleeve continuity issue around 12:11 to 12:19, a quiet ending tail and other strict measurements. Dan approved the exact original with these findings disclosed. Preserve this history and do not call the original or new variant a technical gate PASS without a fresh passing result.

## Exact new task

1. Read `.claude/skills/_shared/VIDEO-RULES.md` in full, the current video skill's adaptation boundary, this handoff, and the finalization and QA records. Verify the source hash before work. Check the two-build machine cap.
2. Work in a new isolated directory such as `/Volumes/Extreme/_edit_work/wv01-edit/speed-1p2/`. Apply a **uniform 1.2x** tempo to the full picture and soundtrack. Preserve the voice pitch. Keep the same story, shot order, graphics, labels, grade, framing and closing words. Make no content cuts, new AI assets or new creative choices. Keep the original files unchanged.
3. Render a separate 1080p MP4 at the source frame size and frame rate. Retiming all subtitle cue starts and ends by the same factor, produce SRT and VTT sidecars. Make a 540p phone review copy from the exact new timeline. Use a clear name such as `WV-01 Website VSL A 1.2x 1080p.mp4`.
4. Verify the full file decodes, speed and duration are correct, speech retains its pitch, words remain intelligible, and sound stays synchronized with picture from start through the final CTA. Check the opening, phone demonstration, fast graphic builds, family shot and CTA in moving context, then review the whole video and audio chronologically. Check subtitle timing and the last words. Speed may make some graphics too brief to read; report a confirmed problem rather than silently changing the locked design.
5. Run fresh exact-file audio and website delivery gates and the native watch pass on the variant. Retiming the gate plan's timed joins, graphics, captions and speech references to the new timeline so old timestamps do not produce false findings. Record every inherited finding separately from any speed-induced defect. Use one independent complete-candidate review. Do not relax thresholds or claim a PASS from Dan's approval of the original.
6. Deliver the 1.2x master, review copy, SRT/VTT, hash, new gate results and a short comparison with the original for Dan's review. Keep WV-01's finalized original and queue state intact. Do not upload, publish, replace a website video, render complete B or start the dispatcher.

## Ready-to-paste starter prompt

Create a separate uniform 1.2x speed variation of the finalized WV-01 version A using `Handoffs/handoff-20260929-wv01-final-a-1p2x-speed-variation.md`. Use the exact final 1080p master and verify its SHA-256 first. Preserve pitch, complete narration, graphics, shot order and closing CTA; retime the SRT and VTT. Render a new 1080p master and 540p review copy, run fresh exact-file picture, sound, subtitle and website gates, inspect the whole video and obtain one independent complete-candidate review. Show me the variant for review. Keep the approved original and editing queue status unchanged, complete B deferred, the dispatcher paused, and uploads and website publishing off.
