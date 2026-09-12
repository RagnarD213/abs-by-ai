# `a10_sq/` — the first SQUARE (1:1) build: Ad 2, 2026-09-11

A 1:1 re-layout of an **approved 9:16 vertical**, not a third recovery of the editor's cut. Read
`Handoffs/handoff-20260911-square-ads-00-shared-rules.md`, then SKILL.md **[A9]**, then this.

| file | what it is | reuse it? |
|---|---|---|
| `vlib.py` | the square layout library: safe area, `window_rect`/`window_crop`, `card_hole`, the media-left/Dan-right split, the overlays | **yes** — the geometry is generic to 1:1 |
| `render.py` | the square renderer: `CROP_W = 1080`, the face track shifted by `(608-1080)/2`, no unsharp on a 1.00x crop, `bleed_sharpen()` | **yes** for any a4/a5-pipeline ad |
| `muxsq.py` | mux that copies the APPROVED VERTICAL's AAC stream and **asserts its md5** before writing | **yes**, change `VERT` |
| `hairgate_sq.py` | the a7 hair gate's two answerable tests, bounds scaled to 1080 tall, the two it cannot answer declared | **yes** |
| `jumpcuts_sq.py` | step 7c structurally: which splices the square leaves bare that the approved vertical covered | **yes** |
| `sqstills.py` | one frame of a media key at 1080x1080 exactly as `render.py` would — the cheap way to settle `ox`/`oy` before a build | **yes** |
| `zwatch_mark.py` | writes the watch-pass record with a hand-written note of which strips were re-looked at | **yes** |
| `qc.json` | the square's per-cut numbers, and why `audio_mode` is NOT verbatim here | template |
| `beats.py` `assets.py` `captions.py` `deliver_sq.py` `centering.py` `landing_check.py` `watch.py` | Ad 2 specific, but the diffs against the 9:16 originals are the point | read the diffs |

## The one thing to internalise before you start

**A full-height window in a 1080-tall frame is always 1.00x, whatever its width.** The crop is 1080
tall and the window is 1080 tall, so the magnification is fixed; a narrower window shows LESS of
the subject, not a wider shot. Muhammad's own 16:9 split gets away with a full-height window only
because his is 945 px of 1920. Size any window beside other content from the MAGNIFICATION you
want, then derive its height: `win_h = win_w * 1080 / (win_w / mag)`.

## The order that worked

```
cp -R <ad>-vert <ad>-sq            # never build inside the vertical's dir; keep *_9x16_orig.py to diff
sqstills.py <key>[:ox[:oy]] ...    # settle every full-bleed crop BEFORE rendering
render.py --selftest               # the crop expression, at 1080 wide
render.py --only <a few beats>     # look at them at full resolution
render.py ; captions.py ; muxsq.py
watch.py + sheets + zwatch_mark.py ; centering.py ; landing_check.py ; hairgate_sq.py ;
caption_sync_check.py ; jumpcuts_sq.py ; qc.py --build-dir .
the independent audit, then deliver_sq.py
```
