CONTENT | SL-06 | Top 5 Zepbound Tips SFC R2

# SL-06 round 2: apply Dan's round-1 notes, build all six Zepbound shorts, gate, audit, deliver

Written 2026-10-12 by Claude (Opus 5.5) at the end of round 1. Round 1 recorded Dan's pickups, finished short D and put
every title, crop, clip, graphic and key point of all six on one review page. Dan reviews that page, then this task builds.

**Recommended: Claude Opus 5.5, high effort.** (Shorts from a long-form are a Claude secondary cut; five renders, gates and an audit.)

## Goal

Six vertical Shorts (1080x1920) from RO-12 "Top 5 Zepbound Tips", delivered as review copies with gate stamps and an
independent audit. No covers, no upload, no queue. The parent goes public Sun Oct 25 2026.

## Read first

1. `.claude/skills/_shared/VIDEO-RULES.md` and `Handoffs/video-editing/00-RULES.md` in full.
2. `.claude/skills/shorts/SKILL.md`, then `.claude/skills/shorts/reference/softblue-sl06/README.md` (this batch's tooling
   and what round 1 learned), then `../softblue-sl03/README.md` for the gate plumbing (`deliver.py`, `rungate.sh`, `declare.json`).
3. `Handoffs/handoff-20261011-sl06-zepbound-shorts-pickups-and-build.md`: Dan's picks and his words. Still the spec.
4. Dan's reply to the round-1 page (he pastes it into the task). If he has not replied, ask for it; do not build on guesses.

## State at the end of round 1 (2026-10-12)

- Review page: http://127.0.0.1:8817/ (folder `/Volumes/Extreme/_edit_work/sl06/round1/`, managed service on port 8817).
- Short D finished: `Videos to Review/Top 5 Zepbound Tips SFC R1 - short D - Inject On Thursday Evening.mp4` (50.45 s, audio
  gate PASS verbatim, stamp beside it). Not yet through `gate.py --format short`, the watch pass or a reviewer.
- Work folder `/Volumes/Extreme/_edit_work/sl06/`: `plans.py` (all six as data), `build/<S>/` (audio, words, cues, shots,
  track, bars), `clips/` (copies of every stock and library clip used), `pickups/` (recording, takes, treated wavs,
  reports), `aiframes/` (C and E start and end frames + REPORT.md), `round1/` (page, stills, items).
- Lengths: A 46.2 s, B 53.7 s, C 54.1 s, D 50.5 s, E 57.3 s, F 54.7 s. E has under 3 s of room.

### Pickups (recorded 2026-10-12 on the Yeti, `pickups/raw_take2.wav`)

| | Line as recorded | Take used (s in the recording) | Mic distance | Notes |
|---|---|---|---|---|
| A | Here's why you should start Zepbound at 1 milligram to avoid the side effects. | 85.77 - 88.89 | close | Dan chose to record it; A opens on it over B0329 |
| B | Here's why you should stop using the pen to inject Zepbound, and why you should use a needle instead. | 29.19 - 33.39 | far | his own rewrite while recording; the only take of this wording |
| C | Here's how to inject Zepbound with a needle, step by step. | 38.59 - 41.06 | far | take 2 of 2 |
| D | Here's why Thursday evening is the best time to inject Zepbound. | 56.36 - 59.31 | close | take 4 of 4; take 3 clipped |
| E | Here's how to come off Zepbound without gaining the fat back. | 74.10 - 76.22 | close | take 3 of 3 |

Treatment (`pickup.py`): EQ fitted toward the film's voice per mic distance (tone error 0.7 dB mean far, 1.0 dB close), level
matched to the next film line (within 0.2 dB), the film's `bed.wav` under it at -26.8 dB, 15 ms de-click. No dereverb, no
noise reduction. Room: film 67 ms; pickups 59 to 80 ms, B reads 101 ms on its single take (far, +17 dB of gain). If Dan
picks "re-record on the lav", the five lines go on the next shoot list and the shorts wait; tell him that plainly.

## Dan's decisions on the page (7). Apply his reply exactly.

1. Pickup sound: use these takes, or re-record on the lav.
2. Title band: ZEPBOUND TIPS (built) or GLP-1 TIPS. For GLP-1 change `plans.TITLE` eyebrows and F's headline to
   "How Much Protein / You Need On A GLP-1".
3. Title copy for all six.
4. Steps in C and E: one step at a time in the bar (built, recommended) or the film's list card (does not fit: captions
   land on his mouth; if he still wants it, split the card in two and show him stills before rendering).
5. AI clip for C's opening: frames `aiframes/C_start.jpg`, `C_end.jpg`. On approval generate motion (9:16, about 4 s),
   prompt must say "fingers stay off the leg, no pinch". Fallback built: B0352 lifted (`plunger`).
6. AI gag for E's last line: frames `aiframes/E_start.jpg`, `E_end.jpg`, as TWO clips with a hard cut (he is drawn larger
   in the end frame). Fallback built: px9154824 (`stairs`).
7. Key-point copy: every bar is in the reply box.

Generation budget: $5 for this video in total, $0 spent. Motion method and checks: `.claude/skills/longform-edit/reference/ro06/README.md`
(`gen_motion.py`). Judge AI clips at playback speed; AI-GENERATED chip on, off faces and bodies; C and E then get
`ai_generated: true` at setup (A and F already do).

## Order of work

1. Rename the task "Top 5 Zepbound Tips SFC R2". Queue stays `in_progress`. Update the one-line board entry.
2. Apply Dan's notes in `plans.py`. Re-run `batch.py audio, words, plan` for every short whose pieces, pickup or covers changed.
3. Re-render bars: `batch.py gfx A B C E` (their `hf/manifest.json` were only time-shifted for the stills after the real
   pickups changed each head; delete those manifests first). D and F bars are current.
4. `batch.py proof S`, look at every sheet, then `batch.py render S` for A, B, C, E, F (about 4 minutes each; two builds at
   most on the machine). Re-render D only if a note touches it.
5. Write `deliver.py` for this batch from `softblue-sl03/deliver.py`: delivery copy to
   `Short-form video content/zepbound-tips-<plans.NAME>.mp4`, `audio_gate.py --reference-mix his_mix.wav --verbatim --ab`,
   REVIEW 540p, Whisper of the delivered file against the captions, gate `plan.json` (declare every join and size step),
   then `_shared/deliver/watch.py`, the judge, and `gate.py --format short`. Report any row that measures Dan's approved
   layout through `declare.json` with his words; never raise a bound.
6. A fresh `ra-reviewer` on the six delivered files, not shown your notes. Expect "does not ship" once; fix and re-run.
7. Deliver: round-2 page on a new port and folder (`round2/`), each finished short also in `Videos to Review/`, the audio
   A/B clips, `notes-SL06.md`, `recipe-SL06/`, update `Short-form video content/zepbound-tips-SHORTS.md`, and
   `queue.py set SL-06 delivered` with the artifact mirror. List the six shorts that need covers (a separate task).
   Posting order to suggest at setup: D, A, F, C, B, E; A and B at least a week apart; each config needs a `pinned_comment`.
8. When Dan finalizes: register new clips in the clip library, delete this video's copies from `Videos to Review/`, remove
   the 8817 and round-2 page services, delete the board entry.

## Open risks the reviewer will look at

- Every same-camera join is a full to mid step (1.2x on screen). SL-03 reviewers wanted about 1.25x or a cutaway. B has two
  adjacent talk joins (0:13 and 0:48), C has seven in-take steps, E has six. If a join reads as a jump, cover it with a clip.
- C has two clips only (the opener and the needle close-up at 0:24): `style:coverage` may fail. Add a steady cutaway, do not tune.
- C ends 40 ms before the film's own audio join at 216.12; the last word is whole on the envelope. Listen on the render.
- B's and C's pickups are the far-mic takes. If the join is heard there and not on D, say so and offer the re-record.
- A caption can hang 0.3 s into the next shot at a clip cut (D 0:20.7). Trim the cue to the cut if the reviewer flags it.
- The audio gate cannot declare a head span: the reference includes the pickup. Report the pickup numbers from
  `pickups/<S>.report.json` in the notes.
- B0458 (Dan's curls, F 0:13) and B0030 (ab wheel) are his real footage: no "real picture" chip on moving footage.
- The board is at its word limit; keep the entry to one line.

## Starter prompt

> Name this task "Top 5 Zepbound Tips SFC R2". This is CONTENT. Read `Handoffs/handoff-20261012-sl06-round2-build-after-dan-review.md` and execute it: apply my round-1 notes below, build the six Zepbound shorts with /shorts in Soft Blue Light, run the gates and an independent audit, and give me the round-2 review page. No covers, no upload. My notes: [paste the reply box from http://127.0.0.1:8817/]
