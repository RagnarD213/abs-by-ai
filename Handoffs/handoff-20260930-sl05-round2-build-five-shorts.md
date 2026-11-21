# Handoff: SL-05 Stop Deadlifting shorts, round 2: build all five (2026-09-30)

## Goal
Build the five Stop Deadlifting shorts Dan picked, from the round-1 locks, all the way to review copies he can watch.
One round: plan every shot, render, gate, independent review, deliver, send Dan the review copies. Then stop.

## Read first
`Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md`, `Handoffs/video-editing/SL-05-stop-deadlifting-shorts.md`,
`.claude/skills/shorts/SKILL.md` (Steps 3-10.2 and the gate section), `.claude/skills/shorts/reference/zeeshan-master/README.md`
(all three SL-04 rounds), then `/Volumes/Extreme/_edit_work/sl05/build/r1/NOTES-round2-prep.md` (every measurement from round 1).

## Locked in round 1 (`/Volumes/Extreme/_edit_work/sl05/round2-plan/decisions.json`, hashes and Dan's words)
1. **Colour A** on Dan's own footage only (`render.js` `GRADE_A`, BT.709 RGB curve + saturation 1.4). Zeeshan's stock and
   AI shots keep his grade (`grade: 'none'` on the shot). Re-measure each rendered short; the sample read picture
   0.290/0.333, skin 0.35/0.39. If a shot drifts orange or crushed, trim that shot's saturation, never the whole short.
2. **Title style A**: the SL-04 J2 band (flush frame, no scrim, title held the whole short, picture from y310).
3. **Audio**: Zeeshan's stereo mix, cut only, 15 ms de-click fades, AAC 320k, `audio_gate.py --verbatim` against his
   same cut (Dan: "Just use whichever one you think is best"; both halves of the A/B were the same mix).
4. **Hair framing accepted** (Dan: "I'll accept the hair framing. I guess we have no choice about that."). Declare
   `hair_top` per build in `gate/<S>/declare.json` citing decisions.json; hair at source row 0 on 751/783 talking frames.
5. **Title copy: NOT answered.** Use the draft in `plan.js` META and list it in the delivery notes and "What I decided"
   so Dan edits on the review copies. Do not call it approved.

## Where the build stands (`/Volumes/Extreme/_edit_work/sl05/build/`)
- `segments.js`: all five shorts measured and splice-tested (S1 57 s, S2 51, S3 48, S4 59, S5 38). `joinShortEnd: true`.
  `SL05_SAMPLE=1` is only the round-1 sample; run the real build WITHOUT it.
- `plan_shots.py`: only S1's first two shots exist. **Plan every shot of all five** from `work/shots_all.json`,
  `work/gfx5.json`, `hair/*.json`, `work/headx.py`, following the round-1 "What I decided" list:
  - Talking shots with no Zeeshan pill: `full` 724x1080 window from row 0, steady per shot, centred on the head.
  - While a KEY POINT or exercise pill is up: card of rows 0-778 (`cardCrop [0,1,0,0.72]`, cardY 420) with his exact
    words re-set in his olive pill on the black field under the card (`pill/make_pill5.py`, add every pill; texts in
    `r1/pills/all.png`, wrap to fit 1040 px). Card starts on a picture cut where possible and ends ~1 s after his fade.
    Two cards back to back share one box.
  - AI clips and stock inserts: whole-frame card so "AI Generated" is never cropped (SL-04 card rules).
  - Zeeshan's zoom blurs: `holdHead`/`holdTail` <= 7 frames (S2 at 240.74-240.907, S4 end 369.17-369.38); keep the
    silent flash at 384.22. Check the S2 cut pair 271.37/271.605 and S4 398.77/398.905 on the picture.
  - S5 junk cut 463.70/464.05: confirm Zeeshan's medium-to-close change covers it; if not, a real size step.
- **Standing rule since 09-30 (memory `shorts-show-whole-exercise`)**: when a short tells the viewer to do an exercise,
  show a few complete reps. S4: T-bar row (374.1-379.2), barbell row (379.2-384.2), lat pulldown (412.7-417.8);
  S5: leg press (439.5-448.8). Check that each exercise is on screen near where Dan names it.
- `overlays.json` has only S1-kp1 (sample timing 7.82-8.94); rebuild it for all five from the plan.
- `r1/wait_sample.sh` miscounts other sessions' zsh wrappers as builds; check `ps` by eye instead.

## Steps
1. Machine cap: at most two video builds across sessions (`ps -Ao pcpu,command | grep -E 'ffmpeg|whisper|render|gate\.py'`,
   ignore `/bin/zsh -c` wrapper lines). Never run anything inside `/Volumes/Extreme/_edit_work/sl04/`.
2. Plan all five, `./build.sh S1 S2 S3 S4 S5`, look at every short's contact sheet and every cut's boundary frames.
3. Cut-continuity pass (`_shared/CUT-CONTINUITY-QC.md`) on the exact candidates.
4. Deliver: adapt `deliver.sh`/`deliver_all.sh` names to `Short-form video content/stop-deadlifting-short<N>_<slug>.mp4`
   (slugs in segments.js), audio gate `--verbatim --ab`, delivered ASR + CTC, `make_plan.py`.
5. `watch.py` on each, fresh-subagent judge, `watch.py --judge`, `gate.py --format short` PASS at the current GATE_VERSION.
6. Independent Opus reviewer (fresh subagent, `ra-reviewer` style) watches the delivered files; expect DOES NOT SHIP the
   first time; fix and re-review (SL-04 needed three rounds).
7. REVIEW 540p copies + A/B clips in `Short-form video content/stop-deadlifting REVIEW/`, `stop-deadlifting-SHORTS.md`
   (each short's in/out, title, parent, notes, draft title copy for Dan to edit), queue:
   `python3 scripts/edit-queue/queue.py set SL-05 delivered` + the Edit Queue artifact write_db.
8. Put new traps in `.claude/skills/shorts/reference/zeeshan-master/README.md` and copy the working SL-05 scripts back
   into the skill reference (git, not media). Update the board line; send Dan the review copies and a numbered action list.

## Constraints
No covers (Codex). No upload, no Blotato: the parent goes public Sun Oct 11 and shorts follow it. No AI generation
planned ($0 spent). No em dashes (grep every note and message). Zeeshan's audio never processed.

## Recommended model
**Opus 5.5, high effort** (SL jobs are Claude secondary cuts; memory `model-routing-plan`).

## Starter prompt
> Read `Handoffs/handoff-20260930-sl05-round2-build-five-shorts.md` and everything it lists, then build all five SL-05
> Stop Deadlifting shorts from the round-1 locks (colour A, J2 title band, Zeeshan's audio untouched, hair framing
> accepted): plan every shot, render, gate, independent review, deliver the review copies to me with the draft title
> copy for me to edit.
