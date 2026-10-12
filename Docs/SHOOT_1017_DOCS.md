# 10/17 shoot: which document is which

Made 2026-10-11. Dan: the shoot doc is kept as it is for editing, and filming uses the four documents built from it.

| document | what it is for | id |
|---|---|---|
| Content Outlines And Scripts For 10/17 SixPackAbs.com Shoot | **The editing copy.** Outlines, filming scripts, every graphic, on-screen text, B-roll and clip cue in place. Editors and edit sessions work from this one. Never strip it. | `1gt8Fi_wUaNaksa8sAdMoBvcdlBhZLek82EpBr-leq-0` |
| 10-17 Shoot - Teleprompter 1 - Dark Green Backdrop | Words only, 21 scripts, 12,437 words | `1esSBLZldEbmSikeESYaXWo6n4vq1h0Qm8AhqB7Mo8cs` |
| 10-17 Shoot - Teleprompter 2 - Green Screen | Words only, 18 scripts, 7,609 words | `1KvL0_IilRCxlofnY5luTfRvjiseGGpGGXU4sAsjbgzQ` |
| 10-17 Shoot - Teleprompter 3 - Outside By The Pool | Words only, the 4 follow-along workouts, 2,763 words | `1yc2xg1sG4lTncvcAmkA17SN-JZnQSsbB9Q-fpEbXotg` |
| 10-17 Shoot - B-Roll List | Every B-roll shot by set, outdoor first, plus what the Edit Queue is blocked on | `1WPx31kcSsGtPyRmNBRb8fJHKC4ivi8gxl1k16wVizSY` |
| 10-17 Shoot - Reaction Clips | Made 2026-10-12. Every clip Dan reacts to (35 links, 17 videos), in teleprompter order, each link opening at the clip's start time | `1BcRpzDQYNCssROEvg10Z9cOL2AtdvBdyqHwvxxwHtQA` |

All five are in My Drive beside the shoot doc, viewable by anyone with the link. Page counts: 22, 18 and 6, all under
Dan's 50-page limit.

**PromptSmart:** the three teleprompter documents were imported on 2026-10-11 as three scripts with the same names
(`my.promptsmart.com/scripts`). The B-roll list is in Drive only, by his instruction.

## Which script is on which set

- **Green screen (18):** What Every Body Fat Percentage Looks Like (On Me), How Losing Fat Changed My Face, I Ranked
  Every Ab Exercise From Worst To Best, Reacting To Celebrity Ozempic Transformations, Reacting To Bryan Johnson's $2
  Million Body, Reacting To The Worst Ab Workouts On Instagram, A Doctor Says Zepbound Eats Your Muscle, and the 11
  Clavicular shorts. The reaction videos were Dan's call. The first three were Claude's pick (a picture on screen most
  of the video) and wait for his word.
- **Outside by the pool (4):** the 5, 10, 15 and 20 minute follow-along workouts.
- **Dark green backdrop (21):** everything else.

## Keeping them in step

The teleprompter docs were built from the shoot doc as it stood at 2026-10-11 18:58 UTC, with no suggestions pending.
If a script changes in the shoot doc after that, rebuild: `.claude/skills/teleprompterscripts/SKILL.md`, section v3.

## Edit Queue items on the B-roll list

- DS-27 Home Workouts short: the six pieces of home equipment (yoga mat, push-up handles, light dumbbells, kettlebell,
  ab wheel, jump rope). When filmed: `queue.py set DS-27 ready`.
- DS-29 Robot Lawn Mower short: the mower leaving its dock, mowing, passing the camera, returning. Then `queue.py set
  DS-29 ready`.
- DS-26 Wispr Flow short is blocked on a screen recording (the ScreenFlow demo), not on B-roll.

## Reaction clips

14 of the 35 links are exact (start and end second, first and last words): the 13 Clavicular clips and their two
alternates. The other 21 say "pick 10 to 30 seconds" inside a window, because the exact seconds were never chosen;
those links open at the start of the window. All 14 YouTube videos answered on 2026-10-12. Dan's own clips (the jump
rope short, the ab wheel video, the salad video) are not on the list: he is not reacting to them.

## More shorts for this shoot: locked picks and a second round of reactions (2026-10-12)

One review page holds all of it: `Docs/shoot-1017-shorts-ideas/index.html`, served at http://127.0.0.1:8881/
(`review_server.py 8881 Docs/shoot-1017-shorts-ideas`). Nothing from it is in the shoot doc yet.

- **Locked by Dan, 7 reactions** (the `LK` list in the page, with his changes): Ronaldo's ab belt, fake ab surgery, the dad
  bod street interview (3 piece cut), Bill Maher on fat shaming, Dr. Mike on tirzepatide, Oatzempic (lesson: check it with
  AI first), the ChatGPT coach (new opening cut; he may still kill it).
- **Locked by Dan, 11 outdoor shirtless shorts** (the `OD` list): towel rows, reverse lunges, bodyweight squats, goblet
  squats, overhead tricep extensions, 3 Rules For Every Rep, Why I Only Do 3 Sets, Why Cables Beat Dumbbells, total body
  every day, working out first thing in the morning, train abs every day. **No gym B-roll on this shoot** (Dan): every shot
  is from the pool and home lists. Three carry an open note on their card (3 sets, cables, the abs list).
- **Waiting for his picks, 20 new reactions** (the `RX` list), chosen by his rules in `/shortsideas`, "Reaction shorts".
- The 9 outdoor ideas he killed are parked in `Docs/NEXT_SHOOT_LIST.md` for the next shoot.

Next: when Dan replies with his keeps from the 20, script every locked short with `/shorts-scripting` into the shoot doc
(reactions under SHORT FORM REACTION OUTLINES, outdoor ones under SHORT FORM WORKOUT OUTLINES), add the clips to the Reaction
Clips document, add the new B-roll shots (overhead tricep extensions, swapping light for heavy dumbbells) to the B-roll
list, and rebuild the teleprompter documents. The outdoor shorts are read shirtless by the pool: they go in Teleprompter 3.

Trap: `review_server.py` treats any quoted string ending in .jpg, .js, .html and so on as a local file, even inside a
script. Build remote image paths in pieces (`"/hqdefault" + ".jpg"`) or the server refuses to start.

## Reaction clip review page (2026-10-12, waiting for Dan)

`http://localhost:8875/` (managed by `review_server.py`, source `review/1017-reaction-clips/`). 29 clips, each with my
pick and up to two alternates, 73 options in all. The data is `Docs/SHOOT_1017_REACTION_CLIP_PICKS.json`.

When Dan replies with his choices: put the exact start and end of each chosen clip into the `[PLAY CLIP ...]` cue of
the shoot doc (direct edits: they are filming directions) and into the Reaction Clips Google Doc, replacing every
"pick 10 to 30 seconds". Nine Clavicular clips also move by a second or two (ends were cutting off a word).

Six script lines the clips do not back up, shown to him on the page for his call: Sharon Osbourne (42 pounds in a
year, not four months), Meghan Trainor (the two quotes are not in the ET video), Charles Barkley (he does not say he
regained it), Oprah (15 pounds, and no "a lifetime thing"), Bryan Johnson's plasma (he does not say he stopped), and
the doctor short (the doctor makes the script's own point about protein and strength training).
