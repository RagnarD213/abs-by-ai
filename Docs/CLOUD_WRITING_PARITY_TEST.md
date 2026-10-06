# Cloud writing parity test

Written 2026-10-06. Purpose: prove a cloud Claude session writes the same quality as a local one for the three jobs Dan
runs most: an ad script, a dedicated short, and a final polish of sales copy.

A cloud session starts from the GitHub repo. It has the skills, `CLAUDE.md`, `AGENTS.md`, `Docs/memory/` and
`.claude/skills/_shared/WRITING-RULES.md`. It has no chat history, no local memory folder, no Chrome and no Mac
clipboard. This test finds what is still missing.

## How to run it

1. Start three cloud tasks on this repo, Opus 5.5, high effort. Paste one prompt into each, unchanged.
2. Score each result against the checklist below. Yes or no per line.
3. Compare with the local baseline scores in "Results".
4. Every cloud "no" that the local run got "yes" is a missing rule. Add it to the skill, to `WRITING-RULES.md` or to
   `Docs/memory/`, push, and run that test again. Stop when cloud matches local.

Limits of this test: it checks that cloud equals local, not that either is perfect. The answer keys are older than
some rules (the ad key is from 2026-08-10, before the no em dash rule and before the 7-day trial became the offer), so
they are the reference for voice only. The rules are scored by the checklist.

## Prompt 1: ad script (/scriptwriting)

```
Writing parity test 1 of 3: ad script. This is a test, so do not edit any existing Google Doc.

Read CLAUDE.md, then .claude/skills/_shared/WRITING-RULES.md and the Docs/memory entries it lists for ad scripts. Then use /scriptwriting to turn the ad outline in Docs/parity-test/case1_input_outline.txt into the finalized word-for-word teleprompter script with filming cues, exactly as you would for a real job. Apply today's rules even where the outline is older than a rule.

Deliver: (1) the full script in chat; (2) a new Google Doc titled "PARITY TEST 1 ad script" plus the word cloud or local and today's date, holding the same script, set to anyone-with-link view, with its link. If you cannot create or share it, say exactly what stopped you and carry on.

Finish with a block headed REPORT that states: where you are running (cloud or local) and the model; the spoken word count; the number of em dashes and en dashes in everything you wrote (count them, do not estimate); every rule file and every Docs/memory entry you actually opened; the real Google Doc and the heading this piece belongs under; and any rule or step you could not follow, with the reason. Do not open Docs/CLOUD_WRITING_PARITY_TEST.md and do not look for an answer key.
```

Answer key for voice: Ad 15, "I Was the Dad Who Swam in a T-Shirt", in the finalized scripts doc
`1r3Jmuihyryq0qv2Y3A--D_yaerF9B_ZqAb-QvOuAwjg` (the version left after Dan's line edit of 2026-08-10, about 630 spoken
words).

## Prompt 2: dedicated short (/shorts-scripting)

```
Writing parity test 2 of 3: dedicated short. This is a test, so do not edit any existing Google Doc.

Read CLAUDE.md, then .claude/skills/_shared/WRITING-RULES.md and the Docs/memory entries it lists for shorts. Then use /shorts-scripting to turn the idea below into the finished teleprompter script with b-roll cues, exactly as you would for a real job.

IDEA:
3 Unexpected Ways Zepbound Helped Me
  - Reduced my alcohol consumption
  - Made me more productive at work
  - Made me sleep better (due to less late night eating)

Deliver: (1) the full script in chat; (2) a new Google Doc titled "PARITY TEST 2 short" plus the word cloud or local and today's date, holding the same script, set to anyone-with-link view, with its link. If you cannot create or share it, say exactly what stopped you and carry on.

Finish with a block headed REPORT that states: where you are running (cloud or local) and the model; the spoken word count; the number of em dashes and en dashes in everything you wrote (count them, do not estimate); every rule file and every Docs/memory entry you actually opened; the real Google Doc and the heading this piece belongs under; and any rule or step you could not follow, with the reason. Do not open Docs/CLOUD_WRITING_PARITY_TEST.md and do not look for an answer key.
```

Answer key for voice: "3 Unexpected Ways Zepbound Helped Me" in the 8/28 shoot doc
`1yZjcG5pkbw0kPsfTvc7OOr2bX6v0bVYMqquUiRENQ4k`, section 6 (the version left after Dan's edits, 198 spoken words).

## Prompt 3: copy polish (/copy-edit)

```
Writing parity test 3 of 3: copy polish. This is a test, so do not edit any existing Google Doc.

Read CLAUDE.md, then .claude/skills/_shared/WRITING-RULES.md and the Docs/memory entries it lists for sales letters. Then use /copy-edit on the passage below, which is from the Abs By AI sales letter. Read the source the letter was adapted from, as the skill says. Make only the changes the skill allows.

PASSAGE:
By combining multiple different frontier AI models - and using the right types of prompts for each - I was able to create the ultimate AI fitness coach.

My AI fitness coach changed my life. It took me from having a soft and flabby dad bod at 38, to having the abs I always wanted at 40.

But my AI coach had a few downsides…

First, it cost me over $1000 a month in AI subscriptions.

Next, it was difficult and complicated to use.

And finally, it just took up a ton of my time.

So I decided to create my own app to do everything my AI fitness coach could do. I wanted to create something that would be simple for me to use, without the subscription costs, and without the endless prompting.

Once I had my AI coach in his own app, my results got FAR better. And working with my coach got far easier.

Deliver in chat: (1) a table of every change as an exact find and replace pair with a one-line reason; (2) the polished passage in full; (3) anything you chose to leave alone on purpose, and why.

Finish with a block headed REPORT that states: where you are running (cloud or local) and the model; the spoken word count; the number of em dashes and en dashes in everything you wrote (count them, do not estimate); every rule file and every Docs/memory entry you actually opened; the real Google Doc and the heading this piece belongs under; and any rule or step you could not follow, with the reason. Do not open Docs/CLOUD_WRITING_PARITY_TEST.md and do not look for an answer key.
```

Answer key: the same passage as it stands today in the sales letter
`1zCLn6pIuxGv4H1hkyieCk2T4NoYAQBnaNKMEFMcYV9o`, end of the section "I Devoted My Life To Creating The Ultimate AI
Fitness Coach". Dan accepted four edits there: "multiple" became "five"; "from having a soft and flabby dad bod at 38,
to having the abs" became "from a soft, flabby dad bod at 38 to the abs"; "Next" became "Second"; "create my own app"
and "I wanted to create something that would be simple for me to use" became "build my own app" and "Something simple
to use". He REJECTED a change to "his own app" in the last paragraph, so a correct run leaves "his own app" alone.

## Checklist

Score every line yes or no. "Dan's read" lines are his call; the rest can be checked by counting.

All three tests:

| # | Check |
|---|---|
| A1 | It read `WRITING-RULES.md` and at least the "anything in Dan's voice" memory entries (its REPORT lists them) |
| A2 | Em dash and en dash count in everything it wrote is 0 |
| A3 | No mention of Dan as a marketer or an ad agency owner |
| A4 | No "my wife"; no "my kids" or "my son" about his own child; before = 38 and 200 lb, abs at 40 |
| A5 | No invented fact, number, habit or study about Dan; every personal fact is on record |
| A6 | No banned claim: no promised physical result, no "trick", no "thousands of guys" or member count |
| A7 | It did not edit any existing Google Doc, and named the right doc and heading for the piece |
| A8 | Dan's read: it sounds like him, blunt and specific, not like an assistant |

Test 1 only (ad script):

| # | Check |
|---|---|
| B1 | Opens on the outline's skip stopper in the first 5 seconds, word for word or stronger |
| B2 | The ask is the 7-day free trial with "tap the button below". It does not ask for a free image upload |
| B3 | No disease name and no drug name (it is an ad) |
| B4 | Cues are in ALL CAPS in square brackets, with a blank line between paragraphs and between cues and spoken words |
| B5 | Spoken length is within 15 percent of the key (about 535 to 725 words) |
| B6 | The test Google Doc exists and is shared, or it said exactly what stopped it |

Test 2 only (short):

| # | Check |
|---|---|
| C1 | 172 to 185 spoken words, and never past the 66 second ceiling |
| C2 | Hook lands in the first 5 seconds and gives a reason to watch |
| C3 | Covers the three bullets, in Dan's first person, with no added point he did not give |
| C4 | Has the `[AbsByAI.com mark on screen]` cue and does not say "tap the button below" (it is organic) |
| C5 | Title in Title Case, script in the skill's layout with b-roll cues |
| C6 | The test Google Doc exists and is shared, or it said exactly what stopped it |

Test 3 only (polish):

| # | Check |
|---|---|
| D1 | It made at least 3 of the 4 edits Dan accepted (see the answer key) |
| D2 | It left "his own app" alone |
| D3 | It changed nothing about the message, the structure or the offer, and kept " - " and the ellipsis as Dan writes them |
| D4 | Every change is an exact find and replace pair with a reason |
| D5 | It kept "$1000 a month" and the ages as written |

## Results

