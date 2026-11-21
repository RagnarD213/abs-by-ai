# AD: Fired Them All R4 quality-control failure, 2026-10-09

The film needs two scoped repairs in R5. R4 is a rejected review candidate, not an approved final film. The investigation and editing-skill repair are complete here; the film changes are handed off separately. No new film was rendered, uploaded or published in this investigation.

## What happened at 4:38

The intended phone scene occupies R4 frames [8248,8338), 4:35.208 - 4:38.211. It maps to Version A frames [5631,5721), 3:07.888 - 3:10.891. Instead of the approved goal photo on a phone, both A and R4 contain a held studio close-up while narration continues.

The original approved component is valid: `/Volumes/Extreme/_edit_work/wv01-edit/round2/previews/P04-lock.mp4`, SHA256 `87ae103edb0830b9880325c7f658ce241008b6196954b28c6abca5bee2475500`, 90 frames, 960x540 at 30000/1001. It shows the correct AI goal image on a physical phone, with its approved AI disclosure.

The production cause was reproduced:

1. `round12/recipe/build.py` encoded asset parts without normalizing their canvas. Its phone part `round12/parts/032-5631-5721.mp4` remained 960x540, then was stream-copy concatenated into a nominal 1920x1080 film. The part validation checked frame counts, not dimensions.
2. FFmpeg extraction at absolute decoded PTS 187.8877 seconds shows the correct 960x540 phone picture in the round12 master.
3. Sequential OpenCV decoding of that same master from frame zero returns the previous 1920x1080 studio image at the phone interval while its reported timestamp advances. The independent full-interval reproduction confirms all 90 decoded arrays are byte-identical to camera frame 5630. It resumes live camera at frame 5721.
4. `round17/recipe/assemble.py` read that master through OpenCV into a fixed-size raw-frame encoder. Its patches did not overlap this scene, so the stale camera image became real frozen pixels in the new, uniform 1080p Version A. R4's native sequential assembly then accurately copied those already wrong pixels.

This is a mixed-resolution decoding failure in an older assembly, followed by preservation of the bad result. R4 itself is uniformly 1080p. It is not a VLC playback fault. Do not overwrite the historical rounds; restore the valid independent component in R5 after normalizing it to the film canvas.

## What happened around 14:07

The user timestamp identifies the final transition sequence. The approved pool clip returns to the A presenter at R4 frame 25316, 14:04.711. P6 enters at frame 25425, 14:08.348, and exits at frame 25495, 14:10.683. Its entry changes from A to C1700 while both pictures are wide; the hands reset visibly.

There is also a sentence-order error. Original A says: "I have never felt better in my life, so tap the button below." The R4 fresh transcription says: "I have never felt better, you've been doing this alone long enough in my life, so tap". The callback was moved to an advanced visual CTA boundary at A frame 22273, which occurs before the original sentence finishes. Original A ASR places "life" at 743.24 - 743.50 seconds and "so" at 743.66 - 743.78. The original source map identifies the completed-phrase join at A22287 (baseline22343), with the 14 original C1698 frames [11884,11898) between the advanced visual cover and that join. These are repair candidates; exact word-tail clearance still requires audio verification in R5.

The picture boundary and the audio insertion point were incorrectly treated as one decision. Fixing an earlier CTA flash left the callback inside a sentence and left a same-framing gesture jump. R5 must move P6 after the complete sentence, then solve the picture cover/crop separately. This conclusion comes from original/fresh transcripts and native picture comparisons; no claim of continuous human listening is made by this investigation.

## Why QC missed defects it could already see

The native watch scan actually flagged a 2.97-second frozen run at 275.24 seconds. It marked `inside_declared: true`, because the plan declared a card/graphic there. That tag was treated as an explanation even though the actual phone graphic was absent.

The prior reviewer explicitly wrote "no actual lockscreen card" and "source-context label differs from visible crop", but marked the scene expected. A contradiction was downgraded to metadata noise instead of becoming a missing-required-scene finding.

`round4/recipe/graphic_refs.py` extracted its graphic reference from the flattened A parent. The goal-lockscreen presence check then correlated the wrong studio pixels against the same wrong studio pixels and reported 0.996. It proved copying, not the presence of the intended phone asset.

For P6, the prior judgment explicitly wrote "Both sides wide but callback source change declared; hands reset low" and nevertheless marked it expected. Declared editing intent was allowed to excuse a visible continuity defect. Later byte-identical review-image reuse preserved that incorrect judgment.

The transcript/reference checks counted surviving words and largely compared the render to the already assembled audio. They did not require original clause order around each insertion. Thus a high overall fidelity score and an audio-reference PASS did not flag a sentence bisected by the callback. The exact fresh ASR already exposed it.

These were production and review errors. The existing detectors and available source material were sufficient to raise findings. An independent reviewer also made the wrong dispositions; independence alone is not proof of review quality.

## Repair applied to the editing skills

Shared `CUT-CONTINUITY-QC.md` now requires:

- Preflight every assembly part's canvas, format, rate, aspect and interpretation before concatenation or a fixed-size raw-frame pipe. Verify decoded contents at component boundaries. Use absolute timestamps on mixed-resolution inputs because filter reinitialization can reset a filter's frame counter.
- An expected-scene checklist tied to independently approved asset paths/hashes. Candidate-derived or suspect-parent references may establish preservation only.
- A disposition for every frozen-run candidate, including declared graphic spans. Clear only the actual approved static asset; keep a frozen talking presenter open.
- Moving original-versus-candidate context at both sides of every pickup, including the entire cutaway-to-callback-to-next-shot sequence.
- Complete original sentence/clause order around callbacks, checked against fresh transcription and actual audio. Choose audio insertions from words, not picture-cover boundaries.
- Reconciliation of contradictory observations and invalidation of previously cleared judgments when their evidence is contradicted.

The shared video rules and project website/ad/long-form skill entry points route to these obligations. The installed Codex `vsl-edit`, `abs-edit-ad` and `long-form-content-edit` adapters also carry the explicit instruction. Their project counterparts preserve the instruction in Git.

## Verification and limits

The independent reviewer applied the revised procedure to actual evidence: the R4 freeze/missing phone and P6 reset remain open; the real approved phone/goal-photo stills remain legitimate static controls. The sentence-order requirement was added after the reviewer identified the split phrase. See the independent postmortem/forward-test files in the private evidence directory.

Two rejected-file controls, with Dan's exact words and the R4 hash, are now in `_shared/qc_corpus/corpus.json`. Targeted strict corpus runs report FAIL/PENDING for automated frozen-run disposition, semantic scene content, presenter continuity and sentence order. Those automated rows are not implemented in the corpus runner. This repair changes the required review procedure; it does not change gate thresholds or pretend new automatic detectors have shipped. Existing native scan and actual review evidence must be used. No global gate code was changed.

Shared QC updates were committed and pushed immediately. The first deployment of these instructions completed successfully on all three Railway services. Subsequent documentation commits follow the same verification. Public repository changes contain prose, paths and hashes, not private video or pictures.

## Evidence and next action

Private evidence: `/Volumes/Extreme/_edit_work/wv01-edit/version-b/round4/review/postmortem-20261009/`. This contains native R4/A comparisons, the original P04 phone image, PTS extraction/log, sequential OpenCV reproduction and independent temporal review. The reproduction includes `independent-round12-cv2-full-freeze.json` and `independent-round12-pts187.8877.log`.

Existing failed judgments: `round4/review/delivery-watch/watch_pass.json`, strips/pairs 61/62 and 183, and `round4/recipe/graphic_refs.py`. Speech evidence: `round17/review/delivered-asr.json` and `round4/review/delivered-asr.json`, segment 246.

Next: execute `Handoffs/handoff-20261009-wv01-b-round5-final-two-fixes.md` as **Fired Them All AD R5**, GPT-6 Astra, high effort. Preserve all unchanged approvals and saved budgets. Deliver the repaired full film for VLC review; do not upload, install or publish it.
