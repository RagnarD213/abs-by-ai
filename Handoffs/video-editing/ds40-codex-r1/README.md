# CONTENT SFC: Bill Maher Fat 90-Year-Old, Codex R1

2026-10-19. Dan requested only a 10-second key, audio and color calibration before any full edit. This is that review phase, not the completed Short. No Dan approval, upload for publication, scheduling or final delivery certification is claimed.

## Review

- Comparison page: http://127.0.0.1:9017/
- Full-quality Drive review: https://drive.google.com/file/d/13SHPFG7GCWHgG_dVhTzrUko7eXKpOC0F/view
- Phone preview: https://drive.google.com/file/d/17AAlvvsveQaUuMOJAvD4sUCFeo19y4eS/view
- Work directory: `/Volumes/Extreme/_edit_work/DS-40-codex/round1/`
- Main file: `review/media/sample.mp4`, 1080x1920, 300 frames at 30000/1001, 10.01 seconds, 12,863,236 bytes.
- SHA256: `874c8363a832bb20a57453a74d6b5da808886524b6013d12a06ea8f1b2eddceb`
- Drive returned the identical SHA256. Both review links returned HTTP 200 without authentication and displayed the intended filenames. Rclone public links were created.
- Managed review server caches media locally and restarts at login. HTTP 200, video byte-range HTTP 206, muted browser playback, seek to 7 seconds and dark-source switch verified.

## Source and treatment

Source is the read-only 10/15 green-screen shoot C1730.MP4. Source interval approximately 1413.0116-1423.0216 seconds, one uninterrupted scripted take beginning "That's why you need to treat your belly fat as an emergency." No internal edit seams. Roll sidecar reused; final full-video take selection and mark-used remain pending.

Decoded native Sony S-Cinetone as BT.709 with source orientation, no log LUT. Native portrait crop 1656x2944 at x252,y500. The key estimates the uneven screen field per frame, solves mixed edge pixels against nearby real foreground, preserves motion-blurred hands and hair, removes residual green, and resizes premultiplied color and alpha together. A ProRes 4444 intermediate retains the matte. Final small crop sets hair clearance and removes the laptop. Real camera detail is retained, no generated person or skin smoothing.

Natural is recommended; Warmer and Brighter alternatives use the exact same passage and matte. Flat light and dark fields are calibration diagnostics, not final video graphics. No captions, music, reaction insert or motion graphics were built.

Audio uses the left lav established by the roll sidecar. The shared voice chain is used after its self-test passed. Chosen treatment: HP70, 120 Hz +1.5 dB, 450 Hz -1 dB, 3200 Hz -1 dB, no expander and no dereverb. The normal expander and dereverb variants scored worse in listening comparisons. Final voice measures -14.1 LUFS and -2.4 dBTP. The selected raw passage does not touch the camera ceiling. No user-facing audible playback occurred during tests.

## Checks and explicit limitations

Independent auditor verified the exact hash, all watch images, 20 full-resolution sample frames, five dark diagnostic frames and native crops; moving video/audio and blind audio comparisons supplement the frame review. Findings: no confirmed material visual defect in the intended light composite, no clipped words or sync drift. Dark contrast reveals a thin hair contour and slight olive near the temple/glasses arm. The broad green-spill claims from one video-model pass were not corroborated in exact pixels. Details and contradictory raw result are preserved in audit records.

The numeric audio gate FAILS four fixed-reference rows: comb 1.03 dB versus 0.89 max; tone mean 4.08/max 8.28 dB versus 1.2/2.5 max; dryness 5.4 dB versus 5.9 min; spread 4.9 dB versus 5.2 min. Listening did not establish an audible defect matching those flags. No threshold or gate code was changed. This is a requested calibration sample for review, not an all-gates-passed master.

The shared watch manifest is independently judged clean, but the delivery gate cannot certify watch:pass because it requires a nonzero edit-boundary count. This genuinely continuous sample has zero boundaries. No fake boundary was added and the gate remains NOT MEASURED. Caption and editorial rows are explicitly inapplicable to Dan's restricted scope; every remaining row was run. See final delivery_gate.json for counts.

External review spend: $0.2445 parent trials plus $0.0046 independent audit, total $0.2491. No paid image/video generation.

## Next action

Dan reviews key edges, selects color and comments on the voice. Keep later work step by step; do not assemble the full Short before calibration feedback. Full take selection, reaction clip sourcing, edit, subtitles, final gates, final independent audit and eventual setup remain unexecuted. A new chat handoff would be R2 under the standing round rule, never a second R1. Claude's parallel directory was not modified.

## Reproduction

These scripts are archived copies. Copy them into a new work directory before running because they derive work paths from their own location. Do not execute from the archive or another session's directory. `render_key.py` makes the native-resolution key master, `finish.py` creates four picture variants, `package.py` combines the voice and creates review encodes, `page.py` builds the review page. The original work directory also retains all source audio extracts, baseline measurements and listening candidates. Respect the two-build machine cap. No application code or deployment changed for this media-only task.
