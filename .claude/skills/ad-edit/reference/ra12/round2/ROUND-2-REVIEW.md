# RA-12 R2 independent review: "The First Step To Getting Abs Isn't A Workout" (9:16 AD)

Reviewer: independent (Opus 5.5), 2026-10-20. Read: AGENTS.md, VIDEO-RULES top sections + label/gate/vertical/B-roll/AI-clip sections, 00-RULES.md, beats_r2.json, cuts.json (assembly map only). Not read: editor notes, decided.json, logs, review page, watch/findings.
Plan note: beats_r2.json has no §11 output format, so this file uses findings + VERDICT.

## File reviewed
`deliver_r2/the first step to getting abs isnt a workout | claude | 9x16 | RA-12 R2.mp4`
- sha256 cbac4bcf2203ac9676aaac04258cbcee9e43454542f9488f5e796de5fb3f16ce (matches brief and the audio stamp)
- H.264 High 1080x1920, 30000/1001, 1386 frames, 46.246 s (under 0:59), yuv420p, BT.709 tagged; AAC LC 48 kHz stereo 272 kb/s
- Loudness -14.2 LUFS, LRA 2.5 LU, true peak -2.2 dBTP (ffmpeg ebur128, my measurement)
- Every frame decoded at full res (BT.709). Picture cuts found at frames 70, 97, 124, 157, 246, 344, 386, 421, 465, 503, 536 (inside P1), 649, 685, 745, 803, 1009, 1178, 1250, 1282: all match the plan.

## Defects

1. **BLOCKER: no passing gate stamps on the delivered file.** `.audio_gate.json` (GATE_VERSION 2.0.0, current) has verdict **FAIL**: tone mean error 1.36 dB (limit 1.2), max 4.59 (limit 2.5). There was no `.deliver_gate.json` when I checked at 18:42 and again later (a gate pass was still queued). Per the gate rule, a missing or failing stamp is a FAIL. R1's delivered file had the same tone FAIL and its deliver gate also read FAIL (`audio:stamp`). If Dan's approved bass voice is the cause, that needs to be recorded the way the rules allow, not left as a failing stamp. I did not listen; the tone figures are measured only.

2. **34.0-36.0 s (T1, frames ~1015-1080): an AI picture of Dan remains.** The app tour's Push-Up demo shows AI-Dan (Dan's face, haircut, black tank) doing push-ups, with the app's small AI-GENERATED badge. The brief asks that no AI picture of Dan remain, and Dan's note says to use the prospect "for everything" because AI images of him make his own abs look AI-generated. Fix: use a tour cut that skips the Push-Up sheet (go straight to calorie tracking), or a demo that does not show Dan, or get Dan's explicit OK to keep it.

3. **2.34-3.24 s (W1): ab wheel colour does not match the presenter footage.** His lit back reads orange. Mean skin saturation 0.48-0.57 at hue about 25°, against 0.25-0.38 at about 20° on the presenter (frames 40, 200, 1300). The picture is also soft. This breaks "All B-roll is colour corrected". The clip is also a small 1010x570 card (about 28% of the screen) with his face turned down and his abs hidden. He does move into the roll-out (the head travels about 80 px over 0.9 s), but at that size and angle it does not read as "me looking the most ripped".

4. **17.12 s (frame 513): one frame of the prospect's before photo with no AI-GENERATED chip.** The chip appears at frame 514. Every AI picture must carry the label for its whole screen time.

## Minor (fix if touched)
5. 12.28-14.0 s: the caption reads "day, stay motivated". The comma splits subject and verb ("guys who ... look at it every day stay motivated"). All words otherwise match the audio exactly for the whole film.
6. 3.24-3.6 s (D1): the salad container is cut off by the left edge as the shot opens. His lips move under the voiceover, with two open-mouth beats at frames 101-103 and 113-115 that roughly coincide with "it's" and "a/diet". At 0.9 s it reads as a quick kitchen cutaway, not a sync fault. Acceptable. It is not between-takes junk: he holds the salad up to the camera.
7. Room-tone dips to -55 to -59 dB (median pause floor -40 dB) at 2.16-2.30 s (just before "isn't" at 2.31), 40.54-40.68 s and 45.42 s. These are candidates for a 5-second listen. I could not listen, so they are unverified.
8. 17.88-21.62 s: the P1 goal picture is a still photo for 3.7 s (photo area change 1.1 over 111 frames). The Soft Blue field moves (9.3), so the motion rule holds. G1's planned "slow push" is barely visible (0.94 change over 1.1 s).

## Checks that passed (measured)
- **Prospect identity:** every AI physique picture (G1, K1, P1 before/after, A1) shows the same lake-dock man. The P1 before (a heavier version of him on the same dock, same navy drawstring shorts) and after are the same person. AI-GENERATED is present on G1, K1, P1 (from frame 514), A1 and Q1 on every sampled frame, and it sits below the picture, not on a face or abs. There is no "Real picture of me" label anywhere. Nothing implies the prospect is Dan.
- **Graphics (C1 22.86-24.86, L1 39.31-41.71, C2 42.78-46.25):** box top at y 1521. The caption band is y 1422-1484 on every frame checked (every 2nd frame), with no caption pixels in the 1486-1519 gap, so there is no overlap and they sit about 36 px directly below the captions. Boxes cover his shorts. The navel and lower abs end above y about 1330 in FAR shots, so his abs stay clear. Each graphic starts or ends on a cut and is fully faded before the size change (frames 744, 1248), so the joins are clean.
- **Hair and headroom:** top crops of every 8th presenter frame plus every join frame show the hair top at about 70-120 px on presenter shots and about 100 px in D1. Never clipped, with slight room every time.
- **Jump cuts:** the presenter joins at 246, 685, 745, 1250 and 1282 each change size by about 20-25% (NEAR/FAR). There is no same-framing join.
- **Lip sync:** face-mesh mouth opening against the audio envelope gives a best offset of +1 to +2 frames (mouth leads), consistent across 10 presenter segments. That is normal anticipation, in sync.
- **AI clips:**
  - K1 (11.48-12.88), phone on marble showing his goal picture. Cause and effect holds (only a gentle camera drift). Sound off, a stranger would say "a phone showing a photo of a fit man". It shows "look at it every day". There is no lock-screen clock, which is fine.
  - Q1 (14.05-15.52), sweaty beginner flat on a gym floor beside a tiny pink dumbbell, with a towel on his chest, breathing and moving his head (motion every frame, change 11.9 first to last). Cause and effect holds. A stranger reads "he gave up / is exhausted", which matches "when everyone else quits".
- **Audio joins:** seamscan over the plan's seam (15.489) and all 18 picture cuts. The 15.489 R1|R2 seam sits in a pause after "quits." (floor -42.7 to -38.9 dB, next word at 15.62) with no click. No dead air, no hard onsets. The "click" list holds plosive transients, not edit clicks. Not verified by ear.
- **First and last frames:** frame 0 is Dan clean, with the caption from 0.2 s. Frame 1385 is Dan with C2 up, a 0.65 s end hold.

## Could not verify
Listening (no audio playback available to me), so audio verdicts are measurement-only. The deliver gate result (it had not finished). Whether Dan has accepted the tone deviation for this film.

VERDICT: DOES NOT SHIP
