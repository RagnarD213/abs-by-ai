CONTENT | SL-06 | Top 5 Zepbound Tips SFC R2

> **2026-10-13, Dan: pickups are recorded on the studio set at the shoot, not on the desk mic.** After hearing the desk-mic pickups in the RO-20 first minutes: "that audio doesn't work... I'm just going to record these pickups on my studio set instead... get all of the pickups that we need for this task and every other outstanding video edit". This job's pickup lines are on the shoot list (`Docs/PICKUPS_1017_SHOOT.md`, the PICKUPS section of the shoot doc, and the pickups teleprompter document). Do not ask him to read them into the desk mic again; build the pickup shorts when the shoot roll is uploaded. Desk takes are timing placeholders only.

> **2026-10-13, Dan to this task: "I'm going to record these pickups in the lavalier mic on Thursday."** (Thursday is
> 2026-10-15.) This handoff now PULLS the five pickups from that recording. It does not record anything and does not ask
> Dan to read into the desk mic. **Do not fire it until both exist: his reply to the round-1 page, and the uploaded pickup recording.**

# SL-06 round 2: apply Dan's round-1 notes, build all six Zepbound shorts, gate, audit, deliver

Written 2026-10-12 by Claude (Opus 5.5) at the end of round 1. Updated 2026-10-13 for the lav pickups. Round 1 built short D against
desk-mic placeholder pickups and put every title, crop, clip, graphic and key point of all six on one review page. Dan
reviews that page and records the pickups on the lav (Thursday 10-15); then this task pulls them in and builds.

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
5. `Docs/PICKUPS_1017_SHOOT.md`: the pickup list he reads from (SL-06 is items 5 to 9) and how the shoot pickups are handled.

## State at the end of round 1 (2026-10-12)

- Review page: http://127.0.0.1:8817/ (folder `/Volumes/Extreme/_edit_work/sl06/round1/`, managed service on port 8817).
- Short D built: `Videos to Review/Top 5 Zepbound Tips SFC R1 - short D - Inject On Thursday Evening.mp4` (50.45 s). Its
  opening pickup is a desk-mic placeholder (below) and gets replaced by the lav take; picture, captions and film sound stand. The audio gate passed it
  (the gate cannot see the dropouts). Not yet through `gate.py --format short`, the watch pass or a reviewer.
- Work folder `/Volumes/Extreme/_edit_work/sl06/`: `plans.py` (all six as data), `build/<S>/` (audio, words, cues, shots,
  track, bars), `clips/` (copies of every stock and library clip used), `pickups/` (recording, takes, treated wavs,
  reports), `aiframes/` (C and E start and end frames + REPORT.md), `round1/` (page, stills, items).
- Lengths: A 46.2 s, B 53.7 s, C 54.1 s, D 50.5 s, E 57.3 s, F 54.7 s. E has under 3 s of room.

### Pickups: pulled from Dan's lav recording of Thursday 2026-10-15

The desk-mic takes in `pickups/` (10-12, `raw_take2.wav`) are TIMING PLACEHOLDERS ONLY. They carry recorder dropouts (the
old ffmpeg capture lost 11.7 % of the audio) and Dan has ruled that desk-mic pickups do not match the films anyway. Nothing
from them ships. They did their job: every short's opening picture, captions and timing were built against them.

**The lines** (`Docs/PICKUPS_1017_SHOOT.md`, items 5 to 9; each is read twice on the recording):

| | Line | Follows into (film line) |
|---|---|---|
| A | Here's why you should start Zepbound at 1 milligram to avoid the side effects. | "And for most of you watching this channel, you should be taking less than the standard 2.5 milligram minimum dose." |
| B | Here's why you should stop using the pen to inject Zepbound, and why you should use a needle instead. (his own longer wording; the default) AND the short version: Here's why you should stop using the pen to inject Zepbound. | "There are two ways to inject Zepbound..." |
| C | Here's how to inject Zepbound with a needle, step by step. | "This takes about 10 seconds once you know what you are doing." |
| D | Here's why Thursday evening is the best time to inject Zepbound. | "The medication is strongest in the first few days after your shot..." |
| E | Here's how to come off Zepbound without gaining the fat back. | "Coming off is where I see people destroy everything they built." |

**How to pull them (first step of the task):**

1. **Find the recording.** Dan uploads it himself. Use the path or Drive link he gives in the starter prompt. If he gives
   none, look for a new shoot or pickups folder on `/Volumes/Extreme/` dated 10-15 or later, then `Docs/SHOOT_1017_DOCS.md`
   and the board. If it is not there, stop and tell him in one line; do not fall back to the desk takes and do not record.
   The same recording also holds the RO-20 and SL-07 pickups: read it, never move, rename or re-encode it.
2. **Get the lav as a WAV.** `.claude/skills/_shared/audio/pick_lav.py <clip>` decides which track or channel is the
   clip-on mic (never hard-code a channel), then pull that track to `/Volumes/Extreme/_edit_work/sl06/pickups/lav_take.wav`
   (mono, 48 kHz, 16-bit) with the pull filter it writes. Check the pull: its length equals the clip's audio length, and it
   is not silent. Build the roll sidecar if there is none (`_shared/rolls/roll_sidecar.py build`).
3. **Find SL-06's lines.** `pickup.py asr pickups/lav_take.wav` prints every sentence with times. The five lines above
   are each there twice (B four times: long, long, short, short, or whatever he actually read). Read the whole transcript
   first: on 10-12 he reworded B while recording, so use the words he said and update `plans.PICKUP` and `plans.TEXT` to match.
4. **Pick the take.** His last clean take of each line (take-selection rule): whole first consonant, whole tail, no peak
   at 0 dBFS, pace like the film line that follows. Measure each take's exact start and end on the envelope, not on
   Whisper's times (the 10-12 script in `softblue-sl06/README.md` does this). For B use the wording his round-1 reply
   names; if he names none, the long one.
5. **Match it to the film.** The lav on the studio set should already be close to the film's voice (same kind of mic and
   room as roll C1706), so expect a small correction. `pickup.py fit pickups/lav_take.wav '<all ten or so SL-06 take spans>' _lav`
   fits the tone toward the film's finished voice; then `pickup.py make <S> pickups/lav_take.wav T0 T1 _lav` for A, B, C, D, E
   (level matched to the next film line, the film's `bed.wav` under it on the film's clock, 15 ms de-click). No dereverb,
   no noise reduction, no gate. If the fit asks for more than about 3 dB in any band, the take is not sitting like the film:
   say so on the round-2 page with the numbers, do not push harder.
6. **Prove the join.** For each of the five: speech level of the pickup against the next film sentence (within 0.5 dB),
   tone error against the film (`<S>.report.json`), room (EDT) against the film's 67 ms, and a Whisper pass of the rendered
   file. Put a 6 second "pickup into film" clip per short on the round-2 page so Dan judges every join by ear.
7. **Rebuild.** Every head changes length, so for A, B, C, D and E: `batch.py audio, words, plan, gfx, proof, render`
   (delete each `hf/manifest.json` first; the A, B, C, E ones were only time-shifted for the round-1 stills). F has no pickup.

Desk-take record, for wording and timing only: A 3.4 s, B 4.5 s (long wording), C 2.7 s, D 3.2 s, E 2.4 s.

## Dan's decisions on the page (7). Apply his reply exactly.

1. Pickups: recorded on the lav 2026-10-15 and pulled as above. His only choice here is B's wording, long (default) or short.
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
2. Pull the five pickups from the lav recording (section above), then apply Dan's notes in `plans.py`.
3. `batch.py audio, words, plan` for all six, then `batch.py gfx A B C D E` (delete their `hf/manifest.json` first: every
   pickup head changes length). F's bar is current unless a note touches it.
4. `batch.py proof S`, look at every sheet, then `batch.py render S` for all six (about 4 minutes each; two builds at
   most on the machine). D is re-rendered too: its opening is the placeholder.
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
- The lav take is the only source: if a line is missing, clipped or misread on the recording, say which one and ask Dan; never patch it from the desk takes.
- A shoot clip can carry the lav on one channel and the camera mic on the other. `pick_lav.py` per file, and check the pulled WAV before fitting it.
- A caption can hang 0.3 s into the next shot at a clip cut (D 0:20.7). Trim the cue to the cut if the reviewer flags it.
- The audio gate cannot declare a head span: the reference includes the pickup. Report the pickup numbers from
  `pickups/<S>.report.json` in the notes.
- B0458 (Dan's curls, F 0:13) and B0030 (ab wheel) are his real footage: no "real picture" chip on moving footage.
- The board is at its word limit; keep the entry to one line.

## Starter prompt

> Name this task "Top 5 Zepbound Tips SFC R2". This is CONTENT. Read `Handoffs/handoff-20261012-sl06-round2-build-after-dan-review.md` and execute it: pull my five pickup lines from the lav recording I made on Thursday (do not record anything, do not use the desk-mic takes), apply my round-1 notes below, build the six Zepbound shorts with /shorts in Soft Blue Light, run the gates and an independent audit, and give me the round-2 review page. No covers, no upload. Pickups recording: [path or Drive link]. My notes: [paste the reply box from http://127.0.0.1:8817/]
