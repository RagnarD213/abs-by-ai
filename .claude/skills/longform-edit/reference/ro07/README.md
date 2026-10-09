# RO-07 "Why You MUST Work Out Every Day" (7/8 kitchen rolls C1484 + C1485): round 1 recipe (Claude Opus 5.5, 2026-10-09)

Two talk rolls filmed off an outline, plus poolside B-roll shot for this video the same day (C1490 to C1494). Starts
from `../ro06/` (which starts from ro10, ro11, ro13, ro16: copy all five in that order, then this folder). Only the files
that differ are kept here. Work dir and media: `/Volumes/Extreme/_edit_work/ro07/` (never commit media; the repo is public).

Order: `pick_lav.py` per roll -> `asr_rolls.py` (medium.en words on each roll) -> `mkglobal.py` -> `edl.py` (pieces anchored on
PHRASES, not typed times) -> `shots.py` -> `words_src_out.py` (words_out.json straight from the roll words + a 4-word repeat
scan) -> `framing.py` -> `grade.py` -> `look.py` -> `plan.py` -> `resolve.py` -> `hyperframes/from_plan.py` (dry run, then
`--render`) -> `stills.py` -> `round1.py first` -> `round1.py context` -> `page.py`.

What changed from RO-06:
- `edl.py`: a piece is `(id, roll, first words, last words, hint)`; `find()` resolves it in the medium.en word list and
  `onset()` / `offset()` set the edges on the measured lav. A typed time can no longer drift from the words. An in point can
  be forced with `"ONSET:a:b"` (first sustained speech between two roll-local times).
- `words_src_out.py` replaces the medium.en pass on the assembled cut for placing graphics (the rolls were already transcribed
  with medium.en). The assembled pass still runs as a cross-check (`asr_assembled.py`).
- `grade.py`: indoor options A/B/C, a shadow-only blue removal for the kitchen rolls, one outdoor grade for the B-roll rolls
  (masks made on the fly). Everything is applied at 16 bits (`format=gbrp16le`): the rolls are 10-bit and 1.5 stops under.
- `build.py`: two sizes only (W camera frame, T 1.3x), the punch-in by default; `grade` on a clip may be a list (one per
  source); a clip may carry `crop`.
- `plan.py`: B-roll straight from the raw rolls (`br(roll, t)` + `grade=roll`); new AI clips as `frames=[start, end]`,
  `pending=True`.

Traps this build paid for:
- **`pick_lav.py`'s default window can land on crew talk.** On C1484 (46.7 to 91.7 s: a plane, Dan asking the operator a
  question) it picked the far mic on a 1.1 ms arrival difference while SNR said the opposite (28.9 against 42.9 dB). Two
  rolls of one shoot must agree: when they do not, re-run with `--ss/--t` on clean continuous speech before believing it.
- **The job doc said "same set as published V3". It was not** (V3 was filmed in the other kitchen, welcome-video shoot
  C0238). Contact-sheet the reference before matching anything to it. No approved look existed for this set, so colour went
  to Dan as a real decision.
- **Dark indoor S-Cinetone with a bright window behind: the shadows are blue, the mids are not.** The black tank top read
  R .067 G .075 B .098 while the fridge mid-tone was neutral. A whole-frame white balance would have tinted his skin; a
  per-channel curve that only acts below about 0.25 fixes the tank top and leaves skin alone.
- **Skin lit flat: anchor on the median, not only Y90.** Skin median 0.26 and Y90 0.29 are almost the same here, so
  matching Y90 to the references' 0.56 put the median at 0.47 against their 0.33 to 0.36. Targets used: Y90 0.46 (rich),
  0.53 (brighter).
- **Whisper folds a false start into a stretched word.** "Counting reps can [stop] Counting reps can lead" came back as
  one "lead" lasting 1.9 s; "Or for those..." sat inside a 2.6 s "just". Re-transcribe every window that holds a word
  over 0.9 s alone (`verify_asr.py`) and take the in point from the lav envelope, not the word time.
- **`verify_asr.py` on a window that starts mid-word returns garbage** ("with you."). Start the window in a pause.
- **zsh aborts a whole `cp a/*.py a/*.json` when one glob has no match.** Half the recipe chain did not copy and nothing
  said so. `setopt null_glob`, then check for `softblue.py` and `gfx.py`.
- **"work out" and "workout" are different tokens.** An end phrase "work out every day" skipped the hook's "workout every
  day" and resolved 16 s later. After `resolve.py`, read every item's duration.
- **Lower third parts must be in the point's order** (`from_plan.py` asserts it): write the point in the order he says it.
- **A waist-up centred medium at 1080p takes no side card** (as on RO-06's close rolls). Lists are lower thirds.
- **A stock still used on a fact card is still that stock source** (the traffic clip was also a cutaway: one had to go).
- Hair: the camera left 20 to 45 px above his hair and it touches the edge for moments in six late shots. Both sizes keep
  the camera's top row; reported, not fixable by a crop.
