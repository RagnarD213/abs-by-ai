# RO-14 "Why You're Not Losing Weight": round 3, two revisions on the round 2 film

**LFC (long-form content, 16:9).** Sidebar name: `Not Losing Weight LFC R3`. Written 2026-10-21 by Claude (Opus 5.5) at the end of round 2.
Recommended: **GPT-6.1 Sol, high** (Dan's 2026-10-20 rule: video edits and continuations default to the newest stable Sol at high).
Dan asked for this handoff instead of continuing in the round 2 task because the Mac was overloaded.

Read first: `.claude/skills/_shared/VIDEO-RULES.md` (top sections: head/hair clearance, AI clips via Flow, AI clip sense QC,
later-round timestamps), `.claude/skills/longform-edit/reference/ro14/README.md` (traps 1-11, round 2 items 10-11), and
`/Volumes/Extreme/_edit_work/RO-14/round2/ROUND-2-EDITOR.md` (what round 2 built, every decision, costs).

## Dan's round 2 notes (2026-10-21, recorded in `/Volumes/Extreme/_edit_work/RO-14/round3-plan/decisions.json`)

> "Okay, revisions for the intro clip: the broken scale. It's not really apparent that the scale is broken. Let that clip run a
> little bit longer so that you can tell that the scale is broken. It just looks like he stepped on the scale the way he did it
> here. At 4:06, I don't think this clip is appropriate because it's the woman taking care of the man's health problems. We need a
> clip of the man taking care of the woman's health problems here. Find that stock clip, or if you can't find that, then just use
> a camera scene."

Nothing else was noted: every other part of the round 2 film stays exactly as delivered.

1. **A1, the broken scale (0:00, the opener).** Round 2 plays only 2.6 s (`A1-flow-t1-rugfix.mp4` frames 31-92: on the scale,
   frowning, steps off, bends and grips it) because every take's LIFT failed review (the scale doubled its display, melted, or
   his foot passed through it). Dan now wants it to run longer so the viewer SEES the scale treated as broken: he lifts it and
   peers at it, shakes or taps it, disgusted. The slot is 0.00-4.97 (words: "You are eating healthy. You are working out, but the
   scale will not move." ends 4.48+). Fill as much of the slot as a clean take allows.
2. **C16 at 4:05.0-4:09.9** (words: "You will spend your 50s and 60s managing her health problems instead of living."). The current
   Pexels 8088977 reads as the woman looking after the man. Replace it with a stock clip of a **man looking after a woman's health**
   (helping his wife take medication, checking her blood pressure or blood sugar, pushing her wheelchair, helping her up from a
   chair, at her hospital bedside). Pexels or existing assets with known rights only (no paid stock). Clip library first
   (`_shared/cliplib/clip_library.py find "husband caring for sick wife"`). **If nothing fits, Dan on camera (camera scene)**:
   check the presenter framing at both edges for a same-size jump (CUT-CONTINUITY-QC), as C23 removal did in round 2.
   Colour-correct the new clip to the film (B-roll rule) and keep it distinct from C17 (BP cuff close-up on a man at 4:12).

## Where things are

- Build: `/Volumes/Extreme/_edit_work/RO-14/round2/` (recipe in `recipe/`, repo copy `.claude/skills/longform-edit/reference/ro14/round2/`).
  Build round 3 in a new `round3/` folder (copy `recipe/` and the data files: shots.json, words_out.json, plan_resolved.json,
  hf/manifest.json + hf/configs, fit/, framing/, lav.wav, pickup/, motion/; repoint `W`). Keep round 2's `final_r4/` and `review/` intact.
- Round 2 master: `round2/final_r4/RO14_MASTER.mp4`, sha256 2cc1d8e26e28310067ff233570c4be4d0216de890a48ef6cdb01abf666aac087,
  15,212 frames (8:27.6). Delivery: `claude edited long form content/22 - Why You're Not Losing Weight/`. Review page :8965.
- Plan: `recipe/plan.py` (A-items via `ai_clip()` reading `motion/windows.json`; C16 is a plain `kind="clip"` with `src`).
  `resolve.py` then the build: `renderq.py run --group RO-14 -- python3 recipe/build.py range 0 507.574 final/RO14_MASTER.mp4`.
  Only A1 and C16 change, so all HyperFrames renders stay as they are (do not re-run `from_plan.py`; G01 ends via manifest `b`).
- AI clip state: `round2/veo/job.json`, takes in `round2/veo/`, reviews in `round2/motion/reviews/`, specs `round2/motion/specs/`.
  **Six newer takes sit undownloaded in the Flow project "RO-14 round2"** (https://flow.google.com/project/c7b955ce-dfe8-4220-82a0-19fbae0652a2):
  A1s (2 more takes, START frame only), A2r3 t4, A6q x2, A2q x2, A2qs x2. Chrome stopped saving Flow downloads mid-run
  (`_shared/veo/README.md`, Traps). Only the A1s takes matter for round 3.

## Then, in order

1. **A1, try for a longer clean take.** (a) Dan allowed automatic downloads for flow.google.com on 2026-10-22 (Chrome site
   settings), so collect the two A1s takes from the Flow project first. (b) Generate new takes in Flow (the account showed Ultra, about 8,500 credits; Fast costs 10, Quality 100):
   START frame only (`round1/aiframes/A1-start.png`; the approved END frame's display position cannot connect to the floor scale's,
   which is why every START+END take doubled the display), Veo 3.1 Quality, 2-4 takes, prompt from
   `round2/motion_prompts/A1q.txt` plus the payoff: after lifting it he **taps the display and shakes the scale, frowning, as if it
   is broken**; both feet clear of the scale; locked camera. Download each take right after it finishes. Spawn the `flow-veo` agent
   (Claude) or follow FLOW-RUNBOOK (Codex).
   (c) Screen each take yourself first (lift: one rigid scale, one display, same size; feet; camera locked), then
   `clipcheck.py` on the chosen window (spec `round2/motion/specs/A1.take.spec.json`) and a fresh `frame-reviewer` with the
   playback-speed rule in its brief (faults under ~0.5 s that a viewer cannot see are notes; anything seen at speed, or broken cause
   and effect, fails). Freeze the rug if it boils (`round2/motion/rugfix.py`).
   (d) If no take passes for the full lift, the fallback is the longest clean window that still shows him lifting the scale and
   looking at it; ask Dan nothing until a pass or this fallback exists. Never ship the doubled display.
2. **C16.** Find and grade the caregiver clip (or camera scene), check its edges and that it shows the line with the sound off.
3. Rebuild, then the round 2 finish chain on the new master (`recipe/finish_chain.sh`, repointed): audio gate, transcript, SRT,
   chapters, watch pass + a fresh judge (`watch.py --judge`), dense hair check plus `recipe/hairedge.py` (every frame, 1080p and the
   540p copy), graphics checks, negative-events scan for the new sha, edit sheet + `validate.py --hash`, delivery gate
   `--format longform`. Expected gate result: only the 4 known rows RO-17 also failed (audio tone, push coverage, two burned-caption
   rows); anything else is a real failure.
4. Independent `ra-reviewer` on the new file, scoped to the two changes plus a normal pass (Dan's three AI questions on A1).
5. Deliver into folder 22 as round 3 (keep round 2 files), copy to `Videos to Review/Not Losing Weight LFC R3 - full film.mp4`
   (replace the R2 copy only after R3 exists), refresh the page on :8965 (round 2 page builder `recipe/page_r2.py`, a round 3 JSON),
   and give Dan the later-round revision list with exact timestamps and watch ranges in chat. `scripts/edit-queue/queue.py set RO-14
   delivered`, mirror to the Edit Queue artifact db, board entry, commit with `safe-push.sh`.

## Known state and risks

- The Mac's render queue was saturated by other sessions on 2026-10-20/21 (waits of 40-120 min per step). Use `--priority` only for
  the steps Dan is waiting on; run long steps in the background.
- The Extreme drive filled up during round 2 (0.7 GB free once); delete only your own superseded intermediates.
- Main-folder pushes are blocked by other sessions' live edits and a 9-file merge conflict; round 2 commits (bad60e5 and the board
  note) are local. Push from the main folder with `safe-push.sh` when it clears.
- Paid Veo: $2.40 of Dan's $7 approval used; the paid service refuses the A4 START frame (E005). Flow first.

## Cost ledger

RO-14 to date about $3.45 of the $15 cap (Gemini ~$1.05, paid Veo $2.40). Flow generations are on the subscription.

## Starter prompt

> CONTENT (LFC). Name this task `Not Losing Weight LFC R3`. Read and execute
> `Handoffs/handoff-20261021-ro14-round3-scale-and-caregiver-clip.md` (my round 2 notes are recorded in it). Make the broken-scale
> opener run longer so it is clear the scale is broken, replace the clip at 4:06 with a man taking care of a woman's health (or a
> camera scene), then rebuild, run every gate and the independent review, and send me the review copy with timestamps.
