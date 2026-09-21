# Handoff: add line breaks to Muhammad's dedicated-shorts scripts doc

Written 2026-09-21 (Claude, Opus 5). Small formatting fix, no new content.

## Goal

Dan likes the new scripts Google Doc for Muhammad's shorts batch, but it reads as one wall of text: there is no space
between paragraphs. Put blank lines in the right places:
- between the filming directions (the bold `[bracketed]` cue lines and the green `USE:` / red `NOT FILMED YET` lines
  under them) and the spoken script,
- between every paragraph of the spoken script,
- between one cue block and the next.

Nothing else changes: same words, same links, same order.

Doc: **Abs By AI - Dedicated Shorts Scripts (22 shorts) - Muhammad batch**
https://docs.google.com/document/d/1SzBTPp-tSjpIRjvKKsHNKduDhwpgqrNZ77hxAAPypaQ/edit
(Dan's Drive root. Its ID is linked from the brief doc `17JhkdWoSjl0BUD3Y6u2a7ePGniChlf0AepS83tahGjU`, so **keep this
same doc ID** if at all possible.)

## Why it happened

The doc was built as HTML (`<h1>`, `<h2>`, `<p>`) and imported into Google Docs with rclone
(`--drive-import-formats html`). Google's HTML import sets paragraph spacing to 0, so every `<p>` lands flush against
the next one.

## What exists

Everything that built the doc is in `/Volumes/Extreme/_edit_work/muhammad-shorts-brief/` (outside the repo on purpose:
it holds Drive IDs for Dan's private files, and the repo is public):
- `build_scripts.py` builds `scripts.html` from the local plain-text scripts copy
  `Media/codex-video-trial/05-recipes/candidates/shoot5-notes.txt` plus the per-cue asset map in `NOTES`.
- `assets_map.py` holds every Drive link. It reads `uploaded.txt` (IDs of the 29 files in the Drive folder
  "Muhammad Shorts Batch - Extra Assets", `1ySXsLSFFHaui2DCgu6Oz3bhJXJ1rT8JP`). Both must sit in the same folder.
- `build_brief.py` builds the brief (imports `SHORTS` from `build_scripts.py`; needs env vars `SCRIPTS_DOC_ID` and
  `AB_ID=1PfKk-VyhpyXNX0XCRy9Zx8nE5NQWd5ug`).
- `scripts.html` / `brief.html`: the exact HTML that was imported.

## Steps

1. **Check Dan hasn't edited the doc by hand since 2026-09-21 21:27 UTC** (Drive MCP `get_file_metadata`, compare
   `modifiedTime`; open it and look). If he has, do NOT regenerate over his edits: add the blank lines in place in
   Chrome instead, or ask him.
2. **Change the generator, not the text.** In `build_scripts.py`, emit an empty paragraph (`<p><br></p>`) after every
   emitted paragraph: after each cue line, after each `USE:` / `NOT FILMED YET` line, after each spoken paragraph, and
   after the "Raw footage / Expected finished / Status" line. Start each short (`<h2>`) on a new page
   (`<h2 style="page-break-before:always">`, except the first) so each script is its own page for the editor.
   Keep the intro paragraph under the `<h1>`.
3. Rebuild: `python3 build_scripts.py` in that folder. Confirm `scripts.html` contains no em dash character (U+2014), per the standing rule.
4. **Replace the content in place, keeping the doc ID.** Drive API `files.update` on
   `1SzBTPp-tSjpIRjvKKsHNKduDhwpgqrNZ77hxAAPypaQ` with `uploadType=media` and the HTML body
   (`Content-Type: text/html`) converts it into the existing Google Doc. rclone's OAuth token for the `gdrive:` remote
   works for this (`~/bin/rclone config dump` gives the token; refresh it with `rclone about gdrive:` first). Read the
   metadata back and confirm the ID and title are unchanged.
   - **Fallback** if in-place update won't take: import a new doc the same way it was first made
     (`~/bin/rclone copy <dir-with-html> gdrive: --drive-root-folder-id=0AFYhPET_BWanUk9PVA --drive-import-formats html --drive-export-formats html`),
     then rebuild the brief with the new `SCRIPTS_DOC_ID` and replace the brief the same way, then trash the old
     scripts doc. Tell Dan the new link.
5. **Verify in Dan's real Chrome** (`mcp__claude-in-chrome__*`; the in-app browser is not signed into Google): open the
   doc, screenshot two or three shorts. Every paragraph separated by a blank line, cues visibly apart from the script,
   links still clickable, each short on its own page.
6. Optional, same root cause: glance at the brief doc. It is mostly lists and tables, so it probably reads fine; only
   touch it if it has the same wall-of-text problem, using the same in-place method.

## Done means

- Same doc ID and title, same text and links, blank lines between all paragraphs and blocks, one short per page,
  checked in Chrome.
- Dan gets one line in chat with the link. No dashboard row (Dan's rule). Delete this handoff's line from the
  HANDOFFS section of `AI_COORDINATION.md` and its row in `Handoffs/README.md`, commit + push those two files.

## Don't

- Don't change wording, links or order. Don't touch sharing (Dan shares the docs himself). Don't contact Muhammad.
- Don't rebuild from the Google Doc's exported text: regenerate from the scripts in the work folder.
