# Campaign Images AD R2

Written 2026-10-01. Ready for a new task; revisions have not been built.
Recommended model: **GPT-6 Astra, High effort**, per `model-routing-plan` (image generation).
Rename the next task **Campaign Images AD R2**.

**Use the Codex subscription to generate the images.**

## Goal and stopping point

Build five targeted revisions from Dan's round-one feedback: K1, K2, R5, R6 and R8. Preserve his 15 unchanged picks. Present the five revisions on one review page and stop for approval. R7-c is now selected and stays unchanged. Do not create extra concepts, rebuild the 100-image set, export a final campaign package, upload to Drive, or create or change any campaign in this round.

This handoff supersedes the build and selection steps in `Handoffs/handoff-20261001-campaign-images-build.md`. That earlier document remains the full creative brief and eventual export specification. Dan's explicit changes below take precedence.

## Exact revisions

| Revised ID | Keep this design | Use this photograph or change |
|---|---|---|
| K1-r2 | K1-b landscape scene, layout and headline | Replace the Dan photo with the real Dan photo used in K1-a. |
| K2-r2 | K2-b square scene, layout and headline | Replace the Dan photo with the real Dan photo used in K2-a. |
| R5-r2 | R5-b portrait scene, layout and headline | Replace the Dan photo with the real Dan photo used in R5-a. |
| R6-r2 | R6-b landscape scene and clean, text-free layout | Replace the Dan photo with the real Dan photo used in R6-a. Keep it text-free. |
| R8-r2 | R8-c blue kitchen, red-haired nutritionist, rounded pearl robot with teal eyes, composition and headline | Change the seated dad's expression and hands to the ready-to-eat action in R8-a. He holds a fork in one hand and a knife in the other, hands separated, smiling eagerly at the food. No clasped hands, clapping or praying pose. |

The A and B entries in Dan's submitted pick list for K1/K2/R5/R6 are source references for ONE combined revision per slot, not requests to deliver both unchanged. R8-c and R8-a similarly describe ONE revised R8-c.

All four A photographs above are **`studio-white-49`**, with glasses and black shorts. The B photograph being replaced is `studio-white-25`, with glasses and denim shorts. Use the original white-49 cutout, not a crop extracted from a flattened JPG. Match the chosen B scene's warm light in code. Keep Dan's identity, face and physique photographic and unchanged.

Dan's R8 wording: "I like the R8C design the best; however I don't like the guy's expression there or what he's doing with his hands, where it looks like he's clapping." He wants "holding the fork and the knife ready to eat" like R8A.

## Recorded picks

| Slot | Dan submitted | Next-round status |
|---|---|---|
| K1 | K1-a, K1-b | Combined revision above |
| K2 | K2-b, K2-a | Combined revision above |
| K3 | K3-b | Keep unchanged |
| K4 | K4-d | Keep unchanged |
| K5 | K5-d | Keep unchanged |
| K6 | K6-d | Keep unchanged |
| K7 | K7-d | Keep unchanged |
| K8 | K8-a | Keep unchanged |
| K9 | K9-c | Keep unchanged |
| K10 | K10-b | Keep unchanged |
| R1 | R1-b | Keep unchanged |
| R2 | R2-b | Keep unchanged |
| R3 | R3-a | Keep unchanged |
| R4 | R4-a | Keep unchanged |
| R5 | R5-a, R5-b | Combined revision above |
| R6 | R6-a, R6-b | Combined revision above |
| R7 | R7-c | Keep unchanged; Dan confirmed in his follow-up |
| R8 | R8-c, R8-a | Targeted revision above |
| R9 | R9-d | Keep unchanged |
| R10 | R10-e | Keep unchanged, clean portrait |

Dan confirmed R7-c after sending his initial list. All 20 slots now have a selection or a specified revision. The original brief requested a clean image in every shape; Dan chose K9-c with text. Preserve this explicit choice and record the cold clean-portrait requirement as unresolved for eventual packaging, without adding an unrequested image now.

## Existing work and source paths

Project root when written: `/Users/danielrose/Documents/Claude/Projects/Abs By AI`. If the planned project move has happened, resolve the same relative paths from the current project root.

Round-one folder: `output/campaign-images-20261001/`.

- `options/ID.jpg`: all 100 finished round-one images, including every reference above.
- `plates/ID.png`: corresponding original AI scenes, without composited Dan or headline.
- `manifest.json`: sizes, source photo IDs, headlines and scene metadata.
- `build.py`: tested composition recipe, real photo crop, grade, shadow and headline placement.
- `review.py`, `index.html`: original review-page generator and page.
- `prompts/`, `logs/`: generation inputs and receipts.
- `BUILD_RECEIPT.json`, `build-check.json`, `qa/visual-checks.json`: counts, file checks and manual visual review records.
- Current round-one URL: http://127.0.0.1:52737/ (local server, may need restarting).
- Real cutout: `photos/finalized social media photos/_cutouts/studio-white-49_CUTOUT.png`.

All 100 files were individually inspected. Eight framing failures were replaced. The count, unique file hashes, dimensions and JPG sizes were verified. Round one used the Codex subscription only; paid generation spend was **$0**. No campaigns were touched. No final Drive package exists.

## Build instructions

1. Read `.claude/skills/_shared/VIDEO-RULES.md` and `.claude/skills/_shared/IMAGE-GENERATION.md`. Inspect the source JPGs and plates named above before editing.
2. Work under `output/campaign-images-20261001/round2/`. Preserve all original files and IDs. These photo assets stay out of the public Git repository.
3. Rebuild the four Dan composites from each exact B plate with `studio-white-49`. This requires no image generation. Adapt the existing recipe while keeping the B layout, `variant='b'` lighting grade and original headline. The original white-49 crop ends at `.87` of its source height. Retain visible abs, centered placement and soft shadow. If copying `build.py` into round2, fix its project-root calculation: its existing `P.parents[1]` assumes the original folder depth.
4. Edit **`plates/R8-c.png`**, using `plates/R8-a.png` as the hands/expression reference. Preserve the C design, cast, kitchen, robot, nutritionist and food. Change only the seated dad's expression and arm/hand action as needed. Feed the text-free plates to the image tool; add the original headline in code afterward. Do not regenerate the whole scene from a text-only prompt.
5. Use `.claude/skills/_shared/codex-image.sh` with repeatable `--image` references, or the subscription's built-in image-editing tool. State the count before generating: one targeted R8 edit initially. The task's $50 paid fallback allowance remains unused. Paid fallback only after Codex fails twice, with estimated cost stated first and a running total; do not spend on the four simple composites.
6. Save the five revised JPGs with the IDs above. Sizes: K1/R6 1200x628, K2/R8 1200x1200, R5 960x1200. Each under 5 MB. Headlines stay Manrope ExtraBold, white first line, yellow second line `rgb(255,214,10)`, black stroke, centered in the top band. R6 has no headline.
7. Inspect all five at full size. Check real source-photo identity, scene preservation, lighting match, visible abs, hands and fingers, correctly held fork and knife, facial expression, no extra limbs, no stray text, no clipped heads and no headline over a face. A successful tool call is not a quality pass.
8. Build one round-two review page showing each revised image next to its relevant original references. Include the 15 unchanged picks in a clearly marked section including R7-c. Keep round-one accessible. Verify full-size viewing and any pick controls, open the page for Dan, and stop for his approval of the five revisions.

## Exact next action

Inspect K1-a/K1-b, K2-a/K2-b, R5-a/R5-b, R6-a/R6-b and R8-c/R8-a. Then make the four source-photo swaps and one targeted R8 edit. There is no need to request permission for those revisions.

## Ready-to-paste starter prompt

Name this task `Campaign Images AD R2`. Read `Handoffs/handoff-20261001-campaign-images-round2.md` and execute it. Use the Codex subscription to generate the images. Make the four A-photo/B-design combinations for K1, K2, R5 and R6, and revise R8-c so the dad holds a fork and knife ready to eat like R8-a. Preserve my 15 unchanged picks, including R7-c. Put the five revisions on one review page with their references, then stop for my approval. Do not build or change any campaign.
