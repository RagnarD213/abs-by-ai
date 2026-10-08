# RO-06 "How To Work Out At Home On A Budget": round 1 is with Dan, round 2 builds the full film

**LFC (long-form content, 16:9).** Sidebar name for the next task: `Work Out At Home LFC R2`.
Written 2026-10-08 by Claude (Opus 5.5) at the end of round 1. Read `Handoffs/video-editing/00-RULES.md`,
`.claude/skills/longform-edit/SKILL.md` and `.claude/skills/longform-edit/reference/ro06/README.md` first.

## Where things are
- Work dir: `/Volumes/Extreme/_edit_work/ro06/` (recipe in `recipe/`, mirrored in the skill's `reference/ro06/`).
- Review page: `round1/index.html`, served with `python3 .claude/skills/_shared/review_server.py 8846 /Volumes/Extreme/_edit_work/ro06/round1`
  (http://127.0.0.1:8846/index.html). First minute: `round1/first-minute/DRAFT - RO-06 round 1 - first minute.mp4`
  (63.0 s, audio gate PASS 12 of 12, stamp beside it). Phone copy in `claude edited long form content/13 - How To Work Out At Home On A Budget/round1/`.
- Cut: 28 pieces from 20 rolls, 17:39 (`edl.json`, `take_map.json`), 124 shots (`shots.json`), framing solved with no
  same-size joins (`build.py segs` prints `jumps: []`). 57 plan items (`plan_resolved.json`), 41 template graphics rendered (`hf/`).

## Nothing is locked by Dan yet. His nine decisions (page header, recommendations pre-filled in the reply box)
1 colour A/B/C (first minute is B) · 2 framing sizes · 3 hair at the top edge on 9 rolls (source framing) · 4 length
(A trim three repeats to about 16:30, B keep 17:39, C about 15:00) · 5 AI product pictures in the price cards ·
6 jump rope "$10" vs "$9" · 7 music bed · 8 app demo treatment · 9 on-camera open vs an AI opener.

## Round 2, after Dan replies
1. Record his answers verbatim in `round2-plan/decisions.json` with sha256 of every file he approved. Re-hash before building.
2. Apply only what he changed. Length option A cuts (source, roll-local): C1569 65.7 to 91.4 (keep the $58 total line before
   it), C1572 16.1 to 29.9, C1580 the restatements at 11.9 to 24.5 and 141.6 to 149.0. Check each on the envelope and by
   medium.en before cutting (lower third G30 is anchored on 'So I want you guys to get started': move its anchor if that line goes); rerun `edl.py` through `resolve.py`, then `from_plan.py` (unchanged scenes are skipped).
3. Still to build: P01 and P02 in the phone card per decision 8 (P02 is a raw placeholder now); a music bed if he says
   yes (Pixabay, transcribe it and require zero words, bed level is a ceiling: read the gate's floor row); stock for
   "my gym where there's bodybuilders" and "get a gym membership" if the closing section needs cover (longest stretch
   with no clip there is under 30 s because of lower thirds; check the gate's static-run row on the real file).
4. Full film: `build.render_range(0, total)`, then SRT, chapters, edit sheet, audio gate, watch pass, dense hair check,
   hyperframes `checks.py`, one independent reviewer (`ra-reviewer`), delivery gate `--format longform`. Report honestly:
   the hair rows will fail on the 9 source-framed rolls unless Dan chose the headroom extension.
5. When the EDL is final run `roll_sidecar.py mark-used` for every source range. Register nothing in the clip library
   until Dan approves the film.

## Honest status
- Not run yet: delivery gate, watch pass, independent review (they need the complete film).
- Spend: $0 metered. Six Codex stills on the subscription. No Gemini calls.
- Not checked by ear by a person: the two cross-take joins (excuses sentence, kettlebell price). Both read clean on
  medium.en and on frame strips; Dan hears the first one in the first minute at 0:28.

## Starter prompt (Claude, Opus 5.5, high)
> Read `Handoffs/handoff-20261008-ro06-round1-dan-review.md` and execute round 2 of RO-06 "How To Work Out At Home On A
> Budget" (LFC, name this task `Work Out At Home LFC R2`) with /longform-edit. My round 1 answers: [paste the reply box].
> Record them, apply only what I changed, build the full 16:9 film, run every gate, the watch pass and the independent
> review, deliver master + SRT + chapters, send me the review copy, update the edit queue.
