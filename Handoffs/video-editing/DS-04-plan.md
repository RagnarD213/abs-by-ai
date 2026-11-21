# DS-04 build plan — "The Only Ab Exercise That Shrinks Your Belly Fat" (dedicated 9:16 short)

**Written 2026-09-16 by the planning session (Fable 5.1, high).** This is the spec the EDITOR (Opus 5, high) builds
to and the REVIEWER (a fresh Fable 5.1, high, that never sees the editor's notes) checks against. Where this plan and
the job doc `DS-04-only-ab-exercise-that-shrinks-belly-fat.md` disagree, this plan wins (it was written after
measuring the rolls); `00-RULES.md` and `AGENTS.md` beat both. Anything not covered here follows
`.claude/skills/shorts/SKILL.md` (vertical finishing, captions, design system, gate) and `.claude/skills/ad-edit/SKILL.md`
Steps 1–4 (take selection, airtight cut, zoom cuts).

Round files live in the work dir: `ROUND-n-EDITOR.md` (editor), `ROUND-n-REVIEW.md` (reviewer). Max three rounds,
then the orchestrator takes the open defects to Dan.

**Same process as RA-01.** The RA-01 editor's pipeline in `/Volumes/Extreme/_edit_work/ra01/` (`ra01lib.py`,
`s01_env.py` … `s26_all.sh`) was built for the same portrait roll family and the same gate; **copy** it into the DS-04
work dir as a starting point and adapt it. Never run anything inside `ra01/` (another session's live build).

---

## 0. Measured facts about the rolls (planner, 2026-09-16) — these override the job doc

### C1656 — the talking roll

| fact | measured value |
|---|---|
| file | `/Volumes/Extreme/abs by ai 8:28 shoot \| jeff \| dan \| ads, dedicated shorts, b roll, scripted long form content/main camera/C1656.MP4` (read-only), 87.6 s |
| stored | 3840×2160, **rotation side-data −90** → ffmpeg autorotates to **2160×3840 PORTRAIT**. Never pass `-noautorotate`, never add a `transpose`. Probe a decoded frame and confirm 2160×3840 first. The job doc's "framed horizontal and centre-safe" is wrong for this roll: it is native vertical. |
| fps | 29.97 (30000/1001) |
| picture | S-Log3 / S-Gamut3.Cine, **outdoors, overcast, by the pool** (same set as C1663 / RA-01). Grade = `lut3d=file=/Volumes/Extreme/_edit_work/website-video-828/slog3_709_e1.45.cube:interp=tetrahedral,eq=saturation=0.88`, decoded BT.709 (`scale=in_color_matrix=bt709:in_range=tv`). If RA-01 round 1 recorded a chosen exposure for this set in `/Volumes/Extreme/_edit_work/ra01/expo.json`, use the same exposure so the dedicated shorts share one look; otherwise 1.45. Record the numbers (§8). No other grade change. |
| audio | **one stereo stream, dual-mono** (L/R correlate +1.000 at lag 0), lav on both. `pick_lav.py` already wrote `C1656.MP4.audio_source.json` beside the roll: SNR 42.4 dB, RMS −26.8 dBFS, EDT 26.7 ms (dry, outdoors → **no dereverb**), 0 clipped, prescribes `-map 0:a:0 -af "pan=mono\|c0=0.5*c0+0.5*c1"`. Use that JSON. Never hard-code a channel. |
| framing in source (2160×3840 decoded) | Dan full-body, shirtless, green shorts, glasses, lav on a necklace, centred at x ≈ 1010–1170. **Face skin starts at y ≈ 1020–1160 (hold-dependent), so hair top ≈ y 960–1100 (≈ 25–29 % down)**, belly button ≈ y 2070, shorts waistband ≈ y 2230, shoes ≈ y 3300. He spans x ≈ 760–1640 (≈ 40 % of the width). Re-measure per hold. |
| ⚠ hairdet on this roll | `hairdet.py detect()` fails here (returns `hair≈200, climb too long`): its "header" luma model assumes a bright wall above the head, and this roll has dark trees. Use it only for the skin-top (`skin`), then find the hair top as the last dark-run row within 150 px above the skin top at the head column, and **prove it on a native-scale proof sheet of the tallest frames** before rendering. Gate the delivered frames with `hairgate.py` as usual. |
| takes | one pass 0:09.3–0:44.4, then three attempts at the "Remember…" line, then the close. Crew talk after 1:16 (listen; the Whisper transcript ends at 1:11.7 + the last line). |

### C1677 — the new 16:9 vacuum b-roll (Dan's script asked for it)

Landscape 3840×2160, 29.97, 205 s, S-Log3, **sunny, hard side light**, poolside with the hot tub behind him, no
glasses, green shorts. Stereo audio = crew direction, not used. Three passes:

| pass | time | what it shows | use |
|---|---|---|---|
| front A | 0:00–0:28 | facing camera, hands on hips, holding vacuums (stomach drawn in, ribs out); 0:16 and 0:22–0:24 he exhales/mouths — fine | **cue 1** (L1) |
| profile | 0:47–0:80 | **side view**: 0:50–0:55 consciously slumped (belly relaxed, head down); 0:56 posture up; 0:57–0:61 sucks the stomach in; 0:62–0:70 holds; 0:71–0:80 second hold, more relaxed | **cue 2** (L7–L9): this IS the script's "breathe out, slump, then posture, suck in, hold" |
| front B | 1:40–2:52 | front vacuum holds again; 1:48 and 2:34 arm drops, 2:00 walks in | spare |
| empty | 0:30–0:46, 0:81–1:39, 2:53–3:25 | nobody in frame | — |

### C1682 — crunches and toe touches (8/28 exercise roll, the other pool, sunny, blue mat)

Landscape 3840×2160, 192 s. Dan on a blue mat, camera at ground level, house behind. 0:57–0:61 sit-up/crunch
reps (seated → lying, hands reaching), **0:62–0:79 toe touches** (legs vertical, reaching for the shoes, ~4 reps),
1:26–1:39 second toe-touch set, 1:41–1:45 seated. `short2_toe-touches.mp4` is a finished Short with burned captions;
never cut from it. **C1683** (172 s, same set) was checked: seated medicine-ball twists (0:10–0:52), planks and
kneeling ab-wheel rollouts — **no lying crunch set**, so the crunch pin is in C1682.

## 1. Deliverables

Delivery folder: `Short-form video content/` (git-ignored — `git check-ignore` before staging anything).
Work dir (create it): `/Volumes/Extreme/_edit_work/ds04/`.

| file | spec |
|---|---|
| `Short-form video content/ds-04_only-ab-exercise-that-shrinks-belly-fat.mp4` | **1080×1920, 30000/1001 fps, h264 yuv420p, AAC 48 kHz stereo, 45–66 s** (target 47–56 s; hard ceiling 66.00 s) |
| `…/ds-04_only-ab-exercise-that-shrinks-belly-fat.mp4.audio_gate.json`, `….deliver_gate.json` | PASS stamps at the current `GATE_VERSION`, sha256-bound to the delivered file |
| `…/REVIEW_540p_ds-04_only-ab-exercise-that-shrinks-belly-fat.mp4` | 540p review copy for Dan's phone |
| `…/AB_ref-vs-ours_ds-04_only-ab-exercise-that-shrinks-belly-fat.mp4` | the audio gate's A/B clip |
| `…/covers/posted covers/ds-04_only-ab-exercise-that-shrinks-belly-fat_cover-A.png`, `…_cover-B.png` + `…/covers/posted covers/youtube/…_cover-A.png`, `…_cover-B.png` | two copy variants × the Instagram and YouTube layouts, built with `/coverimage` (§7) |
| `…/ds-04_notes.md` | take map, every choice and deviation, gate tables, the calls for Dan (§9) |
| `…/ds-04_recipe/` | every script and JSON needed to rebuild the file (copy of the work-dir pipeline + plan.json) |
| `/Volumes/Extreme/_edit_work/ds04/measurements-DS-04.json` | the footage-report numbers (§8) |

No upload, no Blotato, no dashboard row, no Google Ads, **$0 AI generation**. Commit docs/scripts only (this plan, the
job status files), never media.

## 2. Take map (Whisper pass on C1656, times ± 0.5 s — re-align with word timestamps)

Script = `Media/codex-video-trial/05-recipes/candidates/shoot5-notes.txt` lines 665–676. Spoken words win over the
script where they differ; flag drift in the notes.

| line | script (spoken drift in brackets) | source time | use |
|---|---|---|---|
| slate | "This video is the only ab exercise that shrinks your belly fat." | 0:00–0:09 | discard |
| L1 | THIS is the only ab exercise that actually shrinks your stomach. | 0:09.3 | keep — cold open, **cue 1** |
| L2 | Regular ab exercises make your abs look better - if you're already lean. | 0:13.8 | keep — **cue 3** (crunches/toe touches) |
| L3 | But if you have belly fat, they just make your belly bulge out more. ["belly fat bulge out more"] | 0:18.2 | keep |
| L4 | The vacuum is the only ab exercise that can actually shrink your waist. | 0:22.3 | keep |
| L5 | It does this by training your transverse abdominus, the sleeve of muscle that stabilizes your core. [Whisper hears "transverse of dominance" — caption must print **transverse abdominis**] | 0:26.5 | keep |
| L6 | Here is how you do it. ["Here's how you do it."] | 0:31.7 | keep — **cue 2 starts on the next line** |
| L7 | Breathe all the way out, and consciously slump. | 0:33.2 | keep — cue 2 |
| L8 | Then consciously posture, suck your stomach in like you are posing in a bodybuilding show, ["posing for a bodybuilding show"] | 0:35.7 | keep — cue 2 |
| L9 | and hold. ["Then hold."] | 0:41.0 | keep — cue 2 |
| L10 | Three sets of twenty to thirty seconds. | 0:42.0 | keep — chip |
| L11 t1 | "Remember, the vacuum does not burn off fat." (wrong words, stops) | 0:44.4 | discard |
| L11 t2 | "Remember, the vacuum does not burn fat off your stomach." (stops) | 0:47.6 | discard |
| L11 t3 | Remember, the vacuum does not burn fat off your stomach. But it does pull your waist in so your waistline looks smaller - even if you have belly fat right now. ["pull in your waist so that your waistline looks smaller even if you have some belly fat right now"] | 0:57.0–≈1:05.5 | **keep** (only complete take) |
| L12 | If you still have stomach fat, this is the ab exercise you should focus on until you have a flat stomach. | 1:05.9 | keep |
| L13 | Try the vacuum, and leave a comment to let me know how it worked for you. [Whisper dropped "Try"] | 1:11.7–≈1:15.5 | keep — CTA, final line. **Listen for "Try"**: if he says it, keep it; if the audio really starts on "the vacuum", cut in on **"leave a comment to let me know how it worked for you"** instead and record it (§9). Check 1:16–1:27 for a retake before deciding. |

Only one usable take exists for every line except L11, so the "take reel for Dan" step is moot: skip it, say so.

## 3. Length rule

Airtight pause removal per `/ad-edit` (word boundaries place the cuts, silence validates; ≤ 0.35 s between
sentences, natural breath kept before "Remember"). Estimated airtight speech ≈ 47–50 s + a 1.0 s end hold on the
CTA chip. That sits inside 45–66 s. **No speed ramp, no line cut**, never cut L13. If the airtight cut lands under
45 s, do not pad with dead air: let the two b-roll beats carry their natural 0.3–0.5 s tails and hold the end card
to 1.5 s. Record the final length. Container duration must read ≤ 66.00 s.

## 4. Cue map — what is on screen (one 9:16 timeline)

Every asset exists. **AI-generation budget: $0.** No stock. Everything below is Dan.

| beat | on screen | source | treatment | label |
|---|---|---|---|---|
| L1 (9.3–13.8) | **cue 1: front vacuum** | C1677 front A, **0:11.0–0:15.5** (hands on hips, stomach drawn in). Pick the cleanest 4.5 s hold inside 0:08–0:27; avoid the exhale at 0:16 unless it lands on a word. | native-vertical crop of the 16:9 frame: hair-anchored **hair → mid-thigh**, fixed centre on his torso, ~1500 px tall crop (≈ 1.0–1.3× scale into the picture window). No J2 frame — he fits the vertical. | none (real footage of Dan, not a still result photo — `AGENTS.md` "Real videos are not still photos") |
| L2 (13.8–18.2) | **cue 3: crunches → toe touches**, two clips, ~2.2 s each, hard cut between | crunch: **C1682 0:57.5–0:59.7** (sit-up/crunch rep — pick the one rep inside 0:57–0:62 where he curls up fully); toe touch: **C1682 0:66.0–0:68.2** (one full rep, legs vertical, hands to shoes) | he is lying on a mat, so a 9:16 crop slices him: use the **card** treatment — crop the 16:9 to a **4:3 window that contains his whole body** (never slice a limb or the mat edge mid-body), scale to 1080×810, **top-aligned at the picture window's top edge**, J2 field below/around, caption band clear. (Skill judgement call Dan endorsed: "treat a horizontal pose as a card rather than cropping it".) | none |
| L3–L6 (18.2–33.2) | Dan on camera, zoom cuts on the sentence joins | C1656 | §5 | — |
| L5 chip | `TRANSVERSE ABDOMINIS` olive chip in the band's chip slot from "transverse" to the end of L5 | — | §6 | — |
| L7–L9 (33.2–42.0) | **cue 2: the how-to, profile**, one continuous piece | C1677 profile, cut in at **0:51.7 when L7 starts** (offset +18.5 s), run continuously to the end of L9: slump under "breathe all the way out and consciously slump" (0:51.7–0:55.5), he straightens at 0:56 under "Then consciously posture", draws in at 0:57–0:58 under "suck your stomach in", holds through 0:61.7 under "and hold". **Adjust the offset by ≤ 0.5 s so the draw-in lands on "suck your stomach in"; never speed-change the clip.** | native-vertical crop **hair → mid-thigh** on his profile, fixed centre (he sways slightly; contain, do not track) | none |
| L7 / L8 / L9 chips | `1 · BREATHE OUT + SLUMP` → `2 · POSTURE + SUCK IN` → `3 · HOLD`, one at a time, each switching on the first word of its line | — | §6 | — |
| L10 (42.0–44.4) | Dan on camera; chip `3 SETS × 20–30 SEC` from "Three" to the end of the line + 0.8 s | C1656 | §5 | — |
| L11–L12 (57.0–71.5) | Dan on camera, zoom cuts on the sentence joins (three sentences in L11: "Remember…stomach." / "But it does…right now." / L12) | C1656 | §5 | — |
| L13 (71.7–end) | Dan on camera; chip `COMMENT: DID IT WORK?` from "leave a comment" through the end hold (1.0–1.5 s after the last word) | C1656 | §5 | — |

Rules that bind every beat: no physique still photos at all in this short (so no real/AI chips are needed — say so
in `plan.json` by leaving `real_photos` and `ai_inserts` empty lists, not missing); no before/after; no app screens;
no email screen; on-screen text never states a result claim or a number other than the set/rep instruction; no drug
names. The spoken "does not burn fat off your stomach" stays exactly as filmed.

**The two vacuum cues are two different camera setups of C1677 (front, then profile), 40 s apart, not two trims of
one shot.** The job doc's alternative for cue 2 (`v3-short6_vacuum-exercises.mp4`) is a finished Short with burned
captions and is not used. Flag the choice in §9.

## 5. Layout and framing

**Layout (the shorts design system, `/shorts` Step 7 + "Locked design system"):** the title stays on screen for the
whole short and never touches Dan, so the picture is dropped:

```
0–380        J2 title band (field #0D0E0B, faint grid, olive perimeter, corner brackets)
               eyebrow  Copperplate, olive, letter-spaced, ~40 px:   THE ONLY AB EXERCISE THAT
               headline Impact, white, 2 lines, ~96–104 px:          SHRINKS YOUR / BELLY FAT
               chip slot y 312–368, left-aligned x 40: one olive-bordered chip at a time (§4), empty when no chip is due
               AbsByAI.com camel-case, small, muted, bottom-right of the band
380–1920     picture window 1080×1540 (aspect 0.701): Dan / b-roll rendered here
captions     Arial 86 bold white, outline 7, shadow 3, Alignment 2, MarginV 690, PlayRes 1080×1920 (canonical)
```

Assert on the DELIVERED file that the title's glyph box never intersects the person mask (the skill's
`titleclear.py` method) and that no chip ever sits on the picture.

**Talking-head crops (C1656)** — the locked hair-anchored standard, two levels only, measured per hold:
* **NEAR** = hair → belly button (≈ 1160 px tall → ≈ 813 wide at the window's aspect; ≈ 1.33× scale),
  **FAR** = hair → shorts line with the waistband in frame (≈ 1330 px tall → ≈ 932 wide; ≈ 1.16×).
  `y0 = hold's minimum hair top − 4 % of crop height`. Lanczos, no sharpening.
* **Fixed centre per hold** (`_shared/framing-motion.md`): robust median of his torso x per hold; no tracking unless a
  hold cannot be contained, and then say why. Never one x across holds.
* Alternate NEAR/FAR across every visible join; a level change on a sentence boundary at least every ~12 s of
  uninterrupted talk. Zoom cuts, never naked jump cuts. The b-roll beats hide their joins (declare them `covered`).
* Gate rows to satisfy (`short` format): `framing:hair_top`, `framing:headroom` (30–70 px per segment, scaled), `framing:centering`
  (≤ 6 %), `framing:no_wide_level`, `framing:push_coverage` (spread ≥ 1.10). Declare the picture window in
  `talking_head_windows` so the gate measures inside it, not from the canvas top.

**B-roll crops (C1677 / C1682)**: fixed centre per clip, contain the movement (§4), hair-anchored on the standing
clips; the 4:3 card for the mat clips.

## 6. Graphics

J2AD palette from `_shared/motionlib.py` (`chip()`, OLIVE 140,152,88). Minimal-first: the band, the six chips in §4,
nothing else. Chips are square-cornered, olive-bordered, Copperplate/Impact mission style ("TARGET: LOWER ABS"), one at
a time, each ≥ 1.2 s on screen. Start from the scored-source layout (`.claude/skills/shorts/reference/scored-source/`)
for the band and `build-assets.py` for the chip/title PNGs; adapt to `dropTop 380`.

## 7. Audio, captions, cover, gates

* **Audio**: `bash .claude/skills/_shared/audio/selftest.sh` first. Lav per `C1656.MP4.audio_source.json`, mono →
  centred stereo, **`voice_chain.py` only**, no dereverb (EDT 26.7 ms). Music bed: a low Pixabay bed from
  `/Volumes/Extreme/_edit_work/ad1-8-14/music/` chosen with `.claude/skills/ad-edit/reference/rev5/pick_bed.py`,
  ≤ −30 dB under the voice, faded head and tail, dipped at every join (the organic standard — Zeeshan's approved
  ab-wheel videos carry one). Target −14 LUFS, true peak ≤ −1.0 dBTP. `audio_gate.py <master> --ab <AB file>` on the
  delivered file; must PASS.
* **Captions**: burned, word-timed from Whisper on the FINAL mix (never estimated), canonical spec (§5), 2–4 word
  chunks, `abs` lower-case, `AI` upper-case, punctuation-token merge before chunking. Corrections dict must include
  `transverse of dominance → transverse abdominis`, `apps → abs`, `RIP → ripped`. **Every caption proofed word for
  word** (the whole short is under 60 s). A word counts as spoken only if > 50 % of it is inside the cut.
* **Cover** (`/coverimage`): a photo first — build the contact sheet of `photos/finalized social media photos/` and
  pick a standing shot where the abs read hardest, ideally a vacuum-like drawn-in pose; nothing from `Frowning Photos/`.
  If no photo suits, the fallback is a C1677 front-A frame at a full vacuum hold, retouched per the skill. Two copy
  variants, both layouts (Instagram + YouTube builders): **A** eyebrow `THE ONLY AB EXERCISE` / headline `THAT SHRINKS
  BELLY FAT`; **B** eyebrow `BELLY FAT?` / headline `DO THE VACUUM`, subtitle `3 SETS · 20–30 SEC`. No result claim
  beyond the video's own title; no `AbsByAI.com` on the cover unless Dan asks (`AGENTS.md` thumbnail rule).
* **Gates, on the delivered file, in this order**: `audio_gate.py` → `_shared/deliver/watch.py` (real frame-by-frame
  pass over every cut, card in/out and chip in/out → `logs/watch_pass.json`, judged) → `gate.py --format short --plan
  plan.json` (read `gate.py --plan-keys`; supply `target_seconds`, `joins`, `covered`, `punch`, `graphics`,
  `real_photos: []`, `ai_inserts: []`, `cards`, `talking_head_windows`, `words`, `transcript_words`, `source_audio`,
  `watch_log`, `negative_events_scan`, `captions_ass`, `speech_words` + evidence — a missing key FAILS as NOT MEASURED).
  **Never edit `formats.py`, a check or a threshold.** If a row fails, fix the build; if you believe the row is wrong,
  write that in `ROUND-n-EDITOR.md` and leave it failing.
* Also run the shorts skill's compliance scan and the negative-imagery scan; record both.
* Machine cap before every render, transcription or gate:
  `ps -Ao pcpu,command | grep -E 'ffmpeg|whisper|render\.py|gate\.py|qc_style' | grep -v -E 'grep|Renderer'` — two
  builds running → wait.

## 8. Footage-report measurements (`measurements-DS-04.json`) — capture while you work

The planning session writes the talking-short + exercise-b-roll section of `Docs/SHOOT_828_FOOTAGE_REPORT.md` from
this file. Fill every key; write `null` with a `_why` note if a value truly cannot be measured.

```
c1656: {decoded_size, rotation_side_data, fps, duration_s,
        audio: {streams, channels, dual_mono_corr, lav_snr_db, rms_dbfs, clip_count,
                noise_floor_between_words_dbfs, decay_ms (from audio_gate), wind_or_crew_events: [t,...], chosen_map},
        grade: {lut, exposure_chosen, exposures_tested: {e: {face_luma, face_chroma_ab}}, reference_frame_used,
                sky_clip_pct, tree_noise_sd_flat_patch},
        framing: {hair_top_px_per_hold: [...], skin_top_px_per_hold: [...], belly_px, waistband_px, shoes_px,
                  dan_width_frac, near_crop_px: [w,h], far_crop_px: [w,h], near_scale, far_scale,
                  face_sharpness_lapvar: {source_native, delivered, ad1_vertical_reference}},
        focus: {face_sharp: bool, notes}, eyeline: {method, yaw_deg_est, pitch_deg_est, notes},
        lighting: {sky_vs_face_luma_ratio, shadow_side, notes},
        takes: {full_passes: 1, retakes: {L11: 3}, false_starts: 2, crew_chatter_s, usable_span_s, airtight_speech_s},
        length: {airtight_s, final_s}}
c1677: {size, fps, duration_s, lighting: {face_luma_lit_side, face_luma_shadow_side, ratio, sky_or_wall_clip_pct},
        passes: [{name, t0, t1, view, usable}], vertical_crop: {crop_px: [w,h], scale, dan_height_frac},
        exposure_vs_c1656: {lut_exposure_used, face_luma_c1677, face_luma_c1656, note},
        crew_audio: bool, empty_s}
c1682: {size, fps, duration_s, camera_height, sets: [{move, t0, t1, reps}], usable_vertical: bool, why,
        card_crop_px: [w,h,x,y]}
c1683: {same as c1682}
```

## 9. Calls for Dan (put these in `ds-04_notes.md` under "Your calls"; do not wait on them)

1. On-screen title wording: the band prints the script's own title (SHRINKS YOUR BELLY FAT) while Dan says on camera
   the vacuum "does not burn fat off your stomach". Keep the title, or change it to `SHRINKS YOUR WAIST`?
2. Both vacuum cues come from the new C1677 roll (front pass, then the profile how-to). OK, or swap cue 1 to the 8/14
   live set (C1625, 1080p — softer)?
3. L13: whether "Try" was on the audio and what the CTA line finally says.
4. The lying-exercise clips are shown as a 4:3 card on the J2 field (not a sliced 9:16 crop). OK?
5. Music bed on/off for dedicated shorts (the plan puts a low bed on).
6. Cover A vs B, and photo vs the C1677 frame.

## 10. What the editor must NOT do

Touch the raw rolls; generate anything paid; use stock; upload anywhere; queue in Blotato; add a dashboard row; edit any
gate, bound or corpus file; change the delivered name; commit media; run a third concurrent build; speed-ramp; cut
L13; put a title or chip on Dan; slice a limb off in a crop; cut from a finished Short (`v3-short6…`, `short2…`); ask
Dan a question mid-run (record it in §9 instead).

## 11. Round protocol

**Editor, end of round n** → `/Volumes/Extreme/_edit_work/ds04/ROUND-n-EDITOR.md`: what was built, exact paths, every
gate's result table (row → PASS/FAIL + number), deviations from this plan with reasons, §9 calls, and — for round ≥ 2 —
each reviewer defect with `fixed / not fixed + why`. Final message: `DONE round n` + the master path.

**Reviewer, round n** → `ROUND-n-REVIEW.md`. It receives only: this plan, `00-RULES.md`, `AGENTS.md`, the delivered
master, its stamps, the covers and `ds-04_recipe/plan.json` — never the editor's notes. It watches the file at full
resolution, frame by frame at every cut, every chip in/out and every card in/out, reads every caption against the
audio, checks every table in this plan, and reports:

```
VERDICT: SHIP | DOES NOT SHIP
DEFECTS (most serious first):
  D1  <file> <mm:ss.ff–mm:ss.ff>  <what the plan/rule requires>  →  <what the file shows>   severity: blocker|major|minor
CHECKED AND CLEAN: <plan sections verified with no finding>
COULD NOT VERIFY: <what and why>
```

A blocker or major defect = DOES NOT SHIP. Minor-only = SHIP with the minors listed for the next revision.
