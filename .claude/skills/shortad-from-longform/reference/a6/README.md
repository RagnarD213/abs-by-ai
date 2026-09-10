# a6 — Zeeshan's Ad 1 vertical (2026-09-10): the tools behind SKILL.md lessons [A6] 1-24

Run in this order from a build dir (paths inside are this build's; change the constants at the top of each):

| step | script | what it does |
|---|---|---|
| words | `zalign.py` | his transcript vs the raw roll's (fresh Whisper both sides), apostrophes normalised away |
| audio EDL | `zprofile.py` | dense acoustic offset profile (0.1 s hops, 0.7 s windows, 300-3400 Hz) |
| framing | `zfit.py` | his framing (scale, x, y) per 6th frame via `cv2.matchTemplate` over scales |
| picture | `zpic2.py` | per-frame raw index of every talk frame (256x144 caches, `warpAffine`, NCC) |
| EDL | `zedl.py` -> `zedl2.py` -> `zedl3.py` | offsets from audio, cut frames from the picture crossover; bridge + trim |
| overlays | `zov.py` | his overlay in/out frames by residual against the raw, and his one-frame flashes |
| media | `zmatch.py` | in-points/rates of his AI clips, his app-recording time map, his scroll |
| grade | `zlut.py` | his grade as a 33^3 LUT from pixel correspondences (`his.cube`) |
| conform | `zbase.py` | the talk picture on HIS fps grid, LUT-graded, BT.709-tagged, frame count asserted |
| hair/torso | `zmeasure.py`, `zhair.py` | Vision torso anchor + hair top relative to what is above it |
| crop | `zcrop.py` | hair-anchored NEAR/FAR; the level changes only at joins VISIBLE in his cut (his change > 3x local), a run's opening level chosen by measured drift, zero-phase torso track |
| look | `zgfx.py` | his design tokens and graphics rebuilt for 1080x1920 |
| assets | `zassets.py` | lifts from his render (clear of burned labels/CTA), app recording on his time map |
| picture | `zrender.py` | the Python frame compositor (`--stills`, `--cutplan`, full) |
| mux | `zmux.py` | picture copied + his finished mix at AAC 320k, both streams asserted |
| cutdown | `zcutdown.py`, `zcut_build.py` | the <=0:59 plan (edges away from words, J-cut leads, seam flips) and its build dir |
| gates | `zhairgate.py`, `zwatch_sheets.py`, `zwatch_mark.py` | delivered-frame hair gate; watch strips as sheets; the human watch record |

`beats_zee_ad1.py` and `captions_zee_ad1.py` are the build's beat sheet and caption builder, as examples (the caption
builder names each state image by its content -- lesson 24). `watch_zee_ad1.py` is the build's watch pass at 24 fps; its
boundaries include every overlay SUB-ELEMENT's in-time (subtitles, checklist items, an end card's second line) -- lesson 19a.
