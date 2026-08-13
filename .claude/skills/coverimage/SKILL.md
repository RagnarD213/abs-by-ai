---
name: coverimage
description: >
  Build the cover image (grid thumbnail) for an Abs By AI Short/Reel — pick the
  most ripped source image, crop it grid-safe, set the locked J2 tactical type,
  and deliver two variants. Use whenever Dan asks for a cover, a cover photo, a
  thumbnail for a short, or says a short's cover looks wrong — even if he doesn't
  say "/coverimage". For cutting the short itself use /shorts. For long-form
  YouTube thumbnails use /youtube-packaging. For retouching Dan's personal photos
  use /photo-edit.
---

# Cover images for Shorts

Instagram defaults a Reel's cover to frame 0, which on our shorts is the black
opening frame — an empty tile in the profile grid. Every short needs a built cover.

**The abs decide everything.** This is an abs channel; the cover sells the physique
before it sells the topic. A technically clean, perfectly on-topic image is still a
FAIL if the abs don't read. Reject and keep looking rather than shipping one.

## The rules, in priority order

1. **Prefer a photograph over a video frame.** Shoot photography is lit, posed and
   already retouched; a video frame is captured for motion, not physique. If
   `photos/finalized social media photos/` holds a shot of the same movement —
   toe touch, plank, twist, deadlift — use it. Default to photos generally, not
   only on an exact match.
2. **Abs as ripped as possible.** Sharp separation, visible obliques, good
   directional light. This outranks topic match, expression and composition.
3. **Never hunched, folded or soft.** No frame where the torso compresses at the
   waist or the posture reads heavy. Dan rejected a V4 frame for exactly this on
   2026-08-13 — it was on-topic, eyes to camera, hands clear, and still a fail.
4. **A video frame only when** no photo is relevant at all, or the video holds an
   unusually good moment. Then still pick on abs first, and retouch it (below).

Search order: `photos/finalized social media photos/` → the short's own longform.
Do **not** pull from `photos/finalized dating photos/` — retouched for dating apps,
not the brand.

## Run order

### 1. Identify the short and its topic
`YouTube Long Form Video Content/SHORTS_UPLOAD_PLAN.json` maps every short file to
its parent longform, title, hook and tags. Read the entry before choosing an image.

### 2. Find the photo
The libraries have no useful filenames (`photo-44_FINAL_PRIMARY.jpg`,
`SNAPPR Dan Rose Fitness-149.JPG`), so **look, don't grep.** Build a contact sheet
of the whole finalized folder and read it:

```python
from PIL import Image, ImageDraw
import glob, os
fs = sorted(glob.glob('photos/finalized social media photos/*.jpg'))
cols, tw, th = 6, 320, 240
rows = (len(fs) + cols - 1) // cols
sheet = Image.new('RGB', (cols*tw, rows*(th+20)), (20, 20, 20))
d = ImageDraw.Draw(sheet)
for i, f in enumerate(fs):
    im = Image.open(f); im.draft('RGB', (tw*2, th*2))
    im = im.convert('RGB'); im.thumbnail((tw, th))
    x, y = (i % cols)*tw, (i // cols)*(th+20)
    sheet.paste(im, (x, y)); d.text((x+4, y+th+3), os.path.basename(f)[:38], fill=(255,255,255))
sheet.save('sheet.png')
```

Colour-signature searches do **not** work — a greenness scan for the grass-and-mat
toe-touch photo scored it below threshold and missed it entirely. Read the sheet.

### 3. Or pull a video frame (fallback only)
Frames come from the **original longform, never the finished short** — the short has
burned-in word captions across the abs and there is no caption-free frame to steal.

Locate the topic in the longform's `*-words.json` (`chunks[].timestamp`), sample
every 4s across that section, contact-sheet it, then sample every 1.5s around the
best few. Two things that cost time on V4:
- The exercise demo itself is usually **horizontal on the mat** and crops terribly
  into a vertical cover. The talking segments before and after are upright and
  better framed.
- Some frames carry the video's own **teal overlay pill**. Either crop right of it
  (`x > 693` on the V4 source) or pick a frame that has none.

Then retouch it — see `_retouch-prompt.txt` in the covers folder for the exact
wording. `nano-banana-pro`, ~25c, in-place edit: deepen ab shadows, keep skin tone,
moles, clothing and identity, **add no size**. This is standing-authorised spend.

### 4. Set the crop
Panel aspect is `1080 / (1920 - PANEL_Y)`. Overlay a coordinate grid on the source
and read the real pixel bounds rather than guessing:

```python
p = im.resize((1600, int(1600*h/w)))
for x in range(0, p.width, 100): d.line([(x,0),(x,p.height)], fill=(255,0,0)); d.text((x+3,3), str(int(x*w/1600)), fill=(255,255,0))
```

Frame the **whole movement** when it fits — for the toe touch that is ball → arms →
face → abs, which happened to land at 0.81 aspect against the panel's 0.794.

**Keep the abs above y=1680 in the output.** The profile tile crops to 3:4 and
everything below 1680 is gone. On a lying-down subject the abs drift low; check
where they land before committing.

### 5. Build it
Copy `Short-form video content/covers/posted covers/_build-cover-short2.py` and
adapt `SRC`, the crop dict, and the copy. Do not rewrite it — it carries the locked
geometry and the asserts.

**Locked type hierarchy (Dan shipped this as cover D, 2026-08-13):**

| slot | example | font |
|---|---|---|
| eyebrow — attention-getting category | `KILLER SIX-PACK ABS EXERCISE` | Copperplate 36, olive, letterspaced |
| headline — the specific, descriptive thing | `THE TOE TOUCH` | Impact ~150, white |
| subtitle | `TARGET: LOWER ABS` | Impact ~74, olive |

The **specific** line is the big one. A generic category phrase as the headline
tests worse and looks like every other fitness account — that is why the variant
leading with `KILLER SIX-PACK ABS EXERCISE` in Impact lost.

**Copy comes from the short's own on-screen graphic first.** Screenshot the first
seconds of the short and reuse what is burned in. Only write fresh copy when the
short has no title card; then take the eyebrow from the category and the headline
from `SHORTS_UPLOAD_PLAN.json`'s title.

Deliver **two variants** — same photo, crop and frame, differing only in copy. No
approval gate before building; Dan judges the finished covers.

### 6. Verify before sending
- 1080×1920 RGB.
- Every text element between y=240 and y=1620 (the script asserts this).
- Type block clears `PANEL_Y` or the feather eats the last line (asserted).
- Headline fits the column — use the auto-fit helper, never let a line clip.
- Wordmark bottom-**right** (the grid tile paints its play count bottom-left), with
  its scrim if it lands on skin or grass, or it disappears.
- `git check-ignore` the output path before anything is staged — the repo is public
  and these are Dan's personal photos. `Short-form video content/` is ignored.

Save to `Short-form video content/covers/posted covers/` as
`<shortslug>_cover-<X>.png`, and copy the build script beside it as
`_build-cover-<shortslug>.py`. Delete superseded variants so the folder stays
unambiguous when Dan is picking a file in Finder.

## Geometry that must not drift

```
1080x1920               canvas
y 240-1680              what Instagram's 3:4 profile tile keeps
y > 1630                Reels caption row paints over this
right ~15%              Reels action buttons
PANEL_Y 560-700         photo top; type block lives above it
170px feather           photo's top edge ramped into the black, no hard seam
BG (13,14,11)  OLIVE (140,152,88)  GRID (27,30,19)  INSET 28
```

Impact and Copperplate live in `/System/Library/Fonts/Supplemental/`.
`ffmpeg`/`ffprobe` are at `Media/video_edit/bin/` — there is no system ffmpeg.

## Lessons already paid for

- **Photography beat the video frame outright.** The V4 frame was on-topic and
  clean; Dan's verdict was "looks fat, abs aren't defined." The shoot photo of the
  same exercise was better in every way and took one lookup.
- **Don't judge a frame from a thumbnail sheet alone.** Crop the top candidates to
  the subject at full resolution and compare side by side — the ab definition
  difference between adjacent frames is invisible at contact-sheet size.
- **The wordmark vanishes on skin.** Short 1's sat on black and was fine; short 2's
  lands on a sunlit torso and needed a rounded dark scrim behind it.
- **Assert, don't eyeball.** The width assert caught `LOWER AB KILLER` overflowing
  at 1078px against a 964px column before it ever rendered.
