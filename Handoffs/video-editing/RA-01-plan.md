# RA-01 build plan — "The AI Trick That Got Me Abs" (9:16 ≤ 0:59 + 16:9)

**Written 2026-09-16 by the planning session (Fable 5.1, high).** This is the spec the EDITOR (Opus 5, high) builds
to and the REVIEWER (a fresh Fable 5.1, high, that never sees the editor's notes) checks against. Where this plan and
the job doc `RA-01-ai-trick-that-got-me-abs.md` disagree, this plan wins (it was written after measuring the roll);
`00-RULES.md` and `AGENTS.md` beat both. Anything not covered here follows `.claude/skills/ad-edit/SKILL.md`.

Round files live in the work dir: `ROUND-n-EDITOR.md` (editor), `ROUND-n-REVIEW.md` (reviewer). Max three rounds,
then the orchestrator takes the open defects to Dan.

---

## 0. Measured facts about the roll (planner, 2026-09-16) — these override the job doc

| fact | measured value |
|---|---|
| file | `/Volumes/Extreme/abs by ai 8:28 shoot \| jeff \| dan \| ads, dedicated shorts, b roll, scripted long form content/main camera/C1663.MP4` (read-only) |
| stored | 3840×2160, **rotation side-data −90** → ffmpeg autorotates to **2160×3840 PORTRAIT**. Never pass `-noautorotate`, never add your own `transpose`. Probe a decoded frame and confirm 2160×3840 before anything else. |
| fps / length | 29.97 (30000/1001), 218.2 s |
| picture | S-Log3 / S-Gamut3.Cine. Grade = `lut3d=file=/Volumes/Extreme/_edit_work/website-video-828/slog3_709_e1.45.cube:interp=tetrahedral,eq=saturation=0.88` (the approved 8/28 conversion, `website-video-828/grade.txt`). Decode BT.709 (`scale=in_color_matrix=bt709:in_range=tv`). The LUT was fitted indoors; this roll is **outdoors, overcast, by the pool**. You may test exposure 1.35 / 1.45 / 1.55 (`make_lut.py <expo>` in `claude edited long form content/06 - Website Conversion Video (post-generation)/recipe_REV5/`) and pick by measuring Dan's face skin luma/chroma against an approved website-video frame; record the numbers. No other grade change. |
| audio | **ONE stereo stream, dual-mono** (L/R correlate +1.000 at lag 0), lav signal, SNR 47.5 dB, no clipping. `pick_lav.py` already wrote `C1663.MP4.audio_source.json` beside the roll: `-map 0:a:0 -af "pan=mono\|c0=0.5*c0+0.5*c1"`. Use that JSON. ⚠ The memory's "four mono tracks, lav on a:1" describes C1650–C1653; the dedicated-shorts rolls C1654–C1672 were recorded differently. Never hard-code a channel. |
| framing in source | Dan full-body, shirtless, green shorts, centred; hair top ≈ 20 % down the frame (≈ y 780 of 3840), belly button ≈ y 1620, shorts waistband ≈ y 1720, feet ≈ y 2600. He is only ≈ 35 % of the frame width. Sky and trees above, pool behind. Re-measure per hold with `hairdet.py` — these are the planner's estimates from four frames. |
| focus / exposure | face sharp at native scale (hair strands and glasses edge resolve); visible grain in the trees after the 1.45× push; sky near clipping. Record real numbers in `measurements-RA-01.json` (§8). |
| takes | ONE full pass of the script, 0:27.0–≈1:34.5. One retake (L5). After 1:38 the crew talks (raindrops) and Dan starts a **different** script ("How To Generate Abs With AI" = RA-02) — not this job. |

## 1. Deliverables

Folder (create it): `Claude Ad Videos/the ai trick that got me abs - RA-01/`
Work dir (create it): `/Volumes/Extreme/_edit_work/ra01/` — copy anything you need in; never write into another job's dir.

| file | spec |
|---|---|
| `the ai trick that got me abs \| claude \| 9x16 \| RA-01.mp4` | **1080×1920, 30000/1001 fps, h264 yuv420p, AAC 48 kHz stereo, ≤ 59.00 s total** (target 52–58 s) |
| `the ai trick that got me abs \| claude \| 16x9 \| RA-01.mp4` | 1920×1080, same EDL, same audio track (bit-identical mix), graphics re-laid |
| `the ai trick that got me abs \| REVIEW 540p 9x16 \| RA-01.mp4` and `… REVIEW 540p 16x9 …` | 540p review copies |
| `the ai trick that got me abs \| AB audio ref-vs-ours \| RA-01.mp4` | the audio gate's A/B clip |
| `<each master>.audio_gate.json`, `<each master>.deliver_gate.json` | PASS stamps at the current `GATE_VERSION`, sha256-bound to the delivered file |
| `notes-RA-01.md` | take map, every choice and deviation, gate tables, the calls for Dan (§9) |
| `recipe-RA-01/` | every script and JSON needed to rebuild both files |
| `measurements-RA-01.json` | the footage-report numbers (§8) |

No 1:1, no hook variants, no upload, no dashboard row, no Google Ads. Commit docs/scripts only, never media.

## 2. Take map (Whisper pass, times approximate ± 0.5 s — re-align with word timestamps)

Script = `Media/codex-video-trial/05-recipes/candidates/shoot5-notes.txt` lines 259–274. Spoken words win over the
script where they differ; flag drift in the notes.

| line | script (spoken drift in brackets) | source time | use |
|---|---|---|---|
| slate | "we're about to go into the short form ad script section…" | 0:13–0:20 | discard |
| L1 | This picture got me abs. And it's not even real! | 0:27.0 | keep |
| L2 | I generated this picture with AI back when I was 200 lbs ["200 pounds"] | 0:30.4 | keep |
| L3 | And this is what I look like today. | 0:34.4 | keep |
| L4 | Seeing this AI image of myself with abs changed me. | 0:37.1 | keep |
| L5 t1 | It inspired me to start taking my workouts and nutrition seriously again. | 0:40.8 | candidate |
| — | "To generate a picture of yourself," (false start) | 0:44.7 | discard |
| L5 t2 | It inspired me to start taking my workouts and nutrition seriously again. | 0:47.2 | **default pick** (later take) unless t1 measures cleaner — say which and why |
| L6 | To generate a picture of yourself with abs using AI, tap the button below. | 0:52.5 | keep — CTA 1 |
| L7 | And that's only the beginning of how AI helped me to get abs… | 0:57.0 | keep |
| L8 | Once I generated my picture, AI analyzed it and figured out exactly how much fat I had to lose - and where I had to gain muscle - to reach my goal physique. | 1:00.2 | keep |
| L9 | Then it gave me a personalized workout and nutrition plan to hit my goal. | 1:09.2 | keep |
| L10 | I even started using AI to track my macros | 1:13.9 | keep |
| L11 | AI inspired me to work out. And it gave me the exact workout and nutrition plan I needed to hit my goal. | 1:17.1 | keep if length allows (§3) |
| L12 | You can change your life the same way I did. ["the exact same way that I did"] | 1:23.2 | keep |
| L13 | And the first step is generating an AI image of yourself with abs. | 1:26.7 | keep |
| L14 | To generate an image of yourself with six pack abs, tap the button below. | 1:30.5–≈1:34.5 | keep — CTA 2, final line |

Because only one pass exists, the skill's "take reel for Dan" step is moot: skip it, say so in the notes.

## 3. Length rule

Airtight pause removal per the skill (word boundaries place cuts, silence validates). Estimated speech ≈ 55–58 s.
If the airtight cut plus the end hold exceeds **59.00 s**: **no speed ramp, never cut L6 or L14**. Line cut in this
order, one at a time, re-measure after each: (1) drop **L11** entirely (it restates L9; L10 → L12 still flows);
(2) drop **L7**. Record what was cut and the final length. Total container duration must read ≤ 59.00 s.

## 4. Cue map — what is on screen, both aspects, same timeline

Every asset below already exists. **AI-generation budget for this job: $0.** If something appears to need generating,
stop that beat, use Dan on camera instead, and report it — do not spend.

| beat | on screen (9:16) | asset | label |
|---|---|---|---|
| L1 | from the word "This" through "real": **the AI image of Dan**, full-width card on the J2 field | `Media/example pictures/dan by pool.png` (864×1184; the Ad 1 goal image) | `AI-GENERATED` chip |
| L2 | on "I generated this picture" the AI image stays; on "200" cut to the **BEFORE picture** and hold to the end of L2 | `photos/Dan Before Pictures/01_LIGHT_plus8lb_PRIMARY.jpg` (Dan's pick; AI-adjusted +8 lb from a real 2022 photo) | **no chip** (Ad 1 rev-5 precedent, `rev5/gfx5.py` line 73 `layer(before, None, None)`) — flagged to Dan in §9 |
| L3 | on "this is what I look like today": **three real after pictures, rapid**, ≈ 0.55–0.7 s each, sequential, never two on screen | `photos/finalized social media photos/studio-blue-10_FINAL_PRIMARY.jpg`, `studio-gray-41_FINAL_PRIMARY.jpg`, `studio-white-90_FINAL_PRIMARY.jpg` (three backgrounds, three outfits, all smiling, none from `Frowning Photos/`) | `Real picture of me — not AI-generated` chip on each, placed by person-mask measurement, never over face or abs |
| L4 | the AI image again for the line ("this AI image") | as L1 | `AI-GENERATED` |
| L5 | Dan on camera | — | — |
| L6 (CTA 1) | Dan on camera; **CTA pill** appears on "tap the button below" and holds through L6 | pill copy: `Tap the button below` + `AbsByAI.com` (two lines or one pill + URL line) | — |
| L7 | Dan on camera | — | — |
| L8 | "AI analyzed it… how much fat… where I had to gain muscle": the **stats-scan animation over Dan's AI image** (scan line + stats reveal), ≈ 5 s | rebuild from `.claude/skills/ad-edit/reference/ad1/prep_assets3.py` `stats_scan` using `dan by pool.png` as the subject (Ad 1 rev-2 approved device). If the rebuild can't use Dan's own image, skip the beat (Dan on camera) and say so. | `AI-GENERATED` |
| L9 | Dan on camera | — | — |
| L10 | **macro tracker**: the itemized-results moment (food list + calorie total on screen), ≈ 3–4 s, phone recording full-frame in 9:16 | `Media/ad-assets/ad2-nutritionist/clips/app-flow-macro-tracker-itemized.mp4` (1320×2868, 46 s; pick the slice where the itemized list and total are visible). Log it in `reference/demo-clip-log.md` (2nd use). | none (real app screen, no physique) |
| L11–L13 | Dan on camera, zoom cuts | — | — |
| L14 (CTA 2) | Dan on camera; CTA pill from "tap the button below"; then **end card** held ≈ 1.2 s after the last word: the AI image + `Tap the button below` + `AbsByAI.com` | as L1 | `AI-GENERATED` |

Rules that bind every beat: **before → other → after, never side by side**; no app screen that shows before+after
together; no email-capture screen; no "Meet the new you"; on-screen text never states a number, user count or
comparison ("200 lbs" is spoken, not printed); no drug names. The macro clip's own `absbyai.com` pill is fine.

**Chips**: the same solid rounded chip style for both labels (`motionlib.chip`, J2AD palette), large enough to read
on a phone, inside the safe area, clear of the caption band, **never over Dan's face or abs** — position each by
measuring the person mask on the RENDERED frame (head + torso box → largest clear band, usually above the head or
beside him). Put every chip in the plan's `real_photos` / `ai_inserts` (or v2 `label_tracks`) so the gate measures it.

## 5. Framing (talking head)

* Locked hair-anchored standard, two levels only: **NEAR** = hair → belly button, **FAR** = hair → shorts line with
  the waistband in frame; `y0 = hold's minimum hair top − 4 % of crop height`. Measure with
  `.claude/skills/website-video/reference/recipe/hairdet.py`, prove on a native-scale proof sheet of the tallest
  frames, gate the delivered frames with `hairgate.py`.
* **9:16**: the crop is a 9:16 window of the portrait source. Expected sizes: FAR ≈ 1000 px tall (≈ 1.9× upscale to
  1920), NEAR ≈ 840 px (≈ 2.3×). Use lanczos, no sharpening pass. Measure delivered face sharpness against the
  approved Ad 1 vertical and record it (§8) — this is a footage-report finding, not a reason to add a wide level.
* **16:9**: hair-anchored crops of the same portrait source (NEAR ≈ 840 px tall × 1493 wide, FAR ≈ 1000 × 1778),
  same level schedule as the 9:16.
* **Fixed centre per hold** (`_shared/framing-motion.md`): a robust median of his torso position per hold; track only
  if a hold's motion cannot be contained, and say why. Never one coordinate across holds.
* Alternate the level across every visible join (zoom cut, never a naked jump cut); a level change on a sentence
  boundary at least every ~12 s in uninterrupted talk. Gate rows to satisfy: `framing:hair_top`, `framing:headroom`,
  `framing:centering` (≤ 6 % of width), `framing:push_coverage` (spread ≥ 1.10).

## 6. Audio

1. `bash .claude/skills/_shared/audio/selftest.sh` first.
2. Lav per `C1663.MP4.audio_source.json`, mono → centred stereo, through **`voice_chain.py`** only (dereverb only if
   the room measures > 55 ms — outdoors it should not). Music bed ON (locked 2026-08-23): choose from
   `/Volumes/Extreme/_edit_work/ad1-8-14/music/*.mp3` (Pixabay, no attribution) with
   `.claude/skills/ad-edit/reference/rev5/pick_bed.py`, bed ≤ −30 dB ducked. Transition SFX from `_shared/sfxlib.py`
   on card ins only. Target −14 LUFS, true peak ≤ −1.0 dBTP (the chain's −2.5 is fine).
3. `audio_gate.py <master> --ab <AB file>` on BOTH delivered masters; both must PASS.
4. The 16:9 carries the identical mix (same PCM, encoded once, or stream-copied).

## 7. Captions, graphics, gates

* **Captions**: burned, word-timed from Whisper on the FINAL mix (never estimated windows), MadMuscles style (Arial
  Bold, white, black outline, current-word highlight as in the approved Ad 1 / Ad 3 verticals). Geometry from the
  approved vertical recipe `Zeeshan Ad Videos/this picture got me abs - ad 1/recipe-vertical/captions.py` (PlayRes
  1080×1920, its band); 16:9 per the skill (~64 px at 1080p, low third). Captions sit above the CTA pill, never on a
  card or chip, never over a label. **First 30 s proofed word for word.** Corrections dict must include
  `apps → abs` (Whisper mishears "abs" as "apps" throughout this roll) and `RIP → ripped`. "abs" lowercase always;
  "AI" uppercase.
* **Graphics**: J2AD palette (`_shared/motionlib.py`), minimal-first — only the beats in §4, the CTA pill and the
  chips. Start from `reference/rev5/{gfx5,layout5,captions5}.py` and the Ad 1 vertical recipe; both builds in one
  script so a revision re-renders both.
* **Gates, on the delivered files, in this order**: `audio_gate.py` → `gate.py --format ad9x16 --plan plan.json` and
  `gate.py --format ad16x9 --plan plan16.json` (read `gate.py --plan-keys`; supply `real_photos`, `ai_inserts`,
  `cards`, `graphics`, `joins`, `covered`, `punch`, `words`, `transcript_words`, `source_audio`, `banned_source`,
  `watch_log`, `negative_events_scan` — a missing key FAILS as NOT MEASURED) → `watch:pass` is a hard row for
  ad9x16: produce `logs/watch_pass.json` from a real frame-by-frame pass over every cut point. **Never edit
  `formats.py`, a check, or a threshold.** If a row fails, fix the build; if you believe the row itself is wrong,
  write that in `ROUND-n-EDITOR.md` and leave it failing.
* Also run the skill's compliance scan (§9 of the skill) and the negative-imagery scan; record both.
* Machine cap: `ps -Ao pcpu,command | grep -E 'ffmpeg|whisper|render\.py|gate\.py|qc_style' | grep -v -E 'grep|Renderer'`
  before every render or gate; if two builds are running, wait.

## 8. Footage-report measurements (`measurements-RA-01.json`) — capture while you work

The planning session writes `Docs/SHOOT_828_FOOTAGE_REPORT.md` from this file. Fill every key; write `null` with a
`_why` note if a value truly cannot be measured.

```
decoded_size, rotation_side_data, fps, duration_s
audio: {streams, channels, dual_mono_corr, lav_snr_db, rms_dbfs, clip_count, noise_floor_between_words_dbfs,
        decay_ms (from audio_gate), wind_or_rain_events: [t,...], chosen_map}
grade: {lut, exposure_chosen, exposures_tested: {e: {face_luma, face_chroma_ab}}, reference_frame_used,
        sky_clip_pct, tree_noise_sd_flat_patch}
framing: {hair_top_px_per_hold: [...], belly_px, waistband_px, feet_px, dan_width_frac,
          near_crop_px: [w,h], far_crop_px: [w,h], near_upscale, far_upscale,
          face_sharpness_lapvar: {source_native, delivered_9x16, ad1_vertical_reference}}
focus: {face_sharp: bool, notes}
eyeline: {method, yaw_deg_est, pitch_deg_est, notes}  # is he reading off-axis? where was the prompter?
lighting: {sky_vs_face_luma_ratio, shadow_side, notes}
takes: {full_passes: 1, retakes: {L5: 2}, false_starts: 1, crew_chatter_s, usable_span_s, airtight_speech_s}
length: {airtight_s, lines_cut: [...], final_9x16_s, final_16x9_s}
```

## 9. Calls for Dan (put these in `notes-RA-01.md` under "Your calls"; do not wait on them)

1. The BEFORE picture is the AI-adjusted +8 lb version of a real 2022 photo, shown without a label (Ad 1 precedent).
   Confirm, or label it, or swap to the real `00_ORIGINAL_deckchair_upscaled3x.jpg` with the "Real picture" chip.
2. If L11 (or L7) was cut for length, the exact words removed.
3. Spoken claims kept as filmed: "This picture got me abs", "AI analyzed it and figured out exactly how much fat I
   had to lose" — flagged, not changed.
4. Whether the three after pictures should be the studio set (used) or the pool-shoot set.

## 10. What the editor must NOT do

Touch the raw roll; generate anything paid; upload anywhere; add a dashboard row; edit any gate, bound or corpus file;
change the delivered names; commit media; run a third concurrent build; speed-ramp; cut a CTA line; place a chip on
his face or abs; show two physique pictures at once; ask Dan a question mid-run (record it in §9 instead).

## 11. Round protocol

**Editor, end of round n** → `/Volumes/Extreme/_edit_work/ra01/ROUND-n-EDITOR.md`: what was built, exact paths, every
gate's result table (row → PASS/FAIL + number), deviations from this plan with reasons, §9 calls, and — for round ≥ 2 —
each reviewer defect with `fixed / not fixed + why`. Final message: `DONE round n` + the two master paths.

**Reviewer, round n** → `ROUND-n-REVIEW.md`. It receives only: this plan, `00-RULES.md`, `AGENTS.md`, the two masters,
their stamps and `recipe-RA-01/plan*.json` — never the editor's notes. It watches both files at full resolution, frame
by frame at every cut and every card in/out, checks every table in this plan, and reports:

```
VERDICT: SHIP | DOES NOT SHIP
DEFECTS (most serious first):
  D1  <file> <mm:ss.ff–mm:ss.ff>  <what the plan/rule requires>  →  <what the file shows>   severity: blocker|major|minor
CHECKED AND CLEAN: <plan sections verified with no finding>
COULD NOT VERIFY: <what and why>
```

A blocker or major defect = DOES NOT SHIP. Minor-only = SHIP with the minors listed for the next revision.
