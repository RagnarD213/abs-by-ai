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
- **`edl.py`'s out snap can run into the next word when Whisper puts that word within 0.10 s of the last one** (`offset()` is
  then allowed 0.25 s past the next word's start). The hook ended on 0.1 s of the cut sentence's "It's"; a watch-and-listen
  pass on the first minute heard it. After `edl.py`, list every piece whose out is past the next roll word's start and print
  the lav envelope under each (five of six were Whisper's early starts and fine). The fix was two measured edges that keep
  the film's length identical (hook out 5 frames earlier, the next piece in 5 frames earlier in room tone), so no graphic,
  clip or context clip after it moved. The same pass also "saw" a black frame and four jump cuts that are not there.
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

## After Dan's round 1 review (2026-10-12): what changed before the round 2 handoff

- **The opener.** He cut the workout B-roll opener and asked for AI ideas; of ten he took idea 6 (split screen) and added
  his own (a time-lapse of a ripped man at his laptop from 8 AM to 2 PM, then a salad at normal speed). A time-lapse
  needs key frames, not a pair: five were drawn as edits of the first (`ai-frame-prompts/OT-*.txt`). Read the clock in
  every frame at full size, and compare the room across frames: the first empty-chair frame had a different shelf and
  sofa, and a prompt that lists what must not move fixed it.
- **A clock in a generated frame is wrong more often than right.** Idea 6's first start frame read about 12:30 on a
  breakfast scene. Describe the hands ("short hand between the 7 and the 8, long hand straight down"), then crop and look.
- **"B-roll is colour corrected" has to be checked on every clip of Dan, not on the one he names.** C38 (library B0427,
  low sun) read 0.30 on his skin against 0.51 on camera. So did the kettlebell and decline push-up cuts, and the salad
  film's own grade is darker than this film's look. C38 became B0030 (bright daylight); the others got a lift
  (`round2-plan/broll_grades.json`). Measure skin and frame median, then look at the still beside a presenter frame.
- **"A little less echo" is the dereverb's alpha and floor, nothing else.** `audio_options08.py`: four steps on the same
  31 s with the tone held. The step past alpha 0.45 / floor -13 crossed the gate's damage limits and was not offered.
  The room-decay meter did not rank the steps (it read 45, 63, 64, 61 ms); Dan chose by ear (1a: 0.35 / -11). The pick
  goes through the shared chain with `--dereverb alpha=0.35,floor_db=-11`.
- **`review_server.py` run a second time on the same port can fail once with `launchctl bootstrap ... exit status 5`**
  and leave the page down. Run it again and check the URL returns 200 before telling Dan the page is refreshed.
- **A second page beside a served review needs its own folder and port.** The server caches only files linked from the
  folder's index page, so a `round1b.html` next to it returned 404.
- **Dan set this video's AI budget to $15 on 2026-10-12** ("For the budget, let's do $15") after eight clip ideas plus two
  openers priced at about $8.85 against the $5 content cap. The question had to be put three times before it was
  answered: put a spend question first in the message, alone, with the number to say.
