# CONTENT SFC: AI Homework SFC R2 (DS-31), colour options and the approved A1 opener

Rename the new task **AI Homework SFC R2**. Dedicated organic Short from 9/23 roll C1720. Recommended model: **Opus 5.5, high effort**.

## What Dan said on R1 (2026-10-17, verbatim)

> "Okay, revisions: the color correction looks off. Give me a few color correction options here. It looks a little bit too, or not warm enough. The colors aren't vivid and saturated enough. Give me some better color correction options. A1 is approved for the intro clip."

Recorded with hashes: `/Volumes/Extreme/_edit_work/ds31/round2-plan/decisions.json`.

- **A1 "Homework tower" frames are approved** for the opener (0:00-0:02.8, under "If you're in college and you have no time to work out"). It replaces the lecture-hall stock.
- **A2 "Furious professor" was not mentioned:** not approved. Do not generate it; the teacher stock stays.
- **Colour is reopened.** Color A (approved on DS-28, same roll) reads not warm enough and not vivid or saturated enough on this Short.
- **The spoken slip at 0:35** ("Run what it checks you through") got no answer: keep it as filmed (the recommendation).
- Everything else stands: cuts, captions, cards, B-roll picks, voice.

## State

- R1 work folder: `/Volumes/Extreme/_edit_work/ds31/round1/` (leave it untouched). Reviewed master `review/AI Homework SFC R1 - complete Short.mp4`, sha256 in decisions.json. Page http://127.0.0.1:8931/.
- Recipe (copy into `round2/`): `recipe/prep.py`, `audio_refit.py`, `aichat.py`, `picture.py`, `finish.py`, `gateplan.py`, `page.py`. Git copy and the traps this build hit: `.claude/skills/shorts/reference/ds31-ai-homework/README.md`. Read it first.
- Camera grade: `picture.py` applies `COLOR_A` (from `/Volumes/Extreme/_edit_work/ds28/round5/approved-color.json`) to every camera hold before graphics and captions. B-roll grades are per clip in `PLAN`.
- A1 frames: `round1/aiframes/A1-start.png`, `A1-end.png`, spec `A1.spec.json`; gate + reviewer PASS (`gate.py ... --verify` exits 0). Prompts `A1-start.txt`, `A1-end.txt`.
- Spend so far: $0 (frames on the ChatGPT subscription).
- Drive: the Extreme drive had about 5 GB free on 10-15. Keep scratch frames in /private/tmp.

## Round 2 steps

1. Claim: `python3 scripts/edit-queue/queue.py set DS-31 in_progress --by Claude`, mirror to the Edit Queue artifact db, update the board entry `DS-31`. Build in `/Volumes/Extreme/_edit_work/ds31/round2/`.
2. **Colour options (VIDEO-RULES, first-round options section: vary the requested property).** Make 3 or 4 grades that are warmer and more vivid/saturated than Color A at the **same brightness**, plus Color A for comparison. Show each on the same wide, tight and closing frames as stills and as one short moving sample with sound, with the measured numbers (median luma, median saturation, skin hue) beside each. Recommend one. Keep the blue light tubes reading as blue, skin natural (no orange cast). Also show how each sits next to the B-roll (B-roll is graded to sit with the presenter; re-check it against the pick).
3. **A1 motion on the Google Flow subscription** (VIDEO-RULES top section): queue it with `.claude/skills/_shared/veo/veo.py add` and spawn the `flow-veo` agent in the background (no paid Replicate unless Dan says rush). About 2.8 s used, generate one 8 s take. Run the motion gate (`_shared/framecheck/clipcheck.py` with `A1.spec.json`) and a fresh `frame-reviewer` with the three sense questions before the page shows it. Fix faults before Dan sees it (retake or trim). Label it AI-GENERATED, measured off his face.
4. Since colour and A1 are the only open items and the rest is approved, build the **whole Short** with the recommended grade and A1 in place (short-form whole-video rule), so Dan judges the colour in context. The page shows the colour options at the top with the recommendation already applied in the film; his pick of a different option is one camera re-render.
5. Exact-file gates (audio gate, `gateplan.py`, watch pass, fresh judge, delivery gate), one fresh independent audit, deliver: master, phone copy, SRT, audio A/B, stamps, notes, recipe; copy the full film to `Videos to Review/` and open it; refresh the 8931 page with `review_server.py` (same port). Give Dan exact timestamps for the changes (the grade is everywhere; A1 at 0:00-0:02.8).
6. `queue.py set DS-31 delivered` + artifact db. Commit recipe changes and the README traps with `safe-push.sh`.

Known gate rows to expect (not defects, never relax limits): audio tone (approved bass lift), framing head-size rows (Pair B wide keeps the lights), legacy caption-sync waveform row.

## Starter prompt

> Rename this task AI Homework SFC R2. Read `Handoffs/handoff-20261017-ds31-round2-color-options-and-a1-motion.md` and execute it. Dan approved A1 (homework tower) for the opener and wants warmer, more vivid and saturated colour options. Generate the A1 motion on the Google Flow subscription, build the whole Short with the recommended grade, show the colour options on the page, run every gate and an independent audit, and send me the review copy.
