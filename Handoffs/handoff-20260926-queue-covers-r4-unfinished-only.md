# Queue covers round 4: unfinished rows only

Prepared: 2026-09-26. Recommended model: GPT-6 Astra, high effort.

Dan reviewed this task's round 3 gallery and finalized most covers. Build the remaining revisions for rows 12, 13, 14 and the Instagram version of row 16. The next gallery must show only these unfinished items. Do not regenerate or show finalized rows again. This handoff is the next-round brief; the new images have not been built yet.

## Read and locate

- Read `AGENTS.md`, `.claude/skills/_shared/VIDEO-RULES.md` and `.claude/skills/coverimage/SKILL.md` in full before cover work.
- Read `Docs/QUEUE_COVERS_APPROVALS_20260926.json` for the exact approved export paths and hashes. `Docs/QUEUE_COVERS_R3_FBD1_REVIEW.md` records the prior build and checks.
- Shared media root: `/Users/danielrose/Documents/Claude/Projects/Abs By AI/Short-form video content/covers/review/queue-bakeoff-20260924/`. All media paths below are relative to this root unless stated otherwise. The media is Git ignored; use the absolute shared path from a worktree.
- Use **`round3-platform-layouts-20260925-fbd1/`** as the reviewed round 3 source. Its `index.html` was shown at `http://127.0.0.1:8787/index.html`. The similarly named folder without `-fbd1` belongs to a separate task and is not this approval set.
- The reviewed package includes `build_round3.py`, `manifest.json`, `inputs/`, `covers/`, `grid-crops/`, `comparison/` and `quality-checks.json`.
- Earlier source records: `round2-20260925/retouch-provenance.json`, `sources/video-frames.json`, and `Handoffs/handoff-20260925-queue-cover-revisions-r2.md` in the repository. This new feedback supersedes their conflicting frame-selection instructions.

## Finalized choices: freeze and omit from the next gallery

| Row | Final selection |
|---|---|
| 01-03 | Keep existing originals |
| 04 Deadlift trick | 04-A |
| 05 Back move with a towel | 05-A |
| 06 Three minutes | 06-A |
| 07 Four ab muscles | 07-A |
| 08 Toe touch | 08-A |
| 09 V-sit twists | 09-A |
| 10 Spiderman planks | 10-A |
| 11 Why I love the ab wheel | 11-A |
| 15 Why the ab wheel beats crunches | 15-A |
| 16 Home arm workout, horizontal YouTube thumbnail | Keep original `baselines/youtube-01.jpg` |
| 17 Deadlift trick, YouTube Short | 17-A |
| 18 Towel back move, YouTube Short | 18-A |
| 19 Three minutes, YouTube Short | 19-A |

The A approvals cover the separate Instagram and YouTube exports shown in the reviewed package. Dan initially said 9A for Spiderman Planks, then explicitly corrected it to 10A. Use 10-A. Rows 13-A and 14-A have their design direction selected, but the requested new screenshots still need review. Do not mistake those selections for approval of unbuilt revisions.

## Row 12: biggest ab wheel mistake

Keep `FIX THIS FIRST` and `THE BIGGEST AB WHEEL MISTAKE`. Use the A design as the working base, consistent with Dan's other selections; he did not separately name A or B for this row.

Replace the existing two crops of one frame with two genuinely different moments showing the mistake:

- **Top:** starting the rep, arms almost vertical, with the lower-back mistake visible.
- **Bottom:** near full extension at the bottom of the rep, still making the mistake.
- Put a red arrow on each screenshot pointing precisely to Dan's lower back. Both images must demonstrate the mistake; do not use correct-form footage with a red arrow to imply an error.

The top and bottom must read as the beginning and end of one rep. Inspect the actual movement before choosing frames. Keep the wheel, arms and lower back clear enough to teach the point.

## Row 13-A: how to do ab wheel rollouts

The A design is selected. Keep `MY FAVORITE HOME AB EXERCISE` and `HOW TO DO AB WHEEL ROLLOUTS`.

- **Top:** starting the rep, arms almost vertical.
- **Bottom:** arms extended almost fully forward near the bottom of the rep.
- Use small green arrows beneath Dan pointing to his arms and abs. Apply the cues to both views where their target regions are visible. Keep the arrows clear of the body details they identify.

Use correct-form moments and two distinct frames. Preserve the selected typography and general layout; revise the photos and cues rather than proposing another design family.

## Row 14-A: ab wheel workout tip

The A design is selected. Keep `AB WHEEL WORKOUT TIP`.

- **Top:** a new starting-position frame with arms vertical.
- **Bottom:** the fully rolled-out image currently shown in the top panel of 14-A.

Keep the same top-to-bottom start/end arrangement as row 13. The current full-extension source is `round3-platform-layouts-20260925-fbd1/inputs/row14-generated-retouch-alt.png`; its exact crop is recorded in the round 3 manifest. Recover the underlying source as needed, preserving the selected moment. Dan explicitly requested arrows on rows 12 and 13; his row 14 instruction specified this frame order.

## Source for the rollout screenshots

Use the approved finished master in the shared project:

`/Users/danielrose/Documents/Claude/Projects/Abs By AI/YouTube Long Form Video Content/The $17 Ab Wheel Beats Every Crunch - READY FOR UPLOAD/Muhammad edit/The $17 Ab Wheel Beats Every Crunch - Muhammad edit v2 HD - READY FOR UPLOAD.mp4`

Find the actual wrong-form demonstration for row 12 and correct-form demonstration for rows 13-14. Prefer clean frames without burned captions. Record source paths, exact timestamps and hashes for each new still. Do not use two crops of the same moment as start/end, invent an exercise pose, or mistake a merely extended body position for the lower-back error. If the finished master lacks the requested visible mistake, report that specific source gap before substituting a different action.

## Row 16: explanation and Instagram redesign

16-A is for the **same Home Arm Workout long-form video**, not a different video. The screenshot comes from Zeeshan's finished export:

`/Users/danielrose/Documents/Claude/Projects/Abs By AI/Zeeshan Content Videos/arms and shoulders home workout - video 2/arms and shoulders home workout | zeeshan | 16x9 | video 2.mp4`

The source inventory identifies `sources/frames/16-4.jpg` at 475.3 seconds. It shows Dan standing beside the pool with dumbbells. Round 2 made a horizontal alternative from that frame. Round 3 then made portrait companions, which caused the confusion.

Dan's new direction:

- Keep the existing original horizontal YouTube thumbnail, `baselines/youtube-01.jpg`, unchanged and finalized.
- Redesign the **Instagram cover for that same long-form video** around the photo used in the horizontal 16-A. Preserve the exact title `2-minute home arm workout`.
- Horizontal 16-A reference: `round3-platform-layouts-20260925-fbd1/comparison/16-A-round2-wide.jpg` (also `round2-20260925/covers/16-A.jpg`). Clean existing retouched source: `round3-platform-layouts-20260925-fbd1/inputs/row16-generated-retouch.png`.
- Use the clean photo source to redesign the Instagram composition; do not stretch or crop a flattened horizontal thumbnail with its text baked in. Keep Dan's face, hair, arms and relevant equipment intact, and place the title in clear space.
- Clearly label it "Instagram cover for Home Arm Workout long-form video". No further YouTube portrait concept is needed for this row. Do not reopen the finalized original horizontal thumbnail for selection.

## Build, verify and deliver

Save a new `round4-unfinished-20260926/` folder under the shared media root, preserving all prior packages. Build six separate 1080 x 1920 exports for rows 12-14 (Instagram and YouTube for each), one revised 1080 x 1920 Instagram cover for row 16, and four actual Instagram grid previews.

Instagram grid previews must be literal centered crops `(0,240,1080,1680)`, with essential type within y=240..1620. Check that both teaching moments and the arrow targets survive that crop. YouTube images should sit close beneath the headline with no unnecessary black gap. Check every image at full size and phone size for frame order, exact copy, arrow targets, complete hair, equipment, and text clear of Dan.

Deliver one browser gallery containing **only rows 12, 13, 14 and the revised Instagram 16**. For rows 12-14 show Instagram full, actual grid crop and YouTube full side by side. For row 16 show Instagram full and actual grid crop with the explicit long-form label. Include full-size links. Do not put locked rows or old rejected variants back into this gallery.

Record the new source timestamps, build steps, output hashes and visual checks. Verify the approved files still match `Docs/QUEUE_COVERS_APPROVALS_20260926.json`. This task is the revision-and-review round; preserve installed covers and all publishing queues. Do not interpret preparation of this handoff as an instruction to install the approved batch now.

## Ready-to-paste starter prompt

Execute `Handoffs/handoff-20260926-queue-covers-r4-unfinished-only.md`. Preserve all locked selections. Revise only rows 12-14 with distinct start/end rollout screenshots and the specified arrows, and redesign row 16's Instagram cover using the horizontal 16A photo for the same Home Arm Workout long-form video. Keep row 16's original horizontal YouTube thumbnail. Show only these unfinished items in the next gallery, with actual Instagram grid crops and full-size links. Preserve all queues and installed covers.
