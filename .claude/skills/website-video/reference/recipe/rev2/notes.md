# Website conversion video — 16:9 master, REVISION 2

**Rev 1 was rejected 2026-09-02** on audio, framing and graphics, in that order. Rev 2 keeps rev 1's
cut, transcript, EDL and grade (Dan: "the color correction is looking good, the footage looks good")
and rebuilds the three rejected things from measurements. **$0.00 AI generation spend** — every
asset already existed. No production code, no deploy, no native-retest trigger.

| | |
|---|---|
| master | `website_video_16x9.mp4` — **3:51.56**, 1920×1080, 29.97 fps, AAC 256k |
| review copy | `REVIEW_540p_website_video.mp4` |
| audio A/B | `AB_his-vs-ours.mp4` — 12 s of Muhammad's ad, then the same 12 s window of ours |
| audio gate | `voice_ref_check.py` **PASSED** on the delivered file (numbers below) |
| loudness | −14.5 LUFS · true peak −2.5 dBTP · LRA 2.8 LU · voice centred (L/R +0.9999) · **0 silent seconds** on master and review copy |
| framing | three levels, 1.256× / 1.45× / 1.66× on the 4K source — the wide shot and the light never appear |
| graphics | 13 beats (rev 1 had 21): 6 lower thirds, 6 full-frame cards on Muhammad's olive plate, 1 phone PiP |
| script fidelity | **98.7 %** re-transcribed off the finished render |
| gate | QC **14/14 PASSED**, watch pass on the delivered file, contact sheet at 1 frame / 5 s checked for the light / wide shot / black fields |

## 1 — Audio: what was wrong and what changed

Dan heard "the two-channel issue". Measured, it was not — rev 1 read L/R +0.998. It was the **floor**:
the bed at −23 dB, a 3:1 compressor with makeup and two air shelves lifted everything between the words
**9.5 dB above Muhammad's ad**, while the raw lav on its own was 4–5 dB *cleaner* than his.

| voice over floor (dB) | 80–250 Hz | 250 Hz–1 k | 1–4 kHz |
|---|---|---|---|
| Muhammad's ad | 27.6 | 34.7 | 28.0 |
| rev 1 delivered | 18.1 | 25.1 | 20.2 |
| raw lav, untouched | 32.5 | 38.8 | 31.5 |
| **rev 2 delivered** | **30.2** | **35.0** | **28.6** |

Rev 2 chain (`audio3.py`), fitted with `voicefit.py` against his ad using the gate's own metric:

- **EQ fitted to HIS file** (10 bands, iterated because parametric bands interact): fill the thin
  150–250 Hz (+2.7), pull the 600–900 Hz honk (−5.1) and the 1.4–2.2 kHz edge (−3.3), put back the
  air the lav does not have (+7.9 dB above 6.5 kHz). Tone error vs his ad: **0.80 dB mean, 2.10 max**
  (rev 1: 1.70 / 2.83; raw lav: 2.58 / 7.81). Later fit iterations reached 0.30 dB only by alternating
  +4/−3/+1.5/−7 on neighbouring bands — an over-fit comb — so the smooth second iteration ships.
- **No compressor.** A gentle downward expander (1.8:1, 9 dB range) takes the room back between words.
- **Bed at −44 dB** (rev 1: −23). Measured, not guessed: −30 fails the floor by 8 dB, −34 by 5.6, −40 passes
  1.9 dB dirtier than his, **−44 lands on his floor** (+2.6 / +0.2 / +0.6 dB). Every 4 dB of bed is ~2.5 dB
  of floor. Same Pixabay `acoustic_bg` track, sidechain-ducked.
- Loudness finish is the measured gain + limiter (`audio2.py` method, never `loudnorm`).

## 2 — Framing: never the wide shot, never the light

Read off the 4K frame with a burned grid (Dan centred at x≈1980, head top y≈100, navel ≈1290, shorts
≈1580, counter ≈1720, the light's first bright pixel at x=3672):

| level | crop of 3840×2160 | zoom | shows |
|---|---|---|---|
| WIDE (the widest allowed) | 3058×1720 @ (451,40) | 1.256× | top of head → shorts, counter barely visible |
| MID | 2650×1490 @ (655,40) | 1.45× | head → hips |
| TIGHT | 2312×1300 @ (824,40) | 1.66× | head → belly button |
| PIP | 3058×1720 @ (0,40) | 1.256× | WIDE with Dan pushed to 65 % so the phone sits beside him |

The base is re-rendered at the full 4K so even TIGHT is a downscale. `layout.py` asserts every level
is no wider than WIDE and never reaches x>3530; `qc.py` re-asserts it on the plan. TIGHT is used for
8 of 18 holds, MID 5, WIDE 4 (one of them under the photo cards). Holds 9–21 s, eyeline fixed.

## 3 — Graphics: 21 beats → 13, on Muhammad's measured card system

Removed: the pool photo, the assessment / workout / meal-plan / daily-brief screenshots, and all three
bullet panels. Kept unchanged: the six lower thirds. Rebuilt on his system, pixel-measured off his ad:
near-black olive grid field, an olive plate 1476×924 (photos) / 1497×764 (titles) that fills ~75 % of
the frame width, the photo inset 28 px with rounded corners, oblique ExtraBold caps at 0.88 leading.

| time | beat | treatment |
|---|---|---|
| 0:03 | NAME | lower third — Dan Rose / Founder, Abs by AI |
| 0:31 | BEFORE | his 200 lb photo on the plate, ON "Now I've been out of shape"; gone 0.5 s before the next card |
| 0:34 | TODAY | **Muhammad's four shoot photos** in sequence, ~2 s each, over "now at 40 … six-pack abs" |
| 0:51 | NUM1 | lower third — 1 — AI tracks your macros for you |
| 0:57 | MACRO | the real macro-tracker recording as a **phone beside Dan in the footage** (433×820, hairline + shadow), photo → analyzing → itemized |
| 1:18 | FLYBLIND | lower third |
| 1:25 | NUM2 | lower third |
| 2:17 | NUM3 | lower third |
| 2:58 | TRIAL | title card — TRY ABS BY AI / FREE FOR 7 DAYS |
| 3:12 | CANCEL | lower third |
| 3:22 | PRICE | title card — $19.99 / PER MONTH |
| 3:36 | SOLVED | his AI goal image on the plate, AI-GENERATED tag on the photo's corner |
| 3:47 | CTA | title card — TRY ABS BY AI / FOR FREE, holds to the last frame |

## Compliance

- Before and after photos never share a frame: the before card is fully out 0.5 s before the first
  after photo fades in (Dan on camera between them).
- AI-GENERATED on the only AI image (SOLVED). "Results are not guaranteed." on the shoot-photo run.
- The generate-future-self recording (banned "Meet the new you" + email form) is not used; QC
  template-scans every delivered frame against both screens in the phone window.
- No drug names. No email form. No photo-crop screen. No stick-figure workout screen.

## Recipe

`edl.py` → `base.py` (4K, grade + lav) → `env.py` → `tight.py` → `hard_splices.py` → `beats.py` →
`gfx2.py` (cards) + `layout.py pip` (phone) → `layout.py punch|mix` → `audio3.py` (bed −44) →
`captions.py` → `deliver.sh` (gate + A/B, contact sheet, `qc.py`, `watch.py`, review copy).
Audio fit: `voicefit.py fit`. Working dir `/Volumes/Extreme/_edit_work/website-video-828/`;
rev 1's intermediates and scripts are in `rev1/`.
