# RO-08 "Intermittent Fasting: The Best Way To Get Abs": round 2, AI motion and the full film (written 2026-10-12)

**CONTENT, long-form (LFC). Task name for the next session: `Intermittent Fasting LFC R2`.**
Job doc: `Handoffs/video-editing/RO-08-intermittent-fasting.md`. Rules: `Handoffs/video-editing/00-RULES.md`,
`.claude/skills/_shared/VIDEO-RULES.md`, `.claude/skills/_shared/PRE-RENDER-APPROVAL.md`. Skill: `/longform-edit`.

## Where it stands

Dan reviewed round 1 on 2026-10-12 and answered in four messages, all recorded word for word in
`/Volumes/Extreme/_edit_work/ro08/round2-plan/decisions.json`. **No full film exists yet.** Spend so far: $0. Dan answered a fourth time on the frames and the budget; see below.

- Round 1 page (first minute, every graphic and clip): `http://127.0.0.1:8869/`
- Notes page (opener frames, new A6 end frame, voice options, B-roll colour): `http://127.0.0.1:8870/`
- Work dir: `/Volumes/Extreme/_edit_work/ro08/`. Recipe in git: `.claude/skills/longform-edit/reference/ro08/` (README
  first), on top of `reference/ro07/` (same set, same shoot; its rounds 2 and 3 are the model for this round).

## Locked (Dan's words are in decisions.json)

- **The cut** (14:41, 41 pieces), colour D, the two sizes, hair as shot, the 48 lower thirds, the lower third for the app
  at the end, every cutaway he did not name: "Everything else is looking good."
- **Voice 1a**: "Let's go with 1A for the sound." Voice 4's EQ + 1 dB at 120 Hz, dereverb alpha 0.35 / floor -11 dB, no
  expander. It is in `recipe/build.py` (`VOICE4`, `--dereverb`), and `voice/film_voice.wav` is already the whole film in
  1a (correlation 0.9994 with the audition clip he picked). Bed: `bed/bed.wav`, -30 dB.
- **B-roll colour**: "B-roll color is looking good." C38 is library B0030; `broll/B0431_bright.mp4`, `B0453_bright.mp4`,
  `salad_bowl2_bright.mp4`, `salad_dish_bright.mp4` (curves in `round2-plan/broll_grades.json`). Already in `plan.py`.
- **The opener**: the workout B-roll is out. The AI opener `OT` (his own idea, the workday fast time-lapse) has its five
  key frames approved: "The workday fast looks good." It is in `plan.py` as a pending clip over the first sentence (0 to 7.7 s).
- **AI frames approved**: A1 to A5 ("looking good"), A6 with the new end frame `aiframes/A6-end-r2.png` ("A6 looks good").

## Settled by Dan on 2026-10-12 (nothing is open)

- **AI budget: $15 for this video.** "For the budget, let's do $15." It replaces the $5 content cap for RO-08 only, all
  rounds. Estimated use: about $8.85 (A1 to A6 with two lip syncs $4.85, the time-lapse opener $1.80, A7 and A8 $1.40,
  idea 6 $0.80). The rest is room for retakes; keep the ledger and report the total.
- **Opener idea 6** (split screen, same man two mornings): the redrawn frames are approved ("starting frames are looking
  good"): `aiframes/O6-start-r3.png`, `O6-end-r3.png` (left man visibly overweight, right man lean in a tank top).
  **Make both openers** (OT and O6) and show Dan both moving at the head of the first minute; he chooses. The plan
  carries OT; O6 uses the same slot (0 to 7.7 s).
- **A7 and A8:** treated as approved from "Everything else is looking good" (said to him three times, no objection).

## What to build

1. Re-hash against `round2-plan/round2-start-hashes.sha256` (the state at this handoff: approved frames, voice 1a, brightened B-roll, plan). `round1-hashes.sha256` is what Dan saw on the round 1 page (the first minute, plan and film voice have changed since by
   Dan's notes: record expected against actual, do not treat those as faults). Pin the framing solve Dan saw:
   `round2-plan/segs.round1.json` into `build._R2` (the RO-07 round 3 method) before any plan change.
2. **Motion** (`recipe/gen_motion.py`, Veo 3.1 Fast, image + last_frame, about $0.10 a second; never slow or hold a clip):
   - A1, A2: his excuse voice. Motion from the frame pair, then lip sync the speaking man to Dan's own recording
     (`recipe/lipsync.py`, the RO-06 round 4 method in `reference/ro06/README.md`).
   - A3 to A8 (A6 uses `A6-end-r2.png`). When A5 is in, delete C22 from `plan.py`.
   - **O6, the split screen:** one 8 s move from `O6-start-r3.png` to `O6-end-r3.png`, trimmed to the slot. Both halves must keep their own man: read the take for the faces swapping or the divider line bending.
   - **OT, the time-lapse:** three moves, OT-1 to OT-2, OT-2 to OT-3-r2, OT-3-r2 to OT-4 (4 s each), sped up to about
     one second each (speeding up is allowed), then OT-4 to OT-5 at normal speed for the rest of the 7.7 s slot. Check
     the clock hands and the coffee level run forwards at every join, and read every frame for AI faults at playback speed.
3. `resolve.py`, `from_plan.py --render` (nothing should re-render), then the first minute with the opener, the full
   film with the bed (`render_r3.py` pattern), the finish chain (audio gate, transcript, SRT by diffing against a
   transcription of the finished film, chapters, watch pass, hair and graphics checks), one independent `ra-reviewer`,
   the edit sheet, the delivery gate.
4. Round 2 page on a new port: the first minute with the opener, each AI clip moving in context, the full film, and a
   list of every change since round 1 with exact timestamps. Copy the full film and the first minute to
   `Videos to Review/` and remove the round 1 copy.

## Gate status, stated honestly

- First minute (round 1 build): audio gate 12 of 13; the tone row fails on any fixed voice shape. Expect the same on the film.
- Not run yet: delivery gate, edit sheet, watch pass, independent review.
- Cutaway cover about 22 % against the gate's 40 % floor (RO-07 was approved at 27 %). Dan saw the number and asked for nothing.
- Hair touches the top edge for moments in most shots (the camera left about 14 px). Dan was asked and raised nothing: as shot.
- SRT: three one-syllable take openers are missing from `words_out.json`; use the finished-film diff.
- Chapters must not repeat V3's fasting tips (tips 5 and 6 of "My Top 10 Tips").

## Cost ledger (cap: $15 for this video, set by Dan on 2026-10-12)

- Replicate / AI motion: $0.00.
- Codex images on the subscription: 28 (16 for A1 to A8, 1 A6 end redo, 5 time-lapse frames + 1 redo, 4 for idea 6 over two versions + 1 clock fix).
- Gemini: three short listens (take choice, voice, first-minute check) and one roll description, a few cents.

## When Dan finalizes

Mark the footage ranges used on the C1486 sidecar, register the new clips in the clip library, set the queue to
`finalized`, add the Shorts job (List 2) to `00-MASTER.md`, delete the VLC copies and remove the review services on
ports 8869 and 8870 (`review_server.py PORT --remove`).

## Starter prompt

Model: **Claude Opus 5.5, high effort** (routine long-form round; Fable only if this round fails twice).

> Intermittent Fasting LFC R2. CONTENT, long-form. Read `Handoffs/handoff-20261012-ro08-round2-motion-and-full-film.md`
> and `.claude/skills/longform-edit/reference/ro08/README.md`, then run round 2 of RO-08 with /longform-edit: generate
> the approved AI motion (both openers, the time-lapse and the split screen, plus A1 to A8 and the two lip syncs) inside
> the $15 budget I set, build the full film, run every gate and the independent review, and send me the review page
> with timestamps and both openers to choose from. Rename this task `Intermittent Fasting LFC R2`.
