# RO-10 vertical, round 5: apply Dan's answers to the full 9:16 and its 52 s cut

Written: 2026-10-03 by the round 4 session. Recommended: Claude Opus 5.5, high.
Sidebar name: `Calories Reason LFC Vertical R5`. Fire only AFTER Dan has answered the round 4 page.

## Goal

Record Dan's four answers, apply them with kit rules (never a hand edit), re-gate, re-judge only what changed, and
deliver the masters for setup. Do not upload: setup is a separate `/video-setup` task.

## Where round 4 stopped (verified 2026-10-03)

- Review page: `http://127.0.0.1:8812/` from `/Volumes/Extreme/_edit_work/kit9x16/sbl-ro10/review4/`
  (restart: `python3 ~/abs-worktrees/kit-sheet/.claude/skills/_shared/review_server.py 8812 <that folder>`).
- Masters in the build dir `sbl-ro10/`: `calories the reason youre not losing weight | claude | 9x16 | RO-10.mp4`
  (8:38.25) and `... | 9x16 59s | RO-10.mp4` (0:51.8), each with a `_REVIEW_540p.mp4`. Record: `round4_report.json`.
- Full film, gate 2.5.0 `organic9x16`: FAIL, 32 pass, 3 not applicable. Failing and LEFT failing on purpose:
  `style:coverage` 35 % (min 40), `style:static_run` 36.0 s at 1:59.5 (max 30), `cut:splice_visibility` 3 of 24 joins,
  `watch:pass` (3 open judge findings). Cut, gate `short`: FAIL on `framing:push_coverage` only (x1.045, min x1.10).
- Judged: three fresh judges (thirds) + one re-judge of the 61 changed images; the cut one judge + one re-judge.
  Verdict files: `logs/findings_part*.json`, `judged_r1/`, `cut_audit/logs/`, `cut_judged_r1/`.
- Kit changes are pushed from `~/abs-worktrees/kit-sheet` (branch `claude/kit-sheet`): gate format `organic9x16`,
  `kit_plan.py` on a sheet build, `kit_judges.py`, organic brief in `cutdown_pick.py`, aligner and caption fixes.
  Corpus PASS at gate 2.5.0 (162 entries, 6,711 s); audio selftest PASS in the main checkout.
- The work tree's working copy also carries ANOTHER session's uncommitted kit fixes from the main folder (applied
  for the run, never committed there): `render.py` frame-grid fix, `kit_cutdown.py` caption lifts, `cutdown_pick.py
  --ranges/--search`, `kit_plan.py` pause trim. The build dir's `render.py` is that version. If those are on
  `origin/main` by now, `git checkout` the work tree's copies and pull; if not, keep them applied for the rebuild.
- AI spend: 6 cents this round, 75 cents on this vertical in all.

## The four questions on the page

1. The full film: approved, or notes with times.
2. The 52 second cut: approved, or notes.
3. The "Purdue" lower third at 7:19 (heading only for 4.6 s, captions paused under it): leave, or tighten.
4. The three readings: make this film the reference for organic verticals once approved, or talk first.

## Work

1. Record his answers verbatim in `sbl-ro10/review/decisions.json` (`round4_answers`: id, verdict, his words, scope).
2. **If "tighten" (question 3):** a kit rule, not an edit. In `sbl_graphics.py` (it already owns caption lifts and
   mutes from the layout): a lower third whose first part lands more than 2.5 s after it opens is opened 2.5 s before
   that part instead (change the overlay's `t0` in `beats.json` `lower_thirds` and the render's `a`), so captions run
   until it opens. Only G14 (439.35, first line at 443.97) is over 2.5 s on RO-10. Re-render that lower third, then
   `kit_run.py ... --from picture --until mux`.
3. Any other note: fix it in the kit (template, `vertical.py`, `captions.py`, `clip_overrides.json`), rerun from the
   earliest stage it touches. `sbl_graphics.py` and `kit_labels.py` both rewrite `beats.json`: never together.
4. Re-gate: `kit_run.py --sheet SHEET --build B --name "..." --from prewatch --until prewatch` (it stops on the three
   left-failing rows by design; that is expected). Run nothing else that gates at the same time.
5. Re-judge only what changed: move `watch/` and `logs/findings_part*.json` + `negscan_findings.json` into a
   `judged_rN/` folder BEFORE the prewatch, then `carry_verdicts.py --build B --prev B/judged_rN`,
   `kit_judges.py --build B --notes judge_notes.md --rejudge logs/rejudge.json`, one fresh judge on
   `watch/JUDGE_PART_2.md`, then `FORMAT=organic9x16 zsh kit_fold.sh B <film> "<who judged>"`.
6. The cut: `kit_cutdown.py --build --out <cut>` (the pick in `cutdown_ranges.json` stands unless he changes it;
   a hand pick is `cutdown_pick.py --organic --ranges "0-1,11-13,120-123"`), `kit_run.py ... --from cutgate --until
   cutgate`, carry + re-judge in `cut_audit/` the same way, `FORMAT=short zsh kit_fold.sh B/cut_audit <cut> ...`.
7. **If he approves and says yes to question 4:** add both files to `_shared/qc_corpus/corpus.json` as approved
   entries with his words and the measured readings, with `deliver.format` `organic9x16` / `short`. Then, and only
   then, set `organic9x16`'s `style:coverage` and `style:static_run` from the approved file with its provenance
   (as every other format's bounds were set), bump `GATE_VERSION`, run the corpus (`run.py --no-selftest` through a
   scratch folder whose `.claude/skills` links to the work tree and whose other entries link to the main folder;
   the audio selftest runs in the main checkout with `zsh`), and re-gate both files for their stamps.
8. Deliver: copy the masters, review copies, stamps and recipe to
   `claude edited long form content/10 - Calories The Reason You're Not Losing Weight/` (`kit_run.py --deliver`
   does it), update the edit queue, and hand to `/video-setup` in its own task.
9. Close this line on the board and in `Handoffs/README.md`.

## Traps

- A background task is stopped at two hours. Run `gate.py` detached (`nohup`) and wait on its json.
- `rm -f logs/findings_part*.json` aborts a zsh `&&` chain when nothing matches. Use `find ... -delete`.
- The Extreme drive had 53 to 68 GB free. Caption frame sequences are staged on the internal disk now.
- The judges' three flags are identical in the approved 16:9 (lower third timing, the glance at 4:49, the notebook
  still). Do not change the edit for them unless Dan says so.
- Do not upload or publish. RO-10 is organic.

## Starter prompt

> Name this task `Calories Reason LFC Vertical R5`. Read
> `Handoffs/handoff-20261003-ro10-vertical-round5-after-dan-review.md`. Dan's answers to the round 4 page
> (http://127.0.0.1:8812/) are: [paste the reply box]. Record them, apply them as kit rules with no hand edit,
> re-gate, send a fresh judge to only what changed, rebuild the 52 second cut, and deliver the masters for setup.
> Do not upload anything. Explain the results in plain language.

Model and effort: Claude Opus 5.5, high.
