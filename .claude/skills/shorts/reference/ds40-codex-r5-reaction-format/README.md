# Bill Maher Fat 90-Year-Old: Codex R5 reaction standard

**Locked by Dan on October 25, 2026 after comparing the complete Codex and Claude edits.**
CONTENT SFC reference. Since 2026-10-27 no AI owns green-screen editing (Dan: "let's not have any rule for which one"); his lean is Codex for reaction Shorts, Claude for long-form. This replaces the earlier Hormozi Fat Guy Claude R2 format reference. Dan already has the setup handoff; this lock starts no production or upload.

The authority is the exact approved [R5 master](/Volumes/Extreme/_edit_work/DS-40-codex/round5/review/media/bill-maher-fat-90-year-old-r5.mp4), SHA-256 `3808e604f218ad7281865ea74b3cbcf1a740a1bc595d060f1bcb34b8a3f4f720`: 1080x1920, 1944 frames at 30000/1001, 64.8648 s. Film approved October 23; promoted to the house reaction format October 25. `approval.json` records Dan's exact words and scope; `snapshot-manifest.json` hashes the unchanged working recipe and evidence.

## Reuse the sequence Dan chose

| R5 film range | Picture and sound |
|---|---|
| 0:00–0:04.004 (frames 0–119) | Clip full screen with a fixed portrait crop on the speaker. Dan's real synced reaction is lower left at 0.40 scale, flush left/bottom, full camera height with laptop visible. Clip audio only. |
| 0:04.004–0:19.6196 (frames 120–587) | The same speaking clip continues in a full-width horizontal panel. Dan is already large in the foreground, still watching. Title/source label plays ABOVE the panel. Clip audio continues without restarting. |
| 0:19.6196–0:30.2302 (frames 588–905) | Dan begins his response; the interview continues moving SILENTLY behind his head in the same panel, with real keyed hair overlapping the bottom. Keep this clean, single handover without a double-head dissolve or a frozen/restarted clip. |
| From 0:30.2302 (frame 906) | Dan's response on the moving Soft Blue Light field, deliberate fixed wide/tight cuts, relevant motion graphics/cutaways, then his ending. |

The 4.004 s opening and ~30.23 s panel exit are the reference rhythm, not compulsory timecodes on every new source. Match clip length, word boundaries and the first response; preserve this three-stage sequence. Do not substitute the old format that stays portrait for the whole quote and only then shrinks/grows for half a second. R5's changes at 4.004 and 19.6196 s are clean picture cuts, not an invented animated move. Both scripted and off-the-cuff versions, when filmed, use this shared format and are compared as required by VIDEO-RULES.

## Geometry, title, key and colour

- Panel on the 1080x1920 canvas: x=0, y=92, width=1080, height=608; preserve the complete 16:9 picture height (rounding to pixels), no decorative crop that chops it shorter. Title/source label is above it at x=36, y=24, 32 px, using the moving Soft Blue Light HyperFrames media-card family. Replace Bill's name/show with the new speaker/source. Clear the title, faces and captions against the actual footage.
- Dan is composited last, in front of the panel and graphics. The reference measures his hair in EVERY key frame; one fixed placement per take gives at least 28 px overlap even at the lowest posture. The watching layer is scale 1.0; the response is 1.25 with measured horizontal centre. These numbers are source-specific examples: fit the same visible proportions, intact gestures, laptop and safe hair to each new take, rather than copying coordinates blindly.
- The early corner is scale 0.40, x=0, y=1152 on a full 1080x1920 key. Right-edge fade is narrow and expands only for the hand exiting the camera edge. `snapshot/render.py` and `snapshot/layer.py` contain the exact composition, cleanup and light-wrap treatment.
- R5 uses the optimized house Claude R2 key algorithm. `snapshot/recipe/` preserves the actual calibrated R5 copy; shared `chroma-key/README.md` remains the algorithm reference. Calibrate on difficult excerpts per new source; key only used pieces plus handles once, reuse matching stamps, reset temporal neighbours at cuts. Retain strands, watch/glasses opacity and motion blur; measure and inspect pink/light/dark composites. Never run an archived recipe in this reference directory or another editor's work folder.
- **Colour reference is Codex R5 on BOTH Dan and the clip.** Dan uses `snapshot/recipe/grade.py`, `warm`: RGB gains [1.01, 1, 1.015], saturation 1.04, power .97, exposure 1.035, contrast 1.045 about .18. Apply once to reconstructed foreground. Bill's clip retains the source treatment with explicit BT709 TV-range-to-RGB decoding and correct TV-range output, as in `snapshot/render.py`; do not apply Dan's warm transform to the TV clip. On a different set or source, match the approved visible look by calibration, not copied values or a fresh style audition.
- Audio is NOT a newly universal voice preset: Bill Maher's selected Balanced voice remains locked for this film. R5 copied R4 AAC byte-for-byte (`snapshot/audio-copy-identity.json`). New footage keeps the shared source-specific voice procedure and approvals.

## Recipe map and limits

`snapshot/render.py` assembles the full film; `layer.py` keys/composites/grades the foreground; `graphics.py` and `hf/configs/G05.json` build the titled panel; `field.py` builds the moving field. `repair_bmi.py` documents the final internal table repair, so an earlier assembly is not mistaken for the approved master. Plan, approvals, key/QA scripts and the raw final gate/dispositions are preserved beside them. Earlier R4 captions, audio, table and graphics are dependencies in `/Volumes/Extreme/_edit_work/DS-40-codex/round4/`, with a recipe archive in `Handoffs/video-editing/ds40-codex-r4/`.

These are provenance snapshots, not a standalone generic launcher. Copy into the new job and adapt its paths, source ranges, captions, geometry and calibration. The `stills/` files illustrate the approved opening/handover geometry; judge motion and colour from the master. No new media was generated for this lock. Preserve all raw FAIL / NOT MEASURED findings; neither this style approval nor a source-specific gate mismatch changes a gate result. Use the existing exact-file QA and fresh independent review on each new film.

Routing (Dan, 2026-10-27, replaces 2026-10-25): no fixed owner. A video stays with the AI it started on; for a new reaction Short recommend Codex (newest Sol, high), his lean. An active Claude session is not interrupted or taken over by this documentation update. Apply any actual transfer through the existing round/sole-owner controller. Setup, thumbnails and upload remain in the existing setup workflow.
