# Great Again T VSL (WV-03) round 8 motion: collect 23 finished Flow clips (downloads blocked), Codex + Grokbot

Category: AD (WV-03, "Great Again T VSL", native 9:16). Written 2026-11-16 about 18:00 CT by the round 8 motion lead (Claude).
Dan's authorization: standing project rules. Downloads, browser work and Flow generation on his subscription need no
question (AGENTS.md "Standing authorization for downloads", "Google AI subscription first"). Do the whole step.

## What is blocked
All 28 round 8 Veo 3.1 Fast generations ran in Dan's Flow project "WV-03 R8 motion",
https://flow.google.com/project/af76ef7f-7829-4bbe-ac23-f025bd80cecf (17,745 credits left after). 23 finished, 5 came back
"No audio generated". No file could be saved: from about 17:30 CT every Chrome download on the M6 fails silently on
every site (a plain test download from example.com saved nothing either; Flow says "downloaded"). Claude cannot see or click
Chrome's own UI. Likely cause: the M6 internal disk is full (df: 1.7 GB free and falling at 18:00, 4.5 GB at 17:40).
Also check Chrome's download settings, any pending Save dialog and the "multiple downloads" permission for flow.google.com.

## Do this (Codex, on the M6)
1. Fix downloads: free space on the M6 internal drive per memory `work-drive-order` (move finished job folders to the
   Extreme or Seagate with checksums; never delete an original without a verified copy), and/or clear the Chrome block.
   Prove it with one test download.
2. In the Flow project above (Batch view shows each prompt and its frame thumbnails), download each finished tile's
   720p "Original size" (never "1080p Upscaled") into ~/Downloads and collect it:
   `cd "/Users/danrrose/Projects/Claude/Projects/Abs By AI" && python3 .claude/skills/_shared/veo/veo.py collect /Users/danrrose/_edit_work/wv03-r8/mirror/round8/motion <ID> --from ~/Downloads/<file>.mp4`
   Map tiles to IDs by the prompt's first words and the number of frame thumbnails (2 = first and last picture, 1 = first only):

   | prompt begins | frames | ID |
   |---|---|---|
   | A plain basement with grey painted block walls | 2 | AI63x1 (two tiles, both) |
   | A plain kitchen with light wooden cabinets | 2 | AI62x1 (two tiles) |
   | A plain bedroom with a wooden chest of drawers | 2 | AI64x2 (two tiles) |
   | A dim bedroom in grey morning light | 2 | AI67x1 |
   | A large open-plan office late in the evening | 2 | AI68x1 |
   | Two piles of fine light-brown root powder | 2 | AI76x1 |
   | A bright front hall with a honey-coloured wooden floor | 2 | AI73x1 |
   | A bedroom at night ... lamp on a nightstand behind the bed | 2 | AI70x1 |
   | A bedroom at night ... lamp at the right | 2 | AI70x2 |
   | A bright plain medical exam room | 2 / 1 | AI18x1r8 / AI18x1r8s |
   | A restaurant table by a big window over a beach | 2 / 1 | AI26x1r8 / AI26x1r8s |
   | An office with a window at the left, a round wall clock | 1 | AI54x1r8s (two tiles) |
   | A supermarket produce section ... red shopping basket | 1 | AI51x1r8s |
   | A supermarket produce section ... black shopping basket | 1 | AI51x2r8s |
   | A store aisle lined with shelves of plain white supplement bottles | 1 | AI07x1r8s |
   | A rocky hilltop lookout | 2 / 1 | AI58x1r8 / AI58x1r8s |

   `collect` refuses a take that does not open on its first picture; then try the other tile of that prompt.
3. Resubmit once each of the 5 "No audio generated" tiles (Flow Retry or Reuse prompt with the same frames, Veo 3.1 Fast,
   9:16, "Return silent videos" ON): AI57x1r8 twice (front door, parcel), AI51x1r8 (red basket, 2 frames), AI51x2r8
   (black basket, 2 frames), AI07x1r8 (store aisle, 2 frames). Download and collect the results the same way. Prompts and
   frames: `/Users/danrrose/_edit_work/wv03-r8/mirror/round8/motion/veo/job.json`.
4. Push the job folder to the M2: `/Users/danrrose/_edit_work/wv03-r8/tools/push round8/motion` (never use /Volumes on the
   M6; it is a share of the M2 that hangs). Write `round8/motion/COLLECTED` (local, then push) listing every collected ID
   and any tile you could not get, by ID.
5. Do not judge or edit the motion and do not file into the library: the motion lead gates every take, makes the finals
   and files them all into `07 AI Generation Source Archive` (`round8/motion/tools/file_archive.py`, already used for round 7).

Done = every successful generation collected into `round8/motion/veo/` on both Macs, the 5 retries resubmitted and
collected, `COLLECTED` written. Then the motion lead resumes: gate (clipcheck and fresh frame reviewers), finals, MANIFEST,
filing, MOTION_DONE. State on disk: `round8/motion/STATUS.md`.
