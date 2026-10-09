# RO-03 "The Vacuum: Workout Only" (8/14 poolside, C1624-C1629): round 1 recipe (Claude Opus 5.5, 2026-10-09)

CONTENT, long-form family (LFC). A 2:32 follow-along: three 20-second holds, 30 seconds of rest between (Dan's Shoot 4
outline: "go directly into the routine; 3 standing vacuum holds, 20-30 seconds each, 30 seconds rest between").
C1625 holds ONE filmed hold; it is shown three times. Work dir: `/Volumes/Extreme/_edit_work/ro03/`.

**The model is the workout sections of Muhammad's ab wheel cut, not Zeeshan's workout-only video** (Dan, 2026-10-09:
"Don't model it on Zeeshan's videos. He's not the best editor. Model it on Muhammad's workout videos."). Taken from
him: a label on screen through every set, one form cue per set, Dan talking between sets, a size change inside each
set, his silent flash into each set (`build.bloom_frame`, from RO-12), music up in the sets and almost out under the
voice. Not taken: his 3x fast-forward (a follow-along runs in real time), his olive graphics, his URL end pill.

Built on RO-02's recipe (`../ro02/`): same colour cubes, far / near framing, HyperFrames lower thirds, hard cuts.

Order: `edl.py` -> `shots.py` -> `measure.py` -> `skin.py` -> `frames.py` -> `assemble_audio.py` -> `asr_assembled.py`
-> `words_out.py` -> `resolve.py` (writes `plan_resolved.json` and `marks.json`: holds, beeps, flash frames) ->
`from_plan.py --render` -> `build.py framings` -> `build.py audio` (the whole film's mix, once) -> `stills.py` ->
`media.py first` -> `hair_first.py` -> `media.py context` -> `page.py`.

What is new against RO-02:
- `edl.py`: a piece may repeat a source range (set1 / set2 / set3). The rests are set to 30.0 s by moving set 2's and
  set 3's in point, never by trimming speech.
- `shots.py SETCUT`: pure reframe cuts inside each hold. `build.FORCE` gives every set shot its size.
- `frames.gamma`: the three sets share ONE exposure trim (per-shot trims made the same hold change brightness at its
  own reframe cut).
- `gfx.py`: `title_chip`, `work_chip` (RO-02's countdown chip plus a set line; states from `marks.json`). Chips paint
  over the opening clip too.
- `plan.py`: a time may be `("hold", n, seconds)`; `from_plan.py` takes a number in place of a phrase.
- `bed.py` + `build.film_audio`: the bed is built on the film timeline with a swell in each hold; the shared voice chain
  runs ONCE over the whole film and every review clip is a slice of that mix.

Traps this build paid for:
- **The voice chain sets loudness per file.** Run per review clip it made the first minute's speech 4.7 dB louder than
  the film's. Mix the film once, slice it.
- **Music-only stretches break the audio gate's voice rows.** Tone, processing damage and word endings read the holds
  as if they were a voice. Prove the voice by gating the talking sections alone (`speechcheck.py` cuts them out):
  PASS on every row. Report the whole-file rows as they read; do not tune.
- **Chasing -14 LUFS on a film with quiet music-only holds crushes the speech.** The holds drag the integrated number
  down, the chain adds gain (+5 dB), the limiter flattens the voice (spread 5.9 dB, tone max 2.58). Locked instead:
  target -14.5, the chain settles at +2.9 dB, speech alone reads -13.4, the film -15.3.
- **RO-02's fitted EQ failed tone on this subset of rolls** (80 Hz +3.5, 900 Hz -3.4). The fit is per film: run the
  chain without `--eq` on the film's own speech and keep that curve (`FIT.json`).
- **Whisper on an instrumental bed prints "All right." and "Thanks for watching!"** Re-run at shifted offsets: a real
  vocal stays at its source time, these moved with the window.
- **A lower third on the near framing of a side-on hold sits across his waist.** Form cues go on the far framing only.
- **One hair sample read 6 px where its neighbours read 48 and 80:** the mask joined the chimney behind his head.
  Look at the frames before changing a crop.
- zsh does not split `set -- $pair`; drive parameter sweeps from Python.
