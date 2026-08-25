---
name: revisions
description: Review a video cut delivered by an editor (human or a cheaper-model pipeline session) and produce a revisions document in Dan's exact format — timestamped, with specific directions, specific replacement text, and direct links to the exact assets to use. Use whenever Dan shares a video (usually a Google Drive link) and asks to "review it", "give revisions", "write up revision notes", or "check the editor's cut" — even if he doesn't say "/revisions". For revising videos OUR pipeline will re-render itself, /ad-edit and /longform-edit remain the execution skills; this skill produces the review document.
---

# /revisions — review a delivered cut and write Dan-style revision notes

The deliverable is a **Google Doc in Dan's Drive**, written in Dan's voice and format,
**as a draft for Dan's review** — Dan reads it and forwards the link to the editor
himself. Never send anything to the editor directly. Also save a markdown copy in
`revision docs/` in the project folder (repo is public — nothing sensitive in it).

**ALWAYS CONFIRM WHO THE EDITOR IS AND WHICH ROUND THIS IS BEFORE WRITING.** Dan runs
tryouts where several editors cut the SAME script, so a new cut of a video you have
already reviewed is usually a DIFFERENT editor's first attempt, not round 2 of the same
one. Getting this wrong makes the doc read as "you ignored my last notes" to someone who
has never seen them. If the cut arrives as a bare Drive link, ask.

**Write goals, not tool steps.** Dan's editors work with AI editing tools, not a fixed NLE.
Never prescribe a program's menu path ("In Premiere: Modify → Audio Channels"). State the
outcome — "the finished audio must come from the RIGHT channel only, as mono" — and leave
the method to them. A named-tool instruction reads as ignorance of how they work.

Two audiences, same skill:
- **Human editor** (default): plain-language, tool-agnostic directions, links to assets,
  no jargon, no file paths on Dan's machine.
- **Pipeline session** (an /ad-edit or /longform-edit session executing the fixes):
  same document plus exact source timecodes, local asset paths, and script names.
  When Dan asks Fable to review a cheaper model's pipeline output, write BOTH layers —
  the human-readable item and, indented under it, the machine-actionable detail.

## Dan's document format (learned from his own revision docs)

- Title: video name + editor + round number ("Video 1 revisions - Waleed - round 1").
  **Round numbers are per EDITOR, not per video** — during a tryout, three editors can each
  be on their own round 1 of the same script.
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
     rebuild the voice from the RIGHT channel only, as mono. State that as the outcome,
     not as a menu path. Full background: /longform-edit
     Step 0.4. Write this as the #1 THROUGHOUT item in editor-friendly words.
   - **Then always run `reference/chan_align.py video.mp4`.** echo_check alone cannot tell
     "one mic, delayed copy" from "two different mics hard-panned". chan_align reports the
     best-fit delay+gain alignment residual (< −12 dB ⇒ one mic; ≈ −3 dB ⇒ two mics),
     flags polarity inversion, counts clipped samples, and measures how much voice a mono
     fold-down loses in the 300–3400 Hz band. Quote those numbers in the doc.
   - **And always measure loudness:** `ffmpeg -i cut.mp4 -af loudnorm=print_format=json -f null /dev/null`.
     Target −14 LUFS / ≤ −1.5 dBTP. Editors have shipped −8 LUFS / +2.5 dBTP with audible clipping.
   - Music bed: noise floor p5 above ≈ −45 dB in speech gaps *suggests* one; our shoots' raw
     floor is ≈ −53 dB. **This heuristic false-positives on an over-loud, hard-limited master** —
     confirm with per-band gap spectra on the lav channel before claiming a bed exists.
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
5. **A new cut of a video you already reviewed is usually a DIFFERENT editor, not round 2.** Dan runs
   tryouts where several editors cut the same script. On 2026-08-25 a cut of Video 1 was reviewed as
   "round 2" for the previous editor; it was Waleed's FIRST cut and had to be rewritten from scratch.
   Confirm the editor's name and round before writing a word — the framing changes every section,
   and "you didn't do what I asked" aimed at someone who never got the notes is the worst possible
   first contact. Open a first-round doc by crediting what already works ("keep this"), then the fixes.
6. **The two-mic source fault produces DIFFERENT symptoms per editor — test for both.** Editor A's
   Video 1 cut had L and R *identical* (they summed the mics before export). Waleed's cut of the same
   script shipped the **raw two-mic stereo pair** instead — L/R correlation **−0.72 at −7.8 ms**,
   polarity inverted, mono fold-down losing ~4 dB of voice. `echo_check.py` catches the first and
   reads the second as merely "channels differ". The decisive test is a **best-fit delay+gain
   alignment residual** (< −12 dB ⇒ one mic; ≈ −3 dB ⇒ two genuinely different mics) plus a **mono
   fold-down penalty** in the 300–3400 Hz voice band. Both are in `chan_align.py`; run it on every
   cut from every editor. Until an editor is told, they cannot know — write it as source-rig
   background, not as a complaint.
7. **Always measure integrated loudness and true peak, every round.** This cut shipped at
   **−8.04 LUFS / +2.53 dBTP with 166k clipped samples in L**. Nothing in the picture review would
   have surfaced it, and it is the kind of defect that survives to upload.
8. **Do not infer "music bed" from the noise floor alone.** A hard-limited over-loud master pushes
   the inter-word floor to ≈ −31 dB, which trips the "floor above −45 dB ⇒ music" heuristic with no
   music present. Confirm with per-band gap spectra on the LAV channel (a real bed at −20 dB under
   voice reads ≈ −30 dB in 80–500 Hz; this cut read −56 to −61 dB) and check the floor's *variance* —
   a bed is constant, room noise is not.
9. **Check that the right asset is on the right line, not just that an asset is present.** The
   single worst finding this round was the **crude-photoshop gag image used as the hook** at 0:00
   ("this picture got me abs") and again at 2:37 ("the picture that motivated me") — correct only at
   1:04, the photoshop line. Read the transcript against each insert; a technically-clean insert on
   the wrong sentence is worse than a missing one.
10. **Verify who is on screen before writing about it.** Dan is Asian; a reviewer working from
    stills can wrongly conclude a cut features a different presenter. Cross-check against
    `Short-form video content/instagram-danrosefit/profile-photo_danrosefit_1080.jpg` before
    claiming casting problems.
11. **Drive MCP `update_file` is metadata-only** — it cannot rewrite a Doc's body. To fix a
    conversion glitch, `create_file` again and `trash_file` the first. Also: a literal `*` inside a
    `**bold**` run (e.g. `**… "*AI Generated" …**`) breaks the markdown→Docs conversion; escape it
    as `\*` or reword.
