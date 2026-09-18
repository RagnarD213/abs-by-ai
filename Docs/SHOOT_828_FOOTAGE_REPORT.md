# 8/28 shoot — footage report from the first edit (RA-01, 2026-09-16)

**Status: Part A COMPLETE 2026-09-17 — every number is from the files; the editor's per-hold numbers come from
`Claude Ad Videos/the ai trick that got me abs - RA-01/measurements-RA-01.json` (round 1).**

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
* **The indoor 1.45× push is too bright outdoors.** Face luma against the approved website video (73.3):

  | exposure | face luma | error vs reference |
  |---|---|---|
  | 1.00× | 71.0 | 2.3 |
  | **1.30× (used in RA-01)** | 82.6 | 9.3 |
  | 1.45× (the indoor setting) | 88.0 | 14.7 |
  | 1.60× | 92.9 | 19.6 |

  Round 1 used 1.30×; on luma alone an unpushed 1.00× LUT is the closest match, which says this roll was exposed
  about right for daylight and needs little or no push. Round 2 settled on **1.15× with `eq=saturation=1.25`** (the
  indoor setting is 0.88): the independent reviewer found round 1's skin grey-brown at ≈ 60 % of the approved Ad 1
  vertical's face chroma. Saturation alone cannot close that gap — at the 1.25 cap the face reads chroma 22 against
  Ad 1's 30 (≈ 73 %). The rest is hue: overcast daylight against warm indoor light, and a white-balance change on a
  skin-tone subject is against the standing rule. So daylight rolls need a **daylight LUT**, not a saturation knob —
  and Dan's eye on the delivered look.
* Sky clipped on 0.53 % of the top 600 rows; grain in a flat tree patch sd 14.4 after the push (visible at native
  scale, not on a phone).

## 3. Which mic track was clean

The lav, and it is the only useful signal: both channels of the single stream carry it identically. Noise floor
between words −55.8 dBFS; early decay 29 ms (outdoors, so no dereverb — the chain's 55 ms trigger never fires); no
wind or rain inside the kept takes (the crew's raindrops are at 1:38–1:41, after the last RA-01 line).

⚠ **The outdoor lav fails one audio-gate row before we touch it.** The gate's `artifacts` row bounds spectral flux at
the indoor reference × 1.1. Measured with the gate's own function: untreated lav **0.094**, voice chain alone 0.097,
chain + music bed 0.093, delivered mix **0.090**, bound **0.079–0.084**. The chain improves the file (`do_no_harm`
×0.95) and still cannot pass, and processing harder would break the never-over-strip rule. DS-17 (same shoot) hit the
same row. **Dan listened to RA-01 and approved it on 2026-09-18 ("Audio sounded good, and color correction looks
good")**, so RA-01 shipped on his approval with the row recorded as a `known_gap` in the regression corpus; the standing
ruling for the other rolls is still open. Every outdoor 8/28 roll will hit it: this is a property of open-air speech against an indoor reference, and it
needs Dan's ruling (accept outdoors as-is, or have the gate carry an outdoor reference through the regression
corpus) — not a per-video workaround.

## 4. Vertical-crop headroom and how big Dan is in frame

Dan stands full-body, shirtless, centred, with feet on a tape mark. Measured on the 2160×3840 decoded frame: hair top
y 1094–1158 (≈ 29 % down; per-hold minimum 1094–1110), belly button y 2093, shorts waistband y 2170, feet y 3523; he
spans ≈ 41 % of the frame width and sits ≈ 140 px right of centre (hold centres x 1210–1257 of 2160). There is plenty of headroom — the opposite of the 8/14 kitchen rolls, where the hair sat
19–45 px from the top edge.

The cost is resolution. The hair-anchored levels are crops of a portrait 4K frame:

| level | crop (est.) | delivered 1080×1920 | upscale |
|---|---|---|---|
| FAR (hair → waistband + shorts) | 702×1248 (round 1 cut it at 630×1120) | 1080×1920 | **1.54×** |
| NEAR (hair → just below the belly button) | 594×1056 (round 1: 504×896) | 1080×1920 | **1.82×** |

**It shows.** Face sharpness (variance of the Laplacian over the face box, median of four frames): source at native
scale 63.2, round 1's delivered vertical **10.6**, the final round-3 vertical **14.2**, the approved Ad 1 vertical
**29.1** on the same method — about half the reference even after the looser crops. The source is sharp; the softness is entirely
the enlargement. The 16:9 is the easy case (NEAR 1888×1062 = 1.14×, FAR 2144×1206 = 0.90×).

## 5. Focus and exposure

At native scale the face is sharp (hair strands and the glasses edge resolve). Exposure is S-Log3-normal — flat until
converted — with the overcast sky the only near-clipped region (0.53 % of the sky rows).

## 6. Lighting

Overcast daylight, soft, no hard shadow side; the background (pool, stone wall, trees) is busier and brighter than an
indoor set, so chips and captions need their own contrast (a plate or outline), which the J2 chip style provides.
Sky-to-face luma ratio 1.18 (a flat, low-contrast key); the shadow side is camera-right; the pool and the pale
limestone wall fill from below and behind, so the face carries little modelling.

## 7. Teleprompter eyeline

Dan reads the ads off a prompter outdoors. On the planner's frames his eyes are on the lens axis with no visible
down-and-left reading offset. FaceMesh on the graded frames: median yaw −1.3° (range −17° to +8° with natural head
movement), pitch +3.7° — a prompter on the lens axis. Nothing to fix. One full pass per script with a
single retake (L5) and one false start, then straight into the next script — the crew chatter between scripts is the
only cutting room floor.

## 8. Change at the next shoot

1. **Frame tighter for the vertical rolls — the biggest single fix.** Dan is 41 % of the frame width with his hair
   29 % down the frame and his feet in shot; the ad only ever uses hair-to-shorts. A hair-to-waistband framing
   straight out of the camera delivers FAR at ≈ 1.0× instead of 1.54× and NEAR at ≈ 1.2× instead of 1.82×, which is
   most of the gap between our face sharpness and the approved Ad 1's. Keep ≈ 4 % headroom above the hair.
2. **Record the same audio layout on every roll**, or write the layout on the slate. Two families on one day cost a
   wrong memory and a wrong job doc; `pick_lav.py` caught it, a hard-coded map would not have.
3. **Say on the slate whether the camera is rotated.** Rotation side-data is easy to miss in a probe.
4. **One more full pass per ad script.** With a single pass, take selection is forced and any flub is in the ad.
5. **Outdoors the exposure was right; the indoor grade is what's wrong.** Keep exposing as on 8/28; build one
   daylight LUT (≈ 1.0–1.15× push, warmer skin) fitted against an approved frame, and stop reusing the kitchen LUT
   plus a saturation lift.
6. Keep the tape mark and the fixed standing position (it makes the per-hold fixed centre trivial) — just move the camera in.
7. **Get a ruling on outdoor audio before the next outdoor shoot** (§3): either accept the open-air lav against the
   indoor reference, or record one approved outdoor reference for the gate. What in the open-air signal drives the
   reading (pool pump, breeze, traffic) was not isolated; a test recording with and without a lav windscreen at the
   next outdoor setup would answer it.

---

# Part B — the dedicated-shorts talking roll and the exercise b-roll (DS-04, 2026-09-16)

**Status: measured — planner's roll survey plus the DS-04 round-1 editor's numbers
(`/Volumes/Extreme/_edit_work/ds04/measurements-DS-04.json`).** Written from the second edit of 8/28 footage: DS-04 "The Only
Ab Exercise That Shrinks Your Belly Fat", cut from talking roll C1656 with b-roll from C1677 (vacuum) and C1682
(crunch, toe touches). Every number below was measured on the files.

## B1. C1656 — a dedicated-short talking roll, same family as C1663

* **Portrait like C1663**: stored 3840×2160, rotation side-data −90, decodes to 2160×3840. Same rule: never
  `-noautorotate`, never a `transpose`. The DS job docs' line "framed horizontal and centre-safe for vertical crops"
  is wrong for every dedicated short on C1654–C1672.
* **Audio: one stereo stream, dual-mono** (channels correlate +1.000 at lag 0). `pick_lav.py`: SNR 42.4 dB, RMS
  −26.8 dBFS, dryness 7.7 dB, EDT 26.7 ms, 0 clipped samples. Outdoors, so no dereverb is ever needed on this
  family. Noise floor between words −60.3 dBFS; crew/handling events only at 0:03.7, 1:23 and 1:25, all outside the
  cut.
* **⚠ The raw lav fails the audio gate's `artifacts` row before anything touches it.** Untreated spectral flux
  reads 0.102 against a bound of 0.079 (Muhammad's reference 0.072 × 1.10). The shared chain brings it *down* to
  0.089 (×0.88 of doing nothing, so `do_no_harm` passes), and no bed level reaches the bound (−32/−36/−40 dB →
  0.088/0.091/0.093). RA-01 (C1663) hit the identical row. It is a property of this outdoor set's recording, not of
  the chain, and it will recur on every C1654–C1672 edit until Dan rules on it. No threshold was changed.
* **Dan is bigger in frame than on C1663.** Face skin starts at y ≈ 1020–1160 of 3840 (hair top ≈ 25–29 % down,
  against ≈ 20 % on C1663); belly button ≈ y 2070, waistband ≈ y 2230, shoes ≈ y 3300; he spans ≈ 40 % of the width.
  The hair-anchored crops cost less resolution here:

  | level | crop (est.) | into the 1080×1540 picture window | scale |
  |---|---|---|---|
  | NEAR (hair → belly button) | ≈ 813×1160 | 1080×1540 | ≈ 1.33× |
  | FAR (hair → shorts line) | ≈ 932×1330 | 1080×1540 | ≈ 1.16× |

  Measured on the build: hair top y 1094–1110 across eight holds (median 1118 over the roll), head height 368 px,
  belly button y 2078, waistband y 2244, shoes y 3508, Dan 38.9 % of the width. The crops that satisfied the gate
  were **NEAR 700×998 (1.54×) and FAR 848×1208 (1.28×)** — tighter than the planner's estimate because the head has
  to fill ≥ 27 % of the frame. **Delivered face sharpness 21.1 (variance of the Laplacian) against 27.2 on the
  approved Ad 1 vertical**, from 56.9 at native scale: the upscale costs a visible amount of face detail.
* **The hair detector does not work against trees.** `hairdet.py` assumes a bright wall above the head; on this
  roll the trees behind Dan are darker than his hair, so it returns a hair row 800 px too high and "climb too long".
  The skin-top it reports is right; the hair top has to be found as the last dark run within ~150 px above it and
  proven on a native-scale proof sheet.
* **Takes: one pass per line, no safety.** Lines 1–10 in one 35 s pass (0:09–0:44), then three attempts at the
  "Remember, the vacuum does not burn fat…" line (two stopped short, the third is the only complete one), then the
  close. The first Whisper pass dropped "Try" from the CTA line; a second pass and the finished render both hear it
  at 1:11.68, so the line is whole — but it was one take from being a broken CTA. A single fluffed
  word in the hook or the CTA would have had no replacement.
* Grade: exposure **1.30×** measured best against the approved website-video frames (face-luma error 6.6, against
  11.6 at 1.45× and 16.5 at 1.60×) and is what RA-01 measured for the same set, so the outdoor dedicated shorts share
  one look: face luma 79.9, chroma a/b 29/11, sky clip 0.14 %, tree-patch noise sd 7.2.
* Eyeline: yaw −2.5°, pitch +0.3° (FaceMesh) — the prompter sat just off the lens axis; it does not read as
  off-camera. Light: overcast, sky-to-face luma 1.11, skin 87.7 / 82.4 left/right — almost no modelling.

## B2. C1677 — the vacuum b-roll Dan asked the script to film

* Landscape 3840×2160, 205 s, S-Log3, stereo crew audio. **Shot in hard afternoon sun** (the talking roll is
  overcast): one side of his face and torso is lit, the other in shadow, the wall behind him near clipping. The
  vacuum reads well because the side light draws the drawn-in stomach, but the b-roll and the talking head will not
  match in colour or contrast inside one short without a per-clip trim. At the same 1.30× grade his skin reads
  **140.7 on the lit side and 104.2 on the shadow side (1.35:1), against 87.7 / 82.4 on the overcast talking roll** —
  the b-roll skin is 1.3–1.6× brighter than the talking head it cuts to — and 3.5 % of the frame is clipped (wall).
* **He strains through the first front pass.** On 0:06–0:28 his mouth is open at eight points and his eyes are shut
  for most of 0:09–0:23; the longest presentable run is 2.7 s. The edit took cue 1 from the second front pass
  (2:03.0–2:07.6, eyes open, mouth closed).
* Three usable passes: front hands-on-hips holds 0:00–0:28, a **profile pass 0:47–0:80 that performs the script's
  own cue in real time** (slump 0:50–0:55, straighten 0:56, draw in 0:57–0:61, hold to 0:70), and front holds
  1:40–2:52. Between them **100+ s of empty frame** (0:30–0:46, 0:81–1:39, 2:53–3:25).
* He fits a hair-to-thigh vertical crop out of the 16:9 (≈ 1500 px tall → ≈ 1.0–1.3× into the window), so the
  standing vacuum needs no J2 frame. Used (round 2): front 974×1388 (1.11×), profile 916×1306 (1.18×), both
  hair-to-below-the-knee so the caption band clears the stomach. Profile cue timing as measured: fold 0:53.0–0:55.7,
  upright 0:55.9, draw-in 0:56.2–0:57.3, hold to ≈ 1:10. Empty frame: 106 s of 205.

## B3. C1673–C1685 — the exercise b-roll

| rolls | set | light | what | vertical-usable? |
|---|---|---|---|---|
| C1673–C1676 | hot-tub pool, tape mark | hard side sun | kettlebell swings, skipping, dumbbell curls/presses, seated presses, RDLs, bent rows — standing, full body, Dan ≈ 25 % of frame height | yes as a tight crop, ≈ 1.5–2× upscale |
| C1677 | same | same | vacuum (B2) | yes |
| C1678 | same | same | 33 s, mat: push-up / plank | no — lying, needs a card |
| C1679–C1683 | the other pool, blue mat, camera at ground level | warm low sun, then shade | kneeling ab-wheel rollouts (C1679), leg raises + planks (C1680), push-up variants with a chair (C1681), **crunches 0:57–0:61 and toe touches 0:62–0:79, 1:26–1:39 (C1682)**, seated medicine-ball twists, planks, rollouts (C1683) | no for every lying/kneeling move — a 9:16 crop slices the body; they go in as 4:3 cards on the J2 field |
| C1684 | covered patio | shade, dim | handstand push-ups | no |
| C1685 | covered patio | shade, dim | battle ropes | marginal — standing but small in a wide frame |

C1682 measured: **no crunch at all** — 0:56.5–0:58.9 is Dan sitting down and settling, not a rep — then eight
toe-touch reps 0:59–1:20 and five more 1:26–1:39; camera
at ground level (horizon at 0.30 of frame height), side-on. His silhouette spans 1212–1408 px of the 3840 width
against a 1215 px 9:16 window, so a vertical crop slices a limb on every rep; the 4:3 cards used were 1464×1098 and
1694×1270 in round 1 and 2250×1266 in round 2. C1683 holds no crunch and no toe touch either; the script's
"crunches" cue was filled with C1683's seated medicine-ball twist. **Nobody filmed a crunch on 8/28.**

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
8. **Hold the pose with a camera face.** On the vacuum front pass his eyes were shut and his mouth open for most of
   the hold; a b-roll hold needs 5 s with eyes open and mouth closed, called out by whoever is behind the camera.
9. **Frame the talking short tighter.** Even with Dan at 39 % of the width, the gate-legal NEAR crop is a 1.54×
   upscale and the delivered face measures 19.9 against the Ad 1 vertical's 27.2. Hair-to-waistband straight out of
   the camera would deliver both levels at ≤ 1.1×.
10. **Find what makes the outdoor lav "fluxy"** (pool pump, wind on the necklace mount, the mic against bare skin)
   before the next outdoor shoot: both outdoor edits fail the same audio row on the raw signal.
11. **Film the exercise the script names.** DS-04's cue reads "crunches and toe touches — footage exists"; the
   8/28 exercise rolls hold toe touches, twists, planks and rollouts, and not one crunch. Before the shoot, walk
   every b-roll cue in the scripts against the exercise list for the day.
12. **Leave the stomach clear of the caption band on a how-to shot.** Captions sit at 70–84 % of the frame height;
   a profile demo framed hair-to-thigh puts the drawn-in stomach right under them. Shoot it a little wider.
13. Same as Part A §8: 4 % headroom not 25 %, write the audio layout and the camera rotation on the slate, expose
   S-Log3 brighter outdoors, keep the tape mark.
