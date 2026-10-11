# CONTENT: Meal Prep SFC R1, DS-28 approval checkpoint

Round1 is waiting for Dan's creative approval. This is a dedicated Short from C1720, not an ad. The complete59.56s film has not been assembled or certified. No upload or publishing is authorized by this edit task.

Review page: http://127.0.0.1:8891/

Public Drive packet: https://drive.google.com/open?id=122cUvcBr_Aw2U9-xInddlvUGgXB30eSj

Work: `/Volumes/Extreme/_edit_work/ds28/round1/`. Review media: `review/`. Rebuild package: `review/recipe-DS28-R1.zip`. All packet files and hashes: `packet-manifest.json`. Managed server caches linked assets on the internal drive and restarts at login.

## Required files

Read `Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md`, the Codex long-form-content-edit skill, `.claude/skills/shorts/SKILL.md`, shared PRE-RENDER-APPROVAL.md, the DS-28 brief and `review/notes.md`. Read the master and coordination board before claiming the next round. Queue state is `draft_review`, not delivered or finalized.

## Work completed and pending choices

- C1720 indexed with shared roll sidecars. Source is read-only: `/Volumes/Extreme/dan rose fitness 9:23 shoot - vsls, long form content, short form content/C1720.MP4`. Sony FX30 S-Cinetone Rec.709, native portrait. No transpose or log LUT. Dual-mono lav measured with shared picker.
- EDL: source9.1-62.15s, then source79.35-85.85s. Frame-quantized total1785frames at30000/1001,59.5595s. Source closing pickups and crew direction were inspected. The clean final pickup still needs dense head measurements and its full-film join built.
- Three grades tested at two moments beside approved C1652/DS17 references. Middle B selected and shown moving. Keep natural amber studio light and cyan practical lights. No creative look or sound is locked by Dan yet.
- Four30s audio treatments, five randomized listener comparisons, then no-expander finalist comparisons. Exact opening finalist averages: corrected7.6/10, untreated7.0/10. Rankings varied. Shared tone correction without expander or dereverb selected; original volume-corrected comparison is on the page. No private audio processor. Reference and original A/B clips included.
- Two real stock clips: B0503 source12.8-16.1s, meal boxes unpacked, crop608x1080 atx650; B0018 source5.0-8.9s, hands portion food, crop1214x2160 atx1120. Paths in clip-candidates.json. Home-cooking stock rejected as contradictory. Microwave/eating/fridge actions were not filmed; current proposal stays on Dan.
- Shared HyperFrames0.8.97 Soft Blue Light Motivation graphics: G01,4.96-8.24s, MEAL PREP / Skip the kitchen time; G02,28.14-36.66s, MEAL PREP / Save time. Simplify tracking. Both motion clips are shown in context. Word-driven data is in plan_resolved.json, graphics-sheet.json and hf16/configs. Reuse shared vertical.py and maintained compositor, never fork templates.
- White Arial Bold86 captions, outline7, shadow3,2-3word chunks, MarginV420 so they sit below the graphics. Two overlapping cues were repaired by capping padded cue ends at the next cue start. No music, AI images, end logo, cover or derived formats.
- Shared landing tracker anchors actual cut frames and holds each shot independently. Head samples every0.25s, motion reports in motion-stats.json. Do not track across cuts or recenter exits.

## Verification and limitations

The exact1080p opening audio is PASS12/12. Longer40.607s context audio is FAIL11/12: tone maximum3.66dB exceeds2.5dB, mean1.09dB passes. Preserve this open failure; do not relax thresholds.

Context delivery gate2.5.1 is FAIL:33 pass,4 fail,2 not measured. Open: tone, stock coverage17% against30%, far-shot head size23.8% against27%, legacy caption-onset median498ms late. Banned-screen comparison and negative-events evidence are missing. Those rows were not run successfully. No final certification. Caption timing still needs proper independent delivered-audio evidence, not a reused source timing claim.

Visual scan of exact context1217frames: zero black/frozen/unexplained/naked-cut events; both graphics present. One independent GPT-6 Sol reviewer inspected all14 real images and native frames at both caption repairs and the ending: zero open visual defects. Findings and watch log are in preview-qa/. This review certifies the preview picture only, not the unbuilt complete Short or a PASS delivery gate.

Chrome opening and G02 context played to completion without media errors. Backward/forward seeking changed playback time. All14 linked local URLs returned200;8 media URLs returned206 byte ranges. browser-check.json and http-check.json contain evidence. Managed review server refreshed after latest page edits.

## Next action

Wait for Dan's opening/look/sound/assets decision. Record his exact words and scope with file hashes in a new `round2-plan/decisions.json`. Re-hash approved files, leave round1 unchanged, then build in round2/. Tighten the far shots, reassess full-film stock coverage and independently align delivered speech/captions. Build the remaining main take and clean closing pickup with shared framing, audio, captions and graphics. Resolve every open exact-file gate, inspect every join and obtain one independent complete-candidate picture/audio review. Mark source ranges used after the EDL is final. Deliver1080x1920 master, phone copy, A/B, captions sidecar, full recipe and valid stamps. Copy any45s+ review film into `Videos to Review/` and open that folder. Update DS-28 to delivered only when the complete review copy is actually sent. Do not make covers or upload.

Private rebuild entry points: recipe/prepare.py, picture.py, finish-preview.py, page.py. picture.py caches by file presence only, so delete changed scene caches or add fingerprint validation before reuse. finish-preview.py fingerprints composite inputs. Use project ffmpeg and check the two-build cap before running. Every source/reference path is in JSON or recipe code. Some recipe preparation regenerates audio/graphics data, so do not run it blindly on a reviewed round.

## Cost and continuation

Generation$0. Gemini review usage calculated$0.434918 from17 returned receipts at published rates. Provider invoice and editor/reviewer agent token usage are unavailable. No new spend needed to resume assembly. Keep the session$25 generation cap and the separate review approval threshold.

Recommended model: GPT-6 Sol, high effort, throughout including the independent full-candidate review.

Starter prompt: Rename this chat Meal Prep SFC R2. Read Handoffs/handoff-20261011-ds28-round1-dan-review.md. Record my approval or exact changes for the DS-28 opening, look, sound and assets with their hashes, then finish the59.56s dedicated Short using $long-form-content-edit plus the vertical Shorts rules. Preserve reviewed round1, resolve all recorded gate failures, obtain one independent complete-film review, deliver the master and phone review copy, and update00-MASTER.md. No covers or upload.
