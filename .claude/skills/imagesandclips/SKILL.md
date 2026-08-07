---
name: imagesandclips
description: >
  Fill in the actual images and clips for a finished ad/video script — walk every
  bracketed visual cue in the script doc, source or generate the right asset, and
  place it in the Google Doc under its cue. Use whenever Dan asks to "fill in the
  assets", "add the images", "get the clips", or "do the images and clips" for a
  script — even if he doesn't say "/imagesandclips". Writing the script itself is
  /scriptwriting; writing the outline is /ad-outlines; a fully AI-generated video
  ad is /make-ad.
---

# Images and clips for a script

Input: a finished script in **"Abs by AI finalized scripts batch 1 - WITH FILMING
NOTES"** (`1r3Jmuihyryq0qv2Y3A--D_yaerF9B_ZqAb-QvOuAwjg`), where bracketed gold
lines are visual cues. Output: every cue that needs a picture has one sitting
directly under it, plus new cues where the script clearly implies a visual and
nobody wrote one.

## The rule that decides what to add — Dan's, 2026-08-06

**Only add assets the editor could not have chosen just as well herself.** Do not
add generic stock ("a plate of food", "someone at a gym", "money"). She can find
those. Add the things only we know about:

- Six Pack Shortcuts / SixPackAbs.com clips — she has no idea which one has Dan in it
- Dan's before picture, and shots from the recent photo shoot
- Any footage or photos of Dan (including his ad-agency channel)
- Abs By AI before/afters we generate
- **Real screen captures of the live absbyai.com app**
- AI-generated stills/clips we make

When the script implies a clip that doesn't exist, **generate a still that would
make a good START FRAME for it** and add a cue. Dan reviews the still first; the
clip gets made only after he approves.

## Video cues — still first, clip later, link never embed

1. Generate the **still** and put it in the doc under the cue.
2. Dan approves the look.
3. Only then generate the clip.
4. Upload the finished clip to Google Drive and put a **link** in the doc. Never
   try to embed video — a Doc can't hold it.

## Where the assets live

| Need | Source |
|---|---|
| Six Pack Shortcuts / SixPackAbs clips | `Media/B roll/` |
| Dan's own footage | `Media/B roll/youtube ad agency b roll.mov` (his agency channel) |
| Workout B-roll | `Media/B roll/` — 3 min ab workout · deadlift · m-100s · jump rope |
| Before picture, AI future-self, photo-shoot shots | **Already inside the scripts doc** — pull them out of the .docx export rather than re-deriving (see below) |
| App screens | Capture live from absbyai.com (recipe below) |
| Cartoon/gag stills | Replicate `google/nano-banana-pro` |

### B roll — what's actually in each file (verified 2026-08-06, don't re-scan)

The B-roll files are **screen recordings of YouTube**, not raw footage.

- **`interview b roll.mov`** — SixPackAbs.com "How To Lose Your Belly Fat" (3.3M
  views). **Dan is the man on the LEFT.** Best solo close-up of him is at **0:18**.
  This is the go-to for `[SHOW CLIP OF DAN FROM SIX PACK SHORTCUTS]`, especially on
  nutrition ads (the video is about belly fat).
- **`youtube ad agency b roll.mov`** — Dan's own "How To Set Up Your First YouTube
  Ad Campaign", channel *Daniel Rose – Social Response*. Dan alone, on camera,
  whole clip. Use it for the "running a successful ad agency" line.
- **`sixpackabs.com rebrand b roll.mov`** — mostly **Mike Chang and Thomas
  DeLauer**, not Dan. He appears only as a lower-third title card at ~0:11–0:15
  ("Dan Rose · Six Pack Shortcuts Co-Founder & CEO"). Use only if you specifically
  want the title card; it breaks Dan's "keep the focus on me" rule otherwise.
- 3 min ab workout / deadlift / m-100s / jump rope — training B-roll, pick by topic.

**Pick frames by looking, never by guessing.** Contact sheet at 1 fps, then crop
the player region out of the browser chrome:

```bash
FF="Media/video_edit/bin/ffmpeg"   # no Homebrew ffmpeg on this Mac
"$FF" -v error -i "Media/B roll/interview b roll.mov" \
  -vf "fps=1,scale=300:-1,tile=5x4" -frames:v 1 -y sheet.jpg
# sources are 3840x2160; the YouTube player sits at roughly 200,330 1990x1180
"$FF" -v error -ss 18 -i "Media/B roll/interview b roll.mov" \
  -frames:v 1 -vf "crop=1990:1180:200:330" -y still.jpg
```

### Reusing assets already in the scripts doc

The before picture, the AI future-self image and the photo-shoot shots are already
embedded. Pull the exact files instead of hunting the originals — they are also
already scaled correctly for pasting.

```bash
# Drive MCP download_file_content, export mime = ...wordprocessingml.document
# result lands on disk as JSON with base64 `content` (too big to read inline)
python3 -c "import json,base64;d=json.load(open(P));open('doc.docx','wb').write(base64.b64decode(d['content']))"
unzip -oq doc.docx      # images in word/media/
```
Then walk `word/document.xml` paragraphs in order, resolving `r:embed` rIds through
`word/_rels/document.xml.rels`, to map each image to the cue above it. The export
**dedupes** — one file can be referenced at two cues.

### Real app screenshots — retina, from live prod, with zero AI spend

Use the Apple-review comp account (`danroseconsulting+applereview@gmail.com`,
password in `app-store-assets/LISTING_COPY.md`). **Check what it already has before
generating anything** — it usually already holds a saved meal plan, logged meals and
transformations, so nothing needs to be created:

```bash
curl -s -X POST https://absbyai.com/api/auth/login -H 'Content-Type: application/json' \
  -d '{"email":"...","password":"..."}'          # -> token
# then GET /api/mealplan, /api/meals, /api/transformations with Bearer <token>
```

**Never run a generation on that account** — it pollutes the reviewer's gallery and
can displace the curated hero image (2026-07-30 lesson). The app is in App Store
review.

Capture with headless Chrome over CDP (Node 24 has a built-in WebSocket client):

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new \
  --remote-debugging-port=9333 --user-data-dir=<scratch>/prof --no-first-run \
  --hide-scrollbars about:blank &
```
Then `Emulation.setDeviceMetricsOverride` at 390×844 @3× (gives 1170×2532 retina),
set `localStorage.absbyai_session_token`, reload, click hub tiles via
`Runtime.evaluate` on `#hubSection [data-feature="nutritionist"|"macro"|"counsel"]`
(take the LAST match — the first ones are Daily Brief rows), and
`Page.captureScreenshot`.

**Crop the account email out of any hub shot** before it goes in the doc.

### AI stills

`google/nano-banana-pro` on Replicate, `aspect_ratio: "9:16"`, `resolution: "2K"`.
The token is not on this machine — read it from Railway → abs-by-ai → Variables
(Dan copies it; `pbpaste > <scratch>/.keys.env`, chmod 600; never into chat).
~13¢ per image. Prompt style that worked: *"a simple, funny hand-drawn 2D cartoon
illustration on a clean off-white background, vertical composition with lots of
empty space … flat colors, bold clean ink lines, no text."* Say **no text** — the
model will otherwise letter it badly.

## Placing assets in the Google Doc

Pre-scale everything first — **Docs ignores `width=` and CSS `width` and inserts at
natural pixel size.** 300px wide for portrait, 340px for landscape. Convert PNG →
JPEG q86; it took the Ad 2 payload from 1.2 MB to 412 KB, and smaller payloads
paste more reliably (551 KB is a known-good size, 2.8 MB is a known-fail).

**Insert per cue. Do not rewrite the ad** — that would delete Dan-approved copy for
no reason.

### The working loop (each cue)

1. **Jump to the ad** via the left-hand document outline, then scroll and screenshot.
2. **Click at the end of the cue line** (or the last line of the target paragraph)
   and press `End`.
3. **Only now** set the clipboard.
4. `Return`, then `cmd+v`, then screenshot **and look at what actually landed**.

Order matters: positioning between setting the clipboard and pasting is what lets
Docs substitute its own internal clipboard.

Clipboard, both flavors, with readback verification:

```bash
osascript -e 'set the clipboard to {«class HTML»:«data HTML<hex>», «class utf8»:«data utf8<hex>»}'
osascript -e 'get the clipboard as «class HTML»'   # compare hex to what you wrote
```

Wrap the payload as `<p style="…gold bold…">[CUE]</p>` (when adding a new cue) plus
`<p style="text-align:center;margin:0;"><img src="data:image/jpeg;base64,…"></p>`.
Cue style: `font-family:Arial;font-size:10pt;font-weight:bold;font-style:normal;
text-decoration:none;color:#7A6A2E`. Body paragraphs need explicit
`color:#000000;font-weight:normal;font-style:normal` or they inherit the neighbour's.

### Traps — all of these fired on Ad 2 (2026-08-06)

- **`cmd+F` does not work.** Keystrokes sent after opening Docs' find box land in
  the **document**, not the box — with any delay, and clicking the box first just
  steals focus back to the document. It typed `PUSHES A LAME-LOOKING NUTRITIONIST`
  into the H1 title twice. **Navigate by outline + scroll + click. Never by find.**
- **`clipboard info` showing `«class HTML»` proves nothing** — it stays true for a
  stale payload. Read the HTML flavor **back** and compare bytes. Even then, Docs
  can still paste from its own internal clipboard while the system clipboard
  verifiably holds the right bytes.
- **The internal-clipboard trap gets WORSE the longer the editing session runs.**
  On the Ad 2 revision pass it fired on roughly one paste in three, and what it
  pasted came from the user's wider clipboard history — a bank/tax admin screenshot
  and an Apple Developer page — not from the document. Two consequences:
  1. **Re-set the clipboard immediately before EVERY paste**, even when pasting the
     same asset repeatedly, and **screenshot after every paste**. `cmd+z` + re-set +
     re-paste fixed it every time, on the first retry.
  2. **A bad paste can inject sensitive content into the document.** After any long
     pass, export the .docx and enumerate every embedded image (size + which cue it
     sits under), not just the ones you meant to add. A stray screenshot of someone's
     bank page is a much worse defect than a missing picture.
- **Undo is per-operation.** A `Return` plus a paste is two. Undo one at a time and
  screenshot between. After undoing a bad paste, the empty paragraph is usually
  still there and correctly positioned — re-paste into it rather than pressing
  `Return` again.
- **Insert bottom-up when two targets are on screen.** Inserting at the lower one
  first keeps the upper one's coordinates valid.
- **Anchor on the END of a paragraph.** `End` goes to the end of the *visual line*,
  not the paragraph, so clicking mid-paragraph puts the image mid-paragraph.
- **Short text: type it, don't paste it.** Typing at the end of an existing note
  inherits that note's italic styling for free.
- **The Drive text export can be badly stale.** Verify structure in the live editor;
  use a Drive re-read only as the *final* check, after the "Saving…" indicator has
  gone back to the cloud icon.

## Verify before reporting

Re-download the .docx and count images per section, printing the cue above each:

```
13 images  AD 2   ← every cue accounted for, in order
 7 images  AD 1   ← unchanged
 6 images  AD 3   ← unchanged
```
Also confirm the section order and that Production notes is still last, and grep
the text for residue from any bad paste and for the banned copy rules.

## Copy and compliance rules that apply to assets

- **Never render the ChatGPT logo** (or any competitor's mark) in an asset, even
  when the cue asks for it. Use a generic glowing "AI" badge and say so in the note.
  A competitor trademark in a paid ad is a real Google/Meta review risk.
- The **AI future-self image keeps its "AI-GENERATED" tag**. Dan's real photo-shoot
  pictures need no label.
- Never write "GLP-1" or any drug name — "weight loss medication".
- Crude-photoshop gags must be generic fakes, never a real person's face.
- Never sell sleep.

## Record what you did

Write a `PLACEMENT.md` next to the assets mapping every cue → file → source
(including clip timecodes), and note what's still missing and why.

## Lessons

- **Ask before starting.** Dan explicitly wanted questions first on this workflow;
  the answers (which B-roll, how aggressive, real vs fake app shots) changed the
  whole shape of the work.
- **Look at the footage.** The first two frames sampled from the "sixpackabs.com
  rebrand" clip were Mike Chang and Thomas DeLauer. Sampling three timestamps would
  have shipped the wrong man; a 1 fps contact sheet found the truth in one look.
- **Check what the account already has before spending.** Ad 2's three app screens
  cost $0 because the demo account already had a meal plan and logged meals.
- **A missing asset is a finding, not a failure.** The Macro Tracker *result* screen
  needs one real photo of real food — say so plainly rather than faking a plate.
