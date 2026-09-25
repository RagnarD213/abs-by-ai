# DS-18 handoff: remove the upper-right kettlebell title

Prepared September 25, 2026. This is a brief for the next editing task. Do not edit, render, upload, publish or schedule DS-18 while preparing this handoff.

Recommended model: GPT-6 Astra, high effort.

## Dan's final revision request

Remove the black `KETTLEBELL DEADLIFT` graphic from the upper-right corner everywhere it appears. Dan says it adds no value. He likes the R7 B-roll and its synchronization with his narration. Keep the rest of R7 the same, including the exercise clips, labels, green and red arrows, picture cuts, audio, captions, opening, deleted Start Today section, comment CTA, color, runtime, frame size and approved cover. This request does not authorize an upload or publication.

Dan's screenshot shows the title at about 8 seconds on the presenter shot. It is an example of the unwanted graphic, not a request to change the presenter shot or captions.

## Exact starting point

- Delivered R7 master: `/Users/danielrose/Documents/Claude/Projects/Abs By AI/Short-form video content/ds-18_how-to-kettlebell-deadlift.mp4`, SHA256 `06bb4578ce05eff9ec39301f4f2821208433f8fcb2bb5ebb839b78c0470344c7`.
- R7 review copy: `/Volumes/Extreme/_edit_work/ds18-kettlebell-deadlift/review/DS-18-R7-full-video-review.mp4`, SHA256 `5c65d0e26572812928b635135d3b3ab279a13e5ab80eb4194e93c55ca547264b`.
- Work directory: `/Volumes/Extreme/_edit_work/ds18-kettlebell-deadlift/`. The deterministic R7 recipe is `recipe/final_r7_picture_sync.py`; picture map and hashes are in `final-r7-manifest.json`; the approved R6 caption timing is `captions-final-r6.ass`.
- Approved cover: `covers/instagram/ds-18_how-to-kettlebell-deadlift_cover-C-video-frame-r5.png`, SHA256 `6021589257e4be64fa3131313c6ed56048847408fdbb8b74f782dc475c660706`.
- R7 has 1,257 frames at 30000/1001 fps, 1080x1920, 41.9419 seconds. Its four demonstration pairs and final return to green `SQUEEZE GLUTES` are locked.

## Graphic source and affected picture

`assets/title-fullscreen.png` is a transparent 1080x1920 overlay. The unwanted corner title occupies approximately x=730-1053, y=42-191. The same PNG also contains an approved small `AbsByAI.com` mark near the bottom at approximately x=784-975, y=1823-1843. **Remove only the corner title. Keep the lower site mark at the same position and appearance.** Make a revision-specific title-free copy of the overlay; do not overwrite the R7 asset.

The title is visible on all five R7 presenter spans. Bounds below are output frames with the end excluded:

| Frames | Output time | Picture |
| --- | --- | --- |
| 151-280 | 5.038-9.376 s | Presenter, includes Dan's screenshot moment |
| 388-459 | 12.946-15.349 s | Presenter |
| 596-612 | 19.887-20.454 s | Presenter |
| 788-825 | 26.293-27.561 s | Presenter |
| 1052-1256 | 35.102-41.942 s | Presenter and final CTA |

The original R5 renderer `recipe/final_r5.py` overlays this PNG on presenter footage. R7 reuses baked R6 picture before frame 257 and after frame 1051, while its middle block recreates presenter picture with the same PNG. Thus merely changing the PNG in the R7 recipe would leave the corner title visible in the opening presenter span and the final CTA. Rebuild or replace all five presenter spans from clean `picture.mp4`, with the title-free overlay and the unchanged captions, then retain the R7 B-roll spans exactly. `picture.mp4` has 1,358 frames because it predates the R6 removal of frames 1168-1268. For R7 output frames 1168-1256, source picture frames are output frame plus 101. Keep the ripple cut so `START TODAY` does not return.

## Build and verification

1. Read `AGENTS.md`, `.claude/skills/_shared/VIDEO-RULES.md`, `Handoffs/video-editing/00-RULES.md`, `$abs-edit-organic` and `.claude/skills/shorts/SKILL.md`. Check the two-build cap. Claim DS-18 in the edit queue and coordination board before rendering.
2. Copy the R7 recipe into a revision-specific R8 recipe. Use the R7 master and approved clip hashes as locked references. Remove only the upper-right title from each presenter span. Preserve the lower site mark, final caption pixels and all exercise overlays. No new B-roll, music, graphics or cover work.
3. Make consecutive-frame proofs at each entrance and exit of a changed presenter span, plus a moving proof of the screenshot moment and the final CTA. Check the full picture for any remaining `KETTLEBELL DEADLIFT` corner title, missing `AbsByAI.com` mark, caption overlap, black frames, frozen picture or new jump. Compare unchanged B-roll frames and spoken cue matches against R7. Keep the AAC stream byte-identical if the picture-only assembly permits it.
4. Render a full 1080x1920 master and lightweight private review copy. Run exact-file hash and media checks, finished-file speech/caption checks, audio checks, the shared delivery gate, every-frame watch pass and one independent complete-candidate review. Report all gate failures honestly; R7 passed 33 rows and failed six existing audio, framing, caption and placeholder-record rows. Do not change thresholds to force a PASS. A literal headphone listen was unavailable in the R7 task, so arrange one if available in the next task or state that limitation plainly.
5. Deliver the new review copy to Dan. **Do not upload, publish or schedule.** Update `WORK_PACKET.json`, the DS-18 queue, `Handoffs/video-editing/00-MASTER.md` and the DS-18 coordination entry. Set `finalized` only after Dan approves R8. Commit and push only DS-18 tracking changes, then verify the Railway result and `https://absbyai.com`.

## Exact next action

Open R7 and `assets/title-fullscreen.png`. Confirm the title on the five presenter spans, then build a title-free overlay that retains the lower site mark. Make a moving proof of the first presenter span and the final CTA before rendering the full R8 master.

## Ready-to-paste starter prompt

> Read `Handoffs/handoff-20260925-ds18-remove-corner-title.md` and execute it exactly. Remove the upper-right `KETTLEBELL DEADLIFT` graphic from every DS-18 R7 presenter span, while preserving the lower AbsByAI.com mark and everything else Dan approved, especially the synchronized B-roll, arrows, audio, captions, opening, Start Today deletion, CTA and cover. Verify every affected join and the whole finished file, get an independent review, deliver a new private review copy, update tracking, and do not upload or publish. Use GPT-6 Astra at high effort.
