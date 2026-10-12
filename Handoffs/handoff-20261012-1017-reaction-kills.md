# Handoff: take the killed reaction clips out of the 10/17 shoot, rebuild the teleprompter script, finish the clips list

**Written 2026-10-12 (Claude). Recommended: Claude Opus 5.5, High effort, local (needs Chrome for PromptSmart and
rclone for Drive).** Scripts and filming documents, not video editing. The shoot is 10/17.

## Goal

Dan watched every reaction clip on the review page and killed most of them. Three things are owed:

1. The filming scripts in the shoot doc with the killed clips, and the killed shorts, taken out.
2. The Green Screen teleprompter script rebuilt from the edited shoot doc, in Google Drive and in PromptSmart.
3. The Reaction Clips document, holding only the survivors, each link opening at the exact second, to watch from.

Read first: `Docs/SHOOT_1017_DOCS.md` (which document is which, all ids), `.claude/skills/copy-edit/SKILL.md`
("Straight in, or tracked" and "When the scripts are final"), `.claude/skills/teleprompterscripts/SKILL.md` (section
v3 to the end), `Docs/memory/reaction-videos-clips-first.md`.

## Dan's decisions (2026-10-12, his words in quotes)

**Killed, already done in the shoot doc:** the doctor's "Ozempic face" clip and the Elon Musk posts, both in the
Celebrity Ozempic video. One tracked suggestion from that pass may still be pending in the Celebrity script (cutting
"So anyone who tells you that taking a GLP-1 is cheating..."): leave it for him.

**Killed, still to do:**

| what | where | his reason |
|---|---|---|
| Charles Barkley segment | long-form "Reacting To Celebrity Ozempic Transformations" | not attention-getting, does not make sense in context |
| Clips BJ-2 to BJ-7 (bedtime, cold room, eating window, training, pills, his son's blood) | long-form "Reacting To Bryan Johnson's $2 Million Body" | "too boring", "no good lesson I can pull out of it" |
| Whole short | "Reacting To The Worst Ab Workouts On Instagram" | "Terrible choice. This is too boring. Doesn't actually say anything." |
| Whole short | "A Doctor Says Zepbound Eats Your Muscle. He's Wrong." | "too boring" |
| Whole short | "Clavicular Says Billionaires Use A GLP-1 To Stay Lean. You Should Too." | "No good lesson there" |
| Whole short | "Clavicular Wants A Nose Job. He's Wrong." | "too boring, not relevant to us" |
| Whole short | "Clavicular Hits His Face With A Hammer. He's Wrong." | "No good lesson there" |
| Whole short | "Clavicular Says Get A Tan. He's Right." | "Too boring" |
| Whole short | "Clavicular Says Sunscreen Keeps You Looking Young. He's Right." | "too boring" |
| Whole short | "Clavicular Says Supplements Change Your Skin. He's Right." | killed |
| Whole short | "Clavicular Says Groom Your Eyebrows. He's Right." | killed |

**Changed, not killed:**

- Bryan Johnson opener: use alternate 1, `kf9e1o7rUeo` 0:00 to 0:16 ("As a species, we accept our..."). "The first
  one isn't really saying anything, it is just saying who Bryan Johnson is."
- Retatrutide short: keep the short, replace the clip. "Terrible clip of him talking about Reta. So many unrelated
  things in there. I want a clip for that one of him only talking about" retatrutide.

**Open question for Dan, ask it first in one line:** every body clip of the Bryan Johnson video is now killed and
only the opener is left. Kill the whole video for this shoot, or keep it? Claude's recommendation, and the default if
he does not answer: take it out of this shoot, and bring it back only with clips he has watched first (his new rule).

## Survivors, with exact times

All from `Docs/SHOOT_1017_REACTION_CLIP_PICKS.json` (every option, with the words). He chose no other alternates, so
these are the picks.

| video | clip | YouTube id | start to end | seconds |
|---|---|---|---|---|
| How Losing Fat Changed My Face | Clavicular, gym to face | `PQaMZceY-0I` | 9:14 to 9:42 | 554 to 582 |
| How Losing Fat Changed My Face | Clavicular, the 70% line | `PQaMZceY-0I` | 23:34 to 23:54 | 1414 to 1434 |
| Celebrity Ozempic | Sharon Osbourne (E! News) | `oZTHGIoqwI4` | 0:00 to 0:28 | 0 to 28 |
| Celebrity Ozempic | Fat Joe (Page Six) | `XkGHIKXLShA` | 0:00 to 0:20 | 0 to 20 |
| Celebrity Ozempic | Amy Schumer (Howard Stern) | `unx1EuJ8t9s` | 1:05 to 1:27 | 65 to 87 |
| Celebrity Ozempic | Meghan Trainor (ET) | `DNTlfd8Cbk4` | 0:28 to 0:46 | 28 to 46 |
| Celebrity Ozempic | Oprah | `g7pw3MJ7QVE` | 53:28 to 53:44 | 3208 to 3224 |
| Celebrity Ozempic | Tracy Morgan | none | quote on screen, no clip | |
| Bryan Johnson (if kept) | opener, Netflix trailer | `kf9e1o7rUeo` | 0:00 to 0:16 | 0 to 16 |
| Clavicular: Looks Matter More Than Personality | Clavicular | `PQaMZceY-0I` | 3:35 to 3:53 | 215 to 233 |
| Clavicular: Getting Lean Is 70% | Clavicular | `PQaMZceY-0I` | 23:34 to 23:54 | 1414 to 1434 |
| Clavicular: Hair Is Life | Clavicular | `PQaMZceY-0I` | 1:49:29 to 1:49:38 | 6569 to 6578 |
| Clavicular: Retatrutide | NEW CLIP NEEDED | | old one was 1:50:02 to 1:50:15 | |
| Cortisol Belly (dark green backdrop) | TikTok @ebbymoyer, backup @jezebel511 | links in the shoot doc | whole clip | |

## The work, in order

1. **Ask Dan the Bryan Johnson question.** Carry on with everything else while waiting.
2. **Save the text you are about to remove.** Copy every killed short's script, and the Bryan Johnson script if it
   goes, into `Docs/SHOOT_1017_KILLED_SCRIPTS_20261012.md`, so nothing is lost outside Google's version history.
3. **Edit the shoot doc** (`1gt8Fi_wUaNaksa8sAdMoBvcdlBhZLek82EpBr-leq-0`) through the Docs connector with
   `targetRevisionId`: Dan is often in the doc. Tools and steps: `/copy-edit`, "Mechanics: edits through the Docs
   connector". What he ordered goes straight in; wording you had to invent is tracked.
   - Celebrity Ozempic: remove the Charles Barkley clip cue, his paragraph and its on-screen text. The group intro
     ("OK, this last group is the most important one. They all stopped, and the weight came back.") now covers Oprah
     and Tracy Morgan only: offer any reword as a tracked suggestion.
   - Remove the nine killed shorts whole: script, and the outline above it. Fix the Clavicular series note ("All 11
     clips are from one video").
   - Bryan Johnson: per his answer. If it stays, only the opener cue changes (to 0:00 to 0:16).
   - Put the exact times from the table into each surviving `[PLAY CLIP ...]` cue, replacing every "PICK 10 TO 30
     SECONDS INSIDE ...". The Clavicular cues get the corrected ends (the old ones cut off a word).
   - Update the header word counts of the scripts you changed.
   - The B-roll list at the top of the doc, and the B-Roll List Google Doc
     (`1WPx31kcSsGtPyRmNBRb8fJHKC4ivi8gxl1k16wVizSY`): take out shots that only the killed videos needed (the DIM and B6
     bottles, the eyebrow open, the Tan and Sunscreen tags, the Bryan Johnson tags if it goes) and fix the tags on
     shots other videos still use.
   - Verify with `verify_suggestions.py before.json after.json --diff`: every changed line is one you planned.
4. **Retatrutide clip.** The Iced Coffee Hour interview names retatrutide once, inside a rapid-fire list. Find two or
   three candidates where Clavicular talks only about it (another interview or his own video; captions through
   `youtube_transcript_api`), each under 20 seconds, and show them to Dan on the review page before touching the
   script. If nothing good exists, tell him and ask whether to kill that short too.
5. **Rebuild the Green Screen teleprompter script** from the edited doc:
   `.claude/skills/teleprompterscripts/reference/tp_from_shoot_doc.py`. Upload with rclone, check the folder for a
   second file with the same name (replace or duplicate is untested), verify line by line, count the pages. Then
   PromptSmart (`my.promptsmart.com/scripts`, his Chrome): import the new one, confirm it, and move the old "10-17
   Shoot - Teleprompter 2 - Green Screen" script to PromptSmart's Trash (it can be restored from there). Tell Dan you
   did. Teleprompter 1 and 3 do not change.
6. **Reaction Clips document** (`1BcRpzDQYNCssROEvg10Z9cOL2AtdvBdyqHwvxxwHtQA`): survivors only, exact times, links
   cued to the start second (`&t=<seconds>s`). Method and checks: `/teleprompterscripts`, "Reaction clip list". This
   is the document he asked for: "all of these surviving shorts that we didn't kill, with the clips for everything to
   watch."
7. **Refresh the review page** (`review/1017-reaction-clips/`, port 8875, `reaction_clips_page.py` then
   `review_server.py 8875 review/1017-reaction-clips`) so it shows survivors and the retatrutide candidates.
8. **Update `Docs/SHOOT_1017_DOCS.md`**, push with `scripts/git/safe-push.sh`, and delete this handoff's lines from
   `Handoffs/README.md` and the board.

## Still Dan's call (surviving clips where the script says something the clip does not)

- Sharon Osbourne: script says 42 pounds in about four months; the clip says 42 pounds in a year.
- Meghan Trainor: the two quotes in the script are not in this ET video (it reads out her post about Mounjaro).
- Oprah: script says 20 pounds and "a lifetime thing"; she says 15 pounds, and "a lifetime thing" is not said.

He has seen these on the review page and has not answered. Ask once, with the cuts, and do not change the lines
without his word.

## State when this was written

- Shoot doc: the two earlier kills are in. Nothing else in this handoff has been started.
- Teleprompter 2 in Drive (`1KvL0_IilRCxlofnY5luTfRvjiseGGpGGXU4sAsjbgzQ`) and in PromptSmart still has every killed
  script. Do not let him film from it.
- Review page: 28 clips, his kills not yet removed. Reaction Clips doc: the doctor and Elon bullets removed only.
- The captions used for the picks were in a session scratch folder and are gone: fetch again if needed.
- New standing rule, already saved (memory `reaction-videos-clips-first`, `_shared/WRITING-RULES.md` section 4): for
  reaction videos the clips are found first and Dan watches them before any script is written.

## Starter prompt

> Read `Handoffs/handoff-20261012-1017-reaction-kills.md` and execute it. I killed most of the reaction clips for the
> 10/17 shoot. Take the killed clips and shorts out of the shoot doc, rebuild the Green Screen teleprompter script in
> Drive and PromptSmart, and give me the Reaction Clips document with only the survivors, each link opening at the
> exact second. Bryan Johnson video: [KILL IT / KEEP IT]. Find me two or three better retatrutide clips to watch
> before you touch that short.

Model and effort: **Claude Opus 5.5, High.** It edits scripts he films in five days, so a miss costs a filming day.
