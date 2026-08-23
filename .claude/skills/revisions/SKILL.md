---
name: revisions
description: Review a video cut delivered by an editor (human or a cheaper-model pipeline session) and produce a revisions document in Dan's exact format — timestamped, with specific directions, specific replacement text, and direct links to the exact assets to use. Use whenever Dan shares a video (usually a Google Drive link) and asks to "review it", "give revisions", "write up revision notes", or "check the editor's cut" — even if he doesn't say "/revisions". For revising videos OUR pipeline will re-render itself, /ad-edit and /longform-edit remain the execution skills; this skill produces the review document.
---

# /revisions — review a delivered cut and write Dan-style revision notes

The deliverable is a **Google Doc in Dan's Drive**, written in Dan's voice and format,
**as a draft for Dan's review** — Dan reads it and forwards the link to the editor
himself. Never send anything to the editor directly. Also save a markdown copy in
`revision docs/` in the project folder (repo is public — nothing sensitive in it).

Two audiences, same skill:
- **Human editor** (default): plain-language, tool-agnostic directions ("In Premiere:
  …"), links to assets, no jargon, no file paths on Dan's machine.
- **Pipeline session** (an /ad-edit or /longform-edit session executing the fixes):
  same document plus exact source timecodes, local asset paths, and script names.
  When Dan asks Fable to review a cheaper model's pipeline output, write BOTH layers —
  the human-readable item and, indented under it, the machine-actionable detail.

## Dan's document format (learned from his own revision docs)

- Title: video name + round number ("V3 … Second round of revisions", "Video 1 revisions - round 1").
- A **THROUGHOUT VIDEO** section FIRST for anything not tied to one timecode, in
  \*\*BOLD ALL CAPS\*\* headers, each with sub-bullets. Rules he repeats every round
  live here (capitalization, crops, disclosure labels).
- Then a flat list of **timestamped items** in play order. Each item: the timecode
  (single `0:14` or range `1:41 - 1:52`), what to change, and — critical — the
  **specific replacement**: the exact text to put in a graphic, the exact asset with a
  direct Drive link, or exact source timecodes to pull ("Insert 0:57 - 1:02 from this
  video"). "Accelerate footage to fit duration" is the standard instruction when a
  replacement is longer than its slot.
- Give the on-screen POSITION of graphics (lower third, upper right corner, top two
  thirds / lower third splits, full screen).
- Exact text is quoted verbatim; capitalization instruction: Title Capitalization on
  all graphics, "don't use the capitalization I have in this document".
- For AI clips to be generated: give DIRECTIONS for what to generate, don't generate
  it. If we already have a matching asset, link that exact asset instead.
- Why-explanations appear only when the rule is new ("Why this is important: …").
- New standing rules get flagged: "For all future videos, …" / "Hard rule for future videos: …".

## Review workflow

0. **Fetch.** Drive file IDs come from the URL. Download with
   `python3 -m gdown <FILEID> -O video.mp4` into the scratchpad (installed for
   python3.9). `ffmpeg`/`ffprobe` are NOT on PATH — use the static builds in
   `Media/video_edit/bin/`.
1. **Audio first — run `reference/echo_check.py video.mp4`** (needs the static ffmpeg
   on PATH). It reports, at several offsets: L/R cross-correlation+lag AND an
   autocorrelation echo peak in the 3–15 ms window.
   - L/R strongly correlated at 0 lag but echo peak ~7–8 ms in speech ⇒ the editor
     **summed the two camera mics** (right = lav, left = room mic ~2.6 m away; the
     comb filter is baked in and un-EQ-able). The fix must happen at the source:
     re-import the camera files and use the RIGHT channel only, as mono (Premiere:
     Modify → Audio Channels → Mono from Right). Full background: /longform-edit
     Step 0.4. Write this as the #1 THROUGHOUT item in editor-friendly words.
   - Also check for a music bed: noise floor p5 above ≈ −45 dB in speech gaps means
     there is one; our shoots' raw floor is ≈ −53 dB.
2. **Transcribe** with local Whisper `small` (segment timestamps are enough) — this
   maps every script beat to a timecode for the doc.
3. **Look at every second.** Extract frames at 1/2s, montage into labeled contact
   sheets (~60 frames per sheet), and READ them: catalog every insert, graphic,
   stock clip, label, and typo with its timecode. Zoom into anything suspicious.
4. **Compare against the target style** (currently Muhammad A's reference edit:
   pause-free pacing, music bed ~−20 dB under voice, whoosh/pop SFX on every graphic,
   animated bullet builds / lower-third chips / title cards, phrase-synced punch-ins,
   highlight boxes on referenced photos, brighter grade, NO burned captions) — but
   re-skinned to OUR brand, never his pastel cyan.
5. **Check every standing rule** (below). Each violation becomes an item; new
   classes of violation also get a "hard rule for future videos" line.
6. **Choose replacement assets from what already exists** before directing anything
   new (see asset library). Only direct new AI generation when nothing fits.
7. **Write the Google Doc** via the Google Drive MCP `create_file` with
   `contentMimeType: text/markdown` — it converts cleanly to a Doc, including links.
   Keep Dan's `\*\*…\*\*` literal-asterisk look for THROUGHOUT headers. Save the
   markdown copy in `revision docs/`.
8. **Report to Dan** with the Doc link, the top findings, and anything that needs his
   call. He forwards it.

## Standing rules to check every review (Dan's accumulated rulings)

- **Audio**: single-mic rule above; −14 LUFS; true peak ≤ −1.5 dBTP.
- **Compliance (Google Ads)**: NO side-by-side before/afters, ever (before → footage
  → after separately is fine, disclosed); NO morph/transformation-in-one-shot; NO
  body-shaming / belly-fat zooms; NO email-capture form on screen.
- **Disclosure**: "*AI Generated" on every AI visual, full duration; upper-left and
  ~50% larger on full-frame AI clips; centered small tag on panel inserts.
- **Brand graphics**: black bg (or #162118 dark green field), headers large dark
  green ALL CAPS (#8C9858 olive reads on black), body off-white #E9EEDE, red #E22222
  only as attention accent, Manrope, Title Capitalization. Look = YouTube Shorts
  covers / `ad-edit/reference/motionlib.py` GREEN palette.
- **Casting**: goal-body people are white or Asian men 30–50, shredded-not-bulky,
  no unmanly outfits.
- **Product truth**: real app screens and the real generation flow only — never
  invented dashboards or generic AI-app mockups. End cards / demo flows end on the
  after picture ALONE.
- **Presentation**: no raw black pillarboxing of 9:16 assets (brand card or blurred
  fill); alternating ~50%/~70% punch-ins on talking heads; no dead air > 0.3s.
- **Voice input caveat**: Dan dictates; if a quoted correction seems odd, check the
  transcript audio before flagging his script wording as a "typo".

## Asset library (already uploaded to Dan's Drive — link these, don't re-upload)

- Folder **"00 ASSETS USED IN THE REFERENCE AD"** (`10veL4yDYVaaDh1q_2VKJObfa-YpGEW_A`):
  01 hook/endcard pool after-image, 02 before-picture 200lb, 03 heavier-Dan couch AI
  clip, 04–07 photo-shoot stills, 08 crude-photoshop gag clip, 09 REAL
  app-generate-future-self screen recording (use ~0:03–0:26; cut before its
  side-by-side ending), 10–12 REAL app screens (assessment / Monday workout / meal plan).
- Folder **"AI clips for Muhammad"** (`1bO1mZAk0ii9c-m45-YhSYmuYq_qPIpvm`): the four
  Veo benefit/dad clips — attractive-to-women (pool), men-respect-you (gym),
  feel-better (beach run), busy-dad (kitchen) — plus two real fat-dad photos.
- Local-only extras (Seagate `/Volumes/Extreme/_edit_work/ad1-8-14/assets_v1/`):
  `stats_scan.mp4` (scan+stats animation), `p_phone_mock.jpg` (lock-screen mockup).
  For human editors, direct them to REBUILD these natively in brand colors (better
  than compositing our render); only offer the files if Dan wants.
- List a Drive folder's contents with the Drive MCP:
  `search_files` query `parentId = '<folderId>'`.

## Lessons

1. **Google Drive web upload cannot be automated from the Chrome extension.** The
   file input is created transiently and clicked natively; synthetic DragEvent drops
   are ignored (Drive reads `webkitGetAsEntry`, null for scripted DataTransfer), and
   a prototype-click hook did not catch it. Check whether the asset already exists in
   Drive FIRST (it usually does — earlier sessions uploaded the ad1 set); for genuinely
   new small files use Drive MCP `create_file` with base64; for big files ask Dan to
   drag-drop, or convert the item into a "rebuild it natively" direction.
2. **The delivered export can hide the audio defect**: if L/R are identical the editor
   already summed the mics — cross-channel analysis alone says "fine"; only the
   autocorrelation echo peak reveals it. Always run both (echo_check.py does).
3. **Drive UI menus mis-click** (items shift between opens). Keyboard shortcuts are
   reliable: in Drive, `ctrl+c` then `f` = new folder. Screenshot fresh before any
   menu click.
4. Muhammad-reference measured targets, for pacing/music checks: zero gaps ≥ 0.25s,
   music ~−20 dB under voice (floor p5 ≈ −40 dB), luma median ~67, no burned captions.
