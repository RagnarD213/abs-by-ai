# Approval before a full video render

Dan's standing workflow, 2026-09-26. Applies to every new or revised video: filmed ads, organic long-form, website VSLs, dedicated or extracted Shorts, AI ads and aspect-ratio adaptations. This replaces the earlier instruction to build a complete placeholder film while waiting for asset decisions. The model is the WV-01 round-3/round-4 review package.

## The approval package

Before rendering a complete new video, show Dan one review page or brief with:

1. **The first 30 seconds**, finished enough to approve source-specific color, audio, pacing, opening clips and graphics. For a shorter video, use its actual duration. A revision preserves approved color/audio; reuse their approval and sample unless that treatment changes. Dan explicitly waived a fresh 30-second sample for RO-01 revision 4.
2. **Every planned graphic**, in timeline order, using the exact proposed copy and layout. Show the spoken sentence before it, the speech under it and the sentence after it, with source and output times. Show a moving preview when entrance, reveal, animation or exit matters. A style board alone does not approve all graphics in the film.
3. **Every proposed clip**, including stock, existing B-roll, photos and app demonstrations. Show the exact moving trim/crop with surrounding narration, normally about five seconds before and after when practical. Show both the isolated source and in-context preview where useful. The selected source preview remains 0.5-15 seconds; its contextual audition may be longer.
4. **Every proposed AI scene**, with its concept, intended action, matching start/end frames, duration and estimated cost. Generate stills for this review only when authorized. If Dan requests ideas only or says not to generate frames, present concepts and stop before images. After frame approval, generate motion, inspect it and obtain clip approval before the full-film render. Explicit authorization to generate and use a specified clip remains valid; do not ask twice.

Use the exact [Soft Blue Light family](GRAPHICS-STANDARDS.md) and Motivation lower-third format. Each graphic must teach or distill something. A single point normally becomes a concise `KEY POINT:` lower third, with the label in capitals and the point in Title Capitalization. An explicit `TIP:` or numbered section label is allowed. Do not inflate one word or a short sentence into a largely empty full-screen or left-third card. Use a larger layout when a readable study abstract, comparison, diagram, demonstration or substantive list warrants the space. Verify research against the actual source; a screenshot is not evidence for wording the source does not support.

## Lock before assembly

Keep one authoritative approval packet with item IDs, requested changes, approved elements, media paths/hashes, source/output times, before/during/after speech, proposed copy, source provenance, approval scope and Dan's exact decisions. A style approval and an item/content approval are different. Preserve unchanged approved items; show changes and remaining decisions together in one batch, not repeated per-item permission prompts.

A complete film can be rendered only after the first-30-second treatment (or recorded reuse/waiver), all graphics and all selected clips are locked. If one is pending, continue only independent preparation, source analysis, transcripts, edit decisions, isolated graphic previews and short contextual auditions. Do not spend time rendering the whole film with placeholders. Placeholders may exist in the plan and limited review excerpts, which remain clearly marked DRAFT.

Use existing `placeholders.json` for clip identities and approval fingerprints; retain its schema for current tools. Record the opening, all graphics and broader creative approvals in a separate work packet/approval manifest. The queue's `frames_approved` state means frame approval, not proof that every graphic and finished clip is locked. Do not claim a new automated gate exists. Park using supported queue states and preserve a paused dispatcher. No AI session stays alive to poll for Dan's answer.

Once locked, render from approved components, reuse unchanged caches and audio, rebuild only necessary scenes/joins, then perform the existing exact-file checks and full picture/audio review with one independent complete-candidate reviewer. Creative approval does not waive final checks or authorize publishing.

## Editing checks before the package

Review pauses, resets, false starts, stray words and awkward joins against the source and finished audio. Remove confirmed junk without clipping syllables or deleting meaningful teaching breaths. Inspect the words on both sides of each edit. If timing changes, regenerate output time maps, graphics timing, subtitles and chapters. Approval of color or audio treatment survives a necessary clean cut; old exact-file stamps do not.

## Reference workflow

- `Handoffs/handoff-20260925-wv01-round3-lock-crop-and-graphics.md`
- `Handoffs/handoff-20260925-wv01-round4-locked-style-and-iphone.md`
- `/Volumes/Extreme/_edit_work/wv01-edit/round4/index.html` and `WORK_PACKET.json`

Copy the review structure, stable item IDs, context and scoped lock decisions. Do not borrow WV-01 source-specific crop/grade/audio settings. A review page with many videos uses `preload="none"` and supports seeking. Do not execute another task's renderer or modify its work directory.
