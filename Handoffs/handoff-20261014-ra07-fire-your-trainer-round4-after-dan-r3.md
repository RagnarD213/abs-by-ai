# RA-07 "Fire Your Trainer!": round 4 (the three fix clips after Dan's answers, then the 16:9)

**AD (short-form, filmed).** Sidebar name for the next task: `Fire Your Trainer AD R4`.
Written 2026-10-14 by the round 3 session (Claude Opus 5.5). Job doc: `Handoffs/video-editing/RA-07-fire-your-trainer.md`.
Round 3 page: http://127.0.0.1:8847/ (served from `/Volumes/Extreme/_edit_work/ra07/round3/page/`). Recipe:
`.claude/skills/ad-edit/reference/ra07/round3/`, lessons in `/ad-edit` "RA-07 round 3 lessons" (read them first: they cost a day).

## Where round 3 left it

The whole 9:16 is delivered (`Claude Ad Videos/fire your trainer - RA-07/fire your trainer | claude | 9x16 | RA-07.mp4`, 52.7 s;
first 30.13 s frame-identical to the approved round 2 build; mix sample-identical to `mix_bass.wav` before 51.76 s). Plan as built:
`/Volumes/Extreme/_edit_work/ra07/beats_r3_dan.json` (env `I3B=dan`, `I2` defaults to camera in `s70r3_plan.py`).

| slot | time | state |
|---|---|---|
| I2 same sheet | 31.63-34.30 | **camera.** No 1.2 s window of `round2/motion/I2_v3.mp4` passes the take review (phantom shoe f0-8, ghost head f9-10, paper turns to cloth f33 on). Needs a retake from round 1's frames. |
| I3a tweaked shoulder | 36.47-37.87 | clip, `I3a_v1` f13-47, clipcheck + review PASS |
| I3b shoulder fix | 37.87-39.21 | **camera until Dan says yes** to `round3/frames/I3b-end_v13.png` (start of the lateral raise, arms down, pads on the outside of the elbows; gate + reviewer PASS). Then: single-image take (start = end = v13, or start-only), "raises both arms out to the sides to shoulder height and lowers them", clipcheck + reviewer, 40 frames. |
| M1 home curls | 39.21-40.44 | library clip, label moved off his face |
| I4a out of order | 40.44-42.11 | clip, `I4a_v1` f56-96, PASS |
| I4b hack squat | 42.11-44.01 | clip, `I4bW_v1` f22-67 (nod, towel, steps on), PASS. **The lift itself is missing.** Two rep takes failed (start = end barely moves; start-only moved the foot platform: a leg press). |
| I5 back next week | 44.01-47.01 | clip, `I5_v1` f25-96, PASS |

Gates on the delivered file: see the page "Checks". Known: audio `tone` max 2.86 dB (Dan's bass lift); `captions:sync` one miss,
"20" at 21.3 s lights 0.2 s early, inside the approved first 30 s (left untouched by Dan's instruction; fix only if he says so).

## Round 4, in order

1. **Read Dan's reply on the round 3 page** (I3b yes/changes, budget, film notes). Record his words in `round4-plan/decisions.json`.
2. **Budget:** spent $10.00 of the $10 cap (`round2/motion/ledger.json` + `round3/motion/ledger.json`). The page asks to raise it to
   $20. No take without his number.
3. **I3b:** after his yes, the motion (step above). Every take: `clipcheck.py` over the used frames + a fresh `frame-reviewer`, then
   swap into the plan (`I3B=clip`), re-render that one slot.
4. **I4b lift:** a separate short shot cut in after the step-on (e.g. 42.11-43.0 walk-on, 43.0-44.01 the rep). Do not rely on a
   single-image take; generate a START/END pair of the rep from the same camera (derive END from START with Codex `--image`, fix the
   machine geometry in code if needed, `framecheck/README.md` rule 5) and gate both frames first. The rep needs the sled and back pad
   moving on fixed rails and a fixed foot platform.
5. **I2:** retake from `round1/frames/I2-start.png` / `I2-end.png` (round 2's prompt in `gen_motion.py`), then clipcheck + reviewer.
   Run the take review BEFORE building (lesson 4).
6. **Re-render** the 9:16 (`s86r3_assemble.py` with the matching `PLAN`/`SEG`), then `round3/chain_v4.sh`-style chain, plan
   (`s93r3_gateplan.py`), watch + fresh judge, delivery gate, fresh `ra-reviewer`. Deliver, update the page, edit queue `delivered`.
7. **Then the 16:9** from the same cut and sound (handoff 2026-10-14 step 8: edit sheet, gate, watch, review). It was deferred this
   round because the 9:16's clip slots are still changing.

## Recommended model

Claude Opus 5.5, high effort. Escalate to Fable 5.1 only for a clip Opus fails twice.

## Starter prompt

> AD. Rename this task `Fire Your Trainer AD R4`. Read `Handoffs/handoff-20261014-ra07-fire-your-trainer-round4-after-dan-r3.md` and run round 4 of RA-07 "Fire Your Trainer!" with /ad-edit: my answers on the round 3 page are below. Make the shoulder fix and the hack squat lift, retake the same-sheet clip, re-render the 9:16 with every gate, the watch pass and the independent review, deliver it and send me the page. Then the 16:9. Shoulder fix frame: [yes / changes]. AI clip budget: [$20 / other]. Film notes: [none / list]. Use the Codex subscription to generate any new images.
