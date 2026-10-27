# Reaction-video format: the reference build (DS-44 Hormozi Fat Guy SFC, R2 approved 2026-10-23)

Historical reference, superseded by Dan on 2026-10-25: [Bill Maher Codex R5](../ds40-codex-r5-reaction-format/README.md) is now the standard for all reactions. Keep this recipe for existing approved Hormozi exports, not as the default format.
Copy of `/Volumes/Expansion/_edit_work/DS-44/r2/recipe/` (R1 assets live in `../r1/`; R2 symlinks key/src/audio to them).
Copy into your own work folder and edit the constants; never run it inside another job's folder.

| step | file | what |
|---|---|---|
| plate + key | `plate.py`, `stage1_key.py`, `srcprep.py`, `stage15_temporal.py`, `keylib.py`, `common.py` | the house key (DS-40 Claude R2) cached at 0.75 scale; `Y_BOTTOM=3840 ROWS=2880` keeps the laptop for the corner piece (`run_key_watchF.sh`); `run_key.sh` keys the talking pieces (laptop cropped) |
| edit list, audio, words | `prep.py` | clip segments (cut at camera changes, silences under 1 s), roll = clip time + offset (cross-correlate the lav, which hears the laptop), talk pieces in measured dips, voice chain, words on the film timeline |
| media caches | `prep_media.py` | clip frames, B-roll, `--card` = the interview shot for the frame behind Dan's head |
| framing | `framing.py` | corner (0.40 of full size, full-height key), the handover target, the card shots (hair line y 540, W = whole width, T = 0.82), normal W/T talk shots (3.5 % headroom), clip windows per camera shot |
| graphics, captions | `graphics.py`, `captions.py` | Soft Blue HyperFrames lower thirds (check each render's frame count against its slot); captions "Clip" style during the clip, "Default" lowered under the card section's graphic |
| assembly | `assemble.py` | `feather()` soft right edge (`elbow_fw` widens it where an elbow reaches the camera edge), `draw_card()`, the shrinking-clip handover, the silent card |
| checks | `measure_render.py` + `ds44_mcflicker.py`/`ds44_measure_r2.py` (key bar), `gateplan.py`, `chain_qa_r2.sh`, `build_r2.sh` (one queue step) |
| page | `page.py`, `options.py` |

Traps this build paid for: a room-tone segment under the handover carried a hiss; the source tag must sit only on the named
speaker's own shot; check every read of the first line for eyes on camera; the gate's hair rows misread the speaker in the top
frame and behind the corner (known mismatch); the stage-1.5 pool hangs under memory pressure (resume skips finished frames).
