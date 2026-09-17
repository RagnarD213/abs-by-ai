# 8/28 shoot — footage report from the first edit (RA-01, 2026-09-16)

**Status: DRAFT — the planner's own measurements are in; the editor's per-hold numbers are marked `[editor]` and are
filled in from `measurements-RA-01.json` when round 1 lands.**

Written from the first edit of any 8/28 footage: RA-01 "The AI Trick That Got Me Abs", cut from roll C1663. Everything
here was measured on the files, not remembered. Where an existing note (memory `shoot-828-slog3-format`, the RA job
docs) says something different, this report is the correction.

## 1. What the shoot actually is — three different roll families

| rolls | camera | audio streams | what |
|---|---|---|---|
| C1650–C1653 | landscape 3840×2160 | **four mono** LPCM (lav on `a:1`, far mic `a:0`, `a:2`/`a:3` silent) | website conversion video (C1650/51), long-form talking (C1652/53) |
| **C1654–C1672** | **portrait** — stored 3840×2160 with rotation side-data −90, decoded as **2160×3840** | **one stereo stream, dual-mono** (L = R, the lav on both) | the 16 short-form ads and the dedicated shorts (C1663 = RA-01 + RA-02) |
| C1673–C1685 | landscape | one stereo stream | exercise b-roll |

Consequences for every edit of the middle family:

* **The camera was physically rotated.** ffmpeg autorotates on decode, so a probe of the stored stream reads 3840×2160
  while the decoded frame is 2160×3840. Never pass `-noautorotate` and never add a `transpose`. The job docs' line
  "filmed horizontal and centre-safe for vertical crops" is wrong for these rolls: they are **native vertical**.
* **`pick_lav.py` must run per file and its JSON must be used.** On C1663 it reports one stream, two channels
  correlating +1.000 at lag 0 (one signal), SNR 47.5 dB, RMS −25.2 dBFS, zero clipped samples, and prescribes
  `-map 0:a:0 -af "pan=mono|c0=0.5*c0+0.5*c1"`. The "lav on a:1" rule from the memory would map a stream that does
  not exist here.
* Memory `shoot-828-slog3-format` is being amended to say this (it currently generalises the four-track layout to
  "C1650–C1685").

## 2. Colour conversion

* S-Log3 / S-Gamut3.Cine as expected. The approved conversion (`/Volumes/Extreme/_edit_work/website-video-828/grade.txt`)
  is the numpy-built 33³ LUT at exposure 1.45× plus `eq=saturation=0.88`, decoded BT.709. It was fitted on the indoor
  kitchen set; C1663 is **outdoors, overcast, by the pool**.
* On the planner's four test frames the 1.45× LUT gives believable skin and a slightly flat, cool image with the sky
  close to clipping and visible grain in the tree canopy (the push lifts the shadows). Exposure choice among
  1.35 / 1.45 / 1.55 and the measured face luma/chroma against an approved indoor frame: `[editor]`.
* Sky clip % and flat-patch noise sd: `[editor]`.

## 3. Which mic track was clean

The lav, and it is the only useful signal: both channels of the single stream carry it identically. Noise floor
between words, decay/EDT from the audio gate, and any wind or rain events (the crew mentions raindrops at 1:38 on
C1663, right after the RA-01 pass ends): `[editor]`.

## 4. Vertical-crop headroom and how big Dan is in frame

Dan stands full-body, shirtless, centred, with feet on a tape mark. From the planner's frames (2160×3840 decoded):
hair top ≈ y 780 (≈ 20 % down), belly button ≈ y 1620, shorts waistband ≈ y 1720, feet ≈ y 2600; he spans only
≈ 35 % of the frame width. There is plenty of headroom — the opposite of the 8/14 kitchen rolls, where the hair sat
19–45 px from the top edge.

The cost is resolution. The hair-anchored levels are crops of a portrait 4K frame:

| level | crop (est.) | delivered 1080×1920 | upscale |
|---|---|---|---|
| FAR (hair → shorts line) | ≈ 562×1000 | 1080×1920 | ≈ 1.9× |
| NEAR (hair → belly button) | ≈ 472×840 | 1080×1920 | ≈ 2.3× |

Measured per-hold values, the delivered face sharpness (Laplacian variance) against the approved Ad 1 vertical, and
whether the upscale is visible on a phone: `[editor]`. The 16:9 is the easier case (≈ 1.0–1.3×).

## 5. Focus and exposure

At native scale the face is sharp (hair strands and the glasses edge resolve). Exposure is S-Log3-normal — flat until
converted — with the overcast sky the only near-clipped region. `[editor]` adds the histogram numbers.

## 6. Lighting

Overcast daylight, soft, no hard shadow side; the background (pool, stone wall, trees) is busier and brighter than an
indoor set, so chips and captions need their own contrast (a plate or outline), which the J2 chip style provides.
Sky-to-face luma ratio: `[editor]`.

## 7. Teleprompter eyeline

Dan reads the ads off a prompter outdoors. On the planner's frames his eyes are on the lens axis with no visible
down-and-left reading offset; the editor's yaw/pitch estimate per hold: `[editor]`. One full pass per script with a
single retake (L5) and one false start, then straight into the next script — the crew chatter between scripts is the
only cutting room floor.

## 8. Change at the next shoot

1. **Frame tighter for the vertical rolls.** Dan is ≈ 35 % of the frame width; a hair-to-waistband framing straight
   out of the camera would deliver the FAR level at ≈ 1.0× instead of ≈ 1.9×. Keep 4 % headroom above the hair,
   not 20 %.
2. **Record the same audio layout on every roll**, or write the layout on the slate. Two families on one day cost a
   wrong memory and a wrong job doc; `pick_lav.py` caught it, a hard-coded map would not have.
3. **Say on the slate whether the camera is rotated.** Rotation side-data is easy to miss in a probe.
4. **One more full pass per ad script.** With a single pass, take selection is forced and any flub is in the ad.
5. **Expose S-Log3 a stop brighter outdoors** (or use a lower push) — the 1.45× push shows grain in shadow areas.
6. Keep the tape mark and the fixed full-body position: it makes the per-hold fixed centre trivial.

---

# Part B — the dedicated-shorts talking roll and the exercise b-roll (DS-04, 2026-09-16)

**Status: DRAFT — the planner's measurements are in; per-hold numbers marked `[editor]` are filled from
`measurements-DS-04.json` when DS-04 round 1 lands.** Written from the second edit of 8/28 footage: DS-04 "The Only
Ab Exercise That Shrinks Your Belly Fat", cut from talking roll C1656 with b-roll from C1677 (vacuum) and C1682
(crunch, toe touches). Every number below was measured on the files.

## B1. C1656 — a dedicated-short talking roll, same family as C1663

* **Portrait like C1663**: stored 3840×2160, rotation side-data −90, decodes to 2160×3840. Same rule: never
  `-noautorotate`, never a `transpose`. The DS job docs' line "framed horizontal and centre-safe for vertical crops"
  is wrong for every dedicated short on C1654–C1672.
* **Audio: one stereo stream, dual-mono** (channels correlate +1.000 at lag 0). `pick_lav.py`: SNR 42.4 dB, RMS
  −26.8 dBFS, dryness 7.7 dB, EDT 26.7 ms, 0 clipped samples. Outdoors, so no dereverb is ever needed on this
  family. Noise floor between words and wind/crew events: `[editor]`.
* **Dan is bigger in frame than on C1663.** Face skin starts at y ≈ 1020–1160 of 3840 (hair top ≈ 25–29 % down,
  against ≈ 20 % on C1663); belly button ≈ y 2070, waistband ≈ y 2230, shoes ≈ y 3300; he spans ≈ 40 % of the width.
  The hair-anchored crops cost less resolution here:

  | level | crop (est.) | into the 1080×1540 picture window | scale |
  |---|---|---|---|
  | NEAR (hair → belly button) | ≈ 813×1160 | 1080×1540 | ≈ 1.33× |
  | FAR (hair → shorts line) | ≈ 932×1330 | 1080×1540 | ≈ 1.16× |

  Per-hold hair tops, delivered face sharpness against the approved Ad 1 vertical: `[editor]`.
* **The hair detector does not work against trees.** `hairdet.py` assumes a bright wall above the head; on this
  roll the trees behind Dan are darker than his hair, so it returns a hair row 800 px too high and "climb too long".
  The skin-top it reports is right; the hair top has to be found as the last dark run within ~150 px above it and
  proven on a native-scale proof sheet.
* **Takes: one pass per line, no safety.** Lines 1–10 in one 35 s pass (0:09–0:44), then three attempts at the
  "Remember, the vacuum does not burn fat…" line (two stopped short, the third is the only complete one), then the
  close. Whisper heard no "Try" at the start of the CTA line — `[editor]` confirms on the audio. A single fluffed
  word in the hook or the CTA would have had no replacement.
* Grade: the indoor-fitted 1.45× LUT again; exposure chosen and face luma/chroma: `[editor]`.

## B2. C1677 — the vacuum b-roll Dan asked the script to film

* Landscape 3840×2160, 205 s, S-Log3, stereo crew audio. **Shot in hard afternoon sun** (the talking roll is
  overcast): one side of his face and torso is lit, the other in shadow, the wall behind him near clipping. The
  vacuum reads well because the side light draws the drawn-in stomach, but the b-roll and the talking head will not
  match in colour or contrast inside one short without a per-clip trim. Lit/shadow face luma and the wall clip:
  `[editor]`.
* Three usable passes: front hands-on-hips holds 0:00–0:28, a **profile pass 0:47–0:80 that performs the script's
  own cue in real time** (slump 0:50–0:55, straighten 0:56, draw in 0:57–0:61, hold to 0:70), and front holds
  1:40–2:52. Between them **100+ s of empty frame** (0:30–0:46, 0:81–1:39, 2:53–3:25).
* He fits a hair-to-thigh vertical crop out of the 16:9 (≈ 1500 px tall → ≈ 1.0–1.3× into the window), so the
  standing vacuum needs no J2 frame. Crop and scale used: `[editor]`.

## B3. C1673–C1685 — the exercise b-roll

| rolls | set | light | what | vertical-usable? |
|---|---|---|---|---|
| C1673–C1676 | hot-tub pool, tape mark | hard side sun | kettlebell swings, skipping, dumbbell curls/presses, seated presses, RDLs, bent rows — standing, full body, Dan ≈ 25 % of frame height | yes as a tight crop, ≈ 1.5–2× upscale |
| C1677 | same | same | vacuum (B2) | yes |
| C1678 | same | same | 33 s, mat: push-up / plank | no — lying, needs a card |
| C1679–C1683 | the other pool, blue mat, camera at ground level | warm low sun, then shade | kneeling ab-wheel rollouts (C1679), leg raises + planks (C1680), push-up variants with a chair (C1681), **crunches 0:57–0:61 and toe touches 0:62–0:79, 1:26–1:39 (C1682)**, seated medicine-ball twists, planks, rollouts (C1683) | no for every lying/kneeling move — a 9:16 crop slices the body; they go in as 4:3 cards on the J2 field |
| C1684 | covered patio | shade, dim | handstand push-ups | no |
| C1685 | covered patio | shade, dim | battle ropes | marginal — standing but small in a wide frame |

Rep counts, camera height and card crops per roll: `[editor]`.

## B4. Change at the next shoot (talking shorts and b-roll)

1. **Two full passes per dedicated short, or at minimum a second take of the hook and the CTA.** DS-04 had one
   take of every line and possibly lost the word "Try" on the CTA; the "Remember…" line took three attempts.
2. **Shoot b-roll under the same light as the talking head it will cut into.** C1677 is hard sun, C1656 is
   overcast; every dedicated short that uses both carries a visible look change at each cut. Film the b-roll in the
   same hour and setup as the talking roll, or film the talking roll in the same sun.
3. **B-roll for a vertical short should be portrait, or framed for a vertical crop.** The script asked for 16:9
   vacuum footage; the standing vacuum survives a 9:16 crop, but every lying exercise (C1678–C1683) cannot be
   cropped vertical and ends up as a small card. For mat work meant for Shorts: rotate the camera, raise it, and
   frame Dan along the tall axis.
4. **Keep the profile how-to.** C1677's side-view slump-to-draw-in is the best teaching b-roll on the day; do the
   same "perform the cue in real time, from the side" for every how-to line in future scripts.
5. **A darker background behind the head breaks the hair detector.** Either a plain wall/sky above the head, or the
   detector gets a dark-background mode before the next portrait batch.
6. **Trim the empty frame.** C1677 is half empty; C1675/C1676 (7–8 min each) hold long resets. Stop and restart
   the roll between sets so the transcript/contact-sheet pass has less to walk.
7. **The last rolls are dim.** C1684–C1685 under the patio at sunset are a stop or two under the pool rolls; either
   shoot them earlier or light them.
8. Same as Part A §8: 4 % headroom not 25 %, write the audio layout and the camera rotation on the slate, expose
   S-Log3 brighter outdoors, keep the tape mark.
