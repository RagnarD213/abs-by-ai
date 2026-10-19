# CONTENT SFC: Bill Maher Asks If You've Ever Seen A Fat 90-Year-Old. He's Right. (DS-40), Codex R2

2026-10-19. This is a 10.01-second calibration revision only, awaiting Dan. The full Short has not been edited, approved, published or scheduled.

## Review

- Comparison page: http://127.0.0.1:9021/
- Public review folder: https://drive.google.com/drive/folders/1K52GrFaKbqWnoTORTR9bfdQt__IjHCX5
- A, unchanged voice with new wide picture: https://drive.google.com/file/d/1YStGJGkklIL4Jqo-t_AyyQD1vDzOcMEJ/view
- B, balanced: https://drive.google.com/file/d/1JbvZjkrqvtZSWLRLeed6XFnqqhF-n_Zu/view
- C, clearer: https://drive.google.com/file/d/1FnUp_IogCmZjcHt_YUdPPrx3WDcBHnpr/view
- Phone copy: https://drive.google.com/file/d/1YBjjzWKh-L_UlqNYzBIikH2hCeAjVLxS/view
- Moving hair comparison, old above and revised below: https://drive.google.com/file/d/1HyGBvHQG7jMS2rqxlwaCXq1V7vpaeIV8/view
- Work directory: `/Volumes/Extreme/_edit_work/DS-40-codex/round2/`

## Requested changes

Dan liked the warmer color and considered the previous audio fairly decent. He asked for gentle alternative audio, cleaner moving hair edges, and the widest view to inspect arms. Warmer grade is unchanged. A uses the byte-identical R1 voice WAV. R1 page and media remain untouched. Claude's parallel work remains separate.

The widest native camera view records head to waist and laptop, not legs. This is explicitly requested diagnostic framing. Keep normal final framing decisions separate. The source is read-only C1730 from the 10/15 shoot, approximately 1413.0116-1423.0216 seconds, same continuous scripted passage as R1. Final take selection and mark-used remain pending.

## Picture

Native 2160x3840 Sony S-Cinetone BT.709 decoding, no log LUT. The R1 body matte is retained. Hair uses a softer refined alpha, a guided filter and neighboring opaque hair colors to reduce edge discoloration. Previous and next real camera frames are aligned using optical flow, with confidence rejection and blending only around the hair. Alpha and foreground are resized together before the unchanged warm grade. No generated person, skin smoothing or tighter crop. 1080x1920, 300 frames at 30000/1001.

Independent audit confirms less moving fringe and shimmer, recognizable hair texture, intact glasses and arm edges. A little purple/gray fringe remains at the top-right hair, clearest enlarged at 7.9-9.1 seconds. A video-model motion-trail flag was not confirmed as material in native consecutive frames. This is improvement, not a claim of a perfect key. Dan should review 1-3, 4-6 and especially 7.9-9.1 seconds.

## Audio

Shared voice_chain only; shared self-test passed. No dereverb or expander. A is preserved. B and C use mild EQ, matched loudness and an oversampled limiter with more headroom. Parameters are in audio_refine.py and voice-chain receipts. A measures -14.1 LUFS/-2.4 dBTP, B -14.2/-1.3, C -14.3/-1.4.

The original four flags measure resonance, tonal balance, speech-decay contrast and variation in spoken level against a fixed reference. Raw-source resonance also misses the bound; the original treatment reduced the other two dynamics measurements. B now clears decay contrast and speech variation but still fails resonance and tone. A fails four rows; C fails three. No thresholds were changed. A remains the blind listening favorite, matching Dan's opinion. Five-way independent and two earlier listening trials do not establish a consistently superior alternative. Internal Fuller and Focused trials are not offered: neither established a listening advantage, and Fuller sounded more processed in the independent comparison.

## Checks and delivery

Every delivered audio MP4 was gated. The exact A full-delivery gate reports 37 PASS, 1 FAIL (audio), 1 NOT MEASURED and 18 declared NA. No all-pass claim. The independent watch manifest is judged, but the shared watch gate requires a nonzero boundary count and cannot certify a genuinely continuous clip. No fake boundary was added. Source words, sync, stream integrity, dimensions, duration and all 300 frames pass. There are no editorial joins, captions or graphics in this requested test.

Google Drive folder and six videos have verified anyone-with-link reader permissions; returned file sizes match local media. The rclone shared-client quota interrupted upload after A/B; the connected Drive uploader completed C, hair, dark and phone. Connector metadata omits checksum fields, so remote hashes are not claimed. Local hashes are in receipt.json. The managed page caches linked media and survives chat exit. HTTP byte ranges and muted browser playback/seeking/source switches were verified. No audible Mac playback was used.

New external review spend: $0.0363 parent plus $0.0154 independent, total $0.0517. No paid generation.

## Next

Dan picks A/B/C and judges the revised hair and arm edges. Do not start the full Short before that feedback. Later work includes full take selection, reaction source, edit, subtitles, final gates and full independent audit. Recipes here are archive copies: restore them into the external work directory before running. render.py depends on the source paths and R1 recipe recorded in its code.
