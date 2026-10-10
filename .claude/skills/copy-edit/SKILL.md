---
name: copy-edit
description: >
  Final polish pass on finished sales copy before it goes into production: a sales
  letter, a landing page, a VSL or ad teleprompter script, a sales email. Tightens
  the language, fixes typos and inconsistencies, applies the claims rules on record,
  keeps Dan's voice and the VSL language, and delivers every change as a Google Docs
  SUGGESTION so Dan accepts or rejects each one. It never changes the marketing
  message, the structure or the offer. Use whenever Dan asks to polish, sharpen,
  tighten, proofread, copy-edit, or "do a final pass" on sales copy, even if he
  doesn't say "/copy-edit". Writing the copy is /scriptwriting or /scriptfromoutline;
  a teleprompter-only copy is /teleprompterscripts; reviewing a video cut is /revisions.
---

> **Shared writing rules (2026-10-06):** before writing, read `.claude/skills/_shared/WRITING-RULES.md`. It holds the rules every writing skill follows and the list of memory entries (`Docs/memory/`) to read. Where it and this skill disagree, the newer dated line wins.

# Copy edit: the final polish on sales copy

**STATUS: v1, 2026-09-30.** Built from the first run on 2026-09-29: the "Abs By AI sales
letter: AI Got Me Abs at 40" doc (`1zCLn6pIuxGv4H1hkyieCk2T4NoYAQBnaNKMEFMcYV9o`).
46 suggested changes; Dan accepted 37 as written and rejected or re-edited 9. His verdict:
"overall, these edits were excellent." The DO and DON'T lists below are those 46 decisions.
Every future run adds its accept/reject tally to the calibration log at the bottom.

## What this skill is, and is not

- **It is** the last pass before copy ships: spelling, grammar, consistency, tightening,
  factual consistency with the VSL and with Dan's real story, and the claims rules on record.
- **It is not** a rewrite. The marketing message, the argument order, the section structure,
  the offer, the price, the hooks and the CTAs stay exactly as Dan has them. If a whole
  section reads weak, that is a note in the chat report, never a suggested rewrite.
- **Every change is a suggestion.** Dan accepts or rejects each one himself. Nothing is ever
  typed straight into the doc in Editing mode. He explicitly wants to review each change.

**Model + effort:** Opus 5.5, high (updated 2026-10-06 to Dan's 2026-10-02 routing in `AGENTS.md`
and memory `model-routing-plan`: Opus is the default for all writing, ship-critical copy included).
Fable 5.1 is an escalation only, for a one-off second opinion where a rewrite costs a filming day.

## Process

1. **Read the doc and its sources before touching anything.** Pull the doc text with the
   Drive connector (`read_file_content`). Then read whatever the copy was adapted from, so
   the edit matches the language Dan already approved:
   - the long VSL, "AI Got Me Abs at Forty": `1lHzTMJydS7CBH3yigTYDDv1g3z9AJMcqwaPNyyKcIVc`
     (Version A body, Version B "fired them all" intro, and the appendix teleprompter copy)
   - the /start VSL (hero + full cut): `1DL2V34wePN75m1XxAuhpC2nghvobgr4C9RnTyszqqlA`
   - the doc's own header usually names its source ("Adapted from VSL Version A")
2. **Read the rules on record** (all short): memories `ad-suspension-prevention`,
   `ad-copy-no-unbelievable-claims`, `thumbnail-no-claims`, `no-ad-agency-mention`,
   `dan-personal-facts-for-scripts`, `no-em-dashes`, `swearing-never-cut-never-ask`; the
   "Product claims you can make" section of `/scriptwriting` SKILL.md.
3. **Plan every edit offline first**, as a table of exact `find` → `replace` pairs in the
   scratchpad. Copy the `find` string character for character from the Drive export: the
   doc mixes curly (’) and straight (') apostrophes by section, and a mismatch finds nothing.
   Each pair is one sentence or less. Never plan a change that touches a heading's meaning,
   a price, a CTA, or a bracketed layout note (except to fix a typo inside it).
4. **Open the doc in Chrome** (the Claude in Chrome extension, Dan's logged-in Google
   session), switch the mode control (top right, reads "Editing") to **Suggesting**, and
   zoom in on the control to read the word "Suggesting" before doing anything else.
5. **Make ONE test replacement and prove it landed as a suggestion**: green inserted text,
   old text struck through, and a suggestion card under Dan's name with accept/reject.
   Only then run the rest. Dan asked for this confirmation explicitly.
6. **Run the edits through Find and replace** (mechanics and traps below). After each
   batch, re-read the doc with the Drive connector: the export shows every pending
   suggestion as new text immediately followed by the old text, so a missing pair means a
   replacement did not take.
7. **Report in chat** (format below). Leave the Chrome tab open on the doc.

## DO: the changes Dan accepted (37 of 37 in this category)

Fix these every time, without asking.

- **Typos and dropped words.** "Believe it not" → "Believe it or not". "plan just you" →
  "plan just for you". "getting shape" → "getting in shape". "Woop" → "Whoop".
- **Brand and offer consistency across the whole doc.** "Abs by AI" → "Abs By AI".
  "Cancel any time" → "Cancel anytime" everywhere (the trial card and the VSL on-screen line
  say ANYTIME). "7 Day Trial Membership" → "7-Day Trial". "$1000/month" → "$1000 a month"
  when the next paragraph already says "a month". Bullet labels in one case
  ("A Personalized" → "A personalized" when the other bullets are lower-case).
- **Tense and sequence logic.** A heading in the present tense inside a past-tense story:
  "Why Aren't I Using…" → "Why Wasn't I Using…". "First… Next… And finally" → "First…
  Second… And finally". "can AI do" → "could AI do" to match the surrounding "Could AI".
- **Redundancy and filler.** Drop "literally", "also… to", "that" as a
  determiner-heavy connective ("the five ways that it'll help you to finally" → "the five
  ways it'll help you finally"), "as I gained fat" after "as I gained fat" was already the
  point, "I wanted to create something that would be simple for me to use" → "Something
  simple to use". Two sentences that say one thing become one.
- **Awkward phrasing.** "Does it seem like… that making the time… seems nearly
  impossible?" → "Does it feel like… that making time… is nearly impossible?". "That's the
  way that MOST" → "That's how MOST". "can AI do my personal trainer's job better than a
  human trainer?" → "could AI do a better job than my personal trainer?". "in dozens of
  small ways" where "in" was missing.
- **Established compound modifiers get their hyphen:** old-fashioned, all-in-one,
  out-of-shape, easy-to-make. (See DON'T for the one he rejected.)
- **Four-dot ellipses** ("me….to") → the single ellipsis character he uses everywhere else.
- **Facts pulled into line with the VSL and his real story.** "combining multiple different
  frontier AI models" → "combining five different frontier AI models" (the VSL number).
  "After my daily workout, I dedicated my day" → "After my morning workout, I spent the rest
  of the day" (he trains at 8 am; memory `dan-personal-facts-for-scripts`). "One was good
  at" → "One was great at" (VSL wording).
- **VSL phrasing where the letter paraphrases the VSL badly.** "I'll walk you through Abs by
  AI" → "Let me walk you through Abs By AI". The sleep section that opened mid-thought got
  the VSL's opener in front of it ("AI improved my sleep. And once you've got your sleep
  locked in…"). He accepted the structure and then re-worded it himself, so treat VSL
  language as the anchor, not as text to paste over his.
- **Claims rules on record** (the section below). All seven claims edits were accepted:
  "Get Real Six Pack Abs" → "Get Six Pack Abs"; "Thousands of men have used it to get the
  body of their dreams" → "It got me abs at 40, and now you can try it for yourself";
  "ensuring that everyone who tried the app got incredible results" → "beta testing it with
  real guys and fixing everything they ran into"; "instantly and accurately track" →
  "instantly track"; "to make your goal picture a reality" → "built to close the gap
  between your current picture and your goal picture"; "I guarantee these are going to
  surprise you" → "I promise these are going to surprise you"; "the world's ultimate" →
  "the ultimate".
- **Sentence-level tightening that keeps every idea.** "Our videos literally taught millions
  of men to get abs. In my twenties, I devoted my life to fitness. And as a result of this
  obsessive focus, I was able to get in the best shape of my life up until that point." →
  "Our videos taught millions of men how to get abs. In my twenties, I devoted my life to
  fitness, and I got in the best shape of my life up to that point." "It took me from having
  a soft and flabby dad bod at 38, to having the abs I always wanted at 40." → "It took me
  from a soft, flabby dad bod at 38 to the abs I always wanted at 40."

## DON'T: the changes Dan rejected or re-edited (9)

These are the line. A change in one of these categories is not a copy edit; leave it.

1. **Don't rewrite a feature description to match how the app works under the hood.**
   "Integrates with your sleep tracker data from Oura Ring, Whoop, and Apple Watch" was
   rewritten to "Just upload your sleep data…" because the app takes a screenshot. Rejected.
   He fixed the spelling of Whoop himself and kept "Integrates". The mechanism wording is
   marketing message.
2. **Don't swap his sentence for the VSL sentence when his is fine.** "This was me just a
   few years ago." → "This was me at 38. Two hundred pounds." Rejected. The VSL is the
   reference for facts and for wording he has already approved, not a source of
   replacement lines.
3. **Don't "correct" his framing words.** "In today's video and article" → "In the video
   above and the letter below". Rejected. He is happy calling the letter an article.
4. **Don't add grammar he deliberately drops in speech.** "I saw firsthand the technology
   lived up to the hype" → "…firsthand that the technology…". Rejected. Dropped "that" is
   his spoken register.
5. **Don't hyphenate loose comparatives.** "worse tasting meals" → "worse-tasting meals".
   Rejected. Hyphenate the established compounds in the DO list; leave ad-hoc pairs alone.
6. **The AI coach is "he" and "his".** "my AI coach in his own app" → "its own app".
   Rejected. Dan personifies the coach on purpose. Never neuter it.
7. **Never soften his social proof about real people he knows.** "they got incredible
   results" → "they started getting results". Rejected, and he then ADDED a stronger line
   ("Multiple guys I knew lost their belly fat…"). The claims rule removes invented
   numbers ("thousands of men"), not his first-hand statements about friends and clients.
8. **Don't cut a doubled adjective he wrote for weight.** "it was difficult and complicated
   to use" → "it was complicated to use". He accepted "Second" for the sequence fix and put
   "difficult and" back. Trim filler, not emphasis.
9. **Don't convert his parenthetical notes into bracketed notes.** "(Change when the stores
   list the app.)" → "[CLAUDE: change this line…]". Rejected. A note in his format stays in
   his format.

Two things he changed on his own in the same pass, worth knowing (one data point each,
not rules yet): "you'll be SHOCKED" became "you won't believe" (he keeps caps for
emphasis elsewhere: HARDER, FAR, HUGE, NOTHING), and "five AI hacks" became "five AI
techniques" / "five AI tactics" in body copy while the "AI Hack #1" headings stayed.

## Claims rules on record (apply, briefly; this is shipping sales copy)

- **Never promise a body.** No "get real abs", "make it real" as a promise, "make your goal
  picture a reality". The product sells the visualization, the numbers and the plan.
  Dan's own history in the first person is fine ("How I Got Abs At 40", "It got me abs at
  40"). A closing line he took from the VSL ("Then Let AI Help You Make It Real") is his
  call: flag it in the report once, do not suggest against it.
- **No invented social proof.** 75 people had ever completed a generation (2026-09-10).
  Never "thousands", never "everyone got incredible results", never "the world's".
- **Estimates, not measurements.** Photo calorie tracking and body-fat numbers are
  estimates: no "accurately", no "precise".
- **"Promise" over "guarantee"** for anything that is not the trial terms.
- **No drug names, no disease names, no shaming words, no before/after framed as real.**
- **Never say he was a marketer or ran an ad agency.** AI "coded my website, did my
  accounting" is the approved shape (memory `no-ad-agency-mention`).
- **The AI-disclosure line stays where it is**, above the fold or in the offer card.
- **Trial terms always complete:** free days, price, "until you cancel", "cancel anytime in
  two taps". Do not add a claim about an email the system may not send.

## Dan's voice (protect it)

> **Voice method changed 2026-10-10 (Dan Voice P2B; `_shared/DAN-VOICE.md`).** This skill decides WHAT the piece
> says: build the content plan here (points, facts, numbers, order, the ask, length, Dan's own outline wording word
> for word). The sentences are then drafted by the **`dan-voice-writer`** agent, in a clean call that sees only real
> passages of his. Do not draft the words in this session from the voice rules below, and do not polish what the
> writer returns: on the blind bench, rules in the writer's context made Claude easier to catch (92% against 82%).
> The voice rules below remain as background for the content plan and for the final read. Format, length, cue and
> offer rules in this skill still apply in full.

The full guide is `.claude/skills/_shared/DAN-VOICE.md` (with `_shared/voice/sales.md` for letters and VSLs).
Read it before deciding a line is "off voice": lines that look rough (ellipsis beats, a capitalized word, a run-on
sentence, "Listen -") are usually his. The short version:

Short sentences. One-line paragraphs. Ellipses as beats ("How did I do it?…"). ALL CAPS
for a single stressed word. "Guys like us", "regular guys", "dad bod", "slammed",
"stressed out as hell". Dropped "that". The coach is "he". Swearing stays (memory
`swearing-never-cut-never-ask`). Numbers as he writes them ("$1000", "38", "40"). No em
dashes anywhere in anything you write; his hyphen-with-spaces (" - ") is his own device
and stays where he has it.

## Mechanics: suggestions through the Docs connector (first choice since 2026-10-10)

The Docs connector's `update_doc` now makes real tracked suggestions: `writeControl: {"writeMode": "SUGGEST"}`. No
Chrome, no Find and replace, and each edit is its own card. Used on the 10/17 shoot doc: 90 suggestions in five calls.

1. `read_doc` saves the doc as JSON. Write the edits as `ops = [(section, old, new), ...]` in a .py file.
2. `python3 .claude/skills/scriptfromoutline/references/gdoc_edits/suggest_builder.py doc.json ops --show`. It cuts
   each edit down to the words that differ, refuses an `old` that does not match exactly once in its script, and prints
   the request batches. Fix every ERROR before sending.
3. Send two or three ops alone first with `requiredRevisionId` set to the revision it printed. `read_doc` again and run
   `verify_suggestions.py before.json after.json`: the count must match, and "reject-all view equals the doc before"
   must be True. Rebuild the rest from that fresh read with `--skip`.
4. Send the batches highest index first, each with the revision id the last call returned. If a call fails on the
   revision id, Dan is typing in the doc: read it again and rebuild.
5. Verify again with the ops file as the third argument, and save the list as `Docs/COPYEDIT_<doc>_AS_DELIVERED_<date>.md`.

Traps: text Dan typed has curly apostrophes and the builder keeps them. A missing space after a period may be a soft
line break he typed (it shows as `\x0b` in the JSON): look before "fixing" it. Paragraph breaks and moved lines are
not worth a suggestion; name them in the chat report.

## Polishing scripts, not sales copy (first run 2026-10-10, his verdict pending)

A filming script is spoken, and most of it has already been through his hands. So:

- **Find out whose line it is first.** Curly apostrophes are his typing. In his lines fix only a typo, a dropped
  word, a missing period or a misspelled name. Leave his loose grammar ("Here's the 9 exercises").
- **Change a Claude line only for a tell his own lines do not share.** Count the phrase in his typing and in the
  rest of the same doc before touching it. On the 10/17 doc: "every single" 0 in his lines against 14, "I've got" and
  "you've got" 1 against 14, so those went to "every" and "I have". "Here's", "actually", "exactly" and "right now"
  ran at his rate or below it, so they stayed.
- **Put a fragment back into a sentence** ("No food." "Too hard? Do them from your knees." "Same wake up, same
  workout."), and turn a colon reveal ("Here's what most guys don't realize:") into the plain statement.
- **Do not smooth, vary or tighten.** That is what gets a draft caught (`_shared/DAN-VOICE.md`). No new sentences.
- Hooks, facts, numbers, cues, the order and anything he rejected in an earlier round are not touched.

## Mechanics: Google Docs suggestions from Chrome (fallback)

Use this only when the Docs connector is not connected.

- **Suggesting mode:** click the mode control at the top right of the toolbar ("Editing"),
  choose "Suggesting", zoom on the control and read the word before any edit.
- **Every edit goes through Find and replace.** In Suggesting mode each Replace becomes a
  suggestion with its own accept/reject card, and "Replace all" makes one grouped card.
  Per edit: click the Find field, cmd+a, type the find string, wait a second, zoom on the
  counter and confirm "1 of 1" (or the expected count), click the Replace field, cmd+a,
  type the replacement, click Replace. Six to eight edits per browser batch is stable.
- **Open the dialog from the Edit menu, then confirm it is open before typing.** The
  cmd+shift+h shortcut fails silently when focus is not in the document body. On the first
  run it failed once, so the next "click Find field, cmd+a, type" landed in the doc:
  cmd+a selected the ENTIRE document and the typed text replaced it (as a suggestion).
  Recovered with cmd+z, one step at a time, clicking into the doc body before each undo
  because focus drifts to the suggestion card. Never batch a cmd+a after an unverified
  dialog open. Never type into the doc body except for the single case below.
- **Paragraph breaks** cannot be made through Find and replace. Find the text that should
  end the paragraph, close the dialog with its X (the match stays selected), press Right,
  then Return. Verify with a screenshot.
- **Find ignores suggested-deleted text**, so after a replacement the counter shows 0 of 0
  for the old string; use that as confirmation.
- **Case-only replacements register** ("A Personalized" → "A personalized").
- **Literal asterisks in the Drive export are formatting escapes**, not characters in the
  doc. Search for `**` before assuming a typo.
- **Verification** is the Drive export: each pending suggestion appears as
  `new textold text` back to back. Count them against the plan.

## The chat report

Dan does not see the tool calls. The report is what he reads before opening the doc.

1. Confirm Suggesting mode was verified with the test change before the run.
2. The count: changes made, suggestion cards (Replace all groups), none edited directly.
3. Three short groups with two or three examples each: claims rules applied, typos and
   inconsistencies, tightening in his VSL language. State that no em dashes were introduced.
4. "Left alone for your call": at most three items, one line each (a VSL line the claims
   rule would flag, a placeholder still in the doc, an unverifiable story). Never a
   compliance lecture.
5. Anything that went wrong and how it was recovered, in one line. He would rather hear it.
6. The doc link, and where the suggestion cards are (right margin, or Tools > Review
   suggested edits).

## Calibration log

| Date | Doc | Changes | Accepted | Rejected / re-edited | What moved into the rules |
|---|---|---|---|---|---|
| 2026-09-29 | Sales letter: AI Got Me Abs at 40 (draft v1) | 46 | 37 | 9 | DON'T 1 to 9 above; the seven claims edits confirmed |
| 2026-10-10 | 10/17 shoot doc, 43 filming scripts (`1gt8Fi_wUaNaksa8sAdMoBvcdlBhZLek82EpBr-leq-0`) | 90 | pending | pending | List: `Docs/COPYEDIT_1017_SHOOT_POLISH_AS_DELIVERED_20261010.md`. Next session: read the doc, count, fill this row, move rejections into DON'T |

After every run: add a row, and if a rejection reveals a new category, add it to DON'T with
the before and after text. Three rejections of the same kind become a rule; one is a note.
