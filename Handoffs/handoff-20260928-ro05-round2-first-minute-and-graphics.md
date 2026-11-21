# RO-05 "How I Make My Daily Salad": round 2, first minute + every graphic as a screenshot

**Written 2026-09-28 by Claude (Opus 5.5).** Job RO-05 on `Handoffs/video-editing/00-MASTER.md`. This is ONE round of the round
method (`.claude/skills/_shared/PRE-RENDER-APPROVAL.md`, Dan 2026-09-28). Build the round-2 packet, send it, write the round-3
handoff, stop. **Do not render the full video in this round.**

## 1. Dan's verdict on the Fable recut (2026-09-28, his words)
- Intro: *"that intro is fucking awful... What I want is to have the audio in the beginning, so we'll start off on the camera scene.
  I say, 'What's up, guys? Today I'm going to show you how to make my daily salad.' That's a camera scene. Then we cut to the close-up
  image of the salad, and if we have it, we show an image of me or someone else eating the salad and reacting positively. Keep the
  audio from the camera scene."*
- Graphics: *"change the graphic style to the soft blue lights graphic style... Change all graphics to that."* *"I don't like this
  graphic at 106"* (1:06, the KEY POINT "Break Your Fast LOW CARB, Not With Sugar"); *"I'll edit the text and also the graphic style
  in the individual graphics round... all the graphics need to be redone."*
- Colour: *"this still looks washed out to me. It doesn't look saturated enough... I want it to be a little bit more saturated and the
  colors a little bit more vivid."* (The rejected master measured median luma 0.28, median HSV saturation 0.33.)
- Cut: *"The overall cut of the video, I think, is good."* Process: *"export the first 1 minute. That's what I'm going to be the
  pickiest about... Show me the screenshot of the graphic first, and once I approve the screenshot, we'll render the full video again
  once all assets are approved."*

## 2. Locked (do not change)
- The edit: `/Volumes/Extreme/_edit_work/ro05-fable/edl_full.py` (round-4 state, 15:06) except the opening, which this round rebuilds.
  Its take choices, restored lines, GoPro onion cover and junk fixes stand.
- Audio chain and settings (lav channel 1, `voice_chain.py` fitted EQ in `tools/build.py`, `deesser` 0.25, `--tp -4.0`,
  `--oversample 4`), music bed Pixabay `acoustic_bg.mp3` with `BED_PRE = -10` and `--bed-db -30`. Dan did not criticise the audio.
  Never use `organic_flow.mp3` (it has rap lyrics).
- Framing: top-anchored punches, `framing.json`, flash-hidden joins. Hair rule unchanged.
- Delivered reference file (rejected, for comparison only): `claude edited long form content/08 - How I Make My Daily Salad (Fable recut)/How I Make My Daily Salad | fable | 16x9 | RO-05.mp4`, sha256 starts `a1b3e485`.

## 3. What this round builds (work in `/Volumes/Extreme/_edit_work/ro05-fable/round2/`, never overwrite earlier folders)
**A. Colour options.** Three grades, all more saturated and vivid than the rejected one, on the same 6 source moments (the intro,
arugula, onion, chicken, finished salad, CTA): e.g. median saturation about 0.38 / 0.42 / 0.46 with vibrance weighted to the
vegetables and a natural skin check (the 1.38 chroma gain with skin held at 1.12 is the current recipe in `tools/fitgrade.py` and
`grade/params.json`). Show each option as stills side by side with the current grade and one Muhammad frame, with the numbers.
Recommend one; render the first minute in the recommended grade.

**B. The new opening (first minute).** Camera C1535 from 3.30: "What's up guys? Today I'm gonna be showing you how I make my daily
salad." (words 3.36-7.14). Then, with C1535's audio continuing underneath ("This is how I break my fast nearly every day, and this is
my best and my most important nutrition habit..."), cut to the finished salad close-up (C1550 111.0-113.6 or 115.0-119.5) and then
Dan eating it and reacting well: C1551 from about 2.0 (bite at ~3.9-5.0, smile after). Check C1551 frame by frame for the best
bite-and-smile window; if the reaction is weak, say so and offer the best alternative (no AI generation without Dan's go-ahead).
Then back to Dan on camera for the rest of the intro (C1535 to 38.60 per the current EDL). Remove the old hook (C1550 VO over the
salad) from the top; its "about 700 calories" line may stay where it naturally falls later. Export the first 60 s finished with the
recommended grade and the proposed Soft Blue Light graphics in place: `round2/DRAFT - RO-05 round 2 - first minute.mp4` plus a
540p copy.

**C. Every graphic, as a still screenshot.** Redo ALL on-screen graphics of the whole video in Soft Blue Light
(`.claude/skills/_shared/SOFTBLUE.md`, `GRAPHICS-STANDARDS.md`, `softblue.py`). The current inventory (38 graphics + 8 section title
cards, with times) is printed from `full/timeline.json` and listed in section 5. Map: KEY POINT pills and tips to the Motivation lower
third (`TOPIC` = KEY POINT / TIP / INGREDIENT); ingredient chips to a lower third that carries the calories (the app numbers Dan
confirmed on 09-24); the 4-parts, spices and macro stacks to the 3A left-third card; section titles to a Soft Blue Light full-screen
title scene (propose, Dan decides whether to keep section titles); the AbsByAI.com pills to `scene_cta` or a lower third. Rewrite any
text that only echoes the speech into a distilled key point. For EACH graphic: one `.jpg` rendered on the real graded frame it sits on,
with its ID (G01...), output time range, exact copy, and the speech before, under and after it. Lower thirds blur the picture under
them, so render them on the graded, caption-free base frame (`B.lower_third` on the frame, or `lower_third_patch`). Measure every
screenshot against Dan's face and hair (`tools/gfxcheck.py` pattern, largest person only).

**D. Review page.** Copy the structure of `/Volumes/Extreme/_edit_work/ro01/revision4/index.html` (one section per item: still, ID,
times, exact copy, before/during/after speech, Approve / Changes requested / Remove control that saves a JSON) and
`wv01-edit/round11/index.html` (single lazy player for the first-minute draft). Header states what is locked. Send Dan the page and
the first-minute 540p. Keep the number of choices to 2-3 per question.

Not in this round: moving graphic previews, the B-roll/clip approvals (the 14 previews sent 2026-09-24 were never explicitly approved;
they and the GoPro cover go to round 3 in context), the full render.

## 4. Close the round
Record nothing as approved until Dan replies. Write `Handoffs/handoff-YYYYMMDD-ro05-round3-...md` with: Dan's decisions (verbatim,
per item ID, with the screenshot hashes), what round 3 builds (moving previews of the approved graphics, clip approvals in context,
any regrades), the cost ledger ($0 so far on this recut), the recommended model, the starter prompt. Update the queue
(`python3 scripts/edit-queue/queue.py set RO-05 needs --note ...` then the artifact `write_db`), your board entry, `Handoffs/README.md`.

## 5. Current graphics inventory (rejected style; copy to be rewritten)
0:14 How I Make My Daily Salad / My #1 Nutrition Habit; 0:28 KEY POINT Cheap, Simple, And It Keeps You LEAN; **1:01 KEY POINT Break
Your Fast LOW CARB, Not With Sugar (Dan dislikes)**; 1:44 Salad Bar $20 | Homemade $4; 1:57 stack 4 parts; 2:10 Costco rotisserie
chicken + hard-boiled eggs; 2:45 Store Dressing = Cheap Seed Oils; 2:54 Make Your Own With OLIVE OIL; 3:09 01 Arugula 5 cal; 3:14 Why
Arugula?; 3:27 Start light, then top up the lowest bowl; 3:38 02 Carrots 17; 4:02 03 Tomatoes 8; 4:10 Don't Cut Until The Day You Eat
It; 4:23 04 Broccolini 37; 4:40 Chop the stems now...; 4:53 05 English Cucumber; 5:19 English Cucumber Stays FIRM For 7 Days; 5:49 06
Red Onion 9; 6:40 Glass + A SEALED LID; 6:59 OXO Glass Containers; 8:11 Add The Dressing BEFORE The Toppings; 8:27 stack spices; 8:57
07 Olive Oil 252; 9:03 Measure it: 1 tbsp = 120 calories; 9:53 Rotisserie Chicken: Better, HALF THE PRICE; 9:59 08 Chicken 173; 10:19
09 Eggs 162; 10:44 10 Olives 11; 10:57 11 Pico 6; 11:36 Copy The STRUCTURE; 11:52 Any Greens, Any Cruciferous Veg, Any PROTEIN; 12:17
A premium bottle $30; 13:13 Add Context: The AI Can't See Portions; 13:54 stack 683/39/17/51; 13:59 Weighed by hand: about 720;
14:29 and 14:57 AbsByAI.com. Section titles at 0:41, 1:53, 3:05, 6:28, 7:22, 9:43, 11:32, 12:37. Times shift with the new opening.

## 6. Files
Work dir `/Volumes/Extreme/_edit_work/ro05-fable/` (`tools/build.py`, `edl_full.py`, `grade/`, `framing.json`, `full/timeline.json`,
`notes-RO05-fable.md`, `CODEX_METHOD_STUDY.md`, `full/ROUND-1..4-REVIEW.md`). Skill notes: `.claude/skills/longform-edit/reference/ro05-fable/README.md`.

## 7. Model and starter prompt
Claude Opus 5.5, effort high.

> Read `Handoffs/handoff-20260928-ro05-round2-first-minute-and-graphics.md` in full, then `.claude/skills/_shared/PRE-RENDER-APPROVAL.md`, `.claude/skills/_shared/SOFTBLUE.md` and `.claude/skills/_shared/GRAPHICS-STANDARDS.md`. Run RO-05 round 2 only: three more-saturated grade options, the new on-camera opening with the salad and eating shots under my audio, the first minute exported, and every graphic in the video redone in Soft Blue Light and shown to me as a still screenshot on a review page like Codex's. Do not render the full video. Send me the page and the first-minute review copy, then write the round-3 handoff.
