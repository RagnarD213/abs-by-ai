# Default jump-cut and junk-footage QC

Dan requested this default for every video edit and revision on 2026-09-29, after reviewing WV-01 round13. Apply it during source selection, before approval previews, and again to the exact final candidate. Do not wait for Dan to identify a bad cut or noise. This procedure supplements the shared delivery gates and complete picture/audio review; it does not change their thresholds or grant motion, full-render or publishing permission.

## 1. Remove confirmed junk while selecting the speech

Run the existing [junk-footage pass](cut/README.md) against the selected source ranges before the first edit preview. Reuse measured lav selection, available word maps and script; listen to the actual source in context. Inspect the opening, closing, and the lead-in and tail of every selected take, including cuts concealed by clips or graphics.

Look for lip smacks, mouth clicks, throat clearing, false starts, handling noise, unscripted setup speech, abandoned words, repeated failed takes, empty lead-ins, unnecessary pauses and looking away from the camera while waiting or resetting. A script or word map helps locate intended speech but does not decide whether the sound is junk: a lip smack can be transcribed as “I,” and genuine quiet words can be absent from ASR.

For each candidate, record source/output time, heard words, visible behavior and disposition. Compare the actual lav audio, waveform and adjacent picture. Remove only confirmed junk. Keep normal breaths, purposeful emphasis, natural sentence spacing, complete exercise repetitions, necessary teaching pauses and looking toward equipment during a demonstration. Do not impose one pause length on every format or classify every glance away as junk.

Set removal boundaries outside the complete words on both sides, including quiet onsets and final syllables. Restore missing word tails from the original source, keeping the approved source-specific voice treatment and level. Do not synthesize missing speech, stretch a clipped syllable, change a finished editor's mix or add transition noises. Keep any room-tail fade in non-speech audio. Listen to the repaired phrase and its neighboring words in context.

Every pause/noise removal creates a picture decision. Inspect and repair that join under the next section before presenting the preview.

## 2. Inspect every actual picture join

Build a join inventory from source/output cut maps and component boundaries. Include source discontinuities inside reused composites, graphic-covered presenter footage, picture/audio cut offsets, clip entrances/exits, the opening and ending, and the start/end of each newly patched region. Inspect every join, even when an automatic detector did not flag it. Inspect the presenter beneath a graphic that is being replaced or repositioned, since that revision can expose a previously hidden jump.

Use the existing [watch pass](deliver/watch.py) for a continuous native-rate scan and exact boundary strips/pairs. Its scan candidates supplement the join inventory. A same-framing presenter splice can escape a whole-frame difference threshold because only the face or hands jump. A sparse contact sheet, low difference score or pose-matching score does not clear a cut.

For each join, inspect native consecutive frames, at least the outgoing/incoming pair and nearby frames, then a short moving speech context. Confirm the exact file hash, frame rate and frame index. Extract through FFmpeg with sufficient decode lead-in, or decode sequentially. WV-01 exposed a failure where OpenCV random seeking on a concatenated master reported the requested timestamp but returned stale pixels. Do not accept a seek timestamp alone as proof; use verified native extraction or a standalone decoded excerpt.

A defect is an abrupt presenter position, pose, head, hand or gesture change across a cut in substantially the same visible composition. A lower third, phone screen or side card does not cover the presenter and cannot hide that jump. A one-frame return, a few-frame intermediate crop or an uncovered gap before/after a cutaway is also a repair item.

## 3. Fix the cut, then inspect the repair

Use a deliberate cut between clearly distinct fixed wide/tight compositions, or an appropriate approved clip covering the entire discontinuity. Align the composition step or cover to the actual picture splice, including any picture/audio offset. Do not leave a brief island of the old framing, a single-frame flash or a naked tail when the cover ends. Pose-matching can help choose the frame; it does not make a same-framing jump acceptable by itself. An audio crossfade, dissolve, wipe or sound effect is not a substitute for the framing change or clip cover.

Keep horizontal presenter framing fixed within each shot. Do not add tracking, drift, animated zoom or pan to disguise a cut. Preserve approved color, voice treatment, graphic pixels, hair, hands and teaching action. If a chosen tighter crop loses required content, use a safe distinct composition or approved cover instead. New or revised cover assets and graphics still require their normal approval stages.

Recheck the repaired moving context, both sides of the splice, and every boundary introduced by the patch. Verify complete surrounding words, stable voice level, correct picture/audio alignment and no new pose jump or flash. Work on isolated components before the full-render approval boundary. Present each changed join/noise/pause repair separately when Dan requests individual revision approval.

## 4. Evidence and final disposition

Keep one compact report naming the exact media hash and each join/candidate: ID, source/output frame or time, finding, native proof, repair or reason retained, contextual preview and approval scope/status. Record the number of inventoried joins versus inspected joins; uncovered omissions and unresolved candidates remain open. An automated flag is a lead, not a confirmed defect or automatic delete instruction. Conflicting model findings require checking the native picture and original sound; retain the conflicting result and record the evidence behind the disposition.

After all required approvals permit full assembly, repeat the checks on the exact complete candidate and perform the existing complete editor picture/audio review and independent review. A native boundary audit or sparse sheet inspection must not be described as a full human playback watch. Do not mark the candidate ready with unresolved uncovered jumps or confirmed junk, or infer Dan approval from a detector/model pass.

For a format-only adaptation of an approved master, inspect inherited cuts as well as new ones. Preserve the approved master and its mix; report inherited defects and scope the repair with Dan rather than silently rewriting the approved original. Filing or publishing an already approved file alone is not a new editing job.

## Reference case

WV-01 round13: 51 source splices, 141 visible boundaries and 16 separately approved cut repairs. The noise at the next take's start was distinguished from the genuine “I know.” A pause removal retained “there” and “That is what this did for me.” Complete source audio and native frame sequences resolved contradictory model findings around “instantly.” Recipes/evidence: `/Volumes/Extreme/_edit_work/wv01-edit/round13/recipe/` and `round13/review/jump-audit.json`, `audio-repairs.json`, `R04-final-disposition.json`. Those crops, frame counts and prices belong to that recording, not future videos.
