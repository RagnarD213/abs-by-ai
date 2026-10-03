---
name: abs-edit-ad
description: Edit or revise filmed Abs By AI ads from raw camera footage and a spoken script, using the accepted ad treatment and shared video standards. Use for original ad editing; an approved master needing new dimensions or a shorter cut uses the existing adaptation workflow.
---

## Default jump-cut and junk-footage QC (Dan, 2026-09-29)

Follow [the shared cut-continuity and junk-footage pass](../../../../.claude/skills/_shared/CUT-CONTINUITY-QC.md) during source selection, before approval previews, and on the exact final candidate. Inventory and inspect every actual join, including reused composite internals. Fix uncovered presenter jumps with distinct fixed wide/tight cuts or complete approved clip cover, then inspect all repaired boundaries. Verify unscripted sounds, empty lead-ins, unnecessary pauses and camera-away resets against the actual source before removing them. Preserve complete words, normal breaths, teaching action, approved framing/color/audio and all still/frame, motion and full-render approval gates. Use native consecutive frames plus moving/audio context; detector scores, sparse sheets and ASR alone are insufficient.


# Edit a filmed Abs By AI ad

Use this project's accepted original-ad components, with the source-specific limits preserved. Canonical private sources live in `Media/codex-video-trial`; this discoverable skill is an adapter over the existing production code, not an alternate audio chain or quality gate.

Use **Soft Blue Light for all new or revised graphics** and the approved **Motivation format for all lower thirds**. Read the [current graphics standard](references/shared/standards.md#approved-graphics-and-layout-standards-updated-2026-09-26) before choosing graphic components. This overrides older ad palettes and olive/white graphic recipes; preserve source-specific audio, camera color and caption rules.

1. Read [shared standards](references/shared/standards.md) and [ad workflow](references/workflow.md). Confirm the script, raw footage, requested formats and ownership. One editor owns planning through self-QA; one independent reviewer enters only after a complete candidate exists. Do not add recurring planner/supervisor loops. Routine take/graphic choices are delegated in the Codex trial.
2. Choose the accepted recipe through [the registry](references/recipes/recipe-registry-v1/recipe.json). Preserve Ad 1's accepted sound/color, but exclude its four known picture errors. Calibrate microphones, color and framing for new footage.
3. Create the per-video manifest and scene map using [the runner guide](references/runner.md). Keep one short authoritative list of requested changes and approved elements to preserve. For a near-final revision, treat that change list as exhaustive and protect approved elements with hashes or decoded-frame evidence. Check the spoken claim, person, action, before/after role, demonstrative referent and label treatment before rendering.
4. Follow the [complete pre-render approval workflow](references/shared/standards.md#approval-before-a-full-render). Show the first 30 seconds for color/audio and opening approval, every graphic with surrounding speech, clips in context and authorized AI start/end frames. Lock all graphics and finished clips before full assembly; reuse unchanged approvals or an explicit sample waiver. Pending choices stay in the plan or isolated auditions, not a full placeholder film.
5. Run preflight in an isolated directory. Reuse fingerprint-matching scenes, accepted audio, transcripts and assets. After approval, insert the exact approved choices and rebuild only affected scenes/layers/joins. Submit long rendering/waiting to the existing edit queue and do not spend model turns polling it; until its placeholder states exist, persist the packet, park in a supported waiting state and exit.
6. Remove every placeholder before delivery. After editor self-QA, obtain one independent full-candidate review with one consolidated verdict. Keep all exact-file gates and full picture/audio review requirements. Report the revision number, provider charges and available editor/reviewer usage; mark measurements unavailable when the runtime does not expose them.

For format adaptation, cutdowns and specifically filmed short-form, read [workflow boundaries](references/shared/workflow-boundaries.md). Do not silently add formats, publish a trial, or claim the small replay proves a new full-film edit.

## Standard 9:16 centering (Dan, 2026-10-03)

For every vertical talking-head build, read the shared section **Vertical talking head: land on him, then hold** in `.claude/skills/_shared/framing-motion.md` in the Abs By AI project. Use its shared `.claude/skills/_shared/cut/landing.py`, never a private smoother.

1. Split at every picture cut, punch-in and return from graphics. Never smooth across cuts.
2. Land exactly on his measured head centre on the first frame. Measure the actual cut frame.
3. Hold while he is within 3.3% of crop width of centre.
4. Outside it, follow only to the band edge, eased over 0.75 seconds, capped at 28% of crop width per second.
5. Takes wandering less than 6.6% of crop width keep one first-frame-anchored centre.
6. Never recenter the exit.

Call `landing.vertical_track(n, raw_head_x, picture_segments, crop_width, fps)`. This uses `landing.track` with scaled 170/608 speed, 40/608 fixed range, 20/608 tolerance and k=3. Report total crop travel, p90 pan speed, time moving, and median/maximum head distance from centre via `landing.motion_stats`. Inspect actual cut landings and head clearance at the original frame rate. These instructions supersede any continuous vertical recentering or unconditional fixed vertical take in older recipes. Square rules, static horizontal framing and the delivery gate remain unchanged. Approved videos stay untouched.
