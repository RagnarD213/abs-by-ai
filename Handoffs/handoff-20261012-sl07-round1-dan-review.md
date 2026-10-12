CONTENT | SL-07 | If I Had Belly Fat SFC R2

# SL-07: apply Dan's round 1 answers, record the two pickups, build the five Belly Fat shorts

Written 2026-10-12 by Claude (Opus 5.5) at the end of round 1. Round 1 delivered the review page with short B rendered,
12 AI frame pairs and every title, clip, graphic and key point of all five shorts as stills. Dan has not answered yet.
Supersedes `handoff-20261012-sl07-belly-fat-shorts-pickups-and-build.md` (its picks, pickup lines and standing decisions
still hold; read it for them).

**Recommended: Claude Opus 5.5, high effort.** (Five renders, AI motion, gates and an audit; the build will be watched.)

## Where things are

- Review page: http://127.0.0.1:8874/ (`/Volumes/Extreme/_edit_work/sl07/round1/`, `page_r1.py` + `notes_r1.py`). Short B's
  full-quality copy: `Videos to Review/If I Had Belly Fat SFC R1 - short B - Weigh Yourself Every Morning.mp4`.
- Work folder: `/Volumes/Extreme/_edit_work/sl07/`. Everything a short is, is data in `plans.py`. Tools and what round 1
  learned: `.claude/skills/shorts/reference/softblue-sl07/README.md` (read it before touching anything).
- Batch record: `Short-form video content/belly-fat-90-days-SHORTS.md` (cut points, the film's map, notes).
- State per short: audio cut, captions aligned, shot table, face track and key-point bars exist for all five
  (`build/<S>/`). Only B is rendered (`build/B/short2_weigh-yourself-every-morning.mp4`, audio gate PASS verbatim, every
  cut where planned, no frozen frames, captions match its transcript). A, D, E, F are stills only.

## The pickups are NOT recorded

Dan was working in other sessions and never read the two lines; the mic was open 50 minutes. `pickups/B.wav` and `D.wav`
are silent placeholders (`B.PLACEHOLDER`, `D.PLACEHOLDER`), so B was built opening on the film line (the scale clip under
its first 1.4 s). D's build folder still carries the placeholder head from before that switch: run `batch.py audio D`
again before anything else on D.

1. Ask Dan to say "record now" (or to drop a Voice Memo). Lines, three takes each, B then D:
   B "Here's how to know if your fat loss plan is working." D "Here's why you should work out every single morning."
2. Record with `~/.cache/absbyai/rec_mic OUT_DIR SECONDS 30` (never ffmpeg avfoundation: it dropped 11 % of the audio).
   `pickups/watch_lines.py` stops it when both lines were heard twice. Check samples against wall time.
3. `pickup.py asr`, pick the best take of each, `pickup.py fit` on all takes, `pickup.py make B|D raw t0 t1`, delete the
   two `.PLACEHOLDER` files, then `batch.py audio|words|plan|gfx|proof|render` for B and D. Say on the page how each was
   treated and what the room measures (Yeti against the lav).
4. Declare the pickup span to `audio_gate.py --verbatim` (read the gate's plan keys first; never change a bound).

## Dan's four decisions on the page (not answered)

1. The pickups (above).
2. The 12 AI clip ideas: yes, change or no for each (`aiframes/`, `frames.json` has the action line per clip). Default
   offered: yes A1, A2, B2, E1, E2, F1, F2; no B1, D1, D2; A3 and E3 his taste. Where each goes and its plain fallback is
   in `notes_r1.py` (`AI`). Motion only for approved pairs; $5 per short including retries (A has three ideas: opener plus
   one more unless he approves about $6 there). Any short that takes one gets `ai_generated: true` at setup; A has it anyway.
3. Title copy (five, in the reply box).
4. Key-point copy (11 bars, in the reply box; two lines, about 26 letters a line; `gfx` asserts it).

Record his answers in `round2-plan/decisions.json` with his words before building.

## Then build

- Motion for the approved frames (frames first rule is satisfied; register approved clips in the clip library after).
- Add each approved clip as a cover in `plans.py` (9:16 clips fill the picture area; chip off faces and bodies).
- Render A, D, E, F and B again. Proof sheet and the frame-by-frame cut scan on each before the gate.
- `deliver.py` in the work folder is still the SL-03 copy: point it at this batch
  (`Short-form video content/belly-fat-90-days-<NAME>.mp4`, REVIEW folder, declare file) before `copy`.
- `_shared/deliver/gate.py --format short`, the watch pass and judge, then a fresh `ra-reviewer` that is not shown your
  notes. Expect "does not ship" once.
- Deliver per the first handoff, step 5. `queue.py set SL-07 delivered`. List the five shorts that need covers.

## Decisions made in round 1 (on the page under "What I decided"; Dan can overrule any)

- All five endings are whole (each last word measured against the raw lav); no fallback ending was used.
- E is one continuous passage (the 0.6 s pause at 655.2 is kept, with a size step). 42.8 s.
- D opens on the fast jump rope (B0448, full screen), not the ab wheel; the ab wheel is a card where the film had it; D
  ends on the toe touch card. Cards because he travels about 1,400 px sideways in both.
- B's scale clip under the pickup is a square (the scale is the subject). B's study card and 7-day chart are rebuilt
  (`scenes.py`); the weekly check list is two key-point bars.
- E shows Dan's real pool clip B0435 on "once you have your abs".
- F has two phone demos beside Dan: B0035 (taking the photo) and the film's B0038 (the day's log).
- Full caps on three bars only (7 MONTHS, NOTHING, DAILY) and "13 lb MORE" in the study card.

## Cost ledger

Spent: $0 (24 AI frames, 27 generated, on the Codex subscription, about 739,000 Codex tokens). Cap: $5 per short.

## Open risks

- The Yeti against the studio lav: unheard until a pickup exists. Report the room measurement and let Dan listen.
- B1, D1 and D2 are the weak frames (small dial, small coin, quiet picture).
- The face-size step between the two windows is 1.2x (the locked standard); the reviewer may flag a same-take step.
- Two builds at most on the machine. Round 1 ran at a load of 100 or more with two other sessions rendering.

## Starter prompt

> Name this task "If I Had Belly Fat SFC R2". This is CONTENT. Read `Handoffs/handoff-20261012-sl07-round1-dan-review.md` and execute it: record my two pickup lines first (say "record now" when ready), apply my answers from the round 1 page (pasted below), generate motion for the AI frames I approved, then build all five Belly Fat shorts with /shorts in Soft Blue Light, gates and an independent audit. Use the Codex subscription for any new images. No covers, no upload.
>
> My round 1 answers: [paste the reply box here]
