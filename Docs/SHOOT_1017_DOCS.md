# 10/17 shoot: which document is which

Made 2026-10-11. Dan: the shoot doc is kept as it is for editing, and filming uses the four documents built from it.

| document | what it is for | id |
|---|---|---|
| Content Outlines And Scripts For 10/17 SixPackAbs.com Shoot | **The editing copy.** Outlines, filming scripts, every graphic, on-screen text, B-roll and clip cue in place. Editors and edit sessions work from this one. Never strip it. | `1gt8Fi_wUaNaksa8sAdMoBvcdlBhZLek82EpBr-leq-0` |
| 10-17 Shoot - Teleprompter 1 - Dark Green Backdrop | Words only, 21 scripts, 12,437 words | `1esSBLZldEbmSikeESYaXWo6n4vq1h0Qm8AhqB7Mo8cs` |
| 10-17 Shoot - Teleprompter 2 - Green Screen | Words only, 18 scripts, 7,609 words | `1KvL0_IilRCxlofnY5luTfRvjiseGGpGGXU4sAsjbgzQ` |
| 10-17 Shoot - Teleprompter 3 - Outside By The Pool | Words only, the 4 follow-along workouts, 2,763 words | `1yc2xg1sG4lTncvcAmkA17SN-JZnQSsbB9Q-fpEbXotg` |
| 10-17 Shoot - B-Roll List | Every B-roll shot by set, outdoor first, plus what the Edit Queue is blocked on | `1WPx31kcSsGtPyRmNBRb8fJHKC4ivi8gxl1k16wVizSY` |

All four are in My Drive beside the shoot doc, viewable by anyone with the link. Page counts: 22, 18 and 6, all under
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
