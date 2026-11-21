# Handoff: the 10/23 pool shoot filming documents (three teleprompter docs, one Filming document, PromptSmart)

Written 2026-10-20 by Claude (Fable 5.1) after Dan ruled on the last copy polish. Type: CONTENT (29 dedicated shorts,
4 follow-along long-forms, 7 long-form scripts). Not a video edit. Task name: `10-23 Pool Shoot Filming Documents`.
**Model: Opus 5.5, medium effort.** Clear steps, every check is in code, but the output is what Dan reads on the
prompter Friday morning, so not a Sonnet runner.

## What Dan asked for (2026-10-20, his words)

> The teleprompter document. Let's split this into three documents: long form, short form part one, and short form
> part two. We need to limit the length of these documents in order to not crash the iPad teleprompter app.
> The filming document with all filming and editing notes, with everything all together in one document.
> Also, have the new task install or set this up on Prompt Smart for the teleprompter documents.

So four new Google Docs, and the three teleprompter documents imported into PromptSmart. Deadline: before Friday
10/23, when he films by the pool.

## Source

"Gym Shorts Scripts - Friday 10-23 Pool Shoot", doc id `11nUmri621xbb7K44Wxan7IAljK2mJeizDFCRgK752AA`
(https://docs.google.com/document/d/11nUmri621xbb7K44Wxan7IAljK2mJeizDFCRgK752AA/edit). Every script in it is final:
Dan's own edit pass, three copy polishes, and his rulings on all suggestions (zero pending as of 2026-10-20 evening;
`Docs/COPYEDIT_POOL_LONGFORMS_1023_AS_DELIVERED_20261020.md`). **Never edit the source doc.** Read it with the Docs
connector `read_doc` (saves ~930 KB of JSON; parse it with Python, never by eye), build new documents from it, and
prove the source is untouched at the end (`get_file_metadata`: `fileSize` and `modifiedTime` unchanged). Read it
fresh at the start: if a suggestion is pending or anything changed, his version wins.

### Layout of the doc (paragraph start indices as of 2026-10-20, for orientation only; re-read and recompute)

| Part | Where | Shape |
|---|---|---|
| Title and shoot notes | index 1 to 1091 | Heading 1, an intro line, "Before you roll:" with 4 bullets (lav placement, mic level, Stairmaster songs, the new set numbers), then a "-" line |
| 29 dedicated shorts | 1091 to 47413 | Each: Heading 3 `N. TITLE IN CAPS` (1 to 29), one line `186 spoken words, about 50 to 56 seconds.`, then `[CUES IN CAPS]` and spoken paragraphs, no blank lines. One empty Heading 3 at 26293 before short 17: skip it |
| LONG-FORM: FOLLOW-ALONG WORKOUTS (4 cue tracks) | 47413 to 62473 | Heading 2, a note line ("The 10/15 demo clips cover the exercises. These are the spoken parts. A blank line marks where each round cue stood."), then 4 Heading 3 titles (RO-33 The 5-Minute No-Equipment Workout, RO-34 10-Minute Jump Rope And Kettlebell, RO-35 20-Minute Jump Rope And Dumbbell, RO-36 15-Minute Jump Rope And Abs), each with an id line `RO-33.`, spoken paragraphs, and EMPTY paragraphs where round cues stood |
| LONG-FORM OUTLINES (8, NOT SCRIPTED YET) | 62473 to 75704 | Bulleted outlines. **Not filming material: leave out of every document** (the scripts below replaced them) |
| LONG-FORM SCRIPTS | 75704 to end | Heading 2, then 7 Heading 3 titles `SCRIPT: ...`, each with one note line `1587 spoken words, about 11 minutes. Read by the pool, shirtless; Friday's gym B-roll cut in. Lines in [BRACKETED CAPS] are for the editor, not read aloud.` (script 1 adds "Rewritten 2026-10-20 from Dan's notes."), then cues and spoken paragraphs; a `-` line separates scripts. Three of Dan's paragraphs hold soft line breaks (`\x0b`): each starts a new teleprompter paragraph |

Spoken-word totals (2026-10-20): shorts about 5,970; follow-alongs about 2,830; long-form scripts 8,431. At about 570
words a page with no blank lines, nothing here comes near the 50-page limit; the split is Dan's call for the iPad app.

## The four documents

Names (no slash: rclone reads "10/23" as a folder):

1. `10-23 Pool Shoot - Teleprompter 1 - Long Form`: the 7 `SCRIPT:` long-forms in doc order, then the 4 follow-along
   cue tracks in doc order. (Default order; long-forms are what he films first by the pool. If Dan says the
   follow-alongs go first, swap.) About 11,260 words, about 20 pages.
2. `10-23 Pool Shoot - Teleprompter 2 - Short Form (Part 1 of 2)`: shorts 1 to 15. About 3,000 words.
3. `10-23 Pool Shoot - Teleprompter 3 - Short Form (Part 2 of 2)`: shorts 16 to 29. About 3,000 words.
4. `10-23 Pool Shoot - Filming Document`: everything the editor and the shoot need in one place, in this order: the
   "Before you roll" notes; the 29 shorts with their word-count lines, cues and spoken words; the 4 follow-along
   tracks (with the blank lines where the round cues stood, and a note that the 10/15 demo clips cover the
   exercises); the 7 long-form scripts with their note lines and cues; then a **B-roll shot list** section at the end
   (Dan wants everything together this time, not a separate B-roll doc). Keep headings, keep the blank line between
   paragraphs and between a cue and the words it covers (`_shared/WRITING-RULES.md`, section 6: filming scripts keep
   blank lines; teleprompter copies do not). Plain black text.

Teleprompter document rules (`/teleprompterscripts`, v3 and "No blank lines" sections; Dan's settled preferences):
- Words only. Strip every `[...]` cue, every word-count or runtime line, the `RO-33.` id lines, the section intro
  lines, the `-` separators, and the shoot notes. A script's title stays as Heading 2 so the outline lets him jump.
  Shorts keep their number in the title ("1. How To Do Pull-Ups...").
- **No blank line between paragraphs.** The one exception: in a follow-along track, keep the single empty paragraph
  where each round cue stood (the source already has them).
- Plain black normal text, no bold or italics. A page break between scripts (it does not survive the rclone upload;
  fine).
- Zero `[`, `]`, `http`, "spoken words" in the built text: the build prints these counts, all must be 0.

## Build

`reference/tp_from_shoot_doc.py` in `.claude/skills/teleprompterscripts/` parses the 10/17 format (a title paragraph
followed by a "Filming script ..." line). This doc is different (table above), so write `tp_from_1023_doc.py` next to
it, keeping its HTML conventions (`PST`, `BREAK`, `BLANK`), its `built_seq.json` output and its zero-count check:

- A short starts at a Heading 3 matching `^\d+\. ` and ends at the next Heading 3 or Heading 2. Drop its word-count
  line (`^\d+ spoken words`). Title case the CAPS title for the teleprompter heading, or keep it as typed; either is
  fine, say which.
- A follow-along starts at a Heading 3 under the FOLLOW-ALONG Heading 2 and ends at the next Heading 3 or Heading 2.
  Drop the `^RO-\d+\.$` line. Keep an empty paragraph where the source has one.
- A long-form starts at a Heading 3 matching `^SCRIPT: ` (strip the prefix for the heading) and ends at the next
  Heading 3 or the end of the doc. Drop its note line (`^\d+ spoken words`) and `-` lines.
- A paragraph that starts with `[` and ends with `]` is a cue. Split paragraphs on `\x0b`. Pending suggestions are
  read as accepted, and the build prints the pending count: it must be 0.
- The Filming document is the same parse with cues and note lines kept, plus the shoot notes at the top and the
  B-roll list at the end. B-roll list: every `[B-ROLL: ...]`, `[OPEN ON B-ROLL: ...]`, `[FILM AT THE GYM ...]`,
  `[AI GENERATED CLIP ...]`, `[PLAY CLIP ...]` and `[SHOW CLIP ...]` cue, grouped into "Film at the gym on Friday
  (16:9)", "By the pool" and "Editor: AI clips and outside clips", de-duplicated, each bullet naming the script(s)
  it serves. The Never Sore script's `[PLAY CLIP: JRE CLIPS ...]` cue carries a YouTube link and a time range: keep
  the link. Nested `<ul>` imports as real nested bullets.

Upload without Chrome, exactly as the skill says (both format flags, or the upload fails):

    ~/bin/rclone copy out_dir gdrive: --max-depth 1 --include "10-23 Pool Shoot - *.html" \
        --drive-import-formats html --drive-export-formats html --drive-pacer-min-sleep 2s
    ~/bin/rclone lsjson gdrive: --max-depth 1 --files-only --include "10-23 Pool Shoot*" --drive-export-formats html
    ~/bin/rclone link "gdrive:<name>.html" --drive-export-formats html      # anyone with the link (memory drive-always-public)

Verify in code, not by eye: download each back as text (`--drive-export-formats txt`) and compare every non-empty
line with `built_seq.json` (curly quotes and spaces normalized); word counts per document; page counts from a PDF
export (largest `/Count`); source doc `fileSize` unchanged. If Dan edits the source after the upload, rebuild and
re-upload with the same command plus `--ignore-times` (same ids, same links), then re-import into PromptSmart and
trash the old cards.

## PromptSmart (Dan's add-on request, 2026-10-20)

Follow `/teleprompterscripts`, "Upload into PromptSmart", for the three teleprompter documents only (never the
Filming document):
1. `rclone copy gdrive: tmp/promptsmart --max-depth 1 --files-only --include "10-23 Pool Shoot - Teleprompter*"
   --drive-export-formats docx` (a folder inside the project; delete it when done).
2. Claude in Chrome, `https://my.promptsmart.com/scripts`. He is logged in; if it asks for a login, stop and tell him
   (Claude cannot type credentials).
3. Do not click IMPORT. `find` "file input for importing scripts" and hand that element to `file_upload` with the
   three .docx paths.
4. Wait, screenshot: three cards named after the documents. Open one and read `document.body.innerText` with
   `javascript_tool`: word count matches the document (plus about 200 for the page's menus), last lines are the last
   script's, no square brackets. Check the paragraphs sit together with no blank lines.
5. If older 10/23 cards exist from an earlier attempt, move them to PromptSmart's Trash (card menu, Delete; click by
   `find` ref). Note the subscription end date shown on the page; if it is before 10/23, say so.

## Report to Dan

Links to the four documents, the page count and word count of each, the three script names as PromptSmart shows
them, which scripts are in which document, and the source-untouched proof. Wrap-up boxes. Nothing else is owed: the
scripts are final, no edits, no new content ("When moving or reorganizing existing text, add nothing").

## Current state

- Source doc final, zero pending suggestions (2026-10-20 evening). No documents built yet.
- Record of the last polish and Dan's rulings: `Docs/COPYEDIT_POOL_LONGFORMS_1023_AS_DELIVERED_20261020.md`.
- Previous teleprompter builds for reference: `/teleprompterscripts` v3 (10/17 shoot: 3 documents, rclone upload,
  PromptSmart import), `reference/tp_from_shoot_doc.py`, `reference/tp_reflow.py`.

## Starter prompt

> 10-23 Pool Shoot Filming Documents. Run `Handoffs/handoff-20261020-pool-shoot-1023-filming-documents.md`: from
> the final 10/23 pool shoot scripts doc, build three teleprompter documents (long form; short form part 1, shorts
> 1 to 15; short form part 2, shorts 16 to 29) and one Filming document with every filming and editing note and
> the B-roll list together, upload them to Drive with rclone, verify them in code, then import the three
> teleprompter documents into PromptSmart. Never edit the source doc. Report links, page counts and the PromptSmart
> script names.
