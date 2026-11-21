# Handoff: Flow credits, AI clips batch 2 video + batch 3 (2026-11-13)

**Owner:** Claude, Opus 5.5 high. Flow work by background `flow-veo` agents (Sonnet). Reviewers: `frame-reviewer` on Opus 5.5
(the 3-run Fable 5.2 trial is done and logged in memory `fable-5-2-release`; use Fable again only if Dan says so).
**Authorization:** Dan, 2026-11-07 (parent handoff) and 2026-11-13: "Everything is approved. Finalize all these, store them in our clip
library, and give me a handoff for a new batch." Do every step without asking; stop only for Dan's picks (frame pages, video pages) and anything
that would cost money. Never pay, top up or buy credits.
**Deadline and budget:** spend by **Nov 28** (Ultra 20x drops to 5x on Nov 29). This work has used 240 of its 14,000 credits; balance was
21,586 on 2026-11-09. Read the balance before and after each batch and add a line to `Media/flow-credit-log.md`. Veo 3.1 Fast = 10 credits a take,
Omni 1.1 Flash = 12, Nano Banana Pro images = 0. Never Veo Quality unless Dan asks for it by name.
**Parent:** `Handoffs/handoff-20261107-flow-credits-ai-clips-for-next-edits.md` (rules, sources). Receipt to keep current:
`Docs/FLOW_CREDITS_CLIPS_RECEIPT_20261128.md` (finish it by Nov 28).

## Done so far

- Batch 1: 8 clips approved and filed: A0247-A0254 (+ library A0159 for DS-95). IDs are under "Pre-made AI clips" in the DS-97, DS-100,
  DS-102, DS-103, DS-50 and DS-95 job docs. Work folder `~/Projects/_edit_work/FLOWCLIPS/vid-b1/`.
- Batch 2 frames approved by Dan (2026-11-13): folder `~/Projects/_edit_work/FLOWCLIPS/b2/` (ideas.json, prompts/, codex/, google/, pairs/,
  review_results.txt, frames page http://127.0.0.1:9242/). Every pair below passed gate + a fresh reviewer (`gate.py START END --verify` exits 0):

| id | idea | video (job) | approved versions (files) |
|---|---|---|---|
| B2-01 | Can't Go In (arm in cast, looks into gym window) | Why I Use Machines And Cables Instead Of Barbells At 41 (DS-99) | codex/B2-01-*, google/B2-01-* |
| B2-02 | Sitting On His Phone (between sets) | Why You Should Walk Between Your Sets (DS-103) | codex/B2-02-*, google/B2-02-* |
| B2-04 | Laid Up (thin man, hospital bed, leg cast) | Why You Must Stretch After Every Workout (DS-104) | codex/B2-04-* |
| B2-05 | The Straddle Stretch | same (DS-104) | codex/B2-05-*, google/B2-05-* |
| B2-06 | Thermostat On 63 (sleeping peacefully) | Why I Sleep At 63 Degrees (DS-50) | codex/B2-06-* |

  Dan approved "everything" without choosing between the two versions, so make video from **both** versions where there are two;
  he picks between finished clips. Log that pick with `blind.py pick b2/sets/<id> --chose Xn` (sets are built by `b2/build_page.py`).

## Step 1: batch 2 video (do first)

Same routine as batch 1 (`vid-b1/` is the worked example: prompts/, specs/, MOTION-REVIEWER-BRIEF.md, windows.json, review/ page builder):
1. New job folder `~/Projects/_edit_work/FLOWCLIPS/vid-b2/`. Write one motion prompt per clip: locked camera, what never moves, the one motion,
   "his face keeps the same calm expression, lips closed and resting, jaw still; he does not talk". Never write "smile" or "breath".
2. `veo.py add` each approved pair: Veo Fast `--takes 2` plus an Omni twin `<id>o` at 6 s. One `flow-veo` agent for the whole job
   (tell it: check the 9:16 chip and the model chip before every submit; own tab; never touch other tabs).
3. Screen every take yourself first on 1 frame/s strips (`vid-b1/strips/` method); drop takes with belly reveals, objects appearing,
   wrong action. Pick the best take per clip; run `clipcheck.py` through `renderq.py run`; then one fresh motion reviewer per kept take.
4. Expect faults late or early in a take (talking mouths, growing grins, extra people appearing, hands smearing at the end). The reviewer
   names a clean WINDOW; cut each clip to it. A clean 2.5-5 s window is enough.
5. Video page phone-first (copy `vid-b1/review/` builder; `Start silent checks` / `Finish checks for owner` before handoff), Dan approves,
   then file: `clip_library.py add <window cut> --kind ai --status usable-unused --used-in "<job> <title> (planned)" --tags flow-credits-batch2`,
   `clip_library.py sheet`, and add the IDs under "Pre-made AI clips" in each job doc.

## Step 2: batch 3 ideas (in parallel with step 1)

Still unedited January Shorts with lines but no clips yet (check `Handoffs/video-editing/00-MASTER.md` that each is still READY and nobody
has claimed it; skip anything IN PROGRESS):
- 10/23 gym Shorts: What To Do Your First Day At The Gym (DS-95, has A0159), How To Pick The Right Weight (DS-96), The Only 5 Machines
  You Need (DS-98), How To Use The Stairmaster To Burn Fat (DS-94). Lines: `Media/footage-index/shoot-20261023/queue-jobs/DS-xx.json`
  (`all_take_segments`).
- 10/15 talking Shorts: 3 Ways To Lose Fat Without Losing Muscle (DS-51, C1759), Why I Train With A Timer (DS-57, C1777), The Only 2
  Exercises For Lower Abs (DS-46), The Only 2 Kettlebell Exercises (DS-54), The Only Ab Exercise That Hits All 4 (DS-56), Reverse Lunges
  (DS-60), Goblet Squats (DS-62), 3 Rules For Every Rep (DS-64). Lines: `Media/footage-index/10-15-.../<roll>.roll.json` (`transcript.text`).
  How-to demos use REAL footage, never AI (rule 2026-11-13); AI clips only for opinion and "why" lines.
- Search `clip_library.py find` before every idea; offer existing clips first (they cost nothing).
Then: 20-30 ideas, Codex + Google START/END pairs (blind), screen yourself, gate + fresh reviewer, one phone-first page with
**Select** buttons (memory `review-pages-select-not-kill`: untouched means out), Dan picks, then the step 1 video routine.

## Dan's taste (read before writing ideas)

Memory `ai-clip-gags-injury-and-sense` (2026-11-08): no jokes about serious injury (injury lines play straight); every gag must read in one
look; sleep clips show sleeping well; stretches are straddle or pigeon, not a seated fold; trace every hand to its arm (he caught a hand
"coming from his stomach"). He approved: mirror self-check, bathrobe at the gym, caution tape, paramedics by a deadlift, injury-count sign,
bench press in a museum, jiu-jitsu jog, waking up sweating. He rejected: map, plan card (QC miss), dusty gym bag, bouncer, recliner,
hospital curls, ski goggles in bed, penguin.

## Traps that cost time (more in `.claude/skills/ai-clip-ideas/SKILL.md` lesson 6)

- Codex END edits re-texture fabric and redraw faces and machines: say "same fabric, same face, the machine does not move" in every END.
- Google often makes END = START, toothy grins, or a sideways picture with a fake "REC" overlay when the project chip is on 16:9.
- A pair whose END fails twice is dropped (VIDEO-RULES). Screen pairs yourself before reviewers; about half fail first review.
- Never edit a spec after `gate.py` ran; `--verify` refuses until re-gated (then re-record the existing review with `--review`).
- `blind.py build` needs two sources; a one-version idea is shown as plain X1 (`.single-key.json`), not a comparison.
- Copied scripts: fix hard-coded batch folders and globs (`B1-*`) before running.
- Flow's own Agent cannot run a multi-clip brief or self-check (tested 2026-11-08: 1 of 3 clips, no checks). Use `flow-veo` agents.
- Reviewers are the main Claude cost (~150k tokens each). Screen first; send reviewers only takes you would use.

## Starter prompt

> Execute `Handoffs/handoff-20261113-flow-credits-ai-clips-batch-2-3.md` end to end: make the batch 2 videos from Dan's approved frame
> pairs, then batch 3 ideas for the next unedited January Shorts, using the Google Flow credits by Nov 28. Bring me the pages, then
> file what I approve in the clip library.
