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

**STANDING RULE (Dan, 2026-08-08): every video gets TWO thumbnails, built for a
YouTube A/B test.** Not one final plus spares — two deliberate contenders, shown to
him side by side before install, then both loaded as an A/B test after publish.

**REVISED 2026-08-08 — the big black slab is out.** Dan's note on the first V4 pass:
*"too much black, and I'm shoved over too much to the side… I want my image more
centered in the frame, as centered as possible given the text, and less black."*
The type treatment stays; the **layout** changed:

- **Fill the frame with the photograph, not a black rectangle.** Two working layouts,
  both in `YouTube Long Form Video Content/v4-1min-ab-workout/build-thumbs-v4.py`:
  - **`scene`** (portrait source): subject cut out at full height and placed at
    ~0.63 of the width, with a **darkened, scenery-only crop of the same photo**
    behind it. Take the background strip from a part of the frame Dan is NOT in
    (e.g. `x 0.00–0.26`) — using a centre crop puts a ghost duplicate of his torso
    behind the text, which looks like an artifact.
  - **`plank`/full-bleed** (landscape source): cover-crop straight to 16:9, no
    background layer needed at all. The 6720×4480 shoot frames lose only ~15%
    vertically, so this is genuinely edge-to-edge photo.
- **Legibility comes from a gradient scrim, not a solid panel** — a horizontal ramp
  for side text, a soft top-left corner ramp for top text. Still not a blur.
- **Text must sit on empty background, never on Dan.** For a horizontal pose (plank),
  the only clear region is the **top band** — put a 2-line headline there and bias the
  16:9 cover crop upward (`ybias≈0.12`) to buy headroom. Cap the font (~84) and check
  the measured text bottom against where his body starts.
- Type unchanged: white caps **Manrope ExtraBold** (`~/Library/Fonts/Manrope.ttf` —
  variable file defaults to ExtraLight, you MUST call
  `set_variation_by_name("ExtraBold")`), red `rgb(201,48,45)` accent bar left of the
  text, logo `logos/03-symbol-left-text.png` **recolored white keeping alpha**,
  `rgb(5,7,11)` as the scrim/darkening colour.
- **When the video is a workout, one of the two variations should show Dan actually
  DOING an exercise**, not a posed physique shot. The 7-31-26 shoot's exercise frames
  are raw **39–66**: 39/40 seated, **41–48 toe touches with the medicine ball**,
  49–59 standing med-ball and bar, 60–66 Spider-Man planks.
- **The exercise has to READ as an ab exercise to someone scrolling.** Dan rejected a
  Spider-Man plank outright — *"I don't like that exercise because it's a push-up,
  which is not an ab exercise."* A plank/push-up shape is out no matter how good the
  frame is. **Toe touches (lying on the mat pressing the medicine ball up) are the
  approved look** — frame **44** is the pick: landscape 6720×4480, face turned up and
  well clear of a top-left text block, abs and ball both prominent, clean grass in the
  upper left. 43 and 45 are the same setup if you need alternates.
- **Exercise frames are raw and unretouched** — the finalized folder has 98 images and
  **zero exercise shots**. Retouch the chosen frame with `/photo-edit` BEFORE building
  the thumbnail (Dan's explicit instruction, 2026-08-08); the finished file goes into
  `photos/finalized social media photos/` as `photo-<frame>_FINAL_PRIMARY.jpg`.
- **Use a radial (elliptical) scrim, not a rectangular one.** A rect scrim with
  separate x/y falloffs leaves a faint visible box edge mid-frame. Anchor an elliptical
  falloff at the corner so it reaches zero smoothly: `d=hypot(x/rw, y/rh)`,
  `alpha = strength*(1-d)**1.35`, skip `d>=1`.
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

### Widening a portrait photo to 16:9 with generative fill (added 2026-08-30)

Dan's brief on the 3-minute-total-body thumbnail: *"reduce the blur effect and use a
generative fill to fill in the background area… so the whole frame is filled with
something that looks like a real image, like the Top 10 Ab Tips thumbnail."* The
`scene` layout above fakes this with a darkened crop of the same photo; this replaces
it with a real photographic extension. Working build in
`social media graphics/youtube/thumbnails/3 Minute Total Body Home Workout/_build-2026-08-30/`
(`mkseed.py` → `comp.py` → `build-thumbs.py`, plus the exact prompts).

**The pipeline, and every step earns its place:**
1. **Seed canvas.** Place the portrait at full canvas height on a 16:9 canvas, subject
   torso-centre at ~0.66 of the width, and fill the empty sides with a **horizontally
   stretched, heavily blurred copy of the photo's own edge strip** (take ~32% of the
   width, resize to the gap, `GaussianBlur(gap/22)`). Do NOT leave the gap flat white
   and do NOT mirror: a blurred stretch carries the correct vertical banding (sky,
   tree line, fence, grass) with no recognisable structure for the model to duplicate.
   Real photo ends up 43–52% of the frame; the model paints the rest.
2. **Generate** with `gemini-3-pro-image` at `--tier draft` (2K → 2752×1536, $0.134).
   4K is wasted here — the deliverable is 1280×720.
3. **Composite the REAL subject back** over the generated background (below).
4. Cover-crop to 1280×720, scrim, type.

⚠ **THE MODEL SILENTLY RE-CENTRES THE SUBJECT, AND THAT ALONE WOULD PUT THE HEADLINE
ON TOP OF HIM.** First take moved his torso centre from **0.660 → 0.508** — while
preserving his size and vertical position *exactly* (torso width 0.1519 → 0.1500, head
top 0.062 → 0.062). It is a pure horizontal translation, i.e. the model "improving" the
composition. **A COMPOSITION LOCK paragraph fixes it completely** (verbatim in
`po-place.txt`): state that the picture is *deliberately* off-centre, that the empty
left half is negative space for a designer's headline, that he must land at exactly the
same horizontal position as the input, and that **moving him toward the centre is a
complete failure even if it would be a better-balanced photograph**. Re-measured after:
centre **0.660**, torso width **0.1519** — exact. Locking pixels does not work; locking
*intent* does.

⚠ **ASK FOR REDUCED BLUR ACROSS THE WHOLE WIDTH, NOT JUST IN THE FILL.** These shoot
frames are shot wide open and the background is unreadable mush. Instructing the model
to re-render the background "with MODERATELY REDUCED blur, so a viewer can read the
fence rails, the tree trunks and the texture of the grass — but still a real photograph
with real depth of field, the man still the sharpest thing in frame" is what turns the
bokeh into a legible real place. Say explicitly that edge-to-edge sharpness would look
artificial, or it flattens the depth entirely.

**The subject must be composited back — the model re-renders his face and body.** The
standing "never AI-repaint Dan's real photos" rule still holds; only the *background*
is generated. Recipe (`comp.py`):
- Vision person mask (`personmask.swift`, in `.claude/skills/shorts/reference/recentre/`)
  on both the real strip and the generated frame.
- Register by maximising mask IoU over dx∈±40, dy∈±26. Measured on all three:
  **dx=0, dy 0/−2, IoU 0.94–0.99** — the composition lock makes registration trivial.
- Erode the mask (`MinFilter(7)`) then feather (`GaussianBlur(2.2)`) so you never take
  the original's blurry background rim; that is what prevents a halo. Verified at 4×:
  no cut-out edge, no colour fringe.
- Tone-match the real subject to the generated one with per-channel gains on the mask
  core, clipped to [0.88, 1.14] — landed 0.99–1.03 on all three.

⚠ **THE BOTTOM OF A KETTLEBELL/DEADLIFT REP FAILS DAN'S OWN ABS-VISIBLE RULE.** He asked
for a mid-lift action shot; every bottom-position frame (26/27/30/31/34/37) has him
hinged forward with the abs compressed into folds that vanish at grid size. Use the
**top** of the lift instead — standing tall holding the bell still reads as the exercise
and the abs are extended and crisp. Check the torso at 1:1 before committing to an
"action" frame.

**Assert text clearance on the finished file, not the plan.** Person-mask the rendered
1280×720 thumbnail, take the band between the headline's top and bottom y, find the
subject's leftmost column, and require ≥25 px of clearance from the measured text right
edge. This batch: 62 / 103 / 111 px.

⚠ **`logos/03-symbol-left-text.png` NO LONGER EXISTS** — that folder was reorganised and
now holds only banner drafts. The same white wordmark with alpha is at
**`Media/video_edit/work/logo_white.png`** (360×111, identical to `public/img/logo.png`).
It is already white, so the recolour step in the old scripts is now a no-op.

## Shorts

**Use `/shorts` — it supersedes this section.** Every short's audio goes through
`.claude/skills/_shared/audio` and must carry `audio_gate.py`'s PASS stamp before it is uploaded
(`/shorts` `qc.js` and `deliver.js` refuse an unstamped file). That skill carries the full pipeline
(silence-snapped cuts, per-shot classification, the graphics band, captions, QC) plus
working code in `.claude/skills/shorts/reference/`. The rules below are the summary only.

- **Dan picks the segments, not Claude.** Give him a shortlist with the verbatim spoken
  text and timecodes; he picks by letter.
- A Short must **stand alone with its own reason to watch** — "random clips from the
  video" was explicitly rejected.
- **Never crop through a graphic.** Anything with text, numbers or UI gets the whole
  16:9 frame scaled into the vertical frame, never a centre crop.
- **If the subject fills the frame, give graphics their own band** rather than hunting
  for a gap — measure region clearance first. See `/shorts` Step 6.
- Captions: ONLY from Whisper word timestamps. Arial 86 bold, MarginV 690, uppercase
  ABS/AI. 1080×1920, 24fps, crf 18.
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
