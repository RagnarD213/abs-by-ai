# RO-03 "The Vacuum: Workout Only" (8/14 poolside, C1624-C1629): round 1 recipe (Claude Opus 5.5, 2026-10-09)

CONTENT, long-form family (LFC). A 2:32 follow-along: three 20-second holds, 30 seconds of rest between (Dan's Shoot 4
outline: "go directly into the routine; 3 standing vacuum holds, 20-30 seconds each, 30 seconds rest between").
C1625 holds the only hold filmed on this shoot; it is shown three times. Other holds exist on other shoots (8/28
C1677, 7/8 C1490) and are NOT used: Dan, 2026-10-10, "I just want to make sure we avoid mixing the two shoots. I feel
like that's going to look weird" (no sunglasses, different shorts and necklace, oiled skin, another background). Work dir: `/Volumes/Extreme/_edit_work/ro03/`.

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
- **"Only one take exists" was half right, and it took Dan asking to find out.** The job doc named one roll and I searched only that
  video's own rolls. The other holds were silent B-roll on a different shoot (8/28 C1677, 7/8 C1490): no words, so a
  transcript search cannot find them. Before telling Dan footage does not exist, search every shoot: the roll
  sidecars' On screen notes (`Media/footage-index`), `Docs/SHOOT_*_FOOTAGE_REPORT.md`, the clip library (`B0428`,
  `B0429` were cut from C1677) and the sibling job docs (RO-02's listed C1677 as extra B-roll). The sidecars' vision
  notes call almost any shirtless standing shot a "stomach vacuum", so confirm each hit on a contact sheet. Then show
  him a side-by-side still of the two shoots BEFORE planning around the other footage: he rejected the mix on sight.

## Round 2 (2026-10-10): the full film, the gates, the independent review

Order: re-hash `round2-plan/decisions.json` -> `build.render_range(0, total)` into `round2/` -> prove the first minute
against the approved file (PSNR per frame, PCM difference) -> `finish_chain.sh` (audio gate on the film, then on the
speech alone; `finish.py`: SRT, chapters, `plan.json`; watch pass; `../ro02/haircheck.py`; HyperFrames checks) ->
`sheet.py` + `validate.py --hash` -> one `ra-reviewer` (the watch judge and the review in one run) -> delivery gate ->
`deliver.sh` -> `page2.py` -> `review_server.py 8877 round2`.

What is new:
- `finish.py`: `srt_words.json` beside the master lists words to drop or retime, each with the level reading that
  justifies it. Cues are built sentence first, then split where the halves come out even (a comma preferred).
- `sheet.py`: the edit sheet for this build family (several rolls, a crop measured per shot, a cube per exposure
  trim, PIL chips). The shared writer reads single-roll builds and RO-06's layout only.
- `gfx.work_state`: the rest count is capped at the rest's own length.

Traps this round paid for:
- **A countdown rounded up shows one frame too many.** Rest 2 measures 30.016 s, so the chip read 31 for one frame.
  Sheets at one frame a second cannot show it. The reviewer found it by cropping the chip on every frame. Do that
  for any counter before the review.
- **The transcriber invents counting over a silent hold** ("One.", "Three, one.", "Three, two.") and times the first
  word of the next shot inside the hold. Read the lav level at each word before it goes in the SRT: speech reads -10
  to -20 dB here, the holds -45.
- **A word that straddles a join gets an end time from the wrong roll** (`fasting.` ended at 29.76 on a 51.94 start).
  Print every word whose end is missing, before its start, or past the next word.
- **The watch tool wants a verdict on every `pair_` image too** (61 images, not 34). Say so in the judge's brief.
- **Re-rendering one frame changes the encoder's output for the next few frames.** Three watch images differed from
  the judged render by noise (48.9 dB and up). Compare old and new renders per frame, send only the changed images
  to a fresh judge, and say "identical" only for frames that are.
- **A second judge without the plan flagged the flash's first white frame as a blank frame.** Give every judge the
  plan's line on the flash (one all-white frame, a dip, then the bloom: Muhammad's double pulse).
- **The delivery gate's lip-sync row samples five evenly spaced points.** Two fell inside music-only holds and read
  -31 and -3 ms at correlation near zero. Measure the talking sections by hand and report both.
- **"Each repeat changes size at a different moment" was true on paper only.** Set 3 (far to +11.5 s, then near) is
  set 1 (far to +10.0 s, then near) for 18.5 of 20 seconds. When one take is shown several times, lay the size
  schedules side by side on the hold's own clock and check no two sets match for long, and that they do not end on the
  same close picture.
