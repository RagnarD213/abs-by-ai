# WV-01 round17: render complete A and run exact-file QA

Created 2026-09-29. Recommended model: **GPT-6 Sol, High effort**.

## Authorization and scope

Dan's direct words on 2026-09-29: "Everything is approved. Let's go ahead and render the full video in the next task. Make a handoff document". This authorizes rendering **complete A in the next task** from the locked assets. This handoff task did not start that render. Complete film B stays deferred, the edit dispatcher stays paused, and publishing, uploads and setup remain off.

The round16 browser export has `full_render_authorized: false` because that review page could not authorize a full render. Dan's later direct message above authorizes the next task. Do not mistake the page's fixed field for a rejection, and do not ask Dan again before the next task's complete A render.

Production root: `/Volumes/Extreme/_edit_work/wv01-edit/`.
Authoritative next plan: `round17-plan/decisions.json`.
Immutable Dan export copy: `round17-plan/dan-export-original.json`, SHA-256 `b320d01b240863c349850ff63d8d64ca5e179e719ece884c88a17b0a2b4db713`.
Prior round report: `Handoffs/handoff-20260929-wv01-round16-first-minute-review.md`.

## Exact round16 approvals

| Item | Approved file | SHA-256 |
|---|---|---|
| Integrated opening review, 0:00 through 1:10 | `round16/previews/WV-01 round 16 first minute REVIEW 540p.mp4` | `28335a7926aac2c67f72fcb153281ca33543c6b4d1b69d4e6e45123cb51a9386` |
| Matching 1080p opening draft | `round16/previews/DRAFT - WV-01 round 16 - first minute through R02.mp4` | `8e27611390d57c54a4e643dc03c3fd332f6c6bda30c3d7fd9ca05eb8c3d464f9` |
| Closing CTA repair context | `round16/previews/WV-01 round 16 closing CTA repair.mp4` | `7db4d1081549aba8ac9f6c80e68f19114757f51e3e13fe2904ce966ca4f26f21` |

The exported decisions approve both the integrated opening and CTA tail, with timestamps 2026-09-29 18:45:34 UTC and 18:45:49 UTC. Dan's direct message confirms everything is approved. The round16 page remains at http://127.0.0.1:8766/round16/index.html; reviewed outputs stay immutable.

The opening includes the exact R01 clip at baseline frames 240-359, photo 1 at 1768-1872, photo 2 at 1873-1977 and the natural presenter return from 1978. Use its approved 1080p picture and approved opening audio. The CTA begins at baseline frame 22329, 14 frames before the old start, covering the inherited presenter splice. It uses approved CTA source frames 125-407, then 14 continued animation frames through source frame 421. The final film duration is not extended by this repair. Recipe and proof: `round16/recipe/build_first_minute.py`, `round16/recipe/build_cta_tail.py`, `round16/recipe/closing_components.py`, and `round16/review/`.

## Other locks and assembly constraints

- R03-A is approved at its exact natural 132-frame, 4.4044-second trim: `round15/motion/R03-A-trim.mp4`, SHA-256 `4c5d1de6e4e7bc84d9800adbd36b0064fe169f6c5396af8db900c1a682a0dcb8`.
- R12-B is the selected approved family motion at its exact natural 9-second trim: `round15/motion/R12-B-9s.mp4`, SHA-256 `407dbe032175c134bc2131b3ec8a202f4fe91488b52a82c767f21ca2be867519`. R12-A is removed.
- R12-B retains the known shirt-sleeve continuity uncertainty: Gemini motion QC FAIL and owner verdict UNCERTAIN. Dan creatively accepted the exact option with that finding disclosed. Keep the finding in the full-candidate review and never call it a technical QC PASS.
- R05, R07 and R09 moving graphic approvals, the 16 cut repairs, opening look, color and audio, V sit twist phone, exact3A, mirror and photos remain locked. Rehash the 49 records in `round15/review/protected-verification-final.json` and the three round16 files above before assembly.
- The immutable baseline is `round12/delivery/WV-01 round12 complete A 1080p.mp4`, SHA-256 `ba00a9b1ecad1ca9cbb1d6e701efad08e90b8d8960d14c074b842d272dc42c03`. Approval clocks refer to it. Source maps and reusable recipes: `round12/review/SOURCE-MAP.json`, `round12/review/COMPONENTS.json`, `round12/recipe/build.py`, `round13/recipe/previews.py`, `round13/review/timing-crosswalk.json`, `round15/recipe/build_previews.py`.
- Apply R04's plus 7 frames, R10's minus 39 frames, and R11's removal of baseline frames 22196-22220 exactly once. Net change from round12 is minus 56 frames. Never repeat round12's earlier 65-frame or 36-frame removals. The expected total is 22570 frames if no other length changes are made; verify this against the fresh assembly map rather than forcing a count.
- The old round12 full-film website gate was FAIL. Earlier creative approvals and short-preview checks do not change that result. Run gates on the new exact full file.

Known cumulative motion generation estimate remains **$29.008017301463925** against Dan's **$50** cap. Charges for 56 historical still calls and provider invoices are unavailable. No new paid generation is requested. Shared machine limit: no more than two local video builds at once.

## Next task

1. Read the shared video rules, organic production skill, this handoff and `round17-plan/decisions.json`. Rehash locked sources. Work in a new isolated `round17/` directory without overwriting reviewed rounds.
2. Assemble and render complete A once from the locked pieces, including the round16 first minute, R03-A, R12-B, R05/R07/R09, approved cut and narration repairs, and continued CTA tail. Preserve original narration and complete final words. Produce the SRT sidecar.
3. Run fresh exact-file audio, picture and delivery gates. Inspect every actual native join, including composite internals and newly patched boundaries; run source and candidate junk-footage checks. Review the complete picture and audio chronologically, subtitle timing, ending and website gate. Obtain one independent complete-candidate review. Report any defect honestly and fix a confirmed defect before presenting the candidate.
4. Deliver the verified complete A for Dan's review. Do not render complete B or publish, upload, deploy the film, or start the paused dispatcher.

The closing words include "So tap the button below." If upload setup is requested later, classify the finished video from its actual ending before choosing a destination. There is no setup authorization here.

## Ready-to-paste starter prompt

Continue WV-01 from `Handoffs/handoff-20260929-wv01-round17-full-A-render-and-QA.md` using `$abs-edit-organic`. I approved the exact round16 integrated first minute and CTA tail, and I authorize the complete A render in this task. Build it once from all locked choices, including R03-A and selected R12-B; R12-A stays removed. Retain the known family B sleeve QC finding. Run fresh exact-file gates, complete picture and audio QA, native join and junk-footage checks, subtitle checks, and one independent complete-candidate review. Show me complete A for review. Keep complete B deferred, the dispatcher paused and publishing off.
