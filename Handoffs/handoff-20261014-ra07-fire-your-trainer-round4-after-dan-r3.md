# RA-07 "Fire Your Trainer!": round 4 (broken arm, gym closed, leg press out of order, after Dan's round 3 notes)

**AD (short-form, filmed).** Sidebar name for the next task: `Fire Your Trainer AD R4`.
Rewritten 2026-10-16 after Dan's round 3 notes (Claude Opus 5.5). Job doc: `Handoffs/video-editing/RA-07-fire-your-trainer.md`.
Dan's words, verbatim, with each item: `/Volumes/Extreme/_edit_work/ra07/round4-plan/decisions.json`.
Round 3 page: http://127.0.0.1:8847/. Recipe: `.claude/skills/ad-edit/reference/ra07/round3/`. **Read `/ad-edit` "RA-07 round 3
lessons" first** (machine frames fail review many times; carried takes need clipcheck + a reviewer before you build; one CTC window
for caption evidence; pushed cards need tracked label references).

## What Dan said (2026-10-16)

| when | his note | what it means |
|---|---|---|
| ~0:37, injury | "use the clip of the guy with a broken arm going up to the squat rack... He can't do the squats because he has a broken arm. Then he goes on the leg press. We have already generated these clips." | Library clip **A0179** (RA-04's finished clip, approved by Dan there) replaces the tweaked shoulder (I3a) AND the shoulder-fix slot (I3b). The lateral-raise frame work is dropped. |
| ~0:39, can't make it to the gym | "He goes to the gym, and it's closed... some kind of closed sign on the gym, so then he does dumbbell curls... use the clips we already generated" | Gym closed, then the home curls (A0039, already RA-07's M1). **The gym-closed clip was never generated** (see below). |
| ~0:42, equipment broken | "change this to the leg press machine being out of order... and then he does a hack squat machine instead" | New out-of-order clip on a LEG PRESS, then the hack squat. Why: no repeat of the squat rack from the broken-arm clip, and "a barbell cannot be out of order". |

**Not found: a gym-closed clip.** On 2026-10-16 the clip library, every folder in `/Volumes/Extreme/_edit_work`, Codex's logs and the
other tasks' transcripts were searched. RA-04 ("How AI Real Abs") and RA-05 ("Top 3 Tips") each offered "Gym is closed" as an idea
(a man walks up to a gym door with a CLOSED sign, shrugs, cut to him working out at home) and Dan chose other clips, so it was never
made. It is new: START/END frames for Dan's approval first, then motion.

One thing to show Dan on the page, not to change: A0179 ends on the broken-arm man doing a leg press, and about 3 s later another
man finds a leg press out of order. Dan chose both; build exactly that.

## The run 36.47-47.01, recommended layout (check it against the word times in `words_aligned.json`)

Words: "when life gets in the way, When you get injured" 36.54-38.48 / "or you can't make it to the gym one day," 38.58-40.06 /
"or when the equipment you need is broken." 40.50-41.98 / "AI adjusts your plan in seconds," 42.22-43.74 / "while human trainers
leave you confused until next week." 44.00-46.80.

| clip | slot | source |
|---|---|---|
| Broken arm | 36.47-38.58 (2.1 s) | A0179 in two pieces joined by its own scene change: the rack and the head shake (about 1.17-2.2 s of A0179) then the leg press push (about 3.3-4.3 s). The phone part is optional; Dan did not mention it. A0179 is already sped 1.249x: never speed it further or hold a frame. Raw takes if you need more: `ra04/round3/motion/AI1-12_*.mp4`, `AI1-3_*.mp4`. |
| Gym closed | 38.58-39.80 (1.2 s) | NEW AI clip (frames first) |
| Home curls | 39.80-41.02 (1.2 s) | A0039 (M1), label as placed in round 3 (`s75r3_clips.py`) |
| Leg press out of order | 41.02-42.40 (1.4 s) | NEW AI clip (frames first), same man and look as the hack squat clip |
| Hack squat | 42.40-44.00 (1.6 s) | `round3/motion/I4bW_v1.mp4` f22-67 (nod, towel, steps on; PASS), plus the lift if it gets made |
| Back next week | 44.00-47.01 | I5, unchanged |

Every clip at least 1.2 s; `splices left inside holds: []`. Re-check the first 30 s stays frame-identical.

## Round 4, in order

1. **Budget first.** $10.00 of the $10 cap is spent; the round 3 page asked to raise it to $20 and Dan has not answered. Frames
   (Codex) cost nothing; any Kling take needs his number. Put the question first on the page, alone.
2. **Frames for the two new clips** (Codex subscription, `codex-image.sh`, two at a time):
   - *Gym closed:* START: a man in gym clothes walks up to the glass door of a gym with a printed CLOSED sign on it. END (derived
     from START with `--image`, same camera): he reads it, shoulders drop, a shrug. Ideally the same man as the home curls (A0039:
     short grey hair, beard, black t-shirt, black shorts), so the cut to his living room reads as one story.
   - *Leg press out of order:* START/END like round 3's I4a (walks up, sees a yellow OUT OF ORDER sign hanging on the machine, turns
     and shrugs) on a plate-loaded LEG PRESS. Identity: the hack squat man (`round2/frames/I4b-start.png`). Machine reference: RA-04's
     approved leg press frame `/Volumes/Extreme/_edit_work/ra04/round2/frames/F4h.png` (it passed seven reviews). The machine never
     moves in this clip, so lock its pixels with `round3/frames/lock_tone.py`.
   - Gate every pair (`_shared/framecheck/gate.py` with a spec) and a fresh `frame-reviewer`, then a page with both pairs in context
     for Dan's yes. Motion only after his yes.
3. **Re-lay the cut** (`s70r3_plan.py`: drop I3a/I3b/I4a, add the broken-arm, gym-closed and leg-press slots per the table) and
   build the whole 9:16 with A0179 in place and labelled placeholders (the START frame) in the two new slots, so Dan sees the order.
   Run A0179's used ranges through `clipcheck.py` + a fresh reviewer first (it was approved before that rule).
4. **Still open from round 3** (only if Dan gives the budget): the hack squat lift (a START/END pair of the rep, fixed rails and foot
   platform, frames gated first) and the same-sheet clip (I2) retake from `round1/frames/I2-*.png`, currently Dan on camera
   at 31.63-34.30.
5. After Dan approves the new frames: motion, clipcheck + reviewer per take, the whole 9:16 with every gate, the watch pass and a fresh
   `ra-reviewer` (chain: `round3/chain_v3.sh`, plan `s93r3_gateplan.py`, page `s87r3_page.py`). Deliver, page, edit queue `delivered`.
6. **Then the 16:9** from the same cut and sound (edit sheet, gate, watch, review), once the 9:16's clip slots are settled.

## Recommended model

Claude Opus 5.5, high effort. Escalate to Fable 5.1 only for a clip Opus fails twice.

## Starter prompt

> AD. Rename this task `Fire Your Trainer AD R4`. Read `Handoffs/handoff-20261014-ra07-fire-your-trainer-round4-after-dan-r3.md` and run round 4 of RA-07 "Fire Your Trainer!" with /ad-edit: put the broken-arm clip at the injury, make the frames for the gym-closed clip and the leg press out of order, re-lay the run so each fix follows its problem, build the whole 9:16 with placeholders in the new slots, and send me the page with the new frames for my approval. AI clip budget: [$20 / other]. Use the Codex subscription to generate any new images.
