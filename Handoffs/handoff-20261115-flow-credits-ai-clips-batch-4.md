# Handoff: Flow credits, AI clips batch 4 (2026-11-15)

**Owner:** Claude, Opus 5.5 high. Flow work by background `flow-veo` agents; reviewers `frame-reviewer` (fresh one per pair and per take).
**Authorization:** Dan, 2026-11-07 (parent handoff), 2026-11-13 and 2026-11-15 ("give me the handoff for the next batch"). Do every step
without asking; stop only for Dan's picks (frame pages, video pages) and anything that would cost money. Never pay, top up or buy credits.
Never Veo Quality unless Dan asks for it by name.
**Deadline and budget:** spend by **Nov 28** (Ultra 20x drops to 5x on Nov 29). This work has used **1,060 of its 14,000 credits**; balance
was 20,312 on 2026-11-14. Read the balance before and after each run and add a line to `Media/flow-credit-log.md` (the M2's copy is the
master; copy it to the M6 after each line). Veo 3.1 Fast = 10 a take, Omni 1.1 Flash = 10, Nano Banana Pro images = 0. Flow shows
"Leaving Dec 5" on Veo 3.1 Fast and Omni 1.1 Flash; Omni 1.2 Flash is listed but untested here.
**Receipt to keep current:** `Docs/FLOW_CREDITS_CLIPS_RECEIPT_20261128.md` (finish it by Nov 28). Parent rules:
`Handoffs/handoff-20261107-flow-credits-ai-clips-for-next-edits.md`. Previous batch (worked example of everything below):
`Handoffs/handoff-20261113-flow-credits-ai-clips-batch-2-3.md`.

## Current batch4 status (Codex, 2026-11-15)

Video reviews complete; **40 checked cuts across16clips await Dan at http://127.0.0.1:9260/**. Three Cans reviews preserved. Do not restart ideas/frames/motion reviews. Filing actual video selections remains, authorized in this same chat. Exact next commands: `Handoffs/handoff-20261115-flow-clips-batch4-motion-reviews.md`. Credits:490 measured versus540expected,19,822 observed balance; discrepancy50 unreconciled. Receipt updated.

## Done so far (do not redo)

25 clips approved and filed, A0247 to A0271 (tags `flow-credits-batch1`, `-batch2`, `-batch3`), each listed under "Pre-made AI clips" in
its job doc: DS-97, DS-100, DS-102, DS-103, DS-50, DS-95, DS-99, DS-104, DS-94, DS-98, DS-51, DS-46, DS-96. Existing clips reused:
A0159 (DS-95), A0241 and A0188 (DS-51).

## Batch 4: which videos

Check `Handoffs/video-editing/00-MASTER.md` first: take only jobs still READY that nobody has claimed, and read each job doc for clips it
already has. Candidates as of 2026-11-15:

- **New 11/13 green-screen shoot** (job docs name their rolls; transcripts in `Media/footage-index/11-13-dan-rose-fitness-shoot-green-screen/`
  where indexed, otherwise ask the job doc's roll map): long-forms I'm 41. If I Were 25 Again, This Is Exactly How I'd Get In Shape (RO-40),
  I Ranked 15 "Healthy" Foods From Actually Healthy To Basically Candy (RO-41), Why Bulking Is a Scam (RO-42), 7 Fitness Rules That Are
  Completely Made Up (RO-43), I Crashed My Tesla Because I Didn't Trust FSD (RO-39); Shorts The Best Protein Snack Costs $2 And Comes In A
  Can (DS-106), Your Metabolism Is Not The Reason You're Fat (DS-107). Long-forms take more clips each (the green-screen standard opens on
  an AI hook): read `.claude/skills/longform-edit/reference/longform-greenscreen-standard/README.md` for what an AI clip is used for there.
  Skip DS-108 and DS-109 (in review / in progress with Codex) and the Great Again T ads (RA-22 to RA-35) unless Dan asks.
- **Left over from batch 3** (no idea passed or none selected): Why I Train With A Timer Instead Of Counting Reps (DS-57), 3 Rules For
  Every Rep (DS-64), The Only 2 Exercises You Need For A Wide Back (DS-101), The Only 2 Kettlebell Exercises You Need (DS-54), How To Do
  Goblet Squats (DS-62), How To Do Reverse Lunges (DS-60). How-to demos use REAL footage (rule 2026-11-13); AI clips only for opinion and
  "why" lines. Dan passed on B3-16 (kettlebell "for sale") and B3-17 (goblet "crown jewel"): do not offer those again.
- Search `clip_library.py find` (single keywords work best) before every idea and offer existing clips first.

Aim for 20 to 30 ideas. Budget guide: an idea that reaches video costs about 30 credits (2 Veo Fast + 1 Omni); a redo round about 50.

## Routine (same as batches 1 to 3)

1. Ideas: `.claude/skills/ai-clip-ideas/SKILL.md` (read lessons 6, 7 and 8). Copy `b3r/ideas.py` or the M2's `b3/ideas.py` for the prompt,
   END-lock and spec format.
2. Frames: Codex (`_shared/codex-image.sh --model gpt-6.1-sol --effort high`) and Google (Nano Banana Pro in Flow, a `flow-veo` agent with a
   brief like `b3r/GOOGLE-BRIEF.md`) START and END for every idea, each END drawn from its own START. Screen every pair yourself on a sheet,
   then `gate.py START END --spec`, then one fresh `frame-reviewer` per pair you would use (brief: `b3r/REVIEWER-BRIEF.md`). A pair whose END
   fails twice is dropped.
3. Frames page: phone first, **Select** buttons (untouched = out), blind X1/X2 where both sources passed, existing library clips offered in
   their own section. Builder to copy: `vid-b3r/build_frames2.py` or the M2's `b3/build_page.py`. Dan picks; `blind.py pick <set> --chose Xn`.
4. Video: `veo.py add` each picked pair (Veo Fast x2 at 8 s + Omni x1 at 6 s; plan Omni windows inside the first 5 s, it redraws at
   frame 128), one `flow-veo` agent with a brief like `vid-b3d/FLOW-VIDEO-BRIEF.md`, screen on 1 fps and 2 fps strips (`vid-b3d/strips.sh`),
   `clipcheck.py` through `renderq.py run`, one fresh motion reviewer per kept take (`MOTION-REVIEWER-BRIEF.md` in
   `/Volumes/Extreme/_edit_work/FLOWCLIPS/vid-b3d/`), cut to the reviewer's WINDOW, video page (`vid-b3d/build_review.py`), Dan picks.
5. File: `clip_library.py add <window cut> --kind ai --status usable-unused --used-in "<job> <title> (planned)" --tags flow-credits-batch4`,
   `clip_library.py sheet`, IDs under "Pre-made AI clips" in each job doc (script to copy: the M2's `vid-b3d/file_library.py`).

## Two Macs: how this actually ran (2026-11-14)

- The session runs on the **M6** (Dan's Mac, user `danrrose`); the Extreme, the clip-library catalog and the earlier work folders are on
  the **M2** (`ssh m2`, user `danielrose`). Work folders: M6 `~/Projects/_edit_work/FLOWCLIPS/{vid-b3r,vid-b3d}/`, M2
  `~/Projects/_edit_work/FLOWCLIPS/{b1,b2,b3,vid-b1,vid-b2,vid-b3}/`.
- **Put frames, specs, takes and reviews on `/Volumes/Extreme/_edit_work/FLOWCLIPS/<folder>/`**: that path is identical on both Macs (the M6
  mounts the M2's drive), and gate stamps store absolute paths. Stamps made under `~/...` on one Mac do not verify on the other.
- The M6 render line is usually full. Run `gate.py`, `clipcheck.py` and `--verify` on the M2 over ssh (`renderq.py run --group FLOWCLIPS
  --light -- ...`); tell reviewers to record with the same command over `ssh m2` if the local one waits more than a minute.
- **Flow runs in the M2's Chrome**: the only connected browser, deviceId `989f4486-c847-4c4e-a30b-8a4dcf0ee3bc` (its list name changes;
  select by id). Downloads land in the M2's `~/Downloads`: `scp` them back, then collect. `veo.py collect` cannot find ffprobe on the M6:
  prefix `PATH="<repo>/Media/video_edit/bin:$PATH"`.
- Library adds run on the M2 (`ssh m2`, catalog `Media/clip-library/catalog.json` is there). Copy the window cuts over first.
- Review pages: `review_server.py PORT DIR` on the M6 (free port: `editroute.py free-port --from 9250`); test at 375, 800 and 1150 px in
  silent check mode, then hand off. Never `python -m http.server` (a hook blocks it).
- Pushes: `safe-push.sh` has been stopping on other sessions' live files; commits are kept locally. Retry at the end of each phase.

## Dan's taste (read before writing ideas)

Memory `ai-clip-gags-injury-and-sense`, `review-pages-select-not-kill`, skill lesson 8. From batches 2 and 3:
- He likes options: where two versions are both good he keeps both ("give the editors options").
- He rejects anything unrealistic about training: a machine that is not running, a beginner standing frozen, weights that look
  "ridiculously light", a slow controlled lowering in a cheat rep, any rocking in a "strict" rep. Think like a trainer watching it.
- Exercise-form clips: stage "strict" or "does not move" against a wall, pad or bench from the first frame pair; shoot a lean from the side;
  count plates in both frames; use the START frame only when the motion must come back down.
- Approved so far: mirror self-check, bathrobe at the gym, caution tape, paramedics by a deadlift, injury-count sign, bench press in a
  museum, jiu-jitsu jog, waking up sweating, arm in a cast at the gym window, phone on the bench, hospital bed (played straight), straddle
  stretch, thermostat on 63, bored on the stair climber, nervous first day, only five machines, skinny arm on the scale, eggs in a popcorn
  bucket, wall of sit-up tally marks, cheat curl versus strict curl.
- Rejected or not selected: map, plan card, dusty gym bag, bouncer, recliner, hospital curls, ski goggles in bed, penguin, stairmaster
  concert, the tortoise, coffee curl, tiny plate, three dumbbells, kettlebell for sale, goblet crown jewel.

## Starter prompt

> Execute `Handoffs/handoff-20261115-flow-credits-ai-clips-batch-4.md` end to end: batch 4 of the Flow-credits AI clips, for the new 11/13
> shoot's long-forms and Shorts plus the Shorts batch 3 left without clips. Ideas, blind Codex and Google frame pairs, my picks, video, my
> picks, then file what I approve in the clip library. Spend the Google Flow credits by Nov 28.
