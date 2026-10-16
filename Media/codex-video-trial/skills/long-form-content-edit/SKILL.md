---
name: long-form-content-edit
description: Edit or revise organic Abs By AI long-form instructional and story videos from raw footage, with teaching demonstrations, graphics and subtitle sidecars. Use for original long-form content editing; website VSLs, paid ads, extracting Shorts and reframing approved masters use their own workflows.
---

## Current shared editorial rules (Dan, 2026-10-16)

Read the live project [VIDEO-RULES.md](../../../../.claude/skills/_shared/VIDEO-RULES.md) before the historical recipes. In every new first round, including studio footage, show colour and level-matched voice options; offer the broad, entertaining AI clip selection described there; use title capitalization for new graphic copy with rare all-capital emphasis. An internal audio ranking is not a substitute for Dan's audition options. If he requests text ideas before frames, keep that order. Preserve source-specific locks and the existing frame/motion approval gates.

## First round includes the first-minute draft (Dan, 2026-10-16, RO-26 correction)

Every new long-form first round, including studio footage, includes a playable draft of the first 60 seconds, colour-correction options, level-matched audio options, and all proposed graphics/photos/clips. Do not postpone the draft until graphics approval. Use recommended provisional choices in this limited draft; identify pending AI inserts and keep presenter footage there until approved motion exists. This does not authorize a full placeholder film or motion generation before frame approval.

Show every proposed graphic and existing clip in its intended edit with actual narration and about 3–5 seconds before and after, including entrances/exits. A silent four-second animation, isolated B-roll or still is not enough. Use the shared review-page pattern: first minute at top, one floating scrubbable context player, timeline-ordered cards with “Play in context”, and selectable colour/audio comparisons on the same source passage. Test playback, seeking and audible narration. Read the maintained shared review-page instructions, not an old simplified Codex page.

Verify photo provenance before applying a real-picture disclosure. Read `Docs/memory/ro26-ai-pool-photo-correction.md`; Dan explicitly identified RO-26 O01 as AI-generated. Never infer authenticity from a photo folder, realistic appearance or old label.

## Shared HyperFrames graphics (2026-10-03)

For every new build or graphics revision, read the project's [shared HyperFrames method](../../../../.claude/skills/_shared/hyperframes/README.md). Lower thirds, before/fact cards, 3A side lists and cycles use that folder through `from_plan.py`, the shared `composite.py` and `checks.py`, pinned to **hyperframes 0.8.97**. Do not copy or fork its templates. `orglib` and `modern_graphics` panels are superseded for those four kinds; historical recipes remain reproduction records.

Cut first, map the finished words, and store graphics as data in `plan_resolved.json`. Resolve graphic in/out and every part from spoken phrases, never hand-picked whole seconds. Use the maintained Codex integration `scripts/video/hyperframes_graphics.py` for build, per-frame composition and verification. The RO-10 recipe in `.claude/skills/longform-edit/reference/ro10/` is the framing/build reference. New-video adapters copied from older recipes must replace their old panel path with this integration before rendering.

Record each graphic's template, generated config, text and `driven_by` words in the edit sheet, then run the shared sheet validator. Vertical and square adaptations redraw the same configs with shared `vertical.py` / `square.py`. Kinds without an approved template stay on `softblue.py`; new templates need their own graphic-lock approval. Preserve approved videos, source-specific picture/audio, captions and delivery gates. Check actual composite frames for arms, face and colour before presenting them.


## Default jump-cut and junk-footage QC (Dan, 2026-09-29)

Follow [the shared cut-continuity and junk-footage pass](../../../../.claude/skills/_shared/CUT-CONTINUITY-QC.md) during source selection, before approval previews, and on the exact final candidate. Inventory and inspect every actual join, including reused composite internals. Fix uncovered presenter jumps with distinct fixed wide/tight cuts or complete approved clip cover, then inspect all repaired boundaries. Verify unscripted sounds, empty lead-ins, unnecessary pauses and camera-away resets against the actual source before removing them. Preserve complete words, normal breaths, teaching action, approved framing/color/audio and all still/frame, motion and full-render approval gates. Use native consecutive frames plus moving/audio context; detector scores, sparse sheets and ASR alone are insufficient.


## Scene-content and freeze review (Dan, 2026-10-09)

Follow section 5 of the Abs By AI project's `.claude/skills/_shared/CUT-CONTINUITY-QC.md` before assembly and on the exact final candidate. Check required scenes against independently approved components, not references extracted from the candidate or a suspect flattened parent. Review every `scan.frozen` entry, including declared graphic spans, and record the actual static asset or open defect. Compare every pickup entry/exit in moving original and candidate context. A missing required phone/image, accidental talking-head hold or same-framing hand/pose reset remains open even if inherited or declared. Reused identical evidence cannot preserve a contradicted judgment. Keep incomplete checks and existing automated gate failures explicit.


# Edit organic Abs By AI long-form

Use **GPT-6 Sol for the entire organic edit**, including planning, previews, rendering, QA, independent review and revisions. Raise its effort for a difficult section instead of switching models. Use the accepted organic editing/audio components and separately accepted color sample. This Codex adapter reuses existing production modules and private trial recipes; it does not promote a partial color result to a finished full-film master.

Use **Soft Blue Light for all new or revised graphics** and the approved **Motivation format for all lower thirds**. Read the [current graphics standard](references/shared/standards.md#approved-graphics-and-layout-standards-updated-2026-09-26) before choosing graphic components. This overrides older ad palettes and olive/white graphic recipes; preserve source-specific audio, camera color and caption rules.

1. Read [shared standards](references/shared/standards.md) and [organic workflow](references/workflow.md). Verify the brief, raw rolls, assets and ownership. One editor owns planning through self-QA; one independent reviewer enters only after a complete candidate exists. Do not add recurring planner/supervisor loops. In the trial, routine edit choices are delegated.
2. Find the accepted components in [the recipe registry](references/recipes/recipe-registry-v1/recipe.json). Preserve historical sample v1, proposed v1.1 and color addendum as separate records. Measure microphone, posture, framing and color on the actual footage.
3. Use [the runner guide](references/runner.md) to record the video manifest, source/output cut map and scene-to-speech review. Keep one short authoritative list of requested changes and approved elements to preserve. Protect complete teaching demonstrations while removing failed performance and repeated lines.
4. Follow the [organic pre-render path](../../../../.claude/skills/_shared/PRE-RENDER-APPROVAL.md#decision-budget-for-organic-and-other-non-vsl-videos). Use the approved studio framing, colour and audio profile as the source-checked baseline, and show first-round colour and voice alternatives; reuse Soft Blue Light graphics and Motivation lower thirds. Internally inspect every graphic on its real frame and every clip in context, then present the first-minute draft, colour/audio choices and contextual asset previews together in round 1. Refine that draft after Dan’s choices; render the complete video only after required approvals. New AI motion still needs Dan's approval of start and end frames before generation and a contextual motion check afterward. Lock all assets before full assembly; pending choices stay in plans or isolated previews, not a full placeholder film.
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
