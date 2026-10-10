# RO-07 "Why You MUST Work Out Every Day": round 2 is with Dan (written 2026-10-10)

**CONTENT, long-form (LFC). Next task name: `Work Out Every Day LFC R3`.** Skill: `/longform-edit`.
This replaces `handoff-20261010-ro07-round2-revisions.md` (executed).

## State

Round 2 page: http://localhost:8859/ (folder `/Volumes/Extreme/_edit_work/ro07/round2/`, managed review service).
VLC copy: `Videos to Review/Work Out Every Day LFC R2 - first minute.mp4`. Queue state `draft_review`. No full film exists.
Dan has NOT replied yet. Do nothing until he does; then record his words in `round3-plan/decisions.json` first.

## Read first

1. `/Volumes/Extreme/_edit_work/ro07/round2-plan/decisions.json` and `dan-notes-20261009-verbatim.md` (round 1 notes, all built).
2. `.claude/skills/longform-edit/reference/ro07/README.md`, section "Round 2" (order of scripts, traps).
3. `round2/stills.json` (every changed or new item with its times) and `recipe/page_r2.py` (the eight open decisions, `DEC`).
4. `.claude/skills/_shared/VIDEO-RULES.md`, top section.

## Locked (re-hash before touching)

- Colour D, `round1b/colour/option-D.mp4`, sha256 `509b1bf9...ff5f`. Voice 4, `round1b/audio/4-warm-less-room.wav`, sha256 `7ad58a58...01bc`.
- Voice 4 in the build: `build.VOICE4` (shared chain, `--eq`, `--dereverb-because`, `--no-expander-because`). Proven sample-identical
  to the approved audition on the same 31 s.
- A2 frames (approved) and the take `round2/motion/A2-t1.mp4` (sha256 `25fe9f4b...1d4e`), used from 0.8 s. A3 START frame.
- Round 2 first minute: `round2/first-minute/DRAFT - RO-07 round 2 - first minute.mp4` (hash it when Dan approves it).

## Waiting on Dan (the page's eight decisions)

1. A3: START plus the NEW END frame `aiframes/A3-end-r1b.png` (sha256 `0bf1e7cf...b08e`). If approved: add `"A3"` to
   `motion_authorized`, point `gen_motion.py`'s end frame at `A3-end-r1b.png` (it reads `A3-end.png` today) and add its hash to the
   hash list, write `round2/motion/A3.txt`, one 6 s take ($0.60), read it frame by frame, judge at speed, place it.
2. The two picture sizes. 3. Hair at the top edge. 4. Length (18:07 as cut, or about 16:50: the five trims are listed on the page;
   picking it changes the first minute by 19 s, so show that minute again). 5. Gymboss screen recording. 6. The "$50" line.
7. Music bed. 8. No timer in the workout section.

Items 2 to 8 were asked in round 1 and again in round 2. Never infer approval from silence.

## Built in round 2 (do not apply twice)

- Corpus: three entries (`ro07-r1-first-minute-rejected-20261009`, `ro07-colour-D-approved-20261010`, `ro07-voice-4-approved-20261010`).
- Graphics: Dan's 16 capital changes, 16 more thinned, six keep one full caps word (G01, G06, G10, G12, G14, G27). G43 is G43A + G43B.
  All 47 lower thirds re-rendered (gap fix).
- Clips: opener from the top of each rep; C08 later squat reps; C18 jump rope = B0542, handles = `broll/handles_second.mp4`; C20 =
  B0458, B0449, B0450; C21 from 85.6 s; C22 = `broll/handles_first_rep.mp4`; C23 = `broll/pushups_regular.mp4`; C24 = B0433 (real knee
  push-ups). A1 removed. A2 motion placed.
- 10 new cutaways (C30 to C35, C37 to C39, C42: 8 of Dan's own B-roll, 2 library AI clips). Three more were built and cut after a look
  on screen (C36, C40, C41). Cover 20 % to 26 % (gate floor 40 %); more cover needs new stock (alarm clock, commute, couch, tired at night).

## Gates, stated honestly

Audio gate on the round 2 first minute: FAIL, one row of 13 (tone: mean 1.48 dB against 1.2, max 4.89 against 2.5, the top band
reads less treble than the reference). That is the voice Dan chose; nothing was tuned. Whole-film voice (`round2/voice/film_voice.wav`,
measured without a stamp): the same single row. Blind listen: the round 2 first minute and the approved audition "sound exactly the
same", both ahead of the round 1 sound; it also hears slightly clipped word endings from the dereverb, as it did on the audition he
approved. Nothing else has been gated. Round 1's first minute passed the audio gate 12 of 12 and was rejected: in the corpus as a finding.

## Next, once Dan replies

Record decisions with hashes. Apply his notes to `plan.py` (and `edl.py` if he picks the shorter length), re-resolve, re-render only
what changed, show only that. When nothing is pending: full film, music bed if chosen, subtitles, chapters, edit sheet, audio gate,
watch pass, one `ra-reviewer`, delivery gate, delivery folder `claude edited long form content/14 - Why You MUST Work Out Every Day/`,
queue `delivered`. When he finalizes: delete this video's copies from `Videos to Review/` and remove the 8857, 8858 and 8859 services.

## Cost ledger (cap $5 for this video, all rounds)

Replicate: $0.80 (A2). Gemini listens: about 5 cents in round 1b, about 2 cents in round 2. Codex: 8 images on the subscription.
Next expected: A3, one 6 s take, $0.60.

## Model and effort

Opus 5.5, high.

## Starter prompt

> Work Out Every Day LFC R3. CONTENT, long-form. Read `Handoffs/handoff-20261010-ro07-round2-dan-review.md` and the files it lists, then continue RO-07 with /longform-edit. My answers to the round 2 page are below. Record them in `round3-plan/decisions.json` with hashes first, build only what they change, and show me only that. If nothing is pending after my answers, build the full film and take it through every check. [paste the reply box from the round 2 page here]
