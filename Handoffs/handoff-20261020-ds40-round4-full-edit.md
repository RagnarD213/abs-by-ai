**CONTENT SFC. Task name: `Bill Maher Fat 90-Year-Old SFC R4`. Start now.**

# Bill Maher Asks If You've Ever Seen A Fat 90-Year-Old. He's Right.: full edit after key approval

Recommended model: **GPT-6 Sol, high**. Dan approved the R3 key and explicitly authorized the full edit. The fresh task moves from a 10-second calibration into source selection, reaction assembly, captions and full QA. Do not restart the key/audio/color audition. This originating R3 chat stays pinned until Dan unpins it.

## Read first and ownership

Read `AGENTS.md`, `.claude/skills/_shared/VIDEO-RULES.md`, `Handoffs/video-editing/00-RULES.md`, the DS-40 job document, `ds40-codex-r4-plan/decisions.json` and `ds40-codex-r3/README.md` under `Handoffs/video-editing/`. Use Codex `$long-form-content-edit` for source/key/audio/color and `.claude/skills/shorts/SKILL.md` for dedicated vertical finishing. Read the current cut-continuity, pre-render, graphics and caption references. The job is dedicated CONTENT, not an ad or an extracted long-form Short. Do not derive other formats or Shorts.

Read `AI_COORDINATION.md` before claiming the full edit. Claude's parallel competition was authorized separately and remains separate. Do not run or inspect scripts inside its `/Volumes/Extreme/_edit_work/ds40/` build. Do not modify its board entry. Work in a new `/Volumes/Extreme/_edit_work/DS-40-codex/round4/`; preserve R1/R2/R3 and their review servers.

## Exact approval and global standard

Dan's verbatim message is in `decisions.json`: "The hair looks good enough now. Keep the Balanced audio and warmer color and go ahead with the full edit.  This is a significant improvement for the hair. Let's lock this as our chroma key style. I want all the videos keyed out like this. This is a very clean key."

The key is now the shared green-screen standard for both Claude and Codex, recorded in AGENTS, VIDEO-RULES and `.claude/skills/_shared/chroma-key/README.md`, with unchanged reference recipes and hashes. Read that README before building. It combines the accepted R2 body/arm matte with R3 motion-stable hair. Do not revert to R2 hair or a generic one-frame chromakey filter. Calibrate ROI and screen per shot; do not blindly reuse sample geometry or temporal neighbors across cuts. The global lock covers keying, while Balanced audio and warm color are this video's choices.

Approved reference under `/Volumes/Extreme/_edit_work/DS-40-codex/`:

| File | SHA256 |
| --- | --- |
| `round3/review/media/sample.mp4` | `1c07c3d3c585fe05a7a2f1274d4a62bec46de1e6be7bdbfb4214f44af2b7ace1` |
| `round2/voice-balanced.wav` | `089264175840f8aa4956d98a7e8bd82d93bd8c1dcee73493d4733ae224df2a6f` |
| `round2/review/media/balanced.mp4` | `622ec8a71b344a13496277ce3e7c3de17a8229d6d7d71bcea1084256273d0100` |
| `round3/grade.py` | `d6d2c4cd854088f4383649f4b9929631a7f2c3d409c8dd08d1db41a916f600ce` |

Review reference: http://127.0.0.1:9031/
Public Drive reference: https://drive.google.com/file/d/17TO-EYOAOmTu5i1Ivhu7ChOQSu-u3Q09/view
R3 folder: https://drive.google.com/drive/folders/1B162kFjEdHizvnL3-HU-bJY3zJNNwSS2

## Source and full edit

Read-only source: `/Volumes/Extreme/10:15 dan rose fitness shoot - green screen, outdoor shorts, outdoor b roll, studio backdrop/C1730.MP4`. Read `Docs/SHOOT_1015_FOOTAGE_REPORT.md` and the existing roll sidecar. Native auto-oriented decode is 2160x3840, 30000/1001, Sony S-Cinetone BT709. No extra transpose. Left lav is established; avoid loud flat-topped words if a cleaner performance exists.

The approved calibration is only source 1413.0116-1423.0216, 300 frames. It is not the whole take. Full scripted performance starts around 23:12, spontaneous alternative around 24:13. No full take selection, final cut map or final mark-used has happened. Build the main edit from the scripted take and show the off-the-cuff take as the requested alternative. Preserve complete words, natural breaths and deliberate delivery, remove actual resets and failed repetitions.

The reaction clip plays first, with nothing before it. Retrieve the exact source and times from `10-17 Shoot - Reaction Clips`, Google Doc `1BcRpzDQYNCssROEvg10Z9cOL2AtdvBdyqHwvxxwHtQA`; do not guess a substitute. Editing script: Doc `1gt8Fi_wUaNaksa8sAdMoBvcdlBhZLek82EpBr-leq-0`; teleprompter: `1KvL0_IilRCxlofnY5luTfRvjiseGGpGGXU4sAsjbgzQ`. Final 1080x1920, approximately 45-66s per job brief, J2 captions with current Soft Blue Light HyperFrames graphic rules. The laptop was retained only for wide edge inspection; crop it out in the final layout while preserving hair, arms and gestures. Use the established vertical centering method when movement needs it.

Dan has explicitly said to proceed with the full edit. Carry out the full edit with the locked choices, without another ten-second calibration or redundant audio/color question. Follow current specific approval rules for any genuinely new AI frames/motion or uncertain graphic asset; full-edit authorization is not permission to silently choose unseen AI concepts. Prefer the required reaction clip and suitable existing assets; do not invent extra generation to create a new approval dependency. No covers, publishing or scheduling in this editing task.

## Reproduce the accepted picture and sound correctly

R3 `render.py` patched the hair over decoded R2 body pixels for the ten-second sample. It cannot simply be pointed at a longer duration. Adapt the raw body key from R2, then apply the R3 hair method on the selected raw frames. Archive copies of both renderers are in the shared key reference. Keep a five-frame neighborhood within each continuous take only; soft handover and consistent screen field. Use accurate BT709 RGB decoding and matched field colors. The first R3 export had a rectangular tint seam; the delivered and approved export fixed that. Do not use `internal-before-field-match/`.

Keep the exact warm grade recipe. For the complete selected dialogue, apply the final Balanced chain from `round2/audio_refine.py`, not the earlier `audio_build.py`. The shared reference archives the final recipe and audio-options JSON. It uses the shared voice chain, no expander, target -14.1 LUFS, true peak -1.5, oversample 4, and the final Balanced EQ in that script. Recheck the resulting voice against the approved sample without retuning to chase gate scores. Never repeat or stretch the ten-second WAV to cover the full speech.

## QA, delivery and state

Run buildcap before renders, transcription and QC, maximum two builds machine-wide. Retain raw footage read-only. Exact full candidate gets audio/delivery gates, hash-bound watch, every join inspected in native motion and source context, freeze/junk/scene checks, and one independent Sol review. Verify hair throughout the selected footage, particularly turns and gestures on both light/dark fields. The existing `key:hair_temporal_edges` gate is unimplemented; human approval does not make it pass.

Historical R3 gate: 37 PASS, 1 FAIL accepted Balanced comb/tone, 1 NOT MEASURED zero-boundary watch, 18 N/A. Those are historical calibration results, not a pass for the new full film. Actual edit boundaries must be inspected in the full film. Never invent boundaries, loosen thresholds or conceal failures.

Deliver the complete review copy, phone preview and relevant contextual comparisons. Use a new managed review port, silent playback/seek/Reload checks and leave paused. Upload review files to public anyone-with-link Drive and verify. R3 stays intact. Record exact media hashes, costs and actual gate findings. R3 measured external review cost was $0.089616; new task starts its own spend ledger. Subscription usage unavailable. No generation spent in R3.

Update queue/master with queue.py and mirror the status export. Connected Drive `update_file` can replace `/tmp/edit-queue-export/edit-queue-status.json` in existing ID `1RX-GqepEKqB1LgJqJFRyRU2lOJMnRFgg`; pass the full project absolute path and read back. Rclone has hit quota before. Do not touch the paused Victory Dashboard. Remove this handoff from OPEN when starting. Commit/push named records via safe-push. No app code changed in this calibration/standardization phase.

## Start now

> CONTENT SFC. Name this task `Bill Maher Fat 90-Year-Old SFC R4`. Read `Handoffs/handoff-20261020-ds40-round4-full-edit.md` and execute it. Dan approved the R3 chroma key as the global green-screen standard and authorized the full edit. Keep Balanced audio and warmer color. Build the complete reaction Short from the scripted take, with the reaction clip first, captions and current graphics, then run the full checks and independent review. Do not reopen the approved key/audio/color choices. Use GPT-6 Sol at high effort.
