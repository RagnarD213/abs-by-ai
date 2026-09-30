# RO-16 recipe (Claude, round method, 2026-09-30)

Single-roll organic long-form on the 9/23 studio set, reusing the WV-01 locked look (colour C, W2/T2, audio B).
Order: `edl.py` -> `shots.py` -> `assemble_audio.py` + medium.en ASR (`asr_assembled_medium.json`) -> `words_out.py` ->
`plan.py` -> `resolve.py` -> `stills.py` (every graphic/clip on its real frame) -> `build.py range <a> <b> <out>`.
Working copy and media: `/Volumes/Extreme/_edit_work/ro16/` (never commit media; the repo is public).

Traps learned here:
- Whisper small hid three restarts inside "long words" (a 4 s "in", a 2.5 s "it's"); re-transcribe every word > 0.6 s alone
  with medium.en (`verify_asr.py`) and run a medium.en pass on the assembled cut before placing graphics.
- A side card over a tight crop pushes the presenter's arm off frame: cards sit on the wide framing, with a W3 in-between
  size to alternate at joins that fall under a card.
- Full-screen items that start a few frames after a cut, or two full-screen items 0.1-0.6 s apart, flash the presenter
  for 4-8 frames: snap them (`resolve.py`).
- Room tone under joins must be level-matched to the outgoing room; a fixed quiet sample falls under voice_chain's gate.
  Natural pauses after the chain floor at -66 to -88 dB on this roll, so measure a join against those, not against speech.

## Round 2 traps (2026-09-30, full film; details in the delivery folder's notes-RO16.md)
- Scan every clip's first and last used frames for luma ramps before the render: a stock file can open on a fade from black.
- Run scene detection over every clip's used range: a library or export clip can carry its own internal cut.
- A card that spans a join takes its framing from the shot it exits into (`build.segments`); W4 is 1.27x W2. A 1.14x step read as a jump.
- A cutaway that starts on a join must cover the whole shot or leave at least 0.5 s of it; `resolve.py` now snaps both ends.
- The segment cache key has no crop values: a changed crop needs a new framing name.
- `finish.py` writes the SRT, chapters, label chips and the gate plan; `finish_chain.sh` runs audio gate, watch pass and `haircheck.py`.
