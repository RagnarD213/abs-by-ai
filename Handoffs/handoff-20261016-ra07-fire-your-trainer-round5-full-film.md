# RA-07 "Fire Your Trainer!": round 5 (motion for the two new clips, then the full film)

**AD (short-form, filmed).** Sidebar name for the next task: `Fire Your Trainer AD R5`.
Written 2026-10-16 (Claude Opus 5.5) after Dan reviewed the round 4 page and said: *"Everything is looking good. Give me the
handoff document to make the full film in the next round."* Job doc: `Handoffs/video-editing/RA-07-fire-your-trainer.md`.
Dan's words, the approved frames with sha256: `/Volumes/Extreme/_edit_work/ra07/round5-plan/decisions.json`.
Round 4 page (his review): http://127.0.0.1:8856/. Recipe: `.claude/skills/ad-edit/reference/ra07/round4/` and the "RA-07 round 4
lessons" in `.claude/skills/ad-edit/SKILL.md` (read both, plus the round 3 lessons right above it). Work: `/Volumes/Extreme/_edit_work/ra07/`.

## What Dan approved (round 4)

I read "everything is looking good" as a yes to: the two new frame pairs, the order and slot times of the injury run, and the
broken-arm clip as cut. Anything he did not mention is unchanged.

| slot (film time, frames) | clip | status |
|---|---|---|
| A1 36.47-38.54 (62 f) | library clip A0179, frames 0-33 then 101-128 | DONE, reviewed (clipcheck + fresh reviewer PASS). Built in `round4/clips/A1.mp4`. |
| **G1 38.54-39.81 (38 f)** | NEW "Gym closed" | **frames approved, motion to make** |
| M1 39.81-41.01 (36 f) | library A0039 home curls | done, unchanged |
| **O1 41.01-42.41 (42 f)** | NEW "Leg press out of order" | **frames approved, motion to make** |
| H2 42.41-44.01 (48 f) | `round3/motion/I4bW_v1.mp4` from 1.17 s | DONE, reviewed (PASS f28-66) |
| I5 44.01-47.01 (90 f) | round 3's file, unchanged | done |

Approved frames (both pass `framecheck/gate.py --verify`, gate + fresh reviewer):

- **G1:** START `round4/frames/GC-start_v2.png` (man walks up to a glass gym door with a CLOSED sign), END `GC-end_v3.png` (stopped, both palms
  up, shoulders dropped). Spec `GC.spec.json`.
- **O1:** START `round4/frames/LP-start_v1.png` (same man as the hack squat, walks up to a plate-loaded leg press with an OUT OF ORDER sign
  on the backrest), END `LP-end_v4b.png` (glances back over his shoulder, small shrug; feet, hips and arms unchanged). Spec `LP4b.spec.json`.

The built film with the two placeholders is `round4/work/picture_9x16.mp4` (1579 frames); its first 30 s are md5-identical to round 2.
Audio is `round3/mix_bass_r3.wav` (approved voice, bass lift, round 3's smoothed music tail). Do not touch it.

## Budget

Dan set **$20** for RA-07 AI clips (2026-10-16). $10.00 spent before round 4, round 4 spent $0. So **$10 left**: two new clips at about $1
a take (Kling v3 standard) leave room for retakes. Retakes of approved frames need no question; at the cap, ask for more FIRST and
alone, with the number, and never ship a faulty clip (VIDEO-RULES, 2026-10-13).

## Round 5, in order

1. **Motion for G1 and O1** with `round3/motion/gen_motion3.py` as the model (copy to `round5/` or `round4/motion/`): Kling v3 standard,
   START + END image, `require_pass()` first. Both pairs have the SAME FEET in START and END (the gate needs it), so the model must supply the last
   half step on its own. Write that in the prompt ("he takes a last short step, then stops"), and watch for feet that slide or skate: that is the
   likeliest fault. G1 slot is 1.27 s, O1 is 1.4 s, so a 4 s take with a clean 1.3-1.5 s window is enough. The AI-GENERATED label goes on both
   (chip placed by person mask, as `s75r4_clips.py` does for the others).
2. **Each take through the motion gate before anyone sees it** (VIDEO-RULES 2026-10-13/14): `clipcheck.py TAKE --spec spec.json --frames A:B`
   on the part the edit uses, a fresh `frame-reviewer` agent with the three sense questions, `clipcheck.py ... --verify`. Also read the take's
   first and last second frame by frame (Veo/Kling faults live there) and look for a baked cut. A failing take is retaken or cut down to the part
   that passes. If a clip cannot be made to pass inside the budget, put Dan on camera in that slot (his own rule: the camera scene is always
   acceptable) and say so in one line.
3. **Re-lay and build the whole 9:16** from the round 4 recipe: add `G1` and `O1` to `SRC` in `s75r4_clips.py` (with the chosen in-points),
   set `PENDING = set()` in `s70r4_plan.py` and `s86r4_assemble.py`, re-run plan, clips, `work`. Every Dan hold is reused (`round4/seg/`).
   The first 30 s must stay md5-identical (the chain checks it). `chain_all.sh` is the queue-and-wait wrapper (two-build cap: other sessions
   render for long stretches).
4. **Then the gates on the exact delivered file, as round 3 did** (`round3/chain_v3.sh`, `s93r3_gateplan.py`, `s88r3_checks.py`,
   `s92r3_chips.py`, `s96_ctc1.py`, `s91_tail07.py`): the round 3 scripts still name the old clips. Edit `s93r3_gateplan.py` line 56
   (`CLIPS` becomes `H1 A1 G1 M1 O1 H2 I5`, files under `round4/clips`, plan `beats_r4.json`) and `s92r3_chips.py` (chips from `round4/clips/*_chip.png`;
   A1 has two, `A1_p0_chip.png` and `A1_p1_chip.png`, at the same spot). Known and accepted: the audio gate's `tone` row fails on any fixed tone
   shape (the bass lift); say it plainly, do not tune it. Then the watch pass (`deliver/watch.py`) and one fresh `ra-reviewer` on the delivered file.
5. **Deliver the 9:16:** `Claude Ad Videos/fire your trainer - RA-07/fire your trainer | claude | 9x16 | RA-07.mp4`, the page (reuse port 8856 and
   its folder, run `review_server.py 8856 ...` again to refresh its cache), `Videos to Review/Fire Your Trainer AD R5 - whole 9x16.mp4`
   (replace the R4 copy, delete the R3 copy), edit queue `delivered`, and the later-round revision list in chat with exact timestamps
   (what changed: G1 and O1 slots now moving; everything else as Dan saw it).
6. **The 16:9 comes after Dan approves the 9:16** (SKILL: do not double every revision render): edit sheet, gate, watch, review from the same cut and
   sound. Do not start it in this round unless Dan says the 9:16 is approved.

## Facts and traps to carry

- A0179's usable windows are frames 0-34 and 101-128 only. Windows 32-67 and 8-43 failed review (no head shake that reads, a smeared phone out of the
  pocket, arm rising to the hip from frame 35). The clip's scene change is between frames 100 and 101 (found by frame difference, not the 3 fps sheet).
- A mid-stride START and a standing END fail the bone gate; the fix that passed was "both feet stay exactly where they are, only the upper body changes".
  Dan has not asked for a palm-up shrug on O1; the approved END is the head turn and shoulder lift.
- The placeholder band covered the sign and machine in the context clips; it disappears this round, so nothing to fix.
- Still open from round 3, not in this round: the hack squat lift and the same-sheet clip (I2, currently Dan on camera 31.63-34.30). Say so in the
  delivery note and ask Dan once if he wants them next.
- No em dashes anywhere; title-case graphics; no AbsByAI.com mark at the end; AI-GENERATED chip not over faces; never publish the ad organically
  (upload and setup is a separate `/ad-setup` task after Dan finalizes).

## Recommended model

Claude Opus 5.5, high effort. Escalate to Fable 5.1 only for a clip or a review Opus has failed twice.

## Starter prompt

> AD. Rename this task `Fire Your Trainer AD R5`. Read `Handoffs/handoff-20261016-ra07-fire-your-trainer-round5-full-film.md` and run round 5 of RA-07 "Fire Your Trainer!" with /ad-edit: make the motion for the approved gym-closed and leg-press-out-of-order frames (each take through clipcheck and a fresh reviewer before I see it), build the whole 9:16 with both clips in, run every gate, the watch pass and the independent review, and send me the page with a timestamped list of what changed. AI clip budget: $20 total, $10 already spent. Use the Codex subscription for any new images.
