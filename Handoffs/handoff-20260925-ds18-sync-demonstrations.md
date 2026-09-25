# DS-18 handoff: match every demonstration to the spoken instruction

Prepared September 25, 2026. Dan requested this handoff so a new task can make the revision. **Do not edit, render, upload, publish or schedule DS-18 in the handoff task.** This document is the complete brief for the next editing task.

Recommended model: **GPT-6 Astra, high effort.**

## Dan's request

Reverse the four pairs of demonstrations so the correct form appears when Dan describes it, and the mistake appears when Dan warns against it. The pairs are weight placement, toe direction, back position, and glute squeeze versus hip thrust. The screenshot Dan supplied shows `WEIGHT IN FRONT` on screen at 9 seconds while he is introducing the correct weight position. Preserve every other approved choice.

Dan's ordering rule is authoritative: **show the correct form on the correct instruction and the mistake on the warning, throughout the video.** A simple pairwise swap at each existing cut is insufficient if the new boundary still contradicts the speech. Set the picture boundaries from the heard words and inspect the moving demonstrations. Keep the spoken edit, audio treatment, burned caption wording/timing, overall runtime, opening, final `home` to `Leave me a comment` join, and approved cover unchanged unless a specific picture adjustment requires otherwise.

## Current R6 starting point

- Delivered master: `/Users/danielrose/Documents/Claude/Projects/Abs By AI/Short-form video content/ds-18_how-to-kettlebell-deadlift.mp4`
- Master SHA256: `973290bbf870db86e23d01a21c0717458a858e13413cd57a16d4d549cc6de2b5`
- Review copy: `/Volumes/Extreme/_edit_work/ds18-kettlebell-deadlift/review/DS-18-R6-full-video-review.mp4`, SHA256 `1fcb07d824ab1ca55a21b24d2a9d19b045af4ebb6f758ea4481f29ab9787a7eb`
- Format: 1080x1920, 30000/1001 fps, 1257 frames, 41.9419 seconds, H.264/AAC.
- Work directory: `/Volumes/Extreme/_edit_work/ds18-kettlebell-deadlift/`
- Current picture/caption map: `final-r6-manifest.json`, `captions-final-r6.ass`, `finished-asr-r6.json` in that work directory.
- Cached approved labelled and graded clips: `build/final-r5/broll-00.mp4` through `broll-08.mp4`. The renderer `/recipe/final_r5.py` shows how they were assembled; `/recipe/final_r6_cut.py` removed Start Today. Do not run either unchanged over the delivered file.
- Approved cover: `/Volumes/Extreme/_edit_work/ds18-kettlebell-deadlift/covers/instagram/ds-18_how-to-kettlebell-deadlift_cover-C-video-frame-r5.png`, SHA256 `6021589257e4be64fa3131313c6ed56048847408fdbb8b74f782dc475c660706`.

The R6 independent picture review passed all 1257 frames, 24 review images and 11 boundaries. Its findings are `/Volumes/Extreme/_edit_work/ds18-kettlebell-deadlift/review/independent-r6/findings.json`. The exact-file delivery gate is not a PASS: 32 rows passed and 7 failed, including the approved sound/framing/caption treatment, the old placeholder record, and lower B-roll coverage after removing Start Today. Do not change thresholds or claim these failures disappeared without remeasurement.

## Four picture corrections

Times below come from fresh ASR on the delivered R6 master. Confirm by listening and inspecting frames before placing cuts. Preserve the approved clip identity, crop, grade, label, arrow style and full portrait occupancy. The word-aligned cut points are targets, not permission to clip a word or break a teaching repetition.

| Spoken instruction | Current picture | Required picture |
|---|---|---|
| `First, put the weight between your legs` begins about **9.40s**; `not in front of you` begins about **11.56s** | `02-weight-front` at 8.575-10.777, then `03-weight-between` at 10.777-12.779 | Show approved green `WEIGHT BETWEEN LEGS` correction first, including the 9-second moment in Dan's screenshot. Switch to approved red `WEIGHT IN FRONT` mistake on `not in front of you`, close to 11.56s. |
| `your toes facing forward` begins about **17.06s**; `not outward` begins about **18.56s** | `04-toes-out` at 12.779-15.782, then `05-toes-forward` at 15.782-18.986 | Show approved green `TOES FACING FORWARD` during the positive stance instruction, especially 17.06-18.18s. Show approved red `TOES POINTED OUT` on `not outward` around 18.56-19.16s. |
| `look at the ceiling or the sky as you deadlift` runs about **20.46-22.66s**; `your back doesn't get rounded out` about **23.64-25.02s** | `06-rounded-back` at 18.986-22.189, then `07-back-flat` at 22.189-25.692 | Show approved green `BACK FLAT` while Dan gives the correct look-up cue. Show approved red `ROUNDED BACK` when he warns about rounding. Keep the clean complete rounded-back movement without standing junk footage. |
| `squeeze your glutes at the top of the rep` runs about **27.56-29.52s**; `You don't need to thrust your hips out` about **30.08-31.44s**; `Squeeze at the top for extra power` about **31.98-34.96s** | `08-hip-thrust` at 25.692-29.997, then `09-squeeze-glutes` at 29.997-35.102 | Show approved green `SQUEEZE GLUTES` on the first positive instruction. Show approved red `HIP THRUST` on the warning. The narration then returns to correct form: use a suitable later portion of the approved green demonstration again, or the presenter if that better preserves the visible action, while the final positive line plays. Never leave the mistake on screen under that line. |

These four blocks contain the same nine previously approved source clips. Reordering alone can put a correction under a warning, because the clips have different lengths and the speech does not start at the old picture boundaries. Adjust picture in and out points within the existing blocks as needed. Keep each exercise action readable and avoid freezing a frame, unnatural slow motion, chopped repetitions, caption overlap or labels that describe the wrong action. Do not add new B-roll. The exception allowing repeated exercise action inside a teaching demonstration may apply to the final return to `SQUEEZE GLUTES`; use only the existing approved source.

## Preserve and build

1. Read `AGENTS.md`, `.claude/skills/_shared/VIDEO-RULES.md`, `Handoffs/video-editing/00-RULES.md`, `$abs-edit-organic`, and `.claude/skills/shorts/SKILL.md`. Check the machine's two-build cap and claim DS-18 in the queue and coordination board before editing.
2. Start from the R6 timing and accepted picture assets. Make a revision-specific copy of the deterministic assembly recipe. Reorder and retime the four demonstration blocks only. The opening `01-correct-form`, all talking-head sections, narration, audio, captions, colour, and final CTA remain as approved. Never restore the deleted `START TODAY` scene.
3. Inspect moving proof around every spoken phrase and every changed join, with consecutive frames at the joins. In a source clip, `green` must indicate the correct action and `red` the mistake. Verify the captions stay in the low clear band, away from the kettlebell, shoes, face and teaching arrows.
4. Render a full 1080x1920 master and lightweight review copy. Verify the exact delivered hash with finished-file ASR, audio checks, shared delivery gate, every-frame watch pass, and a fresh independent complete-candidate review. Listen to all four blocks and the unchanged final CTA. Report inherited gate failures honestly and do not change thresholds to force a PASS.
5. Deliver the new review copy to Dan. **Do not upload, publish or schedule.** Update `WORK_PACKET.json`, DS-18 queue status, `Handoffs/video-editing/00-MASTER.md` and its entry in `AI_COORDINATION.md`. Mark `finalized` only after Dan approves the new cut. Commit and push only DS-18 tracking changes, then verify the Railway result and `https://absbyai.com`.

## Exact next action

Open R6 and the cached approved clips. Build a word-by-word picture map for the four blocks, then make a short moving proof of each corrected block before the full render. Use the speech onsets above to choose the actual cut frames.

## Ready-to-paste starter prompt

> Read `Handoffs/handoff-20260925-ds18-sync-demonstrations.md` and execute it exactly. Revise only DS-18's four demonstration pairs so the correct form appears on Dan's positive instructions and each mistake appears on its spoken warning. Use the existing approved clips, labels and arrow styles; keep the R6 voice, captions, opening, Start Today deletion, CTA and cover. Verify every changed join and spoken match, rerun all exact-file checks and independent review, deliver a new private review copy, update tracking, and do not upload or publish.
