# Handoff: Fable makes three more AI-Dan exercise demos on Google Flow (2026-11-09)

**Type:** in-app exercise demo (not a content video, not an ad). **Owner:** Claude **Fable 5.2, high effort** (Dan, 2026-11-09: "a handoff document for Fable to make three more exercises using Google Flow"). This is Dan's explicit pick, so it overrides the usual "edits stay on Opus" routing for this job.
**Authorization:** do every step without asking; stop only for Dan's review. Google subscription first for video and images (AGENTS.md, 2026-11-08). Paid Replicate Veo only after a recorded Flow failure, capped at **$10** for this session (inside the $25 standing cap). Up to **5 video takes per exercise**. Do not install anything in the app until Dan says ship.

## The three exercises (not done, not owned by another session)

| id | name | library text (`public/exercises.js`) | camera to start from |
|---|---|---|---|
| `db-kickback` | Triceps Kickback | Hinge forward with a flat back, upper arms pinned parallel to the floor. Extend the forearms straight back until fully straight, squeeze, return. Mistake: dropping the upper arm (only the forearm moves). | true side view, his side to the camera, so the upper arm reads parallel to the floor |
| `db-pullover` | Dumbbell Pullover | On a bench, one dumbbell held in both hands above the chest. Lower it in an arc behind the head to a lat stretch, pull back over the chest. Mistake: bending the elbows more as you lower (arm angle fixed). | side view, bench parallel to the camera (like the fly), head left |
| `db-rear-delt-fly` | Bent-Over Dumbbell Rear Delt Fly | Hinge forward, flat back, light dumbbells hanging under the shoulders, slight elbow bend. Raise them out to the sides like spreading wings, squeeze, lower slowly. Mistake: swinging the torso. | three-quarter front, so both arms open visibly left and right |

Do NOT touch these, they belong to other sessions: chair-squat, db-lunge, bicycle-crunch, db-crunch, db-fly, db-tricep-extension (Claude, [three more demos R3](#local_7682bfb2-8dcd-4311-98b9-22b4c22e9529)), hammer curl, floor press, hip thrust (Gemini), db-shrug, ez-bar-curl, machine-chest-press (Codex).

## Read first

1. `.claude/skills/exercisegeneration/SKILL.md`, all of it, including the new "Three more (2026-11-07): frame-stage traps" section at the end.
2. `Handoffs/handoff-20261106-exercise-demos-three-more.md` (what the last round did, step by step, and its R1/R2 results) and `Docs/EXERCISE_DEMO_FLOW_PILOT_20261105.md`.
3. `.claude/skills/_shared/veo/README.md`, `FLOW-RUNBOOK.md` and the `flow-veo` agent (`.claude/agents/flow-veo.md`) for video; `.claude/skills/_shared/blind-image/FLOW-IMAGE-RUNBOOK.md` and `_shared/IMAGE-GENERATION.md` "Blind Google test" for images.
4. AGENTS.md: "Google AI subscription first" (2026-11-08) and "Empty gym backgrounds stay still" (2026-11-08).

## Dan's form notes from the last round (2026-11-09), bake them in

- **Fly: "his arms aren't bent enough. His arms are excessively straight."** Our fly ran at about 170 degrees of elbow. For any arm-arc move (pullover, rear delt fly) draw a clearly visible, natural elbow bend, roughly 140 to 155 degrees, held the same through the rep. Not locked straight, not a press.
- **Overhead triceps extension: "the motion looks right, but I want them sitting."** Prefer the seated or supported version when a move has one; for these three, the kickback and rear delt fly stay as hinge moves per the library.
- **Weighted crunch was approved to ship** as built: short range, side view on a mat, dumbbell on the chest, background locked. That build is the quality bar.

## Pipeline (what worked, in order)

1. **Workspace:** `python3 .claude/skills/_shared/renderq/renderq.py workdir EXDEMO-FABLE3 --need 5` (internal drive), then make each `Media/exercise-demos/<id>` a symlink into that folder, so the existing tools (which assume `Media/exercise-demos/<id>`) work while the files live on the internal drive. `editcap.py acquire EXDEMO-FABLE3` before the first generation; `release EXDEMO-FABLE3 --review` when the page is up.
2. **Voice-over first** (cheap, ~$0.01 each): MiniMax `speech-02-hd`, voice `R8_NE3EBC2N`, via `Media/exercise-demos/_flowpilot/gen-vo.js <new json>`. Open with "Here's how to do the ...", then setup, execution and the mistake line from the library, `<#0.3#>` pauses, 15 to 18 s. No em dashes.
3. **START and END frames, two blind pairs per exercise:** one pair from Google (Nano Banana Pro in Flow, Image mode, 16:9, 1K Original size download, 0 credits) and one from Codex (`.claude/skills/_shared/codex-image.sh --image Media/exercise-demos/_character/ai-dan-canonical.jpg`), same prompts and references. Each END is an edit of its own START on the same model. Run the Google side as a background Sonnet agent following FLOW-IMAGE-RUNBOOK. Register both with `blind.py add`, never tell Dan which model made which.
   - Prompt pattern: copy `Media/exercise-demos/db-crunch/fp-start-prompt.txt` and `fp-end-prompt.txt` (identity paragraph, explicit camera, every joint angle and contact point, name the wrong pose: "this is NOT a ...").
   - Plan the END prop position against the path Veo will take: a straight line from START to END must not cross his face (the fly END that put the dumbbell head-side of the shoulder made every take sweep across his face).
4. **Clean each END:** `framecheck/lockstill.py START END OUT --box <moving prop at START> --box <moving prop at END>`. Size boxes around the whole prop with margin (a box that clips a dumbbell leaves it see-through). Add a box over any patch a body part vacates, or START's contact shadow comes back as a stain (crunch mat). Never let a box overlap the bench or machine feet.
5. **Gate and review each pair:** `framecheck/gate.py START END --spec spec.json` (spec needs `person.anchored`, `person.compare` with a reason, 3 textured `still` boxes, `props`, `camera: "locked"`; declare a vacated or landing patch in `may_change` with a written reason), then a fresh `frame-reviewer`. Under the Fable trial in AGENTS.md, run the first 3 reviewers with `model: "fable"` and log them in memory `fable-5-2-release`. Expect 1 to 3 review rounds per pair; reviewers caught a floor patch tone step, handle style changes between frames and a bench foot clipped by a box. A Google pair that fails twice is dropped; the Codex pair goes forward.
6. **Video on Flow first:** `veo.py add JOBDIR <ID> --start S --end E --prompt-file P --seconds 8 --model fast` (one job folder per exercise), then spawn `flow-veo` in the background. Download 1080p Upscaled. Check the live result yourself: the old note that Flow's 720p render garbles the chest print is not evidence it still does (AGENTS.md). Only if a Flow take actually fails the print or motion checks, write the failure into the job folder, then fall back to `veo.py api JOBDIR <ID> --paid-ok "<Dan's words above>"` (4 s, $0.40 a take).
   - Motion prompt: copy `Media/exercise-demos/db-crunch/CR2.txt`, including the one-direction / no-pause block and "lips closed, eyes open, print sharp".
   - Change the prompt or the frame between takes; the same frames plus a near-identical prompt gave a near-identical take twice.
7. **Cut at native speed, never setpts:** measure frame-to-frame velocity on a crop around the moving part and cut from a velocity minimum to the next one. Veo often does an extra partial rep first: the clean stretch was the SECOND lowering in both triceps takes. Run `clipcheck.py TAKE --spec spec --frames A:B`, then a fresh motion `frame-reviewer`.
8. **Build:** `zsh ~/Projects/_edit_work/EXDEMO-3MORE/build2.sh <id> <take.mp4> <t0> <t1> 1.0 v1 "--hold 0.17"` (copy that script into the new work folder; it is the pilot `build.sh` plus a hold option and a fixed scratch path). It cuts the palindrome, locks the background, runs the ghost scan, qcunit, the audio gate and the delivery gate, and writes `_flowpilot/app-staging/<id>-v1.mp4`. Then run the new background check `.claude/skills/exercisegeneration/reference/background.py` on every native frame of the unit and on the final narrated file, with reviewed per-frame masks (AGENTS.md, 2026-11-08).
9. **Review page:** copy `~/Projects/_edit_work/EXDEMO-3MORE/mkpage.py` and `entries.json`, point them at the new folder, both blind versions of each exercise on the page labelled X1/X2, plain notes on what is right and what is still off. `review_server.py PORT DIR`, open with `?review_mode=automation` at phone width, check silently at 1080p, then `AbsReviewAudio.handoff()`. Log Dan's picks with `blind.py pick`.
10. **On "ship":** install as in the 2026-11-06 handoff, "Deliver" step 3 (copy to `public/exercise-demos/<id>.mp4`, poster at 1.0 s, re-gate, stamps out of `public/`, add the id to `EXERCISE_DEMO_IDS` in `public/index.html`, `safe-push.sh`, Railway deploy, check on absbyai.com).

## Known traps

- Edit models redraw the whole frame; lockstill fixes the background but not the prop or the floor right under it: compare those to START by eye before gating.
- Front views of overhead arm moves made Veo flare the elbows (3 of 3); side or three-quarter fixed it.
- Push with `scripts/git/safe-push.sh` only. If it stops on another session's files, follow AGENTS.md (`--adopt-stale` for files older than 2 hours); never hand-merge other sessions' files.
- `renderq.py workdir --help` and `editcap.py acquire --help` treat `--help` as a job name and create junk entries; read the script headers instead.

## Deliver in chat

The review page link, one line per exercise (what is right, what is still off), Flow credits used, any paid fallback with the recorded reason, and the two wrap-up boxes.
