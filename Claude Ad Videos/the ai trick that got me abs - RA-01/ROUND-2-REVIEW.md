# RA-01 "The AI Trick That Got Me Abs" — ROUND 2 REVIEW

Reviewer: independent (Fable 5.1), 2026-09-17. Read only: `AGENTS.md`, `00-RULES.md`, `RA-01-plan.md` (§12 rulings
applied), `ROUND-1-REVIEW.md` (+ its evidence), the two round-2 masters, their four stamps, `recipe-RA-01/gate_plan_9x16.json`
/ `gate_plan_16x9.json`, script lines 259–274, the named source assets, the source roll C1663 (crop location only), the
round-1 masters, and the approved Ad 1 vertical. Did NOT read the editor's round files, notes, grade/verify JSON, watch-pass
folders, flux diagnosis or the delivery folder. All evidence is in `/Volumes/Extreme/_edit_work/ra01/review-r2/` (paths
below are relative to it). Machine cap checked before every decode (one other build running).

Files reviewed:
- `master_9x16.mp4` sha256 `5bc6c512…eb07d`, 80,472,539 B — 1080×1920, 30000/1001, h264 High yuv420p bt709/tv, AAC-LC 48 kHz 2 ch, **57.190 s**, 1714 frames
- `master_16x9.mp4` sha256 `1f4367c3…745f`, 65,470,893 B — 1920×1080, same, 57.190 s, 1714 frames

## Round-1 defect status (D1–D11)

| id | round-1 defect | status | evidence |
|---|---|---|---|
| D1 | audio `artifacts` FAIL → all four stamps FAIL | **NOT FIXED — Dan's ruling, not an editor fix** (flux 0.091 vs limit 0.079, his 0.072; untreated 0.097; do_no_harm x0.94) | stamps; `audio_measurements.txt` |
| D2 | captions absent 0–12.2 s / dropped words / mid-sentence starts / 0.84 s silent lead-in | **FIXED** — first cue 0.13 s, last 55.22 s, no gap > 0.4 s, all 192 states word-accurate, first word audible from 0.045 s | `sheets/caps9_1..3.jpg`, `my_whisper.json`, `audio_measurements.txt` |
| D3 | framing one notch too tight; face box to 98 % width; soft | **PARTLY** — levels now match R2 (NEAR crop 596×1059 src px, bottom y=2119 ≈ 26 px below the navel; FAR 704×1251, bottom 2307 ≈ 137 px below the waistband); face box inside 8–92 % on 1032/1043 frames, **11 frames at 00:22.15–00:22.26 reach 92.7–94.3 %** (face intact, nothing clipped); sharpness still ≈ 0.5× Ad 1 at phone size (footage finding, not a defect per §5) | `sheets/crop_NEAR.png`, `crop_FAR.png`, `face_sweep_log.txt`, `sheets/lean_22.59.jpg`, `skin_sharpness.txt` |
| D4 | macro beat ran into the recalculation + a 3-frame foreign screen | **FIXED** — every frame 1098–1190 inspected: same list (273/53/37 cal), total 363 cal, "logged" state, max frame-to-frame diff 3.5/255 (slow scroll only), first frame is the list, last frame is the list, no foreign screen | `sheets/macro9_strip.jpg`, `macro16_strip.jpg`, `macro9/`, `macro16/` |
| D5 | 16:9 pill = full-width band across neck/shoulders | **FIXED** — compact 552×132 pill, text-sized, clear of Dan on every frame; CTA 1 low-left (y 772–904); CTA 2 sits mid-left (y 322–454), not "low" — see D6 below | `sheets/key16_pills.jpg`, `pairs16_2..5.jpg` |
| D6 | skin grey-brown (cheek chroma ≈ 16 vs Ad 1 ≈ 28) | **FIXED** — cheek chroma median 29.4 (a 17, b 24) vs Ad 1 big-face frames 34.7 (a 19, b 29) = **0.85×**, L 33.7 vs 38.4; reads natural and warm beside the cards; trees/pool/shorts not neon | `skin_sharpness.txt`, `sheets/key9_a.jpg`, `reff/` |
| D7 | 13-frame flash of Dan between before and afters | **FIXED** — BEFORE 1.70 s (00:05.02–00:06.23), Dan FAR 0.90 s, afters 0.634 s each | `sheets/pairs9_1.jpg` |
| D8 | chips in the top 3–6 % band; cards on blurred photo | **FIXED** — 9:16 AI chip box (324,200)–(667,261), real chip (108,200)–(895,271): y ≥ 200, right edge ≤ 895 ≤ 940, above the card, off face/hair/abs; end-card chip (168,1296) on the shins; field is flat J2AD (sd 2.3); 16:9 chips fully inside the card frame | `sheets/chips9_zoom.png`, `chips16_zoom.png`, `key16_cards.jpg` |
| D9 | lowercase "it" sentence starts | **FIXED** — 0 lowercase sentence-initial cues in 192 states ("It inspired", "Then it gave", "It gave") | `sheets/caps9_2.jpg`, transcript diff |
| D10 | bed dropout + 15 dB step near 0:56 | **NOT FIXED** — identical dip: 00:55.28–00:56.02 the bed falls to −56…−65 dBFS then steps to −48/−42 within 5 ms at 56.060 s; same absolute position and shape as round 1 | `audio_measurements.txt` (TAIL envelope) |
| D11 | n/a reasons that do not describe this cut; watch pass not independent | **NOT FIXED (not editor-fixable)** — same two n/a rows, same reasons; `watch:pass` now judged by "round-2 editor session… no judge subagent"; this review is the independent pass (R8) | stamps |

```
VERDICT: DOES NOT SHIP

DEFECTS (most serious first):

  D1  both files, whole file — audio stamps
      Plan §1/§6/§7: PASS audio_gate + deliver_gate stamps on each delivered file.
      →  audio_gate (both): row `artifacts` FAIL — "flux 0.091 (his 0.072) … <= his x1.1" (limit 0.079); verdict FAIL.
         deliver_gate 2.1.0 (both): verdict FAIL on `audio:stamp`; every other row PASS or n/a. sha256 and versions
         are current, so these are valid FAIL stamps. The stamp's own do_no_harm row shows the untreated lav at 0.097
         (chain improved it x0.94): the outdoor source is over the bound. Per §12 this is Dan's ruling, not an editor
         fix — do not process harder, do not touch the gate. Stated separately from everything below.  severity: blocker

  D2  both files 00:05.11–00:07.00 — printed number in the caption under the BEFORE picture
      Plan §4: "on-screen text never states a number, user count or comparison ('200 lbs' is spoken, not printed)".
      §12 R1: captions over every beat, never a dropped word.
      →  The burned caption reads "when I was 200 pounds." on the J2 field directly under the heavier BEFORE photo
         (both aspects). The two rules collide on exactly this word and the editor printed it. The gate plan's
         caption_states carry no "200" state (192 states vs 193 spoken words), so the numeral was never proofed by
         the sync gate either. This is a planner/Dan call (drop the numeral, rephrase the cue, or amend §4); it is
         listed as major because §4 names this exact case and ad text is a compliance surface.
         Evidence: sheets/caps9_1.jpg (5.47–6.37 s tiles), sheets/pairs9_1.jpg, sheets/pairs16_1.jpg   severity: major

  D3  both files 00:55.28–00:56.02 — music-bed dropout (round-1 D10, not fixed)
      §12 R7: remove the ≈0.1 s bed dropout and step near 0:56; no other mix change.
      →  Still there, unchanged: 5 ms envelope −45…−50 dBFS to 55.92 s, falls to −56…−65 dBFS 55.94–56.055 s, steps to
         −48 then −42 dBFS at 56.060 s (≈15 dB inside 5 ms). Same absolute time and shape as the round-1 file (whose
         end-card join was at 56.056 s); in round 2 the join is at 55.289 s, so the dip is 0.67 s INTO the end card —
         it is in the bed itself or its envelope, not at a picture join. Low level; still the one measurable
         discontinuity in the mix.
         Evidence: audio_measurements.txt (TAIL 5 ms envelope, round 2 beside round 1)                severity: minor

  D4  master_9x16.mp4 00:22.15–00:22.26 (frames 675–685) — face box past 92 % (round-1 D3, partly)
      §12 R2: his face box stays inside 8–92 % of the frame width on every frame; a hold whose lean breaks that at
      NEAR is cut at FAR.
      →  NEAR hold 20.254–23.156 s: the face box (mediapipe) reaches 92.7–94.3 % of the width for 11 frames as he
         leans right; the face is fully in frame, hair and glasses intact, nothing clipped (lean_22.59.jpg). Every
         other frame of both files is inside 8–92 % (9:16 worst otherwise 91.1 %; 16:9 35.1–81.9 %).
         Evidence: face_sweep_log.txt, faces_9x16.json, sheets/lean_22.59.jpg                          severity: minor

  D5  master_16x9.mp4 every NEAR↔FAR join (00:16.10, 00:20.07, 00:23.05, 00:40.26, 00:44.14, 00:47.17, 00:51.07, 00:53.27)
      — lateral hop between levels
      Plan §5: fixed centre per hold on his torso; `framing:centering` ≤ 6 %.
      →  Each hold is rock-steady (background drift ≤ 0.11 px at 960 wide), and every hold is inside 6 %, but the two
         levels sit on different centres: NEAR holds −1.8…−0.2 % (torso skin-median), FAR holds +2.3…+5.4 % right,
         so at every zoom cut he hops ≈ 4–7 % of the width sideways. Cause: the 16:9 FAR crop is the full source
         width (2140 of 2160 px, x 16–2156) and Dan stands right of the source centre, so FAR cannot be recentred —
         NEAR would have to carry the same offset (or FAR lose a little height) to stop the hop. The gate's centering
         row is n/a for 16:9, so no gate measured this.
         Evidence: mid16/ torso-centre table (in this file's transcript), drift_log.txt, audio_measurements.txt crop
         match, sheets/pairs16_2..4.jpg                                                                 severity: minor

  D6  master_16x9.mp4 00:53.24–00:55.08 — CTA 2 pill not low in the frame
      §12 R4: compact pill, low in the frame, never touching face/neck/shoulders, captions lift above it.
      →  CTA 1 (18.9–20.5 s) is low-left (y 772–904 of 1080) as ruled. CTA 2 sits mid-left at y 322–454 (30–42 % of
         the height), level with his shoulders though not touching him (his fists are lower-left during this line,
         which is presumably why it moved up). Compact and clear, but not "low".
         Evidence: sheets/key16_pills.jpg (n01616), sheets/pairs16_4.jpg                                severity: minor

  D7  stamps — gate paperwork (round-1 D11, not editor-fixable)
      →  9:16 `framing:no_wide_level` n/a "Dan sits in a full-width WINDOW above the text": not this cut (he is
         full-frame; my head height 20–26 % of the frame = not wide, so harmless). 16:9 `framing:centering` n/a
         "bullets left and Dan right": not this cut — see D5 for the measurement the gate did not take. `srt:*` n/a
         fits. `watch:pass` (both) is judged by "RA-01 round-2 editor session… frame-by-frame by the editor, no judge
         subagent" — not independent; per R8 this review is the independent watch judge for round 2.  severity: minor

CHECKED AND CLEAN:
  §1 container: both 57.190 s ≤ 59.00; 1080×1920 / 1920×1080, 30000/1001, h264 High yuv420p, bt709 tagged tv range,
     AAC-LC 48 kHz stereo; 1714 frames each; audio streams byte-identical (packet md5 8732c9f7…, PCM md5 a7a1d2e0…).
     First frame = AI card with chip and caption "This" from 0.13 s; last frame = held end card, luma 71.7 / 37.9
     (not black). Stamps: all four sha256 values match the files; deliver GATE_VERSION 2.1.0 = current gate.py;
     audio stamp version 1 = current.
  §2 take map / script: my own Whisper medium.en pass on the delivered audio = 194 words, L1–L14 all present, in
     order; only drift is Dan's own ("200 pounds", "the exact same way that I did", "And you can change", "It gave
     me"); Whisper's one mishearing ("loot") is captioned correctly as "lose". L5 t2, no false start, L11 kept, nothing
     cut, no speed ramp, both CTA lines intact. No drug names, no user counts.
  §12 R1 beat map, frame by frame at every boundary (sheets/pairs9_*.jpg, pairs16_*.jpg): AI card 0–2.069 (chip);
     Dan NEAR 2.069–3.170 on "And it's not even real" (face in the first 3 s); AI card 3.170–5.072; BEFORE
     5.072–6.773 = 1.70 s from 2 frames before "back"; Dan FAR 6.773–7.674 = 0.90 s; three afters 0.634 s each with
     the real-picture chip; AI card lands 9.576, one frame before "AI"; card holds to 12.312. Lead-in 0.13 s, no
     silent hold. Cards feature-matched to the named files: `dan by pool.png`, `01_LIGHT_plus8lb_PRIMARY.jpg` (no chip
     per plan, §9 call stands), studio-blue-10 / gray-41 / white-90 (none in Frowning Photos/). Never two physique
     pictures at once; before → other → after; no side-by-side, no "Meet the new you", no email screen. Stats scan:
     bars only, no numbers, AI-GENERATED chip, "YOUR WORKOUT PLAN" button (sheets/stats_scan.jpg). Macro tracker: real
     app screen, no physique, itemized list + total stable (D4 fixed); the recording scrolls slowly so a sliver of a
     blue header sits at the card top for the first ≈ 20 frames — cosmetic, content unchanged. End card = AI image +
     chip + "Tap the button below" + AbsByAI.com, 1.90 s.
  §4 chips/labels: every AI beat carries AI-GENERATED, every real photo carries "Real picture of me — not AI-generated",
     none on moving footage of Dan, none over face/hair/abs (9:16 chips above the card; end-card chip on the shins;
     16:9 chips on the card frame). 9:16 safe area satisfied (y = 200, right edge ≤ 895).
  §5 framing: hair never clipped in either aspect — tallest frames (9:16 f489/f677/f1411, 16:9 f446/f1616) show
     ≥ 80 px of headroom above the hair (sheets/hair_tops.jpg); crops fixed per hold (corner-patch drift ≤ 0.68 px at
     540 wide, ≤ 0.11 px at 960 wide); levels alternate at all 13 visible talking joins, NEAR head 24.7–26.2 % vs FAR
     20.2–22.2 % of the frame (spread ≈ 1.19); no naked jump cut at any of the 26 boundaries; 16:9 face box always
     inside 35–82 %.
  §6 audio: −14.2 LUFS, LRA 3.3, true peak −2.1 dBTP, L/R identical (side −57 dBFS), no silent seconds; 0 of 41
     boundary joins with a click above 1.13× the local ceiling (gate: 0/20 above 1.25×); level steps at joins are word
     onsets after airtight pause removal, not seams; no clipped words (every join's after-window ramps naturally).
     Music bed sits ≈ −45…−50 dBFS between words (legal, effectively inaudible — unchanged from round 1; Dan's call).
  §7 captions: first 31 s proofed word for word against the audio (108 tiles): every word correct, "abs" lowercase,
     "AI" uppercase, no "apps"/"RIP", sentence starts capitalised, current-word highlight on the spoken word (audio
     onsets checked for the four largest Whisper deltas: caption within −40…+90 ms of the true onset), captions never on
     a chip, the pill or a face, always below the card on the J2 field, above the pill.
  §12 R4/R5/R6: 16:9 pill compact and clear of Dan (D5 fixed; D6 above for placement); skin natural (chroma 0.85× Ad 1,
     face luma Y median 83 box / 93 skin-band); cards on a flat dark field; 9:16 pill URL line ≈ 30 px, legible.
  Viewer judgement: muted, the first 3 s now read as a hook — AI picture + label + "This picture got me abs." then his
     face on "not even real"; with sound, speech from the first frame. The photo run (1.7 / 0.9 / 0.63×3 s) is brisk
     and registers. Pill copy and end card are clean. Sharpness at phone size is ≈ half of Ad 1 (face Laplacian
     variance 112 vs 218 at 360 px wide) — visibly softer beside the studio photos; per §5 this is a footage-report
     number, not a build defect.

COULD NOT VERIFY:
  - Listening by ear: every join, the tail and the loudness were measured, not heard; the `artifacts` FAIL still needs
    a human ear (Dan's ruling).
  - The delivery folder (names, 540p copies, A/B clip, notes, recipe, measurements JSON) — barred from it.
  - Whether the R5 "face luma 73 ± 5" target was met by the editor's own method — my Y-box median is 83 (skin band 93);
    the measurement region is not specified in the plan, so I report mine rather than a pass/fail.
  - The 16:9 NEAR crop in source coordinates (only the FAR crop match completed); centering was measured on the
    delivered frames instead.
  - Lip-sync beyond the gate's audio-vs-source row (+0.04 ms) — not re-measured.
```
