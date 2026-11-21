# RA-01 square (1:1), round 2 review

File reviewed: `/Volumes/Extreme/_edit_work/ra01-sq/master_1x1.mp4`
sha256 `3e7939bcc571c9a895429278d59a40b07465c1bda76ad5c76095ae93723ecedd` (matches the sha I was given), 63,039,980 bytes.
Reference: approved 9:16 `/Volumes/Extreme/_edit_work/ra01/master_9x16.mp4`, sha256 `02d032180a3eb42dc81d1857613df55ef4b715ab4d31e315834baf2a63003e51` (matches SQUARE-PLAN section 2).
Evidence (all 1714 frames of both files decoded as BT.709, face boxes and person masks on all 1040 on-camera frames, caption masks on every frame of both files, contact sheets, my own transcript): `/Volumes/Extreme/_edit_work/ra01-sq/review-r2/`.
Not read: any notes file, any ROUND-n-EDITOR file, any watch-pass findings file.

```
VERDICT: SHIP
DEFECTS (most serious first):
  M1  00:36.00-00:36.60 (frames 1079-1097)  a zoom cut should read as a deliberate shot  ->  the new NEAR shot is only 19 frames (0.63 s) before the macro card. It starts on a new sentence ("I even started using"), the level change is real (face 238 to 285 px) and it is the same length as each of the three after-picture cards, so it reads as a punch-in into the card, not as a glitch. It is the shortest presenter shot in the film and the one place a viewer could feel a quick double cut (FAR, NEAR, card inside 0.63 s). Opinion only, no rule broken.   severity: minor
  M2  recipe  the recipe beside the master describes the delivered file  ->  `cta_1x1/cta.json` records placement "level: NEAR" for both pills, but each pill also plays over FAR frames (566-569 and 607-614 for pill 1, 1612-1615 for pill 2). The delivered picture is clean on those frames (see D4 below); only the record is incomplete.   severity: minor
  NOTE (Dan's call, not a defect)  00:03.07-00:03.17 (frames 92-94) show the AI card where the approved 9:16 shows Dan, by round 2 ruling D1(a). Both CTA pills still print AbsByAI.com, as the approved 9:16 does, by ruling D6.

ROUND 1 DEFECTS:
  D1  FIXED.
      Frame 92 (00:03.07): frames 90, 91 are Dan NEAR; frame 92 is already the AI card with its AI-GENERATED chip (hard cut, no blend frame). The splice is covered by the card. Captions did not move ("real." is on 85-97 in both files).
      Frame 570 (00:19.02): frames 568, 569 FAR (face about 242 px), frames 570, 571, 572 NEAR (about 274 px). The hand jump now lands on a level change.
      Frame 1079 (00:36.00): frames 1077, 1078 FAR (238 px), 1079 to 1081 NEAR (285 px). Covered by a level change.
      Every visible presenter join changes level. Measured median face width per hold: 62-91 NEAR 292, 203-229 FAR 223, 369-489 NEAR 281, 490-569 FAR 242, 570-606 NEAR 274, 607-694 FAR 243, 695-744 NEAR 278, [stats card], 957-1078 FAR 238, 1079-1097 NEAR 285, [macro card], 1191-1224 FAR 240, 1225-1332 NEAR 284, 1333-1425 FAR 240, 1426-1535 NEAR 289, 1536-1615 FAR 238, 1616-1656 NEAR 275. Alternation holds at 490, 570, 607, 695, across 745-956 (NEAR to FAR), at 1079, across 1098-1190 (NEAR to FAR), and at 1225, 1333, 1426, 1536, 1616.
      No other uncovered splice: inside every hold the frame difference stays under 7 (cuts measure 28 to 117), and the only in-hold values above 5 are continuous arm gestures (1340-1344, 1634-1638, checked by eye) and the pill fades.
  D2  NOT PRESENT YET, as expected this round: no `master_1x1.mp4.deliver_gate.json`. Per my brief the stamp is written after this review and the watch-pass judge, so it is not counted. It must exist at GATE 2.4.0 with this sha before delivery.
  D3  FIXED. `beats.json` and `timeline_1x1.json` give the same 24 cuts I detected on the file (62, 92, 152, 203, 230, 249, 268, 287, 369, 490, 570, 607, 695, 745, 957, 1079, 1098, 1191, 1225, 1333, 1426, 1536, 1616, 1657) and the same NEAR/FAR level per hold. `cta_1x1/cta.json` boxes (x 224-854, y 600-732 and y 574-706) match the delivered pills (dark fill measured x 228-851, y 604-729 and y 578-703). Leftover nit is M2.
  D4  FIXED. Pill 1: fades in 566-570, solid 571-611, fades out 612-614, gone on 615. Pill 2: fades in 1612-1617, solid 1618-1651, fades out 1652-1655, gone on 1656, before the end card. Both pills are centred on the frame (centre x 539.5). Pill centre minus his face centre: median -9.5 px on pill 1 (range -27 to +36 as he moves), median +5 px on pill 2 (range -10 to +14). Jaw clearance (pill top to the lowest chin landmark) is at least 118 px on pill 1 and 98 px on pill 2 on every solid frame; the fade frames are FAR frames where his chin is higher still. On both NEAR and FAR frames the pill sits on the chest and pec line with the first row of abs visible below it (full-resolution crops `abs1.jpg`, `abs2.jpg`). It never touches the caption (pill bottom 732, caption top about 895).
  D5  FIXED. Video stream 8.54 Mbps (container 8.82 Mbps), inside the 8 to 12 Mbps rule.
  D6  FIXED. End card 1657-1713 shows the AI image, the AI-GENERATED chip and one bar reading "Tap the button below". No AbsByAI.com line on any frame of it.

CHECKED AND CLEAN:
  Section 1 container: 1080x1080, 30000/1001, h264 High, yuv420p, BT.709 on all three tags, tv range, progressive, 1714 frames, 57.190467 s (under 59.00), AAC LC 48 kHz stereo.
  Section 2 audio: packet md5 of a:0 is e70729ca074f2d559b7f4f7ef408985a on the square and on the approved 9:16. Bit identical. Measured -14.2 LUFS integrated, LRA 3.3 LU, true peak -2.1 dB. No level jump at any picture seam (20 ms RMS either side of 92, 490, 570, 607, 695, 957, 1079, 1098, 1191 differs only as speech does). No added sound effects are possible in an identical stream.
  Section 3 beat map: every beat starts and ends on its stated frame (cut list above). All cuts are hard cuts. Cards by eye at 0, 61, 120, 175, 239, 258, 277, 320, 368, 745, 800, 870, 956, 1098, 1150, 1190, 1657, 1713 are the right card for each beat.
  Captions: caption masks compared on all 1714 frames of both files. Text shape and highlighted word match on every frame (zero mismatches). 195 change frames in each file; the only four differences in the automatic list (607, 745, 502, 554) are background changes in the band, not text changes. First caption frame 5, last 1655, in both. All 32 caption states of the first 10 s and 48 more spread over the rest were read side by side against the 9:16 (`cap_first10.jpg`, `cap_rest.jpg`): identical words and highlight. My own transcript of the delivered audio (Whisper medium.en) matches the burned words for the first 30 s word for word. One centred line, text about y 900 to 965. No caption on the end card.
  Framing on the two new shots and the three changed holds (person mask and face box on every frame): hair top is 46 to 62 px below the top edge on 570-606, 48 to 83 on 1079-1097, 46 to 69 on 607-694, 39 to 89 on 695-744, 42 to 71 on 957-1078. Lowest value anywhere in the film is 37 px. Face box stays inside 32.9 to 65.4 % (570-606), 34.5 to 65.7 % (1079-1097), 34.5 to 70.9 % (607-694), 33.3 to 67.4 % (695-744), 34.4 to 68.8 % (957-1078); whole film 27.3 to 72.2 % (limit 8 to 92). Background drift inside every hold is under 0.75 px, so each hold has a fixed centre with no pan or tracking. Two levels only. Framing height matches the 9:16 where the level is unchanged (face width ratio 0.55 to 0.59) and differs only on the holds the ruling swapped.
  Chips: AI-GENERATED on ai_hook, ai_gen, ai_again, the stats card and the end card; "Real picture of me - not AI-generated" (hyphen) on all three afters; none on the BEFORE card or macro card, per plan. Every chip sits on the dark field above its picture (chip bottom y 131 to 136, picture top y 148 or lower), so it cannot touch face, hair or abs. All fully readable and inside the frame.
  Cards: flat dark field, no blurred backing, pictures end above the caption band. One physique picture per frame; order is before (152-202), Dan FAR (203-229), then the three afters. No side-by-side. BEFORE keeps the belly and belly button. The afters and the AI image keep the whole head and the shorts line. Before and after are the same person.
  Analysis card 745-956: moving on every frame (scan line, then BODY FAT, FAT TO LOSE, MUSCLE TO GAIN bars and the YOUR WORKOUT PLAN band build in; one near-still frame only). Bars carry no printed numbers. End card: moving on every frame (slow push on the picture), never blank.
  Macro card 1098-1190: same content as the 9:16 at the same frames, larger, stable.
  Safe area: no text-like pixels below y 985 on any sampled frame (every third frame). End card bar sits at about y 775 to 900.
  No black frame (darkest frame mean luma is above 12 everywhere), no run of 4 or more identical frames. First frame is the AI card with its chip; last frame is the end card.
  No banned screens, no drug names, no email screen, no side-by-side app screen.
  Stamps: `audio_gate.json` sha256 matches the file, gate_version 2.0.0 is current, PASS, and my loudness and peak agree. `labelcheck.json` sha256 matches. `audio_identity.json` hashes match what I measured.

VIEWER OPINION ON THE TWO SHORT NEAR SHOTS:
  570-606 (37 frames, 1.23 s): reads as a deliberate push-in. It lands exactly on "tap the button below" with the pill coming up, which is where an editor would punch in. Good.
  1079-1097 (19 frames, 0.63 s): reads as a zoom cut into the card, not as a mistake, because it starts on a new sentence and his mouth opens on the cut. It is quick. Acceptable; see M1.

COULD NOT VERIFY:
  Real-time playback and listening by ear: I stepped frames, measured and transcribed. How M1 feels at speed is a judgement from stills.
  Phone-size legibility: judged from full-resolution frames.
  The deliver gate rows (banned-screen scan, watch pass): no stamp yet and I do not run gates.
  Which photo files the cards were built from: checked by eye against the 9:16, not by file hash.
  Chip clearance was verified by geometry (chip on the field above the picture), not by a person mask on the card frames.
```
