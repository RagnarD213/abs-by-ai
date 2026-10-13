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

## Round 2 (2026-10-12): the AI motion, two openers, the full film

Order: re-hash (`round2-plan/round2-start-hashes.sha256`) -> pin the solve (`build._PIN` = `round2-plan/segs.round1.json`) -> prompts in
`round2/motion/` (kept here in `ai-motion-prompts/`) -> `gen_motion08.py` (13 takes, four at a time) -> `lipsync08.py` + `lipstrip08.py` ->
`opener_ot.py` -> `plan.py` (motion in, C22 out) -> `resolve.py` -> `from_plan.py --render` -> `round2.py first`, `first O6`, `context` ->
`render_r2.py` -> `finish_chain_r2.sh` (`finish08.py`) -> `ra-reviewer` -> edit sheet -> delivery gate -> `page_r2.py` (port 8871) -> `deliver_r2.sh`.

- **Several Veo takes at once need a ledger with no shared file.** `gen_motion08.py` writes one json per take and sums them; it refuses a
  take that would pass the cap. Thirteen takes ran four at a time in about seven minutes.
- **A time-lapse from key frames:** one 4 s move per pair, prompted as time-lapse footage ("two hours pass in four seconds", the clock
  only ever moves clockwise), then `opener_ot.py` DROPS frames (never blends) so 10.6 s runs in 2.9 s, and the last pair plays at normal
  speed. The clock hands wander inside a take and a numeral can flash on the dial for a frame; at 3.6x nobody sees it. What has to be right
  is each join: the same hour and the same coffee level on both sides. Key frames drawn at slightly different sizes read as the camera
  breathing once in the fast part.
- **Veo turned an analog wall clock into a digital "8:00" display for three seconds** (split screen, first take) when the prompt only said
  the hands move. The second take described the clock ("a plain white face and two thin black hands, never a digital display, no digits")
  and put "digital clock, digits" in the negative prompt: clean. A clock is the first thing to read in any take that has one.
- **Lip sync on a face that lies sideways works if the model gets it upright.** `lipsync08.py` sends only a window round the head, turned
  90 degrees and enlarged 2x, and lays the result back through a feathered mask (nothing outside the window changes: 0.2 levels). Tested
  on 2.5 s first ($0.21). Sync only the stretch where he faces the camera; Veo started the roll-over at 3.5 s though the prompt said 5.5.
- **`lipmeasure20.py`'s number is weak on a whining, grimacing mouth:** A1 read r 0.18 against the unsynced take's -0.10, A2 0.05 against
  -0.06, yet in both the lips close on every m and b. `lipstrip08.py` (the mouth followed with the face mesh, every second frame labelled
  with the word being said) is the check that decides; give both to the reviewer.
- **The AI label's default corner can cover what the clip is about.** Top right sat on the wall clock in the opener and the donut clip, and
  top left sat on a man's forehead in the split screen. `chip_xy` / `chip_anchor` on a plan item (`build.py`). Look at the chip on a frame
  of every new AI clip.
- **A lower third planned over a placeholder can hide the gag once the clip moves.** G20 lay over the donut box for A5's first 2.6 s, the
  exact stretch where the box empties. Its text now lands on the sentence before ("And there's a reason for that") and it is off as the
  clip starts. After motion arrives, list every lower third that overlaps an AI clip and look.
- **A take that is longer than its slot can lose its slow start, not its payoff:** A6 starts 1.6 s in (the walk to the fridge is out), A7
  0.6 s in. Print the frame-to-frame change over the part used: no take here hangs on its end frame.
- **The gate's `compliance:negative_events` row wants a recorded scan** (`negative_events_scan.json` beside the master, sha256 and
  findings); the watch pass's contact sheets stacked three to a page are that scan in four looks.
- **Subtitles:** four take openers ("The", "In", "Now that's", "The") come from the finished-film diff (`round2/srt_words.json`), one doubled
  word is dropped (`srt_drop.json`, new in `finish08.py`), drug names are spelled in `srt_fixes.json`, and a sentence that starts inside
  a cue now gets its capital.
- **What two independent reviews found on this round (the build's own checks found none of it):** the lip-sync paste left the last
  synced face on the floor for 3.4 s after the man rolled away (`alphamerge` repeats its last frame: the mask is now trimmed to the
  synced frames, and a composite is checked at its END, not at two early frames); the AI label sat on a background bartender's face;
  a Veo take's last frame was 9.7 levels from the key frame the next take starts on, so a cut between them at normal speed jumped
  (search the take's tail for the closest frame and end there: frame 88 of 96 here, 2.2 levels); "9 a .m." and "o 'clock" in the SRT.
  The first render did not ship; the second did. `carry_r2.py` kept 474 of 494 image verdicts (a defect verdict is never carried).
- **The no-sync fallback take does not reach the approved end frame** (it is made from the START frame only). Say so on the page and
  ask Dan to watch that clip; a mouth that pants a little with the eyes shut does not read as speech.
- **Chapter stamps are whole seconds:** anchor each on the sentence's true first word ("The", "Now,"), then `floor(t + 0.25)`. An
  anchor on the second word stamps the chapter after the first word has been said.
- Round 2 delivered 2026-10-13: page 8871, audio gate 12 of 13, delivery gate 32 pass and 7 known fails, $10.57 of the $15 cap.
  Next: `Handoffs/handoff-20261013-ro08-round3-after-dan-review.md`.

## After Dan's round 2 review (2026-10-13): three AI clips rejected that every check had passed

He chose opener A, removed A4 ("I don't think that illustrates the idea well, or the joke really lands here") and A3 ("The water jumps
up in the air for no reason... It makes no physics sense"), and sent A5 back ("all the donuts just disappear, vaporize, and go
nowhere... things that look like AI slop like this get caught in quality control and don't make it to my review"). His words are in
`round3-plan/decisions.json`; the rule is VIDEO-RULES.md, top section (2026-10-13). What the build did wrong, so it is not repeated:

- **A fault I can describe on the review page is a fault I should have fixed.** Both oddities were written there ("the rumble reads as
  water splashing up out of three glasses", "the box empties in a one second fast-forward") and shipped as if naming them were enough.
- **Never ask the model for a time jump inside one take.** The A5 prompt said "time speeds up into a fast time-lapse for a moment...
  the box empties". Veo cannot eat five donuts in a second, so they vanish. An hour passing is a CUT between a shot at nine and a shot
  at ten. The opener's time-lapse works because the whole shot is one, and nothing in it has to disappear.
- **A cause the viewer cannot see is no cause.** "A deep rumble comes from him" is sound; the picture only showed water jumping.
  If the idea needs the prompt to explain it, pick another idea or leave the camera scene.
- **Give the reviewer the three questions per clip** (cause and effect, sound-off test, does it show the line). Two reviewers read
  every frame of these clips for melting hands and labels and were never asked whether the scene made sense.
- Removing a cutaway can break the hold rule under a pinned solve: with A4 out, three shots of one take run 30 s at one size.
  Next: `Handoffs/handoff-20261013-ro08-round3-revisions.md`.
