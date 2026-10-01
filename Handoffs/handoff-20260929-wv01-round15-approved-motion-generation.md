# WV-01 round15: approved motion generation and individual clip review

Created 2026-09-29. Recommended model: **GPT-6 Sol, High effort**.

## Goal and current authorization

Generate exercise A and both family variations from their exact approved frame pairs, inspect the actual motion, and show only the new clips in speech context for individual approval. The three round14 moving graphics are now approved and remain locked. Work in a new isolated `round15/` directory. Preserve every prior reviewed output.

Dan's latest direct instruction:

> Everything is approved and you're good to generate the clips. You're authorized to go up to a $50 budget for video generation on this video. Don't ask me for permission until you hit that budget

This approves all three delivered round14 moving graphics and authorizes the requested clips. It replaces the earlier $20 cumulative cap and the pending $5.38 budget question. **Do not ask for budget or unchanged-frame permission again below the $50 cumulative video-generation cap.** Purposeful retries within that cap are authorized. Keep receipts and count failed attempts. No motion generation or rendering ran during preparation of this handoff.

Finished motion has not yet been generated or approved. Show it for its own approval, including a family A/B choice. No full render before those remaining motion approvals. B remains deferred, dispatcher paused, no publishing, upload, website replacement or application changes.

Project root: `/Users/danielrose/Documents/Claude/Projects/Abs By AI`.
Production root: `/Volumes/Extreme/_edit_work/wv01-edit`.
Approved graphics review: http://127.0.0.1:8766/round14/index.html.

## Read first

1. `Media/codex-video-trial/skills/abs-edit-organic/SKILL.md`, its applicable shared workflow, `.claude/skills/_shared/VIDEO-RULES.md`, `PRE-RENDER-APPROVAL.md`, `GRAPHICS-STANDARDS.md` and `CUT-CONTINUITY-QC.md`.
2. `round15-plan/WORK_PACKET.json`, `decisions.json`, `budget-authorization.json` and `cost-ledger.json` under the production root. These include Dan's latest exact words and supersede older budget holds and pending graphic template fields.
3. `round14/decisions.json`, `review/approval-registry.json`, `review/EDITOR-QA.md`, `review/junk-dispositions.json`, `review/protected-verification-final.json`, `review/cost-ledger.json` and `review/current-provider-pricing.json`.
4. `Handoffs/handoff-20260929-wv01-round14-motion-and-graphic-approvals.md` for original motion specifications; its old budget-hold checkpoint is superseded by this handoff.
5. `round13/review/placement.json`, `join-repairs.json`, `audio-repairs.json`, `timing-crosswalk.json`, `jump-audit.json`, `R04-final-disposition.json`; `round12/review/COMPONENTS.json`, `SOURCE-MAP.json`, `approved-fingerprints.json`, exact-file gate and complete-review records.

The existing review page and preparation receipts may still display pending fields. The latest direct-chat approvals in `round15-plan/decisions.json` are authoritative. Do not submit locked graphics for approval again.

## Locked moving graphics

All paths below are relative to the production root. Dan approved each exact delivered file through his latest Everything is approved instruction.

| ID | Exact approved moving context | SHA-256 |
|---|---|---|
| R05 | `round14/previews/R05-context.mp4` | `dbe9fc110088be8d7aeb74294991f2933bd063a63413306fc337857d93ea68c6` |
| R07 | `round14/previews/R07-context.mp4` | `5e37e99fb660ebebbf2d78aadf6dcbd545e673225eb0a8623fae659f20114647` |
| R09 | `round14/previews/R09-context.mp4` | `e25da15fb3e9e6ee41c2e68e96ca0da783fc8d562b83e271010356b9668398a7` |

R05 retains the exact food title and cyan labels, existing meal imagery and Soft Blue Light motion. R07 reveals all five approved points as spoken, using the approved alternating fixed wide/tight presenter seam pattern. R09 taps Greek Yogurt Berry Bowl and shows the approved recipe/image in the existing phone shell; its simulated UI provenance is retained. The earlier chicken demonstration stays unchanged.

Preserve all earlier opening, color C, audio/bass B, W2/T2 framing, V sit twist, exact3A, clip/photo/audio repairs and all 16 approved cut repairs. Do not rebuild them unless a concrete integration defect requires a separately scoped fix.

## Exact authorized frame pairs

Use the existing files in `round13/frames/`. No new still-generation call is needed.

| Motion | START SHA-256 | END SHA-256 |
|---|---|---|
| R03-A | `416931946bb4cbe28cbe26fec94dba28e360c082994c43def01d6f572281b9ac` | `eda7608cebf8da04de7f956c2864153fd9365d48284eb56190c93bbd429bfb07` |
| R12-A | `69a2633493dccd4dc88501f94a3d162f2512bddb14f936f28058dff1195da46c` | `b2a3ca25a9e5b64637df1912fea56a0f04cf931347780a8a1ed9dc166ea4a0d6` |
| R12-B | `6ee0c667a73acd1561a70b1d0addfc85e50cbee64b1c7757d48aaa3eda2bbcb2` | `cfe93c2b6de9cf626f242c02ebd9069c90956e153b6968070ae7304315ab133a` |

Each path is `round13/frames/<ID>-start.png` or `<ID>-end.png`. R03-B is unselected; no remake requested. R12-B is a family option, distinct from deferred full-film version B.

## Execution

1. Rehash the locked graphics, six endpoint files and protected inputs. Preserve current rounds, local server and shared two-build limit. Confirm dispatcher PAUSE remains present. Fresh provider pricing checks are read-only; no permission stop is needed within the authorized cap.
2. Adapt `round14/recipe/generate_motion.py` into `round15/recipe/`. Its prompts and exact-pair hash checks are prepared. Replace its obsolete `authorized_additional_usd` assertion with the actual `round15-plan/budget-authorization.json` cumulative-cap policy. Copy or read that authorization directly. Remove the obsolete one-attempt/no-retry permission restriction; retain resumable prediction IDs, safe submission handling and per-attempt receipts. Never duplicate an ambiguous submission or overwrite a paid result. A retry gets a new attempt ID and ledger entry.
3. Generate **R03-A, 6 seconds**: the real man watches his identical virtual self squat on the TV, then performs the same controlled squat beside it. Preserve identity, exercise, feet/mat contact, room and screen geometry. Actual screen action and real exercise motion must occur, with no static montage or held tail. Intended speech starts People who watched a virtual version of themselves exercising, baseline about218.05seconds.
4. Generate **R12-A and R12-B, 9 seconds each**. Exactly father, wife on one side and child on the other. A: wife folds towel, child adjusts dolphin pool toy. B: wife rolls towel on table, child adjusts goggles. All stay naturally alive before the father pulls his intact T-shirt over his head and clears both arms, then lowers the complete shirt. Wife and child look up with quiet admiration. Check complete fabric continuity, plausible arms/hands, face/body identity, small family movements and final seconds. No extra people, morphing shirt, body transformation, frozen family or tail. Compare both actual outputs and recommend the better one.
5. Adapt `round14/recipe/build_previews.py` into the isolated new round. It supports R03-A/R12-A/R12-B contexts and has no full-film entry point. Preserve exact mirror footage/join outside the pool replacement. Family placement starts baseline frame 21957, around732.632seconds; the legacy pool ends 22218. The approved R11 removal is 22196-22220. Apply it once, protecting there and That's what this did for me. Use natural trims, not stretching, freezing or slowing generated clips. Show each complete isolated 9-second option as well as its contextual trim.
6. Apply default cut/junk QC before delivery. Inspect every actual source/clip entrance, exit and composite internal join in native consecutive FFmpeg frames plus moving/audio context. Fix uncovered presenter jumps with distinct fixed compositions or approved complete cover. Protect full words, natural breaths, gestures, hair and purposeful teaching action. Detector/model flags require actual verification. Do not call sparse sheets a complete watch.
7. Prepare a **changes-only round15 page** with one lazy player, round12 baseline clocks, separate R03-A/R12-A/R12-B finished-motion controls and a family selection. List approved graphics as locked records. Preserve the launch agent `com.absbyai.wv01-review` on 8766 and old pages. Serve round15 alongside them from `/Users/danielrose/Library/Application Support/AbsByAI/WV01Review/round15/`. Use `shutil.copyfile`, since copy2's file-flag copying can fail on the SSD. Reuse `serve_package.py`, updating its round and byte-range test file.
8. Reuse `inspect_previews.py` with new contexts; skip AppleDouble files by matching `R*-build.json`, not all `*-build.json`. Sequential decoding or native FFmpeg extraction is mandatory: OpenCV random seeks on the concatenated master previously returned stale pixels. Record full decode, exact hashes, native join inventory/dispositions, moving motion/anatomy QC and browser playback. Update costs and approvals without inferring Dan's finished-motion verdict.
9. Deliver the three motion contexts and family recommendation, then park for individual approval. No complete or placeholder film. Only after these approvals may a later task assemble A and run fresh exact-file gates, full editor picture/audio QA, one independent complete-candidate review and Dan's verdict. Do not start that reviewer on these isolated options.

## Timing and preserved baseline

Immutable master: `round12/delivery/WV-01 round12 complete A 1080p.mp4`.
SHA-256: `ba00a9b1ecad1ca9cbb1d6e701efad08e90b8d8960d14c074b842d272dc42c03`.
Review SHA-256: `49dba4bb3d2da64e0e5568632a0e0abdfd5955f57bf03360cb5ceca84e37d44f`.
22,626 frames at 30000/1001 fps, 754.9542 seconds. Every approval clock refers to this baseline. Keep the old/new timing crosswalk.

R04 adds 7 original source frames. R10 removes 39 junk lead-in frames. R11 removes 24 pause frames. Net approved audio change minus 56 frames. Round12's prior 65 narration frames and 36 ending-room frames were already removed once; do not subtract them again. R04's conflicting model flash/word-tail findings were resolved with native sequences and direct source audio. Preserve that disposition and exact approved repair.

## Verification and known limits

Round14 verified 34 imported artifact records and 39 protected inputs. Its three context files decode fully: 480, 1731, 480 frames. All 13 actual joins were inspected in native five-frame strips. R07's 248 sequential samples were viewed at 7-frame intervals, about 0.234 seconds. Shared audio selftest passed; focused owner-assisted audiovisual QA passed all three graphics; browser playback, one lazy player, baseline clock, 8 served files and byte ranges were verified. Numeric hair measurement was unavailable because OpenCV's cascade asset is missing; actual dense framing evidence remains. This is isolated component QA, not a new complete-film review.

The source junk pass covered 15 pieces across C1697/C1698 with 43 unverified leads. The alleged Stanford reset overlapped intact speech and was unsupported by native frames, so it was retained. A model's contradictory suggestion to retain the R11 pause does not override Dan's approved removal. Details: `round14/review/junk-dispositions.json`.

Inherited complete-film website gate FAIL remains. Creative approval does not imply delivery PASS. Editor token counts and actual provider invoices are unavailable. No independent complete-candidate reviewer ran during round14.

## Budget ledger

**Cumulative cap now $50**, explicitly authorized by Dan for this video. Earlier $20 cap, $5.38 permission hold and no-paid-retry proposal are superseded. Do not reset the ledger on a new task or ask again before the cap. Announce estimates, record exposed actual costs or honest estimates and stop before spending beyond $50.

Known historical motion estimate: **$12.824017301463925**. Historical 56 built-in still calls have unavailable charges, not zero. Preserve that fact without repeating the budget stop Dan just removed. Last verified Kling v3 pro 1080p/no-audio price on 2026-09-29: **$0.224/second**, with evidence in `round14/review/current-provider-pricing.json`. Initial 6+9+9-second batch estimates **$5.376**, putting known motion estimates at **$18.200017301463925**, plus unknown historical still charges. Verify current price before the next calls. No generation occurred during this handoff preparation.

Round13 focused QC estimate **$0.209889**, round14 **$0.250684**, separate from generation. Gemini QC follows the existing separate standing authorization. Keep one cumulative generation ledger including failed attempts and retries; no production app generation endpoint, user credits or deviceId test calls.

## Ready-to-paste starter prompt

Execute `Handoffs/handoff-20260929-wv01-round15-approved-motion-generation.md` with `$abs-edit-organic`. All three round14 moving graphics are approved. Generate exercise A and both exact approved family frame pairs, inspect their motion, and show changes only for individual clip approval with a family recommendation. The cumulative WV-01 generation budget is now $50; do not ask for spending permission again below that cap. Preserve earlier approvals and apply default cut/junk QC. No full render before the remaining finished-motion approvals. Keep B deferred, dispatcher paused and publishing off.
