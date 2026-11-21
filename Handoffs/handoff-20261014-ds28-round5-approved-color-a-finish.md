# CONTENT: Meal Prep SFC R5

Rename the next chat **Meal Prep SFC R5**. DS-28 is a dedicated organic Short. Recommended model: **GPT-6 Sol, high effort**. This is a controlled color-only rebuild of an approved edit, followed by visual review.

## Goal and settled approvals

Apply **Color A, Clean and balanced**, to every original-camera scene in the complete 59.5595-second Short. Dan selected it on 2026-10-14: "Let's go with the clean and balanced". Before that he said: "Everything else is approved" and requested color selection first, then the full re-edit in the following round. R5 is that full re-edit. Do not offer more color choices or reopen other approvals.

Authoritative color approval: `Docs/DS28_APPROVED_COLOR_A_20261014.json`. It holds the exact filter, approved preview path/hash and preserved elements. Read `Docs/DS28_R4_COLOR_OPTIONS_20261013.md` and `Docs/DS28_R3_FINISH_REVIEW_20261013.md` for completed work and verification. Earlier motion handoff: `Handoffs/handoff-20261012-ds28-round3-approved-motion.md`.

Approved comparison: `/Volumes/Extreme/_edit_work/ds28/round4-color/review/A.mp4`, SHA256 `561f5744d7b305e782b805e8fa6628144eafa9b62ff607c5a103bf4665ce223c`. Its three excerpts show wide, tight and the closing take. All four comparison files have identical audio, frames and timing.

Preserve the complete R3 edit: Pair B tracking/crops, both approved AI scenes and placements, seven graphics, captions, speech timing, audio, normal speed, closing pickup and all cuts. No covers, extra formats, uploads or publishing. Do not start a thumbnail/setup workflow. No still or motion generation is needed.

## Files and working state

- R3 complete master: `/Volumes/Extreme/_edit_work/ds28/round3/review/Meal Prep SFC R3 - complete Short.mp4`, SHA256 `9d69fd1c7b58dd75104df872f5a573684e42b47c3e8b50f11d65b8e89e8c2060`.
- R3 work: `/Volumes/Extreme/_edit_work/ds28/round3/`. Recipes: `recipe/picture.py`, `graphics_runtime.py`, `finish.py`, `patch_graphic_edges.py`, `contexts.py`. Data: `shots.json`, `framing-report.json`, `source-measurements.json`, `captions.ass`, `gate-plan.json`, `aac-reuse-proof.json`, `caption-alignment-evidence.json` and `finished-asr.json`.
- R4 color work: `/Volumes/Extreme/_edit_work/ds28/round4-color/`. `recipe/build.py` demonstrates applying the exact grade to original camera picture before approved graphics/captions. `options.json`, `selected-color.json`, `approval.json`, `excerpt-map.json` and `review/manifest.json` record recipes and evidence. `recipe/verify.py` checks media/audio integrity. Current review page is this round's page.
- Raw: `/Volumes/Extreme/dan rose fitness 9:23 shoot - vsls, long form content, short form content/C1720.MP4`. Stored 3840x2160 with rotation90; decodes 2160x3840. Sony FX30 S-Cinetone / Rec.709. No log conversion, LUT or extra transpose.
- Keep source9.1-62.15, then79.35-85.85. Final target: **1785 frames, 30000/1001 fps, 1080x1920, Rec.709**, duration59.5595s. Reuse exact `shots.json` source/cut mapping and tracking instead of hand-entering approximate cut times.
- Build in a new `/Volumes/Extreme/_edit_work/ds28/round5/`. Preserve rounds1-4 and their approvals. R3 `work-packet.json` lists the superseded presenter grade B; the explicit R5 request and selected-color record override only that grade.

## Execute

1. Read current project instructions, full shared `.claude/skills/_shared/VIDEO-RULES.md`, the Codex `long-form-content-edit` skill, current pre-render/cut-continuity/framing rules, and live board. Claim only DS-28. Keep the dispatcher paused. Follow the current limit on simultaneous heavy builds; do not introduce another scheduler.
2. Verify both hashes above and load the exact Color A filter from the approved JSON. Rebuild all 17 original-camera segments from raw, including the closing take. Copy/adapt the existing recipe into round5; preserve its measured tracking, source map and frame count. Do not reuse camera segment caches containing the rejected grade. Reuse the unchanged R3 AI parts, not regenerated motion. Do not apply a correction to the flattened full master, which would recolor approved graphics, captions and AI footage.
3. Composite the same approved graphics after grading through the existing maintained shared modules. Preserve G03/G06 HyperFrames0.8.97 and the accepted illustrated ribbon design. Use frame-rounded graphic intervals. R3 repaired four one-frame graphic tails at frames457,558,843,1349; preserve those repairs. Do not restore float-boundary tails or copy superseded templates. Burn the final R3 `captions.ass` with unchanged text and film timings, and retain its SRT sidecar.
4. **Stream-copy the approved R3 master's AAC audio** into the new export. Do not rerun the voice chain, refit tone, change bass, remove pauses or alter captions to pursue a legacy metric. Prove identical extracted AAC SHA256: `72dc18a349f860e85b90a28dac6c33fa446f37b61b2667b9672907178c1de52c`. R3 ASR may be reused only with this proof and an explicit binding to the new master hash; do not claim a fresh transcription if none ran.
5. Inspect full-color consistency across all wide/tight camera holds and the pickup, comparing the delivered pixels to the approved A preview at its mapped film frames. Inspect camera/AI transitions, skin, blacks, blue fixtures, highlight texture and approved graphics. Preserve motion split0:00-0:04.97, camera return0:04.97, and full-screen reuse0:18.62-0:22.49. Keep the closing pickup0:53.05 and subsequent deliberate framing change0:56.22. The media must still show actual approved AI movement, with labels intact.
6. Run current exact-file checks on the actual new master, full native chronological/boundary inspection and supported full audio review. Use one editor self-QA plus one fresh independent complete-candidate reviewer with one consolidated verdict. Scope the review to the color revision and unintended regressions; do not reopen approved creative choices or start recurring review loops. Preserve truthful exact-file evidence and distinguish detector failures from confirmed defects.
7. Deliver complete R5 master, phone copy, SRT, unchanged audio comparison, reproduction recipe, manifest and honest check status. Copy the full-quality 45s+ review to `Videos to Review/Meal Prep SFC R5 - complete Short.mp4` and open the folder. Provide exact new-film revision/watch ranges in chat. Color affects camera footage throughout; useful ranges:0:04.97-0:10.64,0:28.13-0:33.67,0:53.05-0:59.56. Link short contextual clips if available, plus the full film.

## Measurements and approvals are separate

R3 independent review inspected41images and19joins, finding no confirmed visual defect. Dan subsequently approved everything except color and has now approved Color A. The historical exact-file delivery result remains32PASS/7FAIL/0NOTMEASURED/3N/A; audio fails tone only. These are measurements, not reasons to change approved creative elements.

The seven R3 failed rows: audio stamp (mean tone error1.245dB versus1.2, maximum3.073 versus2.5); off-camera coverage26% versus30%; headroom, minimum head size and push coverage for the approved Pair B wide/tight views; a deliberate continuous-take wide/tight change at56.22 just above the numerical splice ceiling; and legacy waveform caption timing. Actual ASR matched187/188words, with the quick spoken your separately confirmed. Caption repairs and AAC identity are documented. Current VIDEO-RULES explicitly records fixed approved bass/tone as a known tone-gate mismatch; retain the approved sound. Do not crop away the approved fixtures or add more B-roll for the legacy coverage gate. Never change thresholds or manufacture PASS stamps. Record new gate results and inspect actual regressions without reopening approvals.

## Review page and records

Keep **http://127.0.0.1:8891/**. The managed service currently owns `round4-color/review`; when round5 is ready, replace only this same task's service root through `.claude/skills/_shared/review_server.py`. Keep original files. Run the managed command after page changes to refresh its local cache; verify linked files200, MP4 range206, actual browser playback and seeking. Show the completed R5 film first, with selected Color A and no unanswered asset choices. Keep the review usable on mobile and desktop.

Read the board again before finishing and edit only the DS-28 entry; run `scripts/board-check.sh`. Commit/push named task documents using `scripts/git/safe-push.sh`. Queue/MASTER files had unrelated live RA-13/RO-17 edits when Color A was recorded, so selection was saved in the dedicated approval JSON and board without modifying those files. At R5 start, inspect the current queue again and update only DS-28 when safely possible; never include another owner's pending edits in a commit. Dispatcher remains paused. No Victory Dashboard work.

Existing motion spend is$1.40 of the cumulative$5 allowance; no motion spend is planned. Gemini review estimates total$0.800848 through R3; R4 cost$0. State a new review estimate before any paid calls and keep a usage ledger; provider invoices and editor token totals were unavailable. No new task or automation has been created by this handoff.

## Ready-to-paste starter prompt

CONTENT: Rename this chat Meal Prep SFC R5. Read Handoffs/handoff-20261014-ds28-round5-approved-color-a-finish.md and execute it. Color A, Clean and balanced, is approved. Apply its exact filter to all original-camera footage in the complete Short before graphics and captions. Everything else is approved: preserve Pair B, AI motion and placements, all seven graphics, cuts, captions and the approved AAC audio. Finish the complete 59.56-second R5 Short, inspect it and obtain one independent complete-candidate review, then give me the full film and exact watch ranges. No covers, extra formats or uploads.
