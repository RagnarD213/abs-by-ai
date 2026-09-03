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
1. **Audio first — run the shared standard on the editor's file, so the doc quotes the same numbers
   we hold ourselves to** (2026-09-02; `echo_check.py` and `chan_align.py` are now shims):

       python3 .claude/skills/_shared/audio/pick_lav.py CUT.mp4 --analyse
       python3 .claude/skills/_shared/audio/audio_gate.py CUT.mp4 --no-stamp --ab AB_his-vs-editor.mp4

   `pick_lav --analyse` prints every stream/channel with SNR, decay, EDT, clipping, and the pairwise
   lag + polarity — it handles 2-channel files AND the 8/28 four-track rolls (the old `chan_align.py`
   exited "not stereo — nothing to compare" on those, so the review gate reported nothing wrong).
   `audio_gate` measures the delivered file against Muhammad's ad on the ten rows Dan rejects on
   (image, comb, room, tone, floor, dryness, loudness, spread, true peak, silence/length). Quote the
   FAIL rows with their numbers in the doc, in editor-friendly words, and attach the A/B clip. The
   signatures to recognise:
   - L/R strongly correlated at 0 lag but echo peak ~7–8 ms in speech ⇒ the editor
     **summed the two camera mics** (right = lav, left = room mic ~2.6 m away; the
     comb filter is baked in and un-EQ-able). The fix must happen at the source:
     rebuild the voice from the RIGHT channel only, as mono. State that as the outcome,
     not as a menu path. Full background: /longform-edit
     Step 0.4. Write this as the #1 THROUGHOUT item in editor-friendly words.
   - Two mics hard-panned (raw pair shipped): `pick_lav` reads a strong pair peak at ±7–8 ms,
     zero-lag near 0, and the gate's L/R row fails. Two mics summed: L/R ≈ +1.0 but the gate's comb
     row fails (ripple ≈ 1.1 dB vs his 0.54). Roomy: the EDT row (>80 ms; his 40).
   - Loudness and true peak are gate rows (−14 ±1 LUFS, ≤ −1.0 dBTP). Editors have shipped
     −8 LUFS / +2.5 dBTP with audible clipping.
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

- **Audio**: the `_shared/audio` gate rows above — lav only (per `pick_lav`, never "right channel"
  on an 8/28 roll), no comb, room ≤ 80 ms, −14 LUFS, true peak ≤ −1.0 dBTP.
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
12. **Read the Upwork/message thread BEFORE writing a round-2 doc.** On 2026-08-30 Waleed delivered
    a "final video" whose picture was byte-for-byte his first cut. The thread settled the framing:
    Dan *had* sent the round-1 doc and Waleed *had* acknowledged it — but every message in both
    directions for the five days after was about audio only. So the doc leads with "our conversation
    narrowed to audio" instead of "you ignored my notes". Same facts, opposite outcome for whether
    the editor stays. Establish (a) was the doc actually sent, (b) what has been discussed since,
    (c) what the editor believes the remaining scope is.
13. **Frame-diff the new cut against the previous delivery — it is the decisive measurement for
    "were the revisions applied".** `ffmpeg -i old -i new -filter_complex
    "[0:v]scale=320:180,format=gray[a];[1:v]scale=320:180,format=gray[b];[a][b]blend=all_mode=difference,
    signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=diff.txt"`. Waleed's read **0.144
    mean / 0.547 max luma levels across all 8,012 frames, zero above 2.0** — pure re-encode noise.
    Identical frame count and identical duration to the microsecond corroborate it. This turns
    "you didn't do the revisions" from an accusation into a number, which is both fairer and harder
    to argue with. It also means **every timecode in the previous doc is still exactly valid** — say
    so, it makes the re-do feel far smaller to the editor.
14. **`_edit_work/<job>/C1591.wav` is a 16 kHz MONO Whisper input, not the camera audio.** Panning
    `c0=c1` off it returns silence and every spectral comparison reads exactly zero correlation. The
    real two-channel 48 kHz audio is in the camera `.MP4`. `ffprobe` the channel count before
    trusting any raw-file comparison.
15. **Music can only ADD energy, never subtract — so a measured HF deficit against the raw file is
    always real attenuation, whatever the bed is doing.** Useful because the bed contaminates the
    band ratios: on this cut it sat only 7.7 dB below the mix at 3.5–6k and 4.8 dB at 6–9k, so the
    measured −2.6 dB HF cut understated a true voice cut nearer −3.5 dB. Quote the conservative
    number; it cannot be argued down. Measure the bed's per-band contribution (speech-frame vs
    gap-frame band energy) before attributing any boost to EQ — a low-end lift *can* be the bed.
16. **When an editor draws a scope line, concede the subjective half and keep the objective half.**
    Waleed's covering note declared further audio work to be "specialist audio-post… spectral
    matching, multiband processing, professional mastering". Contesting that invites a walk-off.
    The doc instead reframed the three remaining audio items as what they measurably are — a limiter
    ceiling, a fader move, and one tonal note explicitly marked "your call" — and let the clipping
    stand on its own (**6,333 samples pinned at full scale, up from 2,426**), because a sample at
    0 dBFS is not a matter of taste. Give the editor a way to comply without retracting anything.
17. **`whisper` shells out to `ffmpeg` by name.** Without the static build on `PATH` the transcribe
    call fails and writes an EMPTY transcript rather than erroring visibly. Check the output has
    lines before using it. **scipy is not installed on this Mac** — write the alignment and band
    analysis with numpy only (`np.correlate` plus cumulative-sum sliding normalisation works fine).
18. **Retention is part of the deliverable when Dan says so.** Alongside the doc, write the
    paste-ready messages: one to send, one for a scope pushback, one nudge. The thing that makes a
    fixed-price freelancer quit is believing the revision loop is unbounded — state explicitly that
    nothing in the doc is new, that the list ends the job, and that there is more paid work behind
    it. Advise Dan **not to release a funded milestone** before the outstanding work lands; it is
    the only structural leverage left.
19. **When the editor's OWN earlier cuts already have the right sound, measure those and make them the
    target.** Muhammad's Ad 3 (2026-09-01) shipped the raw two-mic pair (L/R −0.72 at −7.85 ms,
    inverted) while his Ad 1 and Ad 2 measured as one mic (residual −18 to −26 dB). "Do exactly what you
    did on Ad 1 and Ad 2" lands better than any explanation, and it is provably achievable by him.
    Compare speech-band spectra too: the bare right channel is ~6 dB duller above 2.5 kHz than his
    Ad 1 mix, so say "add the same top-end back" or the single-mic fix will sound worse to him.
20. **"Add it to this doc" = append a new H2 section in the SAME bullet format, via the osascript HTML
    clipboard + cmd+v at the end of the doc (click the last line, End, Return x3 to leave the list).
    Set the clipboard IMMEDIATELY before the paste** — a concurrent session overwrote it between set
    and paste and a stray file path landed in Dan's doc; cmd+z, re-set, paste again, then verify by
    Drive read-back. Check the pasted section AND that the previous section is byte-unchanged.
21. **Asset folder for the trainer-ad AI clips is `1ZO4wukehoHAwnRRyDyFKm4hFtXMYF2Ex`** (8 s hook
    cutdown `1Io6XQlkym21ufR2aUZz_dc_j0tU_2VMC`, 35 s story `1mW5nEDjDbPCJUJGtjHUCrGqRVsX-Lhie`); the
    real app screens (trainer assessment `1wFsyT9eKeUVzDcF0L7bbAPn5DSAVdRIs`, workout day
    `11AS0LYjs-LfUPuhhVqGdAtiN1sjkJ02j`) are in the reference-ad folder, and the installed exercise
    demos are public at `https://absbyai.com/exercise-demos/<id>.mp4` — link them, never re-upload.
    The trainer-assessment screen shows the GOAL image alone, so it is the clean replacement whenever
    an editor puts the app's "Meet the new you" side-by-side on screen (three editors have now).

22. **Every revision doc is written as Dan, first person, and never says Claude wrote any of it (Dan,
    2026-09-02).** No "Claude's additions", no "reviewed by Claude", no split between his items and ours.
    When Dan has already typed a few items into the doc, absorb them into the full list in the same voice
    and format — rewrite his bullets in the doc's style rather than leaving them as a separate block — so
    a reader cannot tell which items he typed and which were measured. The editor is to believe Dan did
    every revision personally. Same rule for the markdown copy and the section headers.

23. **Round 2 of Muhammad's Ad 3 (2026-09-02) — three measurements that decided the doc.** (a) *Which mic
    did the editor use?* Cross-correlate the new cut's mono against EACH channel of the previous delivery
    with an FFT over a ±2 s lag window — his V2 matched V1-RIGHT at +0.89 to +0.91 and V1-LEFT at −0.7,
    at a constant +13.7 ms (a re-conform offset; under a frame, not a sync fault). A ±12.5 ms sample-loop
    search returned ~0.2 and would have said "unknown source". (b) *Same duration to the microsecond does
    NOT mean the picture is unchanged* — he replaced inserts in place; the frame-diff was 27 mean with the
    only quiet stretches being the two "keep" clips. Read the diff as a map of what changed, not just a
    changed/unchanged verdict. (c) His masters sit at −18 LUFS (Ad 1 −18.2, Ad 2 −19.1, V2 −18.4), so the
    gate's loudness row fails on every cut of his; the doc asked for −14 with a limiter rather than
    "match Ad 1" again. His review copies are 854×480 (Ad 2's was too); the 1080p comes with the final,
    so ask for it, don't flag it as a defect.
24. **Google Docs paste inherits the cursor line's character style.** The round-2 section landed entirely
    bold because the last empty paragraph carried bold from the previous section (the B button was lit).
    Look at the toolbar before cmd+v; if B is active press cmd+b first. cmd+z removes the whole paste
    cleanly. Also: `cmd+End` does nothing in Docs on a Mac — `cmd+ArrowDown` goes to the end.

23. **Getting a NEW small clip to the editor when the Drive uploader cannot be driven (2026-09-02).** Base64
    through the Drive MCP is a token trap (a 1.8 MB clip is ~2.5 M characters in one tool call — never do
    it), and Drive's web uploader still exposes no file input to `file_upload`. The route that works:
    drop the muted clip in `public/ad-assets/` (gitignore exception `!public/ad-assets/*.mp4`, keep each
    under ~3 MB), commit, push, wait for the Railway deploy, and link
    `https://absbyai.com/ad-assets/<name>.mp4` in the doc — the exercise demos already ship this way.
    Only Dan's own footage that is going into a public ad anyway; the repo is public.
24. **Dan's real supplement stack is on camera for the whole 03 supplements longform**
    (`claude edited long form content/03 - …/CUT_v1_graded_NO-GRAPHICS.mp4`, no lower thirds). A bottom-band
    crop panned across the counter (`crop=1280:720:x='(in_w-1280)*t/5.5':y=340` → 1080p) makes clean
    product B-roll with his face out of frame; the pan is at `Media/ad-assets/batch1-ads/clips/`.
25. **In Google Docs, `cmd+End` did nothing through the extension; `cmd+ArrowDown` jumps to the end of the
    document.** The last line of a Muhammad doc has been a plain paragraph, so no Return x3 was needed —
    screenshot first and read the toolbar's list button before pressing Return.
26. **A script can hand the editor ONE app clip for a whole section, and he will lay it under the first
    line of that section.** Ad 4's supplement-audit scroll ran under "upload a picture… generate a future
    self", not under "take a photo of your supplements" seven seconds later. Walk every app screen against
    the exact sentence it plays under, the same as lesson 9 for images.
27. **Whisper is a Python module here, not a command: `python3 -m whisper CUT.mp4 --model small --language en
    --output_format json`** with `Media/video_edit/bin` on PATH. A bare `whisper` call fails silently inside a
    backgrounded shell (lesson 17's empty transcript, again). Also: in zsh, `echo ==== X` errors ("= not found")
    because a leading `=` is filename expansion — quote separators. Both cost a rerun on Ad 5 (2026-09-03).
28. **Peaks at 0 dBTP on a −19 LUFS master can be the VOICE, not the SFX.** Ad 5 measured −18.9 LUFS with 58
    separate seconds touching 0 and 1,800 clipped samples; per-second peak scan (numpy on the mono decode)
    showed plain talking-head seconds (1:36, 1:40, 1:52, no whoosh) at +2.4 dB. Ad 4's whoosh-only finding does
    not generalise — always run the per-second scan and name the quiet seconds in the doc, so the editor puts
    a limiter on the mix rather than just turning the SFX down.
29. **The SCRIPT can contradict a standing rule — the rule wins, and say so in the doc.** Ad 5's script cue
    for the closing app clip reads "the app's own before/after reveal screen — in-product footage is the one
    place a before/after pair is safe". It is not (Dan's rulings on Ads 2, 3 and 4). The doc told Muhammad to
    ignore the note; the scripts doc itself still needs correcting. Read every bracketed cue against the
    rules list before assuming the editor got it wrong.
30. **Two new layouts that are still a before/after in one frame:** a two-panel with an ARROW between heavier
    Dan and ripped Dan (Ad 5, 1:27 — the editor split a single AI clip into panels), and any belly-grab /
    pinch stock close-up (Ad 5, 1:11 — body-shaming under Google's weight-loss policy). Both are now in the
    standing rules. The fix for the arrow panel is to play the clip full frame in one panel, not to drop it.
31. **Appending to Muhammad's batch doc: `reference/md_to_docs_clipboard.py <md>` builds the nested-list HTML
    and sets the clipboard in one step** (the `markdown` package is not installed; a hand-rolled converter
    mangled Dan's `\*\*` headers twice before the tree version). Then in Docs: click in the body,
    `cmd+ArrowDown`, check B is off, `cmd+v`, and verify with a Drive `read_file_content` read-back that the
    new H2 is there and the previous sections are unchanged. Pasted H2s land black while Dan's are blue —
    cosmetic, he has not objected.
