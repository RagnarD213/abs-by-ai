# AD: Fired Them All website VSL, Version B intro first cut

Created 2026-10-07 for a new Codex task. Recommended model: **GPT-6 Astra, high effort**. Task title: **Fired Them All AD R1**. Astra is appropriate because this is a new sales opening with take selection, a new visual argument, and a precise join into an approved film.

## Goal

Make the first reviewable cut of the **WV-01 Version B opening only**, in 16:9. The opening begins with Dan saying he fired his personal trainer, nutritionist and meal-prep service, develops the three hours versus 165 hours support gap, and ends with his skeptical-viewer bridge. Join it to the approved Version A picture and audio at **“Number one, AI got me back in the gym.”** Show Dan the new opening and join for review. Do not render the complete B film in this round.

This is the website VSL with a direct button CTA, classified as an AD for the project's video rules. It is not an organic channel video. Nothing in this handoff authorizes an upload, website installation or publishing.

## Sources verified on disk

- Raw Version B intro: `/Volumes/Extreme/dan rose fitness 9:23 shoot - vsls, long form content, short form content/C1699.MP4` (7:07.928, 3840x2160, 29.97 fps).
- Raw Version B pickups: `/Volumes/Extreme/dan rose fitness 9:23 shoot - vsls, long form content, short form content/C1700.MP4` (1:59.620). These six callbacks are for the later complete B assembly, not this first opening cut.
- Approved Version A master: `/Volumes/Extreme/_edit_work/wv01-edit/round17/final/WV-01 FINAL Website VSL A 1080p.mp4`, SHA-256 `acddfb5b3bad7bb6d85f937b74054fafb4be33505f49ae91cd765a8ecac88836`. Its SRT and VTT are beside it. Dan approved this exact A master on 2026-09-29. Preserve it unchanged.
- The A master reaches **“Number one, AI got me back in the gym” at 00:02:50.537** in its SRT. That is a navigation marker, not a frame-accurate splice. Match the heard words, picture and audio at the actual join.
- Reusable source transcripts and timings: `Media/footage-index/dan-rose-fitness-9-23-shoot-vsls-long-form-content-short-form-content/C1699.roll.md`, `C1700.roll.md`, their `words.json` sidecars, and `Handoffs/video-editing/WV-01-SOURCE-MAP-20260924.md`. Local planning transcripts are in `Media/wv01-planning-20260924/`.
- Shoot properties: `Docs/SHOOT_923_FOOTAGE_REPORT.md`. This shoot is S-Cinetone/Rec.709, not S-Log. Its single audio stream is dual mono. C1699 measured more room echo than A, so match its sound to the approved A reference by listening, using the shared audio tools.

## Script and intended structure

Dan's recorded teleprompter script is [VSL 1, Version B intro](https://docs.google.com/document/d/1qt47J2sWcdLXIQYQ055dooKPad8cOJrFMsYhj0VWrIQ/edit). The production directions are in [9/23 Shoot Scripts & B Roll](https://docs.google.com/document/d/1tTPTksuG_YwifjMWohtmXpelrjTFdo8KzjfxyuVvxq4/edit), under **“Fired them all, EXTENDED INTRO (VSL Version B)”**. Verified local snapshots of both documents are `Media/wv01-planning-20260924/source-teleprompter.json` and `source-cues.json`. Read the live documents for any later edits before cutting, then compare their wording with the recorded speech. The recorded performance controls the edit unless Dan has specifically requested a change.

The seven scripted beats are: B1 fired the three helpers and showed the result; B2 trainer credibility; B3 five things and app promise; B4 why the viewer lacked an expert team; B5 the 168-hour week and unsupported 165 hours; B6 AI's ongoing availability and Dan's better result; B7 the skeptic bridge into the shared motivation section. The 9/24 production plan, `Handoffs/video-editing/WV-01-EDIT-PLAN-20260924.md`, gives the visual treatment. Preserve the support-gap argument, not just the first sentence.

C1699 has false starts. `00:20-01:29` contains partial opening attempts; `01:34-02:37` is the strongest complete opening candidate in the source map. At about `03:48-04:18`, choose the take that says trainer, nutritionist **and meal-prep service** to match the opening. A retake swaps in “sleep coach.” At `04:19-04:54`, the drive-through and fridge sequence repeats; use one progression. `06:47-07:03` contains a clean skeptical-viewer bridge candidate. Listen and inspect actual takes before choosing frame boundaries. Exclude slate and production talk. Dan already confirmed the personal story, so do not reopen it as a factual question.

The original script estimates a roughly 3:44 spoken introduction at Dan's planned pace. Actual edit length follows the best recorded delivery. Do not speed up speech to hit the estimate.

## First-round edit and review

1. Read `$vsl-edit`, `.claude/skills/_shared/VIDEO-RULES.md`, `PRE-RENDER-APPROVAL.md`, `GRAPHICS-STANDARDS.md`, `CUT-CONTINUITY-QC.md`, and `Handoffs/video-editing/00-RULES.md`. Check the coordination board for another WV-01 owner before claiming implementation. Work in a new isolated folder such as `/Volumes/Extreme/_edit_work/wv01-edit/version-b/round1/`. Do not overwrite A or earlier review rounds.
2. Verify the A master hash. Make a take map for C1699, selecting complete, natural lines and marking every false start, repeat and join. Build a clean speech cut. Keep horizontal presenter framing static. Match the approved A look, graphics family and sound where the recordings permit, using the project's current shared methods.
3. Search the clip library before choosing B-roll. Reuse approved A proof photos and old-channel footage where suitable. The B concept has new role cards and a 168-cell support graphic: show material new graphics as stills on the actual graded frame, then moving context for approval. Do not add generic illustration that weakens Dan's personal argument. Any new AI motion needs Dan's approval of its start and end frames before generation. Plan this round without paid generation.
4. Prepare a review page with the new opening in moving context, the B-to-A join, graphic stills and motion where ready, the source choices, and a short **“What I decided”** list. Put the first minute at the top. A labelled placeholder is acceptable only for a planned clip whose assets still need approval. A full placeholder film is not the deliverable.
5. Review every source and picture join for presenter jumps and junk footage, listen across the B-to-A audio transition, and inspect moving picture for readable text and clean framing. Show Dan the 540p review copy plus the best-quality preview. State which creative assets still need approval. Do not claim full-film or delivery-gate completion from an opening preview.
6. Record Dan's exact decisions and asset hashes, then make the next focused round handoff. Once this opening is approved, a later task can build complete B with the six C1700 callbacks in the places specified by `WV-01-SOURCE-MAP-20260924.md`. Preserve approved A scenes and the established seven-day trial, $19.99 per month offer.

The existing A master has a recorded website delivery-gate FAIL despite Dan's creative approval. The B opening must report its own checks honestly; do not describe the inherited A gate result as a pass.

## Ready-to-paste starter prompt

AD: Edit the WV-01 “Fired Them All” Version B website VSL intro as **Fired Them All AD R1**. Use `$vsl-edit` and `Handoffs/handoff-20261007-wv01-version-b-intro-first-cut.md`. Cut C1699 into the substantial B opening, develop the 168-hour support argument, and make a clean join to the approved A master at “Number one, AI got me back in the gym.” Reuse approved A assets and look, show me a first-minute and opening review packet with material new graphics and clips in context, and record take choices and checks. This task is the first cut of the opening only. Keep the complete B render, C1700 callbacks, uploads and publishing for later tasks.
