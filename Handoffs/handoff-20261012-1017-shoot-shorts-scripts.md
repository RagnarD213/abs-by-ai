# Handoff: script the 26 locked shorts for the 10/17 shoot, and update the Reaction Clips document

**SFC (short-form content). Written 2026-10-12 by Claude, at Dan's request. Not started.**

## Goal

Dan locked 26 new dedicated shorts for the 10/17 SixPackAbs.com shoot on 2026-10-12: 15 green screen reactions and 11
outdoor shirtless shorts. They exist only as outlines on a review page. This task turns every one into a filming
script in the shoot doc, adds the 15 clips to his Reaction Clips document so he has them cued up on his computer on
shoot day, adds the new B-roll shots to the B-roll list, and rebuilds the teleprompter documents.

## Another handoff touches the same documents: do that one first

`Handoffs/handoff-20261012-1017-reaction-kills.md` (written the same day by another task) removes the reaction clips
and shorts Dan killed from the shoot doc, then rebuilds Teleprompter 2 and the Reaction Clips document with the
survivors. Check `AI_COORDINATION.md` and the shoot doc before starting:

- **If it has not been run,** run it first in this task, or confirm with Dan that it runs first. Do its shoot doc
  edits, then add the new scripts, and do the teleprompter rebuild, the PromptSmart import and the Reaction Clips
  document ONCE at the end, for both.
- **If it has been run,** the Reaction Clips document already holds only survivors: add the 15 new clips to it, and
  do not put back anything that was removed.
- Either way, the finished Reaction Clips document holds: the surviving old clips, plus these 15.
- Two shorts it removes were the format examples for reaction shorts ("A Doctor Says Zepbound Eats Your Muscle" and
  "Reacting To The Worst Ab Workouts On Instagram"). Dan called both "too boring". Do not model the new scripts'
  content on them.

**Update 2026-10-12: it has been run.** The shoot doc, Teleprompter 2 (8 scripts), the Reaction Clips document
(survivors only, exact times) and the B-roll list are cut down. The Bryan Johnson video is out too. One thing is still
open from it: the Retatrutide short has no clip until Dan picks one. State and ids: `Docs/SHOOT_1017_DOCS.md`,
"Dan's clip kills, done 2026-10-12".

## Read first

1. `Docs/shoot-1017-shorts-ideas/ideas.json`: **the source of truth.** Every locked short: title, verdict, video id,
   start and end seconds (`segs`), first and last words, Dan's reaction bullets, B-roll, and the notes. The same
   content with working players: http://127.0.0.1:8881/ (if it is not answering:
   `python3 .claude/skills/_shared/review_server.py 8881 Docs/shoot-1017-shorts-ideas`).
2. `Docs/SHOOT_1017_DOCS.md`: the ids of the shoot doc, the three teleprompter documents, the B-roll list and the
   Reaction Clips document.
3. `.claude/skills/shorts-scripting/SKILL.md`, `.claude/skills/_shared/WRITING-RULES.md`,
   `.claude/skills/_shared/HOOKS.md`, `.claude/skills/_shared/DAN-VOICE.md`. The words are drafted by the
   `dan-voice-writer` agent from a content plan, never in the main session.
4. In the shoot doc, read two finished examples before writing: "Clavicular Says Looks Matter More Than
   Personality. He's Right." (a reaction short Dan kept; the format is outline bullets, then `SCRIPT:` with a
   `[PLAY CLIP: ...]` cue) and "The Only 2 Exercises You Need For Bigger Arms" (the workout short format with
   `[B-ROLL: ...]` cues).
5. `.claude/skills/teleprompterscripts/SKILL.md`, sections "v3" and "Reaction clip list".
6. Memory: `reaction-videos-clips-first` (Dan has watched all 15 of these clips: that rule is met), `filming-scripts-first`, `personal-facts-only-when-relevant`, `dan-personal-facts-for-scripts`,
   `shorts-open-with-pickup`, `organic-drug-names-allowed`, `reaction-clip-criteria`.

## Decisions already made (do not reopen)

- The 26 shorts and their clips are Dan's picks. Build exactly these. Do not swap a clip or a person.
- Every script is a FILMING script: graphics, on-screen text, B-roll and the clip cue as their own ALL CAPS bracketed
  lines. Three hooks per script, the best one in the script and two as HOOK TAKES under it.
- Hard ceiling 66 seconds including the clip. A reaction script's spoken words shrink as the clip grows: with a 15
  second clip about 135 to 150 words, with a 24 second clip about 110. `/shorts-scripting` owns the exact spec.
- The clip cue uses the exact seconds from `ideas.json`:
  `[PLAY CLIP: creator, "video title", URL, m:ss to m:ss]`. A multi-piece clip lists every piece in order.
- Organic close: "Subscribe, and go to SixPackAbs.com for all my newest videos." Never "tap the button".
- No gym B-roll on this shoot (Dan). Outdoor shorts use pool and home shots only.
- Three locked shorts are about looking at yourself, so each teaches one thing: Maher's "don't weigh me" card
  teaches the daily weigh-in, Maher on fat shaming teaches the shirtless mirror, Bert Kreischer teaches the weekly
  shirtless photo.
- Dr. Mike's clip comes from a video that also recommends testosterone and growth hormone. Leave both out.
- No compliance, legal or reputation commentary on any clip or person (`AGENTS.md`).

## Ask Dan once, at the start, then keep working

Send these as one numbered message and draft everything that does not depend on the answers while you wait. Where
he does not answer, use the default.

1. **Ronaldo belt clip:** he said "start it at 5 seconds rather than 15 seconds". Default: starts at 0:05, ends
   0:15. The other reading is a 5 second clip, 0:00 to 0:05.
2. **Kevin James, cheat days:** Dan's own rule on cheat days or cheat meals is not on record. Default lesson: no
   cheat days; fit a treat inside that day's calories.
3. **Hormozi, the stopping point:** the card's "the day you're 3 pounds over, you cut back" is Claude's wording.
   Ask for his real number. With no answer, leave a marked gap `[DAN: your number]`, do not invent one.
4. **Outdoor "Why I Only Do 3 Sets Per Exercise":** it is his gym rule; on record his home workouts run on a
   timer. Default: script it as written, shown with dumbbells by the pool.
5. **Outdoor "Why Cables Beat Dumbbells":** it cannot be cut without cable footage and there is no gym B-roll.
   Default: script it, film the talking part, and mark its B-roll "gym, next shoot" on the B-roll list.
6. **Outdoor "Why You Must Train Your Abs Every Day":** three of the six exercises he names are gym moves.
   Default: keep all six in the words, show the three home ones.
7. **The ChatGPT coach reaction:** kept, but he called the first cut boring and the creator is not a big name.
   Default: script it with the new opening (0:14 to 0:27).

Also leave these as marked gaps unless the shoot doc already answers them: what ab etching costs (fake ab surgery),
and Dan's cues for the vacuum (take them from the Vacuum video outline; do not write new ones).

## The 15 reactions (green screen)

1. **Cristiano Ronaldo Sells An Ab Belt. It's Harder Than A Workout.** https://www.youtube.com/watch?v=RA45cq0i2AA&t=5s , 0:05 to 0:15 (10 s). "Cristiano Ronaldo SIXPAD Commercial 2015 in Tokyo".
2. **Surgeons Now Carve Fake Abs Into Belly Fat. Don't Do It.** https://www.youtube.com/watch?v=gNsElkQnkxE , 0:00 to 0:17 (17 s). 6abc Philadelphia, "New procedure uses foam to sculpt belly fat into 6-pack abs".
3. **Women Say They Love The Dad Bod. They Don't.** https://www.youtube.com/watch?v=LbwgABvQdUA&t=16s , 0:16 to 0:20, then 0:26 to 0:38, then 2:05 to 2:13 (24 s). Man vs Street, "Girls Like The Dad Bod Until We Showed Them This".
4. **Bill Maher Says Fat Shaming Should Come Back. He's Right.** https://www.youtube.com/watch?v=Dm4TAdiEFn0&t=353s , 5:53 to 6:10 (17 s). Real Time with Bill Maher, "New Rule: The Fudge Report".
5. **Dr. Mike Says Tirzepatide Is A Dial For Your Body Weight. He's Right.** https://www.youtube.com/watch?v=4jmKrdcjurA&t=660s , 11:00 to 11:23 (23 s). Renaissance Periodization, "Three Drugs Every Male Over 40 Should Take".
6. **TikTok Says Blended Oats Work Like Ozempic. They Don't.** https://www.youtube.com/watch?v=HBa5ZBBKAHM&t=26s , 0:26 to 0:43 (17 s). Good Morning America, "What to know about the 'oat-zempic' craze".
7. **He Hired ChatGPT As His Coach For A Year. He's Right.** https://www.youtube.com/watch?v=r7P9cxULmY8&t=14s , 0:14 to 0:27 (13 s). Aaron, "I Let AI Coach Me for a Year - Here's the Truth".
8. **Bill Maher Asks If You've Ever Seen A Fat 90-Year-Old. He's Right.** https://www.youtube.com/watch?v=yfiWjnStE3w&t=135s , 2:15 to 2:33 (18 s). Real Time with Bill Maher, "New Rule: Fat Acceptance".
9. **There's Now A Card That Tells Your Doctor Not To Weigh You. Bill Maher Is Right.** https://www.youtube.com/watch?v=yfiWjnStE3w&t=291s , 4:51 to 5:10 (19 s). Real Time with Bill Maher, "New Rule: Fat Acceptance".
10. **Bert Kreischer Thought His Billboard Was Photoshopped. It Wasn't.** https://www.youtube.com/watch?v=yaNjaOEaCE8&t=98s , 1:38 to 1:54 (16 s). JRE and Friends, "Joe Rogan Gives Bert Kreischer A Reality Check".
11. **Kevin James Tried One Cheat Day A Week. It Wrecked His Diet.** https://www.youtube.com/watch?v=tX5ZQ8rfHzY&t=41s , 0:41 to 0:49, then 0:58 to 1:07 (17 s). JRE Clips, "Kevin James on Cheat Days and Losing 60lbs After Fasting for 41 Days".
12. **Post Malone Lost 55 Pounds By Cutting Out One Drink. He's Right.** https://www.youtube.com/watch?v=4_mAsqSyAYU , 0:00 to 0:14 (14 s). Page Six, a clip from The Joe Rogan Experience.
13. **Terry Crews Doesn't Eat Until 2 PM. He's Right.** https://www.youtube.com/watch?v=dW_99QcCTzE , 0:00 to 0:12 (12 s). Business Insider, "Terry Crews on intermittent fasting".
14. **Alex Hormozi Asks A Fat Guy Why He Isn't 200 Pounds Heavier. He's Right.** https://www.youtube.com/watch?v=37mqHjJOS50&t=171s , 2:51 to 3:10 (19 s). The Iced Coffee Hour, "Alex Hormozi's advice on weight control".
15. **Mr. Olympia Shows The Vacuum. Here's How To Do It At Home.** https://www.youtube.com/watch?v=Y9yF7Ih49K8 , 0:00 to 0:15 (15 s). Chris Bumstead, "HOW TO HIT A VACUUM".

Check by eye before scripting: the Ronaldo belt ad and the Chris Bumstead vacuum have no speech, so their seconds
were set from a single frame. Open each, find the best 10 to 15 seconds, and correct `ideas.json` if they move.

## The 11 outdoor shirtless shorts

1. **How To Do Towel Rows (A Back Exercise With No Equipment)** B-roll: Pool shot 3 (towel rows, plus the close-up of the towel around the post).
2. **How To Do Reverse Lunges** B-roll: Pool shot 4 (with the beginner version).
3. **How To Do Bodyweight Squats** B-roll: Pool shot 1 (with the chair version).
4. **How To Do Goblet Squats** B-roll: Pool shot 16 (3 reps with the 50 pound kettlebell, plus picking it up).
5. **How To Do Overhead Tricep Extensions** B-roll: New shot for the pool list: 3 slow reps from the side, with a close-up of the elbows pointing up.
6. **3 Rules For Every Rep** B-roll: Pool shot 10 (3 fast, sloppy curls and 3 slow ones) and pool shot 8 (push-ups with handles). I swapped the cable examples for push-ups.
7. **Why I Only Do 3 Sets Per Exercise** B-roll: Pool shots 9 and 10 (side laterals, dumbbell curls) and shot 7 (kettlebell deadlifts). New shot: swapping the light dumbbells for the heavy ones.
8. **Why Cables Beat Dumbbells For Building Muscle** B-roll: Pool shot 10 covers the dumbbell half only.
9. **Why I Do A Total Body Workout Every Day** B-roll: All pool shots: jump rope (6) for the cardio, reverse lunges (4) or goblet squats (16) for legs, push-ups (8), towel rows (3) and side laterals (9) for upper body, toe touches (5) for abs.
10. **Why I Work Out First Thing In The Morning** B-roll: From the Around The House list: stepping outside into the morning sun, AG1 and the cold brew. Then any pool workout shots. No gym door shot.
11. **Why You Must Train Your Abs Every Day** B-roll: Pool shots 14 (ab wheel), 5 (toe touches) and 17 (vacuum).

The form cues in `ideas.json` are Dan's own words from his 10 Exercises, 5 Minute Workout and kettlebell outlines.
Keep them. Each how-to shows 3 full reps (memory `shorts-show-whole-exercise`).

## What to deliver

1. **Scripts in the shoot doc** (`1gt8Fi_wUaNaksa8sAdMoBvcdlBhZLek82EpBr-leq-0`). Reactions go at the end of SHORT
   FORM REACTION OUTLINES, before the Clavicular series heading. Outdoor shorts go at the end of SHORT FORM WORKOUT
   OUTLINES. Each one: the outline bullets, then the script, in the format of the two examples above. Re-read the doc
   immediately before writing into it: Dan edits it. Never strip or reorder what is there.
2. **The Reaction Clips document** (`1BcRpzDQYNCssROEvg10Z9cOL2AtdvBdyqHwvxxwHtQA`). Dan asked for this by name on
   2026-10-12: "modify my reactions document to add in the clips from here that I'll need to have queued up on my
   computer to react to." Add all 15 under GREEN SCREEN, in the order the scripts sit in Teleprompter 2. One heading
   per short, one bullet per clip piece: a link that opens at the first second, the source, the time range and
   length, and the first and last words. These are exact times, so no bullet says "pick" (except a clip still marked
   check by eye). Method and the in-code checks: `/teleprompterscripts`, "Reaction clip list".
3. **The B-roll list** (`1WPx31kcSsGtPyRmNBRb8fJHKC4ivi8gxl1k16wVizSY`): add, under the pool set, overhead tricep
   extensions (3 slow reps from the side, close-up of the elbows pointing up), swapping the light dumbbells for the
   heavy ones, a side close-up of how low the chest goes on push-ups with handles, and tag each existing pool shot
   with the new short that uses it. Add the cable shots under the gym set marked "next shoot".
4. **Teleprompter documents**, rebuilt from the shoot doc: the 15 reactions join Teleprompter 2 (Green Screen), the
   11 outdoor shorts join Teleprompter 3 (Outside By The Pool). Keep each under Dan's 50 page limit; split if one
   goes over. Re-import the changed ones into PromptSmart.
5. **A record** of the scripts as delivered in `Docs/` (same pattern as `Docs/SCRIPTS_1017_SHOOT_D_AS_DELIVERED_20261006.md`),
   and `Docs/SHOOT_1017_DOCS.md` updated with the new counts.

## Verification

- Word count and runtime range on every script; nothing over 66 seconds with its clip.
- `grep -c` for em dashes and en dashes on everything written: 0.
- Every clip id, link, time range and quote in the Reaction Clips document is found in the shoot doc text, and every
  YouTube id answers (`python3 .claude/skills/reaction-clips/reference/yt.py c ID ...`).
- Re-read the shoot doc after writing and confirm Dan's existing scripts are untouched.

## Size and order

26 scripts is a long task. Work in two passes and push the as-delivered record after each: the 15 reactions first
(they also drive the Reaction Clips document), then the 11 outdoor shorts, then the B-roll list and the teleprompter
rebuild last. If context runs past half, stop after the reactions pass and suggest a handoff for the rest.

## Finish

Delete this handoff's line from `AI_COORDINATION.md` and its row from `Handoffs/README.md`, and report in chat with
numbered action items for Dan at the end.

## Recommended model and starter prompt

**Claude Opus 5.5, high effort** (memory `model-routing-plan`: all writing, shorts scripts included).

> SFC. Read `Handoffs/handoff-20261012-1017-shoot-shorts-scripts.md` and execute it: write filming scripts for the 26
> shorts I locked for the 10/17 shoot (15 green screen reactions, 11 outdoor shirtless shorts) into the shoot doc,
> add the 15 clips to my Reaction Clips document so I have them cued up on shoot day, add the new B-roll shots, and
> rebuild Teleprompter 2 and 3. Ask me the open questions once at the start and keep drafting while I answer.
