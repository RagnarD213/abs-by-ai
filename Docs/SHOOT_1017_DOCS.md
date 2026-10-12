# 10/17 shoot: which document is which

Made 2026-10-11. Dan: the shoot doc is kept as it is for editing, and filming uses the four documents built from it.

| document | what it is for | id |
|---|---|---|
| Content Outlines And Scripts For 10/17 SixPackAbs.com Shoot | **The editing copy.** Outlines, filming scripts, every graphic, on-screen text, B-roll and clip cue in place. Editors and edit sessions work from this one. Never strip it. | `1gt8Fi_wUaNaksa8sAdMoBvcdlBhZLek82EpBr-leq-0` |
| 10-17 Shoot - Teleprompter 1 - Dark Green Backdrop | Words only, 21 scripts, 12,437 words | `1esSBLZldEbmSikeESYaXWo6n4vq1h0Qm8AhqB7Mo8cs` |
| 10-17 Shoot - Teleprompter 2 - Green Screen | Words only, 8 scripts, 4,958 words, 9 pages (rebuilt 2026-10-12 after Dan's clip kills; same Drive id, replaced in place) | `1KvL0_IilRCxlofnY5luTfRvjiseGGpGGXU4sAsjbgzQ` |
| 10-17 Shoot - Teleprompter 3 - Outside By The Pool | Words only, the 4 follow-along workouts, 2,763 words | `1yc2xg1sG4lTncvcAmkA17SN-JZnQSsbB9Q-fpEbXotg` |
| 10-17 Shoot - B-Roll List | Every B-roll shot by set, outdoor first, plus what the Edit Queue is blocked on | `1WPx31kcSsGtPyRmNBRb8fJHKC4ivi8gxl1k16wVizSY` |
| 10-17 Shoot - Reaction Clips | Every clip Dan reacts to, survivors only since 2026-10-12 (12 links, 7 videos), in teleprompter order, each link opening at the clip's exact start second | `1BcRpzDQYNCssROEvg10Z9cOL2AtdvBdyqHwvxxwHtQA` |

All five are in My Drive beside the shoot doc, viewable by anyone with the link. Page counts: 22, 9 and 6, all under
Dan's 50-page limit.

**PromptSmart:** the three teleprompter documents were imported on 2026-10-11 as three scripts with the same names
(`my.promptsmart.com/scripts`). The B-roll list is in Drive only, by his instruction. Teleprompter 2 was imported again
on 2026-10-12 (script 1488017) and the 10-11 copy moved to PromptSmart's Trash. His subscription shows "expires Oct 20, 2026".

## Which script is on which set

- **Green screen (8, was 18):** What Every Body Fat Percentage Looks Like (On Me), How Losing Fat Changed My Face, I Ranked
  Every Ab Exercise From Worst To Best, Reacting To Celebrity Ozempic Transformations, and four Clavicular shorts
  (Looks Matter More Than Personality, Getting Lean Is 70%, Retatrutide, Hair Is Life). The reaction videos were Dan's
  call. The first three were Claude's pick (a picture on screen most of the video) and wait for his word.
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

Every time in the Reaction Clips document is exact since 2026-10-12, and matches the `[PLAY CLIP ...]` cue in the
shoot doc. Dan's own clips (the jump rope short, the ab wheel video, the salad video) are not on the list: he is not
reacting to them. The Retatrutide short has no clip yet (see below).

## 26 more shorts locked for this shoot, not scripted yet (2026-10-12)

Dan locked **15 green screen reactions and 11 outdoor shirtless shorts** over two idea rounds. They are outlines only.

- **Source of truth:** `Docs/shoot-1017-shorts-ideas/ideas.json` (titles, video ids, start and end seconds, first and last
  words, reaction bullets, B-roll, open notes). The page built from it, with a working player per clip:
  http://127.0.0.1:8881/ (`review_server.py 8881 Docs/shoot-1017-shorts-ideas`). Rebuild the page with
  `.claude/skills/reaction-clips/reference/page.py`, never by hand.
- **No gym B-roll on this shoot** (Dan). The 9 outdoor ideas he killed for that reason are parked in
  `Docs/NEXT_SHOOT_LIST.md`.
- **Next:** `Handoffs/handoff-20261012-1017-shoot-shorts-scripts.md` writes the 26 scripts into the shoot doc, adds the 15
  clips to the Reaction Clips document, adds the new B-roll shots and rebuilds Teleprompter 2 and 3.
- How the clips were chosen, and the log of what Dan kept and killed: `.claude/skills/reaction-clips/SKILL.md`.

Trap: `review_server.py` treats any quoted string ending in .jpg, .js, .html and so on as a local file, even inside a
script. Build remote image paths in pieces (`"/hqdefault" + ".jpg"`) or the server refuses to start.

## Dan's clip kills, done 2026-10-12

He watched all 30 clips and killed 18. Out of the shoot doc, the Reaction Clips document, the B-roll list and
Teleprompter 2 (Drive and PromptSmart): Charles Barkley, the doctor's "Ozempic face" clip and the Elon Musk posts (all
Celebrity Ozempic, now 1,230 spoken words), the whole Bryan Johnson video, and nine shorts (Worst Ab Workouts, the
Zepbound doctor, and Clavicular's GLP-1, Nose Job, Hammer, Tan, Sunscreen, Supplements and Eyebrows). Every removed
script is saved word for word in `Docs/SHOOT_1017_KILLED_SCRIPTS_20261012.md`. His reasons: `/teleprompterscripts`,
"What Dan killed".

**Bryan Johnson was removed on a default, not on his word.** Every body clip was killed and he did not answer keep or
kill. To restore it, paste its section from the killed-scripts file before LONG FORM WORKOUT OUTLINES and rebuild
Teleprompter 2.

**Open, all Dan's:**

- **Retatrutide clip.** Three candidates are on the review page, `http://127.0.0.1:8875/` (source
  `review/1017-reaction-clips/`, data `Docs/SHOOT_1017_REACTION_CLIP_PICKS.json`): VladTV `GRHcYzsTvlM` 1:42 to 1:55
  (my pick, "I advocate for retatrutide"), Hannity `al13dc8reXg` 30:42 to 30:51 ("reta is extremely safe"), VladTV
  4:37 to 4:50. Times are from captions, good to a second or two. When he chooses: put it in the outline cue, the
  script cue and the header of that short, change the series note ("The clips are from one video..."), add the link
  to the Reaction Clips document, and check the script still fits the clip. The script has not been touched.
- **Two tracked suggestions in the Celebrity script:** cutting "So anyone who tells you that taking a GLP-1 is
  cheating..." (from the earlier pass) and "They all stopped" to "They both stopped". Teleprompter 2 was built with
  both accepted. If he rejects either, rebuild it.
- **Three script lines the surviving clips do not back up:** Sharon Osbourne (script: 42 pounds in about four months;
  clip: in a year), Meghan Trainor (the two quotes are not in the ET video), Oprah (script: 20 pounds and "a lifetime
  thing"; clip: 15 pounds, and the phrase is not said). Not changed without his word.
