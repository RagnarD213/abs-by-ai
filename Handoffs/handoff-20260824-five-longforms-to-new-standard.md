# Handoff: bring the five delivered longforms up to the new /longform-edit standard

**Date:** 2026-08-24
**Project:** Abs By AI — longform content pipeline
**Why this exists:** Dan's Phase C answer, 2026-08-24 — *"Create a handoff document to rebuild the file, which I will execute if I have extra limit remaining on my subscription this week."*
**Business goal:** the channel's first five videos should look like they came from the same show as the sixth.

## Objective

Apply the style standard that `/longform-edit` now enforces (`reference/qc_style.py`, 13 hard
failures) to the five longforms already delivered in
`claude edited long form content/`. The ab-wheel rebuild of 2026-08-24 is the worked
example; every script it used is in `reference/` and is documented in that folder's README.

**None of these five is published yet.** There is no urgency and no rollback risk.

## Where each one actually stands — MEASURED, not estimated

Run on 2026-08-24 with the new gate. This is what you are buying.

| video | runtime | gate | cuts/min | longest static | coverage | captions | bed |
|---|---|---|---|---|---|---|---|
| 01 spray tan | 18:53 | **9 / 3** | 10.8 ✓ | 22.7 s ✓ | **28%** ✗ | **8%** ✗ | ✗ |
| 02 Zepbound | 30:28 | **6 / 6** | **1.6** ✗ | **186.0 s** ✗ | **0%** ✗ | **0%** ✗ | ✗ |
| 03 supplements | 23:30 | **6 / 6** | **0.6** ✗ | **453.7 s** ✗ | **0%** ✗ | **0%** ✗ | ✗ |
| 04 invest-health | 53:17 | **7 / 5** | **3.0** ✗ | **90.2 s** ✗ | **6%** ✗ | **0%** ✗ | ✗ |
| 05 meal prep | 3:48 | **9 / 2** | ✓ | ✓ | ✓ | n/a (split-screen) | ✗ |

Every one **passes** on the things the last audio pass fixed: stream, loudness, true peak,
channel SNR, L/R correlation, dead air, splices. **The audio is already good on all five.**
What is missing is the style pass — the same thing that was missing from the ab-wheel cut.

**Read the table this way:**
- **05 meal prep is nearly done.** It needs a music bed and nothing else. ~30 minutes.
- **01 spray tan is close.** It already has 71 cutaways and 205 visual changes from its rev-1
  pass; it needs burned captions, a bed, and more coverage. ~1 session.
- **02, 03 and 04 have effectively no style pass at all.** 0.6–3.0 cuts/min, 0–6% coverage,
  and one 7½-minute stretch (supplements, 6:30–14:04) with no visual change whatsoever.
  These are the real work.

## Recommended order — stop after any step

1. **05 meal prep** — add a bed. 30 min. (Do not add burned captions: it is the split-screen
   tutorial the `.srt`-only rule was actually written for. Step 8.)
2. **01 spray tan** — captions + bed + top up coverage from 28% to 40%. ~1 session.
3. **04 invest-health** — the biggest audience payoff per minute of work, but it is **53
   minutes long**; consider cutting it down first (two approved cut-down variants already
   exist: `INVEST_HEALTH_conservative.mp4` 43:31 and `INVEST_HEALTH_sub30.mp4` 28:25 — Dan
   never picked one, and picking one is a prerequisite, not part of this job).
4. **02 Zepbound** and **03 supplements** — a full style pass each. ~1 session apiece.

**Budget honestly: five sessions if you do all of it, and one for the first two together.**

## The procedure, per video

The picture does not need re-rendering from source. Every one of these has its graded cut
(`CUT_v*_graded_NO-GRAPHICS.mp4`) and its `edl.json` beside it, and its segment cache on
`/Volumes/Extreme/`.

0. **Repath if anything still points at the Seagate.** It is gone; everything is on
   `/Volumes/Extreme/`. `export PATH=/Volumes/Extreme/_edit_work/bin:$PATH` in every
   background command — Whisper shells out to a bare `ffmpeg`.
1. **Baseline the gate** so you know what you are fixing:
   `python3 reference/qc_style.py <FINAL.mp4> --srt <its .srt> --talking-head`
2. **Punch-ins** — `reference/subject.py` then the framing half of `reference/plan_punchins.py`.
   This alone takes 0.6–3.0 cuts/min past the 4.0 gate and is the single highest-value step.
   Three crop levels, 0.74 floor, a shot holds its crop across pause cuts. **Step 5.4.**
3. **Coverage** — `reference/plan_map.py` prints every gap with the transcript inside it, so
   each clip is chosen for the line it illustrates. Pexels via the in-app browser (the search
   pages 403 to curl; the recipe is in Step 5.5 and in `build_inserts_motion.py`).
   **Cast to Dan's brief: white or Asian men 30–50.** Four of the 38 results pulled for the
   ab wheel read as men in their titles and were women.
4. **Animated graphics** — `_shared/motionlib.py`, palette `MIL`, spec in
   `reference/HOUSE_STYLE.md`. Convert the existing static chips; do not re-interpret the style.
5. **Music** — `reference/pick_bed.py`. Pixabay, commercial, no attribution. Pick on
   FLATNESS and EQ the shape; the shape is the fixable half.
6. **Captions** — `reference/captions_burn.py`. Talking-head only; 05 stays `.srt`-only.
7. **Re-gate, then deliver** over the same filename, keeping the previous master as
   `*_PRE_REBUILD.mp4`.

## Things to avoid — all of these cost real time on the ab-wheel rebuild

- **Do not touch the colour grade.** All five were graded per roll and validated closed-loop.
- **Do not re-fit a voice EQ by copying another roll's curve.** They differ in opposite
  directions — the spray-tan roll needed the reverse correction to the ad roll.
- **Do not chase runtime with a whole-video wpm figure.** The ab-wheel cut read 151 wpm and
  its talking was already at 194–239; the number was dragged down by silent demo sections.
  Measure pace PER BEAT before deciding anything is slow.
- **Word-guard every cut.** An envelope at −40 dB cannot see a quietly-spoken "But" or
  "Second". Unguarded, the ab-wheel plan deleted 20 real words and clipped 3 more.
- **`-frames:v N`, never `-t`,** when rendering pieces — `-t` emitted an extra frame on 27
  of 85 pieces and drifted the audio 0.9 s. And cut the audio in ONE graph, not per piece.
- **Target loudnorm TP −2.5 when delivering AAC.** The encoder overshoots ~1.8 dB.
- **Long renders: never poll for a filename** — see the existing section in SKILL.md.

## Relevant files

- **Videos:** `claude edited long form content/0{1..5} - …/`
- **Skill:** `.claude/skills/longform-edit/SKILL.md` — read **Step 2.5** first, then 5.4, 5.5, 7, 7.5, 8
- **Gate:** `.claude/skills/longform-edit/reference/qc_style.py`
- **Style spec:** `.claude/skills/longform-edit/reference/HOUSE_STYLE.md`
- **Worked example:** `spec_example_abwheel.py` in the same folder, and the full build in
  `/Volumes/Extreme/_edit_work/abwheel/r2/`
- **Shared graphics/SFX:** `.claude/skills/_shared/motionlib.py`, `sfxlib.py`

## Exact next action

Start with **05 meal prep** — pick a bed with `pick_bed.py`, mix it with `audio_final.py`,
re-gate. It is 30 minutes and it takes one video to 11/11.

### Starter prompt

> Execute `Handoffs/handoff-20260824-five-longforms-to-new-standard.md`. Work in the
> recommended order and stop when I run out of limit — each video is independently
> deliverable. Re-gate with `reference/qc_style.py` before and after each one.
