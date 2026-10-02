# `softblue-sl03/`: the first Soft Blue Light shorts batch (SL-03 Daily Salad, round 1, 2026-10-02)

Round-1 tooling only (stills and the review page). The batch renderer is round 2's job. Work folder:
`/Volumes/Extreme/_edit_work/sl03/` (run from there; these are copies kept in git).

- `snap.py`: silences on the long-form's dry voice track (`voice_raw.wav`, no music bed), 10 ms RMS, 26 dB under speech
  p90. `segments.json`: the six shorts' cut points and why each moved.
- `hair/measure.py NAME ROLL T0 T1`: person-mask top and face box every 0.25 s on a RAW roll.
- `lib.py`: graded raw-frame grabs (the long-form's own lut chain), the Soft Blue title band (y 0 to 310), caption mock, wordmark.
- `lt.py`: a 9:16 HyperFrames lower third as a still on a real frame (content + glass mask snapshots, `composite.glass`).
- `stills.py`, `page.py`: the round-1 stills and page (`review_server.py 8809 round1`).

## What round 1 learned

- **Our own long-form's `base.mp4` is not graphics-free.** RO-05's base has the title cards and the phone demo baked in.
  Cut from the RAW rolls through the long-form's `timeline.json` (roll, in, f0/f1) with its luts.
- **Under the 310 px title band the kit's lower-third position (bottom at 68 %) lands on Dan's chin** when a handheld
  camera pushes in: face bottom measured y1254 in the 1.2x window, y1097 in the full window. So: the full window while a
  bar is up, the strip moved down 72 px (bottom y1378), copy held to TWO lines, captions from y1412. Measure the face
  bottom over every bar's whole span, not on its still.
- **A handheld extreme close-up needs a following window** (face centre moved 878 to 1298 px in 1.7 s); every other
  shot is a fixed window per shot.
- **Phone demo in 9:16:** phone beside Dan (shell 1.2x, Dan in a 440 x 1190 window, captions on the field under both)
  read better than phone stacked over a wide strip of Dan. Dan's pick is recorded in the round-2 handoff.
