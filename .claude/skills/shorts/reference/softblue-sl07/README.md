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
