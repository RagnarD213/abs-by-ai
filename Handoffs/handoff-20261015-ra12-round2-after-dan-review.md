# RA-12 "The First Step To Getting Abs Isn't A Workout": round 2, after Dan's round 1 answers

**AD (short-form, filmed).** Sidebar name for the next task: `First Step Abs AD R2`.
Written 2026-10-15 (Claude Opus 5.5) at the end of round 1. Job doc: `Handoffs/video-editing/RA-12-first-step-to-getting-abs-isnt-a-workout.md`.
Read first: `.claude/skills/_shared/VIDEO-RULES.md`, `_shared/PRE-RENDER-APPROVAL.md`, `/ad-edit` (RA-12, RA-14, RA-15 sections),
`.claude/skills/ad-edit/reference/ra12/README.md` (stage order, eleven lessons).

## State

* Round 1 page: http://127.0.0.1:8842/ (`/Volumes/Expansion/_edit_work/ra12/round1/index.html`). The WHOLE 9:16 ad, 46.25 s,
  every line, nothing pending. Master sha256 2c34bf8d1a80, filed in `Claude Ad Videos/the first step to getting abs isnt a workout - RA-12/round 1 review/`
  with `notes.md` (take map, every choice) and the three review files. VLC copy: `Videos to Review/First Step Abs AD R1 - whole ad 9x16.mp4`.
* Work dir `/Volumes/Expansion/_edit_work/ra12/` (Seagate; the Extreme drive is full). Raw roll C1667 on Extreme (read only).
* Independent review round 3: SHIP. Delivery gate 2.6.0: 36 pass; open `audio:stamp` (tone row, the known bass-lift miss),
  `compliance:labels` (gate sampling bug on 0.9 s spans; separate task), `watch:pass` (8 judge defects, all decision 3).
* Spend: about $0.02 transcription, $0 of the $10 AI budget.

## Dan's three decisions (on the page)

1. Whole ad: approve, or changes by ID/time.
2. Opener: keep the library montage (recommended), or pick AI opener ideas (Missing box lid, Mirror double take, Blindfold archery,
   Roundabout, Flat-pack chaos, Dartboard in the dark) for START/END frames.
3. Buttons and KEY POINT over his midsection: A (recommended) keep the RA-14 spot for the buttons and end L1 before the FAR hold at
   41.71 s; B keep all as is; C compact chest-height button (RA-01 style).

Record his answers verbatim in `/Volumes/Expansion/_edit_work/ra12/round2-plan/decisions.json` (PRE-RENDER-APPROVAL "How a round works").

## Next actions by answer

* **A on decision 3:** in `s84_plan.py` set L1's `t1` to `t_so` (41.71 s), re-run from the plan step (`chain_c2.sh` pattern: plan, s04b,
  plan, sheet, `vertical.py --render --force`, cards, captions, holds, `gate_seq.sh`), judge, gate. Record his words on the remaining
  C1/C2 judge defects as `accepted_by_dan` in `findings.json` (never edit the watch log).
* **AI opener picked:** frames on the Codex subscription (`_shared/codex-image.sh`), `framecheck/gate.py` + a fresh `frame-reviewer`
  before the page; motion only after he approves frames. Round 2 is then a frames round.
* **Approved as is:** build the 16:9 from the same edit (RA-15 lesson 18 `hv16.py`; 16:9 levels in `ra01lib.Aspect("16x9")`;
  horizontal framing static per shot), gate it, independent review, then move both masters out of `round 1 review/` into the ad
  folder root with the `/editor-deliveries` names, set the queue to `delivered` again, then `/ad-setup` when Dan says.
* Delete `Videos to Review/First Step Abs AD R1 - whole ad 9x16.mp4` when Dan finalizes; stop the page with
  `review_server.py 8842 --remove`.

## Traps (full list in the README)

`s08_audio.py` must be the length-preserving version (the RA-14 copy drifts 6 ms per splice). `voice_chain.py --frame-lock` hangs:
trim the mix with apad/atrim. `TAIL_EXTRA="abs:0.06,generate:0.10"` in the EDL call. `HEAD_SRC=178.26 EDGE_OVERRIDE="R1.end=194.86,R2.start=211.98"`.

## Model

Claude Opus 5.5, high effort (a bounded revision on a locked recipe).

## Starter prompt

> AD. Rename this task `First Step Abs AD R2`. Read `Handoffs/handoff-20261015-ra12-round2-after-dan-review.md` and build round 2 of RA-12 "The First Step To Getting Abs Isn't A Workout" with /ad-edit from my round 1 answers: [paste my answers]. Record my words, make the changes, rebuild from the plan step, re-run the watch judge, delivery gate and an independent review, and stop for my review (or, if I approved the 9:16, build the 16:9 and deliver both).
