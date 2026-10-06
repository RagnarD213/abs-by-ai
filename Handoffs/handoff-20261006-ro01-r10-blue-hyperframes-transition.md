CONTENT | RO-01, "How To Keep Your Muscle While You Lose Fat" | LFC | Round 10

# Remove the old opening graphic, update every graphic, and restore the missing tip introduction

Written 2026-10-06 from Dan's review of the R9 full film. Name the next task **Keep Your Muscle LFC R10**. Recommended model: **GPT-6.1 Sol, high effort**. Use the `long-form-content-edit` skill and the project's `/longform-edit` workflow. Read `.claude/skills/_shared/VIDEO-RULES.md`, `.claude/skills/_shared/GRAPHICS-STANDARDS.md`, and `.claude/skills/_shared/hyperframes/README.md` before editing. The overnight dispatcher remains paused.

## Current film and decisions

- Review master: `/Volumes/Extreme/_edit_work/ro01/revision9/full/RO01_MASTER_R9_FINAL_REVIEW_1080p.mp4`, SHA256 `16da7e740f520d06440ff8cee6c4e8eb6eca66c9fadf1f54ffe9c4ce9395f6cb`. It is 1920x1080, 30000/1001 fps, 21,247 frames, 11:48.94.
- Current subtitles, chapters, and QA: `/Volumes/Extreme/_edit_work/ro01/revision9/full/RO01_R9_FINAL.srt`, `RO01_R9_CHAPTERS.txt`, and `RO01_R9_QA_REPORT.md`.
- R9 assembly and timeline: `/Volumes/Extreme/_edit_work/ro01/revision9/recipe/build_full.py` and `/Volumes/Extreme/_edit_work/ro01/revision9/full/piece-plan.json`. Original camera edit map: `/Volumes/Extreme/_edit_work/ro01/scene-jobs.json`. R4 graphic source map: `/Volumes/Extreme/_edit_work/ro01/revision4/asset-graphic-manifest.json`.
- Keep the approved H04 opening motion from 0:00 to 0:05, B01 motion, R3 presenter color and voice, the selected `Werq` instrumental and its approved first-minute balance, the J01 five-frame cut, and the existing editorial decisions except where Dan's new requests require changes. H06 and B02 stay out.
- Dan wants a complete R10 review film with corrected subtitles and chapters. Do not upload, publish, deploy, make thumbnails, make a full vertical or square version, make a one-minute ad cut, or resume the dispatcher. Organic Shorts are a separate later job.

## Revision 1: 0:07 old green graphic

Dan identified the small old-style **"Keep your muscle"** graphic over his chest at 0:07. **Remove it entirely. Show only the camera shot in that portion.** Do not replace it with a new lower third. The chip is old `g00`, visible after H04 ends at about 0:05 until about 0:09.41. It is baked into the R3 picture that R7 used for the H04 context, so removing an overlay from the R9 assembly cannot remove it.

Source trace: `/Volumes/Extreme/_edit_work/ro01/revision7/recipe/build_context.py` takes the H04 motion for 0:00 to 0:05 and then copies the R3 master picture to 0:12.3. In `/Volumes/Extreme/_edit_work/ro01/scene-jobs.json`, `scene-001` is original `C1606.MP4` at source 4.5018 seconds, output frames 54 to 282, with the old `g00` attached. `scene-002` starts at output frame 282 with clean camera. Rebuild the 0:05 to 0:09.41 picture from the original C1606 camera, matching the existing grade, crop, shot timing and continuous motion. The clean scene method is in R9 `build_full.py`, `render_scene()`. Keep the approved H04 frames and narration untouched. Check the joins at 0:05 and 0:09.41 frame by frame and listen across both.

## Revision 2: full-film Soft Blue Light and HyperFrames audit

The R9 film contains **17 graphic segments** inherited from R4. Their sampled frames are in `/Volumes/Extreme/_edit_work/ro01/revision10_review/graphics_all_1.jpg`, `graphics_all_2.jpg`, and `graphics_all_3.jpg`. They look broadly blue, but their source recipe uses the earlier `softblue.py` renderer rather than the current shared HyperFrames templates. Rebuild and visually check **every graphic** to the current Soft Blue Light standard. Preserve the approved information, the spoken-phrase relationships and sensible on-screen durations. Do not leave any old green chip or mixed graphic treatment in the final film.

| Graphic type | IDs | R9 approximate positions | R10 direction |
| --- | --- | --- | --- |
| Presenter lower thirds | G01, G03, G04, G06, G10, G11, G14, G17, G20, G22, G26, G36 | 0:17, 0:44, 1:06, 1:27, 2:24, 2:44, 3:52, 4:41, 5:25, 5:50, 6:35, 8:30 | Rebuild with the approved HyperFrames `lower-third` template and the Motivation lower-third format. Match text, beats and camera framing. |
| Four-point recap | G44 | 10:34 | Rebuild with the approved HyperFrames `side-list` template if it preserves the existing meaning and timing. |
| Research cards | S01, S02 | 0:29, 7:35 | Use a current HyperFrames template where it fits. Otherwise use the shared Soft Blue Light field and glass treatment for the specialized study layout. Preserve the study content. |
| Dose and step-down diagrams | D01, D02 | 1:39, 4:25 | Preserve the science diagrams and their sequence. The currently approved HyperFrames set has no exact dose-diagram template, so use the shared Soft Blue Light design and motion treatment rather than forcing a diagram into the wrong template. |

The shared approved HyperFrames templates are `lower-third`, `before-card`, `side-list`, and `cycle`, pinned to version 0.8.97 in the project workflow. Use `scripts/video/hyperframes_graphics.py`, `from_plan.py`, the shared compositor and checks. Record the render source, phrase timing and visual QA for each of the 17 segments. Recheck every graphic in the finished film, including its first and last frames, at phone viewing size. The R4 motion clips B01, B03, B04, B05, B06 and B07 are footage, not graphic cards to redesign.

## Revision 3: restore the missing line at about 4:32

R9 moves from **"step down gradually in addition to stepping up gradually"** straight to **"[Skip] the injector pen and go for the needle."** It omits Dan's spoken introduction, making the new tip feel like missing footage. The source is present in `C1607.MP4`:

- Source 600.36 to 604.96: "Don't drop yourself off a cliff, step down gradually in addition to stepping up gradually."
- Source **631.12 to 634.62**: **"Okay, here's the next thing you have to know about weight loss medication."**
- Source 635.28 to 637.86: "Skip the injector pen and go for the needle."
- Source 638.58 to 640.14: "Now let me explain why this is."

Evidence: `/Volumes/Extreme/_edit_work/ro01/analysis/C1607.txt` and the source word index at `/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/footage-index/abs-by-ai-8-14-shoot-teleprompter-ads-indoor-talking-content-outdoor-workout-content-jeff-chagrin-dan-rose/C1607.roll/words.json`. R9 `scene-062` ends after source 604.501 seconds; `scene-063` begins at source 635.18 seconds. That 30.7-second source jump explains the missing introduction. The current subtitles also omit or clip "Skip."

Restore the actual spoken introduction from the original camera and lav footage. Audition source 630.8 to 640.2 with the current cut, choose natural in and out points, and keep the full first word of "Skip." Use a clean shot change or short breath at the tip boundary so the explanation feels deliberate. Include "Now let me explain why this is" only if it makes the subsequent edited sentence flow naturally. Do not manufacture Dan's words. Keep D02's step-down explanation complete before the new introduction. Reposition G17 and every later graphic to the revised spoken beats. The added line will move all downstream timings, so rebuild the SRT, chapters, music extension, graphic plan and exact-file checks from the new final timeline.

## Finish line and review

Build one native 1920x1080 R10 candidate. Watch the entire film with sound, inspect all 17 graphics plus the removed 0:07 spot, and review the 4:25 to 4:45 transition in context. Check every splice, the first-minute picture and music against the R9 approved treatment, the complete words, caption sync, chapters, music loops and ending. Run the project's exact-file audio, visual, framing and delivery gates, then one independent full-candidate review. Fix failures and recheck the affected gates. Deliver the master, SRT, chapters, hashes, gate evidence and a concise change list to Dan for review. Note any automated gate warning that is visually cleared.

## Ready-to-paste starter prompt

Name this task **Keep Your Muscle LFC R10**. This is CONTENT, RO-01 LFC. Execute `Handoffs/handoff-20261006-ro01-r10-blue-hyperframes-transition.md` with `/longform-edit`. Use the R9 final review master as the editorial reference. At 0:07, remove the old green "Keep your muscle" chip completely and show clean original camera footage. Scan all 17 other graphic segments and rebuild them in the current Soft Blue Light and approved HyperFrames treatment. At about 4:32, restore my actual source line, "Okay, here's the next thing you have to know about weight loss medication," so the transition into the injector-pen tip is smooth. Keep my approved footage, voice, color, music and edits outside these changes. Finish and fully review the 16:9 R10 film, SRT and chapters, then show me the complete candidate. Do not upload, publish, deploy, make ad formats or resume the dispatcher.
