# website-video/ — the post-generation conversion video (2026-09-01, 8/28 shoot, C1650+C1651)

The first cut from the 8/28 shoot and the first TRUST-tuned edit: plays on absbyai.com right
after a visitor generates their goal image. Same pipeline shape as `../rev5` and the Ad 3 dir
(`/Volumes/Extreme/_edit_work/ads234-8-14/c1593/`), with these differences:

| file | what is new |
|---|---|
| `make_lut.py` | **S-Log3 / S-Gamut3.Cine → Rec709 33³ .cube built in numpy** (Sony transfer, gamut matrix, soft shoulder). The 8/28 shoot is the first in this format; `lut3d=...:interp=tetrahedral` in `grade.txt`, exposure 1.45×, saturation 0.88. |
| `edl.py` | phrase-anchored spans across TWO rolls, edges validated against a −40 dB envelope |
| `base.py` | multi-source concat; **a:1 is the lav** (4 mono LPCM tracks on this shoot); renders **2560×1440** so the 1.30 punch never upscales |
| `tight.py` | calmer pause pass: pauses ≥0.30 s shortened to ~0.30 s, never removed |
| `layout.py` | 3 levels, 9 s minimum hold, hard splices covered hardest-first with a 3.5 s floor, phone panels LEFT with Dan in the right column |
| `audio2.py` | **gain + alimiter instead of loudnorm** (loudnorm fell back to DYNAMIC on this mix); limiter delay measured (239 samples) and removed; no SFX bed |
| `gfx.py` | J2AD palette, slow drifts, "Results are not guaranteed." on real-physique cards, heading-width assert, CTA card that HOLDS to the last frame |

Numbers on the delivered file: 3:51.56, −14.2 LUFS, TP −2.2 dBTP, L/R +0.9986, 203 wpm,
fidelity 99.0 %, 47 visual changes, median hold 5.1 s, longest 13.7 s, coverage 54 %.
