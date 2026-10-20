---
name: copy-edit
description: >
  Final polish pass on finished copy before it goes into production: a sales
  letter, a landing page, a VSL or ad teleprompter script, a sales email, or the
  filming scripts in a shoot doc. Fixes typos and inconsistencies, removes
  AI-sounding wording, applies the claims rules on record and keeps Dan's voice.
  Edits Dan is sure to accept go straight into the Google Doc; only the uncertain
  ones are tracked as suggestions for him to review. It never changes the marketing
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

**v2, 2026-10-11.** Second run: 90 suggestions on the 43 filming scripts of the 10/17 shoot doc. Dan accepted 81 as
written, rejected 6 and rewrote 3, then changed how edits are delivered: the ones he is sure to accept go straight
into the doc, and only the uncertain ones are tracked. Start at "Straight in, or tracked".

## What this skill is, and is not

- **It is** the last pass before copy ships: spelling, grammar, consistency, tightening,
  factual consistency with the VSL and with Dan's real story, and the claims rules on record.
- **It is not** a rewrite. The marketing message, the argument order, the section structure,
  the offer, the price, the hooks and the CTAs stay exactly as Dan has them. If a whole
  section reads weak, that is a note in the chat report, never a suggested rewrite.
- **Most edits go straight into the doc. Only the uncertain ones are tracked** (Dan, 2026-10-11; this
  replaces "every change is a suggestion" from 2026-09-29). The two lists are in the next section.

## Straight in, or tracked (Dan, 2026-10-11). READ FIRST.

Dan, after ruling on 90 suggestions: "all the edits that you're highly confident that I will accept are just made
into the document. The only ones you are putting into track changes in Google Docs for me to review are ones where
you're not certain whether or not I'll accept it."

**Straight into the doc, no review:**

- Spelling, names, capitalization and punctuation: a missing period, a comma in a run-on, a missing space,
  "1.5mg" to "1.5 mg", "Brian Johnson" to "Bryan Johnson".
- Any edit to a filming direction: bracketed cues, on-screen text, B-roll and shot lists, header notes, word counts.
  His test: "anything that does not substantially change what I'm reading off the teleprompter".
- A sentence that does not parse without the fix: a dropped word, a doubled word, the wrong form of a word ("safer
  are more effective", "this gradually approach", "show you them", "realized out that AI was the going to").
- A swap he has accepted every time. On record: "every single" to "every" (12 of 12). A padding word that
  appears twice in one sentence loses one.
- A fact or number brought into line with the same script (the cue says "about 200", the line says "over 200").
- The mechanical result of an instruction he gave: renumbering after he adds or removes an item, a title he dictated.

**Tracked, for him to review:**

- Any rewording of a sentence he reads, however likely: a fragment put back into a sentence, a colon reveal made
  plain, a kicker cut. He accepted 18 of 19 on 2026-10-10, but each one is new wording, and three times he kept the
  idea and wrote his own words.
- A category with a mixed record: two short sentences merged into one (5 of 7), "I've got" and "you've got" to
  "I have" and "you have" (9 of 11).
- A new kind of edit, a new spoken line, a spoken line cut.
- In sales copy, every claims edit.

**Never** (he rejected each one): DON'T 10 to 12.

**Moving a category between the lists.** After each run read the doc, count, and fill the calibration log. A tracked
category he has accepted every time over 10 or more decisions moves to the straight-in list with its count. A
straight-in edit he changes back moves that category to tracked; a second one makes it a DON'T. When it is not
clear which list an edit belongs on, track it.

**Reaffirmed 2026-10-13, after a run that tracked everything.** Mid-run he said "make sure you're using the track
changes feature... so I can review all these edits", and the five spelling and capitalization fixes were tracked
along with the cuts. Afterwards: "only changes you're not sure whether or not to accept need to be done with track
changes. Things like correcting a spelling error, capitalization, or things like that should be made directly in the
document... so that I don't spend time reviewing them going forward." So a request to use track changes covers the
edits that need his judgment. Spelling, obvious grammar and obvious capitalization still go straight in.

**A direct edit is still checked and still recorded.** After the send, diff the whole doc against the read taken
before it (`verify_suggestions.py --diff`): every changed line must be one that was planned. Both lists go in the
as-delivered file so the next session can see what he changed back.

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
   Mark each edit direct or track (section above). **Steps 4 to 6 are the Chrome fallback; with the Docs connector
   follow "Mechanics: edits through the Docs connector" instead.**
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

## When the scripts are final: make the filming documents (Dan, 2026-10-11). Always, without being asked.

Dan: "When we finalize everything, going forward, let's always upload teleprompter documents." A polish pass on
filming scripts is not finished at the last tracked suggestion. It is finished when the documents he films from
exist. "Final" means he has ruled on every tracked suggestion (none pending in the doc) and has said the scripts are
good, or has asked for the filming documents. Then do all of this in the same session:

1. **One teleprompter document per filming set**, words only, built with `/teleprompterscripts` (section v3). The
   sets so far: dark green backdrop, green screen, outside. Ask which set a script is on only if it is not clear.
2. **No teleprompter script over 50 pages.** A set longer than that is split in two (the build script does it at a
   script boundary). Count the real pages after upload.
3. **Upload each teleprompter document into PromptSmart** (`my.promptsmart.com/scripts`, his Chrome, he is logged
   in). Steps in `/teleprompterscripts`.
4. **A separate B-roll list**, bullets by set, saved in Google Drive only. It is never put in PromptSmart.
5. **If any script reacts to a clip: a reaction clip list**, each link opening at the clip's start time, Drive only
   (Dan asked for one on 2026-10-12; steps in `/teleprompterscripts`).
6. The polished shoot doc stays as it is: it is the editing copy, with every graphic and cue in place.
7. Report the links, the page counts, and which script went on which set.

## Mechanics: edits through the Docs connector (first choice since 2026-10-10)

The Docs connector's `update_doc` writes both kinds: `"writeMode": "EDIT"` types the change in, `"writeMode":
"SUGGEST"` makes a tracked suggestion with its own card. No Chrome and no Find and replace. Tools:
`.claude/skills/scriptfromoutline/references/gdoc_edits/`.

1. `read_doc` saves the doc as JSON. Write the edits in a .py file as `ops = [(section, old, new, 'direct'),
   (section, old, new, 'track'), ...]`.
2. `python3 suggest_builder.py doc.json ops --only direct --show`. It cuts each edit down to the words that differ
   and refuses an `old` that does not match exactly once in its script. Fix every ERROR, read the list, then send
   the batch with `{"writeMode": "EDIT", "targetRevisionId": <the REVISION it printed>}`.
3. `read_doc` again and run `verify_suggestions.py before.json after.json --diff`. Read every changed line.
4. `suggest_builder.py after.json ops --only track`, built from that fresh read, sent with
   `{"writeMode": "SUGGEST", "targetRevisionId": <its REVISION>}`.
5. `read_doc` and verify once more (after a tracked send, "reject-all view equals the doc before" must be True).
   Save both lists as `Docs/COPYEDIT_<doc>_AS_DELIVERED_<date>.md`.

Traps:
- **Dan is often in the doc while this runs.** `targetRevisionId` makes the doc merge the edit with whatever he
  typed since the read, so nothing of his is overwritten. `requiredRevisionId` fails the whole call instead. Send
  within a minute or two of the read, and never send with no revision id at all: stale offsets land in the wrong place.
- Text Dan typed has curly apostrophes and the builder keeps them.
- A missing space after a period may be a soft line break he typed (`\x0b` in the JSON): look before "fixing" it.
- A paragraph inserted as a suggestion is one card however long it is. Inserted text takes the format of the
  character before it. A moved line is not worth an edit; name it in the chat report.

## Polishing scripts, not sales copy (first run 2026-10-10: 81 of 90 accepted)

A filming script is spoken, and most of it has already been through his hands. So:

- **Find out whose line it is first.** Curly apostrophes are his typing. In his lines fix only what is on the
  straight-in list: a typo, a dropped word, a missing period, a misspelled name. Leave his loose grammar ("Here's
  the 9 exercises"), his conjunctions and his missing articles (DON'T 11).
- **Change a Claude line only for a tell his own lines do not share.** Count the phrase in his typing and in the
  rest of the same doc before touching it. On the 10/17 doc: "every single" 0 in his lines against 14, "I've got" and
  "you've got" 1 against 14, so those went to "every" and "I have". "Here's", "actually", "exactly" and "right now"
  ran at his rate or below it, so they stayed.
- **Put a fragment back into a sentence** ("No food." "Too hard? Do them from your knees." "Same wake up, same
  workout."), and turn a colon reveal ("Here's what most guys don't realize:") into the plain statement. All
  accepted, all tracked (new wording).
- **Do not smooth, vary or tighten.** That is what gets a draft caught (`_shared/DAN-VOICE.md`). No new sentences.
- Hooks, facts, numbers, the order and anything he rejected in an earlier round are not touched.

DON'T, from his 6 rejections and 3 rewrites (numbering continues the list above):

10. **Don't touch a hook he has left in place, even one Claude wrote.** "Some celebrities on Ozempic look
    incredible. Others look sick. The difference isn't the drug. It's what they did while they were on it." was
    offered as one plain sentence and he kept the original. He rewrites the hooks he wants changed himself.
11. **Don't change the small words in a line he typed.** "But it can be hard to lose your love handles" to "And it
    can be hard..." and "during commercial breaks of a football game" to "during the commercial breaks..." were
    both rejected.
12. **Don't fold a short tag sentence into the one before it.** "...and 1 ab exercise. 3 sets of each." and "At 25%,
    your belly still sticks out in a shirt. You don't have muscle definition anywhere." stayed as two sentences.
    Other merges were accepted, which is why a merge is always tracked and never typed in.

## Cutting a script to length (first run 2026-10-13: 22 of 29 cuts accepted)

Dan asked for the 19 reaction shorts to be cut to 66 seconds with the clip. Whole sentences only, every cut tracked.

- **A leftover draft line that repeats a paragraph he wrote: cut it.** 9 of 9 accepted (straight apostrophes mark
  the draft, curly ones his typing).
- **His own lines: 13 of 20 accepted, 2 replaced by a shorter line of his, 5 put back.** What he put back:
  - short emphasis tags he had just typed ("And you should too." "As in, you should start them right now." "That's
    hard for a lot of people to believe."). Same family as DON'T 8 and 12: they are weight, not filler.
  - the instruction said again at the close ("Just up your Zepbound dose, and you can lose all the weight you want.").
    That is the takeaway, not a restatement.
  - the other half of a contrast ("If you're not fasting, then you'll probably have to eat a small, low calorie dinner").
- **What he cut himself to make room:** a study statistic (the finasteride numbers) and a proof-by-crowd line ("Terry
  Crews does it, I do it, and literally millions of other men are doing it too"). He gives up outside proof before
  his own instruction or emphasis. So cut a quoted study or a second proof before a line that tells the viewer what
  to do. His own numbers (doses, pounds, days) stay.
- **A cut that removes a payoff he wants comes back shorter, in his words.** "And at the same time, you'll actually be
  training a deep ab muscle that makes your belly bulge out less." became "And vacuums will actually make your belly
  bulge out less." Offer the cut and expect this; never write the short version for him.
- **The sentences he typed in his most recent pass are the last to cut.** All five he put back were from the edit he
  made that afternoon.
- **He may leave a script over the limit on purpose.** After his rulings three ran 68 to 72 seconds. Re-count, give
  him the list once, and do not cut again unasked.
- Tool for the sends: a plan of `('sent' | 'para', script, text)` cuts turned into `deleteContentRange` requests,
  highest index first, sent in one call with `writeMode: SUGGEST` and `targetRevisionId`. A whole paragraph takes the
  blank line after it. Verify with `verify_suggestions.py` and re-count the accept-all view.

When he agrees a line is off but the fix needs new words, he tends to write his own: "for almost none of his money"
was offered as "for almost no money" and became "without spending anything"; "Let's start with abs. I have three."
became "Let's start with my three favorite ab exercises." Offer the plainest version and expect it to change.

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

1. The two counts: how many edits went straight in, and how many are tracked for him. Say the direct edits were
   checked with a before and after diff of the whole doc.
2. What is tracked and why it needs his eye, in one line per kind.
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
| 2026-10-10 | 10/17 shoot doc, 43 filming scripts (`1gt8Fi_wUaNaksa8sAdMoBvcdlBhZLek82EpBr-leq-0`) | 90 | 81 | 6 rejected, 3 rewritten | DON'T 10 to 12; the straight-in and tracked lists. List and result: `Docs/COPYEDIT_1017_SHOOT_POLISH_AS_DELIVERED_20261010.md` |
| 2026-10-11 | Same doc, "10 Exercises" script rewrite (first run under straight in or tracked) | 46 direct, 5 tracked | pending | pending | `Docs/SCRIPT_10_EXERCISES_REWRITE_AS_DELIVERED_20261011.md`. Next session: read the doc, see what he changed back, fill this row |
| 2026-10-13 | Teleprompter 2, 19 reaction shorts (`1KvL0_IilRCxlofnY5luTfRvjiseGGpGGXU4sAsjbgzQ`): cut to 66 s with the clip | 0 direct, 34 tracked (29 whole-sentence cuts, 5 one-word fixes) | 22 cuts and all 5 fixes | 5 cuts rejected, 2 cuts replaced by a shorter line of his own | "Cutting a script to length" below; simple fixes are never tracked, whatever else is. `Docs/COPYEDIT_1017_REACTION_SHORTS_66S_AS_DELIVERED_20261013.md` |
| 2026-10-14 | Teleprompter 3, 11 outdoor shorts (`1yc2xg1sG4lTncvcAmkA17SN-JZnQSsbB9Q-fpEbXotg`), all still Claude's draft | 7 direct (hyphens, "every single"), 9 tracked (4 merges, 5 repeat-sentence cuts) | 7 as written, plus 1 rewritten in his words ("sit down with good posture") | 1 rejected: cutting the tricep closer that repeats the opener | `Docs/COPYEDIT_1017_OUTDOOR_SHORTS_AS_DELIVERED_20261014.md`. Next session: read his rulings, fill this row |
| 2026-10-18 and 10-19 | Gym Shorts Scripts, 27 shorts for the 10/23 pool shoot (`11nUmri621xbb7K44Wxan7IAljK2mJeizDFCRgK752AA`), after Dan's own edit pass | 48 direct (typos, hyphens, word counts, filming lines matched to his rewrites), 4 tracked (2 repeat-sentence cuts, 1 more cut, 1 "First," fix) | pending | pending | Opener lessons went to `_shared/HOOKS.md` (he rewrote 23 of 26 openers). Two soft line breaks of his looked like missing spaces: left alone. `Docs/COPYEDIT_GYM_SHORTS_1023_AS_DELIVERED_20261018.md`, `..._20261019.md`. Next session: read his rulings, fill this row |
| 2026-10-20 | Same doc, the seven 10/23 pool long-forms, after Dan's 10/20 line edits (Fable 5.1) | 29 direct (13 "every single", 5 hyphens, 1 period, the leg-press count and two cues matched to his edits, 7 word counts), 5 tracked (3 repeat-sentence cuts, 2 double-introduction fixes) | pending | pending | "I've got" left alone: his own 10/20 line uses "you've still got", so the tell is his here too; count his lines before swapping. `Docs/COPYEDIT_POOL_LONGFORMS_1023_AS_DELIVERED_20261020.md`. Next session: read his rulings, fill this row |

After every run: add a row, and if a rejection reveals a new category, add it to DON'T with
the before and after text. Three rejections of the same kind become a rule; one is a note.
