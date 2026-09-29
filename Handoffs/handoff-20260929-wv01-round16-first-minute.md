# WV-01 round16: approved motions, first-minute review

Created 2026-09-29. Recommended model: **GPT-6 Sol, High effort**.

## Goal

Make the next edit in a new isolated `round16/` directory. Show the final opening and first minute with the approved pieces together. Then record Dan's decision. Do not render the complete film in this round. Full-film B stays deferred, the edit dispatcher stays paused, and publishing stays off.

Production root: `/Volumes/Extreme/_edit_work/wv01-edit/`.
Decision plan: `round16-plan/decisions.json` under that root.
Dan's original export is preserved at `round16-plan/dan-export-original.json`, SHA-256 `4c77bb05056a3d132e8dfe2bbd8de864480d114366c6ac52fd269924be8edddc`.
Previous round details: `Handoffs/handoff-20260929-wv01-round15-motion-results.md`.

## Dan's decisions

Dan wrote: "Okay everything is approved. Anything else we need to do before we render the next video? Create a handoff document to make the next edit in the new task". His attached exported choices are more specific:

| ID | Decision | Exact approved or removed review files |
|---|---|---|
| R03-A | Approved | `round15/previews/R03-A-context.mp4` (`dc67718d07e548944c6d89fdc51222ebdba2fe1b7d5e7e5f4575ec73fdcfe596`); `round15/motion/R03-A-trim.mp4` (`4c5d1de6e4e7bc84d9800adbd36b0064fe169f6c5396af8db900c1a682a0dcb8`) |
| R12-A | Remove | Preserve both reviewed files as history; do not install this option. Dan's note: "The other clip was better". |
| R12-B | Approved and selected | `round15/previews/R12-B-context.mp4` (`9559875134c1af3fddb398c330b8cb3352aa1ae9fd1729feaef01e5e0baa52de`); `round15/motion/R12-B-9s.mp4` (`407dbe032175c134bc2131b3ec8a202f4fe91488b52a82c767f21ca2be867519`) |

The review export still says `full_render_authorized: false`, a default field from the approval page. Dan approved the two selected motions in his message and export. It does not state that he has seen the final combined first minute. Do not ask him to reapprove these exact motions or the three approved round14 moving graphics (R05, R07, R09).

Family B's shirt sleeves remain an **editor QC uncertainty**. Gemini's motion verdict was FAIL; native consecutive frames showed gradual head clearance, while clear sleeve passage could not be established. Dan approved the exact B option with that finding visible. Record this as creative acceptance of the known issue, not a technical QC PASS. Preserve the report for the complete-candidate review. No new generation is requested.

## What remains before a complete render

1. **Integrated first-minute preview.** The approved opening look and phone exercise already exist. R01, the approved existing clip, changes baseline 0:08-0:12. Build a short preview of the current opening with that clip and the later approved changes. Include the R02 photo action that begins around 0:59 through its natural exit near 1:06, so the preview does not end in the middle of it. This is the remaining pre-render review step in `.claude/skills/_shared/PRE-RENDER-APPROVAL.md`. Save the exact file and Dan's decision. Earlier approvals of individual parts remain locked.
2. **Closing CTA tail repair.** Round15 covered an exposed presenter splice by advancing the existing approved CTA 14 frames, from baseline frame 22343 to 22329. The round12 `round6/previews/closing-context.mp4` source has exactly 408 frames and the previous assembly used its last frame. Applying a `source + 14` mapping through the old film end would read past that file. Inspect the final words and actual CTA source. Resolve the last 14 frames with a natural ending or continuous approved-style CTA motion, without freezing, stretching, truncating speech, or re-exposing the presenter jump. Review the small changed ending if its visible treatment changes.
3. After the first-minute decision and CTA repair, a later task can assemble complete A from locked pieces and run fresh exact-file gates, full chronological picture and audio QA, native cut and junk-footage checks, subtitle timing, and one independent complete-candidate review. The inherited round12 full-film website gate was FAIL. Creative approvals do not change that result; the new exact film must be tested.

## Build facts to preserve

- Immutable round12 baseline: `round12/delivery/WV-01 round12 complete A 1080p.mp4`, SHA-256 `ba00a9b1ecad1ca9cbb1d6e701efad08e90b8d8960d14c074b842d272dc42c03`. Approval clocks refer to it. Rehash 49 protected records in `round15/review/protected-verification-final.json` before editing.
- Source maps and working code: `round12/review/SOURCE-MAP.json`, `round12/review/COMPONENTS.json`, `round12/recipe/build.py`, `round13/recipe/previews.py`, `round13/review/timing-crosswalk.json`, and `round15/recipe/build_previews.py`. Adapt in `round16/`; never overwrite a reviewed output.
- Exercise R03-A uses the exact approved 132-frame, 4.4044-second natural trim, not the settled 6-second paid source. Family R12-B uses its approved natural 9-second trim, not the 10-second paid source. Preserve their AI labels and exact contextual decisions.
- Approved moving graphics R05/R07/R09 stay fixed. Preserve the first-minute color, audio, crop, opening, V sit twist phone, exact3A, mirror, photos and 16 approved cut repairs. R04 adds 7 narration frames; R10 removes 39; R11 removes baseline frames 22196-22220 once. Net audio change after round12 is minus 56 frames. Do not apply round12's earlier 65-frame or 36-frame removals again.
- Round15 inspected 17 actual native joins and reused the source-junk pass over 15 selected C1697/C1698 pieces and 43 detector leads. Keep full words, breaths and teaching action. Source and final candidate need their own cut and junk-footage pass.
- Known cumulative motion-generation estimate: **$29.008017301463925** against Dan's authorized **$50** cap. Charges for 56 historical still calls and provider invoices are unavailable. No new paid call is required for this round. Separate round15 Gemini QC estimate: $0.847312.
- Shared limit: no more than two local video builds at once. Review server `com.absbyai.wv01-review` on port 8766 stays available; preserve older pages. Keep `scripts/edit-queue/PAUSE` in place. No uploads or publishing.

## Exact next action

Read the round16 decision plan and the production skill. Rehash the approved sources, then build and review only the current first-minute excerpt in an isolated round16 folder. Investigate the 14-frame CTA tail in parallel without starting the complete film. Deliver the excerpt for Dan's decision with a short list of any remaining technical repairs.

## Ready-to-paste starter prompt

Continue WV-01 from `Handoffs/handoff-20260929-wv01-round16-first-minute.md` using `$abs-edit-organic`. My round15 export approves exercise R03-A and family R12-B, removes R12-A, and selects B. Build the final combined first-minute preview in a new isolated round, including the approved R01 clip and the complete R02 photo action, then show it for approval. Resolve the 14-frame closing CTA tail for later assembly. Preserve all other exact approvals and the known family B sleeve QC finding. No full render in this round. Keep full-film B deferred, dispatcher paused and publishing off.
