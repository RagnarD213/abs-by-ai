# Reference pipelines

Working code from the two shorts builds, kept in git because the folders they ran in
(`YouTube Long Form Video Content/`, `Short-form video content/`) are git-ignored and the
original V4 pipeline was already lost that way once.

**Copy a directory into `YouTube Long Form Video Content/<slug>/` and adapt.** Do not
rewrite from scratch.

## Which one

| | `full-bleed/` | `band/` |
|---|---|---|
| Built for | V2 "six ways AI abs", 7 shorts, 56 shots | V4 short1 rebuild, 1 short, 6 shots |
| Footage | full-bleed 9:16 crop | lower ~74%, graphics band on top |
| Use when | some region of frame is reliably clear of the subject | nothing is clear — measure first (Step 6) |
| Graphics | cards + repositioned PiP inside the full-bleed frame | dedicated band, one chip at a time |

`full-bleed/` is the more complete pipeline (multi-segment, automated QC).
`band/` is the better layout when the subject fills the frame.

## Run order

**full-bleed**
1. `silencedetect` → `silence.txt` (see SKILL.md Step 3)
2. `node segments.js` — phrase → silence-snapped cut points; asserts every cut is in silence
3. `node detect-shots.js` — scene detection + one frame per shot → `shots/manifest.json`
4. `python3 contact-sheet.py` — labelled sheets with the 9:16 window drawn on; classify by eye
5. edit `plan.js` (per-shot treatment + hand offsets), then **re-run** `choose-crops.py`
6. `python3 choose-crops.py` → `crops.json` + `review-crops.jpg` — **look at the sheet**
7. `python3 build-assets.py` — bg, wordmark, titles, chips; asserts title clearance
8. `python3 preview.py` — one still per treatment using the SAME geometry render.js uses
9. `node render.js [IDS...]` → `out/`
10. `node qc.js` — specs, duration, black frames, caption bounds, splice click test

**band**
1. `silencedetect` → `silence.txt`
2. `node plan.js` — segment + chip windows + shot detection → `shots.json`
3. `python3 crops.py` (or hand-set `x` in `layout.json` — automation failed on this footage)
4. `python3 assets.py` — bg, header, wordmark, one chip per reveal
5. `node render.js`

## Adapt these first

- **Paths.** Every script resolves `ffmpeg` at
  `../../ad-factory/the-upload/node_modules/ffmpeg-static/ffmpeg` and `ffprobe` at
  `../../Media/video_edit/bin/ffprobe`, relative to the work folder. There is no system
  ffmpeg on this Mac.
- **Source filename + words json** at the top of `segments.js` / `plan.js`.
- **`layout.json`** — all frame geometry. `preview.py` and `render.js` both read it, so what
  is reviewed is what gets encoded. Keep it that way.
- **Phrase strings** in `segments.js` are matched against normalised text: apostrophes are
  stripped, so write `"Here's another way"` as it is spoken, not `"Here is another way"`.
