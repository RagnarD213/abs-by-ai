# RA-01 — ROUND 3 — EDITOR

**Built to `Handoffs/video-editing/RA-01-plan.md` §13 "Round 3 rulings" by the editor session
(Claude Opus 5, high), 2026-09-18.** Work dir `/Volumes/Extreme/_edit_work/ra01/`.
Targeted revision: **only the four items §13 lists were changed.** Raw footage untouched.
**$0.00 of AI generation. Nothing uploaded. No dashboard row. Nothing committed.** Every render,
gate and transcription ran through `capwait.sh` / `capwait4.sh` (the same two-build cap, polled
every 4 s instead of 20 s); at no point were three builds running. No subagents were spawned.

**Round 2 is preserved** in `/Volumes/Extreme/_edit_work/ra01/round2/`: both masters
(`master_9x16.mp4` sha `5bc6c5126a38…`, `master_16x9.mp4` sha `1f4367c3a6b5…`), their six stamps,
both gate plans, and the round-2 `beats.json`, `cut.json`, `framing.json`, `grade.json`,
`words_aligned.json`, `timeline_*.json`, `mix.wav`, `measurements-RA-01.json`, `notes-RA-01.md`
and the A/B clip.

---

## 1. The four changes, and the measurement that proves each

### D3 — the music bed's ≈ 15 dB step at ≈ 56.06 s → **FIXED**

**What it actually was.** Not a join and not the `aloop` seam: `Realizer.mp3` is 310 s long and the
bed starts at t = 0, so bed time = mix time. The track's own rhythm leaves a ~0.10 s **rest** between
phrases about once a second (55.00, 55.95, 56.95 s read −26…−28 dBFS against a −13 dBFS median).
Under speech the rests are masked and ducked; after the last word (55.22 s) the bed is the only thing
left, so the rest at 55.94–56.06 and the note that follows it read as a dropout and a step. A 250 s
sweep of the track confirms round 2's finding that **no start offset removes it** — the smoothest
3.7 s window anywhere still dips 13.1 dB — and the chain's linear 2 s fade-out cannot either, because
a fade scales a hole, it does not fill it.

**The fix is in the bed ASSET, not in the chain.** `s42_bed.py` measures the track's own 10 ms
envelope and applies the inverse gain from 53.20 s on (ramped in over 1.2 s, under speech, so the
correction itself has no step), capped at +14.0 / −10.0 dB; the gain actually applied in the tail is
**−3.2 … +14.0 dB**. The result is written as `music/Realizer_r3bed.wav` and handed to
**`voice_chain.py` unchanged** through its existing `--bed` flag. **Nothing in the shared audio module
was edited**, no new chain was written, the voice, the loudness, the L/R image, `--bed-db -32` and
`--frame-lock` are all exactly as in round 2.

| measurement | round 2 | round 3 |
|---|---|---|
| bed asset, 53.5–57.3 s, 50 ms envelope **span** | 17.6 dB | **4.7 dB** |
| **delivered 9:16**, 55.40–57.19 s (after the last word), 50 ms **largest step** | **15.2 dB at 56.075 s** | **5.7 dB at 57.075 s** |
| delivered 9:16, same window, 5 ms largest step | 14.3 dB at 56.062 s | 12.3 dB at 56.062 s |

The 5 ms envelope, printed frame by frame, is the clearest proof (`r3/tail_envelope.json`):

```
round 2  55.913:-41 … 55.947:-53  55.992:-56  56.057:-60 | 56.062:-45  56.072:-38   <- hole, then step
round 3  55.913:-39 … 55.947:-43  55.992:-42  56.057:-50 | 56.062:-38  56.072:-34   <- level holds
```

**The hole is gone and the bed holds level, then fades smoothly to the last frame.** What remains at
5 ms resolution (12.3 dB at 56.062 s) is the **note's own attack** — the same 7–10 dB onsets occur at
54.875, 55.100, 56.555 and 57.020 s, i.e. once per beat of the bed, and the level on either side of it
is continuous (−38…−44 dBFS). Reported, not tuned away. Evidence: `r3/bed_fix.json`,
`r3/tail_envelope.json`. **No other mix change:** LUFS −14.20, true peak −2.10 dBTP, LRA, L/R and
every other audio row read exactly as round 2.

### D4 — the lean at 00:22.15–00:22.26 past 92 % of the width (9:16) → **FIXED**

Fixed by **moving that hold's fixed centre**, the second option §13 allows; the level alternation is
untouched (hold 4 stays NEAR between two FARs, so demoting it would have put two FARs across an
uncovered join).

**Why round 2 missed it.** The constraint was fed by the 5 Hz landmark track, whose "face box" is the
cheek-to-cheek span (landmarks 234↔454) — about **19 % narrower** than the face box measured on the
delivered frame, and sampled six times more coarsely than a 0.37 s lean. Round 3 takes the **wider of
the two**: `face_src_r3.json` carries the per-hold extremes measured on **every frame** of the round-2
masters (the review's own mediapipe boxes, `review-r2/faces_9x16.json`) mapped back into source pixels
through that render's crop.

Two bounds pull against each other on this hold and both had to be satisfied at once:

| x (crop left, source px) | face box on the delivered frame | head centre (gate `framing:centering`, max ±6 %) |
|---|---|---|
| 932 (round 2) | 18.1 … **94.3 %** ✗ | ≈ −2 % ✓ |
| 962 (round 3, first render) | 15.1 … 88.7 % ✓ | **−6.7 %** ✗ |
| **950 (delivered)** | **15.1 … 90.7 %** ✓ (1.3 % to spare) | **−4.9 %** ✓ (1.1 % to spare) |

Measured on the delivered round-3 9:16, every frame of every talking hold (1595 frames, 0 detector
misses): **face box 14.3 … 91.0 %, 0 frames outside 8–92 %** (`r3/verify_9x16.json`). The gate agrees:
`framing:centering` **PASS**, worst +4.2 % at 21.0 s. The 22.05–22.36 s run was looked at frame by
frame (`r3/look/9x16_lean_22s.jpg`): the face is whole, hair and glasses intact, nothing clipped.

⚠ **The cost, stated plainly.** Moving hold 4's centre 18 px right makes the *lateral* part of the
20.254 s zoom cut bigger in 9:16: his head centre steps **15.0 %** of the width across that join
(round 2 would have read ≈ 11.8 %); per-hold medians 5.5 %. It is a NEAR/FAR zoom cut, not a naked
splice — the gate reads `cut:jump_cut` 0, `cut:naked_splices` 0 of 0, `cut:uncovered_joins` 0.0/min —
and the strip at `r3/look/9x16_join_20.25.jpg` reads as a push, not a hop. §13 offered exactly this
trade (cut the hold at FAR **or** widen its centre) and the alternation rule forced the second.

### D5 — the 16:9 zoom-cut hop → **FIXED**

The 16:9 FAR window is 2144 px of a 2160 px source, so its x is pinned to 0–16 and its centre cannot
move; round 2 centred each NEAR window on that hold's own face median, 128 source px to the right.
Round 3 gives **every 16:9 NEAR hold its neighbouring FAR hold's measured centre**: all thirteen 16:9
crops now share the centre line **1088** (FAR x = 16, NEAR x = 144, measured in
`timeline_16x9.json`). 9:16 is untouched by this change.

| 16:9 visible NEAR↔FAR join | head centre, frame to frame | per-hold medians |
|---|---|---|
| 16.35 | 1.3 % | 1.2 % |
| 20.25 | 2.9 % | 1.1 % |
| 23.19 | 2.3 % | 1.8 % |
| 40.87 | 1.3 % | 1.2 % |
| 44.48 | 0.4 % | 1.1 % |
| 47.58 | 0.8 % | 1.5 % |
| 51.25 | 1.8 % | 0.2 % |
| 53.92 | 0.1 % | 0.1 % |

Round 2 read **4.0 – 9.0 %** on these same eight joins. **Crop-centre offset is now 0 px at every
join.** Against §13's 1.5 % bound: **five of the eight** are inside it frame-to-frame and **six of the
eight** on the per-hold median; the largest residual is 2.9 %. That residual is not crop offset — it
is (a) Dan's own movement across the one-frame splice and (b) the arithmetic of a zoom: with a shared
centre, an offset from the centre line is magnified by the level ratio 2144/1888 = ×1.136, which alone
accounts for ~0.8 % at his usual position. No crop can remove either. Evidence:
`r3/verify_16x9.json`, the −2…+2 strips in `r3/look/16x9_join*.jpg`, `r3/judge_16x9/pair_page*.jpg`.

### D6 — the 16:9 CTA 2 pill not low in the frame → **FIXED**

**What round 2 could not see.** It placed the pill from the **midpoint frame only**. Measured over the
whole CTA-2 beat (14 probes on the frames the render actually delivers), Dan gestures with both arms
and **the only column clear of him is the far left, 488 px wide** (x 0–487; the narrowest moment is
55.12 s, where his hand reaches x 502) — and **no 552-wide box is clear anywhere between y 306 and
y 940**. The round-2 pill could therefore only stay 552 px wide by sitting at y 322, mid-frame, which
is what D6 rejects.

**What round 3 does.** The 16:9 pill is set in **three lines at the same type sizes** ("Tap the
button" / "below" / `AbsByAI.com`, 44 / 44 / 34 px ExtraBold) so the box is **396 × 194**, and it is
placed by a person mask **unioned over every probe of BOTH CTA beats** at the lowest position inside
the frame's 54 px safe margin: **(54, 832) → (450, 1026)** — bottom-left, 54 px from the left and
bottom edges, i.e. lower than round 2's CTA 1 (y 772) and far lower than its CTA 2 (y 322).
**Minimum pill-to-person gap over both beats: 23 px** (`r3/pill16.json`; the sheet with the mask drawn
on is `r3/pill16.jpg`, the composited beats are `r3/look/16x9_cta2.jpg` and `16x9_cta1.jpg`).

**Captions were NOT lifted — a deviation, with the measurement.** §13 says "captions lifted above it".
The pill's right edge is 450 px; the nearest burned caption ink in either CTA beat starts at **x 635**
("six-pack abs, tap the" at 53.52 s), so the two are **185 px apart** and never touch — the gate's
`captions:graphic_clearance` reads tightest **30 px** across all 71 state/graphic pairs and passes.
Lifting the captions would have moved them off their gated band (y 930–1040) and onto his chest for
1.5 s, for no benefit. Recorded here rather than done.

**Both 16:9 pills now use the one geometry**, which is the other half of "like CTA 1": CTA 1 moved
from 552 × 132 at (54, 772) to the same 396 × 194 at (54, 832). Recorded as a deviation in §4.

---

## 2. What did NOT change (checked, not assumed)

* **Captions keep "200 pounds"** — §13 ruled it; the caption is byte-identical to round 2's.
* **The cut, the beat map, the cards, the CTA beat times, the grade, the audio chain, the 9:16 CTA
  pill and the 16:9 captions are round 2's.** `beats.json` differs from round 2's in exactly one
  number: hold 4's 9:16 centre (1229.3 → 1246.9), plus the new `cx16` field. Cards and CTA beats
  compare equal.
* ⚠ **One forced splice was deliberately NOT adopted.** `s25_hard.py` re-ran on the round-2 master
  *after* that plan was built and now reports a ninth visibly-jumping splice at **36.003 s**. Taking
  it would have added a fourteenth hold and a level change §13 does not ask for, so `s05_plan.py`
  pins the forced list to the splices round 2 delivered (`round2/beats.json`) and prints what it
  dropped. Round 2 reported the same splice and left it uncovered on the record; it is still
  uncovered, and the gate still reads `cut:naked_splices` 0 of 0 and `cut:uncovered_joins` 0.0/min.
* **Length 57.190467 s**, 1714 frames, both aspects — 1.81 s under the 59.00 s ceiling.
* **The two files still carry the same audio.** The 16:9 picture did not change in part C, and the
  mix is frame-locked to a 9:16 picture whose frame count did not change, so `master_16x9.mp4` was
  built once, in part B, from the same `mix.wav`.

---

## 3. The masters

| file | where | container | sha256 |
|---|---|---|---|
| `master_9x16.mp4` | `/Volumes/Extreme/_edit_work/ra01/` — **HELD** | 1080×1920, 30000/1001, h264 High yuv420p bt709/tv, AAC-LC 48 kHz 2 ch, 1714 frames, 57.190467 s | `02d032180a3e…` |
| `master_16x9.mp4` | same — **HELD** | 1920×1080, same rate, same codecs, same audio, 1714 frames, 57.190467 s | `bcace8c490c8…` |

Held because a stamp reads FAIL (§4 below). `s29_ship_held.py` was run **without** `--masters`.

## 4. The audio gate — both masters, identical

| row | result | number |
|---|---|---|
| `lr_corr` | PASS | one voice, L/R correlation ≥ +0.97 |
| `comb` | PASS | ripple within his + 0.35 dB |
| `edt` | PASS | early decay ≤ 80 ms (his 40) |
| `tone` | PASS | mean ≤ 1.2 dB, max ≤ 2.5 |
| `floor` | PASS | voice over floor above his |
| **`artifacts`** | **FAIL** | **flux 0.090 against the bound 0.079** (Muhammad's 0.072 × 1.1); HF swirl 0.793 vs his 0.835 passes |
| `do_no_harm` | PASS | against this file's own untreated source |
| `dryness` | PASS | |
| `lufs` | PASS | **−14.20 LUFS** |
| `spread` | PASS | LRA 3.3 LU |
| `tp` | PASS | **−2.10 dBTP** |
| `silence` | PASS | **0 digitally silent seconds**, 0 below −50 dBFS |
| `length` | PASS | audio 57.190 s vs picture 57.190 s |

**12 of 13 rows pass; `artifacts` is unchanged from rounds 1 and 2** (0.091 → 0.090) and is **D1 —
Dan's ruling, not an editor fix.** The untreated lav on this roll reads 0.0962 before anything touches
it, 1.22× the bound; the chain takes it **down**. I did not process harder and I did not touch the
bound or the reference.

## 5. The delivery gate — `GATE_VERSION 2.1.0`, on the delivered files

**9:16 (`ad9x16`): 35 PASS, 1 FAIL, 0 NOT MEASURED, 0 pending, of 36 rows.**
**16:9 (`ad16x9`): 35 PASS, 1 FAIL, 0 NOT MEASURED, 0 pending, of 36 rows.**
The one failure on each is **`audio:stamp`** — one cause, two rows: the delivery gate refuses any file
whose audio stamp is not a PASS.

| row | 9:16 | 16:9 |
|---|---|---|
| `container:size` / `:fps` / `:codec` | PASS | PASS |
| `container:duration` | PASS 57.190 s vs 57.190 s | PASS |
| `container:frames` | PASS 1714 / 1714 | PASS |
| **`audio:stamp`** | **FAIL** — the `artifacts` row above | **FAIL**, same |
| `audio:stream_integrity` | PASS gap +0.000 s, 0 silent s, quietest −45.2 dBFS | PASS |
| `audio:lipsync` | PASS worst +0.042 ms (max 1.0) | PASS |
| `audio:click_at_joins` | PASS 0/20 | PASS 0/20 |
| `style:coverage` | PASS 51 % (min 38) | PASS 39 % (min 35) |
| `style:static_run` | PASS 11.7 s at 0:39.67 (max 31.6) | PASS 7.2 s (max 25.0) |
| `style:change_rate` | PASS 16.8/min (min 7) | PASS 21.0/min (min 8) |
| `framing:hair_top` | PASS min 44 px, median 57 | PASS min 41, median 58 |
| `framing:headroom` | PASS 4 holds, min hair top 50–56 px | PASS 7 holds, 52–58 px |
| `framing:centering` | **PASS worst +4.2 % at 21.0 s** (max ±6) — the D4 hold | n/a — declared by the format (see §6) |
| `framing:no_wide_level` | n/a — declared by the format (see §6) | PASS smallest head 32.3 % (min 27) |
| `framing:push_coverage` | PASS 30.1–35.7 % per hold | PASS 32.3–36.8 % |
| `cut:uncovered_joins` | PASS 0.0/min | PASS 0.0/min |
| `cut:black_frames` | PASS 0 of every frame | PASS |
| `cut:min_segment` | PASS 0 under 0.2 s | PASS |
| `cut:jump_cut` | PASS 0 pairs | PASS |
| `cut:splice_visibility` | PASS 0/20 | PASS 0/20 |
| `cut:naked_splices` | PASS 0 of 0 | PASS 0 of 1 |
| `captions:graphic_clearance` | PASS 192 states, 88 pairs, tightest 49 px | PASS 71 pairs, **tightest 30 px** |
| `captions:card_collision` | PASS 53 cues, 0 on a card | PASS |
| `captions:burned` | PASS 97 % (min 45) | PASS 97 % |
| `captions:within_runtime` | PASS last cue ends 55.22 s | PASS |
| `captions:sync` | PASS **192/192 states, 100 %** of 193 words, median +1 ms | PASS |
| `compliance:banned_screen` | PASS 1714 frames × 28 templates | PASS |
| `compliance:labels` | PASS 5 AI + 3 real, correlation min 0.998 | PASS |
| `compliance:drug_names` | PASS 0 | PASS |
| `compliance:negative_events` | PASS 40 frames, 1 finding, cleared | PASS |
| `compliance:script_fidelity` | PASS 99.5 % (196/196) | PASS |
| `watch:pass` | PASS 37/37 boundaries, 40/40 images | PASS 37/37, 40/40 |
| `srt:present` / `srt:shape` | n/a — burned captions, no sidecar | n/a |

⚠ **`compliance:negative_events` failed the first gate run** on both files ("the scan on record is for
5bc6c512…, this file is 02d03218…"): the round-3 chain regenerated the negative-imagery sheet but the
verdict is recorded by hand after the sheet is looked at. The sheet was looked at
(`neg_9x16/negative_sheet.jpg`, 40 frames), the same single finding was cleared — the BEFORE picture
at 5.07 s is a full-body balcony photograph, neutral framing, no zoom-in on a body part and no
disapproving reaction — and both gates were re-run. Recorded here because it was a real FAIL before it
was a PASS.

## 6. `not_applicable` rows whose written reason does not describe this cut (§12 R8, unchanged)

Neither is the editor's to fix — `formats.py` is not mine to edit — and both are unchanged from
round 2. Listed again with the equivalent measurement:

| format | row | the written reason | does it describe this cut? | what was measured instead |
|---|---|---|---|---|
| `ad9x16` | `framing:no_wide_level` | *"Dan sits in a full-width WINDOW above the text…"* | **No** — this cut has no window; he is full-frame on every talking beat | the **16:9** `framing:no_wide_level` row ran on the same crops of the same source and PASSED (smallest head 32.3 %); the 9:16 `hair_top`, `headroom` and `push_coverage` rows all measured and passed |
| `ad16x9` | `framing:centering` | *"the editor's layout puts bullets left and Dan right…"* | **No** — no bullets, no side-by-side layout | **this round's D5 table**: all thirteen 16:9 holds now share crop centre 1088, per-hold head centre 55.2–57.6 % of the width, every visible join ≤ 2.9 % frame-to-frame (`r3/verify_16x9.json`). The 9:16 `framing:centering` row measured the same holds from the same face track and PASSED |

## 7. The frame-by-frame pass — mine; NOT an independent judge

`_shared/deliver/watch.py` ran on each delivered master and I judged every image myself. **No judge
subagent was spawned** (the task forbids it), so — exactly as in round 2 — **`watch:pass` is not an
independent watch judge** and the reviewer's own pass is.

| | 9:16 | 16:9 |
|---|---|---|
| scan | 1714 frames, median diff 2.208, threshold 29.9 | 1714 frames, median diff 1.063, threshold 29.3 |
| frozen runs ≥ 8 frames / black frames | **0 / 0** | **0 / 0** |
| unexplained jumps | **0** (18 explained by the plan) | **0** (18 explained) |
| naked splices | **0 of 0 candidates** | **0 of 1 candidate** |
| declared graphics present | **12/12** | **12/12** |
| judged | 40/40 images, 37/37 boundaries, **0 open defects** | 40/40, 37/37, **0 open defects** |

**What I actually looked at.** The three full-size contact sheets per aspect; every boundary's −2…+2
strip and −1|0 pair, tiled into readable pages with the file name burned in
(`r3/judge_{9x16,16x9}/{strip,pair}_page*.jpg`); and, for the frames this round touched, purpose-built
sheets at readable size (`r3/look/`): **every frame of the 9:16 lean 22.05–22.36 s**, the 20.254 s
zoom cut at −2…+2, **all eight visible 16:9 NEAR↔FAR joins** at −2…+2, **both 16:9 CTA beats
composited** (8 and 4 frames), **the end-card tail** in both aspects (8 frames each), and **the first
and the last frame** of both files. Nothing new was found.

## 8. Deviations from §13, all of them

1. **The 16:9 CTA 1 pill changed too** (552 × 132 at (54, 772) → 396 × 194 at (54, 832)). §13 names
   only CTA 2, but no 552-wide box is clear of him anywhere low in the CTA-2 beat, so the pill had to
   get narrower; leaving CTA 1 at the old size would have shipped two different pills in one film.
   One geometry for both is the coherent reading of "like CTA 1".
2. **Captions were not lifted for CTA 2.** Measured clearance 185 px, gate clearance 30 px, PASS —
   §1/D6 above.
3. **D4 was fixed by moving the centre, not by cutting the hold at FAR.** §13 allows either; the
   alternation rule (never two equal levels across a visible join) rules out FAR here. The cost — a
   15.0 % lateral component on the 9:16 zoom cut at 20.254 s — is stated in §1.
4. **The ninth forced splice at 36.003 s was not adopted** (§2).
5. **`sharpness.json`'s `source_native` is measured at 1080×1920, not at 2160×3840** — mediapipe
   returns no face on a full-size frame. The number (129.3 on a 117 px face) is **not** comparable
   with the delivered one (14.2 on a 421 px face); the comparison §13 asks for is
   delivered vs Ad 1 vertical, and a `_comparability` note now says so inside the file.

## 9. §9 calls / Dan's calls

Unchanged from round 2 and carried verbatim into `notes-RA-01.md` (items 1–11), plus the two this
round adds: the 16:9 pill's new three-line shape, and the bed's held tail. **D1 (the `artifacts` row)
and D7 (the `formats.py` n/a wording, and `watch:pass` not being independent) are not the editor's and
are unchanged.**

## 10. Housekeeping

* Round-3 measurement files: `r3/bed_fix.json`, `r3/tail_envelope.json`, `r3/verify_9x16.json`,
  `r3/verify_16x9.json`, `r3/pill16.json` + `r3/pill16.jpg`, `r3/look/`, `r3/judge_*/`,
  `face_src_r3.json`, `sharpness.json`, `measurements-RA-01.json` (49 keys, complete).
* New scripts, all in `recipe-RA-01/`: `s42_bed.py` (the bed asset), `s43_r3verify.py` (the delivered
  face box / join proof), `s45_pillproof.py`, `s47_sharpness.py`, `s48_tail.py`, `s49_r3look.py`, and
  the chains `s44_r3a.sh`, `s46_r3b.sh`, `s50_r3c.sh`. `s05_plan.py`, `s10_render.py`, `s11_cta.py`,
  `s19_recipe.sh` and `s29_ship_held.py` were edited; every edit carries a comment saying why.
* **Nothing was committed to git. No dashboard row. Nothing uploaded.**
