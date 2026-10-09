# RO-07 "Why You MUST Work Out Every Day": round 1 is with Dan (2026-10-09)

**CONTENT, long-form (LFC). Task name for the next session: `Work Out Every Day LFC R2`.**
Job doc: `Handoffs/video-editing/RO-07-why-you-must-work-out-every-day.md`. Rules: `Handoffs/video-editing/00-RULES.md`,
`.claude/skills/_shared/VIDEO-RULES.md`, `.claude/skills/_shared/PRE-RENDER-APPROVAL.md`. Skill: `/longform-edit`.

## Where it stands

Round 1 of the round method is delivered: the look, every graphic and clip, three AI frame pairs and the finished first
minute. **No full film exists yet, on purpose.** Nothing is approved until Dan replies.

- Review page: `http://localhost:8857/` (folder `/Volumes/Extreme/_edit_work/ro07/round1/`, generator `recipe/page.py`).
- VLC copy: `Videos to Review/Work Out Every Day LFC R1 - first minute.mp4`.
- Work dir: `/Volumes/Extreme/_edit_work/ro07/`. Recipe in git: `.claude/skills/longform-edit/reference/ro07/` (read its
  README first: order of scripts and every trap).

## Files to read first

1. `.claude/skills/longform-edit/reference/ro07/README.md`
2. `/Volumes/Extreme/_edit_work/ro07/recipe/edl.py` (the cut: 60 pieces anchored on phrases, each with its reason) and `plan.py`
3. `/Volumes/Extreme/_edit_work/ro07/round1/index.html` (what Dan was shown and asked)
4. `/Volumes/Extreme/_edit_work/ro07/round2-plan/round1-hashes.sha256` (re-hash before touching anything)

## What was built

- **Cut:** rolls C1484 (intro takes) and C1485 (body), 30:29 raw to 18:07. 60 pieces, 138 shots, 0 same-size joins
  (`build.py segs`). Lav is channel 1 on BOTH rolls (the C1484 sidecar says channel 0: wrong, see the recipe README).
- **Look:** three options A / B / C in `grades.json`; the first minute uses C (`look_option.txt`). Two sizes: W camera
  frame, T 1.3x. There was no approved look for this set (the job doc's "same set as V3" is wrong).
- **Graphics:** 45 lower thirds and 1 fact card from the approved HyperFrames templates (`hf/`), all rendered.
- **Clips:** 28. Dan's own poolside B-roll for this video (raw rolls C1490 to C1494, graded per roll), his library
  equipment B-roll, nine library stock clips, two library AI clips, one new Pexels clip (6322934, brushing teeth), the
  RO-06 phone demo, and three NEW AI clips that exist only as start / end frames (`aiframes/A1..A3-start/end.png`).
- **First minute:** `round1/first-minute/DRAFT - RO-07 round 1 - first minute.mp4` (64.7 s, sha256 starts `59ff56f27d4bfe3f`).

## Gate status, stated honestly

- Audio gate on the first minute: PASS, 12 of 12 (`.audio_gate.json` beside it). Voice only, no music bed yet.
- NOT run: the delivery gate, the edit sheet, the watch pass and the independent review. They need the full film.
- Known gap for the full film: cutaway cover is 21 % against the gate's 40 % floor. About 20 more cutaways are owed
  (Dan's own B-roll first, then library, then Pexels) and must be shown to Dan as new items in round 2.
- Hair: the camera left 20 to 45 px above his hair; it touches the edge for moments in six late shots (e3a, wr2, m4,
  out4, out5, e3c). Both sizes keep the camera's top row. Asked as decision 3.
- Lower thirds with two parts sit close together after punctuation (the known template spacing fault from RO-06).

## What Dan was asked (11 decisions; my recommendation first)

1 Colour (C). 2 Framing (approve). 3 Hair at the top edge (leave). 4 Length (B, about 16:50; the five trims are listed on
the page). 5 AI clips A1, A2, A3 (approve frames). 6 Opening (his B-roll, as built). 7 Gymboss on screen (he sends a
screen recording). 8 The "$50 for all that stuff" line (keep, no price on screen). 9 Knee push-up AI demo (keep). 10 Music
(quiet bed, as on RO-06). 11 Timer in the workout section (no).

## Authorizations

- **AI motion: NONE yet.** Do not generate motion for A1, A2 or A3 until Dan approves their frames in his reply. When he
  does: `recipe/gen_motion.py` (Veo 3.1 Fast, image + last_frame, about $0.10 a second), one take each, trim to the slot,
  never slow or hold. Frame hashes are in the hashes file; changed frames need approval again.
- Stock: Pexels and the library only. Images: Codex on the subscription only.

## Cost ledger (cap: $5 for this content video, all rounds)

- Replicate / AI motion: $0.00.
- Codex images: 7 (character sheet + three frame pairs), subscription, $0.
- Gemini listen (one call, intro takes and objections): a few cents, under the standing review authorization.
- Estimated next: three Veo takes, about $2.40 if all approved.

## Exact next action

When Dan replies: record every answer in `/Volumes/Extreme/_edit_work/ro07/round2-plan/decisions.json` (item, path,
sha256, verdict, his exact words, scope, next action, plus `motion_authorized` and `new_frames_before_motion`). Then, in
a new `round2/` folder: apply his look and length choices in `edl.py` / `look_option.txt`, generate only the approved AI
motion, add the owed cutaways and the music bed, rebuild the first minute if anything in it changed, and build the full
film only when nothing is pending. Then the edit sheet, audio gate, watch pass, one independent review (`ra-reviewer`),
the delivery gate, and the delivery folder `claude edited long form content/14 - Why You MUST Work Out Every Day/`
(master, `.srt`, chapters, notes, recipe, REVIEW 540p, audio A/B). Set the queue to `delivered` only then.

## Model and effort

Opus 5.5, high (routine organic long-form, per the model routing plan).

## Starter prompt

> Work Out Every Day LFC R2. CONTENT, long-form. Read `Handoffs/handoff-20261009-ro07-round1-dan-review.md` and
> `.claude/skills/longform-edit/reference/ro07/README.md`, then continue RO-07 with /longform-edit. My round 1 answers:
> [paste the reply box from http://localhost:8857/]. Record them in `round2-plan/decisions.json`, re-hash the round 1
> files, generate only the AI motion I approved, add the owed cutaways and the music bed, show me anything new, and build
> the full film only when nothing is pending. Then every gate, the independent review, and deliver master + SRT +
> chapters with the review copy.
