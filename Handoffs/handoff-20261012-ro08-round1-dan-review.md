# RO-08 "Intermittent Fasting: The Best Way To Get Abs": round 1 is with Dan (2026-10-12)

**CONTENT, long-form (LFC). Task name for the next session: `Intermittent Fasting LFC R2`.**
Job doc: `Handoffs/video-editing/RO-08-intermittent-fasting.md`. Rules: `Handoffs/video-editing/00-RULES.md`,
`.claude/skills/_shared/VIDEO-RULES.md`, `.claude/skills/_shared/PRE-RENDER-APPROVAL.md`. Skill: `/longform-edit`.

## Where it stands

Round 1 of the round method is delivered: the finished first minute, every graphic and clip, eight AI frame pairs and
three voice options. **No full film exists yet, on purpose.** Nothing is approved until Dan replies.

- Review page: `http://localhost:8869/` (folder `/Volumes/Extreme/_edit_work/ro08/round1/`, generator `recipe/page.py`).
- VLC copy: `Videos to Review/Intermittent Fasting LFC R1 - first minute.mp4`.
- Work dir: `/Volumes/Extreme/_edit_work/ro08/`. Recipe in git: `.claude/skills/longform-edit/reference/ro08/` (read its
  README first: order of scripts and every trap). It starts from `reference/ro07/` (same set, same shoot).

## Files to read first

1. `.claude/skills/longform-edit/reference/ro08/README.md`, then `reference/ro07/README.md` (rounds 2 and 3: motion, bed, full film, finish chain)
2. `/Volumes/Extreme/_edit_work/ro08/recipe/edl.py` (the cut: 41 pieces anchored on phrases, each with its reason) and `plan.py`
3. `/Volumes/Extreme/_edit_work/ro08/round1/index.html` (what Dan was shown and asked)
4. `/Volumes/Extreme/_edit_work/ro08/round2-plan/round1-hashes.sha256` (re-hash before touching anything)

## What was built

- **Cut:** roll C1486, 23:06 raw to 14:41. 41 pieces, 104 shots, 137 picture segments, 0 same-size joins, longest hold
  21.7 s (`build.py segs`). Lav is channel 1 (the roll sidecar said channel 0: wrong, see the recipe README).
- **Look:** colour D, Dan's RO-07 pick, reused after a source check (the roll measures the same). Two sizes: W camera
  frame, T 1.3x.
- **Voice:** RO-07's voice 4 plus a +1 dB bass lift at 120 Hz (`build.py`, `RO08_BASS_DB`). Film voices on disk:
  `voice/film_voice.wav` (+1 dB, used), `film_voice_nobass.wav`, `film_voice_bass3.wav`. Bed: `bed/bed.wav` at -30 dB.
- **Graphics:** 48 lower thirds from the approved HyperFrames template (`hf/`), all rendered. Title capitalisation, no
  full-caps words. No side cards, no title cards, no fact cards.
- **Clips:** 39. Dan's own footage (library B0542, B0438, B0427, B0431, B0453; three shots cut from the approved salad
  film's graphics-free base, `broll/salad_*.mp4`), library stock and one library AI clip (A0158), 19 new Pexels clips
  (`stock/px_<id>_*.mp4`), the RO-06 phone demo, and eight NEW AI clips that exist only as start / end frames
  (`aiframes/A1..A8-start/end.png`, prompts in `aiframes/prompts/` and in the repo recipe).
- **First minute:** `round1/first-minute/DRAFT - RO-08 round 1 - first minute.mp4` (65.6 s, sha256 in the hashes file). The framing solve Dan saw is saved as `round2-plan/segs.round1.json` (pin it with `build._R2` before any plan change).

## Gate status, stated honestly

- Audio gate on the first minute: 12 of 13 rows pass. The tone row fails (mean 1.7 dB against 1.2): it fails on any fixed
  tone shape, and this is the voice Dan chose on this set. Reported, not tuned.
- NOT run: the delivery gate, the edit sheet, the watch pass and the independent review. They need the full film.
- Cutaway cover is about 21 % against the gate's 40 % floor (RO-07 was approved at 27 %). Said on the page.
- Hair: the camera left about 14 px above his hair (median) and it touches the top edge for moments in most shots. Both
  sizes keep the camera's top row. Asked as decision 5.
- SRT: three one-syllable take openers ("The", "In") are missing from `words_out.json`. Build the SRT with the RO-07
  round 3 method (diff against a transcription of the finished film).

## What Dan was asked (6 decisions; my recommendation first)

1 AI clips A1 to A8 (approve the ones he likes; all eight cost about $6.20, over the $5 cap, so drop two or raise to $7).
2 Opening (his own footage for the first sentence, as built). 3 Voice (1: +1 dB bass). 4 Length (keep 14:41). 5 Hair at
the top edge (leave as shot). 6 The app at the end (lower third as built, or the RO-06 phone tour beside him).

## Authorizations

- **AI motion: NONE yet.** Do not generate motion for any of A1 to A8 until Dan approves that clip's frames in his
  reply. When he does: `recipe/gen_motion.py` (Veo 3.1 Fast, image + last_frame, about $0.10 a second), one take each,
  trim to the slot, never slow or hold. A1 and A2 are his excuse voice: lip sync the speaking man to Dan's own recording
  (`recipe/lipsync.py`, the RO-06 round 4 method in `reference/ro06/README.md`). Changed frames need approval again.
- If A5 (the donut food coma) is approved, remove C22 (the stock man asleep at his desk) from `plan.py`.
- The $5 per video cap stands unless his reply raises it.
- Stock: Pexels and the library only. Images: Codex on the subscription only.

## Cost ledger (cap: $5 for this content video, all rounds)

- Replicate / AI motion: $0.00.
- Codex images: 16 (eight frame pairs; the character sheet is RO-07's), subscription, $0.
- Gemini listens: two short calls (intro takes; voice options), a few cents, under the standing review authorization.
- Estimated next: up to eight Veo takes ($5.20) plus two lip syncs (about $1.00) if all are approved and the cap is raised.

## Exact next action

When Dan replies: record every answer in `/Volumes/Extreme/_edit_work/ro08/round2-plan/decisions.json` (item, path,
sha256, verdict, his exact words, scope, next action, plus `motion_authorized` and `new_frames_before_motion`). Re-hash
the locked files against `round2-plan/round1-hashes.sha256`. Then, in a `round2/` folder: generate the approved motion,
apply his graphic and clip notes in `plan.py`, re-resolve, re-render only the changed lower thirds
(`from_plan.py --render`), pin the framing solve (`build._R2`, the RO-07 round 3 method), and, if nothing is pending,
render the full film with the bed, run the finish chain (audio gate, transcript, SRT, chapters, watch pass, hair and
graphics checks), one independent `ra-reviewer`, the edit sheet and the delivery gate, then the round page with exact
timestamps of every change. Chapters must not repeat V3's fasting tips (tips 5 and 6 of "My Top 10 Tips"). When Dan
finalizes: mark the footage ranges used on the roll sidecar, register the new clips in the clip library, set the queue
to `finalized`, add the Shorts job (List 2) to `00-MASTER.md`, and delete the VLC copies.

The C1486 roll sidecar was rebuilt on 2026-10-12 with the correct lav (channel 1).

## Starter prompt

Model: **Claude Opus 5.5, high effort** (routine long-form round; Fable only if this round fails twice).

> Intermittent Fasting LFC R2. CONTENT, long-form. Read `Handoffs/handoff-20261012-ro08-round1-dan-review.md` and
> `.claude/skills/longform-edit/reference/ro08/README.md`, then run round 2 of RO-08 with /longform-edit. My round 1
> reply is below: record it word for word in `round2-plan/decisions.json`, generate motion only for the AI clips I
> approved, apply my notes, and if nothing is pending build the full film, run every gate and the independent review,
> and send me the review page with timestamps. Rename this task `Intermittent Fasting LFC R2`.
>
> [paste the reply from the review page here]
