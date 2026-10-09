# RO-03 "The Vacuum: Workout Only": round 1 is with Dan (2026-10-09)

**CONTENT, long-form family (LFC).** Sidebar name for the next session: `Vacuum Workout Only LFC R2`.

## Goal
A 2:32 follow-along from the 8/14 poolside rolls: three 20-second vacuum holds with 30 seconds of rest between (Dan's
Shoot 4 outline). Round 2 builds the full film once Dan answers round 1.

## Dan's instruction this round (2026-10-09)
"Don't model it on Zeeshan's videos. He's not the best editor. Model it on Muhammad's workout videos." The job doc
said Zeeshan's ab wheel workout-only video; that is overridden. The reference is the workout sections of
`YouTube Long Form Video Content/The $17 Ab Wheel Beats Every Crunch - READY FOR UPLOAD/Muhammad edit/`.

## What Dan has
- Page: http://127.0.0.1:8877/ (managed review server, folder `/Volumes/Extreme/_edit_work/ro03/round1`).
- VLC copy: `Videos to Review/Vacuum Workout Only LFC R1 - first minute.mp4` (66 s, sha256 40bbd85a05c816e3a2f5903621475c6abbd48b171c63f4a68d4e91a0c854b60d).
- Three questions, each with my pick A: (1) the one filmed hold shown three times, (2) the trip-hop music bed,
  (3) Muhammad's flash on the cut into each set.

## Decisions already made (on the page under "What I decided")
- Cut: intro line (C1625 24.02-29.80), set 1 (C1625 33.40-55.60), rest 1 talk (C1626 28.17-52.52), set 2 with its
  lead-in (C1625 29.95-55.60), rest 2 talk (C1624 18.37-46.64), set 3 (C1625 33.85-56.30), ending (C1626 2.97-18.44),
  sign-off (C1629 4.84-12.30). 15 shots, 4,544 frames. Rests 29.98 and 30.02 s. No pause was tightened.
- Reused locks from RO-02: colour A, far / near framing with half headroom, Soft Blue Light, the HyperFrames lower
  third, the countdown chip style, hard cuts.
- New graphics shown as stills: title chip (T00), set and rest countdown chip (K00), six lower thirds (G01 to G06).
- Sound: the film is mixed once (`build.py audio`), target -14.5; speech alone passes the audio gate on every row at
  -13.4 LUFS. The whole mix fails four rows because the holds are music only (tone, artifacts, dryness, loudness
  -15.3). Reported on the page, nothing tuned.
- No AI, no stock. Spend $0.

## Files
- Work: `/Volumes/Extreme/_edit_work/ro03/` (`recipe/`, `round1/`, `round2-plan/decisions.json` with hashes, all pending).
- Recipe in git: `.claude/skills/longform-edit/reference/ro03/` (README has the order and the traps).
- `cache` and `hf/renders` are symlinks into `~/.cache/absbyai/ro03/`.

## Not done (round 2, after Dan replies)
1. Record his answers in `round2-plan/decisions.json` with his exact words; re-hash the round 1 files first.
2. Apply his notes, then `build.render_range(0, total)` for the full film in `round2/`.
3. SRT (uploaded, not burned), chapters, edit sheet + `validate.py`, hair check on the whole film, audio gate,
   watch pass, delivery gate `--format longform`, one independent reviewer on the finished file.
4. Deliver to `claude edited long form content/13 - The Vacuum Workout Only/` with the 540p review copy, audio A/B,
   stamps, notes and recipe. Full film to `Videos to Review/` (replace the first minute copy).
5. `roll_sidecar.py mark-used` for every source range once the cut is final; `queue.py set RO-03 delivered`.
6. Register nothing in the clip library (no new clips).

## Open risks
- Dan may not want one hold repeated three times; option B is a 45-second single set.
- The delivery gate will fail the same rows RO-02 failed on this poolside framing (headroom, no-wide-level, splice
  visibility, the two caption rows), plus the audio rows above. Report them; do not tune.

## Recommended model and effort
Claude Opus 5.5, high. A small, recipe-backed build with gates and one reviewer.

## Starter prompt
> CONTENT (LFC). Rename this task `Vacuum Workout Only LFC R2`. Read `Handoffs/handoff-20261009-ro03-round1-dan-review.md` and `.claude/skills/longform-edit/reference/ro03/README.md`, then run round 2 of RO-03 "The Vacuum: Workout Only" with /longform-edit: record my round 1 answers below in `round2-plan/decisions.json`, apply them, build the full film, run every gate and one independent review, deliver the master, SRT and review copy, and update the edit queue. My answers: [paste the reply from the review page]
