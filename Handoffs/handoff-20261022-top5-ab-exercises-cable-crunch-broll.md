# Top 5 Ab Exercises SFC R4: swap in Dan's own cable crunch B-roll (DS-01)

**CONTENT (SFC), dedicated Short. READY 2026-10-26: cable crunch footage (B0574, B0582, B0583) and Muhammad's HQ V4 are both in.**
Recommended: Claude Opus 5.5, high effort (our in-house re-edit, started on Claude).

## Goal
Dan accepted Muhammad's Top 5 Ab Exercises V4 on 2026-10-22, but the one stranger in it, the stock cable crunch clip,
gets replaced on our side with real footage of Dan doing cable crunches. One clip swap, nothing else changes.

## Decisions already made (do not reopen)
- Muhammad's V4 is approved as is. Everything outside the cable crunch span stays frame-identical: his cut, his audio
  mix (memory `editor-audio-untouched`), his captions and our graphics.
- Dan wants this done in-house, not sent back to Muhammad.
- Accepted leftovers, do not fix: the "hold the five pound plate" line (0:41.8 - 0:43.6) shows bodyweight toe touches;
  the closing tight shot is about 15-20% closer than the wide.

## Inputs
- **Base cut (HQ ARRIVED 2026-10-26):** `Short-form video content/Top 5 Ab Exercises - DS-01/Top 5 Ab Exercises | muhammad | 9x16 | V4 HD.mp4` (same path on Extreme; Drive `1pqSpRjOyBgnVu769CU1CZLEnRqFj5HOn`). Light check vs V4: `revision docs/shorts-revisions-muhammad-10-26-26.summary.md`. Build on it.
- Earlier instruction, kept for reference: prefer Muhammad's HQ export of Top 5 V4 (asked for on 2026-10-22; check his Upwork messages and Drive
  owners `sharkimageryproduction@` / `wadeededitteam@`). If it has not arrived, build on the V4 review copy
  (Drive `1XPDgy1IzwHfSS-d1myAbRutwKW0T4k4O`, local `/Volumes/Extreme/_edit_work/revisions-20261022/muhammad/dl/ds01_v4.mp4`,
  1080x1920, 29.97 fps, 1,575 frames, 52.55 s, 3.3 Mbps) and keep the splice as a script so it re-runs on the HQ export
  in minutes. Light-check the HQ against V4 first (same frame count; frame difference = re-encode noise).
- **New B-roll:** Dan's cable crunch footage filmed 2026-10-23. Find the newest shoot folder (nightly copy routine:
  Extreme, Seagate, Drive). If the roll has his spoken take announcements, boost and transcribe it
  (`/revisions` lesson 75) and use only a take he calls good. Cable crunch done right: kneeling, rope by the head,
  hips still, crunch the ribs toward the pelvis.
- **Our graphic for that span:** `/Volumes/Extreme/_edit_work/revisions-20261013/muhammad/kit/03_ds01_top5/mov/g04_0m18_9s_section.mov`
  ("EXERCISE 3 OF 5: The Cable Crunch", transparent 1080x1920, already timed from 0:18.9).

## The span to replace
Cuts measured on V4 (`revisions/reference/cuts.py`): the stock clip runs from the cut at **0:18.79 (frame 563)** to the cut at
**0:25.99 (frame 779)**, between the spiderman plank and the V-sit twist. Words under it:
"Number three, the cable crunch. If you have a gym, this is the one. Safe for beginners and you can load it heavy enough
to wreck an advanced lifter." (0:18.9 - 0:26.0).

## Build
1. `editcap.py acquire DS-01 --title "Top 5 Ab Exercises" --type SFC` before any render (`_shared/VIDEO-RULES.md`, "Active edit cap"). Heavy steps through the render queue.
2. Lay Dan's clip out exactly like Muhammad's other exercise clips in this video: full width, full height of the footage,
   sides cropped in on Dan as far as the whole rep allows, blurred copy of the clip filling above and below. Match the
   band position and blur of the spiderman plank and V-sit clips (measure them on V4 frames). Grade it to match the
   8/28 pool clips around it (lesson 59 numbers; "All B-roll is colour corrected").
3. Put a clean rep under "the cable crunch" and keep reps moving through the whole span; accelerate or trim to fit.
   Hard cuts in and out at 18.79 and 25.99, like V4.
4. Composite `g04_0m18_9s_section.mov` on top at 100%, unmoved.
5. **Captions:** V4's word captions are burned in, so the span needs them rebuilt in Muhammad's style. Measure his font,
   size, weight, shadow and position on V4 frames on either side of the span and match them word for word to the
   words above (word timing from Whisper on the base cut's audio). Compare side by side with V4 at 0:18.5 and 0:26.5.
6. Audio: copy Muhammad's track untouched (stream copy or sample-identical).
7. Prove the rest is unchanged: subtract every frame outside 18.79 - 25.99 from the base cut (re-encode noise only).
   Run the delivery gate, the hair-top/framing read on the new clip, and the picture-beat line for the span
   (Dan's footage is real moving footage: no label).
8. Review page with the full Short and a watch range 0:17 - 0:28, then stop for Dan
   (`editcap.py release DS-01 --review`). Edit queue: `delivered`.

## After Dan approves
- Edit queue `finalized`, release the edit slot, file the master as `Short-form video content/ds-01_top-5-ab-exercises.mp4`
  (plus Extreme and Drive copies).
- Setup is a separate `/video-setup` task (five Codex covers, Dan's pick, Blotato). The Shorts calendar has
  Top 5 Ab Exercises on Thu Dec 31, 2026 (`Docs/SHORTS_RELEASE_CALENDAR.md`).

## Current state (2026-10-22)
Review of V4: `revision docs/shorts-revisions-muhammad-10-22-26.summary.md`. Edit queue DS-01 = `blocked` until the B-roll
exists. Nothing built yet.

## Starter prompt
> Read `Handoffs/handoff-20261022-top5-ab-exercises-cable-crunch-broll.md` and execute it. Top 5 Ab Exercises SFC R4: replace the stock cable crunch clip (0:18.79 - 0:25.99) in Muhammad's approved V4 with my cable crunch B-roll from today's shoot, matching his layout, captions and our graphic, everything else untouched. Review page, then stop for me.


## October 23 library dependency resolved (2026-10-25)

Dan finalized the exercise identities and Color C. The checked full-quality cable-crunch assets below are registered in the shared library and have verified copies on Extreme, Expansion and Drive. Use the final Color C editing masters, then fit them to the approved film as already required. The source range map and checked clip hashes are in `Media/footage-index/shoot-20261023/permanent-library-map.json`. Original recordings remain on Expansion.

- **B0574**: checked native editing master. Resolve its path/link and exact source range through the private shared catalog.
- **B0582**: checked native editing master. Resolve its path/link and exact source range through the private shared catalog.
- **B0583**: checked native editing master. Resolve its path/link and exact source range through the private shared catalog.

The longer side-angle second take is the first candidate for the 7.2-second replacement. Inspect its complete motion and keep the rope near the head, ribs curling toward the pelvis and hips steady. The short frontal close-ups provide alternatives. Teaching intent remains unknown where the source did not establish it; these are identified cable-crunch assets, not a blanket endorsement of every rep. The stock-footage dependency is resolved. The existing film revision has not been executed by this footage-preparation task. No editing chat was started.
