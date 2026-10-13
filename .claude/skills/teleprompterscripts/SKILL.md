---
name: teleprompterscripts
description: >
  Produce a clean teleprompter-only copy of a finalized scripts Google Doc — strip
  every filming direction, bracketed cue, image, asset caption, per-ad note and
  production-notes section, leaving nothing but the words Dan reads on camera.
  Use whenever Dan asks for a "teleprompter version", a "clean copy for the
  teleprompter", a copy "with the filming notes removed", or to get a scripts doc
  ready for his editor to load into a teleprompter app — even if he doesn't say
  "/teleprompterscripts". Writing the script itself is /scriptwriting; placing the
  images and clips is /imagesandclips.
---

> **Shared writing rules (2026-10-06):** before writing, read `.claude/skills/_shared/WRITING-RULES.md`. It holds the rules every writing skill follows and the list of memory entries (`Docs/memory/`) to read. Where it and this skill disagree, the newer dated line wins.

# Teleprompter-only copy of a finalized scripts doc

**STATUS: v2 — 2026-08-26, second run: the Shoot 5 doc
("Abs By AI Shoot 5 … - FILMING SCRIPTS FOR EDITOR" → "Abs By AI Shoot 5 - TELEPROMPTER ONLY").
v1 was 2026-08-11, the batch-1 ad run.**

## The one rule that outranks everything else

**NEVER open, edit, or delete anything in the source document.** That doc is the
editor's working copy — it carries the filming directions, the placed images, the
clip filenames and timecodes, and the per-ad compliance notes. Losing it costs
several sessions of work.

The safe method is **not** "make a copy, then delete things out of it." It is
**build a brand-new document containing only the spoken words.** The source is
never opened in the Docs editor at all, so there is no undo stack to get wrong
and no way to damage it. Dan approved this substitution on the batch-1 run;
the end result is identical and it is far more reliable than driving the editor
to delete 200+ blocks.

**Prove the source is untouched** at the end by re-reading its metadata and
confirming `fileSize` is unchanged.

## Dan's settled preferences (batch-1 run, do not re-ask)

- **Ad titles stay** as Heading 2, so the doc outline lets the editor jump to a
  script. Everything else above the spoken words goes.
- **One document, all ads** — not one doc per ad.
- **Plain formatting** — black body text, no bold, no italics, no colour, normal
  size. Teleprompter apps set their own font and size; styling in the doc is noise.
- **Runtime / word-count lines get stripped** ("~610 spoken words ≈ 3:45–4:15").

## What gets stripped

Everything except ad headings and spoken paragraphs:

| Element | Looks like |
|---|---|
| Doc title + intro instruction line | "Spoken words are in regular text — read these…" |
| Runtime line under each title | `~610 spoken words ≈ 3:45–4:15 at normal pace.` |
| Bracketed cues (bold **and** plain) | `**[SKIP STOPPER — OPEN TIGHT ON POSTER]**`, `[END BEFORE PICTURE]` |
| `[END]` markers | `**[END]**` |
| Images | every embedded image |
| Asset captions under images | `Clip: ai-clip-crude-photoshop.mp4 — USE THE FULL 5s… <drive url>` |
| Caption fragments with no marker | `Real app — a workout day: …`, `The pool frame from the shoot — pool visible behind him.`, `LEFT = the warning picture…`, `Goal image alone, AI-GENERATED tag on.` |
| Per-ad notes | `Ad 8 note: this is the ONLY ad in the batch that needs a new asset…` |
| Production notes section | the whole trailing `## Production notes` block |

## Procedure

### 1. Read the source doc

`read_file_content` on the Drive file id. It will exceed the token limit — the
tool saves the full JSON to a file. Extract `fileContent` to a text file with
python and work from that; don't try to read it into context.

### 2. Classify every paragraph in code, not by eye

Work on the markdown-ish text export, one non-empty line = one paragraph.
Rules that worked, in order:

1. `# ` → doc title, drop.
2. `## ` → ad heading, **keep**; unless it is `Production notes`, which switches
   on a "drop everything after this" flag.
3. Strip surrounding `*`/`**` and markdown escapes, then:
   - starts `[` **and** ends `]` → cue, drop. *(Catches both the bold and the
     plain cue styles — several ads use un-bolded cues.)*
   - matches `^Ad \d+ note:` → drop.
   - contains `spoken words` and starts `~` → runtime line, drop.
   - contains `drive.google.com` → asset caption, drop.
   - starts with a caption prefix → drop. The batch-1 set was:
     `Clip:` · `Goal image` · `Real app —` · `LEFT =` · `The bad` ·
     `The deliberately-bad` · `This is the RAW before picture` ·
     `The outdoor shoot frame` · `The pool frame from the shoot` · `Use the` ·
     `Image:` · `Photo:`
   - leading single `*` → stray italic note, drop.
4. Everything else → spoken, keep. Convert markdown links
   `[SixPackAbs.com](http://sixpackabs.com)` → plain `SixPackAbs.com`.

### 3. Two verification sweeps BEFORE building — both are load-bearing

Asset captions are the hard part: they are plain paragraphs with no marker, so
a prefix list is a guess until you check it.

- **Sweep A — every paragraph that directly follows a cue.** Print them all and
  read them. That is where captions live, and it is a short list (~200 lines).
  On the batch-1 run this surfaced 12 captions the first-pass rules missed.
- **Sweep B — every kept paragraph with no first/second-person pronoun.**
  Spoken copy is almost always "I/you/my/your/we". A paragraph with none of
  those is either a caption or a punchy one-liner; print them and eyeball.
  Batch 1 returned 9, all genuine lines ("One was a warning.", "...to this.").

Then a final assertion pass on the built output: zero bracketed cues, zero
`drive.google.com`, zero `.mp4`, zero `Ad N note`, zero `spoken words`,
zero `[END]`.

### 4. Build the HTML

One `<h2>` per ad, one `<p>` per spoken paragraph, with
`style="color:#000000;font-weight:normal;font-style:normal"` on every paragraph
so nothing inherits styling from the paste context. Put a page break before each
`<h2>` except the first:

```html
<p><br clear="all" style="page-break-before:always"></p>
```

### 5. Create an empty Google Doc, then paste into it

`create_file` with `contentMimeType: application/vnd.google-apps.document`, the
new title, and the **same `parentId` as the source** so it lands beside it.

**Do NOT try to pass the HTML through the create_file tool call.** Batch 1's HTML
was 78 KB / 104 KB base64 — retyping that into a tool call is both expensive and
a real corruption risk (a prior session silently corrupted a 14 KB base64 payload
by one byte). Put it on the clipboard from the local file instead, where nothing
is transcribed:

```bash
python3 -c "print(\"osascript -e 'set the clipboard to «data HTML%s»'\" % open('teleprompter.html','rb').read().hex())" > setclip.sh
bash setclip.sh && osascript -e 'clipboard info'   # expect: «class HTML», <bytes>
```

Then, **in this exact order** (the order is the whole trick):

1. Open the new doc in Chrome and **click into the empty body first.**
2. **Re-run `setclip.sh` now**, immediately before pasting.
3. `cmd+v` once.
4. **Screenshot.** Never assume the paste landed.

If Docs pastes something stale instead (its internal clipboard can win even when
`clipboard info` reports the correct HTML at the correct byte count), `cmd+z`
once, re-set the clipboard, click back into the body, and paste again. The doc is
brand-new and empty, so a bad paste here is harmless — that is another reason the
build-fresh method beats editing a copy.

### 6. Verify

Wait ~10 s for Docs to settle (the Drive text export is eventually consistent and
a read taken mid-sync can look wrong), then:

- `read_file_content` the new doc and assert the eight "zero" checks from step 3.
- Assert the **spoken paragraph sequence is identical** to what you built —
  normalize curly quotes and whitespace, then compare the lists element by
  element. Count parity alone is not enough. Batch 1: 374/374, exact match.
- Confirm the heading count equals the ad count. **Watch the numbering** — batch 1
  has 13 ads numbered up to AD 15 (there is no AD 11 or 12). Don't "fix" that.
- `get_file_metadata` on the **source** and confirm `fileSize` is unchanged.

## Lessons

- **The cue style is not consistent across ads.** Ads 1–8 mostly use
  `**\[CUE\]**`; later ads have plain `[SHOW BEFORE PICTURE]` paragraphs. A rule
  keyed on the bold markers alone silently leaves cues in the teleprompter text.
- **Captions are invisible to pattern matching.** `The pool frame from the shoot
  — pool visible behind him.` is a well-formed English sentence with no marker of
  any kind. Only Sweep A finds these. Budget for reading that list.
- **Sanity-check the number Dan says.** He asked for "all 15 scripts"; the doc
  holds 13, numbered 1–10 and 13–15. Report the real count rather than inventing
  two ads or silently disagreeing.
- **`clipboard info` returning the right flavour and byte count does not prove
  the paste will use it.** Screenshot after every paste. This trap has now fired
  in four separate sessions across three skills.


## Lessons added on the Shoot 5 run (2026-08-26)

- **A bold-only line is NOT reliably a title.** Long-form scripts carry bold
  *section* headers in exactly the same style as video titles
  (`**WRAP UP AND CTA**`, `**STRATEGY ONE: AUTOMATE IT WITH AI**`). A
  "whole line is bold ⇒ heading" rule promotes 10 of those to `<h2>`. **Match
  titles against an explicit list you enumerated by eye, and drop every other
  bold-only line** — those are section labels, not spoken, and not read aloud.
- **Three ad titles in the Shoot 5 doc are malformed in the export**
  (`**What's The Best Ab Exercise?****` on one line, a bare `****` on the next,
  then the first spoken line opening with an unclosed `**`). After the bold
  regex runs, `.strip('*')` the result and discard lines that are nothing but
  asterisks — otherwise those three titles silently fall through to the
  section-header rule and vanish.
- **Sweep B's yield scales with how ad-like the copy is.** 70 of 426 paragraphs
  had no first/second-person pronoun and every one was genuine spoken copy
  ("It's a picture.", "AI fixes all three.", "Here's how it works."). Read the
  list, but do not treat its size as a red flag the way batch 1's 9 suggested.
- **The clipboard trap fired again, on an empty brand-new doc.** First `cmd+v`
  did nothing at all — the doc stayed blank while `clipboard info` reported
  `«class HTML», 114490`. Fix that worked: clear the clipboard
  (`osascript -e 'set the clipboard to ""'`), re-set the HTML flavor, click into
  the body, paste. **That is five sessions across four skills now — always
  screenshot.**
- **Do not build from a fresh Drive read when you already have the content.**
  The Shoot 5 run built straight from the local markdown that had produced the
  source doc minutes earlier, so the source was never opened in the editor at
  all and `fileSize` was provably identical afterwards.


## v3, 2026-10-11: one doc per filming set, built from the Docs connector, uploaded without Chrome

Dan asked for three teleprompter docs from the 10/17 shoot doc (43 scripts): dark green backdrop, green screen, and
outside by the pool, plus a separate B-roll list. Result: 21, 18 and 4 scripts, every line identical to the source.

- **Build with `reference/tp_from_shoot_doc.py`.** It reads the saved `read_doc` JSON of the shoot doc, finds each
  script, drops the cues, sorts the scripts into sets and writes one HTML file per set. Edit `SETS` at the top for
  each shoot. The source doc is only read.
- **How Dan split the sets (2026-10-11).** Green screen: "all of the reaction videos and anything else you think
  would make sense on a green screen where there's extensive content behind me". Used: every reaction video and
  short, plus the three videos with a picture on screen most of the way through (Body Fat Percentage, Ab Ranking,
  Losing Fat Changed My Face). Outside: the follow-along workouts. Dark green backdrop: everything else.
- **A follow-along workout stays words only.** No round labels. A blank line is left where each round cue stood, so
  the rest scripts are apart on the prompter.
- **No Chrome: upload with rclone.** The clipboard paste takes over Dan's browser and has failed in five sessions.
  This does not touch his screen:

      ~/bin/rclone copy out_dir gdrive: --max-depth 1 --include "<prefix> - Teleprompter*.html" \
          --drive-import-formats html --drive-export-formats html --drive-pacer-min-sleep 2s
      ~/bin/rclone lsjson gdrive: --max-depth 1 --files-only --include "<prefix>*" --drive-export-formats html
      ~/bin/rclone link "gdrive:<file name>.html" --drive-export-formats html

  The first makes real Google Docs (headings, page breaks, nested bullets all convert). The second gives their IDs.
  The third turns on anyone-with-the-link viewing. Traps: both format flags are needed, or the upload fails with
  "can't convert .html to a document with a different export filetype"; no slash in the file name ("10-17", not
  "10/17"), rclone reads it as a folder; add `--drive-root-folder-id <id>` to land in a folder other than My Drive.
- **Verify by downloading back as text**, not by eye:
  `rclone copy gdrive: back --max-depth 1 --files-only --include "<prefix> - Teleprompter*" --drive-export-formats txt`,
  then compare each file line by line with `built_seq.json` (curly quotes and spaces normalized). 10-11: 518 of 518,
  345 of 345, 102 of 102. Then `get_file_metadata` on the source: `fileSize` and `modifiedTime` unchanged.
- **The B-roll list is its own doc**, bullets by set, in the order Dan films (he asked for outdoor first). Nested
  `<ul>` inside `<li>` imports as real nested bullets. Add what the Edit Queue is blocked on for B-roll:
  `Handoffs/video-editing/jobs.json`, `state` "blocked" with b-roll in `needs`.
- **The teleprompter copy matches the filming script word for word.** When Dan edits the shoot doc after the docs
  are made, rebuild and upload again with the same `rclone copy` plus `--ignore-times`. Tested 2026-10-12: it says
  "Copied (replaced existing)", the doc keeps its id and link, and no second file appears. List the folder anyway.
  In PromptSmart there is no replace: import the new file, check it, then use the old card's menu, Delete (it asks
  "Move to trash bin?", and it can be restored). Click the menu by `find` ref; a coordinate click missed it.
- **No teleprompter script over 50 pages (Dan, 2026-10-11).** "A maximum length of 50 pages per teleprompter
  script... If there's more than 50 pages on a single set, break it into two." The build script splits a set over
  25,000 words (about 45 pages) at a script boundary and names the parts "(Part 1 of 2)". Count the real pages after
  upload: export as PDF (`rclone copy gdrive: pdf --max-depth 1 --files-only --include "<prefix> - Teleprompter*"
  --drive-export-formats pdf`) and read the largest `/Count` in each file. 10-11: 22, 18 and 6 pages. The page break
  before each script does not survive this upload, so the docs run on continuously.

### Upload into PromptSmart (Dan, 2026-10-11): the last step, every time

Dan reads from PromptSmart Pro. Every teleprompter document goes in as its own script; the B-roll list does not.

1. Export the Google Docs as Word files into a folder inside the project (the browser tool can only read files
   there): `rclone copy gdrive: tmp/promptsmart --max-depth 1 --files-only --include "<prefix> - Teleprompter*"
   --drive-export-formats docx`. Delete the folder when done.
2. Claude in Chrome, new tab, `https://my.promptsmart.com/scripts`. He is logged in (the account email shows top
   right). If it asks for a login, stop and tell him: do not type credentials.
3. Do not click IMPORT (it opens a file picker the tools cannot see). `find` "file input for importing scripts" and
   give that element to `file_upload` with the .docx paths. Up to 5 files in one go.
4. Wait 5 seconds and screenshot: each file shows as a card named after the document. Open one, and with
   `javascript_tool` read `document.body.innerText`: the word count should be the document's (plus about 200 for the
   page's own menus), the last lines should be the last script's, and there should be no square brackets.
5. Close the tab. Tell Dan the three script names as they appear in PromptSmart.

The page shows when his subscription ends. If that date is before the shoot, say so in the report.

### Reaction clip list (Dan, 2026-10-12)

For the 10/17 shoot Dan asked for one more filming document: "a bullet point list of all the clips that I am
reacting to, queued up to the time frame that I'm going to react to it". Claude's reading: make it whenever a shoot
has reaction videos.

- One heading per video, in the order of the teleprompter documents. One bullet per clip: a link that opens at the
  clip's first second (`https://www.youtube.com/watch?v=<id>&t=<seconds>s`), the source, the time range, and the
  first and last words if the script gives them. X and TikTok links go in as they are.
- Take every `[PLAY CLIP ...]` cue from the scripts. Where the script cue has no link or no quote (the Clavicular
  shorts), the outline bullet above the script has both. Leave out his own videos: he is not reacting to those.
- A cue that says "PICK 10 TO 30 SECONDS INSIDE 0:00 TO 2:11" has no exact time. Link to the start of the window and
  say "pick" in the bullet. Do not invent a time.
- Check before upload, in code: every video id, link, time range and quote in the list is found in the shoot doc
  text, and every YouTube id answers at `https://www.youtube.com/oembed?url=...&format=json` (200 and a title).
- Upload and share it the same way as the other documents. It is not a teleprompter script: Drive only.
- **Changing the list later: edit the doc in place with the Docs connector** (2026-10-12), so the link Dan has keeps
  working. Text typed into the middle of a linked label does NOT take the link: after changing "opens at 0:00", send
  an `updateTextStyle` with `link`, `underline` and `foregroundColor` over the whole label, then read back and check
  that each link's second equals its "opens at" time.
- `reaction_clips_page.py`: an option may carry its own `video_id` and `source`, for candidates from different videos
  in one row (used for the retatrutide replacements).
- **Review page with my pick and alternates (Dan, 2026-10-12):** "a review page with all of the clips you recommend
  and one or two alternatives". How it was made: captions for every source video with `youtube_transcript_api`
  (start time per line); one helper agent per video group reads the script and the captions and returns, per clip,
  a pick and up to two alternates with whole-second start and end, first and last words, the words, and a one-line
  reason; `reference/reaction_clips_page.py page.json out_dir` builds the page (three cards per row, one shared
  YouTube player that plays start to end, "Use this one" buttons that write the reply); serve it with
  `_shared/review_server.py PORT out_dir`. Tell each helper to report where the script says something the clip does
  not: on 10-12 that found six lines. If an alternate carries the line Dan reacts to better than the script's
  window does, make it the pick and say so under "What I decided".
- **A reaction clip has to give him something to react to (Dan, 2026-10-12).** After watching the picks he cut two:
  a doctor explaining "Ozempic face" ("too boring to react to") and two Elon Musk text posts ("not enough to react
  to"). A calm explainer or a screenshot of a post is not a reaction clip. Pick the moment with a claim, a result or
  a face on screen, and say so on the page when a slot has nothing better.

### A blank line between ALL paragraphs (Dan, 2026-10-13)

Dan opened Teleprompter 2 and saw a solid block of text: "The scripts don't have line breaks between them... always
have line breaks between paragraphs so they look normal." The builder had written each spoken line as a paragraph with
nothing after it, and the 10-11 and 10-12 checks (lines matched, no brackets) could not see that.

- `tp_from_shoot_doc.py` now writes an empty paragraph (`<p><br></p>`) after every spoken paragraph, and a second one
  where a round cue stood. Any other builder or hand-made filming document does the same. The pickups document was
  fixed in place through the Docs connector: one `insertText` of a line break at the start of each paragraph that sat
  directly under another, highest index first.
- **New check, every build:** export as text and count non-empty lines directly followed by a non-empty line. The
  count must equal the number of scripts (each title sits on its first paragraph) and nothing more. Then open one
  document in the browser and look.
- Blank lines cost pages: about 390 words a page now (12,437 words = 32 pages), so `MAX_WORDS` is 16,000 (about 41
  pages) to stay under his 50. Count pages from the PDF by page objects (`/Type /Page`); the largest `/Count` can be
  the bookmark count instead.
- PromptSmart keeps the blank lines from the Word export. After re-importing, move the older cards to its Trash. A
  script can do the card menu, Delete and the confirm button with `element.click()`; read the dialog's text (it names
  the script) before confirming.

### Writing new scripts into a long shoot doc with the Docs connector (2026-10-13)

Used for the 26 shorts added to the 10/17 shoot doc (290,000 characters). No Chrome, no clipboard.

- **Insert every group at the same index, last group first.** Pick the empty paragraph where the block belongs, send
  `insertText` at its index with `"\n" + lines + "\n"`, and repeat at the SAME index with the group that goes before
  it. Nothing depends on the length of what was typed, so one slip cannot push the next insert into the wrong place.
  Two or three scripts per call (about 8,000 characters).
- **Then read the doc back and diff it against the local copy before any formatting.** Compute bold, italic and bullet
  ranges from where the text actually landed (`createParagraphBullets` on the outline lines; without real bullets
  `tp_from_shoot_doc.py` cannot tell where a script ends). 10-13: 1,251 new paragraphs, 0 differences.
- **Hook takes** go under the Subscribe line as a `[HOOK TAKES: ...]` cue followed by the two extra first lines as
  plain spoken lines, so they reach the teleprompter and Dan can film them.
- rclone's Drive login cannot call the Docs API (the API is off for that client), so the connector is the only way in.
- A YouTube frame cannot be checked by eye from the built-in browser pane: the video area screenshots black. A clip
  with no speech stays "check by eye" in the Reaction Clips document until Dan or a Chrome session looks at it.

### What Dan killed after watching the 10/17 reaction clips, and what he kept (2026-10-12)

His rule from this: clips first, he watches, then scripts (`_shared/WRITING-RULES.md`, section 4). Use this list to
judge a candidate before it reaches him.

| killed | his reason |
|---|---|
| A doctor explaining "Ozempic face" | "Too boring to react to" |
| Two Elon Musk text posts | "Not enough to react to" |
| Charles Barkley on a GLP-1 shortage | Not attention-getting, does not make sense in context |
| Six Bryan Johnson clips (bedtime, temperature, eating early, training, pills, plasma) | "Too boring", "no good lesson I can pull out of it" |
| A trailer line that only says who Bryan Johnson is | "Isn't really saying anything" (he took the alternate) |
| A 7-day belly fat workout intro | "Terrible choice... doesn't actually say anything. No purpose in watching this video." |
| A doctor on muscle loss | "Too boring" |
| Clavicular on GLP-1s, bone smashing | "No good lesson there" |
| Clavicular on a nose job | "Too boring, not relevant to us" |
| Clavicular on tanning, sunscreen, skin supplements, eyebrows | "Too boring" |
| Clavicular's retatrutide mention inside a rapid-fire list | "So many unrelated things in there. I want a clip... of him only talking about" it |

Kept: Clavicular saying looks matter more than personality, that getting lean is 70% of it, that hair is life;
Sharon Osbourne, Fat Joe, Amy Schumer, Meghan Trainor and Oprah on their own results. What the kept ones share: a
well-known person makes one blunt claim about looks or results, in a few seconds, that Dan can agree or disagree with
and then teach from. What the killed ones share: an explainer, a routine, a list, a product detail, or a person the
viewer does not care about.

