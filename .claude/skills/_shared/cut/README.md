# `_shared/cut`: the junk-footage pass and take selection

The six junk-footage detectors that used to sit in three skills' `work/` folders, run as **one
report produced before the render**, plus **take selection**, which did not exist before
2026-09-24. Executed from `Handoffs/handoff-20260911-junk-footage-pass.md`.

```bash
# the cut as its EDL describes it, measured on the source roll BEFORE any render exists
python3 .claude/skills/_shared/cut/junk.py <roll.MP4> --ranges ranges.py|edl.json|tight_cuts.json \
        [--tight tight.mov] [--pieces segments.json] [--af "pan=mono|c0=c1"] --out junk_report.json

# a delivered file (transcribes it; cached by sha256 under Media/_cache/asr/)
python3 .claude/skills/_shared/cut/junk.py <delivered.mp4> --out junk_report.json

# which take of each beat to keep, as a list for Dan
python3 .claude/skills/_shared/cut/takes.py <roll.MP4> --out takes_report.json --md takes.md

python3 .claude/skills/_shared/cut/tests/test_junk.py      # the fixture; run.py runs it as step 0c
```

## What is in the report

| class | from | what it is | confidence |
|---|---|---|---|
| `PAUSE` | shorts `junkscan.py` | a measured gap ≥ 0.55 s inside a piece | low < 0.65 s (breath, never strip), medium, **high ≥ 1.0 s** |
| `HEAD` | `junkscan.py` | speech starts > 0.45 s after the piece's first frame | medium / high > 1 s |
| `SPLICE` | `junkscan.py` | a source picture cut inside a piece (a naked jump cut unless hidden) | medium |
| `SWALLOWED` | shorts `fixonsets.py` | a gap ≥ 0.25 s wholly inside a word | low < 0.45 s (timing only), medium, high ≥ 0.9 s |
| `STRETCH` | ad-edit `repeat_scan.py` | a word > 0.7 s; verified alone: **confirmed** only if the isolated pass hears extra words | verified |
| `REPEAT` | `repeat_scan.py` | a repeated 4-gram within 25 s, classified **RESTART** / **REINTRO** / **ANAPHORA** | see below |
| `ORPHAN` | ad-edit `orphan_scan.py` | speech-level energy no word covers, ≥ 0.30 s; verified alone | verified |
| `HARD_SPLICE` | ad-edit `hard_splices.py` | pre-render, needs `--tight`: a join whose frame difference exceeds the tight cut's own p99 | medium / high > 2× |
| `PAUSEJUMP` | shorts `pausejump.py` | pre-render: how visible removing a PAUSE would be, vs the source's adjacent-frame baseline | ≥ 3× = real jump |

**The repeat classifier** (measured 2026-09-24 on the rev-0 spray-tan reconstruction, where Dan's
4:00 junk take and eleven of his deliberate repeats sit side by side):

* **RESTART** (junk): a measured hesitation, a gap past breathing rhythm (> 0.65 s) or a word
  stretched past 0.7 s, within 1.5 s before the second copy or inside it, **and** the second copy
  re-says the first (whole ≥ 0.6 or continuation ≥ 0.4). A weak re-say needs a strong (≥ 1.0 s)
  hesitation. *"then this if[0.7 s] you[1.6 s] have someone who can help you"* is this.
* **REINTRO** (listen, low): the same phrase said again fluently after ≥ 8 words of other content.
  The doubled Oura-ring introduction is this; so is *"an AI personal trainer, which takes your
  before picture… an AI nutritionist, which takes your before picture…"*, a deliberate parallel
  list. **No detector separates those two; a person can in two seconds.** REINTRO never fails
  the gate on its own.
* **ANAPHORA** (deliberate, low): everything else. *"He's trying to avoid cancer. He's trying to
  avoid skin damage."* His rhetorical repeats are deliberate; only re-introductions are junk.

**Verification.** `STRETCH`, `RESTART`/`REINTRO` and `ORPHAN` candidates are re-transcribed alone
(4 s window, `medium.en`, `condition_on_previous_text=False`) before they count. `verified` is
`confirmed`, `not confirmed` or `None` with `--no-verify`. An unverified flag is a lead, not a finding.

## What fails a delivery

Two rows in `_shared/deliver/gate.py`, both measured off the delivered file's own audio
(`_shared/deliver/checks/junk.py`), bounds in `formats.py`:

* `junk:repeated_take`: zero **confirmed** RESTART / hidden-restart / dropped-take candidates.
* `junk:dead_air`: no silence inside the speech over the format's bound: 1.0 s for ad-shaped
  formats (the longest in any approved file is 0.94 s), 2.0 s for `longform` (approved C1652 R4
  carries 1.7 s under cutaways). ⚠ Dan's 1.21 s spray-tan pause sits under the longform bound; on a
  longform the pre-render report's `PAUSE` rows (high at ≥ 1.0 s) are where that is caught.

Both rows take the plan's `speech_words` when its evidence is delivered-audio ASR bound to this
sha256, and otherwise transcribe the file (chunked runner, small model, cached by sha256). The
first gate run on a new render therefore takes minutes, not seconds.

## Take selection (`takes.py`)

A take is a run of speech with no gap ≥ 1.0 s; a group is a take plus the takes that re-say it
(whole-text ≥ 0.72, or the same first twelve words ≥ 0.75). Per group, the four rules:

1. **later-take-wins only when the later take is fluent** (no restart, no gap ≥ 0.9 s, no swallowed
   pause ≥ 0.45 s) and complete (≥ 60 % of the group's longest take);
2. **a roll's noise floor identifies the bad take**: a take whose 5th-percentile floor sits > 4 dB
   above the roll's *typical take floor* (median over takes ≥ 3 s), or > 5 dB in the 20-200 Hz band;
3. **cut the whole restated sentence**: a restart inside the chosen take keeps from the second copy;
   a chosen take that opens by re-saying the previous chosen take's tail ends that take's keep
   before the restated sentence;
4. **anaphora stays, re-introductions are a listen** (the classifier above).

Proof on C1512 (the spray-tan roll, 60 takes): the picks agree with the human edit at the intro
(take 9 at 2:15.7; the edit used 2:15.85) and the outro (take 60; the edit's *"final take, 3 earlier
outros dropped"*), and rule 3 finds the same *"in my normal life"* restatement the edit's own
comment records. Its list is in `Docs/TAKE_SELECTION_C1512_20260924.md`. **Dan reviewed the picks on
a labelled clip of every take (2026-09-24) and agreed with all three**: intro take 5, closing take 4,
and the stumble cut as the whole sentence. His words for rule 1: "usually the last take is clean. If
there's no problem with it, keep the last take", with the caveat "not all the time, maybe there's a
stronger take before", which is why fluency decides. **It recommends; it does not cut.**

## Proof

* The rev-0 spray-tan cut (the file Dan rejected with *"junk footage and repeated takes were kept
  in here"*) is not on disk; its recipe is (`rev0/ranges.py`) and the source roll is on the Extreme
  SSD, so the report was run in pre-render mode on that recipe, with verification. Both defects
  Dan named reproduce: the 4:00 junk take reads `REPEAT RESTART high, confirmed` (3:57.7 → 4:04.6,
  the isolated pass hears "If you have someone who can help you do it. Let's say… if you have
  someone who can help you apply") with `PAUSE 1.46 s high` and `STRETCH you 1.6 s` inside the
  second copy; the 11:08 pause reads `PAUSE 1.66 s high`. The same run confirms two `ORPHAN` runs
  (6:11 "my tanning", 10:33 "he takes": words the roll transcript dropped) and the 12:29 restart
  rev 1 left in, and reads all eleven of his rhetorical repeats as `ANAPHORA`.
* Corpus entry `spraytan-longform-rev0` points at the rev-2 master (`FINAL_spraytan_PRE_REBUILD.mp4`),
  which rev 1 had already cleaned of both. What that file still carries is the stumble its own
  recipe marks *"kept (no clean internal cut)"*: *"if you are super pale. Now, if you are super
  pale"* at 12:23, RESTART high, confirmed by the isolated pass: so `junk:repeated_take` fails it
  honestly. See the entry's `measured`.
* `tests/test_junk.py`: the shapes above as synthetic fixtures, no Whisper, run by `qc_corpus/run.py`.

## The picture-cut half of this folder (VQC-C, Opus 5.5, 2026-09-24, same day)

`_shared/cut/` is one folder for two halves of the same problem. This README's top half is the
AUDIO side (what to cut: junk, pauses, takes). The other half, shipped the same afternoon from
`Handoffs/handoff-20260909-vqc-C-phase4-cut-technique.md`, is the PICTURE side (how to cut it so
the join does not read):

* `piccuts.py`: the pose-matched picture cut, the only copy. The audio splice stays; the picture
  cut moves 1-15 frames to where Dan's head is in the same place and size on both sides (Muhammad's
  J/L-cut), against `piccuts_calibration.json` (his trusted Ad 2 cuts median 17.9 px of head jump;
  Ad 1 attempt 1 median 39.0).
* `landing.py`: the crop-track smoother with a 0 px landing after every cut (the per-segment median
  that used to look into the next take is gone).
* `deadair.py`: pause shortening with per-format presets, every removal decided by `piccuts.py` and
  flagged `cover` + `watch` when the head still jumps. It honours the same two measurements this
  half does: a pause removal is as visible as the fault (4.97-12.46 vs a 1.30 baseline) and
  0.55-0.65 s is breath.

How they meet: the junk report's `PAUSE` and `PAUSEJUMP` rows say WHERE the dead air is and how
visible its removal would be; `deadair.py` + `piccuts.py` make the removal and place the picture
cut. `junk:dead_air` on the delivered file then checks nothing was left. Each module's docstring
is its manual; `tests/test_piccuts.py` is that half's fixture.

## Where the old copies are

The three ad-edit tool copies (`reference/repeat_scan.py`, `orphan_scan.py`, `hard_splices.py`) are
deleted. The copies inside frozen build recipes (`shorts/reference/*/work/`,
`website-video/reference/recipe/**`) stay, because those folders re-render past deliveries; they are
recipe files, not the live tool. Do not fix a bug in one of them: fix it here.

---

# The picture cut (VQC-C, 2026-09-24): `piccuts.py`, `landing.py`, `deadair.py`

Our cuts read as jump cuts because we cut the PICTURE on the AUDIO splice. Muhammad cuts it 1-15 frames
away on a frame where Dan's pose matches (a J- or L-cut). These three files are the only copy of that
technique; every video skill calls them. `Handoffs/handoff-20260909-vqc-C-phase4-cut-technique.md`.

```bash
# every talk splice: the frame the PICTURE cuts on (audio untouched, length unchanged)
python3 piccuts.py decide --build DIR --mode raw --raw ROLL [--rolls rolls.json] --grade grade.py \
        --edl edl.json [--talk talk_spans.json]              # -> DIR/piccuts.json + DIR/edl_picture.json
python3 piccuts.py decide ... --mode master --reference his_16x9.mp4   # conforming to an editor's cut
python3 piccuts.py strips --build DIR --raw ROLL --grade grade.py --edl edl.json --crop 0.30,0.70
                                                             # -2..+2 frame strips, audio cut vs chosen, for EYES
# pauses shortened (never removed outright), every removal paired with a picture decision
python3 deadair.py --edl edl.json --raw ROLL --preset ad|website|shorts --out DIR --pair --grade grade.py
python3 landing.py selftest                                  # the crop track lands ON him at every cut
```

**How the frame is chosen (raw mode).** Search ±15 frames for the k where Dan's head (mediapipe face box:
centre shift + height change, 1920-wide px) is in the same place on the last outgoing and first incoming
frame; ties within 4 px go to the higher high-passed NCC (hands, shoulders), then the smaller |k|. No
face: NCC alone. A take is never on screen for fewer than 8 frames. Above the calibrated head jump
(`piccuts_calibration.json`, 28.5 px = midpoint of Muhammad's median 17.9 and attempt 1's 39.0) the
cut is flagged `cover: push` + `watch: true`: the render covers it, the watch pass looks at it.

**Why head, not NCC** (Ad 1 attempt 1, 72 splices, 2026-09-24): exposed cuts (head jump > 28.5 px)
ON the audio 50 · NCC choice 39 (+4 no face) · head choice **10**. NCC picked a frame worse than the audio cut
at 2.78 s (96 vs 47 px) and 11.50 s (42 vs 15 px). Eye check: 5 of 5 random "fixed" cuts hold the
head across the cut; the 4 flagged ones still show a step (3 smaller than before).

**`landing.py`** is the per-segment crop smoother (shrinking median window, endpoint-anchored
forward/backward slope-limited blend): landing and exit error 0 px. 2026-09-24 fix: the sample
forced onto a take's last frame used to be interpolated toward the NEXT take (kit_track /
facetrack4), so the crop slid toward his post-cut position before the cut (selftest: exit error
188 px median before, 0 after). `kit_track.py`, `facetrack3.py`, `facetrack4.py` import it.

**`deadair.py`** presets: `ad` 0.22 s min, keeps 0.055 + 0.100 (ad-edit modern60); `website` 0.30,
0.12 + 0.18 (the trust cut); `shorts` 0.66 (0.55-0.65 s is breath, never touched). On one uncut
minute of C1591: dead air 21.9 % → 0.0 %, 27 removals, 26 moved to a head-matched frame, 5 flagged.

**Grade** lives beside the picture reference: `_shared/reference/luma_lift.py` measures the graded
talking head on the watch scan's instrument and sizes a shadow lift to Muhammad's centre (69.1),
never past his `hi`, refusing any lift that grows clipped highlights by > 1 point.

The forks are gone: `a2/piccuts.py` deleted; `kit9x16/kit_cuts.py` is a 5-line shim; `build_kit.py`
calls `piccuts.py` directly. `a6/zedl.py` / `zedl2.py` remain as the frozen recipe of Zeeshan's
whole-edit recovery (a different job: acoustic offset profile + picture crossover at 24 fps).
