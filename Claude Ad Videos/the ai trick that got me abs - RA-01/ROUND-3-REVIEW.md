# RA-01 "The AI Trick That Got Me Abs" — ROUND 3 REVIEW (final round)

Reviewer: independent (Fable 5.1), 2026-09-18. Read only: `AGENTS.md`, `00-RULES.md`, `RA-01-plan.md` (§12 + §13 rulings),
`ROUND-2-REVIEW.md` (+ `review-r2/` evidence), the two round-3 masters and their four stamps, `recipe-RA-01/gate_plan_*.json`,
the round-2 masters + stamps in `round2/` (before/after only), and the approved Ad 1 vertical. Did NOT read any
`ROUND-n-EDITOR.md`, `notes-*.md`, `r3_*.json`, `verify_*.json`, `grade.json`, the `watchpass_*` folders or the delivery folder.
All evidence is in `/Volumes/Extreme/_edit_work/ra01/review-r3/` (paths below are relative to it). Machine cap checked before
every decode (one other build running: the kit9x16 gate). Masters were not modified; nothing was rendered.

Files reviewed:
- `master_9x16.mp4` sha256 `02d03218…03e51`, 80,473,688 B — 1080×1920, 30000/1001, h264 High yuv420p bt709/tv, AAC-LC 48 kHz 2 ch, **57.190 s**, 1714 frames
- `master_16x9.mp4` sha256 `bcace8c4…4fa45`, 65,570,603 B — 1920×1080, same, 57.190 s, 1714 frames

## Round-2 defect status (D1–D7)

| id | round-2 defect | status in round 3 | evidence |
|---|---|---|---|
| D1 | audio `artifacts` FAIL → all four stamps FAIL | **NOT FIXED — Dan's ruling, not an editor fix** (flux 0.090 vs limit 0.079, his 0.072; untreated 0.097, chain ×0.93) | stamps (rows dumped in this file's transcript) |
| D2 | printed "200 pounds" in the caption | **CLOSED by §13 ruling** — caption still prints "when I was 200 pounds." (f162–f209); allowed | `sheets/caps_1.jpg` |
| D3 | music-bed dropout + 15 dB step at 56.06 s | **FIXED** — the trough is filled: 50 ms envelope now a monotonic fade −42 → −69 dBFS from the last word to the last frame, largest 50 ms step +2.6 dB (was +15.2); voice and bed unchanged elsewhere (0.00 dB level delta, diff signal 37 dB below the bed in pauses). Residual: a 15 ms musical transient at 56.055–56.070 s (−53 → −40.7 → −36.9 → −41 dBFS at 5 ms, 143 Hz dominant, no sample-level click) — the bed's own beat, 23 dB under the voice | `tail_r3_9x16.txt`, `tail_r2_9x16.txt`, `tail_samples.txt`, `bed_pauses.txt`, `audio_diff_r3_vs_r2.txt` |
| D4 | 9:16 face box past 92 % at 00:22.15–00:22.26 | **FIXED** — hold 20.254–23.190 s re-centred (median head 45.1 %, was 48.0 %); face box 15.1–90.7 % of the width, 0 of 88 frames outside 8–92 % (was 11, max 94.3 %); every other talking frame of both files inside 8–92 % (9:16 worst 91.0 %, 16:9 46–71 %). Side effect: the zoom cut at 20.254 s now slides his head 60.0 % → 44.9 % (−15.0 % of width; round 2 −12.4 %) — see N1 | `face_analysis.txt`, `sheets/lean_r2_vs_r3.jpg` |
| D5 | 16:9 lateral hop at every NEAR↔FAR join (4–9 %) | **FIXED to within measurement** — per-hold head-centre medians differ by ≤ 1.74 % at all 8 joins (−1.27, +1.15, −1.74, +1.23, −1.11, +1.51, +0.20, −0.10; bound 1.5 %: 7/8 inside, 23.19 s at 1.74 %); frame-to-frame worst −2.91 % (20.254 s), then −2.33, −1.78, −1.33, +1.25, +0.78, +0.35, +0.15 (round 2: 3.9–9.1 %). Dan now sits at 55–58 % of the width at both levels; visually no hop | `face_analysis.txt`, `sheets/joins16_r2_vs_r3_a.jpg`, `_b.jpg` |
| D6 | 16:9 CTA 2 pill mid-frame | **FIXED** — both CTAs use one compact two-line pill at x 58–447, y 836–1023 (389×187, bottom at 95 % of the height); 0 person pixels inside it; nearest person pixel 53 px (CTA 2 f1640) / 201 px (CTA 1); captions stay in their band beside it, left edge ≥ 191 px right of the pill on every pill frame (f569–612, f1616–1660), never overlapping. Captions sit beside, not above (the letter of R4) — no collision, not a defect | `pills16_measure.txt`, `caption_vs_pill16.txt`, `sheets/pills16.jpg` |
| D7 | gate paperwork (n/a wording; watch judge not independent) | **NOT FIXED (not editor-fixable)** — same two n/a rows with the same wording; `watch:pass` judged by "round-3 editor session … NO judge subagent"; this review is the independent pass | stamps |

```
VERDICT: DOES NOT SHIP

BLOCKER — Dan's ruling, separate from the editor's work:
  D1  both files, whole file — audio stamps
      Plan §1/§6/§7: PASS audio_gate + deliver_gate stamps on each delivered file.
      →  audio_gate v1 (both): row `artifacts` FAIL — "flux 0.090 (his 0.072) … <= his x1.1"; verdict FAIL.
         deliver_gate 2.1.0 (both): verdict FAIL on `audio:stamp` only; all 35 other rows PASS or n/a. sha256 of all four
         stamps match the delivered files; GATE_VERSION 2.1.0 = current gate.py; audio STAMP_VERSION 1 = current.
         The stamp's do_no_harm row shows the untreated lav at 0.097 (chain ×0.93): the outdoor source is over the bound.
         Per §12/§13 this is Dan's call — not processed harder, gate untouched.                        severity: blocker

EDITOR-CONTROLLED WORK: SHIP-clean. No major or blocker defect remains in anything the editor controls.
Residual observations (minor / cosmetic), for the record or a later revision:

  N1  master_9x16.mp4 00:20.22–00:20.25 (f606→f607) — zoom cut reads as zoom + sideways slide
      §13 D4 offered "cut that hold at FAR, or widen its fixed centre"; the editor widened the centre.
      →  Across the join his head moves 60.0 % → 44.9 % of the width (−15.0 %; round 2 −12.4 %) while the scale steps
         FAR→NEAR (face height 21.7 % → 25.8 %). ≈ 9 % of that is his own lean at the tail of the FAR hold (FAR hold
         median 50.7 %, f606 at 60.0 %), ≈ 5.5 % is the new hold's centre (45.1 %, 4.9 % left of frame centre — inside
         the 6 % gate; gate row reports worst +4.2 % at 21.0 s). The other seven 9:16 joins: |f2f| ≤ 4.5 %, |hold
         medians| ≤ 4.0 %. Judgement: still a zoom cut (levels alternate, scale ×1.19), not a naked jump, but the slide
         is a touch larger than round 2. Cutting the hold at FAR (the §13 alternative) or moving the join a few frames
         off his lean would remove it.                                                                  severity: minor

  N2  both files 00:56.055–00:56.070 — residual bed transient (D3 tail)
      →  5 ms RMS −47.8 → −53.0 → −40.7 → −36.9 → −41.1 → −44.7 dBFS: a 15 ms bump ≈ 8 dB above the surrounding bed
         (−44…−46), 143 Hz dominant, max sample step −31.7 dBFS (the bed-only stretch 55.3–55.9 s reaches −29.2, so no
         click). It is the bed's own beat now exposed by the filled trough; 23 dB under the voice, under a silent end
         card. Measured, not heard.                                                                     severity: minor

  N3  master_16x9.mp4 — D5 residual vs the 1.5 % bound
      →  Per-hold medians: 23.19 s join at 1.74 %, 47.58 s at 1.51 % (6 of 8 ≤ 1.3 %). Frame-to-frame: 20.254 s −2.91 %,
         23.19 s −2.33 %, 51.25 s −1.78 %. The residual is his own motion between the source frames either side of an
         airtight join, magnified ×1.17 by the NEAR crop; the crops themselves are fixed (frames 490–566 and 695–697
         differ from round 2 only by uniform encoder noise, mean |Δ| 1.6/255, no block above 2.1). Visually clean at
         every join (sheets/joins16_r2_vs_r3_*.jpg).                                                    severity: minor

  D7  stamps — gate paperwork (unchanged, not editor-fixable)
      →  9:16 `framing:no_wide_level` n/a "Dan sits in a full-width WINDOW above the text": not this cut (he is full-
         frame; head 18–26 % of the frame, so not wide — harmless). 16:9 `framing:centering` n/a "bullets left and Dan
         right": not this cut — the measurement the gate did not take is in D5/N3 above. `srt:*` n/a fits. `watch:pass`
         (both): "37/37 boundaries … judged by RA-01 round-3 editor session … NO judge subagent" — not independent; this
         review is the independent watch judge for round 3.                                             severity: minor

CHECKED AND CLEAN:
  §13 (a) music bed: measured on BOTH files from the last spoken word (55.22 s) to the last frame at 5 ms and 50 ms
     (identical results — the AAC streams are byte-identical, md5 ecfc550e…): 50 ms series −42.2 dBFS at 55.20 s falling
     smoothly to −69.4 at 57.10, largest 50 ms step +2.6 dB (56.05 s) and −5.7 dB at the very end of the fade (57.05 s,
     −65 dBFS); round 2 at the same points: −57…−59 dBFS trough then +15.2 dB at 56.05. 5 ms series: 0 steps > 6 dB
     except the N2 transient (10 5-ms steps > 6 dB, all inside 56.01–56.07 s and at the −60 dBFS fade tail). "No other
     mix change": bed level in 149 pause windows median −42.4 dBFS in both rounds (per-window delta median 0.00 dB,
     p5/p95 −0.03/+0.04); speech windows delta 0.000 dB; difference signal in speech −42.7 dB relative (AAC
     requantisation in the 300–3 kHz voice band). Loudness re-measured: −14.2 LUFS, LRA 3.3 LU, true peak −2.1 dBTP.
  §13 (b) 9:16 lean: see D4. Hair never clipped (gate hair_top min 44 px; every tile on sheets/cuts9_*.jpg shows headroom).
  §13 (c) 16:9 hop: see D5/N3 — measured on every NEAR↔FAR join (16.35, 20.254, 23.19, 40.874, 44.478, 47.581, 51.251,
     53.921 s), last 10 / first 10 frames and per-hold medians, mediapipe face box at 960 px wide.
  §13 (d) 16:9 pills: see D6. CTA 1 f569–f612 (18.99–20.42 s, fades in/out over 3 frames), CTA 2 f1616–f1653
     (53.92–55.16 s); "tap" is spoken at 19.00 s and 54.70 s.
  Regression vs round 2: same 57.190 s and 1714 frames on both; audio identical on both aspects (AAC md5 equal; PCM
     md5 5750a4e8… equal); 9:16 picture pixel-identical to round 2 except frames 607–694 (the D4 hold; frames 575–606
     differ only by encoder lookahead noise, mean |Δ| 1.2, no localized block); 16:9 differs only in the NEAR holds
     (62–94, 369–489, 567–694, 957–1097, 1225–1332, 1426–1535, 1613–1656) and the pill regions, as §13 D5/D6 require.
  §1 container: both ≤ 59.00 s; sizes, fps, codecs, bt709 tv tags, AAC 48 kHz stereo as specified; first frame = AI card
     with chip (caption "This" visible from f5 = 0.167 s, speech audible from the first frames); last frame = held end
     card (AI image + AI-GENERATED chip on the shins + "Tap the button below" + AbsByAI.com), 1.90 s hold.
  §2 script: my own Whisper small.en pass on the delivered audio = 194 words, L1–L14 present and in order, L5 t2, L11
     kept, nothing cut, both CTA lines intact, no drug names, no user counts; Whisper's one mishearing ("loot") is
     captioned correctly as "lose".
  §7 captions, first 31 s proofed word for word against the audio (110 word tiles, sheets/caps_1..4.jpg): every word
     correct, "abs" lowercase, "AI" uppercase, "six-pack", sentence starts capitalised ("It inspired", "And", "Once",
     "Seeing", "To"), no "apps"/"RIP"/"loot", current-word highlight on the spoken word; the four largest Whisper deltas
     checked on the audio envelope: "got" onset 1.10 s vs caption 1.101; "back" 5.16 vs 5.172; "to" 30.48 vs 30.497;
     "real." cue at 3.070 inside the 2.95–3.18 s pause (0.12 s before the /r/). Captions never on a chip, the pill or a
     face; on cards they sit below the card on the J2 field.
  §4 / §12 R1 beat map at every boundary (sheets/cuts9_1..3.jpg, cuts16_1..4.jpg): AI card 0–2.069 → Dan NEAR
     2.069–3.170 → AI card 3.170–5.072 → BEFORE 5.072–6.773 (1.70 s, no chip per plan; §9 call stands) → Dan FAR
     6.773–7.674 (0.90 s) → three real afters 0.634 s each (studio-blue-10 / gray-41 / white-90, real-picture chip on
     each) → AI card 9.576–12.312 → talk → CTA 1 → talk → stats scan 24.858–31.932 (bars only, no numbers,
     AI-GENERATED) → talk → macro tracker 36.637–39.740 → talk → CTA 2 → end card 55.289–57.190. Before → other → after,
     never two physique pictures at once, no side-by-side, no "Meet the new you", no email screen.
  Macro beat (D4 of round 1): frames 1097–1107 and 1181–1191 inspected one by one (sheets/macro9_edges.jpg): same
     three-item list, total 363 cal, "logged" state, first and last frame are the list, no recalculation, no foreign
     screen.
  Chips (D8 of round 1): 9:16 chips above the card at the top of the safe area, right edge inside 940 px, never on face,
     hair or abs; end-card chip on the shins; 16:9 chips inside the card frame (sheets/chips9.jpg, chips16.jpg). 9:16
     chip frames are pixel-identical to round 2.
  Skin (D6 of round 1): 9:16 cheek patch identical to round 2 (L 33–38, a 14, b 16, chroma 21.3); 16:9 recropped holds
     chroma 21.3–23.3 vs round 2 20.5–22.7 (same grade); Ad 1 big-face frames 25–29 with the same patch → ≈ 0.8×; trees,
     pool and shorts not neon.
  §5 framing: levels alternate at all 13 visible talking joins (face height NEAR 24–26 % vs FAR 18–22 %); 0 naked jump
     cuts at the 22 picture joins (9:16) / 20 (16:9); hold crops fixed (no per-hold drift seen on any pair).
  §6 audio seams: 0 of 22 picture joins with a sample step above the file's own p99.99 ceiling (0.248; worst join 0.092
     at 8.942 and 36.637 s); the RMS steps at 9.576 s (+16.6 dB) and 44.478 s (+21.6 dB) are word onsets after airtight
     pause removal, unchanged from round 2.
  Viewer judgement, 9:16 at phone size (sheets/hook_end.jpg + the cut sheets): the hook works — AI picture with the
     label and "This picture got me" from the first frame, his face on "not even real" at 2.07 s. The photo run
     (1.7 / 0.9 / 0.63 × 3 s) is brisk and readable; the BEFORE lands on "back". Sharpness: face Laplacian variance at
     360 px wide, matched face size 150–205 px: round 3 NEAR 84–96 (median 93), FAR 69–166; Ad 1 vertical 137–228
     (≈ 190) → ≈ 0.5×, visibly softer than the studio photos beside it — the same footage-report number as round 2, not
     a build defect per §5. End card: clean, chip off the physique, pill + URL legible.

COULD NOT VERIFY:
  - By ear: every measurement above (tail, seams, loudness, N2) is instrumental; the `artifacts` FAIL still needs a
    human ear (Dan's ruling).
  - The "abs." cue at 1.502 s: the envelope shows the "me"+"abs" vowels running together 1.17–1.52 s, so I could not
    place the "abs" vowel onset; the gate's aligner reports worst +18 ms and the frames are identical to round 2 — no
    regression, but not independently confirmed.
  - The delivery folder (names, 540p copies, A/B clip, notes, recipe, measurements JSON) — barred from it.
  - Lip-sync beyond the gate's audio-vs-source row (+0.04 ms) — not re-measured.
  - The 9:16 crop in source coordinates for the re-centred hold (only delivered-frame measurements taken).
```
