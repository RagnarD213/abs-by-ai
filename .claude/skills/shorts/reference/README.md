# Reference pipelines

Working code from the two shorts builds, kept in git because the folders they ran in
(`YouTube Long Form Video Content/`, `Short-form video content/`) are git-ignored and the
original V4 pipeline was already lost that way once.

**Copy a directory into `YouTube Long Form Video Content/<video folder>/working files/` and adapt.** Do not
rewrite from scratch.

## Which one (index corrected 2026-09-02)

| directory | built for | status |
|---|---|---|
| **`zeeshan-master/`** | SL-04 Arms & Shoulders, cut from an EDITOR'S finished 16:9 master (2026-09-24) | **CURRENT for editor masters.** His audio verbatim at 320k, three row-0 windows + inset cards for his graphics, CTC caption timing, delivered-ASR gate evidence. Read its README |
| **`clean-master/`** | supplements (03) batch, 8/3 shoot, cut from the NO-GRAPHICS master | **CURRENT.** Multi-segment, raw-roll inserts, bleeps, `finishaudio.py` = the shared audio chain + gate per short, `deliver.js` requires the stamp. Its `qc.js` and `syncgate.py` were deleted 2026-09-16: the delivery gate `_shared/deliver/gate.py` (caption sync included) replaced them |
| **`zepbound/`** | Zepbound (02) batch | **CURRENT** — clean-master plus the title-ink clearance check (his head sits at source row 0) |
| **`spray-tan/`** | spray-tan (01) batch, rev 1 | the audio lessons: room measurement (EDT), dereverb, bounds scan. Its `audiogate.py`/`dereverb.py` are now shims to `_shared/audio` |
| `recentre/` | the 8/27 centring fix | the person-mask centring gate |
| `band/` | V4 short1 rebuild | the band layout when the subject fills the frame |
| `full-bleed/` | V2 "six ways AI abs" | picture code only — **DO NOT USE FOR AUDIO** |
| `scored-source/` | ab-wheel batch (cut from a scored, finished edit) | picture code only — **DO NOT USE FOR AUDIO** |

**Audio is not per-pipeline any more.** Every `render.js` pulls the lav per `pick_lav.py`'s
`audio_source.json`; `finishaudio.py` (clean-master/zepbound/spray-tan) runs
`.claude/skills/_shared/audio/voice_chain.py` then `audio_gate.py` on every short; `deliver.js` and the
delivery gate (`python3 .claude/skills/_shared/deliver/gate.py <short.mp4> --format short --plan plan.json`)
refuse a short without the gate's stamp. The per-pipeline `qc.js` and `syncgate.py` copies were deleted
2026-09-16; the delivery gate is the only QC. `full-bleed/` and `scored-source/` were never given a chain —
they pulled the default stream with no channel selection — so their output fails the gate unstamped.
Copy `clean-master/` for a new batch.

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
10. `python3 .claude/skills/_shared/deliver/gate.py out/<short>.mp4 --format short --plan plan.json` — the
    delivery gate (specs, duration, black frames, caption bounds and sync, splices, audio stamp). The old
    `qc.js` was deleted 2026-09-16.

**band**
1. `silencedetect` → `silence.txt`
2. `node plan.js` — segment + chip windows + shot detection → `shots.json`
3. `python3 crops.py` (or hand-set `x` in `layout.json` — automation failed on this footage)
4. `python3 assets.py` — bg, header, wordmark, one chip per reveal
5. `node render.js`

## Adapt these first

- **Paths.** `ffmpeg` is ALWAYS `Media/video_edit/bin/ffmpeg` (the render-queue wrapper, VIDEO-RULES
  "Video builds: the render queue", 2026-10-20) and `ffprobe` is `Media/video_edit/bin/ffprobe`. The
  current pipelines (`zeeshan-master/`, `clean-master/`, `zepbound/`, `scored-source/`) already resolve
  `FF` there in `config.js`. The two oldest, `full-bleed/` (`render.js`, `detect-shots.js`, `preview.py`)
  and `band/` (`plan.js`, `crops.py`), still hard-code
  `ad-factory/the-upload/node_modules/ffmpeg-static/ffmpeg`, which bypasses the queue: re-point that
  line before running a copy. Never call `ffmpeg-static` or `ffmpeg.real` directly. There is no system
  ffmpeg on this Mac.
- **Source filename + words json** at the top of `segments.js` / `plan.js`.
- **`layout.json`** — all frame geometry. `preview.py` and `render.js` both read it, so what
  is reviewed is what gets encoded. Keep it that way.
- **Phrase strings** in `segments.js` are matched against normalised text: apostrophes are
  stripped, so write `"Here's another way"` as it is spoken, not `"Here is another way"`.
