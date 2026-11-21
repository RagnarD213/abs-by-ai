# Ad 10 square cutdown (1x1 59s), round 1 independent review

File reviewed: `my dad bod at 38 my dad bod at 40 | claude | 1x1 59s | ad 10.mp4`
sha256 `b58968c8f5bb0d845cb7bf83b560a1c95fe062f7528656fec43dce15e11e367d`, 45,898,040 bytes.
Reviewer: independent ra-reviewer, 2026-10-04. Builder notes, editor round files and recipe-square were not read.

## VERDICT: DOES NOT SHIP

One blocker: section 3 opens on a third of a second of a frozen AI man who is not Dan, straight after "this is
where I'm at today" over Dan's real flex photo. The approved vertical cutdown does not show him there.

## Findings

1. **0:48.01 to 0:48.35 (cut frames 1439 to 1448). BLOCKER.** Section 3 opens on 10 frames of the AI-GENERATED beach
   card (a different man, not Dan), frozen (frame to frame difference 0.04 to 0.07 on a 270 px scale, so no motion),
   then hard-cuts to the phone app demo at 0:48.35. The previous frame (1438) is Dan's real flex photo under "this is
   where I'm at today", so a viewer sees Dan's result and then a stranger for a third of a second in the silent gap
   before "So generate...". The approved vertical cutdown shows something else at the same frames 1439 to 1448: the empty
   card with the phone fading in (no beach man). Cause, measured on the full files: in the full vertical the beach clip
   moves until frame 5169 and the card-out transition starts at 5170. In the full square the beach clip stops moving at
   frame 5160 and holds a frozen frame to 5179, then cuts to the phone at 5180. So the square changed this beat's
   timing, and the cut plan's section 3 start (5170) now lands inside the frozen tail. The brief's "same cuts" holds for
   every cut time (the cut lists of the two cutdowns match frame for frame), but not for the picture at this beat.
   Fix: reproduce the vertical's card-out at 5170 to 5179 in the square (or start section 3 at 5180 and keep the audio
   untouched), then re-prove the seam. The full square carries the frozen tail too (2:52.5 to 2:53.0), see item 9.

2. **0:30.16 to 0:33.03 (cut frames 904 to 990; full square 2707 to 2793). SHOULD FIX.** The push on the full-bleed
   AI pool goal picture advances only every other frame: the frame difference alternates strictly between about 1.87
   and 0.03 for three seconds, which is a 15 fps judder on a full-screen still. The approved vertical moves on every
   frame here (2.1 to 2.3 per frame, no zero frames). This is new in the square, not inherited.

3. **0:21.86 to 0:22.89 (frames 655 to 685). SHOULD FIX, inherited.** He says "how did I get my abs back at 40?" and
   the caption group ends on "back at" with "at" lit through the word "40" (speech onset 22.44 s measured on the audio
   envelope). "40?" is never on screen. The approved 9:16 cutdown has the identical omission (checked at the same
   frames). It is the hook's punchline number, so it is worth fixing in the caption layer even though Dan approved it.

4. **0:00.00 to 0:03.10 (frames 0 to 93). NIT, inherited from the approved first minute.** The push on the before
   card moves on roughly two of every three frames (differences 0.4 to 0.6, then 0.04 to 0.1). Small and slow, so
   barely visible; the first-minute file Dan approved on 10-03 shows the same pattern. The vertical moves every frame.

5. **Label wording. NIT.** The ad uses two wordings of the real-picture label: "Real picture of me - not AI-generated"
   on the cards and the app demo (0:00, 0:09.1, 0:48.35 to 0:52.2) and "Real picture of me. Not AI-generated." on the
   full-bleed photos (0:08.1 to 0:09.1, 0:27.1 to 0:30.1, 0:46.0 to 0:48.0). The vertical uses one wording throughout.
   Dan approved the first minute with this, so not a blocker, but one wording reads more deliberate.

6. **Encode. NIT.** Video stream 6.10 Mbps (container 6.43). The square shared rules
   (`Handoffs/handoff-20260911-square-ads-00-shared-rules.md` line 25) ask for 8 to 12 Mbps. No visible blocking at full
   resolution on the busiest frames I checked (tree bokeh at 0:08.8, pool tiles at 0:30.1).

7. **0:08.78 to 0:09.10 and 0:28.63 to 0:30.06, the hands-on-hips real photo. NIT.** Hair top sits about 15 px below
   the frame top. Not cut, but tighter than the other photos (35 to 70 px) and than the vertical's crop of the same
   picture.

8. **0:00.00 to 0:03.10, opening before picture. INFO (checked under the 2026-10-04 belly rule).** The standard
   seated sunglasses before photo, head to navel, in a card. No hands on the body, no pinch, no crop centred on the
   belly. I found no violation; recorded because the rule asks the reviewer to check every picture in the first 30 s.

9. **Full square, 2:52.45 to 2:53.03 (full frames 5161 to 5179). INFO, outside this file.** The beach clip freezes for
   19 frames and the vertical's card-out transition is missing. Harmless in the full film's flow, but it is the source
   of item 1 and the fix belongs there.

10. **Inherited caption gaps. INFO.** No captions over cards and full-bleed photos, so "This is my dad bod at 38"
    (0:00 to 0:02.5), "And this is my dad bod at 40" (0:07.7 to 0:10.5) and "But to actually get real abs in real life"
    (0:26.8 to 0:29.9) are uncaptioned. Same in the approved vertical cutdown; recorded only.

## What I checked

- **Container:** 1080x1080, H.264 High, yuv420p, BT.709 tagged (tv range), 30000/1001, 1,712 frames, 57.124 s video
  and audio, AAC LC 48 kHz stereo about 318 kb/s. Under 0:59.
- **Audio:** packet md5 of `-map 0:a -c copy -f md5` equals the approved 9x16 59s file's (`ca5d023f23582b7773c95f9d5668bb75`
  both), and the framemd5 lists (timestamps included) match. ebur128: -13.6 LUFS integrated, LRA 3.2 LU, true peak
  -1.0 dBTP. Audio against the full square at the mapped times: correlation 0.9999 / 0.9998 / 0.99999 at lag 0 for the
  three sections. Both section seams (30.063 s, 48.015 s) fall in gaps at -34 to -40 dB; no click (second-difference
  peak within the file's own p99.99). The one 5 ms bump at 48.03 s is present at the same place in the full square, so
  it is source content, not the join. I measured the audio; I could not listen with ears.
- **Seam proof against the full square:** every cut frame k compared at full resolution with full frame (0..900,
  2704..3241, 5170..5442). Mean absolute difference 0.0 to 1.0 on all frames, no frame where a neighbouring full frame
  matches better, except frames 1439 to 1443, which differ only in the caption band area: the full square still prints
  "years younger." there and the cutdown does not (expected, captions). Pictures otherwise equal.
- **Viewer pass:** a full-resolution frame every 8 frames (214 frames, about 100 of them talking head), every picture
  cut as n-2, n-1, n, n+1 at full size (30 cuts), the first and last three frames, the opening of section 3 frame by
  frame (1437 to 1449), the studio photo 1378 to 1392, the caption "40" window, and the same frames of the vertical
  cutdown and both full files where a question came up. No black or blank frames, no one-frame glitches at card edges,
  no wrong or doubled labels, no label on face or abs, no em dash on screen, no banned screen (app demo is single-phone,
  same person before and after: Dan's sunglasses photo to his AI pool goal), no side-by-side.
- **Edges:** every frame's outer 2 rows and columns against the next 4: 62 flags, all smooth content gradients (door
  frame, pool wall) on inspection, no thin lines.
- **Camera:** background-only phase correlation and a column-profile check on every talking-head hold. Holds mostly
  still (0 to 1 px per frame); two eased follows at 0:14.2 to 0:14.7 (peak 8 px per frame, about 240 px/s, ramping up
  and down) and 0:17.3 to 0:17.6 (5 px per frame). No one-frame sideways pop. Every cut lands with his head near centre.
- **Captions, first 30 s word for word:** the delivered audio transcribed with Whisper small, then each lit-word change
  (tracked per frame by the (104,197,255) highlight) checked against speech onsets on a 10 ms level envelope:
  "I was eating healthy / working out four times / a week and doing my / absolute best / same business same kid / same
  stress about two / years apart / So / how did I get my abs / back at / with abs" all match the words heard, onsets
  within about 0 to 100 ms. Missing word: "40?" (item 3).
- **Stamps:** `.deliver_gate.json` sha256 and bytes match the file, `gate_version` 2.4.0 equals `GATE_VERSION` in
  `_shared/deliver/gate.py`, verdict PASS. `.audio_gate.json` sha256 matches, gate 2.0.0 equals the current
  `audio_gate.py`, mode reference-verbatim, PASS. Note: both stamps passed a file carrying the item 1 blocker.
- **Standing rules:** same person before and after (yes), no side-by-side (yes), labels off face and abs (yes), no
  banned screens (yes), no printed numbers or unbelievable claims on screen (the "I Used AI To Get REAL ABS" bar is the
  approved wording), hair inside the frame on every talking-head frame I opened (35 to 70 px), length 0:57.1.

## What I could not verify

- Real-time playback with ears and eyes; motion and audio judgements above are from measurements and frame sequences.
- Whether the person holding the phone at 0:33.1 to 0:35.2 (face out of frame) is Dan; it is inherited from the
  approved vertical.
