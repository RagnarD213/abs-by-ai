# `zeeshan-master/`: Shorts cut from an EDITOR'S finished 16:9 master (SL-04, 2026-09-24)

Built on `scored-source/`, for Zeeshan's "Arms & Shoulders Home Workout" (five shorts, all SHIPS on a fresh-reviewer
audit and GATE 2.3.0 PASS). Start here for any batch of shorts from Zeeshan's, Muhammad's or Waleed's finished cut.
Paths in `config.js` are absolute to the SL-04 master and the build ran in `/Volumes/Extreme/_edit_work/sl04/build/`.

## Run order

```
node ../whisper_words.js master16k.mp3 words.json        # Replicate, word timestamps (batch_size 8: 24 ran out of GPU memory)
python3 work/vad.py work/master48.wav work/gaps.json      # speech gaps under a music bed
python3 work/fixonsets.py                                # Whisper onsets/offsets out of measured silence
edit segments.js                                         # pieces: phrase anchors + explicit inAt/outAt inside gaps
python3 work/cuts.py                                     # FULL-RATE cut finder (the 320x180 scene detector missed his punch-ins)
python3 work/subject.py / work/gfxscan.py                # Vision masks per shot; when/where his pills and chips are up
python3 work/ctc_source.py                               # caption timing: CTC forced alignment of the source words
edit plan_shots.py                                       # every shot: full / mid / zoom window or inset card, WITH its reason
./build.sh A B ...                                       # plan -> assets -> render (chip names follow the plan)
./deliver_all.sh                                         # copy, audio_gate --verbatim, delivered ASR + CTC, gate plan
watch.py -> fresh-subagent judge -> watch.py --judge -> gate.py --format short
```

## What this batch learned (all measured)

- **His audio ships untouched**: map `0:a:0` stereo, cut only, 15 ms de-click fades, and encode AAC at **320k** (his
  bitrate). At 160k ffmpeg's AAC pushed his -1.1 dBTP to **+1.3 dBTP**; 256k was worse; 320k lands exactly on his.
  Gate with `audio_gate.py --reference-mix <his same cut, no fades> --verbatim` (`render.js` writes `his_mix.wav`).
- **Three windows, all from row 0** (his wides put the hair at source rows 0-12, so nothing above can be kept):
  full 724x1080 (1.49x), mid 604x900 (1.79x), zoom 530x790 (2.04x, excludes his lower-third band rows 804-907 whole).
  Never zoom a MEDIUM shot: rows 0-790 end at his hips and the caption band lands on his abs.
- **His graphics are whole or absent.** Lower thirds: zoom window or an inset card cropped x0.09-0.88 (holds every
  pill through its slide-in, measured x202-1623). Top-left chips (x up to 763): a window starting right of them, or
  a card. **Pills fade 0.5-0.8 s longer than any colour scan says**: end the card ~1 s after the scan (two reviewers
  caught sliced ghosts at a card exit).
- **A framing change must be a real size change.** Mid on a wide ~= full on his medium: the cut between them read as a
  jump (1.08x). Measure the step on the rendered frames; the fixed cut measured 1.28x.
- **His zoom-blur transitions sit at section boundaries.** Hold the last/first sharp frame over them (`holdTail` /
  `holdHead`, <= 7 frames so the watch pass does not call it frozen) while Dan is silent, or split the piece around
  the silence (short4).
- **Captions: Whisper onsets run 130-420 ms early** in continuous speech on his mix. `work/ctc_source.py` re-times
  them (median +153 ms), and the gate measures against a different pass: the DELIVERED file's ASR re-timed by CTC
  (`gate/ctc_delivered.py`). Give the gate one delivered word per caption chunk, matched in full-stream order
  (DS-17 method); matching chunk-first words alone lands "is"/"the" on the wrong occurrence.
- **Whisper stamps the last words before a music-only stretch with a bogus zero-length end-of-file time.** They are
  real words: re-time them after their predecessor (dropping them made the gate find speech with no words).
- Card the live-round slices (timer + exercise pill whole) with a J2 "EXERCISE n OF 3" chip; J2 chips go on the black
  field, never on him.
- Framing rows `hair_top` and `no_wide_level` are declared per build (his source framing); single-piece shorts
  declare `click_at_joins` / `splice_visibility`; a rep-cadence repeat in his approved cut declares
  `junk:repeated_take`. Every declaration carries its reason in `gate/<S>/declare.json`.

## Round 2 (2026-09-29): what Dan's notes taught

- **Measure the hair before promising a recrop.** `hair/measure.py` (Vision mask every 0.25 s) over every talking shot:
  on this shoot the CAMERA framed Dan's hair at source row 0 on most wides and mediums, and the 8/3 main-camera
  originals (C1582-C1587) have the same framing. No window can add rows above row 0; a card shows the same cut edge.
  Check the source (and the raw camera file) first, then pick context lines by their measured headroom.
- **SUPERSEDED 2026-10-01 (Dan): never crop a card's height to remove an editor's pill; show the whole frame, his pill whole inside it, our bar off for that shot. See VIDEO-RULES, "A horizontal clip inside a vertical or square frame is never cropped shorter".** The old recipe, for the record: **Replace an editor's pill by cropping, not covering.** Zeeshan's lower-third pills live in source rows 804-907 on
  every frame, entry and fade included. `cardCrop` y 0-0.739 (rows 0-798) removes his pill whole; our pill
  (`pill/make_pill.py`, his olive (77,86,49), text (230,237,216), measured padding) goes on the black field under the
  card with an alpha fade (`overlays.json` entries with `png`).
- **A still-image grade test under-reads saturation.** `grade/skin.py` on RGB stills predicted skin sat 0.75 for
  `eq=saturation=1.18`; the rendered file measured 0.79 (the YUV-RGB round trip inside `curves`). Always re-measure
  the rendered file, then trim. Short 1's final grade: `curves 0.25/0.155 0.5/0.335 0.75/0.56 1/0.84, eq sat 1.08`.
- **zsh does not word-split `${@:-A F C}`**: `deliver_all.sh` with no arguments ran one bogus id. Fixed with `set --`.
- **Title band frame is flush with the canvas edge** (`INSET = 0`), Dan 2026-09-25: the frame must share the video's edge.
- **Reviewer rounds this batch needed (2026-09-29): three.** Fixes that came from the fresh reviewers, all now plan
  options in `plan_shots.py` / `render.js`: `cw`/`ch` (a custom window, e.g. 536x800 to stay above his pill band),
  `slideFrom`/`slideDelay`/`slideFrames` (glide between two of our windows inside an editor's own zoom, instead of a
  one-frame sideways jump), `xKeys` (keyframed window when a demo's arm span is wider than the window), card `slow`
  (retime a card's last clean second across a label slide-out and a zoom blur, so nothing freezes while he talks),
  piece `fadeOut` (a longer seam fade where a rumble was cut to silence), and a caption never runs past its audio join.
  Per-shot grade saturation (`GRADE_SAT`): one overall grade made the editor's own shot-to-shot shift worse.
- **The title scrim is gone**: it darkened the band's white corner brackets to grey (~65/255).

## Round 3 (2026-09-30): short 1's new side-lateral ending

- **Cut where the audio says, not where VAD says.** No VAD gap existed between "laterals," and "I'll": an envelope +
  spectrogram of `master48.wav` found the trough (music floor, -40 dB) 35 ms after the "s" hiss. Test the candidate
  out-points by splicing and running local Whisper (`import whisper`, `small.en`, numpy audio, `fp16=False`): 220.60 read
  "lateral,", 220.63 read "laterals,". Such pieces are written as explicit `{start, end, ...}` objects with the reason.
- **Whisper invents a leading "And" on a clip fed alone**; judge an in-point in context (splice it onto the previous piece).
- **The watch gate's `junk:dead_air` bound is 1.0 s.** A demo pause over it is cut inside its VAD gap, and the picture must
  change at that join. Check the pose on BOTH sides: a punch-in from arms level to his overhead Y was still the confusing
  pose (reviewer). Dan's own demo never HOLDS the pose his words point at (hands sweep from overhead through level to
  below; person-mask extremes per frame), so the card holds its last level frame over the silent pause (`holdTail`,
  <= 7 frames) and the reps enter ON the word "like", at the top of a rep. Match the picture to the word, not the join.
- **Find an editor's transition by per-frame sharpness** (Laplacian on a 480x270 grey decode): the whip started 244.37,
  the last sharp frame was 244.334. A pill's fade by an olive-pixel count in its box: it started 559.57.
- **A grade built for sun-blown footage wrecks evening footage.** Short 1's curve took the live round's skin from luma 0.44
  to 0.29; `NO_CURVE` in `render.js` skips the curve per shot and keeps a saturation push (1.35).
- **Captions:** a piece that continues the previous piece's sentence gets `continues: true` (no capital "If"); a short
  sentence-ending word joins a 4-word cue instead of flashing alone, and a cue's end is floored to the centisecond at a
  join (libass rounds 42.405 up to 42.41 and held it on the next shot's first frame). Both are opt-in per short
  (`joinShortEnd: true`) so finalized shorts rebuild exactly as approved.
- **Re-running `work/ctc_source.py` re-times every short's words** (it had never aligned short 3's opener). For a revision,
  merge the new times for the revised pieces only and keep the rest (`work/words_aligned.r2.json` was the base).
- **Two cards back to back share one box** (same crop and y), or the frame edge jumps 28-38 px on the cut (reviewer).
- **The verbatim audio gate checks whole seconds 1..N-1.** A file that runs 0.01 s past a whole second pulls the tail
  fade into the last checked second (-2.1 dB, FAIL); end the music a few frames earlier rather than touching the bound.
- Reviewer rounds this revision needed: four (arm pose at the pause cut, one rep only, no tail fade, a 6-frame caption;
  card box jump; the how-to pose on screen for 5 frames).

## SL-05 (2026-09-30): "Stop Deadlifting", five shorts. Scripts in `sl05/`

Built in `/Volumes/Extreme/_edit_work/sl05/build/`; the SL-05 versions of every script are in `sl05/` beside this file
(the files one level up are SL-04's). Five to six independent review rounds per short. What they taught:

- **Never shrink Dan into a card to show a key point.** The round-1 plan put him in an inset card on black with the
  editor's pill re-set under it. Every reviewer rejected it (up to 58% of a short was a small picture on black). What
  shipped: Dan always full height, and OUR full-width bar (his colours, font and words) laid exactly over the rows of
  the editor's burned pill, which any 9:16 window would slice. `pill/make_pill5.py` + `BARS` in `plan_shots.py`.
  Measure his pill's rows per pill (a 3-line pill started at row 762, a 2-line at 794): a fixed crop sliced the tall one.
- **A bar covers a fading pill for longer than a colour scan says.** On at first-5%-frame minus 0.35 s, off at
  last-5%-frame plus 1.2 s (`r2/pilltime.py`). At plus 0.5 s his ghost showed through our fade.
- **An editor's "cuts" between medium and close can be ANIMATED ZOOMS** (frame difference ramps over ~12 frames,
  `r2/cutframe.py`). The window must not change size inside one; glide its centre (`slideFrom`, 14 frames) so Dan stays
  centred in both framings. One shared centre left him 186 px off.
- **`-ss` returns the frame AFTER a time that falls between frames.** Map every shot to an exact source frame
  (`ss = (n - 0.3) / FPS`) and make each piece's output frames 1:1 with source frames, or a hard cut flashes one frame
  of the next shot.
- **The full-rate cut finder misses same-framing jump cuts** (whole-frame difference 3-7). `r2/jumps.py` (face-band
  difference spike against its neighbours) found seven; its frame index was ONE LATE, so confirm each with a
  max-difference check around it before planning. Cover each with a FULL<->PUNCH step on the exact frame.
- **PUNCH = 527x786 (1.37x)** while his pill is up (rows 0-786 exclude it); 556x830 (1.30x) otherwise, which is what
  the gate's push row counts as the same shot. A 1.2x step is the minimum that reads as a cut.
- **Blur transitions at piece edges:** cover them with the neighbouring B-roll running long (an L-cut row,
  `lcut:<out at>:<picture src>`) or start the piece after the blur. A held frame under a spoken word reads as a frozen
  mouth; a slowed stock clip stutters (its 24p cadence doubles up). A fade of the last 16 frames to the field hides an
  outgoing blur at the very end.
- **Piece edges need the 5-12 kHz band, not only VAD.** VAD called 338.27-338.81 silence; it held the "-tion" of one
  word and the "You" of the next. Three reviewers measured three different faults at one join. Check each edge on the
  speech-band AND sibilant-band envelope in 20 ms steps and transcribe the splice.
- **Tail fade 0.04 s, not 0.15:** the longer fade swallowed the last word of three shorts.
- **Caption traps:** `t2ass` wrote 30.995 s as "30.100" and libass dropped the cue (round centiseconds first); a CTC
  time can land a word before its predecessor ("no what matter"), so force onsets monotonic; never re-time words from
  a delivered alignment made before a piece changed length; two-line cues reach his chin in a close shot under a bar
  (`oneLine`, `breakBefore`, `capLow` per short).
- **ffmpeg's AAC overshot his true peak by 0.3 dB at 320k** on one short; `aac_at` did not.
- **`gate/ctc_delivered.py`:** split a long window at its largest gap, never mid-phrase, and keep each window's padding
  inside the gap to its neighbour, or edge words align into the neighbour's speech.
