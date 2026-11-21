# House style for longform graphics

Measured off the outside editor's 6:58 cut of the ab-wheel video (2026-08-24), then
recoloured to Dan's round-1 revision note: *"Make green used in graphics slightly darker,
military green that matches green used in these graphics."*

Implemented as `motionlib.MIL` in `.claude/skills/_shared/motionlib.py`. Do not
re-interpret it per video — that is how five longforms ended up with five looks.

## Colour

**His card gradient, sampled from three title-card frames:**

| | R | G | B |
|---|---|---|---|
| dark end | 84 | 93 | 55 |
| light end | 141 | 152 | 97 |
| mean | 109 | 119 | 75 |

His light end is essentially our brand `OLIVE (140,152,88)`. "Slightly darker, military
green" is therefore a stop below that, desaturated toward olive drab:

```python
MIL.field    = (13, 14, 11)     # near-black field, the J2 cover BG
MIL.field_hi = (21, 23, 18)     # the radial lift on the field
MIL.deep     = (46, 54, 32)     # gradient dark end, deep blocks
MIL.mid      = (78, 89, 50)     # plate and bar green, number chips
MIL.accent   = (104, 118, 66)   # gradient light end, rules, hairlines
MIL.ink      = (255, 255, 255)
OLIVE        = (140, 152, 88)   # brand olive: eyebrows and hairlines ONLY
```

**No red in this palette.** `hot` is the brand red everywhere else, but a red rule under a
"$17" callout on an olive/black card reads as a different brand. `MIL.hot = MIL.accent`.

## Type

Manrope throughout (`~/Library/Fonts/Manrope.ttf`), never Impact — Impact is the `/shorts`
cover face. Headlines ExtraBold, sheared 10° for the oblique caps; body Bold.

| element | size | weight |
|---|---|---|
| title-card headline | 104 | ExtraBold, oblique 10°, leading 0.98 |
| title-card subtitle | 46 | Bold, dark ink on a near-white strip |
| section label | 54 | Bold on near-white; number ExtraBold on `MIL.mid` |
| lower-third lead | 52 | ExtraBold |
| lower-third body | 46 | Bold |
| stack item | 62 | Bold, white on `(12,14,10,232)` with a 9 px `accent` bar |
| big number | 230 | ExtraBold |
| watermark | 30 | Bold, white @205, 2 px black shadow |

## Layout

* **1920×1080, 30000/1001.** Everything is an alpha QTRLE `.mov` — libx264 cannot carry
  alpha, and pre-multiplying against a guessed background is how graphics get grey fringes.
* **Corner brackets + tick marks** on every full-screen graphic (`bracket_frame`), inset
  30 px, arm length 8.5% of the short side. Corners only: a continuous rectangle reads as
  a border, brackets read as a viewfinder.
* **Inset window** `[280, 168, 1640, 933]` — 1360×765, 16:9, radius 26.
* **Phone window** `[760, 96, 1160, 940]` — 400×844, radius 42. Anything vertical uses
  this; fitted into the 16:9 window a phone recording is 352 px across and reads as lost.
* **Lower-third band** y 796–884. **Caption band** y ~950–1020 (ASS MarginV 62 at 58 px).
  Those two must not be merged — they carry different information.
* **Watermark** `AbsByAI.com` bottom-right, camel case, never all-caps.

## Timing

| element | duration | entrance |
|---|---|---|
| title card | 3.2–3.6 s | field 0.18 s, plate 0.35 s, lines stagger 0.10 s |
| section label | 3.2–3.8 s | slide 0.36 s, plate 0.30 s, text wipe 0.34 s |
| lower third | 3.4 s | bar drops 0.27 s, plate grows, text wipes |
| stack | one item per spoken name | 0.40 s each |
| big number | 2.3–2.7 s | letter-by-letter 0.36 s |

Sync every cue to the WORD that introduces it, found with a phrase search that starts
AFTER a given time — a repeated line matches the wrong occurrence otherwise.
