---
name: long-form-content-edit
description: Edit or revise organic Abs By AI long-form instructional and story videos from raw footage, with teaching demonstrations, graphics and subtitle sidecars. Use for original long-form content editing; website VSLs, paid ads, extracting Shorts and reframing approved masters use their own workflows.
---

## Default jump-cut and junk-footage QC (Dan, 2026-09-29)

Follow [the shared cut-continuity and junk-footage pass](../../../../.claude/skills/_shared/CUT-CONTINUITY-QC.md) during source selection, before approval previews, and on the exact final candidate. Inventory and inspect every actual join, including reused composite internals. Fix uncovered presenter jumps with distinct fixed wide/tight cuts or complete approved clip cover, then inspect all repaired boundaries. Verify unscripted sounds, empty lead-ins, unnecessary pauses and camera-away resets against the actual source before removing them. Preserve complete words, normal breaths, teaching action, approved framing/color/audio and all still/frame, motion and full-render approval gates. Use native consecutive frames plus moving/audio context; detector scores, sparse sheets and ASR alone are insufficient.


# Edit organic Abs By AI long-form

Use **GPT-6 Sol for the entire organic edit**, including planning, previews, rendering, QA, independent review and revisions. Raise its effort for a difficult section instead of switching models. Use the accepted organic editing/audio components and separately accepted color sample. This Codex adapter reuses existing production modules and private trial recipes; it does not promote a partial color result to a finished full-film master.

Use **Soft Blue Light for all new or revised graphics** and the approved **Motivation format for all lower thirds**. Read the [current graphics standard](references/shared/standards.md#approved-graphics-and-layout-standards-updated-2026-09-26) before choosing graphic components. This overrides older ad palettes and olive/white graphic recipes; preserve source-specific audio, camera color and caption rules.

1. Read [shared standards](references/shared/standards.md) and [organic workflow](references/workflow.md). Verify the brief, raw rolls, assets and ownership. One editor owns planning through self-QA; one independent reviewer enters only after a complete candidate exists. Do not add recurring planner/supervisor loops. In the trial, routine edit choices are delegated.
2. Find the accepted components in [the recipe registry](references/recipes/recipe-registry-v1/recipe.json). Preserve historical sample v1, proposed v1.1 and color addendum as separate records. Measure microphone, posture, framing and color on the actual footage.
3. Use [the runner guide](references/runner.md) to record the video manifest, source/output cut map and scene-to-speech review. Keep one short authoritative list of requested changes and approved elements to preserve. Protect complete teaching demonstrations while removing failed performance and repeated lines.
4. Follow the [organic pre-render path](../../../../.claude/skills/_shared/PRE-RENDER-APPROVAL.md#decision-budget-for-organic-and-other-non-vsl-videos). Reuse the approved studio framing, color and audio profile after checking the actual new roll; reuse Soft Blue Light graphics and Motivation lower thirds. Internally inspect every graphic on its real frame and every clip in context, then present one compact look-and-assets packet covering only material new choices. Show the finished first minute as the next checkpoint, then render the complete video after approvals. New AI motion still needs Dan's approval of start and end frames before generation and a contextual motion check afterward. Lock all assets before full assembly; pending choices stay in plans or isolated previews, not a full placeholder film.
5. Adapt the existing workflow in an isolated directory and preflight. Reuse fingerprint-matching scenes, accepted audio, transcripts and assets. After approval, insert the exact approved choices and rebuild only affected scenes/layers/joins. Submit long rendering/waiting to the existing edit queue and do not spend model turns polling it; until its placeholder states exist, persist the packet, park in a supported waiting state and exit.
6. Remove every placeholder and deliver an SRT sidecar, with no running burned captions or watermark. After editor self-QA, obtain one independent full-candidate review with one consolidated verdict. Keep all exact-file gates and full picture/audio review requirements. Report the revision number, provider charges and available editor/reviewer usage; mark measurements unavailable when the runtime does not expose them.

See [workflow boundaries](references/shared/workflow-boundaries.md) for Shorts or format adaptation. Phase 5's small component replay proves packaging/cache behavior; transfer to a new full video still needs its own build and review.

## Standard 9:16 centering (Dan, 2026-10-03)

For every vertical talking-head build, read the shared section **Vertical talking head: land on him, then hold** in `.claude/skills/_shared/framing-motion.md` in the Abs By AI project. Use its shared `.claude/skills/_shared/cut/landing.py`, never a private smoother.

1. Split at every picture cut, punch-in and return from graphics. Never smooth across cuts.
2. Land exactly on his measured head centre on the first frame. Measure the actual cut frame.
3. Hold while he is within 3.3% of crop width of centre.
4. Outside it, follow only to the band edge, eased over 0.75 seconds, capped at 28% of crop width per second.
5. Takes wandering less than 6.6% of crop width keep one first-frame-anchored centre.
6. Never recenter the exit.

Call `landing.vertical_track(n, raw_head_x, picture_segments, crop_width, fps)`. This uses `landing.track` with scaled 170/608 speed, 40/608 fixed range, 20/608 tolerance and k=3. Report total crop travel, p90 pan speed, time moving, and median/maximum head distance from centre via `landing.motion_stats`. Inspect actual cut landings and head clearance at the original frame rate. These instructions supersede any continuous vertical recentering or unconditional fixed vertical take in older recipes. Square rules, static horizontal framing and the delivery gate remain unchanged. Approved videos stay untouched.
