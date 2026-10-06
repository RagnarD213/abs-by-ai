# Handoff: write the scripts for the 10/17 shoot outlines

**Written 2026-10-06 (Claude, cloud). Recommended: Claude Opus 5.5, High effort. Cloud or local. Run as 4 separate
sessions (batches A to D below), one batch each, so every session keeps a clean context.**

## Goal

Turn every outline Dan approved in **"Content Outlines And Scripts For 10/17 SixPackAbs.com Shoot"**
(`1gt8Fi_wUaNaksa8sAdMoBvcdlBhZLek82EpBr-leq-0`,
https://docs.google.com/document/d/1gt8Fi_wUaNaksa8sAdMoBvcdlBhZLek82EpBr-leq-0/edit) into a word-for-word
teleprompter script, inserted **directly below its own outline** in the same doc. Dan films on 10/17.

Dan already edited the outlines. **His edited outline is the brief.** Lines he wrote are used as he wrote them; his hook
is the opener, verbatim (SKILL.md rule N).

## Read before writing (every batch)

1. `.claude/skills/_shared/WRITING-RULES.md` and the memory entries it lists for Dan's voice, content scripts and shorts.
   Especially `Docs/memory/dan-personal-facts-for-scripts.md` (updated 2026-10-06 with his routine, gear, skin
   routine and the **no bench at home** correction).
2. `.claude/skills/_shared/DAN-VOICE.md` and `_shared/voice/content-longform.md` / `content-shorts.md`.
3. `.claude/skills/_shared/HOOKS.md`.
4. `.claude/skills/scriptfromoutline/SKILL.md` in full: WHAT DAN CHANGED, THE CALORIES PAIR, and THE 10/17 OUTLINES.
   Then `references/dan-edits-2026-10-06-1017-outlines.md` (how Dan edited these exact outlines).
5. Shorts (batch C, D): `.claude/skills/shorts-scripting/SKILL.md` (172 to 185 spoken words, hard 66 second ceiling).
6. In the doc itself: the two **"SCRIPT:"** blocks another session wrote at the top for Dan's own two outlines. That is
   the format to copy. If Dan has edited those scripts by the time you start, diff them against
   `Docs/SCRIPTS_1017_SHOOT_TOP2_*` if a copy exists, or just read his changes, and apply the lessons.

## Format (copy the top two SCRIPT blocks)

- **Filming scripts, not teleprompter scripts (Dan, 2026-10-06).** Every graphic, on-screen text, B-roll, clip and editor
  note goes on its own line in `[ALL CAPS BRACKETS]`; add `[ON SCREEN TEXT: ...]` for each numbered item. Note line
  says "Filming script". Teleprompter copies are a later step. Batch C (`Docs/SCRIPTS_1017_SHOOT_C_AS_DELIVERED_20261006.md`) is the model.
- Bold line `SCRIPT: <outline title>`, then an italic note line (spoken word count, minutes at Dan's pace, which
  bracketed cues are filming notes), then the script as plain paragraphs with a blank line between paragraphs and
  between a filming note and the spoken words.
- **Not bullets.** A paragraph inserted right after a bulleted outline line inherits the bullet: run
  `deleteParagraphBullets` over the inserted range.
- Filming cues in bracketed caps on their own line: `[B-ROLL: ...]`, `[FULL SCREEN GRAPHIC: ...]`, `[PLAY CLIP: ...]`.
- Long-form content: about 1,500 to 2,200 spoken words (the top script is 1,979 words, about 14 minutes). Workouts:
  as long as the timed workout plus intro and cues. Shorts: 172 to 185 spoken words.
- Close every script on: subscribe, and go to SixPackAbs.com to get all my newest videos. No AbsByAI pitch.
- No em dash or en dash (`grep -c` must be 0). Run `python3 scripts/voice/voice_stats.py` on each draft.

## Instructions Dan left inside the outlines (do all of them)

- **What Every Body Fat Percentage Looks Like:** all before pictures on one full-screen graphic (deck chair shot in the
  middle, the two shirt-on photos with his daughter on the sides). Body before/after never on one graphic. One open
  cue, `[DAN: your estimate]% body fat at 200 pounds`: keep it as a `[DAN: ...]` gap, do not invent a number.
- **How Losing Fat Changed My Face:** find a real **Clavicular** clip on face versus body (URL plus mm:ss range), then
  Dan's partial agreement exactly as his outline says. Face before/after may share one graphic; use the touched-up
  photo that shows his jawline best as the after.
- **I Ranked Every Ab Exercise:** his tiers now: bottom = regular crunches and sit-ups; middle = regular planks and
  reverse crunches (his `[DAN: confirm...]` cue is answered by his edit, drop it); top = cable crunches, leg raises,
  decline sit-ups, ab wheel, toe touches, vacuum; #1 = his 3 exercise ab workout. Fix the broken line "and toe
  touches: the 2 I'd pick for your lower abs" (reverse crunches moved out of that tier). Note in chat that the "Only 2
  Exercises You Need For Lower Abs" short still uses reverse crunch plus toe touch; script it as Dan left it.
- **Cortisol Belly:** the fixes are now 6 (he added "quit stressful relationships" and "don't use stress as an excuse
  to overeat"). Change "the 4 things" in the intro and the review graphic to 6. Keep his blunt wording.
- **Reacting To Celebrity Ozempic Transformations:** add one more male example where he marked it (after Sharon
  Osbourne). Best candidate from the 10/06 research: **Fat Joe** (said Ozempic, about 200 lb over years, credits
  low-carb and exercise; Page Six https://pagesix.com/2024/10/15/lifestyle/fat-joe-admits-to-using-ozempic-after-200-pound-weight-loss/;
  clips https://www.youtube.com/watch?v=XkGHIKXLShA (1:02) or Club Shay Shay https://www.youtube.com/watch?v=5GVsLGoT7tM).
  Alternates: Jim Gaffigan (Mounjaro, about 50 lb, verify), Elon Musk (X posts only).
- **I'm 41. These Are The 9 Exercises I Do Every Week:** write it as a scripted studio video with B-roll cut in, and
  put a full B-roll shot list to film after the script.
- **The 5-Minute No-Equipment Workout:** exercise 5 is now toe touches; write its cues and beginner scaling.
- **10-Minute Jump Rope And Kettlebell Workout:** alternate jump rope rounds with kettlebell deadlifts, toe touches and
  push-ups with handles. Rework the timing and rounds to fit.
- **20-Minute Jump Rope And Dumbbell Workout:** alternate jump rope with side laterals, curls, push-ups with handles and
  kettlebell deadlifts. **No bench**, so no bench press, rows or flies on a bench. Fix the equipment line.
- **All home workouts:** no bench. "One hand on a bench or chair" becomes a chair.
- **A Doctor Says Zepbound Eats Your Muscle. He's Wrong.:** Dan sharpened the title; the script takes that side.
- **Why Zepbound Is Actually Free:** keep the aggressive lifetime-cost argument Dan asked for. Every number stays real
  and linked.
- **Deleted by Dan:** "The Only 2 Exercises You Need For A Bigger Chest At Home" (no bench). Do not script it.

## Evidence cues to fill (as you script each outline)

About 23 `[CLAUDE - INSERT EVIDENCE: ...]` / `[CLAUDE - VERIFY AND LINK: ...]` cues remain. Fill each with a real,
verified study: the outcome the viewer cares about as one big plain number, one population note, and the link
(SKILL.md rule L). `pmc.ncbi.nlm.nih.gov` fetches cleanly; pubmed often blocks fetches. Starting points to verify, not
facts: spot reduction (Vispute 2011, 6 weeks of ab training, no belly fat change); sleep and fat loss (Nedeltcheva
2010, 5.5 h vs 8.5 h sleep, 55% less fat lost); stress eating (Epel 2001); sit-up spine load (McGill) and the US Army
dropping sit-ups (2020); coconut water calories (USDA) and hydration (Kalman 2012); jump rope vs jogging METs
(Compendium of Physical Activities); cool bedroom and sleep; gynecomastia prevalence; average US male body fat
(NHANES DXA); face fat and attractiveness (Coetzee 2009); V-shaped torso attractiveness; slow vs fast reps (Burd
2012); NFL broadcast commercial breaks and minutes; which ab exercise hits all 4 ab muscles (EMG studies; Escamilla
2006 ab wheel); why belly and side fat goes last. If a study cannot be verified, say it plainly in the script note and
tell Dan in chat; never invent one.

## Batches (one session each)

- **A. Long-form content (8):** Body Fat Percentages, It's Boring, Cortisol Belly, Love Handles, Man Boobs, Zepbound Even
  If You're Ripped, How Losing Fat Changed My Face, Ab Exercise Ranking.
- **B. Long-form reactions and workouts (7):** Celebrity Ozempic, Bryan Johnson, 9 Exercises, 5-Minute Workout, the 3
  jump rope workouts. Reaction scripts: Dan's take is scripted; the clip is a `[PLAY CLIP: ...]` cue with URL and range.
- **C. Shorts (15):** Lower Abs, V-Taper, Jump Rope vs Treadmill, Coconut Water, 63 Degrees, Fat Without Muscle Loss,
  Zepbound Is Free, Bigger Arms, Kettlebell, 3 Exercises In 5 Minutes, All 4 Ab Muscles, Timer vs Reps, Commercial
  Break, Worst Ab Workouts, The Doctor Is Wrong.
- **D. Clavicular looksmaxxing shorts (not outlined yet).** Dan's decision: **Clavicular clips only** (no other
  creators). One short per tactic, each a real clip (URL plus mm:ss, 10 to 30 s), Dan's take, one action step.
  Disagree: plastic surgery (nose job), bone smashing, testosterone as a teenager, unapproved drugs such as retatrutide
  (not FDA approved as of 2026-10-06; Lilly plans to file Q1 2027). Agree: a GLP-1 for life, a skincare routine,
  skincare supplements (his DIM and B6), a good haircut, threaded eyebrows, a tan, getting lean and ripped, looks
  matter most. Main source: Iced Coffee Hour, https://www.youtube.com/watch?v=PQaMZceY-0I. YouTube captions are
  blocked from the cloud; chapter lists come through the Invidious API at `invidious.f5.si`; a local session is better
  for exact timestamps. Write each as outline plus script together, below a bold `SHORT FORM REACTION OUTLINES:
  CLAVICULAR SERIES` heading at the end of the doc. Add the face versus body clip for batch A if A has not found one.

## Delivery (every batch)

1. Write the batch into a local file first: `Docs/SCRIPTS_1017_SHOOT_<A|B|C|D>_AS_DELIVERED_<date>.md`.
2. Checks: 0 em and en dashes; every Dan fact is on record; every study and clip has a working link; shorts within 172
   to 185 words; Dan's hooks used verbatim.
3. **Re-read the doc right before each write.** Other sessions edit this doc (one added the two top scripts on 10/06);
   never reuse indexes from an earlier read. Use `writeControl.requiredRevisionId`.
4. In the cloud, use `mcp__Google_Docs__update_doc`: insert each script below the last line of its outline, working from
   the bottom of the doc upward so earlier indexes stay valid. Keep each call to about 15,000 characters of text, then
   re-read for fresh indexes. Then bold the SCRIPT line, italicize the note line, and remove bullets from the inserted
   range. Locally, the Chrome paste method in `.claude/skills/ad-outlines/SKILL.md` works too.
5. Re-read the whole doc and confirm: every script sits under its outline, Dan's text is unchanged, no stray bullets.
6. Commit the as-delivered file. Report in chat: the doc link, the scripts added, any cue still open.
7. Last batch to finish: remove this handoff's row from `Handoffs/README.md` and its line from `AI_COORDINATION.md`
   (re-read the board first, run `scripts/board-check.sh`). Victory Dashboard is paused: no dashboard steps.

## Starter prompts

> **A:** Execute batch A of `Handoffs/handoff-20261006-1017-shoot-scripts.md`: write the scripts for the 8 long-form
> content outlines in my 10/17 shoot doc, each directly below its outline.

> **B:** Execute batch B of `Handoffs/handoff-20261006-1017-shoot-scripts.md`: write the scripts for the 2 long-form
> reactions and 5 workouts in my 10/17 shoot doc, each directly below its outline.

> **C:** Execute batch C of `Handoffs/handoff-20261006-1017-shoot-scripts.md`: write the scripts for the 15 shorts in my
> 10/17 shoot doc, each directly below its outline.

> **D:** Execute batch D of `Handoffs/handoff-20261006-1017-shoot-scripts.md`: write the Clavicular looksmaxxing
> reaction shorts (outline plus script each), Clavicular clips only, at the end of my 10/17 shoot doc.

Model for every batch: Claude Opus 5.5, High effort.
