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
pickup.py asr|fit|make    Dan's recorded opening line fitted to the film's voice
watch_lines.py            waits for Dan to read the pickup lines while rec_mic records, then stops the recorder
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
