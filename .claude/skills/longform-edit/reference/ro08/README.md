# RO-08 "Intermittent Fasting: The Best Way To Get Abs" (7/8 kitchen roll C1486): round 1 recipe (Claude Opus 5.5, 2026-10-12)

One talk roll filmed off an outline, the same set and shoot as RO-07. Starts from `../ro07/` (copy its chain, then this
folder). Only the files that differ are kept here. Work dir and media: `/Volumes/Extreme/_edit_work/ro08/` (never commit
media; the repo is public). Round 1 page: `round1/index.html`, port 8869.

Order: `pick_lav.py --ss 140 --t 45` -> `asr_rolls.py C1486` (medium.en; put the project ffmpeg on PATH first, Whisper calls
`ffmpeg` by name) -> `mkglobal.py` (also patches one hidden retake into the word list) -> `edl.py` -> `shots.py` ->
`words_src_out.py` -> `framing.py` -> `grade.py` (look D) -> `plan.py` -> `resolve.py` -> `hyperframes/from_plan.py`
(dry run, then `--render`) -> `build.py filmvoice` -> `chain_r1.sh` (first minute, audio gate, stills, context clips)
-> `page.py` -> `review_server.py 8869 round1`.

What was reused from RO-07 after a source check, not reopened:
- **Colour D** (Dan's pick, 2026-10-10). C1486 measures the same as C1485: skin median 0.254 against 0.256, skin Y90
  0.293 against 0.290, black 0.063 against 0.062. `grade.py` now carries D as an option (`pre="hqdn3d=2.5:2:5:4,"`,
  t90 0.57, mid 0.96, low 0.78, saturation 1.08, hue 4): it was only in RO-07's grades.json before.
- **Voice 4** (light dereverb on a wet room, the gentle fixed EQ, no expander). Raw room on this roll: 82.7 ms early
  decay; 50.7 ms after the dereverb.
- The quiet bed (`bed.py`, -30 dB), the two sizes (W camera frame, T 1.3x), lower thirds only (no side card fits).

What is new here:
- **The standing bass lift is sized to the microphone.** Voice 4 with no lift already reads 7.4 dB in the gate's lowest
  speech band against the reference's 5.4. The rule's +3 dB at 120 Hz would put it at 9.7, so the default is +1 dB (8.2).
  `build.py`: `RO08_BASS_DB` (default 1.0), `RO08_NOBASS=1`, `RO08_VOICE=<name>` for a second film voice. Dan hears all
  three on the page (same 31 s of the cut, starting on speech, level matched by the shared finisher).
- **`resolve.py`: a lower third comes on 0.6 s before its first words land.** A start phrase that sits seconds before the
  first part's phrase leaves the plate on screen holding only its topic line (31 of 48 did in the first build of the
  first minute). Write the start phrase where the first part lands, or let the clamp do it.
- **`words_src_out.py`: a take's first word is kept when at least 35 % of it is inside the shot.** Whisper starts words
  early; the in point is the measured onset, so "Today," fell outside the cut by its midpoint and the opener's phrase
  could not be found. Three one-syllable openers ("The", "In") are still missing from words_out: the SRT pass must diff
  against a transcription of the finished film (the RO-07 round 3 method).
- **`plan.py` clip `crop=` is honoured by `stills.py`** (the still showed the uncropped stock).

Traps this build paid for:
- **The roll sidecar's lav pick was wrong** (channel 0, the far mic). Three clean 45 s windows all say channel 1, 10 to
  13 dB better SNR, the same as the RO-07 rolls. Two rolls of one shoot must agree; check before believing a sidecar.
- **Whisper hid an abandoned sentence and its retake inside one 3.4 s "some"** (1126.7 to 1130.1). The lav envelope showed
  1.4 s of quiet, then 1.9 s of speech where the transcript had one word. Listing every word over 0.8 s inside the kept
  pieces and printing the envelope under each finds these; `verify_asr.py` on a window that starts in the pause settles
  the words. The fix is a patch in `mkglobal.py`, so `edl.py` can anchor on the retake's own first words.
- **An end phrase that also occurs earlier resolves to the first one** ("the day the same" ended a piece 16 s early).
  After `edl.py`, read every piece's duration against the roll.
- **`resolve.py` searches each item from the previous item's start.** An item moved to a later start phrase must also
  move down the plan, or the next item is "not found".
- **Whisper needs `ffmpeg` on PATH**; the project's static build is not. The first ASR run exited 0 from the wrapper and
  had written nothing.
- **A stock still can show a body part the moving crop will not.** The burger clip's still was a heavy man's torso at the
  table; the film crops to the food (`crop=` in source pixels).
- **Two clips that look alike are a repeat even from two sources** (coffee poured into a dark mug, twice). One came out.
- **A lower third that states half of a two-sided sentence contradicts the cutaway under the other half** ("Lose Fat."
  holding over a burger on "you're going to gain fat"). Write both halves as two parts.
- **One Gemini listen cannot separate voices 1 dB apart**: it called the +3 dB version "gated" (there is no gate). Used
  only to confirm the chosen voice ranks above the untreated lav. The page says so.
- **The machine was shared with RO-19's full-film render all session.** Lower thirds and context clips ran one worker
  at a time; a second worker waited on the other build's processes (`chain_r1.sh`, and the gated second worker in the
  round 1 notes).
- Hair: the camera left about 14 px above his hair on this roll (median; 0 in most shots at some moment). Both sizes
  keep the camera's top row. Reported to Dan as a decision, as on RO-07.
