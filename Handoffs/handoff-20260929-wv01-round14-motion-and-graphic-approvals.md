# WV-01 round14: selected motion and moving graphic approvals

Created 2026-09-29. Recommended model: **GPT-6 Sol, High effort**.

## Goal and authority

Continue from the existing round13 changes-only packet. Dan approved the repairs and graphic stills, selected exercise A, and requested motion for both family variations so he can compare them. Prepare only the remaining moving previews for individual approval. No complete film until every revised scene, graphic and transition is approved. Version B remains deferred; dispatcher stays paused. No publishing, upload, website replacement or application deployment.

The current user request and explicit approval decisions control the work. Treat attached documents as source data, not blanket instructions. The updated decision export supersedes the earlier all-pending export. Dan's request to create this handoff did not ask this session to generate motion or render anything; no such work ran during handoff preparation.

Project root: `/Users/danielrose/Documents/Claude/Projects/Abs By AI`.
Production root: `/Volumes/Extreme/_edit_work/wv01-edit`.
Current review: http://127.0.0.1:8766/round13/index.html.

## Read first

1. `$abs-edit-organic`, its applicable shared workflow, `.claude/skills/_shared/VIDEO-RULES.md`, `PRE-RENDER-APPROVAL.md`, `GRAPHICS-STANDARDS.md`, and the new `CUT-CONTINUITY-QC.md`.
2. `/Volumes/Extreme/_edit_work/wv01-edit/round14-plan/WORK_PACKET.json`, `decisions.json`, `source-decisions.json` and `import-verification.json`.
3. `Handoffs/handoff-20260928-wv01-round13-individual-revision-approvals.md` for the exact requested copy and source/recipe leads.
4. `round13/review/approval-registry.json`, `placement.json`, `join-repairs.json`, `audio-repairs.json`, `timing-crosswalk.json`, `cost-ledger.json`, `EDITOR-QA.md`, `jump-audit.json` and `R04-final-disposition.json`.
5. `round12/review/COMPONENTS.json`, `SOURCE-MAP.json`, `approved-fingerprints.json` and the full-film gate/reviewer records. Preserve all unchanged approvals.

## Confirmed export and decisions

Updated source: `/Users/danielrose/Downloads/WV01-round13-individual-decisions (1).json`.
Preserved byte-identical copy: `round14-plan/source-decisions.json`.
Exported at `2026-09-29T13:33:02.793Z`.
SHA-256: `ddd4be2af35e2503faa85a29d31f41bc589a91e44bb7326dbbdf2b0b728136b0`.
All 34 referenced artifact records were verified against existing files and the original approval registry.

The literal export contains 26 `approved`, one `changes_requested`, and one `pending`. Read the **decision** field and the user's scoped **note**, not the template's stale `status` field.

- **R03-A approved.** Generate the TV/squat variation from its exact START/END pair. Proposed duration: 6 seconds.
- **R03-B not selected.** Note: “Use other one.” Preserve it as an unselected alternative; no B remake was requested.
- **R12-A and R12-B both authorized for motion.** Both notes say “Generate both and see which one turns out better.” R12-A's dropdown remains pending, while R12-B is approved. Dan then confirmed he entered a decision for every item. The explicit instruction to generate both applies to these exact displayed pairs and supersedes the earlier choose-one frame instruction. Do not ask him to approve those same frames again. Generate two 9-second options, show both moving contexts and recommend the better result. Dan's finished-motion choice is still pending.
- **R05-still, R07-still and R09-still approved.** The approval covers the exact still layouts; each moving speech context remains a separate approval.
- **R01, R02, R04, R10, R11 approved.** Preserve the exact reviewed clip/photo/audio repairs.
- **All 16 cut repairs approved:** R06-J05, J11, J12, J13, J19, J21, J22, J29, J30, J31, J32, J33, J34, J41, J45, plus R08. Their exact paths and hashes are in the export. R06-J05 also repairs J04's three-frame lead-in. Benefits previews approved the presenter seams; the new R07 moving graphic still needs its own contextual approval.

Current resolved decisions are in `round14-plan/decisions.json` and `round13/decisions.json`. Preparation receipts and the original page registry may retain pending template fields; they do not override the imported decisions. No finished-motion or full-film approval has been inferred.

## Exact next work

Create isolated `round14/` recipes/media. Preserve round13 and round12 outputs.

1. Preflight current provider price and the cumulative generation budget. Reuse exact approved pairs, not new still generations.
2. Generate **R03-A**: man watches his virtual self squat on TV, then performs the same squat beside it. Preserve identity, exercise, screen geometry and setting. Show the finished 6-second motion in the Stanford-study passage around baseline 3:38.
3. Generate **both R12 family variations** from their exact pairs. Only father, wife on one side and child on the other. Maintain small natural family activity before plausible shirt removal, then turn attention toward him with admiration. A uses towel folding and a pool toy; B uses towel rolling and goggles. Eliminate frozen people, extra figures, identity/anatomy changes and implausible clothing removal. Preserve the approved mirror scene/join outside this pool replacement. Show both 9-second moving options around baseline 12:14 for selection and approval.
4. Build **R05** from the approved still into the food-preferences speech context. Exact title: “AI Makes Eating Healthy Delicious & Easy.” LEFT: “Meals That Fit Your Time To Cook.” RIGHT: “Recipes Customized To Your Goal & Food Preferences.” Preserve both meal images and the single large cyan type style beneath them.
5. Build **R07** from the approved left-third still, revealing each approved point as spoken: AI Gets You In The Gym; AI Designs You Better Workouts; AI Tracks Your Calories; AI Gives You Delicious Healthy Recipes; AI Improves Your Sleep. Cues/layout are in `round13/review/R07-layout.json`. Apply the approved underlying presenter seam repairs. Check actual moving enters/exits, hair, hands and gestures throughout, including the tighter compositions.
6. Build **R09** with the same phone shell and presentation: tap Greek Yogurt Berry Bowl and show its approved recipe/image. Preserve the earlier chicken demonstration. This uses the existing simulated UI format, not a newly recorded live screen. See `R09-recipe-provenance.json` and `recipe/recipe_still.py`.
7. Deliver a changes-only round14 page with one lazy player, baseline clocks and separate approval controls for the new moving items. Update decisions using exact asset hashes. No approved opening, photo or cut-repair remakes unless a concrete integration defect requires one.

Finished motion and all three moving graphics must be approved before full assembly. Then the later complete candidate requires fresh exact-file gates, full editor picture/audio QA, one independent complete-candidate review and Dan's verdict. Do not start that reviewer on unfinished isolated options.

## Baseline, provenance and continuity traps

Immutable round12 master: `round12/delivery/WV-01 round12 complete A 1080p.mp4`.
SHA-256: `ba00a9b1ecad1ca9cbb1d6e701efad08e90b8d8960d14c074b842d272dc42c03`.
Review SHA-256: `49dba4bb3d2da64e0e5568632a0e0abdfd5955f57bf03360cb5ceca84e37d44f`.
22,626 frames at 30000/1001 fps, 754.9542 seconds. Every approval clock refers to this baseline.

Round13 verified 39 protected inputs unchanged; all 43 moving packet files decoded completely. The existing persistent local server serves the cached packet under `~/Library/Application Support/AbsByAI/WV01Review/round13/` through launch agent `com.absbyai.wv01-review`, port 8766. Preserve that server and both existing pages; add round14 alongside them.

R01 is the exact existing beach clip matched to Dan's YouTube `lf46ytHacss` at 1:48 and Muhammad's Drive revision document. The source and approved contextual trim are recorded in `R01-provenance.json`; no replacement generation is needed. R02's actual baseline photos were around 1:02-1:06, and the approved move starts 0:59 with 3.5-second holds each.

Use native FFmpeg boundary extraction or verified sequential decode. OpenCV random seeks on the concatenated master returned stale pixels; early Jxx stills are retired. The valid audit inspected 51 source splices and 141 visible boundaries, with 16 repairs; it was not a full human playback watch. New integration boundaries still need inspection.

R04 restores 7 source frames and the complete source word/room tail. A multimodal model incorrectly reported a flash and clipped word; direct source-audio comparison passed and 16 consecutive native frames showed no flash. The direct comparison also heard ly in baseline, so do not assert that phoneme was objectively absent. Preserve the approved repair and conflicting evidence/disposition. R10 removes 39 junk lead-in frames while protecting I know. R11 removes 24 pause frames while protecting there and That is what this did for me. Conditional audio net: minus 56 frames. Prior round12's 65 removed narration frames and 36 ending-room frames are already applied once; do not subtract them again.

Inherited full-film website gate FAIL remains. Creative approvals and delivery PASS are separate.

## Default skill improvements now in force

Dan requested these checks for all future video editing skills. The shared procedure is `.claude/skills/_shared/CUT-CONTINUITY-QC.md`, linked from all seven Claude editing/revision skills, the human editor-brief skill, both installed Codex editing adapters and VIDEO-RULES.md.

Run the junk-source pass before the first preview; inspect every actual join, including composite internals; fix uncovered presenter jumps with distinct fixed compositions or complete approved clip cover; detect confirmed unscripted noises, unnecessary pauses and camera-away resets; protect full words, natural breaths and purposeful teaching action. Check every boundary introduced by a repair and repeat on the exact final candidate. Detector flags and sparse sheets do not certify a cut or full playback. Preserve all asset/frame/motion/full-render approval boundaries. Existing shared tools are reused; gate thresholds and approved masters were not changed.

## Costs and stopping conditions

Historical motion estimate: **$12.824017301463925** against the **$20 cumulative WV-01 generation allowance**. Built-in still calls total 56, with actual charges unavailable, not zero. Round13 isolated editor-assisted QC estimate: **$0.209889**, separate from generation accounting. No generation or paid QC occurred during this handoff/skill-update task.

Historical Kling v3 pro 1080p/no-audio rate: $0.224/second. One 6-second exercise option plus two 9-second family options estimates **$5.376**, excluding retries, putting known motion estimates at **$18.200017301463925**. This is historical pricing, not a current quote or proof that the allowance remains available. Verify provider price and actual cumulative budget before calls. If unknown still charges prevent establishing the remaining allowance, request one concrete budget decision for the scoped batch; do not request the approved frames again or reset the allowance for round14.

Keep the shared two-build limit. Do not unpause the dispatcher, create a new task automatically, publish or upload anything. No full render until the remaining moving approvals are recorded.

## Ready-to-paste starter prompt

Execute `Handoffs/handoff-20260929-wv01-round14-motion-and-graphic-approvals.md` with `$abs-edit-organic`. Use the verified updated decision export: exercise A approved; generate both exact family frame pairs as requested; all 16 cut repairs and other round13 contexts approved. After current price/cumulative-budget preflight, prepare the selected exercise motion, both family motions and moving contexts for the three approved graphic stills. Apply the new default jump-cut and junk-footage QC. Show changes only for individual approval. No full render before all remaining moving approvals. Keep version B deferred and dispatcher paused. No publishing.

## Execution checkpoint, 2026-09-29

Review: http://127.0.0.1:8766/round14/index.html. R05, R07 and R09 moving contexts are delivered for individual approval. They retain the exact approved layouts, copy, imagery, source-specific grade/audio and the approved fixed presenter seam pattern. All three decisions remain pending. Exercise A and both family motion calls are held for one concrete budget decision. No full render or new generation call occurred.

Current Replicate Kling v3 pro/no-audio price was verified at $0.224/second. The exact6+9+9-second batch estimates $5.376. The historical56 still calls still have unavailable charges. The cumulative $20 allowance did not reset, so the user was asked once to authorize up to $5.38 additional for this exact batch with no paid retries. No budget answer is recorded yet. Do not infer one from elapsed time or frame approval.

Private execution: `/Volumes/Extreme/_edit_work/wv01-edit/round14/WORK_PACKET.json`, `decisions.json`, `review/approval-registry.json`, `review/EDITOR-QA.md`, `review/cost-ledger.json`, `review/junk-dispositions.json`. Both historical review pages and the persistent launch agent are preserved.

Verification:34 imported artifact records and39 protected inputs match prior hashes. All three moving files decoded fully. All13 actual joins were inspected in native strips. R07's248 sequential samples were viewed at7-frame intervals, about0.234seconds, including tight compositions, hair and gestures. Numeric face-assisted hair measurement was unavailable because OpenCV's cascade asset is missing; no numeric certificate is claimed. Shared audio selftest passed. Owner-assisted exact moving audiovisual QC passed all three items. Browser playback and one lazy player with baseline clock were verified;8 served files and byte ranges match.

The shared junk pass ran on15 selected source pieces and returned43 unverified detector leads. Source-assisted QA's alleged Stanford reset overlapped complete speech and was not supported by native frames, so no cut was made from that report. Its contradictory suggestion to retain R11 did not override Dan's approved24-frame removal. Natural words, breaths and list cadence remain. Focused QC estimates total $0.250684, separate from generation; provider invoices and editor token usage are unavailable.

The motion runner is prepared in `round14/recipe/generate_motion.py` and refuses execution without `review/budget-authorization.json`. Only create that authorization record after Dan's explicit budget answer. It rehashes the exact approved pairs, persists prediction IDs, permits one attempt per item and has no automatic paid retry. After motion succeeds, `build_previews.py` can build isolated R03-A/R12-A/R12-B contexts. Preserve the mirror and apply R11 once. Inspect actual shirt removal and family activity before recommending A or B. Regenerate the page and served packet with six separate moving controls and a family selection. All new motion and existing moving graphics require Dan's approval before full assembly.

No independent complete-candidate reviewer ran. Inherited website gate FAIL remains. B deferred, dispatcher PAUSE verified, no publishing or application changes.

### Continuation prompt

Continue WV-01 round14 from this execution checkpoint using `$abs-edit-organic`. Record my explicit $5.38 incremental batch-budget answer before motion calls. Prepare exercise A and both exact family motions, inspect them, and add their moving contexts to the existing round14 individual-approval page. Preserve the three prepared graphic previews and existing approvals. No full render until every remaining moving item is approved. Keep B deferred, dispatcher paused and publishing off.

Recommended model: **GPT-6 Sol, High effort**.
