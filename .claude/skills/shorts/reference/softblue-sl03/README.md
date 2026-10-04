# `softblue-sl03/`: the first Soft Blue Light shorts batch (SL-03 Daily Salad, round 1, 2026-10-02)

Round-1 tooling only (stills and the review page). The batch renderer is round 2's job. Work folder:
`/Volumes/Extreme/_edit_work/sl03/` (run from there; these are copies kept in git).

- `snap.py`: silences on the long-form's dry voice track (`voice_raw.wav`, no music bed), 10 ms RMS, 26 dB under speech
  p90. `segments.json`: the six shorts' cut points and why each moved.
- `hair/measure.py NAME ROLL T0 T1`: person-mask top and face box every 0.25 s on a RAW roll.
- `lib.py`: graded raw-frame grabs (the long-form's own lut chain), the Soft Blue title band (y 0 to 310), caption mock, wordmark.
- `lt.py`: a 9:16 HyperFrames lower third as a still on a real frame (content + glass mask snapshots, `composite.glass`).
- `stills.py`, `page.py`: the round-1 stills and page (`review_server.py 8809 round1`).

## Round 2: the batch renderer (2026-10-02). Start here for the next Soft Blue shorts batch from our own long-form

Everything a batch decides is data in `plans.py` (pieces, pause trims, B-roll covers, size-step splits, per-shot windows,
key-point bars as phrases, caption text as spoken). `batch.py` does the rest, run from `/Volumes/Extreme/_edit_work/sl03`:

```
batch.py audio S..    cut the long-form's approved mix (15 ms de-click fades) + his_mix.wav (no fades, the gate's reference); prints the bed level at each join
batch.py words S..    CTC forced alignment (WAV2VEC2) of plans.TEXT on the cut audio -> words.json, then cues.json
batch.py plan S..     shot table: one shot per continuous run of a roll (the long-form's audio map), covers, SPLIT size steps
batch.py track S..    Vision face box + person mask at 6 fps per shot (cached by roll + range)
batch.py gfx S..      HyperFrames lower thirds (content + glass mask), cached by config hash; asserts two lines and the 68,1130-1012,1378 box
batch.py proof S..    still of every shot's in / mid / out and every bar settled: look at these before rendering
batch.py render S..   the short + source_picture.mp4 (no graphics, for the watch pass)
deliver.py copy S..   delivery copy, audio_gate --verbatim, REVIEW 540p, Whisper of the delivered file (caption diff), gate plan
page_r2.py            the one review page for the batch (review_server.py 8811 r2/review)
```

What round 2 learned (all measured on this batch):
- **Ear-check every piece opening IN CONTEXT with Whisper word times, not the long-form's word list.** Short 2's opening
  "But" sat 65.69-65.75, after the silence round 1 trusted; cut at 65.77. Short 5's "And the option" is real (keep it in the
  caption), while a leading "And" heard elsewhere was not. Splice the previous piece on, transcribe, then read the envelope.
- **Our own long-form's joins are the cleanest cut points** (short 4 opens 20 ms inside one, piece 3 of short 4 drops a
  dangling "Number one," at one).
- **Shots follow the audio map, so lip sync is the roll's own.** A continuous take split across two audio pieces is one shot
  (key on raw minus film offset), or the proof shows a false cut.
- **Pauses over the gate's 1.0 s dead-air bound** (the olive-oil pour, the app typing) are cut to 0.9 s and the PICTURE plays
  faster across them: no jump cut, nothing lost.
- **The music bed in the mix sits at -30 to -50 dB at every join** (bed.wav is on the same clock); 15 ms dips were enough.
- **Close-ups need a tight deadband**: a face 510 px wide in a 724 window cannot wander 94 px. `window_path` sets the
  deadband from the face width. A shot where he shows something to the lens (the olive oil bottle) gets `keys`.
- **The phone beside Dan only works when his face fits the 399 px source window.** Extreme close-ups in the demo (dictating
  the note, reading the AI's questions) use the phone alone, centred, same 1.2x size.
- **A bar never crosses a piece join** (`bar_times` clamps to the next join): a key point about one passage must not ride
  into the next one.
- **The field drifts** (keyframes every 0.5 s, blended): a static field under a static phone reads as a frozen frame and the
  watch pass counts it.

### What the independent reviews taught (eight review passes, 2026-10-02/03)

Every one of these was a "DOES NOT SHIP" before it was fixed. The planner in `batch.py` now does them by default.

- **Steady crops first; a deadband follow reads as panning.** `plan_holds` (set `auto=True` on a talking shot) splits one
  continuous take into steady holds that alternate the two sizes, and at each in-take cut his face keeps its on-screen
  position (a size step with a sideways slide is a jump). Where he walks so far that no steady crop holds his face, the
  hold becomes a smooth follow that eases in from where his face was and eases into the steady crop that follows, with no
  cut (`seamless`). `deliver.py` declares a seamless pair as one framing segment.
- **Extreme close-ups (head 680+ px in the 724 window) follow his HEAD, not his face box** (`head=True`): the Vision face
  box stops short of his ears, so a face-centred crop clips an ear with room on the other side. `cmd_track` records the
  person mask's extent at eye level (`hx0`/`hx1`).
- **A same-camera join needs a displayed face change of about 1.25x or a cutaway**, measured on the frames either side
  (`track.json` face width times the window scale), not from the window names. A lean-in can cancel a size step.
- **A cutaway must be steady and have no talking face.** Two were rejected: one ended on a handheld tilt, one showed his
  mouth moving over silence. Check the raw range frame by frame, and never use the same B-roll shot twice in a short.
- **A camera whip inside a take is covered, not followed** (short 4: two whips to and from the olive oil bottle).
- **`round()` is half-to-even**: on a take whose raw offset lands on .5 of a frame it repeats one source frame. Frame
  indices use `floor(x + 0.25)`.
- **A pause trim that skips picture needs a cutaway nobody could find; keep the pour as a teaching pause** (declare
  `junk:dead_air` with the reason) rather than play it past about 1.7x.
- **Captions under the phone need 20 px to the phone's real outline** (y1612, not y1600), and the wordmark sits at y1850
  for the whole of a phone short.
- **A key point never crosses a piece join, and its second line lands within about 0.2 s of its words.**

Gate plumbing (`deliver.py`): `speech_words` is ONE word per caption cue (its first), `verbatim_source_ctc` evidence;
framing levels come from measured face size at each boundary; the negative-events scan is written per render; rows that
measure Dan's approved choices (hair at row 0, the full crop level, B-roll coverage, captions under the phone, the side
panel) are declared per short in `gate/declare.json` with his words and the decision hashes. Run the gate through
`rungate.sh`: `speech.wait_for_build_slot` counts any process whose command line contains `gate.py`, including the shell
that launched it and any watcher that greps for it.

## Round 3 (2026-10-04): revising two shorts after Dan's review. Read before changing any piece list

Dan approved four of six and asked for a new opening on one short and new closing content on another. It took four
renders and four review passes, and every block came from the NEW material. What that taught:

- **The long-form mix trims the tail of the last word at every one of its own audio joins** (its edit cuts to the next
  take and the next sentence covers the missing tail). The short's audio is that mix, cut only, so the tail does not
  exist. A word that sits at a long-form join ("cheaper" at film 97.76, "spices" 570.94, "tablespoons" 560.09,
  "dressing" 172.02) may only be used as a run-on: the next piece must start within about 0.1 s, as the long-form plays
  it. **Never end a short on one, and never leave one before a pause.** Pick the last line from sentences that end
  before a natural pause INSIDE one take: list sentences whose end is more than 0.3 s from every `timeline.json` "A"
  boundary and is followed by a measured silence of 0.2 s or more. The audio gate cannot see this (its reference has
  the same trimmed word); Whisper prints it as a shortened word ("spice", "dress", "cheap").
- **Check every candidate cutaway frame by frame before planning it, for motion AND focus.** Handheld B-roll here is
  steady for one to three seconds at a time. Per-frame phase correlation on a 480 px copy finds camera moves, but it
  reads a shot as steady when hands or a lid fill the frame, so also look at tiles 0.4 s apart with a grid. Variance of
  the Laplacian on the crop finds soft focus (the dressed-bowl shot C1548 is soft until 101.9). A cutaway that needs
  more steady footage than the roll has is the wrong cutaway: shorten the audio piece, or use another picture.
- **Two close-ups of him from the same camera need a cutaway between them**; the two windows only give 1.2x.
- **A take the long-form's audio map steps back by a few ms** (C1548 at film 524.07, 20 ms) repeated one source frame.
  `cmd_plan` now carries the step forward inside the shot, and `Short.fidx` moves the frame-index rounding off a
  boundary. Check `np.diff` of the frame indices of every talking shot before rendering.
- `style:coverage` (30 % of runtime off the main scene's palette) fails when a revision removes a B-roll passage. Add
  steady cutaways from the shoot; a second take in a different spot and an extreme close-up both count as off-palette.
- The round 3 page is `page_r3.py` (two shorts as questions, the approved four as a record line).
- ⚠ `batch.py plan` with no short named, or naming an approved short, rewrites its `shots.json`. Name the shorts.

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
