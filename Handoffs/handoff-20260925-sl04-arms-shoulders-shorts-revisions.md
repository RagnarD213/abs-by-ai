# Handoff: SL-04 arms and shoulders shorts, round 2 revisions (2026-09-25)

## Goal
Apply Dan's round-1 notes to the five SL-04 shorts cut from Zeeshan's "Arms & Shoulders Home Workout", re-gate, get an
independent review, and send Dan new review copies. Read `Handoffs/video-editing/00-RULES.md` and
`.claude/skills/_shared/VIDEO-RULES.md` first, then `.claude/skills/shorts/reference/zeeshan-master/README.md` (the
pipeline these shorts were built with and every trap it hit).

## Decisions already made (Dan, 2026-09-24/25; do not reopen)
- Five shorts, content locked except where noted below. Zeeshan's audio stays untouched (cut only, `--verbatim` gate).
- **No cover images in this task.** Dan kept only short 2 cover B
  (`Short-form video content/covers/posted covers/arms-shoulders-short2_do-this-before-you-take-your-shirt-off_cover-B.png`
  and its `youtube/` twin). Codex makes the other covers in a separate task. Do not run `/coverimage`.
- Dan likes all the clips chosen. Only short 1 needs a colour fix: *"Only the first video needs a color correction fix.
  The rest look good."*
- No triceps footage and no photo stand-ins anywhere (Dan 09-24).

## Dan's notes, per short (his words, then the exact fix)

**All five: the top graphic is misaligned with the video edge.** *"The top of our graphic is misaligned with the edge
of the video. I want you to extend that out so it aligns with the edge of the video and it's not inside the video
edge."* Verified on a still (short 4, 20 s): the J2 title band's olive perimeter and white corner brackets are drawn
28 px inside the canvas (`INSET = 28` in `build-assets.py` `tactical_bg()`), while the picture below runs the full 1080
width from y=310. Fix: make the band's frame flush with the video's left and right edges (perimeter and brackets at
x=0 and x=1080, bottom edge meeting the picture top at y=310), so the frame and the video share one edge. Show Dan a
before/after still in the review message.

**Short 1, "Make Your Waist Look Smaller"** (`arms-shoulders-short1_make-your-waist-look-smaller.mp4`)
- Colour: *"the sunlight on me in this clip is very blown out and overbrightened... Reduce the brightness. Increase the
  saturation. Get this up to Muhammad standards."* Grade the picture of short 1 only. Targets from VIDEO-RULES
  (RO-05 rejection): Muhammad's median luma ~0.22-0.28 and median saturation ~0.32-0.39. Measure short 1's shots now,
  build the grade, and prove it on side-by-side stills against Muhammad's frames (Ad 1/Ad 6 masters, BT.709 decode)
  BEFORE the full render. Decode BT.709. Do not touch the audio.
- Hair: *"My hair goes out of the frame a little bit. We have to eliminate this for all videos going forward. If you
  have room on the top, then crop a little bit higher so there's a little bit of extra space above my head."* (Now a
  standing rule in VIDEO-RULES, "Hair never leaves the frame".) Every window currently starts at source row 0.
  Measured: on some of Zeeshan's WIDES his own camera frame cuts the hair (source 2:06 and 3:35 hair touches row 0);
  mediums have 30-60 source px of room. Measure the hair top every 0.25 s on every talking shot of every short. Where
  the delivered hair is within ~20 px of the picture top: if the source has room, place the window so there is a
  little space above his hair; if the source itself cuts the hair, change that stretch's treatment (a different shot
  of the same words, a card, or a trim at a pause) rather than ship it, and if no option exists, show Dan the frame
  and ask, once, in the delivery message. Remove the `framing:hair_top` declaration from each `gate/<S>/declare.json`
  and let the gate measure it.

**Short 2, "Do This Before You Take Your Shirt Off"** (`arms-shoulders-short2_do-this-before-you-take-your-shirt-off.mp4`)
- Top graphic alignment (above). Colour: leave as is.
- The graphic at ~3 s: Zeeshan's pill "Great Exercise Before A Photo Shoot" (card F-s01, source 103.6-106.6) becomes
  **"Use this 2-minute workout to pump up before a photo shoot"**, centred. Zeeshan's own pill must not appear (whole or
  sliced): crop the card above his pill band (source rows 804-907) or cover it, and draw the new pill in his style
  (rebuilt from his frames: olive fill (76,87,48), white type, his font size and padding measured off the frame),
  horizontally centred on the canvas, on the same beat.

**Short 3, "Raise Your Elbows, Not Your Hands"** (`arms-shoulders-short3_raise-your-elbows-not-your-hands.mp4`)
- Context first: *"it's not even obvious what exercise we're talking about. Find a clip where I'm saying 'side
  laterals'... to establish a context to put first."* Recommended (checked): source **245.5-248.1**, "Common mistakes I
  see with the side laterals" (CTC words 245.83-247.80, measured silence 247.80-248.48), then the existing piece from
  264.22 ("When they go to the top, they don't get their elbows high..."). Reads as one sentence. Verify the 245-248
  picture for Zeeshan's graphics and his whip transition just before (~243.9-244.5, must not show) and pick the
  window/card by the same rules. Alternative if that fails: 208.5-211.28 "Alright, let's talk about the next exercise,
  the side laterals" (not used by any other short). Never reuse 213.15-238.10 (short 1).
- Top graphic alignment.

**Short 4, "Stop Swinging Your Curls"**: top graphic alignment only.

**Short 5, "How To Do Bicep Curls"**: top graphic alignment, and *"In the beginning of the video, in the first few
seconds, my hair goes out of frame. Recrop that."* Shot H-s00 (source 125.2-142.35, zoom window 2.04x): the source
frame there cuts the hair (measured). Apply the hair rule above: a treatment where his hair is not cut.

## Current state
- Build folder (Extreme SSD): `/Volumes/Extreme/_edit_work/sl04/build/` with `segments.js` (pieces), `plan_shots.py`
  (every window and reason), `render.js`, `build-assets.py`, `captions.js`, `overlays.json`, `build.sh <IDS>`
  (plan -> assets -> render), `deliver_all.sh` / `deliver.sh` (copy, audio gate, delivered ASR + CTC, gate plan),
  `make_plan.py`, `work/ctc_source.py` (caption timing), `gate/<S>/` (plan, declare.json, negative scan, watch, logs).
  IDs: A = short1, F = short2, C = short3, K = short4, H = short5. Git copy of the scripts:
  `.claude/skills/shorts/reference/zeeshan-master/`.
- All five currently pass `gate.py --format short` (GATE 2.3.0) with fresh-subagent watch judges; each re-render
  changes the sha, so every changed short needs a new watch pass, judge and gate.
- Note: `work/words_aligned.json` was improved after shorts 2, 4 and 5 were rendered (measured-silence and squeezed-word
  corrections), so re-rendering them will shift a few captions slightly. That is expected; re-check captions:sync.
- Delivered files, stamps and `arms-shoulders REVIEW/` (540p review copies) are in `Short-form video content/`;
  the sheet is `Short-form video content/arms-shoulders-SHORTS.md` (update in/out and lengths for short 3).
- Edit queue: SL-04 set back to `ready` with a note pointing here. Board: HANDOFFS line in `AI_COORDINATION.md`.

## Steps
1. Claim: `python3 scripts/edit-queue/queue.py set SL-04 in_progress --by Claude` (+ Artifact write_db per
   `.claude/skills/_shared/edit-queue/README.md`); replace the HANDOFFS line with one ACTIVE entry.
2. Build-assets fix (flush frame) once; short 1 grade stills vs Muhammad; hair measurements on all five; short 3
   segment change; short 2 pill.
3. `./build.sh A F C K H`, then `./deliver_all.sh`, negative-events JSON (1 s spacing), `make_plan.py`, `watch.py`,
   a fresh reviewer subagent per the /shorts skill (Opus 5.5 per memory `reviews-on-opus-5-5`), `watch.py --judge`,
   `gate.py --format short`. Fix and repeat until every short passes and the reviewer says SHIPS.
4. New 540p review copies; `queue.py set SL-04 delivered`; commit scripts/docs (never media) and push.
5. Message Dan: what changed per short in plain words, then numbered action items at the bottom, then the five review
   copies sent LAST (memory `action-items-at-bottom`).

## Risks
- The hair rule can conflict with Zeeshan's own framing on wides; do not silently declare it away.
- Cards that end on Zeeshan's pills: his fades outlast any colour scan by 0.5-0.8 s; check rendered frames.
- Two builds max on the machine (`ps` check before rendering).
