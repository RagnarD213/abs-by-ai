# RA-01 — ROUND 2 — EDITOR

**Built to `Handoffs/video-editing/RA-01-plan.md` §12 "Round 2 rulings" by the editor session
(Claude Opus 5, high), 2026-09-17.** Work dir `/Volumes/Extreme/_edit_work/ra01/`.
Raw footage untouched. **$0.00 of AI generation. Nothing uploaded. No dashboard row. Nothing
committed. No third concurrent build — every render, gate and transcription ran through
`capwait.sh`.** No judge subagents were spawned; the frame-by-frame pass is mine.

**Round 1 is preserved.** `round1/master_9x16.mp4` (sha `3e5e32bb8a56…`), `round1/master_16x9.mp4`
(sha `57cde3cf8846…`), their four stamps and both round-1 gate plans are in
`/Volumes/Extreme/_edit_work/ra01/round1/`.

---

## 1. What R1–R8 asked for, and what was done

| ruling | what it asked | what the build does |
|---|---|---|
| **R1** first 12 s | captions from the first word over every beat; ≤ 0.15 s lead-in; a new L1–L4 beat map | captions on **every one of the 193 words** (192 states, 53 lines, 0 suppressed), over the photo cards and the phone recording; the first word lands at **0.140 s**; the new beat map is below |
| **R2** framing | the plan's two levels; face box inside 8–92 % of the width; fixed centre per hold | 9:16 **NEAR 594×1056**, **FAR 702×1248** (spread ×1.182); 16:9 **1888×1062 / 2144×1206** (×1.136); **13 holds**, centre = the hold's own median face centre, moved **0.0 px** in every one; on the DELIVERED frames the face box never leaves 21.2–87.0 % of the width (196 samples, 0 violations) |
| **R3** macro slice | a stable itemized list + total; no recalculation; end ≥ 3 frames before the screen change | slice **40.50 → 43.60 s** of the recording. It changes screen at **43.80 s**, so the slice ends **6 frames early**; the recalculation (458 → 342) and the "Log Meal" press are both before 40.5 s |
| **R4** 16:9 CTA pill | compact, sized to its text; low; never on his face, neck or shoulders | a **552×132** pill placed by person mask in the clear field beside him |
| **R5** skin colour | exposure 1.00–1.30 by face luma; saturation up from 0.88 to ≥ 85 % of Ad 1's face chroma, cap 1.25; no hue/WB change; proof sheet | **exposure 1.15, saturation 1.25**. Face luma 76.2 against the 73.3 target. Face chroma on the delivered frames **24.46 = 81.3 % of the Ad 1 vertical — the 85 % floor is NOT reached at the 1.25 cap** (see D6) |
| **R6** chips and field | 9:16 chips y ≥ 200, x ≤ 940, above the caption band; cards on the flat J2AD field; 16:9 chips fully inside the card | 9:16 chips at **y = 200**, right edge ≤ **896**; every card on the flat J2AD field; 16:9 chips inside a header the card reserves, asserted fully inside the panel |
| **R7** music bed | remove the ≈ 0.1 s dropout and step near 0:56 | **no pause cut is made after the last word**, so the join that stepped is gone. What remains there is the music's own rest (see D10) |
| **R8** gate paperwork | list each n/a row whose written reason does not describe this cut | §10 below |
## 2. The R1 beat map as built

| words | picture | from → to | length |
|---|---|---|---|
| "This picture got me abs." | the AI image card, AI-GENERATED chip, **from frame 0** | 0.000 → 2.069 | 2.07 s |
| "And it's not even real!" | **Dan on camera, NEAR** | 2.069 → 3.170 | 1.10 s |
| "I generated this picture with AI" | the AI image card again | 3.170 → 5.072 | 1.90 s |
| "back when I was 200 pounds." | the **BEFORE** picture, from the word "back" | 5.072 → 6.773 | **1.70 s** (floor 1.20) |
| the pause + "And this" | **Dan on camera, FAR** — the "other" between before and after | 6.773 → 7.674 | **0.90 s** (floor 0.80) |
| "is what I look like today." + the pause + "Seeing this" | the three real after pictures, one at a time | 7.674 → 9.576 | **0.634 s each** (floor 0.60) |
| "AI image of myself with abs changed me." | the AI image card, landing on "AI image" | 9.576 → 12.312 | 2.74 s |

**Deviation from the table in R1, measured.** The ruling draws the Dan beat over "And this is what
I" and starts the photographs on "look". That leaves the photographs
`t("AI") − t("look") = 1.38 s`, i.e. **0.46 s each**, which breaks the ruling's own 0.60 s floor;
even starting Dan on the word "and" leaves 2.60 s for a 0.80 + 1.80 requirement — exactly zero
margin. Both cuts were therefore taken two words earlier, into the **pauses** on either side of
"and this" (6.52–7.02 s and 7.40–7.82 s). Every floor in the ruling is met with margin, the
structure the ruling is about (before → a real beat of Dan → after, never two physique pictures at
once) is intact, and both cuts now land in silence instead of on a word.

**Lead-in.** Whisper puts the first word at 26.92 s of the roll; the envelope does not move until
27.185 s and the CTC alignment on the finished mix reads 27.30. The head edge is cut from the
**envelope onset**, and the delivered first word lands at **0.140 s** (round 1: 0.84 s).

**Captions.** 193 words, **192 states in 53 lines, none suppressed**, over the photo cards and the
phone recording. Every sentence starts with a capital; two sentence breaks Whisper had run together
were restored from the script ("…got me abs. And it's not even real." and "…was 200 pounds. And this
is what I look like today."). "abs" lowercase, "AI" uppercase, no "apps". The first 30 s read word
for word against the script. **0 blank frames between states.**
## 3. R2 — the framing levels, the centres, and the 8–92 % rule

**The levels.** The ruling's figures (NEAR ≈ 603×1072, FAR ≈ 707×1256) are not on the exact-9:16
even-pixel lattice, and a crop that is not an exact 9:16 rectangle in even pixels drifts on scale.
The nearest lattice points were taken, and the crop bottoms land where the locked standard puts them:

| | crop (source px) | y0 = hair_min − 4 % | bottom | anchor | upscale |
|---|---|---|---|---|---|
| 9:16 NEAR | **594 × 1056** (m=33) | hair − 42 | ≈ 2114 | just below the belly button (2093) | 1.818× |
| 9:16 FAR | **702 × 1248** (m=39) | hair − 50 | ≈ 2298 | waistband (2170) + 128 px of shorts | 1.538× |
| 16:9 NEAR | **1888 × 1062** (m=118) | hair − 42 | ≈ 2120 | — | 1.017× |
| 16:9 FAR | **2144 × 1206** (m=134) | hair − 48 | ≈ 2258 | — | 0.896× |

Spread ×**1.182** (9:16) and ×**1.136** (16:9), both over the `framing:push_coverage` floor of 1.10.

⚠ **The 16:9 heights cannot be the 9:16 heights.** R2 asks for "the same heights", but a 16:9 window
of a 2160-px-wide portrait source cannot be 1248 px tall — it would need 2219 px of width. FAR is
therefore the widest legal window, 2144×1206, and NEAR 1888×1062. Recorded as a deviation forced by
the source.

**The centres and the 8–92 % rule.** The tracker was extended to record the **face box**, not just
its centre, and the sample rate raised from 4 Hz to 5 Hz (round 1's worst lean — the ear at 98.2 %
of the frame width — fell between two 4 Hz samples). 276 of 276 samples valid, 0 discarded.
Feasibility at a level is arithmetic: a hold fits iff `max(fx1) − min(fx0) ≤ 0.84 × crop width`.

| hold | level | beat | hair_min | face-box span | band available (0.84 × cw) | centre | moved from the median |
|---|---|---|---|---|---|---|---|
| 0 | NEAR | 2.07 → 3.17 | 1102.0 | 269.9 | 499 | 1216.0 | **0.0 px** |
| 1 | FAR | 6.77 → 7.67 | 1108.0 | 295.3 | 590 | 1234.3 | **0.0 px** |
| 2 | NEAR | 12.31 → 16.35 | 1104.0 | 407.9 | 499 | 1220.4 | **0.0 px** |
| 3 | FAR | 16.35 → 20.25 | 1104.0 | 378.4 | 590 | 1212.3 | **0.0 px** |
| 4 | NEAR | 20.25 → 23.19 | 1104.0 | 376.8 | 499 | 1229.3 | **0.0 px** |
| 5 | FAR | 23.19 → 24.86 | 1108.0 | 307.5 | 590 | 1207.3 | **0.0 px** |
| 6 | NEAR | 31.93 → 36.64 | 1100.0 | 362.7 | 499 | 1227.3 | **0.0 px** |
| 7 | FAR | 39.74 → 40.87 | 1106.0 | 262.5 | 590 | 1219.3 | **0.0 px** |
| 8 | NEAR | 40.87 → 44.48 | 1104.0 | 276.9 | 499 | 1220.6 | **0.0 px** |
| 9 | FAR | 44.48 → 47.58 | 1098.0 | 398.7 | 590 | 1218.8 | **0.0 px** |
| 10 | NEAR | 47.58 → 51.25 | 1100.0 | 294.4 | 499 | 1229.9 | **0.0 px** |
| 11 | FAR | 51.25 → 53.92 | 1102.0 | 307.2 | 590 | 1242.6 | **0.0 px** |
| 12 | NEAR | 53.92 → 55.29 | 1100.0 | 283.9 | 499 | 1235.3 | **0.0 px** |

**All thirteen holds fit their intended level with room to spare**, so no hold had to be demoted and
the NEAR/FAR alternation the ruling asks for is unbroken across every visible join. The centre is the hold's own median face
centre in every case — the 8–92 % constraint never had to move it. R1 names hold 0 NEAR (the hook)
and hold 1 FAR (the "other" beat between the before and the after pictures); both are as named.

**Why thirteen and not eight.** The first plan carried round 1's hard-splice list forward by word pair and only three of the eight pairs still existed in this cut, so five visibly-jumping splices would have been left uncovered. `s25_hard.py` was re-run on the delivered picture, its eight measured times were stamped with this cut's own signature, and the segmentation was rebuilt from them: **the eight forced times are exactly the eight hold boundaries** 16.35, 20.25, 23.19, 40.87, 44.48, 47.58, 51.25 and 53.92. Holds 0 and 1 are the two the R1 beat map adds inside the first eight seconds.
## 4. R5 — the grade, and why the chroma floor is not reached

Every number below comes from ONE routine (`s32_grade.py → skin_stats`) run on both sides: the face
is located by mediapipe, the skin inside the face box is selected by the same R>G>B test the round-1
exposure probe used, and every statistic is a **median** so a highlight or a glasses frame cannot
move it. Chroma is CIELAB √(a\*²+b\*²).

**The two references**

| | face luma | L\* | a\* | b\* | chroma |
|---|---|---|---|---|---|
| approved website video (11 s / 30 / 60 / 95, the luma reference the plan names) | **73.35** | 32.3 | 16.2 | 14.3 | 21.87 |
| approved **Ad 1 vertical**, 11 talking-head instants (the chroma reference) | 76.39 | 34.1 | **17.3** | **23.8** | **30.11** |

R5's floor is 85 % of 30.11 = **25.59**.

**The sweep** (exposure first, by face luma; then saturation, at each exposure that is inside the
73 ± 5 band)

| exposure | face luma @ sat 0.88 | luma error | chroma @ sat 0.88 | chroma @ sat 1.25 | face luma @ sat 1.25 |
|---|---|---|---|---|---|
| 1.00 | 70.9 | 2.41 | 14.23 | 20.91 | 70.1 (err 3.29) |
| **1.15** | 76.9 | 3.59 | 15.01 | **21.96** | **76.2 (err 2.87)** |
| 1.30 *(round 1's)* | 82.6 | 9.27 | 15.76 | — | outside the band |

**Chosen: exposure 1.15, saturation 1.25.** Both 1.00 and 1.15 are inside the luma band at sat 0.88;
they were each taken all the way to their own chosen saturation and judged there, because
`eq=saturation` moves face luma a little as well — and at the saturation actually delivered, 1.15 is
both **closer on luma** (2.87 vs 3.29) and **higher on chroma** (21.96 vs 20.91). The exposure that
looked best at sat 0.88 is not the one that is best at the grade that ships.

**⚠ THE FLOOR IS NOT REACHED.** At the ruling's 1.25 cap the delivered face chroma is **21.96 —
72.9 % of Ad 1's 30.11, against the 85 % floor.** Extrapolating the sweep, ~1.55 would be needed,
well past the cap. The reason is in the a\*/b\* split, not in the amount of colour: ours reads
a\* 15.6 / b\* 14.3 (hue ≈ 43°) against Ad 1's 17.3 / 23.8 (hue ≈ 54°). Ad 1 is lit by warm indoor
light; this roll is overcast daylight, which is genuinely bluer. `eq=saturation` scales a\* and b\*
together, so it can add colour but cannot move the hue — and **R5 forbids a white-balance or hue
change.** Closing the gap needs Dan's ruling on the look, which is why it is item 5 of his calls.

**Not neon.** Whole-frame chroma at the chosen grade: p95 25.1, p99 31.5, against 16.9 / 21.0 at
round 1's e1.30/sat 0.88. The proof sheet `recipe-RA-01/grade_proof.jpg` shows four graded frames
beside four Ad 1 frames: the trees stay green, the pool stays pool-blue and the shorts stay
bottle-green. Cards and the phone recording are **not** regraded.
## 5. R4 — the 16:9 CTA pill

Round 1 drew a **1800-px-wide** solid band across the whole frame; at CTA 2 it lay across Dan's neck
and shoulders and hid the top of the physique (D5). The pill is now **552 × 132** — sized to
"Tap the button below" plus its padding — and placed by measuring him on that beat's own rendered
frame with the Apple Vision person mask, taking the **lowest** clear position that stays above the
burned-caption band.

| beat | pill | placement |
|---|---|---|
| CTA 1 (18.89 → 20.52) | `54, 772 → 606, 904` | the lowest position the caption band allows (y max = 930 − 26 − 132 = 772), in the clear field to his left, over the pool |
| CTA 2 (53.79 → 55.26) | `54, 274 → 606, 406` | his raised left hand occupies x ≤ 606 from y ≈ 280 to y ≈ 904 on that frame, so 274 is the lowest clear position; measured, not chosen |

⚠ **Why beside him and not on him.** A 16:9 window of this portrait roll is 1888–2144 source px
wide and Dan is only ≈ 35 % of it, so there are ~600 px of clear field on each side and **no clear
horizontal band anywhere on his body** — hair to waistband fills the frame height. "Low in the
frame, never touching his face, neck or shoulders" can only be satisfied beside him, and that is
where it goes. The 9:16 pill is unchanged from round 1 (the reviewer accepted it: 960 px, on the
chest, clear of the face) and is still placed per beat from his own chin and head height.

## 6. R7 — the bed step near 0:56

Round 1's D10 was a **step at a join**: after "below." the bed sat at −57 dBFS (the ducker
releasing) and jumped to −38.6 dBFS in 40 ms at the 56.056 s splice — a pause cut that removed
0.133 s of tail silence and cost the one join in the file that measured as a discontinuity.

`s03_edl.py` now refuses any pause cut whose in-point is at or after the last word. **The joins list
ends at 53.921 s; there is no join anywhere in the tail.**

What is still measurable there is the music: `Realizer.mp3` has a **rest of its own** at that point
in the track — measured on the source file, −28.6 dB against a −13.4 dB local median over 0.1 s at
55.95–56.05 s. It is not a splice, not a click, and it sits in a bed that is ≈ 46 dBFS down and
already fading out. I did **not** move the bed to hide it: scanning all 310 s of the track, the best
available start offset still leaves a 10.8 dB rest in the tail (this one is 15.2 dB), and changing
the track or its phase is a bigger mix change than R7 allows. Recorded rather than tuned away.

SFX stay out, as the ruling accepts (`sfx_probe.json`: adding them lowers the failing `artifacts`
flux slightly but breaks the passing `tone` row, 0.74/1.92 → 1.24/4.63 against 1.2/2.5).
## 7. The two masters

| file | where it is | spec | sha256 (first 12) |
|---|---|---|---|
| `master_9x16.mp4` | `/Volumes/Extreme/_edit_work/ra01/` — **HELD** | 1080×1920, 30000/1001, h264 yuv420p bt709, AAC 48 kHz 2 ch, **1714 frames, 57.190467 s** | `5bc6c5126a38` |
| `master_16x9.mp4` | same — **HELD** | 1920×1080, same rate, same codecs, same audio, **1714 frames, 57.190467 s** | `1f4367c3a6b5` |

**57.190 s against the 59.00 s ceiling — 1.81 s of margin.** No line was cut, no speed ramp, neither
CTA line touched. Both masters carry the same mix (the 16:9 is muxed from the same `mix.wav`).

## 8. The audio gate (`_shared/audio/audio_gate.py`), both masters, identical

| row | result | number |
|---|---|---|
| `lr_corr` | PASS | one voice, L/R correlation +0.9998 (≥ +0.97) |
| `comb` | PASS | ripple 0.60 dB vs his 0.54 (≤ his + 0.35) |
| `edt` | PASS | early decay 29 ms (≤ 80; his 40) |
| `tone` | PASS | mean 0.80 dB (≤ 1.2), max 2.00 (≤ 2.5) |
| `floor` | PASS | voice over floor 30.2 / 37.1 / 29.6 vs his 27.6 / 34.7 / 28.0 |
| **`artifacts`** | **FAIL** | **flux 0.091 against the bound 0.079** (his 0.072 × 1.1); swirl 0.792 vs his 0.835 passes |
| `do_no_harm` | PASS | flux ×0.94 and swirl ×0.83 against this file's own untreated source (≤ ×1.35) |
| `dryness` | PASS | 9.1 dB drop 64 ms after a word vs his 7.4 |
| `lufs` | PASS | −14.20 LUFS (−14.0 ± 1.0) |
| `spread` | PASS | speech spread 6.9 dB vs his 8.2; LRA 3.3 LU (his 3.5) |
| `tp` | PASS | −2.10 dBTP (≤ −1.0) |
| `silence` | PASS | 0 digitally silent seconds, 0 below −50 dBFS |
| `length` | PASS | **audio 57.190 s vs picture 57.190 s** (round 2 fixed this; see §12.2) |

**12 of 13 rows pass. `artifacts` is the one failure, and it is D1 — Dan's ruling.** The untreated
lav reads flux **0.0962** before anything touches it, i.e. 1.22× the bound; the chain takes it to
0.091 (×0.94). Nothing in the mix can be removed to get under: the bed *lowers* flux, there are no
SFX, and processing further is what `audio-never-over-strip` and the `do_no_harm` row exist to stop.

## 9. The delivery gate (`_shared/deliver/gate.py`, `GATE_VERSION 2.1.0`), on the delivered files

**9:16 (`--format ad9x16`): 35 passed, 1 failed, 0 NOT MEASURED, 0 NEEDS HUMAN REVIEW, 0 pending, 3 declared n/a.**
**16:9 (`--format ad16x9`): 35 passed, 1 failed, 0 NOT MEASURED, 0 NEEDS HUMAN REVIEW, 0 pending, 3 declared n/a.**

The one failure on each is the same row, and it is the audio row above:

| row | 9:16 | 16:9 |
|---|---|---|
| **`audio:stamp`** | **FAIL** — "no valid audio-gate stamp … artifacts — fix the audio, do not deliver" | **FAIL**, same |

Every other row, both files:

| row | 9:16 | 16:9 |
|---|---|---|
| `container:size` / `:fps` / `:codec` | PASS | PASS |
| `container:duration` | PASS 57.190 s vs target 57.190 s | PASS |
| `container:frames` | PASS 1714 present, 1714 planned | PASS |
| `audio:stream_integrity` | PASS gap +0.000 s, 0 silent seconds, quietest −45.6 dBFS | PASS |
| `audio:lipsync` | PASS worst +0.042 ms (max 1.0) | PASS |
| `audio:click_at_joins` | PASS 0 of 20 joins | PASS 0 of 20 |
| `style:coverage` | PASS **53 %** off the main scene (min 38) | PASS **39 %** (min 35) |
| `style:static_run` | PASS 11.7 s at 0:39.67 (max 31.6) | PASS 7.2 s (max 25.0) |
| `style:change_rate` | PASS 16.8/min (min 7) | PASS 21.0/min (min 8) |
| `framing:hair_top` | PASS min **44 px**, median 57 (min 20) | PASS min 41, median 58 |
| `framing:headroom` | PASS 3 tracked holds, min hair top 50–56 px (band 20–70) | PASS 8 holds, 52–59 px |
| `framing:centering` | PASS worst **−1.2 %** at 23.5 s (max ±6) | **n/a — declared by the format**, see §10 |
| `framing:no_wide_level` | n/a — declared by the format, see §10 | PASS smallest head **32.4 %** (min 27) |
| `framing:push_coverage` | PASS head 30.1–35.3 % of window per hold | PASS 32.4–36.6 % |
| `cut:uncovered_joins` | PASS 0.0/min | PASS 0.0/min |
| `cut:black_frames` | PASS 0 frames under luma 6.0, every frame scanned | PASS |
| `cut:min_segment` | PASS 0 under 0.2 s | PASS |
| `cut:jump_cut` | PASS 0 pairs | PASS |
| `cut:splice_visibility` | PASS 0 of 20 | PASS 0 of 20 |
| `cut:naked_splices` | PASS 0 naked of 0 candidates | PASS 0 of 1 |
| `captions:graphic_clearance` | PASS **192 PNG states verified in the delivered pixels**, 88 state/graphic pairs, tightest **49 px** (min 20) | PASS 71 pairs, tightest **30 px** |
| `captions:card_collision` | PASS 53 cues, **1 card**, 0 on a card | PASS |
| `captions:burned` | PASS **97 %** of sampled frames (min 45) | PASS 97 % |
| `captions:within_runtime` | PASS 53 cues, last ends 55.22 s | PASS |
| `captions:sync` | PASS **192/192 states, 100 %** of 193 delivered-audio words, median +1 ms | PASS |
| `compliance:banned_screen` | PASS 1714 frames × 28 templates, 0 hits | PASS |
| `compliance:labels` | PASS 5 AI + 3 real, correlation min **0.998**, 0 missing, 0 wrong | PASS |
| `compliance:drug_names` | PASS 0 | PASS |
| `compliance:negative_events` | PASS 40 frames, 1 finding, cleared | PASS |
| `compliance:script_fidelity` | PASS 99.5 % (196 of 196) | PASS |
| `watch:pass` | PASS **37/37 boundaries, 40/40 images**, judged by this editor session | PASS 37/37, 40/40 |
| `srt:present` / `srt:shape` | n/a — a vertical ad burns its captions | n/a |

**There is no NOT MEASURED row and no skipped check on either file.**
## 10. R8 — `not_applicable` rows whose written reason does not describe this cut

`formats.py` is off limits to an editor and rightly so, so these are reported, not worked around.
Each one is listed with the equivalent measurement that WAS made, so nothing is hidden behind an n/a.

| format | row | the reason `formats.py` gives | does it describe this cut? | the equivalent measurement |
|---|---|---|---|---|
| `ad9x16` | `framing:no_wide_level` | *"Dan sits in a full-width WINDOW above the text (Step 5 rule 1 of /shortad-from-longform), so his head is ~22 % of the frame by layout, not by a wide crop: the approved Ad 1 vertical reads 427–436 px of 1920 on its window beats"* | **No.** This cut has no window: Dan is full-frame on every talking-head beat. | the **16:9** `framing:no_wide_level` row ran on the same crops of the same source and PASSED; `framing:hair_top`, `:headroom` and `:push_coverage` all measured and passed on the 9:16 |
| `ad16x9` | `framing:centering` | *"the editor's layout puts bullets left and Dan right (Muhammad Ad 2 holds read +482..+495 px); centring is the layout's call"* | **No.** This cut has no bullets and no side-by-side layout; Dan is centred, and plan §5 names this row as one to satisfy. | the **9:16** `framing:centering` row measured the same eight holds from the same face track and PASSED; `r2/verify_16x9.json` records the delivered face-centre range for the wide file as well |
| both | `srt:present` / `srt:shape` | *"a vertical / 16:9 ad burns its captions; there is no sidecar deliverable"* | **Yes.** Both files burn their captions; the `.srt` in `cap_<k>/` is build evidence, not a deliverable. | — |

Nothing else is declared n/a on either format.
## 11. The reviewer's eleven defects, one by one

### D1 — the audio `artifacts` row (blocker) — **NOT FIXED, BY RULING; the masters are HELD**

Plan §12: *"D1 … is **Dan's ruling, not an editor fix** — do not process harder, do not touch the
gate; masters stay HELD."* The row is left failing, both masters stay in the work dir, and item 8 of
`notes-RA-01.md` puts the decision in front of Dan with the A/B clip.

Measured on this round's mix: delivered flux **0.091** against the bound **0.079**; the **untreated**
lav reads **0.0962**, so the source is 1.22× over the bound before anything touches it and the chain
takes it *down* (×0.94, which is what `do_no_harm` reports and passes). `formats.py`, every check,
every threshold and every corpus file are untouched. I do not think the row is wrong: it is telling
us this outdoor roll's lav is noisier frame to frame than the indoor reference, and the fix is at the
microphone on the next shoot.

### D2 — no captions in the hook; captions off under every card (major) — **FIXED**

`s07_captions.py` suppresses nothing. **193 words, 192 caption states in 53 lines, none suppressed**,
over the photo cards and over the phone recording. The gate verified all **192 states in the
delivered pixels** and aligned **192/192 (100 %)** to the delivered-audio words, median +1 ms.
Round 1 had no caption at all before 00:12.24; this cut carries one from **0.140 s** to 55.22 s.
`captions:burned` reads **97 %** of sampled frames (round 1: 64 %).

### D3 — both framing levels a notch too tight (major) — **FIXED, and proven on the delivered frames**

The levels are re-cut to R2 (§3). The consequence the reviewer measured — *"face box reaches 96.4 %
of frame width … 98.2 % (ear on the right edge)"* — is gone: `s33_verify.py` measures the face box on
**196 delivered frames at 6 Hz** and the worst readings are **21.2 % / 87.0 %** of the frame width,
**0 violations of the 8–92 % rule**. (16:9: 41.3 % / 66.5 %, 0 violations.) The gate's own
`framing:centering` reads worst **−1.2 %** against a ±6 % bound.

⚠ **The sharpness finding is unchanged and is now larger, by arithmetic.** Face Laplacian variance
normalised to a 256 px face: ours **30.4** against the approved Ad 1 vertical's **108.5** = **0.28×**
(16:9: 35.8 = 0.33×). Round 1 measured 0.34× at a *tighter* crop. A wider crop puts fewer delivered
pixels on his face, so normalising to 256 px upsamples more — the source has not changed and the
upscale is *lower* than round 1's (1.82× vs 2.14×). Plan §5 says this is a footage-report finding,
not a reason to add a level, so it is recorded and nothing was done to the crop.

### D4 — the macro slice ran into the recalculation (major) — **FIXED**

The recording was scanned for change at 10 Hz: it is stable **only between 40.5 s and 43.8 s**, and
43.8 s is where it changes screen. The slice is **40.50 → 43.60** — six frames clear of the change,
and after the 458 → 342 recalculation and the "Log Meal" press, both of which are before 40.5 s. I
verified the **last ten frames of the beat one by one** (`r2/strips_9x16/macro_tail_10.jpg`): the
itemized list, the 363 cal total and the "logged" confirmation are identical on every one.

### D5 — the 16:9 CTA pill was a full-width band across his neck (major) — **FIXED**

A **552 × 132** pill sized to its own text, placed by person mask in the clear field beside him
(§5). Round 1's was ~1800 px wide and lay across his neck and shoulders.

### D6 — skin colour (major) — **FIXED AS FAR AS THE RULING ALLOWS; the floor is not reached**

Exposure **1.15**, saturation **1.25** (§4). On the **delivered frames**, face chroma is **24.46**
against the Ad 1 vertical's **30.08 = 81.3 %**, against R5's 85 % floor (16:9: 24.41 = 81.1 %).
The reviewer measured round 1 at ≈ 57 % on their own equivalent comparison. **The floor is missed by 3.7 points at the ruling's
1.25 saturation cap**, and the reason is hue, not amount: our daylight reads a\* ≈ b\*, Ad 1's warm
indoor light reads b\* half again as large as a\*, and R5 forbids a white-balance change. Item 5 of
Dan's calls.

### D7 — the 13-frame flash of Dan between BEFORE and AFTER (minor) — **FIXED**

R1's beat map gives the "other" beat its own words and **0.90 s** (round 1: 0.43 s), and the BEFORE
picture now holds **1.70 s** (round 1: 0.83 s). Both cuts land in pauses.

### D8 — chips in the platform UI band; cards on a blurred copy of the photo (minor) — **FIXED**

9:16 chips sit at **y = 200** with their right edge at **668 / 896** (bound 940); round 1 had them at
y 60–122, inside the band the platform UI occupies. Every card is on the **flat J2AD field**. 16:9
chips sit inside a header the card reserves (§12.1), asserted fully inside the panel — and that
assertion caught the same defect recurring at 96 px of header (§12.1).

### D9 — sentence-initial lowercase in the captions (minor) — **FIXED**

Casing comes from the previous word's punctuation, and the two sentence breaks Whisper ran together
are restored from the script. Proofed word for word over the first 30 s.

### D10 — the bed step at the 56.056 join (minor) — **FIXED (the join is gone)**

No pause cut is made after the last word, so there is no join in the tail at all — the joins list
ends at 53.921 s. What remains at that instant is the music's own rest, measured in the source track
(§6). `audio:click_at_joins` reads **0 of 20 joins**.

### D11 — `not_applicable` reasons that do not describe this cut (minor) — **DOCUMENTED (R8)**

§10. Both are reported with the equivalent measurement that was made; `formats.py` is untouched.
## 12. Six defects this round found in its OWN work, before anything was gated

None of these was in the reviewer's list; each was found by measuring or looking at what round 2
had just built. They are recorded because the same class will recur.

1. **The 16:9 label chip stuck 21 px out of the top of its card.** R6 asks for the chip *fully
   inside* the card, so the card was given a reserved header — at 96 px. The two-line
   "Real picture of me — not AI-generated" chip is **114 px tall**, so it overflowed the panel: D8's
   own defect in a new place. The header is now **140 px** and two assertions refuse to build a card
   whose chip is not inside both the header and the panel.
2. **The mix came out 0.235 s short of the picture.** The end hold was raised from 1.40 s to 1.65 s
   in the plan, and `s08_audio.py` kept its own copy of the old number — the audio gate's `length`
   row failed (audio 56.955 s vs picture 57.190 s). `END_HOLD` now lives once, in `ra01lib.py`, and
   the mix is additionally **locked to the picture** with `voice_chain.py`'s own `--frame-lock`, so a
   frame-snapped end hold can never leave the audio short again.
3. **A two-frame blank at every one of the 52 caption line changes.** The state schedule ended each
   line 0.06 s before the next began — 3.0 s of blank spread over the film, reading as a flicker on
   every line. With round 1's captions switched off under the cards this was mostly invisible; with
   R1's continuous captions it is not. The last word of a line now holds until the next line starts.
   Measured after the fix: **0 gaps between 192 states.**
4. **The 9:16 card metadata was stale.** The first 9:16 card build aborted on the macro assertion
   *before* writing `meta.json`, so the file on disk was still round 1's — wrong rectangles for
   every card and no entry at all for the new `ai_gen` card. That is exactly the
   "geometry bound to another render" fault the v2 evidence contract exists to forbid, and it would
   have gone into the gate plan. The cards were rebuilt; their mp4s came out **bit-identical**
   (`r2/cards9_sha_before.txt` vs `r2/cards9_sha_after.txt`), so only the metadata changed and no
   re-render was needed.

5. **The macro card's FIRST FRAME was an empty field, on both aspects.** The card is built by
   overlaying the seeked recording onto a colour source; without `setpts=PTS-STARTPTS` the
   recording's first frame arrived after the colour source's, so frame 0 of the card was bare field
   — one near-black frame at the cut into the card (luma **14.9 / 16.0** against **124.8 / 88.1** for
   every other frame). The delivery gate's black-frame bound is luma 6.0, so nothing measured it; it
   was found by looking at the contact sheet. Fixed, and the builder now asserts that the card's
   first and last frames actually contain the recording.
6. **The cut OUT of the macro beat landed on a look-away.** Round 1 gave the card a 0.60 s tail
   because the cut back to camera landed on an eye-squeeze; R3's stable-slice cap took that tail
   away and the cut landed on the same moment again. Measured with `s40_blink.py` over frames
   1168–1200: his eyes never close (eye-aspect-ratio **0.23–0.29**, median 0.270 — it is not a blink)
   but his **head is down** and his gaze with it until about f1187. The card now holds to **39.74 s**
   and the shot starts with him looking at camera. This is the checklist's `visual_junk` item, and it
   is the reason the plan's own 0.60 s tail existed.
## 13. The frame-by-frame pass — mine, no judge subagent

Run with the shared `_shared/deliver/watch.py` on each delivered master, then judged by me from the
images. **No judge subagent was spawned.**

| | 9:16 | 16:9 |
|---|---|---|
| scan | 1714 frames, median diff 2.212, threshold 28.788 | 1714 frames, median diff 1.058, threshold 39.067 |
| frozen runs ≥ 8 frames | **0** | **0** |
| black frames | **0** | **0** |
| unexplained jumps | **0** (18 explained by the plan) | **0** (18 explained) |
| naked splices | **0 of 0 candidates** | **0 of 1 candidate** |
| declared graphics present | **12/12** | **12/12** |
| boundaries | 37 declared, 0 detected → 37 strips, 37 pairs, 3 sheets | 37 → 37 strips, 37 pairs, 3 sheets |
| judged | **40/40 images, 37/37 boundaries, 0 open defects** | **40/40, 37/37, 0 open defects** |

**What I actually looked at, and how.** Each boundary's five consecutive frames (−2…+2) and its
−1|0 pair, tiled into readable pages with the file name burned into each tile
(`r2/judge_<key>/{pair,strip}_page*.jpg`), plus the three contact sheets at full size, plus the
extra strips the brief names by hand (`r2/strips_<key>/`): **the last ten frames of the macro beat**,
the **first ten frames** of the film, and the **first and last frame**. Two defects came out of it,
both fixed and both re-verified on the final render (§12.5 and §12.6).

**One splice is uncovered and I am reporting it rather than covering it.** `s25_hard.py` re-measured
the delivered picture after the macro beat moved and now flags the join at **36.003 s** — it used to
sit under the macro card's in-point and no longer does. Its frame difference is **7.93** against the
file's own p99 control of **5.13**: in range with the other uncovered splices before they were
covered (6.6–16.1), and far under the 24–27 the covered ones read once a level change sits on them.
Looked at frame by frame (`strip_025`), it is continuous speech: his mouth moves, his hands and the
background do not. The gate agrees — `cut:splice_visibility` 0 of 20, `cut:naked_splices` 0 of 0
candidates, `cut:uncovered_joins` 0.0/min. Covering it would mean a fourteenth level change inside a
4.7 s hold, which is the pacing ad-edit lesson 64 warns about. **Left as it is, on the record.**
## 14. Deviations from the plan, all of them

1. **§12 R1's word split for the before → other → after run.** Taken two words earlier so the
   ruling's own three floors (BEFORE ≥ 1.2 s, the Dan beat ≥ 0.8 s, each photograph ≥ 0.6 s) can all
   be met; the arithmetic that forces it is in §2. Both cuts now land in pauses.
2. **§12 R2's crop figures.** Rounded to the exact even-pixel 9:16 / 16:9 lattice (594×1056 and
   702×1248 instead of 603×1072 and 707×1256); the bottoms land where the standard puts them. The
   16:9 heights cannot equal the 9:16 heights — a 1248-px-tall 16:9 window needs 2219 px of width
   and the source is 2160 wide — so FAR is the widest legal window, 2144×1206.
3. **§4's "phone recording full-frame in 9:16".** R1 requires the caption band to be clear on every
   beat, so the macro card is laid out inside `A.CARD_RECT` like the others. The crop is tighter than
   round 1's whole-phone window because at card size the whole phone would put the itemized list at
   0.47× and it would not read; the window is the result card itself.
4. **§4's stats-scan layout in 9:16.** The picture is 58 % of the card width rather than 82 %,
   because the three rows and the plan band now have to fit inside the card rectangle above the
   caption band.
5. **§12 R6 and the 16:9 chips.** "Fully inside the card" cannot be done by searching the card for a
   clear band — a portrait photograph fitted to a 16:9 height is filled by Dan head to toe, and the
   mask search returned NO CLEAR BAND on every card. The card is given a reserved header instead.
6. **§6's transition SFX.** Still none; R7 accepts the round-1 measurement.
7. **The bed's musical rest near 0:56 is left alone.** R7 asks for it to go; the join that caused the
   step is gone, but the rest belongs to the track and no start offset of `Realizer.mp3` removes it.
8. **The take reel.** The plan itself says to skip it when only one pass exists, and only one does.

## 15. Housekeeping

* `.claude/skills/ad-edit/reference/demo-clip-log.md` — RA-01's asset uses updated to round 2, with
  the macro recording's stable window (**40.5–43.8 s**, screen change at 43.80) written down so the
  next build cannot repeat D4.
* `recipe-RA-01/REBUILD.md` — rewritten for round 2: the grade stage, the pinned head edge, the
  face-box track, the hard-splice re-measure and the delivered-frame verification are all in it.
* **Nothing committed to git.** `formats.py`, every check, every threshold and every corpus file are
  untouched. Nothing uploaded. No dashboard row. $0.00 of AI generation. Raw footage untouched.
* Round 1's masters, stamps and gate plans are preserved in `round1/`.
