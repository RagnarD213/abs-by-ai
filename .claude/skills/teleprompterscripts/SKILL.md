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

# Teleprompter-only copy of a finalized scripts doc

**STATUS: v1 — created 2026-08-11, from the batch-1 run
("Abs by AI finalized scripts batch 1 - WITH FILMING NOTES" → "… - TELEPROMPTER ONLY").**

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
