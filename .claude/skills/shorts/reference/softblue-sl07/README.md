# `softblue-sl07/`: SL-07 If I Had Belly Fat shorts (round 1, 2026-10-12)

The Soft Blue shorts batch renderer from `softblue-sl03/`, carried through SL-06 (pickups, rebuilt film graphics) and adapted
to a long-form built with the RO-16 recipe. Work folder: `/Volumes/Extreme/_edit_work/sl07/` (run from there; these are copies
kept in git). Read `softblue-sl03/README.md` first: every lesson there still binds.

```
snap.py A0 A1 ...         silences on the film's dry voice + words + film joins around each planned cut
batch.py audio S..        cut the film's approved mix (15 ms de-click fades) + his_mix.wav (the gate's reference)
batch.py words S..        CTC alignment of plans.TEXT -> words.json, cues.json
batch.py plan S..         the shot table (run again after track when a shot uses auto holds)
batch.py track S..        Vision face box + person mask at 6 fps per talking shot
batch.py gfx S..          HyperFrames key-point bars, cached by config hash
batch.py proof S..        in / mid / out still of every shot and every bar settled
batch.py render S..       the short + source_picture.mp4
export_stills.py S..      round-1 stills (one per title, crop level, clip, graphic and bar) + items_<S>.json
page_r1.py                the round-1 page from notes_r1.py (review_server.py 8874 round1)
pickup.py asr|fit|make    Dan's recorded opening line fitted to the film's voice (a desk take is a PLACEHOLDER: see round 2)
watch_lines.py            waits for Dan to read the pickup lines while rec_mic records, then stops the recorder
gen_motion.py ID TAG S    Veo 3.1 Fast motion from an approved frame pair (decisions.json hashes), 9:16, ledger
chipplace.py S..          where the AI-GENERATED chip fits on each AI clip without touching a person (person mask, 8 frames)
scan.py S..               frame-by-frame: planned cuts against big picture changes, frozen frames, a strip of every cut
remux.sh S NAME           swap the audio of a rendered short without re-rendering the picture (frame count asserted)
deliver.py copy|plan S..  delivery copy, audio gate --verbatim, REVIEW 540p, transcript diff, gate plan
page_r2.py                the round-2 page (all five finished) from notes_r2.py
```

## What is different from SL-03 and SL-06

- **The film's map is `shots.json`, not `timeline.json`.** RO-16's recipe writes `shots.json` (raw frame range and film frame
  range per shot, after the round 2 and 3 pause trims). `piece_map.json` beside it is stale by 1.7 s. `batch.A_pieces` reads
  `shots.json`; master audio against the lav through it measured 0.0 ms at 9 points. Check that before trusting any map.
- **No music bed in this film** (pauses 36 dB under speech in the master), so `pickup.py` lays nothing under the pickup.
- **A short builds with or without its pickup.** While `pickups/<S>.PLACEHOLDER` exists, `batch.head` is 0, `batch.text` drops
  the pickup's caption piece and the opening cover ends at its `nohead` time. Delete the placeholder when `pickup.py make`
  has written the real wav, then run audio, words, plan, gfx, render again.
- **`fit="span"`** (plans cover): a card as tall as a clip's sideways travel allows (`span=(a, b)` columns of a 16:9 clip, full
  height). Used for the ab wheel and the toe touch, where Dan travels about 1,400 px sideways.
- **A key point's second line is searched after its first** (`bar_times`): "for 90 days" was found 20 s earlier in short A and
  gave a bar a negative length. HyperFrames then fails its check with "Timeline did not advance under seek".
- **Bars wrap at about 26 letters a line.** `gfx` asserts two lines; print `V.lt_scenes(...)[1]["lines"]` for every bar first.

## What round 1 learned

- **Record with `_shared/audio/rec_mic.swift`.** `ffmpeg -f avfoundation` dropped 11 % of the Yeti's audio in three takes of
  three (VIDEO-RULES, "A Short opens like a dedicated video"). Dan had four sessions open and did not read the lines for
  50 minutes: leave the recorder and `watch_lines.py` running and keep building.
- **Never wait on `pgrep -f "<text>"` from a shell whose own command line contains that text.** Two wait loops matched each
  other and stalled the build for 10 minutes. Wait on a file the job writes.
- **Measure a clip's sideways travel on a gridded strip before choosing its crop.** Reading it off a contact sheet put the ab
  wheel in the wrong half of the frame twice.
- **The handoff's "last word sits on a film join" risks were checked against the raw lav**, not assumed: each last word had
  finished (level under -55 dB) before the film's audio departs from the lav, so no ending moved.
- **Library `B0376` is the same file as RO-16's scale stock `p7555158`.** A "different scale shot" has to be a different file.

## Round 2 (2026-10-13): what the build and eight independent reviews taught

Five first reviews all said DOES NOT SHIP. Every item below was a finding; the tools now do the right thing by default.

- **A desk-mic pickup is a labelled placeholder (VIDEO-RULES 2026-10-13).** `plans.PICKUP[S]["placeholder"]=True` burns a
  small PLACEHOLDER AUDIO tag while it plays and `deliver.dname` adds "PLACEHOLDER PICKUP" to the file name. Two rounds of
  tone matching (six-take fit, then a per-take fit plus narrow corrections, `stage2.py`) got the gate's tone error under
  1.2 dB and a blind listener still picked the pickup out in a third to a half of tries. Do not repeat that work.
- **The audio gate cannot judge a pickup.** `--verbatim` compares against `his_mix.wav`, which already contains it.
- **A blind listener flags ANY edit.** The control clip that spans one of the film's own takes was called "a pickup" in 6 of
  13 tries. Always include that control, or a result reads as worse than it is.
- **The AI-GENERATED chip:** `softblue.disclosure` at its default size 23. Passing `size=30` (inherited from SL-06) put the
  lettering on the bottom edge of a 505 px chip that covered hair and ran off the frame, while the gate plan declared
  280 x 60. `deliver.py` now declares the chip's real box. Place it with `chipplace.py`; u=1.6 (326 x 65) fits beside any head.
- **Listen to where a short ends, against the raw lav, to 10 ms.** "sacrifice" lost its final s because a low-level
  fricative (-43 dB) after the vowel was read as a breath. A reviewer comparing against the film caught it.
- **A key point is read while it builds.** "Stop Weighing Yourself And" stood alone for 1.5 s and said the opposite of the
  short. Read line 1 on its own; give line 2 at least 1.5 s after it lands; print `lt_scenes` on line 1 alone to catch a
  part that wraps (a 30-letter first part left "It" hanging on line 2).
- **Old AI clips fail today's sense rule.** The film's approved busy-dad clip turns a carafe into a moka pot; in a tall crop
  it also lost the kids, so the words had no picture. Real stock replaced it. Check a library AI clip like a new one.
- **A phone recording is checked on EVERY frame.** Found, in order: the recording's own bezel as black wedges; a 2 px
  bezel line; a black camera view as a box in a white display (`darkfill`: the whole phone screen goes black); the
  recording's closing animation as a black block (`skip=[(a, b)]` jumps over it); a page animation at the end flashing at
  the corners (move the window). `round=N` fills each corner wedge with the page colour beside it, per frame.
- **Cards over an empty field read as unfinished to every reviewer.** Prefer a clip that fills the frame (Dan's curls and
  jump rope; the overhead scale) to a card (toe touch, side-view scale), unless the action truly needs the width.
- **Brighten Dan's overcast pool rolls** (`BRIGHT`): skin 77 against the presenter's 94 before.
- **Steady windows centre on his median position**, not the middle of his travel (an opening shot sat 58 to 123 px right).
- **Captions end on the cut** when they would linger a few frames past it; a caption never joins two sentences.
- **Give each reviewer a private scratch folder.** Five in parallel shared one and one of them decoded another's frames.
- **`watch.py` writes beside the video unless told otherwise:** pass `--out` and `--log` per short, or five runs overwrite
  each other in the delivery folder.
- **The delivery gate waits while two other builds run** and may never start on a busy afternoon; a stale gate process also
  counts as a build for other sessions. Kill a gate whose file has been re-rendered.
- **Count the B-roll share BEFORE the first render.** The gate's `style:coverage` row wants 30% of a short's runtime off
  the presenter, and it counts clips, scenes and phone demos only: key-point bars over Dan count for nothing. Two shorts
  here passed three independent reviews and then failed the gate at 10% and 21%, because the parent film has almost no
  B-roll over those passages and the shorts inherited that. Sum the non-talk rows of `build/<S>/shots.json` at the plan
  step; under about 33%, add library clips to the stills page in round 1, not after the reviews.
- **What `deliver.py plan` must hand the gate** (each cost a 6 to 8 minute run to find): `banned_source` and
  `banned_times` (else `compliance:banned_screen` is not measured), BOTH `label_chips.ai` and `label_chips.real` when a
  short has an AI clip (the row checks the AI label is there and the real-photo label is not, so it needs both images),
  and a `negative_events_scan` line that is true at the moment it is written (it reads the watch log now).
- **Run the gate only through `rungate.sh`**: started from a shell line that itself contains "gate.py", the gate counts
  its own launcher as a build and waits on itself.
- **The caption reference file rounded badly** (32.9997 s wrote 32,000): fixed here and in `softblue-sl03/deliver.py`.
- **The review server shows a cached copy.** After `page_r2.py`, run `review_server.py 8874 <dir>` again or the page Dan
  opens is the old one.
- **`batch.chip_png` drew the gate's label reference with dark letters** (an int16 overflow), so `compliance:labels`
  read -0.18 on a short whose label was on screen and correct. Fixed here and in `softblue-sl06/batch.py`. Before a
  30-minute gate run, measure the reference against the delivered frame yourself: crop the frame at the insert's `pos`,
  grey both, correlate (the gate's own method, `checks/compliance.py` `labels`). 0.99 is right; under 0.85 fails.

## Round 3 (2026-10-16): the studio pickups, the B-roll share, and what the checks caught

- **A lav pickup from another set is measured before it is treated.** The plan was the film's own voice EQ (RO-16 round 3
  `voice_chain.json` `eq`) on the 10/15 green-screen takes (roll C1722). Measured band by band against the film line after
  it (`r3probe/bands.py` in the work folder: speech frames, dB relative to the total), the film EQ moved both takes FURTHER
  from the film: the green-screen lav already reads fuller and much brighter on s sounds, and the film EQ adds bass and top.
  Two independent reviewers flagged it. `pickup.py make --eq-json` takes any fit file; a band-by-band match from the raw take
  (shrink 0.8, cap 9 dB, plus `deesser=i=0.35`) measured 0.7 to 1.8 dB off instead of 5.5 to 6.2.
- **The blind listener is noisy; use enough tries and the controls.** 6 to 8 tries a version, Gemini 3.1 Pro (2.5 Pro is gone).
  It preferred the matched version on one take and the film-EQ version on the other, and called a half-way version worse than
  both. Ship the better one per take, and give Dan both on the page: the call is his ear.
- **No hole at the pickup join:** `plans.PICKUP[S]["xfade"]` crossfades the pickup's last 60 ms into the film's own audio from
  just before its first piece, which then runs on with no 15 ms fade-in (`batch.cmd_audio`). Two fades meeting left a 20 ms dip
  to -82 dB that a listener heard as a tick.
- **Check library AI clips like new ones, and before choosing them.** A0083 and A0086 (a lean man eating) carry a white-and-black
  outline on every edge, invisible in the contact sheet, obvious when a vertical enlarges them 1.8x. Frame-reviewer FAIL.
- **An approved AI take can fail on what it shows.** AI_B1 (the metronome scale): the model interpolated START to END, so the
  needle made one 180-degree sweep (reads as weight gain) and stretched. The man and room were still, so `r3_needle.py` keeps the
  take and redraws only the dial: a needle-free plate (left half of one frame, right half of another), a drawn needle swinging
  +-24 degrees every 1.3 s in the dial's perspective. Motion gate and a fresh reviewer passed it. AI_B2a changed the man's hair
  texture mid-shot: dropped, the candles shot carries the whole line.
- **Run `clipcheck.py` and a fresh `frame-reviewer` on every AI clip a page will show, old ones included** (`r3_clipcheck.py`,
  `r3_fr_brief.py`). Three of seven failed here; all three had passed earlier reviews that were asked about other things.
- **Captions break at a picture cut** that falls in a gap between words, and the cue after it starts on the cut
  (`batch.cmd_cues`: `cuts`). The "never open a cue on a word the cue before says" rule had pulled a word across a cut.
- **B0031 (curls) has a rest with both arms down about every 2 s.** Start at t=0.0 and the clip ends mid-rep; at t=1.0 a
  4 s window ended on him standing still. B0073 freezes from 3.67 s; past 3.0 s the dad walks out of frame.
- **Shell traps that cost an hour:** `sed -i` on a log another process appends to replaces the file, and that process keeps
  writing to the deleted one (wait on a PID instead: `r3_post.py ... pid=N`). `pgrep -f "text"` inside `sh -c '...text...'`
  matches itself.
- **The Extreme drive filled (0 bytes free) mid-round.** Put frame dumps in the session scratchpad on the internal disk.
