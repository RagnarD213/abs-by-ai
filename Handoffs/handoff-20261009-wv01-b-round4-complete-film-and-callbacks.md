# Fired Them All AD R4: complete Version B and callbacks

Date: 2026-10-09, America/Chicago. Recommended model: GPT-6 Astra, high effort.

## Goal and approval

Build the complete website VSL Version B from the approved R3 opening, the approved Version A shared body, and six filmed C1700 callback lines. Deliver a complete reviewable film with exact-file QC, subtitles, edit sheet and working browser/VLC review copies. This is a website video despite the task's AD label.

Dan approved R3 in the local task **Fired Them All AD R3** (thread `01a11df7-7545-7235-a9e8-b71b552230ca`): “All right everything is looking good. This is finalized and approved. Give me a handoff document for the next step”. This locks the completed opening and its demonstrated A transition, including the firing and phone motion. Do not reopen these creative decisions or request the same approval again. The complete B film and callbacks have not yet been assembled or reviewed. Uploading, website installation and publication are subsequent actions requiring their own authorization.

Project: `/Users/danielrose/Documents/Claude/Projects/Abs By AI`. Read `AGENTS.md`, current `AI_COORDINATION.md`, `.claude/skills/_shared/VIDEO-RULES.md` in full, and the `vsl-edit` skill before editing. Preserve concurrent board, social and other video work; register only your own R4 entry. The global cap is two video build/QC/transcription jobs.

## Exact locked inputs and join

Private R3 root: `/Volumes/Extreme/_edit_work/wv01-edit/version-b/round3` (abbreviated R3 below).

Approved file: `R3/previews/Fired Them All AD R3 - opening and join 1080p.mp4`.

- SHA256: `81110e1409266f1e6a07f2f30aa6ee8147315d2a65e504d61fab892e6448c8f3`.
- 308802762 bytes, 7943 frames at 30000/1001 fps, 265.0314333333333 seconds, 1920x1080 H264 BT709, AAC 48 kHz stereo.
- **Use R3 frames `[0,7640)` as the B opening (254.921333 seconds), then A frames `[5111,22570)` exactly once.** R3's final 303 frames already contain A `[5111,5414)` as review context. Never concatenate the entire 265-second preview followed by A starting at 5111; that duplicates 10.11 seconds. `R3/review/join-map.json` is authoritative.
- Base before callback additions and recap removal: 25099 frames, 837.4699666666667 seconds (13:57.47). Calculate final runtime from the exact selected EDL. Do not impose an arbitrary duration or speed up speech.

Approved A: `/Volumes/Extreme/_edit_work/wv01-edit/round17/final/WV-01 FINAL Website VSL A 1080p.mp4`.

- SHA256: `acddfb5b3bad7bb6d85f937b74054fafb4be33505f49ae91cd765a8ecac88836`.
- 22570 frames, 753.085667 seconds; SRT, VTT and FINALIZATION.json beside it.
- Preserve the original file byte for byte. Reuse its approved shared body, offer, seven-day trial, $19.99/month, cancel-anytime wording and exact final CTA/end. No new AbsByAI.com mark or wholesale graphics rebuild.

Accepted opening/join audio reference: `/Volumes/Extreme/_edit_work/wv01-edit/version-b/round1/previews/DRAFT - Fired Them All B opening and join 1080p.mp4`, SHA256 `6e60be3d333a603b45bf3a2214d5cc6d341bf44b3a9c59ef170157da376e7bba`.

Locked grade: `/Volumes/Extreme/_edit_work/wv01-edit/round2/recipe/grade-C.cube`, applied after 1080 BT709 scaling. Source is S-Cinetone/Rec709, not S-Log. Presenter static wide geometry is `3552:1998:144:162`; tight is `2856:1606:492:170`. New pickup geometry must be checked against actual hair, arms and matching pose.

R3 recipes: `recipe/build_r3.py`, `integrate_r3.py`, `generate_motion.py`, `prepare_r3.py`. Retain current assets and custom graphics, not historical template substitutes. Firing frames `[0,147)`, phone `[147,292)`, presenter return `[292,300)`, verified body `[300,7943)`. Firing stamps at 33/71/108; completed-pose 1 REP chip at 262. Trainer closed eyes and the upward-only curl were disclosed before this approval and are accepted. Preserve the studio-blue early photo trio, mixed-case “What you'll learn today” title, custom hour graphics, laptop `[5740,5897)` and monitor `[6095,6276)` natural planning clips.

## Six callbacks to select and insert

Raw source: `/Volumes/Extreme/dan rose fitness 9:23 shoot - vsls, long form content, short form content/C1700.MP4`, 119.620 seconds, 3840x2160 at 30000/1001, one dual-mono audio stream. Existing index is sufficient; do not blindly retranscribe everything.

Project references:

- `Media/footage-index/dan-rose-fitness-9-23-shoot-vsls-long-form-content-short-form-content/C1700.roll.md`, `.roll.json`, `.roll/words.json`.
- `Media/wv01-planning-20260924/C1700-planning-transcript.txt` and `source-cues/source-teleprompter.json`.
- `Handoffs/video-editing/WV-01-SOURCE-MAP-20260924.md` and `WV-01-EDIT-PLAN-20260924.md`.
- Original B scope: `Handoffs/handoff-20261007-wv01-version-b-intro-first-cut.md`; prior rounds: `handoff-20261008-wv01-b-round2-opening-revisions.md` and `handoff-20261008-wv01-b-round3-selected-motion-and-opening.md`. Their old budget and pending approval statements are superseded here.

Navigation ranges below are seconds in C1700, not final edit boundaries. Listen to the actual source and adjacent phrases, compare alternate takes, choose the clean complete take and natural breaths. Remove numbered slates, false starts, repeats and aborted takes. Machine transcript hears “twenty-second” as “22nd”; do not invent replacement narration.

| Pickup | Spoken line | Source navigation | Shared-body placement |
|---|---|---|---|
| P1 | This is the twenty-second one I told you about. | 19.84-22.04 or 23.08-25.54 | Production cues say after “Number one. AI got me back in the gym”; source-map says after goal-image explanation. Resolve this discrepancy from meaning, latest cues and surrounding recorded audio before locking the EDL. Preserve the approved B opening. |
| P2 | And think about that. No nutritionist on earth can sit next to you at every single meal. This does. | About 28-35.26 or 38-44.70 | After the existing food-photo/calorie section. |
| P3 | That's what replaced my meal-prep service. And honestly, the food got better. | 50.98-55.02 or 58.78-62.84 | After the meal-prep food-improvement point. |
| P4 | So that's the other hundred and sixty-five hours, covered. | 71.44-74.60 or 76.16-78.96; 67-69.68 is partial | Replace the first recap sentence starting “So if you don't think AI can get you in shape...” rather than adding a second recap. |
| P5 | That's your trainer, your nutritionist and your meal planner, all three, for less than one hour with a human trainer. | About 87-95.48 or 96.90-103.60; 84.56 is a false start | After the $19.99 monthly-price statement. |
| P6 | You've been doing this alone long enough. | 108.92-110.84; exclude aborted 116.48-117.86 | Before the final invitation. |

Useful prior assets: `/Volumes/Extreme/_edit_work/wv01-edit/selection/auditions/C1700-RAW-AUDITION.mp4` with source JSON, and `/Volumes/Extreme/_edit_work/wv01-edit/review/focused-findings/B-callback-{1..6}.wav`. These are references, not approved edit boundaries. There is no finished callback EDL yet. Grade-C representative proof already exists at `/Volumes/Extreme/_edit_work/wv01-edit/round3/review/C1700-locked-C.jpg`, contact sheet `rolls-locked-C-contact.jpg`, and that round's `QA.md`.

Prepare a six-row take/placement map and short context previews covering each new splice. Use genuinely distinct static wide/tight cuts or approved full-cover to hide mismatched joins, with clean source audio. Follow the VSL workflow for any materially new visuals needing approval before full rendering; don't ask to reapprove locked opening assets. Fit only the new pickup audio to the accepted shared chain. Cut/splice approved A and B audio without a global remix, new voice, music or SFX. Encode picture consistently before AAC mux; mixed encoder-parameter concat-copy previously caused random-seek playback defects.

## Verification already completed and remaining technical work

R3 exact-file audio gate PASS: -14.20 LUFS, -1.60 dBTP, no silent seconds, 0 ms lip sync at five checks. Compressed AAC packet hashes and timings match the accepted R1 reference. Actual integrated title/G05/G10 clearance PASS. Hair, headroom, no-wide-level and push-coverage framing checks PASS. Edit sheet validates: 44 segments, 811 words, 8 graphics, 9 pictures; 78 SRT cues in runtime. Native 7943-frame decode and 304 independent random seeks passed. Shared watch reviewed all 65 boundaries and 141 emitted actual images with zero open defects. The 7870 detector event is actual phone-screen progress animation, not an exposed presenter splice.

Evidence under `R3/review/`: `integrated-checks.json`, `integrated-clearance-checks.json`, `integrated-sheet-validation.json`, `r3-integrated-independent-audit.json`, `integrated-watch/watch_pass.json`, `integrated-cut-metadata-recheck.json`, `integrated-watch-row-recheck.json`, plus receipt, logs and both initial/corrected gate plans. Read the precise scope of each report. No continuous human watch/listen or full source-pixel comparison of the entire integrated file was claimed by the agent.

**Creative approval does not change the machine delivery stamp.** R3's original all-row website gate remains FAIL: 28 PASS, 5 FAIL, 6 NOT MEASURED. Corrected camera metadata merges only identical crop/side with contiguous source frames; targeted min_segment and jump_cut now PASS. Targeted watch PASS likewise does not replace the all-row result.

Before final B delivery, resolve strict splice_visibility findings and supply banned-screen reference, rendered label-chip evidence, negative-event report and fresh exact finished-transcript evidence. The existing shared gate `deliver/gate.py run()` obtains format config before loading the plan and does not pass `plan.caption_mode`; it ignores explicit website `caption_mode: srt` and applies burned-caption checks. Inspect current code first, because another session may have fixed it. Any necessary gate wiring repair must follow shared regression corpus tests and GATE_VERSION policy. Never relax thresholds or bypass missing evidence. R3's approval corpus entry preserves measured passes and remaining FAIL honestly. No gate code was changed in R3 closeout.

Create fresh exact-file full-B audio/delivery gates, native-frame cut/watch findings, lipsync/clearance checks, seeking checks and human review evidence appropriate to actual scope. Record unresolved failures honestly. Keep SRT/VTT and a provenance-bound edit sheet current as callbacks shift the timeline. Opening approval alone is not full-B delivery approval.

## Generation budget and closeout

Standing Replicate authorization saved in canonical `.claude/skills/_shared/VIDEO-RULES.md`, commit `e3cb1f370313dfc02f1a5e7a251e007a4b228ba7`: **$50 total per website video, $5 per organic YouTube/Instagram content video, $10 per unlisted advertised ad**. Necessary images, endpoints, motion and paid retries count across all rounds of a video. Existing keys and necessary input images are authorized within the remaining category budget; do not request that same permission again or reset the cap in R4. New materially different creative endpoints still follow the asset approval workflow.

R3 needed only the locked firing/phone motion from Replicate `kwaivgi/kling-v2.5-turbo-pro`. Sources: `R3/motion/firing-source.mp4` (SHA256 `1a50868a7527f228768407f90426c739616c3ec26bf7d8f29ee4b1e1c70b3626`) and `phone-source.mp4` (`645c912d1f7b196bd47c4171fdde050d661a0098529547f4337bf5103e5e1d77`). Successful pair estimate $0.70; discontinued Kling2.1 failures conservatively reserve $0.90. Actual charges unknown; all four attempts and prediction receipts remain in `R3/review/generation-ledger.json`. No new generation is currently needed.

R3 creative approval is recorded in `R3/review/R3-final-approval-20261009.json`, the exact edit sheet and execution status. Private masters, sources, recipes and QC remain intact. Temporary same-video `Videos to Review` copies and the finalized port 8873 review service are removed during closeout; do not rely on that old URL. Stage R4 via the maintained review-server helper, verify actual playback and range seeking, and provide full-quality review files 45 seconds or longer in `Videos to Review`. Remove only this video's copies after its next finalization.

Do not rerun old status writers from the Codex workspace (`finish_integrated_review.py`, `update_complete_status.py`, `finish_r3_records.py`, `update_r3_status.py`); they restore obsolete pending states. Work in a new private `version-b/round4` recipe/review tree. Commit only your task's named project files with `scripts/git/safe-push.sh`, shared files immediately after editing, then verify the required automatic deployment/live site. Do not touch other sessions' implementation.

## Starter prompt

Continue Fired Them All AD as R4 using this handoff. Preserve the finalized R3 opening, assemble the complete Version B shared body, select and insert the six C1700 callbacks with natural picture/audio joins, resolve the documented delivery-check gaps, and deliver the complete film for review. Follow current VSL standards and saved Replicate budgets. Do not upload or publish.
