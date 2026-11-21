CONTENT | RO-01, "How To Keep Your Muscle While You Lose Fat" | LFC | Round 8

# H04 opener locked: first minute, then final film

Written 2026-10-05 after Dan reviewed the Round 7 motion in narration context. Recommended next task: **Claude Opus 5.5, high effort**, per the current model routing rule for routine RO long-form edits. Task name: **Keep Your Muscle LFC R8**. Use `.claude/skills/longform-edit/SKILL.md`; the existing Codex `$long-form-content-edit` recipe and Round 7 files are source records. Read `.claude/skills/_shared/VIDEO-RULES.md` in full before editing. The overnight dispatcher remains paused.

## Dan's decisions, now locked

Dan said: "Okay for the opening sequence let's go with H04. That looks good: this single guy doing curls and getting skinny B01 looks good."

- **H04 is the final opener.** Use the exact generated motion with the single man curling the dumbbell and becoming visibly thinner. Motion: `/Volumes/Extreme/_edit_work/ro01/revision7/motion/H04-kling25-a1.mp4`, SHA256 `d14edee82ec4045bae1638f7a9ce0d5f4e597e1f140a10c57c13f892ff895572`. Dan reviewed it with narration in `revision7/review/H04-context.mp4`, SHA256 `a8160d877a67dff46cf2080edd5ae9d06322fcd99a0a8250cd2c840102f76c91`.
- **B01 motion is approved.** Use `/Volumes/Extreme/_edit_work/ro01/revision7/motion/B01-kling25-a1.mp4`, SHA256 `e9e65e10ba47f175af6bec602a9507ed7b454d9bba039bf525ca3fe690611b93`. Its narration-context review is `revision7/review/B01-context.mp4`, SHA256 `cb36db5faea1754d3830ae6bb5124ed87912a0b77c29d829968217ee79e2eeb3`. The man takes one small bite, then winces and holds his stomach.
- H06 was an alternative, **not selected**. Do not put it in the film or ask Dan to choose the opener again.
- B02 remains removed. Fill its former R3 190.7897 to 198.4897 second slot with clean graded presenter footage and preserved R3 audio. Do not generate B02 or restore its graphic.

Machine-readable decision record: `/Volumes/Extreme/_edit_work/ro01/revision7/decisions-20261005.json`, SHA256 `13ccf461b29768d2f2be73055347dc13fb6d59adc2fe380da318f7b458a944f9`. Dan has approved H04 and B01 motion, **not** the finished first minute or full film.

## Preserve the earlier approvals

- R3 master: `/Volumes/Extreme/_edit_work/ro01/RO01_MASTER_R3.mp4`, SHA256 `17f666fc1a54f078768f6bef902ee22219f46b92681da627bbf0c68ab27a6f4f`. Preserve its approved camera color and audio. R4 source and recipe are under `revision4/`, including `recipe/`, `scene-jobs.json`, `grade.json` and `assets/source-grade.cube`. `PICTURE_CLEAN.mp4` contains baked older graphics, so rebuild affected sections from the raw source and approved treatment.
- Preserve the **23 exact approved R4 items** in `/Volumes/Extreme/_edit_work/ro01/revision5-plan/decisions.json`, SHA256 `8c34b785ab2ae40eb6c489aa0d7baa6548bb4c15ebdf994d495d0494d6ed4f15`: G01, S01, G03, J01, G04, G06, D01, G10, G11, G14, D02, G17, B03, G20, G22, B04, B05, G26, B06, S02, G36, G44 and B07. Round 7 verified 51 referenced asset hashes in `revision7/motion-QA.json`. Recheck exact files before assembly. Preserve approved copy, crops, look and timing except shifts required by J01.
- Apply J01's approved five-frame pause cut **once**, retaining the complete words "forever" and "Now". The reviewed cut removes approximately R3 57.671333 to 57.838167 seconds, shifting later content by 0.166833 seconds. Verify against the canonical recipe before final splice.
- The six approved R6 endpoint frames and their hashes remain in `revision6/frame-manifest.json`. No new motion generation is needed. Round 7's estimated provider submissions bring the known estimate to $1.732 for the video; actual provider and still-image charges are unavailable. Do not regenerate approved motion casually.

Prior handoff with exact approval history and build order: `Handoffs/handoff-20260929-ro01-r7-approved-frames-motion-to-final.md`. Round 7 work root: `/Volumes/Extreme/_edit_work/ro01/revision7/`. The review server at `http://127.0.0.1:8786/index.html` is only a reference for the already made decision.

## Next task, in order

1. Verify the locked hashes and source map. Inspect `revision7/recipe/build_first_minute.py` before running it; it is a prepared draft, not a proven final pipeline. Build the finished 16:9 first minute with **H04**, the approved R4 elements in that span, R3 color/audio, and the J01 cut. Check picture, speech, timing, hair clearance, joins and sound in the rendered minute.
2. Show that finished first minute to Dan in a working review page and stop for his verdict. Record any requested changes. Do not infer approval from his H04/B01 decision. If he approves the first minute, proceed to full assembly. If the round ends while awaiting his answer, write a short continuation handoff.
3. Build the complete 16:9 RO-01 candidate with H04, approved B01, all 23 locked R4 items and clean presenter footage in B02's old slot. Preserve the R3 color and sound. Keep the horizontal presenter picture static. Apply the approved J01 cut once. No full-length vertical, square or one-minute cut of this CONTENT video; Shorts are a separate later `/shorts` job.
4. Regenerate the SRT and chapters against the actual final timeline. Run exact-file video, audio and subtitle delivery gates, inspect every join and the complete candidate in chronological order with sound, then get one independent full-candidate review. Correct real failures and recheck affected gates. Deliver the full film, SRT, chapters, gate stamps, review evidence and provider cost record to Dan. The full film remains subject to his final review.

Do not repeat the old calibration, reopen approved H04/B01 or R4 decisions, make thumbnails, upload, publish, deploy the app or resume the overnight dispatcher in this edit task. The later setup task handles five thumbnail choices and distribution after Dan approves the film.

## Ready-to-paste starter prompt

Name this task **Keep Your Muscle LFC R8**. Execute `Handoffs/handoff-20261005-ro01-r8-h04-first-minute-and-final-film.md` with `/longform-edit`. This is CONTENT, RO-01 LFC. Dan chose and approved H04, the single man curling and getting skinny, as the opener, and approved B01 in narration context. Keep H06 out and B02 removed. Preserve R3 color/audio and all 23 exact approved R4 items. Build and show me the finished first minute with H04, then, after I approve it, assemble, check and deliver the full 16:9 film with SRT and chapters. Do not repeat calibration, make ad-format derivatives, publish, upload, deploy or resume the dispatcher.
