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
