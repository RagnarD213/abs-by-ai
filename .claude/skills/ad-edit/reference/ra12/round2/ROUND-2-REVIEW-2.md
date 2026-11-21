# RA-12 R2 independent re-review: "The First Step To Getting Abs Isn't A Workout" (9:16 AD), fixed build

Reviewer: independent (Opus 5.5), 2026-10-20 evening. Read: AGENTS.md, VIDEO-RULES (hair, render queue, B-roll colour sections), 00-RULES.md, beats_r2.json, cuts.json (assembly map), the previous ROUND-2-REVIEW.md, the two stamps. Not read: editor notes, decided.json, notes_r2.json, logs, review page, watch/.
Plan note: beats_r2.json has no §11 output format, so this file follows the previous review's layout (defects, passed checks, could not verify, VERDICT).
Excluded by the brief (not counted): the app tour's Push-Up demo (AI presenter in a tank top, app AI badge), captions over the bottom of the full prospect photos, the audio tone row FAIL (Dan's bass lift), and the delivery gate stamp.

## File reviewed
`deliver_r2/the first step to getting abs isnt a workout | claude | 9x16 | RA-12 R2.mp4`
- sha256 391811ce7afe16ff5d523ad2a735f2a3f276d51f1687f3fbd386d12b568cf3a4 (matches the brief, the `.audio_gate.json` and the `.deliver_gate.json`)
- H.264 High 1080x1920, 30000/1001, 1386 frames, 46.246 s (under 0:59), yuv420p, BT.709 tagged; AAC LC 48 kHz stereo 272 kb/s
- Loudness -14.2 LUFS, LRA 2.5 LU, true peak -2.2 dBTP (my ebur128 measurement, identical to the previous build)
- Every frame decoded at full res as BT.709. Picture cuts found: 70, 97, 124, 157, 246, 344, 386, 421, 465, 503, 536, 649, 685, 745, 803, 1009, 1178, 1250, 1282, all as planned, plus 1080 and 1112, which are screen changes inside the approved app tour (T1).
- Stamps: audio GATE_VERSION 2.0.0 (current, verdict FAIL on the excluded tone row only; every other row passes). A deliver stamp (GATE_VERSION 2.6.1, current) already exists from 20:13 with verdict FAIL. It does not record which row failed, and the brief excludes it.

## The three items asked

**(a) Ab wheel W1, 2.34-3.24 s (frames 70-96): PASS, with a minor residual.** The card is now about 1020x860 (it was 1010x570) and starts on the roll-out. Measured on the same skin mask (YCrCb skin, V>0.25), W1 skin is median S 0.55-0.60 at hue 26°, against 0.58-0.60 at 24° on presenter frames 0, 40, 200 and 1300. The shaded forearm reads S 0.60 at 24°, an exact match. The skin is not darker than the presenter (V 0.47 shade to 0.80 sunlit, against 0.56-0.72).
Residual: the sunlit back (box x380-560, y800-900) still runs warmer for the first half of the clip. It measures S 0.72 to 0.65 at 30° (frames 70-83), easing to 0.57 at 28° by frame 96, against 0.51-0.61 at 24° on the presenter's chest. Lab chroma is 47 against 35. The grade also pushed the shaded whites cool (white chair b -19, concrete b -7) where the presenter's stone wall reads warm (b +8). At playback speed it reads as golden-hour sun on his back rather than a grading fault. Listed as minor 1 for Dan's eye.

**(b) The prospect's before photo on the phone (P1), frames 513-535 (17.12-17.85 s): PASS.** I checked frame by frame at full res. The AI-GENERATED chip (template match 1.00 at y 1606) is present on frames 512-535, so it arrives one frame before the before photo appears (frame 512 still shows the form; the photo first shows at 513). The chip stays on through the full goal photo, frames 536-648 (match 1.00 at y 1585), and is gone at 649 on the cut back to Dan. Frames 503-511 show only the app form, with no picture. The previous defect (frame 513 without a chip) is fixed.

**(c) No regressions against the previous passed list: PASS.**
- Buttons and KEY POINT under the captions: C1 (685-744), L1 (1178-1249) and C2 (1282-1385) were checked on every other frame. No caption or white text pixels fall in the y 1486-1520 gap, and the box tops sit at about y 1530, below the caption line. The boxes cover his shorts, and his abs stay clear (frame 1385 checked).
- Hair room: I measured the hair-colour component top on 186 presenter frames (every 4th frame plus the first and last frame of every hold). The minimum is 70 px (frame 1350), the median 94 px and the maximum 139. Slight room in both sizes and never clipped. D1 hair sits at about 100 px.
- Jump cuts: the presenter joins at 246, 685, 745, 1250 and 1282 each change size, NEAR to FAR or back (frames on each side checked). No same-framing join.
- Lip sync: I compared face-mesh mouth opening with the audio envelope on all 11 presenter holds. Nine give a best lag of +1 to +2 frames (mouth leads), the same as before. Two are inconclusive (246-344 r 0.16; 745-803). In 745-803 the cut lands on 4 frames of a wide-open mouth with no sound (24.86-24.96 s, a breath before "And" at 25.00). "And your picture isn't just motivation" then tracks visually frame by frame. This is not a sync fault. See minor 3.
- Labels: AI-GENERATED appears on every frame of G1 (124-156), K1 (344-385), Q1 (421-464), P1 (512-648) and A1 (803-1008, the smaller chip in a fixed position on all 206 frames). Every chip sits below the picture or phone, never on a face or abs. There is no "Real picture of me" label.
- Same prospect: G1, K1, P1 (before and after) and A1 all show the same lake-dock man in navy drawstring shorts. Nothing implies he is Dan.
- Captions, first 30 s, word for word against a Whisper medium.en transcript of this file: every word matches and its highlight lands on the spoken word. The "free." caption arrives at 21.40 s against a Whisper onset of 21.26 s, within tolerance.
- First and last frames: frame 0 is Dan clean with no caption until 0.15 s. Frame 1385 is Dan with C2 up.
- Audio joins: seamscan ran over the plan's one audio seam (15.489) and all 21 picture joins. The 15.489 seam sits in the pause after "quits." (-35 to -41 dB, next word at 15.62), with a maximum sample step of 0.0066 and no click. There are no hard onsets and no dead air. Every other flag falls on a picture-only cut over continuous voice.

## Defects
None blocking.

## Minor (fix if touched, or put to Dan)
1. **2.34-2.8 s (W1):** the sunlit back is still warmer than the presenter's skin (S +0.06 to +0.11, hue +6°, chroma 47 against 35), and the shaded whites lean blue (b -19 against the presenter's +8). If Dan finds it orange: pull the highlight saturation on the back only and warm the shadows back to neutral, rather than cooling the whole clip.
2. **12.28-14.0 s:** the caption still reads "day, stay motivated". The comma splits subject and verb. Carried over from the previous review.
3. **24.86-24.96 s (frame 745):** the zoom cut opens on 4 frames of a wide-open mouth with no sound before "And". It is natural (a breath), but a 4-frame later in-point would be cleaner.
4. **Room-tone dips** to -52 to -59 dB at 2.16-2.30 s (just before "isn't"), 40.52-40.68 s and 45.42-45.48 s, against a pause floor of about -40 dB. These are unchanged from the previous build and need a 5-second listen.

## Could not verify
- Listening: I have no playback, so the audio verdicts rest on measurement only (the dips in minor 4 and the 15.489 seam).
- Which row fails in the existing `.deliver_gate.json`: its rows carry names only. The brief excludes it.
- A frame-for-frame comparison with the previous build: that file was overwritten. I compared against the previous review's recorded numbers and frame list.

VERDICT: SHIP
