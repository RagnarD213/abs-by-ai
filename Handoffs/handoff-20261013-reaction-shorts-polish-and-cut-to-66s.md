# Handoff: copy polish the 19 reaction shorts in Teleprompter 2 and cut each one to 66 seconds

**SFC (short-form content). Written 2026-10-13 by Claude, at Dan's request. DONE 2026-10-14: every step, including the shoot doc.**
Sidebar name for the new task: `10/17 Reaction Shorts SFC Polish`.

## State at 2026-10-13 18:50 (read this first; it replaces the steps below where they differ)

**Done:** the polish and the cuts (34 tracked suggestions), Dan's rulings on all of them, the re-count, and the
PromptSmart import. Dan also had all four teleprompter documents changed to no blank lines between paragraphs.

**Left: step 3 only, carrying his final words into the shoot doc** (`1gt8Fi_wUaNaksa8sAdMoBvcdlBhZLek82EpBr-leq-0`).
- The words to use: `Docs/SCRIPTS_1017_SHOOT_REACTION_SHORTS_FINAL_20261013.md` (the 19 shorts), and for the long
  videos diff Teleprompter 2 against the shoot doc's filming scripts (Body Fat intro, Celebrity Ozempic passages).
- Three shorts run over 66 seconds by Dan's choice (Dad Bod 72.2, Retatrutide 69.4, Terry Crews 68.4). Do not cut them.
- Hormozi stays at "two pounds" and Ronaldo keeps its context line: Dan did not change either.
- New standing rules from this run: spelling, grammar and capitalization fixes go straight in, never tracked
  (`/copy-edit`); teleprompter documents have no blank lines and script edits happen in the shoot doc from now on
  (`/teleprompterscripts`). The shoot doc keeps its blank lines.
- When the shoot doc matches Teleprompter 2, remove the warning at the top of `Docs/SHOOT_1017_DOCS.md`. Do not
  rebuild Teleprompter 2 from the shoot doc until then.

Starter prompt: SFC. Rename this task `10/17 Reaction Shorts SFC Shoot Doc`. Read
`Handoffs/handoff-20261013-reaction-shorts-polish-and-cut-to-66s.md`, "State at 2026-10-13 18:50", and do the one
step left: carry the final wording of the 19 reaction shorts and my long-video edits from Teleprompter 2 into the
shoot doc's filming scripts, clip cue first, no hook takes. Claude Opus 5.5, high.

## Goal

Dan films these on 10/17. He edited the reaction shorts himself on 10-13, directly in the teleprompter document, and
12 of the 19 now run long. This task does two things to those 19 scripts, in that document:

1. Run the copy polish skill (`/copy-edit`) on them.
2. Edit each one down so it is **at most 66 seconds, clip included.**

Dan's words, 2026-10-13: "edit these down with a target maximum length of 66 seconds each. If it's a little bit over
60 seconds, then I can accelerate the footage." And, to be exact: "I want all of these scripts to target a maximum
length of 66 seconds, not 60 seconds." So the limit on the page is 66. Do not cut any script toward 60.

## The document, and the one trap

- **Work in Teleprompter 2:** `1KvL0_IilRCxlofnY5luTfRvjiseGGpGGXU4sAsjbgzQ` ("10-17 Shoot - Teleprompter 2 - Green
  Screen"). The 19 shorts run from "Cristiano Ronaldo Sells An Ab Belt..." to the end of the document ("Clavicular Says
  Hair Is Life"). The four long videos above them are not part of this task.
- **Teleprompter 2 is ahead of the shoot doc.** His edits exist only there. **Never rebuild it from the shoot doc**
  (`tp_from_shoot_doc.py`): that erases his work. Edit it in place with the Docs connector.
- Read the live document first and compare it with `Docs/SCRIPTS_1017_SHOOT_REACTION_SHORTS_DAN_EDITED_20261013.md`
  (the snapshot taken at 18:00 on 10-13). Anything different is a newer edit of his: keep it, and re-count.

## Read first

1. `Docs/SHOOT_1017_DOCS.md`: the note at the top, and the ids of every 10/17 document.
2. `.claude/skills/copy-edit/SKILL.md`: "Straight in, or tracked", "Polishing scripts, not sales copy", DON'T 10 to
   12, and the Docs connector mechanics.
3. `.claude/skills/shorts-scripting/SKILL.md`: "REACTION SHORTS: THE CLIP PLAYS FIRST" (what he changed on 10-13, with
   his own first lines), the 66 second rule and lesson 30.
4. `.claude/skills/teleprompterscripts/SKILL.md`: "When Dan edits a teleprompter document himself, it becomes the
   master", "A blank line between ALL paragraphs", and the PromptSmart upload steps.
5. Memory: `reaction-shorts-clip-first`, `scripts-blank-line-between-paragraphs`, `swearing-never-cut-never-ask`,
   `no-em-dashes`, `organic-drug-names-allowed`.
6. What he started from, to see his direction: `Docs/SCRIPTS_1017_SHOOT_26_SHORTS_AS_DELIVERED_20261013.md`.

## The length rule, as a word budget

Count at his slow pace, 198 words a minute, and add the clip. A script fits when
`spoken words / 198 x 60 + clip seconds` is 66 or less. That gives each short a word budget of
`(66 - clip seconds) x 3.3`, rounded down. Counts are from the 18:00 snapshot; re-count from the live document.

| # | short | clip | words now | most words allowed | cut at least |
|---:|---|---:|---:|---:|---:|
| 1 | Cristiano Ronaldo Sells An Ab Belt. It's Harder Than A Workout. | 10 s | 151 | 184 | fits |
| 2 | Surgeons Now Carve Fake Abs Into Belly Fat. Don't Do It. | 17 s | 163 | 161 | **2** |
| 3 | Women Say They Love The Dad Bod. They Don't. | 24 s | 170 | 138 | **32** |
| 4 | Bill Maher Says Fat Shaming Should Come Back. He's Right. | 17 s | 195 | 161 | **34** |
| 5 | Dr. Mike Says Tirzepatide Is A Dial For Your Body Weight. He's Right. | 23 s | 177 | 141 | **36** |
| 6 | TikTok Says Blended Oats Work Like Ozempic. They Don't. | 17 s | 186 | 161 | **25** |
| 7 | He Hired ChatGPT As His Coach For A Year. He's Right. | 13 s | 209 | 174 | **35** |
| 8 | Bill Maher Asks If You've Ever Seen A Fat 90-Year-Old. He's Right. | 18 s | 214 | 158 | **56** |
| 9 | There's Now A Card That Tells Your Doctor Not To Weigh You. Bill Maher Is Right. | 19 s | 122 | 155 | fits |
| 10 | Bert Kreischer Thought His Billboard Was Photoshopped. It Wasn't. | 16 s | 210 | 165 | **45** |
| 11 | Kevin James Tried One Cheat Day A Week. It Wrecked His Diet. | 17 s | 174 | 161 | **13** |
| 12 | Post Malone Lost 55 Pounds By Cutting Out One Drink. He's Right. | 14 s | 143 | 171 | fits |
| 13 | Terry Crews Doesn't Eat Until 2 PM. He's Right. | 12 s | 209 | 178 | **31** |
| 14 | Alex Hormozi Asks A Fat Guy Why He Isn't 200 Pounds Heavier. He's Right. | 19 s | 167 | 155 | **12** |
| 15 | Mr. Olympia Shows The Vacuum. Here's How To Do It At Home. | 15 s | 150 | 168 | fits |
| 16 | Clavicular Says Looks Matter More Than Personality. He's Right. | 18 s | 136 | 158 | fits |
| 17 | Clavicular Says Getting Lean Is 70% Of Softmaxxing. He's Right. | 20 s | 125 | 151 | fits |
| 18 | Clavicular Recommends Retatrutide. He's Wrong. | 13 s | 193 | 174 | **19** |
| 19 | Clavicular Says Hair Is Life. He's Right. | 9 s | 163 | 188 | fits |

Do not pad a script that already fits. A script may land under its budget; it may not land over.

## How to cut (his words, fewer of them)

- **Cut whole sentences, not words inside his sentences.** Trimming inside a line he typed is the edit he rejects
  (copy-edit DON'T 11). No new sentences. If a cut leaves a join that does not read, cut one more sentence instead.
- **Cut first:** a paragraph left over from Claude's draft that now says the same thing as a paragraph he wrote. His
  typing has curly apostrophes; the draft has straight ones. Known cases: Dr. Mike ("Tirzepatide is the drug in
  Zepbound..." and "But here's the lesson. Tirzepatide is a dial..."), Oatzempic ("Here's the lesson. When something
  on social media..." against his "So don't fall for TikTok fitness trends..."), Post Malone and Kevin James (the
  draft's bottom line beside his own close).
- **Cut next:** a second example, a sentence that restates the line before it, a sentence that describes what the clip
  just showed.
- **Keep:** the first line (his verdict), the lesson with its numbers, his hardest line in each script, and his close.
  Every short still starts with no line before the clip and no recap of the clip.
- **Never cut a line because it swears or because it is blunt**, and do not soften one. No compliance, legal or
  reputation commentary on any line or person (`AGENTS.md`).
- Do not touch the titles. Do not add hook takes back.

## How the edits go in

- **Polish, by the skill's own lists.** Typos, a dropped word, a misspelled name and punctuation go straight in. Any
  rewording of a line he reads is a tracked suggestion. In his lines, fix only what is on the straight-in list.
- **Every length cut is a tracked suggestion** (the skill's rule for a spoken line cut), sent with the Docs
  connector in suggestion mode. Build each script's set of cuts so that accepting all of them lands it at or under
  its budget. Dan can then use "Accept all" once, or reject a cut and tell you what to cut instead.
- Read the document back after sending. Check that only planned lines changed, that every paragraph still has a
  blank line after it, and that no em dash or en dash was added.
- Save an as-delivered file in `Docs/` (pattern: `Docs/COPYEDIT_1017_SHOOT_POLISH_AS_DELIVERED_20261010.md`) listing,
  per short: words before, words after if all cuts are accepted, total seconds, each sentence cut, each polish edit
  and whether it was direct or tracked.

## Ask Dan once, at the start, and keep working

1. **Hormozi:** the script says "two pounds over". His Fat Shaming and Bert Kreischer edits say three. Default: leave
   it as he has it.
2. **Ronaldo:** it still opens (after the clip) with "Cristiano Ronaldo will sell you a belt that shocks your abs.
   Here's what nobody tells you about it." The ad has no speech, so the line was kept as context. Default: keep it.

## Then, in this order

1. Report in chat: one table (short, words before, words after, seconds after), then the count of direct edits and
   tracked suggestions, then numbered action items. Tell him "Accept all" finishes it.
2. **After he has ruled on the suggestions:** re-count every short from the live document, confirm all 19 are at or
   under 66 seconds, and re-import Teleprompter 2 into PromptSmart (move the older card to its Trash). Update the
   word count for Teleprompter 2 in `Docs/SHOOT_1017_DOCS.md`.
3. **Then carry the final words into the shoot doc** (`1gt8Fi_wUaNaksa8sAdMoBvcdlBhZLek82EpBr-leq-0`), which still
   has the old versions: 15 scripts at the end of SHORT FORM REACTION OUTLINES and the 4 Clavicular scripts after
   them. For each: replace the spoken words with the teleprompter's, make the first cue the clip
   (`[OPEN ON THE CLIP, PLAYING BEHIND DAN ON THE GREEN SCREEN. DAN IS ON SCREEN WATCHING IT AND DOES NOT SPEAK UNTIL IT
   ENDS: ...]`), remove the `[COLD OPEN...]` cue and the hook takes, put the B-roll and on-screen cues where his new
   lines call for them, and fix the word count in each note line. Method for writing into that doc:
   `/teleprompterscripts`, "Writing new scripts into a long shoot doc with the Docs connector". Also carry over his
   edits to the long videos in Teleprompter 2 (the Body Fat intro and several Celebrity Ozempic passages). When the
   two documents match, remove the warning at the top of `Docs/SHOOT_1017_DOCS.md`.
   If context is past half before this step, stop after step 2 and suggest a handoff for it.

## Not in this task

- The 11 outdoor shorts in Teleprompter 3. They run 36 to 50 seconds and have not been polished. Say so in the
  report; do not start them unless Dan asks.
- The clips themselves. Ronaldo (0:05 to 0:15) and Chris Bumstead (0:00 to 0:15) are still "check by eye".

## Verification

- All 19 at or under 66 seconds at 198 words a minute plus the clip, counted from the live document, once the
  suggestions are accepted.
- No line before the clip in any of the 19, and no hook takes.
- `grep -c` for em dashes and en dashes on everything written: 0.
- Text export of Teleprompter 2: no paragraph sits directly under another, except a title and its first paragraph.
- PromptSmart shows one "10-17 Shoot - Teleprompter 2 - Green Screen" card, with the final word count.

## Finish

Delete this handoff's line from `AI_COORDINATION.md` and its row from `Handoffs/README.md`. Report in chat with
numbered action items at the end.

## Recommended model and starter prompt

**Claude Opus 5.5, high effort** (memory `model-routing-plan`: all writing and copy polish).

> SFC. Rename this task `10/17 Reaction Shorts SFC Polish`. Read
> `Handoffs/handoff-20261013-reaction-shorts-polish-and-cut-to-66s.md` and execute it: run the copy polish skill on
> the 19 reaction shorts in my Teleprompter 2 document, and edit each one down to a maximum of 66 seconds including
> the clip. Work in Teleprompter 2 itself, never rebuild it from the shoot doc. Ask me the two open questions once at
> the start and keep working while I answer.
