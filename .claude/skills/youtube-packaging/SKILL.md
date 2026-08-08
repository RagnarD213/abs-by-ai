---
name: youtube-packaging
description: Package an Abs By AI YouTube video for upload — SEO title options, description with UTM link + chapters, tags, pinned comment, thumbnails, and Shorts cutdowns. Use whenever Dan asks to get a video ready for YouTube, make thumbnails, or cut Shorts.
---

# YouTube video packaging (Abs By AI channel)

Established with Dan on 2026-08-04 while packaging the channel-intro video (V1).
Working example output: `YouTube Content/channel-intro/` (PACKAGING.md, thumbnails, shorts/).

## Workflow

1. **Transcribe** the video with the ad-factory Whisper pipeline (word timestamps —
   `bakeoff/.env` has `REPLICATE_API_TOKEN`; model + call shape in
   `ad-factory/the-upload/assembly/transcribe.js`). The transcript drives titles,
   chapters, and Shorts.
2. **Titles:** give Dan 5 options targeting real search queries (the "get abs with
   AI / ChatGPT fitness / abs at 40" families), with a recommendation.
3. **Description:** hook line, absbyai.com link with
   `utm_source=youtube&utm_medium=video&utm_campaign=<video-slug>`, chapters built
   from the real transcript timestamps, AI-imagery disclosure line, subscribe CTA.
4. **Tags + pinned comment** (comment carries a `utm_medium=comment` link).
5. **Thumbnails** — see rules below.
6. **Shorts** — see rules below.
7. **Upload checklist:** Not made for kids; **altered/synthetic content disclosure
   box = YES** (AI transformation imagery qualifies); custom thumbnail; pinned
   comment posted + pinned; end screens once a second video exists.

## Thumbnail rules

**SUPERSEDED 2026-08-07 — read this first.** Dan **rejected** the old
Arial-Black-white-text-with-heavy-black-stroke look and directed that thumbnails
match the **channel banner** instead. The style below is current; the Arial Black
recipe that used to live here is dead. V2's Aug-7 finals
(`thumb-poolstand-*`, `thumb-redshorts-*`) are the reference, NOT its Aug-4/5 ones.

- **Current system (banner-derived):** solid `rgb(5,7,11)` background, **never a blur
  effect**; white left-aligned caps headline in **Manrope ExtraBold**
  (`~/Library/Fonts/Manrope.ttf` — the variable file defaults to ExtraLight, you
  MUST call `set_variation_by_name("ExtraBold")`); red `rgb(201,48,45)` accent bar to
  the left of the text; logo lockup `logos/03-symbol-left-text.png` top-left,
  **recolored to white keeping alpha** or it vanishes on black; the photo panel sits
  right and dissolves into the black via a darkening ramp + alpha feather.
- **Working build script to copy:** `YouTube Long Form Video Content/v4-1min-ab-workout/build-thumbs.py`
  (adapted from `six-ways-ai-abs/build-thumbs.py`). Takes an output dir + `yes|no` for
  the logo; per-photo crop boxes are fractions of the source, head-top → just below
  waistband.
- **Source photos: `photos/finalized social media photos/`.** (The path this file
  used to give, `photos/finalized photos/`, **does not exist** — corrected 2026-08-08.)
  Never AI-generated bodies or video stills unless Dan says so.
- **Never AI-repaint Dan's real photos** for thumbnails. Composite programmatically
  over the untouched photo. AI generation was tried 2026-08-04 and rejected.
- **Two variations per video = two DIFFERENT photos, SAME text.**
- **Dan's hard rule: abs visible in every variation, and text must NEVER overlap them.**
- **The 7-31-26 pool shoot is 2747×4096 portrait, so a straight 16:9 crop cannot hold
  face and abs at once** (needs ~3900px width). Thumbnails from it must be composites —
  which the panel layout above already is.
- **Prefer a photo that previews the video's content over a generic physique shot.**
  For V4 (1-minute ab workout) `photo-49` won because Dan is holding a medicine ball
  on a mat — the actual equipment in that workout.
- Canvas 1280×720 JPG under 2 MB.
- Finals go in `social media graphics/youtube/thumbnails/<Video Name>/` (own subfolder
  per video, never loose files). Keep `-nologo` variants alongside the `-FINAL`s.
- Installing fonts needs no permission.
- **Save location (Dan's standing instruction, 2026-08-04):** finalized thumbnails
  go in `social media graphics/youtube/thumbnails/<Video Name>/` — always create
  a subfolder named for the video and save all of that video's thumbnail
  variations inside it. Never dump loose files into `thumbnails/` itself.
- Working command pattern: see the `thumb-towel-v1` / `thumb-flag-v1` recipe in
  the channel-intro session — crop/scale to 1280×720, then one drawtext per line.

## Shorts rules (Dan's feedback, 2026-08-04)

- **Dan picks the segments, not Claude** — at least until a pattern is established.
  Give him the sentence-timestamped transcript; he highlights the parts.
- A Short must **stand alone with its own reason to watch** (a complete valuable
  idea, tip, or story) — "random clips from the video" was explicitly rejected.
- **Check for full-frame text/graphic overlays before cropping.** The video's
  16:9 graphics get cut off by a blind 9:16 center crop. For segments containing
  graphics: scale-and-letterbox those moments or reframe — never crop through
  a graphic.
- Captions: ONLY from Whisper word timestamps (canonical grouping spec in
  `ad-factory/the-upload/assembly/captions-from-words.js`); Cap style, MarginV 690,
  uppercase ABS/AI emphasis. 1080×1920, crf 18.
- Post cadence: one Short every 2–3 days after the longform, not all at once.

## Configuring YouTube Studio directly (learned 2026-08-08 — do not re-derive)

Dan's expectation is that Claude **applies** the packaging in Studio, not just writes
a document. All of it is drivable through the Chrome MCP except pushing the video
file itself.

**What Claude CANNOT do: upload the video file.** Long-form files are 0.4–3 GB; the
only way to hand a local file to a page is via browser memory, and a 3 GB blob crashes
the tab. Chrome's native file picker isn't drivable either (computer-use is read-only
on browsers). **The file drag is Dan's, ~30s per video.** Everything after is Claude's.

**Getting the THUMBNAIL file in — three methods, only the third works on Studio:**
1. ❌ **localhost `fetch` → DataTransfer** (the technique that works on Play Console):
   **blocked by studio.youtube.com's CSP.** The request never leaves Chrome; the fetch
   just hangs until aborted and the local server logs nothing.
2. ❌ **`file_upload` MCP tool** — its `paths` param is broken (validation error
   "expected array, received undefined"). Still broken as of 2026-08-08.
3. ✅ **Clipboard image + a `paste` event.** Put the JPEG on the macOS clipboard
   (`osascript -e 'set the clipboard to (read (POSIX file "…") as «class JPEG»)'`),
   register a capture-phase `document` `paste` listener that takes
   `ev.clipboardData.files[0]`, `preventDefault()`s, wraps it in a `File`, assigns it
   to `input#file-loader` via `DataTransfer`, and dispatches `change`. Then click a
   neutral spot and send `cmd+v`. **No clipboard permission is needed** this way —
   `navigator.clipboard.read()` DOES need one and just freezes the renderer (45s CDP
   timeout) with no visible prompt.
   **After the change event, `input.files.length` reads 0. That is Studio consuming
   and clearing the input — success, not failure. Verify in the Thumbnail section, not
   the input.** Remember the listener dies on navigation; if it wouldn't, remove it.

**Pasting the DESCRIPTION:** `pbcopy` under the default locale mangles UTF-8 —
em-dashes arrive as `,Äî`. Export `LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8` before
`pbcopy`, and round-trip `pbpaste | grep "—"` to confirm before pasting.

**Other Studio quirks:**
- The upload stepper **refuses to advance while any required field is unanswered** —
  in practice "Is this video made for kids?". Answer it first or nothing else is reachable.
- `Escape` closes the **whole** dialog, not just a sub-editor. Fields already showing
  "Saved as private" are safe, but reload and re-verify rather than assuming.
- The content-list row caches the old title/thumbnail after saving. **Reload before
  concluding a write failed.**
- Ref-based clicks fail on the "Edit draft" button; use screenshot coordinates.
- Scrolling with the cursor over the description box scrolls the textarea, not the
  dialog. Put the cursor over the right-hand preview column instead.
- The schedule **time** field is a combobox: typing "5:00 PM" fills the box but may not
  commit. Scroll the list and click the real option.
- Tags are inherited from the previous upload via "Reuse details" — **add** the
  video-specific ones rather than replacing Dan's channel tags.
- Timezone "Local Time" is GMT-05:00 (Dan is Central).

## Hygiene

- `YouTube Content/` and `photos/` are git-ignored — keep all media out of the
  public repo.
- Zero AI generations against the production app; thumbnails/transcription cost
  cents via Replicate.
