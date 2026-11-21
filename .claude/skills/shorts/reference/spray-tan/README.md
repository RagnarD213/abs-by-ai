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

---

# REV 1 (2026-09-02) — Dan rejected the audio. The cause was the ROOM, not the channel.

His words: *"The audio is no good… I believe it's the same two-channel issue… we only want to
use the right channel in mono."* **Measured on the delivered file, against the source put through
the identical EQ chain:**

| candidate | correlation |
|---|---|
| **RIGHT channel only + same EQ** | **+0.9912** |
| LEFT only + same EQ | +0.5965 |
| L+R sum + same EQ | +0.6877 |

The single-mic fix was already applied. **The real gap is reverb**, and nothing in the pipeline
had ever measured it:

| | early decay time | octave shape vs his ad | floor under voice |
|---|---|---|---|
| shipped (rejected) | **85 ms** | 0.74–0.86 dB | 36.0 dB |
| **rev 1 (delivered)** | **29–40 ms** | **0.17–1.08 dB** | 46–53 dB |
| his reference ad | 40 ms | — | 36.2 dB |

Also ruled out with evidence: a music bed masking his room (his EDT is 37 ms even high-passed at
250 Hz, so his voice is genuinely dry), noise floor, level, clipping.

**Fix:** `work/dereverb.py` — spectral subtraction of the late field, run on the concatenated
`audio.wav` before the mux (`alpha=0.62 d1_ms=20 d2_ms=150 floor_db=-24 smooth=0.30`). ffmpeg has
no dereverb filter and `arnndn` has no model here; a broadband expander only reached 63 ms and
pumped. `floor_db` is the lever — raising `alpha` past 0.62 makes EDT *worse*.

**New hard gate:** `work/audiogate.py`, wired into `qc.js`. EDT ≤ 55 ms, shape ≤ 1.00 dB, floor
within 3 dB of the reference — measured on the delivered file.

## Three bugs this rev found, all of which had shipped or would have

1. ⚠ **A stereo WAV read as mono is invisible to a byte-size check.** The first dereverb build
   read `audio.wav` ignoring `nchannels`; on a dual-mono file that treats L,R,L,R as consecutive
   samples — a zero-order hold, i.e. a savage lowpass. The shorts came back **11–16 dB down above
   450 Hz** and the guard passed, because a mono file with twice the frames is byte-identical in
   size. Now de-interleaved on read, and `render.js` asserts **duration and channel count** via
   ffprobe.
2. ⚠ **`finishaudio.py` matched the batch to its own MEDIAN.** That only makes the shorts
   consistent with each other; it has no authority over whether they are right, and it fought the
   post-dereverb EQ. It now targets Muhammad's ad directly.
3. ⚠ **It PREDICTED its EQ instead of verifying it.** One-octave `equalizer` filters overlap, so
   the achieved response is a smeared version of the gains requested — it reported 0.3–1.3 dB
   while the delivered files measured 1.2–3.0. It now encodes, measures the **real output**, and
   folds the residual back in, **damped by half and keeping the best iterate** (undamped feedback
   diverged: F went 2.2 → 6.5 dB).

⚠ **A 9–14 kHz band was added to the corrector and REVERTED.** It sits ~47 dB below the peak
band, overlaps 6.7 kHz so heavily that the loop diverged, and was never audible. The gate and the
corrector now measure the same seven bands and select frames at the same percentile — when they
disagreed, they disagreed by up to 0.9 dB and sent me chasing a phantom.

## Dan's content revisions, all applied

Killed **C** (wear briefs, not boxers) and **E** (no soap, no scrubbing) — *"no value, no reason
for anybody to watch."* **A** retitled *Why Tanning Makes You Look More Ripped* / eyebrow *Look
better in fitness photos*. **H** eyebrow → *Fitness photo shoot tips*. 4, 5, 6, 7 unchanged.
Six shorts, delivered in his order.

## Known, and reported rather than buried

**Short 2 (B) measures 1.08 dB shape against a 1.00 gate** — the entire residual is one band,
**2.7 dB bright at 6.7 kHz**; every other band is within 0.8 dB, and its EDT is 37 ms. The
iterative fit chose this as its best; forcing it further destabilised other shorts. Flagged rather
than fudged, and the gate threshold was deliberately NOT relaxed to hide it.
