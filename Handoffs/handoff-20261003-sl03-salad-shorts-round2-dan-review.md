# SL-03 Daily Salad shorts: round 2 delivered, waiting on Dan's review

**Written 2026-10-03 by Claude (Opus 5.5). Task name for the next round: `Daily Salad SFC R3`. Recommended: Claude Opus 5.5, high.**

## State

All six shorts are cut, delivered and on one review page. Nothing is uploaded, queued or covered. Nothing posts before
RO-05 is public on Oct 18. Dan has NOT reviewed them yet; `delivered` is not `finalized`.

- Review page: `http://127.0.0.1:8811/` (serve with
  `python3 .claude/skills/_shared/review_server.py 8811 /Volumes/Extreme/_edit_work/sl03/r2/review` if it is down).
- Delivered files: `Short-form video content/daily-salad-short1..6_*.mp4`, each with `.audio_gate.json` (verbatim PASS) and
  `.deliver_gate.json` (2.4.0 PASS). Review copies and sound checks: `Short-form video content/daily-salad REVIEW/`.
- Notes: `Short-form video content/daily-salad-SHORTS.md` (status table, key-point copy, what is declared in the gate).
- Build: `/Volumes/Extreme/_edit_work/sl03/r2/<S1..S6>/` (shots, tracks, bars, gate plans, declarations),
  reviews `r2/REVIEW-r2*.md` (eight passes).
- Recipe in git: `.claude/skills/shorts/reference/softblue-sl03/` (`plans.py` = every decision as data, `batch.py`,
  `deliver.py`, `page_r2.py`, `rungate.sh`, README with what the reviews taught).
- Look locked into `_shared/GRAPHICS-STANDARDS.md` ("Soft Blue shorts standard") and the `/shorts` skill.

## What Dan is asked (2 decisions on the page)

1. Approve the six shorts, or changes by short number and time.
2. The following crop in the extreme close-ups of shorts 4 and 5 (keep, recommended; or try a stiller crop that only
   moves when his head nears an edge).

Everything else is under "What I decided" on the page: key-point copy for shorts 2 to 4, no bars on the app shorts,
short 2 starting on "Let's" (ear check), the dropped "Number one," and "So", the shortened pauses, cutaways, phone alone
where his face is too close, posting shorts 5 and 6 a week apart, the "1 photo" title note. Spend $0.

## When Dan replies

- Record his words in `/Volumes/Extreme/_edit_work/sl03/round3-plan/decisions.json` with the file hashes
  (`shasum -a 256` on the six delivered files).
- **Approved as is:** `queue.py set SL-03 finalized --by Claude --note "<his words>"`, mirror to the Edit Queue page,
  delete the board entry, register the B-roll inserts in the clip library (list in `daily-salad-SHORTS.md`), and write
  the one Claude handoff for covers plus setup (five thumbnail choices per short, "Use the Codex subscription to generate
  the images"), to run after Oct 18.
- **Changes:** edit `plans.py`, then per changed short: `batch.py audio/words/plan/track/gfx/proof/render`,
  `deliver.py copy`, watch pass, a fresh `ra-reviewer` judge, `watch.py --judge`, `rungate.sh`. A changed file needs all of
  it again; an unchanged file keeps its stamps. Never re-render a short he approved.
- Decision 2 = B: in `plans.py` drop `head=True` follow for S4 shot 1 and S5 shots 0 and 8 in favour of a hold-until-edge
  window (the last reviewer estimated 20 to 28 % less travel); proof it on stills first.

## Traps

- Other sessions render on this machine; the gate waits for a build slot and can sit for an hour. Launch it with
  `rungate.sh` only (a shell or watcher whose command line contains `gate.py` counts as a build and deadlocks it).
- Port 8810 belongs to another session's server.
- `deliver.py` is shadowed by `_shared/deliver` on `sys.path`; load it by path (see `page_r2.py`).

## Starter prompt

> Name this task `Daily Salad SFC R3`. Read `Handoffs/handoff-20261003-sl03-salad-shorts-round2-dan-review.md`. My
> review of the six Daily Salad shorts: [paste the reply box from the review page]. Record my decisions, make only the
> changes I asked for, re-check any changed short (watch pass, independent audit, gates), and if everything is approved,
> mark SL-03 finalized and write the covers and setup handoff. No upload.

Model and effort: Claude Opus 5.5, high.
