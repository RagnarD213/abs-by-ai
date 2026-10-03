---
name: long-form-content-edit
description: Edit or revise organic Abs By AI long-form instructional and story videos from raw footage, with teaching demonstrations, graphics and subtitle sidecars. Use for original long-form content editing; website VSLs, paid ads, extracting Shorts and reframing approved masters use their own workflows.
---

## Shared HyperFrames graphics (2026-10-03)

For every new build or graphics revision, read the project's [shared HyperFrames method](../../../../.claude/skills/_shared/hyperframes/README.md). Lower thirds, before/fact cards, 3A side lists and cycles use that folder through `from_plan.py`, the shared `composite.py` and `checks.py`, pinned to **hyperframes 0.8.97**. Do not copy or fork its templates. `orglib` and `modern_graphics` panels are superseded for those four kinds; historical recipes remain reproduction records.

Cut first, map the finished words, and store graphics as data in `plan_resolved.json`. Resolve graphic in/out and every part from spoken phrases, never hand-picked whole seconds. Use the maintained Codex integration `scripts/video/hyperframes_graphics.py` for build, per-frame composition and verification. The RO-10 recipe in `.claude/skills/longform-edit/reference/ro10/` is the framing/build reference. New-video adapters copied from older recipes must replace their old panel path with this integration before rendering.

Record each graphic's template, generated config, text and `driven_by` words in the edit sheet, then run the shared sheet validator. Vertical and square adaptations redraw the same configs with shared `vertical.py` / `square.py`. Kinds without an approved template stay on `softblue.py`; new templates need their own graphic-lock approval. Preserve approved videos, source-specific picture/audio, captions and delivery gates. Check actual composite frames for arms, face and colour before presenting them.


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
