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

## Round 1 was rejected (2026-10-09): what went wrong, so it is not repeated

Dan: "one of the worst edits that you have done in a long time." Colour and sound rejected, capitals overused, weak B-roll.
- **Colour:** option C was picked on numbers (skin median, hue against the published references) and never looked at full
  size beside an approved frame. It read dim, muddy and orange. D (brighter, lighter saturation, denoised) won once four
  options were viewed side by side. Dark, backlit footage needs the eye test before anything is rendered for Dan.
- **Sound:** the chain's automatic tone match was fitted on a room with 69 ms early decay and added 5 dB of treble; the
  expander chopped the room tail off word endings. The audio gate passed it 12 of 12. A blind listen scored it 4 of 10,
  below the untreated lav (5), with a light dereverb plus a gentle fixed EQ and no expander at 8. On a wet room, run the
  five-way audition (`audio_options.py`) BEFORE the first minute.
- **Capitals:** one FULL CAPS word in almost every lower third. Title case is the default (VIDEO-RULES, top section).
- **B-roll:** chosen for the exercise it showed, not for how he looks. Opener favourites: B0448, B0456, B0453.
- The fix for the process is in `_shared/PRE-RENDER-APPROVAL.md`, "Before Dan sees anything".
Round 1b (`round1b/`, page 8858): colour D and voice 4 locked by Dan on 2026-10-10. Next: `Handoffs/handoff-20261010-ro07-round2-revisions.md`.

## Round 2 (2026-10-10): what was built and the traps

Order: corpus entries -> `voice_chain.py --no-expander-because` (new shared flag) -> `plan.py` (capitals, G43 split, clips,
10 cutaways) -> `resolve.py` -> `from_plan.py --render --force` (every lower third: the template gap fix) -> `build.py filmvoice`
-> `r2media.py first | stills | context` -> `page_r2.py`. Page: `round2/index.html`, port 8859.

- **Voice 4 through the shared chain is sample-identical to the approved audition** (`build.VOICE4`: `--eq`, `--dereverb-because`,
  `--no-expander-because`). Proof on the same 31 s: correlation 1.0, residual 0 (`round2/voice/proof31_chain.wav`). The audio gate
  fails it on the tone row only (less treble than the reference, by design). Report it; do not tune it.
- **Review context clips take their voice from one whole-film chain render** (`build.py filmvoice`, then `render_range(...,
  audio="slice")`). A 10 s clip run through the chain alone can read a dry room and the dereverb opt-in would refuse it; a
  slice also sounds exactly like the film will.
- **The B-roll rolls need a grade entry for every kitchen option.** `grades.json` had A/B/C only for C1490 to C1494, so look D
  raised KeyError on the first poolside clip. D and E now point at their own outdoor grade.
- **The library filed two clips wrongly, and the plan believed it.** B0433 is his real KNEE push-ups (the round 1 plan said no
  real footage existed and used the AI demo); B0431 is kettlebell DEADLIFTS, not swings. Contact-sheet the source roll before
  writing "no footage exists". Both entries are corrected.
- **8/28 roll C1680 holds every push-up level side on in low sun** (knee 12 to 36 s, regular 48 to 72 s and 144 to 156 s, handles
  188 to 212 s and 226 to 250 s). `broll_cuts.py` cuts from it with the library's approved grade (1.30 LUT, saturation 0.88,
  cooled). The 7/8 handle roll C1492 has the from-behind angle Dan disliked.
- **Start on the first rep means finding it frame by frame**: a 0.25 s contact sheet of the first seconds of each candidate
  (squats in C1490 start at 85.9 s, not 78; the handstand and decline clips start a rep at 0.0, not 1.0).
- **No footage twice also means no shared frames between two clips of one take** (round 1 had C08 inside C21's range).
- **A stock or AI library clip can carry burned-in text from the film it came from** (A0138 has another video's lower third,
  A0019 ends on a red X). Look at the contact sheet before placing one.
- Cover went from 20 % to 26 % with 10 cutaways (13 built, 3 cut after their stills were looked at: burned-in text, and two
  clips of Dan lying flat or seen from behind). Look at every new clip's still on the sheet before the context render, not
  after: each plan change re-solves the framing. The library has no clip for the alarm clock, commute, couch and
  tired-at-night lines. More cover needs new stock.

## Round 3 (2026-10-10): two trims, the A3 motion, the full film, and what two independent reviews found

Order: `broll_cuts.py` (the handstand re-cut) -> `plan.py` (C01, C31, A3) -> `gen_motion.py A3 A3-t1 6` -> `resolve.py` -> pin the solve
(`build._R2` from `round3-plan/segs.round2.json`) -> `from_plan.py --render` (nothing changed) -> `bed.py` -> `render_r3.py` ->
`finish_chain_r3.sh` (audio gate, transcript, `finish_r3.py`, watch pass, hair, graphics checks) -> `ra-reviewer` -> fixes -> render again ->
`carry_r3.py` -> a second `ra-reviewer` on the 14 changed images and the fixes -> edit sheet -> delivery gate -> `page_facts_r3.py`,
`page_r3.py` (port 8860) -> `deliver_r3.sh`.

- **"Start on the rep" needs a per-frame height curve, not a contact sheet.** Template-match his shorts down the frame on a low-res graded
  proxy of the whole roll (`round3/work/measure_hs3.py`): the handstand roll C1684 holds still until 15.88 s, so library B0456 (12 to 22 s
  of it) opens on two seconds of nothing. A colour mask of the shorts failed (the hedge is green too); the template match is clean.
- **A library AI clip can end in a frozen frame before its burned-in mark.** A0019 is one still from 6.25 s; the red X is drawn over that
  still from 6.87 s. Reading the tail for the X alone passed a cut that ran 0.37 s into the freeze; the watch pass's `scan.frozen` and the
  reviewer both caught it. Before trimming any library clip near its end, print the frame-to-frame difference of its last two seconds.
- **A 24 fps clip in a 29.97 film repeats one frame in five.** That is not a hold; a hold is several identical frames in a row.
- **Veo with a first and last frame reaches the last frame early and hangs there.** A3 hit the end pose at 3.8 s of 6 s and floated for
  2.2 s. Use the part before it, and move the clip so the action lands on the word (`late=` on the start phrase), not the slot's old start.
- **Moving one clip's edges re-solves the framing of the whole film.** A3's new start flipped two shots ten seconds away and slid a run's crop
  4 px. `build._R2` + `OVERRIDE` now pin every shot to the solve Dan reviewed; print the diff against the last `build.json` before rendering.
- **Low-angle GoPro B-roll shows the set.** B0476 has a crew member at the left edge looking into the lens beside a reflector (nobody saw
  it on the round 2 stills). Its source is 1440x1080, so a plan `crop` is in SOURCE pixels (the first try in output pixels broke the pipe).
  Look at the edges of every wide B-roll clip at full size.
- **Mouth clicks at the head of a take:** `build.DUCK` turns a 60 ms window down 40 dB in the untreated voice (6 ms ramps). The reviewer
  measured them (peak in 10 ms steps against the pause floor); the audio gate cannot see a 30 ms click.
- **Subtitles from the roll words drop the first word of many takes** (its start falls in the cut gap) and can splice a false start
  ("produces This is better"). Diff the SRT against a transcription of the FINISHED film (`difflib` on normalised words), settle each
  difference with a medium.en pass on a 12 s window, then `round3/srt_words.json` (inserted words with times) and `srt_fixes.json`.
  An inserted word must sort before the word it precedes, or the cue reads "counting reps Counting to reps can lead".
- **Chapters:** a lower third's start phrase is often mid-sentence. Anchor each chapter on the sentence's first words (`CHP` in `finish_r3.py`).
- **Bed level on an indoor lav:** -30 dB (the chain's ceiling) put the pause floor level with the reference (+1.3 / -0.5 / +2.1 against a
  -3.0 limit on the film); -24 was 1 dB from failing. Whisper returns "Music" tags and a low-confidence phrase at a truncated end on an
  instrumental; re-run the window with trailing context before reading that as words.
- **After a reviewed render, compare every frame of the next render with it** (`carry_r3.py`, 480x270 PSNR). Unchanged strips keep their
  verdict; only 14 of 520 images needed a fresh judge. x264 also re-encodes about 35 frames before each changed stretch (49.9 dB or
  better): say so in the log.
- **Gemini's listening check invents dropouts** (again): it heard "digital silence" in pauses that measure the same as every other pause.
  Measure 20 ms RMS before acting on it. `gemini-2.5-pro` is retired; `GM=gemini-3.1-pro-preview`.
- Gates on the delivered file, stated honestly: audio gate 12 of 13 (tone: the voice Dan chose); delivery gate fails on the audio stamp,
  cover 27 % (floor 40), hair top and headroom (camera framing), splice visibility, two caption false alarms, a repeated-take false alarm,
  and the watch row (hair open until Dan's word). Review 1 DOES NOT SHIP (the C31 freeze), review 2 SHIP.
- **Dan approved the round 3 film on 2026-10-11:** "Okay, this is looking good. This is approved." Finalized the same day: footage ranges
  marked used on seven rolls, clips A0158, A0159 and B0545 to B0549 registered, corpus entry `ro07-r3-final-approved-20261011`, edit sheet
  approved, queue `finalized`. He wrote no line on hair at the top edge, so it stays as shot (editor's reading, recorded as such). His
  thumbnail mix for this video (1 pool, 1 studio, 1 real exercise frame or photo, 2 AI, five unique designs) is in
  `Handoffs/handoff-20261011-ro07-thumbnails-and-video-setup.md`.
