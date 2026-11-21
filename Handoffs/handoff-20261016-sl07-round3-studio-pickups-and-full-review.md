CONTENT | SL-07 | If I Had Belly Fat SFC R3

# SL-07 round 3: put the studio pickups in, add the extra B-roll, give Dan one review of all five shorts

Written 2026-10-16 by Claude (Opus 5.5). Supersedes `handoff-20261013-sl07-round2-dan-review.md` (kept for history, the
file map and the round 2 lessons; read its "Where things are" section).

**Recommended: Claude Opus 5.5, high effort.** Four re-renders, pickup treatment, four fresh reviews, five gates.

## Dan's decision, 2026-10-16

Dan did **not** review round 2: "without the pickups, I don't have context. I'll review all the other changes once you
integrate the pickups in the next round." So round 3 delivers all five shorts, complete, with the studio pickups in,
and the round 3 page carries every open question from round 2 as well (they were never answered). Do not stop mid-round
to ask him anything; build everything below, then put the questions on the page.

## 1. The studio pickups (recorded 10-15, roll C1722)

- Roll: `/Volumes/Extreme/10:15 dan rose fitness shoot - green screen, outdoor shorts, outdoor b roll, studio backdrop/C1722.MP4`
  (green screen set, not the studio set; same lav as the films). Audio is the **lav on the LEFT channel only**; the right
  channel is empty (peak -78 dBFS). Use `pan=mono|c0=c0`. Memory `shoot-1015-format`; roll notes `C1722.roll.md`.
- Takes (roll seconds, from the roll transcript; both lines word for word as scripted):

| Take | Line | Roll time | Peak | Speech RMS | Floor |
|---|---|---|---|---|---|
| B1 | "Here's how to know if your fat loss plan is working." | 281.50 to 283.54 | -3.7 dB | -23.8 | -59.8 |
| **B2** | same, retake | **284.60 to 286.72** | -5.3 | -25.1 | -54.4 |
| D1 | "Here's why you should work out every single morning." | 288.42 to 290.62 | -6.6 | -24.6 | -58.0 |
| **D2** | same, retake | **291.94 to 294.24** | -6.1 | -24.9 | -54.6 |

  No clipping on any take (0 samples over -0.5 dBFS). **Use B2 and D2** (memory `take-selection-rule-approved`: the last
  clean take). Raw mono cuts with 0.4 s handles are already saved: `pickups/studio1015/{B1,B2,D1,D2}_raw.wav`;
  measurements in `pickups/studio1015/takes.json`. Check each word with `pickup.py asr` before using it.
- Treatment: the film's own voice chain, not the desk fit. The RO-16 chain is recorded in
  `/Volumes/Extreme/_edit_work/ro16/round3/RO16_MASTER.mp4.voice_chain.json` (`eq` string; dereverb null). Apply that
  `eq` to the raw lav take, then do what `pickup.py make` does after its EQ step (cut on silence with a short pad, level
  matched to the film line that follows, true-peak cap at the film's peak, 8 ms fade in, 15 ms de-click). `make` today
  applies the desk-mic fitted EQ (`fit_B.json`/`fit_D.json`): add a flag or a small variant that uses the film chain
  instead, and do not reuse the desk fit. No dereverb, no gate, no noise reduction (memory `audio-never-over-strip`).
- Write `pickups/B.wav` and `pickups/D.wav` (stereo, dual mono, same lead and tail as `make` writes). Keep the desk
  versions as `pickups/desk/B.wav`, `pickups/desk/D.wav` before overwriting.
- Remove `placeholder=True` from both entries in `plans.PICKUP`. That drops the on-screen PLACEHOLDER AUDIO tag and the
  "PLACEHOLDER PICKUP" file-name suffix by itself (`deliver.dname`). Delete the two old PLACEHOLDER-named files in
  `Short-form video content/` and `Videos to Review/` once the new ones are delivered.
- Picture under the pickup stays B-roll (B: the overhead scale clip; D: the jump rope), so the green screen never shows.
  Confirm on the frame scan.
- Check the join: run the blind listener (`listen/gemini_listen.py`, film-only and film-join controls, as in round 2) on
  both. Report the result on the page. The green screen room is not the studio room, so report what the listener and
  the room measures say (EDT against the film's 64 ms) instead of chasing it; Dan judges by ear.

## 2. The extra B-roll (the gate's `style:coverage` row)

Staged in `round3-plan/coverage.json` with film times, crops and the line each clip plays under; stills already on the
round 2 page (`r2/review/cov/`). Dan has not seen them. **Build them in** (they are needed to pass the gate) and list
them on the round 3 page as "my call, swap any of them":

- "Stop Trying To Lose 1 Pound A Week" (10% now): overhead scale `p6719385` at film 53.10 to 56.55; Dan's jump rope
  `B0448` (BRIGHT) at 63.40 to 67.75; Dan's curls `B0031` (BRIGHT) at 97.38 to 101.45. About 33% after.
- "The 3-Pound Rule" (21% now): salad into containers `B0019` (`clips/B0019.mp4`, fx 0.62) at 674.42 to 677.94; Dan's ab
  wheel `B0030` as a span card at 682.50 to 685.46 (the ending). About 37% after.
- "Work Out Every Morning" (29%): lengthen the stairs cover (`A0159`) end from 308.45 to about 309.75 if the clip is long
  enough, else extend another clip about 1.3 s.
- Recount every short's share from `build/<S>/shots.json` before rendering (clips, scenes and phones count; key-point bars
  over Dan do not). Each must be at least 33%.

## 3. Everything else stays as built in round 2 (Dan reviews it all in round 3)

- The four reworded key points stay; the page shows old and new wording.
- **The "working out on vacation" clip is NOT made**: its frames (`aiframes/D3_start.jpg`, `D3_end.jpg`) were never
  approved, and motion needs approved frames. The ab wheel stays in that slot. Put the two frames on the round 3 page
  again with the same context; if Dan says yes, it is a small round 4 (`gen_motion.py D3 D3_v1 4 pair`, about $0.60,
  three AI sense questions, replace the `abwheel` cover at 321.70 to 325.73, re-review D).
- "Track Your Calories With A Photo" is finished (review SHIP, gate PASS 39 of 39). Do not re-render it. Its one open
  question goes on the page: the "Today's total" line at 0:37 to 0:40.

## 4. Build, check, deliver

1. `batch.py audio|words|plan|gfx|proof|render` for B and D (the pickup length changes, so everything after it shifts),
   and for A and E (new covers). Two builds at most on the machine; other sessions render too.
2. Proof sheet and frame-by-frame cut scan on each (`scan.py`).
3. `deliver.py copy` then `deliver.py plan` for A, B, D, E. The plan now supplies the banned-screen source, both label
   templates and a truthful judge line; it was never run for B and D with those, so check `plan.json` for both.
4. `watch.py` with `--out` and `--log` per short; a **fresh `ra-reviewer` per short** (A, B, D, E), each with its own
   scratch folder and not shown any notes; fold each verdict with `watch.py --judge`; `deliver.py plan` again.
5. `./rungate.sh S` for A, B, D, E (never a bare gate command; never change a bound). F already has its stamp.
6. Round 3 review page: copy `page_r2.py`/`notes_r2.py` to `page_r3.py`/`notes_r3.py`, new folder `r3/review/`, serve
   on port 8874 again (`review_server.py 8874 <dir>` re-stages the cached copy). Dan has not seen round 2, so the page
   presents each short whole, plus a short "what changed since round 1" list per short with timestamps (later-round
   rule). Sections: the five shorts, the pickups (how they were treated, listener result), the extra B-roll, the
   vacation frames, the reworded key points, the F question, checks, one reply box. VLC copies in `Videos to Review/`
   named `If I Had Belly Fat SFC R3 - <title>.mp4`.
7. `queue.py set SL-07 in_progress --note ...`, mirror to the Edit Queue artifact, `queue.py mark-synced SL-07`; update
   the board entry; push `softblue-sl07/` changes. No covers, no upload.

## Open risks

- The green screen room may still be heard at the join. If the listener picks it out, say so on the page; do not spend a
  round matching it (Dan's 10-13 rule applies to desk recordings; for a lav take, Dan decides by ear).
- Gate runs take 6 to 30 minutes when other sessions render, and two waiting gates block each other until a render ends.
- `B0019` came from the library's staged copy; register any new use in the clip library (`clip_library.py add`) after.

## Starter prompt

> Name this task "If I Had Belly Fat SFC R3". This is CONTENT. Read `Handoffs/handoff-20261016-sl07-round3-studio-pickups-and-full-review.md` and execute it: put my studio pickups from roll C1722 into "Weigh Yourself Every Morning" and "Work Out Every Morning", add the extra B-roll from `round3-plan/coverage.json`, re-render what changed, then run the watch judge, a fresh independent review and the delivery gate on every changed short, and give me one round 3 review page of all five shorts. Use the Codex subscription for any new images. No covers, no upload.
