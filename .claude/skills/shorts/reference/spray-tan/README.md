# `spray-tan-first/` — Shorts from "01 - My First Spray Tan" (2026-09-02)

Copied from `zepbound-honest-update/` (itself copied from the supplements batch) and adapted.
Both earlier READMEs are kept beside this one — everything in them still applies; this file
records only what was DIFFERENT on this roll.

## Source

`CUT_v1_graded_NO-GRAPHICS.mp4` (1133.866 s container, 29.97 fps, **44 EDL ranges**), never the
delivered `FINAL_spraytan.mp4` and never `FINAL_spraytan_PRE_REBUILD.mp4`.

The 8/27 rebuild took the delivered master to **44 % insert coverage AND cut the locked kitchen
shot into 167 punched shots**. Cutting from it would have put someone else's crop underneath
ours and forced half of every short into a card.

⚠ **THE CLEAN MASTER CARRIES THE UNREPAIRED TWO-MIC RECORDING.** Only the delivered masters were
ever audio-fixed. Measured at t=600 s:

| file | L/R corr | best lag | dyn range L / R | verdict |
|---|---|---|---|---|
| **CLEAN master (what we cut from)** | **+0.054** | **−7.46 ms** | 44.9 / **49.3 dB** | two mics |
| delivered `FINAL_spraytan.mp4` | +0.9999 | 0.00 ms | 41.7 / 41.6 | true mono |
| `FINAL_spraytan_PRE_REBUILD.mp4` | +1.0000 | 0.00 ms | 45.0 / 45.0 | true mono |
| raw roll C1512 | +0.005 | −7.42 ms | 55.1 / **66.6 dB** | two mics |

Right channel only, as mono, as on the two previous batches.

## ⚠ The two-timeline trap fired again — and the LENGTH CHECK PASSED THE BAD WAV

`preflight.py`'s cheap detector (decoded samples vs container duration) said **both** candidate
extractions were fine: −3.8 ms and +0.9 ms. Cross-correlating each against `-ss` pulls at eight
points is what actually separated them:

| extraction | length vs container | lag vs `-ss`, 8 points |
|---|---|---|
| `aresample=async=1:first_pts=0` (the supplements recipe) | −3.8 ms ✓ | **+16.6 … +94.4 ms, wandering** |
| **`aresample=async=1:min_hard_comp=0.005:first_pts=0`** | +0.9 ms ✓ | **0.00 ms at 6 of 8, ±2.3 ms worst** |

The drift is non-monotonic — it wanders with the joins, so it is per-join pts overlap, the same
cause as the Zepbound roll. **Never accept the length check alone; always cross-correlate.** The
same filter is at the head of the renderer's audio pull (`render.js` `TIMELINE_FIX`).

## Voice chain: fitted against Muhammad's AD, and the gate DROPPED again

Fitted with `work/finalchain.py` against `Muhammad Ad Videos/this picture got me abs | muhammad
| 16x9.mp4` (indoor talking head, same rig — never the outdoor ab-wheel cut). Octave-band shape
difference **2.22 → 0.35 dB RMS**. The roll is dull: it needed **+3.1 dB at 80–160 Hz** and
**+3.8 / +5.6 dB above 5 kHz**.

⚠ **No denoiser and no gate.** Floor relative to voice, measured before deciding:

| | 80–250 Hz | 250–1 k | 1–4 k |
|---|---|---|---|
| Muhammad's ad (the reference) | 27.0 | 34.2 | 26.0 dB |
| **ours, right channel, plain** | **29.3** | **34.0** | **26.3 dB** |
| ours + `afftdn` + `agate` | 30.8 | 34.3 | 27.5 dB |

The plain right channel already matches the reference and is 2.3 dB cleaner in the low band. The
cleanup buys 0.3–1.5 dB and costs word tails, so it is not applied. Chain = right channel →
`highpass 75` → fitted 8-band EQ → de-esser, then `finishaudio.py` (pure gain + limiter, never
`loudnorm`, which falls back to dynamic mode silently when the gain exceeds the peak headroom).

## Vertical geometry

`cropTop 0`, window 738×1080 (1.46×), picture dropped to **y=340** — the same numbers as the
Zepbound roll, and for the same measured reason: **head top is source row 0** on 10 of 12 sampled
frames and rows 6–7 on the other two. The camera frames him to the top edge; his hair is slightly
clipped in the source. Any crop off the top cuts it.

⚠ **The anchor was verified on drawn frames before any number was trusted** (`work/geo/anchors.jpg`),
which is the Zepbound lesson. On THIS framing the torso block and the head agree to within 13 px of
source — unlike the Zepbound roll, where they diverged by 150 px, because there he was cut at the
waist with his arms swinging through the anchor's coverage band and here he is framed chest-up.

**His centre wanders 0.5076 → 0.5948 across the video — 167 px of source, ~245 px delivered.** That
is far above the ~35 px "invisible" threshold, so per-shot centres are not optional on this roll.

⚠ **The source already alternates its own punch.** 20 of the 44 EDL ranges carry
`crop=1728:972:96:0,scale=1920:1080` — a centred 1.111× push. So half the inherited joins carry a
framing change before ours is applied, and his apparent size changes between ranges. Per-shot
measurement absorbs both.

## Splices

44 cuts, measured at full frame rate rather than predicted (`work/splices.py`). The EDL cumsum is
early by a monotonically growing **+0.036 → +0.403 s** (render.py's per-range frame rounding).
Weakest peak 5.3×, no weak boundaries.

## ⚠ The torso anchor is bimodal here too — on ONE shot, and that is why HEAD is used

The 12-frame reconnaissance sample said head and torso agreed to within 13 px, which would have
justified either. The **per-shot** measurement over all 22 shots says otherwise:

| anchor | cross-shot spread | worst head-vs-torso divergence |
|---|---|---|
| torso block | **230 px** of source | — |
| **head (used)** | **114 px** of source | — |
| | | **E-p0-s01: 121 px** |

One shot (E's second) reproduces the Zepbound failure exactly: he gestures with the frame-right
arm and it flips in and out of the anchor's 60 %-coverage band. **A reconnaissance sample is not a
substitute for measuring every shot** — the failure is per-shot by nature, so a sparse sample can
miss it entirely. Crops are the per-shot **head** median (`work/mkcrops.py`); `work/centregate.py`
measures the same anchor on the delivered file.

## Boundaries: three of thirteen ran past a splice

`work/boundscan.py` (new here, generalised from the Zepbound scan) checks every piece boundary
against the frame-measured splice table. Three crossed and are pinned 20 ms inside:

| | boundary | splice | fix |
|---|---|---|---|
| A p2 OUT | 94.250 | 94.230 | `outAt: 94.210` |
| B OUT | 163.510 | 163.332 | `outAt: 163.312` |
| D OUT | 387.400 | 387.323 | `outAt: 387.303` |

B's IN needed the opposite treatment: `inAt: 115.805`, 20 ms **after** the splice at 115.785, so
the short does not open on a frame of the previous take. Every override still has to land inside
measured silence and is asserted to.

## Segments

| id | slug | runtime | pieces / shots |
|---|---|---|---|
| A | cameras-flatten-your-abs | 57.4 s | 4 / 4 |
| B | i-asked-ai-where-to-get-a-spray-tan | 47.5 s | 1 / 2 |
| C | wear-briefs-not-boxers | 48.8 s | 3 / 3 |
| D | never-sleep-in-a-spray-tan | 45.8 s | 1 / 2 |
| E | no-soap-no-scrubbing | 49.6 s | 1 / 2 |
| F | a-tan-with-no-sun-damage | 48.5 s | 1 / 2 |
| G | dont-go-full-donald-trump | 59.4 s | 1 / 2 |
| H | how-to-maximize-your-photo-shoot | 50.4 s | 1 / 5 |

**407 s total, all inside the 45–60 s brief, no source second used twice** (asserted in
`segments.js`; the only permitted overlap is a shared pause between two adjacent shorts).

## Not done, deliberately

* **No AI cover clips** (`inserts.js` empty) — every join is hidden by the punch alternation, and
  the source already alternates its own centred 1.111× punch across 20 of its 44 ranges.
* **No bleeps** — [B] contains "my shitty pictures". Dan's standing writing rule asks for
  profanity at peak emphasis; flagged in SHORTS.md rather than decided for him.
* **Whisper pass b** (the orphan-scan insurance) was **killed at 68 %**: another session drove the
  machine to load 294 with seven concurrent builds, and pass a plus a caption proofread is what
  the Zepbound batch shipped on too.

## One tooling fix worth keeping

`syncgate.py` had two real bugs, found by running it on a batch it had never seen:

1. It read `build/<ID>.ass`; the renderer writes `build/<ID>/<ID>.ass`. The Zepbound folder
   happened to carry stale top-level copies, so the gate had never exercised this path.
2. Its first-word-clipped test compares a `medium.en` caption against a `base.en` transcription,
   and the two models tokenise AND spell differently ("All right," vs "alright"). A word-identity
   test cannot pass that. It now falls back to a similarity ratio on the opening letters.
