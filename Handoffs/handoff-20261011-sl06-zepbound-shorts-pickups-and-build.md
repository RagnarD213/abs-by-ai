CONTENT | SL-06 | Top 5 Zepbound Tips SFC R1

> **2026-10-16: round 1 is done and its recording steps are history.** The pickups were recorded on the shoot lav (roll
> C1722) and are chosen and matched. The next step is `handoff-20261012-sl06-round2-build-after-dan-review.md`; this file stays
> the spec for the segment picks and Dan's words.

# SL-06: record Dan's pickups, then build six Zepbound shorts (round 1)

Written 2026-10-11 by Claude (Opus 5.5) at the end of the segment-selection session. Dan picked the segments and changed
four of them. Nothing is cut yet. This task records his pickup lines, shows him the round-1 review page, and builds the batch.

**Recommended: Claude Opus 5.5, high effort.** (Shorts from a long-form are a Claude secondary cut; the build will be watched.)

## Goal

Six vertical Shorts (1080x1920) from the RO-12 "Top 5 Zepbound Tips" long-form, each one point, each opening like a
dedicated video. Deliver review copies to Dan. No covers, no upload, no queue. The parent goes public Sun Oct 25 2026;
no short posts before it is verified public.

## Read first

1. `Handoffs/video-editing/00-RULES.md` and `.claude/skills/_shared/VIDEO-RULES.md` in full. New since this job was
   written: "A Short opens like a dedicated video: record a pickup, never Number two" (2026-10-11, top of the file),
   "All B-roll is colour corrected before it goes in a video" (2026-10-11), "The first 5 seconds get the most effort"
   (10-08), "Round 1 always reviews every graphic, stock item and clip" (10-08), "Review videos also go in Videos to
   Review/" (10-08), the funny-AI-clip rule (10-10).
2. `.claude/skills/shorts/SKILL.md`, then `.claude/skills/shorts/reference/softblue-sl03/README.md` (the batch renderer
   for a Soft Blue shorts batch from our own long-form; start from it, in a new work folder `/Volumes/Extreme/_edit_work/sl06/`).
3. `Short-form video content/zepbound-tips-SHORTS.md` (the batch record: pieces, word-for-word text, decisions).

## Source

- Master: `claude edited long form content/09 - Top 5 Zepbound Tips/Top 5 Zepbound Tips | claude | 16x9 | RO-12.mp4`
  (9:11.42, sha256 `7f6766c5e1d82881fb2a56b9b7414f6baa0bbe49f027828e507991d9f7cae67b`). `.srt` and chapters beside it.
- Build files: `/Volumes/Extreme/_edit_work/ro12/out/` (`timeline.json` = blocks, items, shots; `mapped-words.json` =
  film-time words; `voice_raw.wav` = dry voice for silence snapping; `bed.wav` = the music bed on the same clock;
  `FINAL.mp4` = the master). Recipe: `recipe-RO12/` in the delivery folder. Raw roll: 9/23 shoot, C1706 only, one
  dual-mono lav. Crops and lut: `notes-RO12.md` (W2 `3552:1998:144:162`, T2 `2608:1466:616:184`, `grade-C.cube`).
- Cut from the RAW roll through the film's timeline with its luts, as SL-03 did. The film's `BASE.mp4` has graphics baked in.
- Do not run anything inside `/Volumes/Extreme/_edit_work/ro12/`. Copy what you need.

## The six shorts (Dan's picks, 2026-10-11)

Film times, measured on `mapped-words.json`. Snap every cut to measured silence on `voice_raw.wav`; ear-check each
piece opening in context (SL-03 round 2 lesson). A piece that ends on one of the film's own audio joins may only run
straight on (SL-03 round 3 lesson). `/` marks a join that needs a size step or a clip.

| | Title (working) | Opens with | Film pieces | Length |
|---|---|---|---|---|
| A | Start At 1 mg, Not 2.5 | film line (Dan's pick) | 1:00.5 - 1:07.1 / 1:20.7 - 1:30.6 / 1:31.0 - 1:48.1, 1:48.1 - 1:56.5 | 42 s |
| B | Use A Needle And Vial, Not The Pen | **pickup B** | 0:40.7 - 0:48.9 / 0:54.9 - 0:59.9 / 1:07.7 - 1:11.8 / 1:57.1 - 2:06.7 / 2:21.0 - 2:41.9 | 48 s + pickup |
| C | How To Inject In 10 Seconds | **pickup C** | 2:44.8 - 3:35.9 | 51 s + pickup |
| D | Inject On Thursday Evening | **pickup D** | 4:18.2 - 5:05.1 | 47 s + pickup |
| E | How To Come Off Without Regaining It | **pickup E** | 5:41.1 - 5:50.7 / 6:02.4 - 6:47.0 | 54 s + pickup |
| F | How Much Protein You Need On Zepbound | film line | 6:50.8 - 7:44.9 | 54 s |

G (the "still soft" warning) is cut. Dan: "make all of them except for G."

What Dan changed, in his words:
- **A:** "I want to start with 'And for most of you watching this channel, you should be taking less.' Cut that content in
  the beginning about the quick pen and auto injector. If there is more content about taking a 1 mg or 1.5 mg dose after
  that, then include that... It's a little confusing to have two points in a video like that." So A is the dose only. The
  1.5 mg maintenance lines (1:48.1 - 1:56.5) are added. Drop the leading "And" only if the cut is clean. The line "That is
  less than half of what the pen would give you" stays (it is about the size of the dose); cut it if it reads as pen talk
  on the page.
- **B:** "move that content from the beginning of A into B, and then cut some other content to make room for that." B is
  now pen versus needle only. In: the two ways to inject, the problem with the pen, the vial and needle line, "less
  painful than the pen... You control the needle", the syringe-reading passage. Out to make room: "The pen exists because
  the manufacturer assumes...", "And I want to be practical here...", the ice cube.
- **C:** "Avoid starting the video on number 2." Pickup replaces "Number two, how to actually inject."
- **D:** "change that to a sentence that will make the short seem like dedicated content, like 'Here's why you should
  inject Zepbound every Thursday evening' or 'Here's why Thursday evening is the best time to inject Zepbound.'" The
  pickup replaces "Number three, inject Thursday evening. This one is free and almost no one thinks about it." (the second
  sentence points at a list too).
- **E:** "Give me the pickup for the first line." The pickup goes first; the film's "Coming off is where I see people
  destroy everything they built" follows it.
- **F:** "Good as is."

Word-for-word text of every piece: `Short-form video content/zepbound-tips-SHORTS.md`.

## The pickups

Drafted through `dan-voice-writer` (two clean calls, wording unchanged). Dan records option 1 of each unless he
prefers an alternate; he was sent all of these on 10-11. Each is said in about 3 to 4 seconds.

| | Record this (option 1) | Alternates | The film line that follows |
|---|---|---|---|
| B | **Here's why you should stop using the pen to inject Zepbound.** | 2. Here's the best way to inject Zepbound if you want to control your dose. 3. If you're injecting Zepbound with the pen, you're doing it the hard way. | "There are two ways to inject Zepbound, by filling a needle from a vial or with a KwikPen or auto-injector." |
| C | **Here's how to inject Zepbound with a needle, step by step.** | 2. Here's how to inject Zepbound with a needle so it's nearly painless. 3. Here's how to give yourself a Zepbound injection the right way. | "This takes about 10 seconds once you know what you are doing." |
| D | **Here's why Thursday evening is the best time to inject Zepbound.** (Dan's own line) | 2. Most diets fail on the weekend, so inject Zepbound every Thursday evening. 3. Inject Zepbound on Thursday evening if your diet always falls apart on the weekend. | "The medication is strongest in the first few days after your shot and it fades towards the end of the week." |
| E | **Here's how to come off Zepbound without gaining the fat back.** | 2. Don't just quit Zepbound cold when you hit your goal weight. 3. If you're going to stop taking Zepbound, here's the right way to do it. | "Coming off is where I see people destroy everything they built." |

A and F have no pickup: Dan chose A's opening line himself and approved F as is. If A's "And for most of you watching
this channel..." reads as mid-thought once it is cut, offer him one pickup for it on the review page; do not add one unasked.

### Recording them (first thing in the task, while Dan is at the desk)

Dan wants to record "right into Claude". His desk mic is the Yeti: ffmpeg audio device `[0] Yeti Stereo Microphone`
(`Media/video_edit/bin/ffmpeg -f avfoundation -list_devices true -i ""` to confirm the index).

1. Show Dan the four lines in chat. Tell him: when you say go, read each line two or three times with a breath between
   takes, B then C then D then E, at the pace and energy of the film.
2. (Corrected 2026-10-12: do NOT use the ffmpeg command below. It silently dropped 11.7 % of the audio. Record with
   `~/.cache/absbyai/rec_mic OUT_DIR 120 30`; see `handoff-20261012-sl06-round2-build-after-dan-review.md`.)
   Record one take of about 90 seconds in the background:
   `Media/video_edit/bin/ffmpeg -f avfoundation -i ":0" -t 90 -ac 1 -ar 48000 /Volumes/Extreme/_edit_work/sl06/pickups/raw_take1.wav`
   If macOS refuses the mic, do not fight it: ask Dan to record a Voice Memo or QuickTime audio file and drop it in the chat.
3. Transcribe with word times, split on silence, pick the best take of each line (clean first consonant, no clipped
   tail, pace matching the film line that follows). Play nothing back to Dan as a question; choose.
4. Treat each pickup so the join is not heard: `voice_chain.py` fitted toward the FILM's voice on this roll (not the
   default reference), loudness matched to the film line that follows it, the film's `bed.wav` under it at the level the
   mix has there, a 15 ms de-click at the join. Never dereverb to chase a number (memory `audio-never-over-strip`).
5. The film's approved mix after the join is cut only, as in SL-03 (`audio_gate.py --verbatim` against `his_mix.wav`).
   The pickup seconds are new audio, so the verbatim row needs the pickup span declared, not waved through. Read the
   gate's plan keys first; if the gate has no way to declare a head span, report that to Dan with the measured numbers
   and do not change a bound.
6. Each pickup is fully covered by picture (below) and gets captions like any other line.

## Opening picture and covers (first 5 seconds)

| | 0:00 to about 0:04 | Why |
|---|---|---|
| A | Library clip **B0329** (already vertical: gloved hand sets out a syringe and glass vials) under his first line, then Dan | no pickup here; he is on camera, so the clip is a cover of choice, about 3 s |
| B | The film's 2:02 clip (hand holding a vial with the syringe in it, `stock/px6824226.mp4`), full screen, under the pickup | names the thing he is talking about. It appears again in the film at 1:59; use a different clip there in this short |
| C | **New AI clip, frames first:** a seated man in shorts brings a small insulin syringe to the outer front of his thigh, midway down. No pinch (three pinch generations landed on the kneecap in RO-12). Fallback: the Soft Blue title treatment over B0352 (finger on a syringe plunger) | nothing in the library shows a thigh injection; every stock injection shows a pen in the belly |
| D | The film's 5:09 clip (a hand circling a date on a calendar in red marker, `stock/px9057559.mp4`) under the pickup | "Thursday evening"; that clip sits outside this short's range |
| E | Library **B0376** (feet step onto a bathroom scale) under the pickup, then Dan on "Coming off is where..." | the short is about the scale deciding the dose. Use a different scale shot at "letting the scale tell you when to stop" |
| F | The film's 7:34 clip (sliced chicken on a board) for about 2.5 s under his first line, then Dan, then the AI split screen (A0058) at "a catastrophic amount of muscle" | his opening line is a plain statement; the food is the stronger picture |

Also offer, as frames only: one funny AI clip for E's last line ("Walk down the stairs instead of jumping off the roof"):
a man in gym clothes at the edge of a low garage roof about to hop off, then the same man walking down the stairs.
Fallback is the film's staircase clip. This follows the 10-10 rule for lines with no literal picture.

Check every clip against the no-belly-framing rule, colour correct all B-roll to the film's look (10-11 rule), and never
repeat a stock clip inside one short. Search the clip library again before anything new.

## Standing decisions for this batch (already told to Dan; he did not overrule them)

- Look: the Soft Blue shorts standard he approved on SL-03 (title band y 0 to 310 for the whole short, two steady
  windows, two-line HyperFrames key-point bar, captions under it, B-roll filling the picture area). No look round.
- The film's graphics are rebuilt for vertical, never sliced: the 1 mg, 2 mg, 2.5 mg ramp (A), the five-step injection
  list as the bottom card (C), the seven-day strength chart (D), the taper list as the bottom card (E), the phone
  beside Dan for the meal-photo demo (F). Title case; full caps only where a word truly carries the punch (10-09 rule).
- "Not medical advice. Talk to your doctor." small on screen in every short.
- AI clips keep AI-GENERATED chips, off faces and bodies: A0137 nausea clip in A (1:42), A0058 split screen in F
  (6:55). Those two shorts get `ai_generated: true` at setup, as does any short that takes a new AI clip.
- Generation budget: $5 per short, frames through Codex (`_shared/codex-image.sh`), motion only after Dan approves frames.
- Four parked shorts from the on-hold "My Honest Zepbound Update" cover the same topics (`zep-short2`, `3`, `4`, `6`).
  These new ones are the ones that post; the parked files are not touched.
- Posting order to suggest at setup: D, A, F, C, B, E. A and B at least a week apart.

## Open question to put on the review page (one line, not a blocker)

The title band: "GLP-1" (the standing default for on-screen graphics on organic videos) or "Zepbound"? Dan was asked
on 10-10 and did not answer. Build the title stills both ways for D and let him pick once for the batch. Captions spell
Zepbound either way.

## Order of work

1. Rename the task "Top 5 Zepbound Tips SFC R1". Claim: `python3 scripts/edit-queue/queue.py set SL-06 in_progress --by Claude`,
   mirror to the queue page (`.claude/skills/_shared/edit-queue/README.md`), update the one-line board entry.
2. Record the pickups (above) while Dan is there.
3. Round-1 review page (`_shared/PRE-RENDER-APPROVAL.md` layout, `review_server.py`, a port no other review uses):
   the first short finished (do D first: one continuous passage plus a pickup, so it proves the pickup join), the AI
   frame pairs, "What I decided", then every title, bar, card and clip of all six as stills on real frames, three per
   row. Copy the finished short to `Videos to Review/` as `Top 5 Zepbound Tips SFC R1 - short D - <title>.mp4`.
4. After his notes: build the other five, run `_shared/deliver/gate.py --format short` and the watch pass on each
   delivered file, then a fresh `ra-reviewer` audit that is not shown your notes. Expect "does not ship" once.
5. Deliver: `Short-form video content/zepbound-tips-short<N>_<title>.mp4` + stamps, REVIEW 540p copies, the audio A/B
   clip, `notes-*.md`, `recipe-*/`, and update `zepbound-tips-SHORTS.md`. `queue.py set SL-06 delivered`. List the six
   shorts that need covers (a separate task). Register any new clip in the clip library once approved.

## Risks

- C's last word ("fast", 3:35.9) sits 0.26 s before a film audio join. If its tail is clipped, end C on "If you bled, or
  if it actually hurt, you messed it up." (3:30.0).
- B has four internal joins on one locked camera. Each needs a real size step (about 1.25x displayed face change) or a
  clip; two same-size joins in a row need a cutaway (SL-03 lessons).
- The Yeti in the office will not sound like the lav in the studio. If the fitted pickup still reads as a different
  room next to the film line, say so on the review page and let Dan hear it; a re-record with the lav is his call.
- The subtitle reads "Again, Monday through Thursday" at 4:32 in D. Listen; it may be a mis-hearing. Caption what he says.
- Two builds at most on the machine. Check before every render.

## Starter prompt

> Name this task "Top 5 Zepbound Tips SFC R1". This is CONTENT. Read `Handoffs/handoff-20261011-sl06-zepbound-shorts-pickups-and-build.md` and execute it: record my four pickup lines into the Yeti first, then show me the round-1 review page with short D finished and every graphic and clip as stills, then build the six Zepbound shorts with /shorts in Soft Blue Light, gates and an independent audit. No covers, no upload.
