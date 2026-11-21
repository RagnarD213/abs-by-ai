# RA-01 — ROUND 1 — EDITOR

**Built to `Handoffs/video-editing/RA-01-plan.md` by the editor session (Claude Opus 5, high),
started 2026-09-16, finished 2026-09-17.** Work dir `/Volumes/Extreme/_edit_work/ra01/`.
Raw footage untouched. **$0.00 of AI generation. Nothing uploaded. No dashboard row. Nothing
committed. No third concurrent build — every render, gate and probe ran through `capwait.sh`.**

> **Note on this round.** The first editor instance was killed mid-run by a spend-limit error,
> after both masters had been rendered and while the watch pass was being judged. This session
> resumed rather than restarting: it re-verified the masters against the plan itself, finished the
> 9:16 watch pass, found and fixed one real build defect, re-ran both delivery gates from scratch,
> and wrote the delivery and these round files. Everything below was verified against the files on
> disk in this session; nothing was taken on trust from the previous run's notes.

---

## 1. What was built

| file | where it is | sha256 (first 12) |
|---|---|---|
| `master_9x16.mp4` — 1080×1920, 30000/1001, h264 yuv420p, AAC 48 kHz stereo, **57.591 s** | `/Volumes/Extreme/_edit_work/ra01/master_9x16.mp4` — **HELD, see §4** | `3e5e32bb8a56` |
| `master_16x9.mp4` — 1920×1080, same EDL, **bit-identical audio**, 57.591 s | `/Volumes/Extreme/_edit_work/ra01/master_16x9.mp4` — **HELD, see §4** | `57cde3cf8846` |

Both masters' audio streams decode to the **same MD5 (`f078ac48e76737d890476c5f28bb74dc`)**, so
plan §1's "same audio track (bit-identical mix)" is satisfied by measurement, not by intent.

**Delivered into `Claude Ad Videos/the ai trick that got me abs - RA-01/`:**

```
the ai trick that got me abs | REVIEW 540p 9x16 | RA-01.mp4      540x960,  57.60 s
the ai trick that got me abs | REVIEW 540p 16x9 | RA-01.mp4      960x540,  57.60 s
the ai trick that got me abs | AB audio ref-vs-ours | RA-01.mp4  the audio gate's A/B clip
the ai trick that got me abs | claude | 9x16 | RA-01.mp4.audio_gate.json      (FAIL stamp)
the ai trick that got me abs | claude | 9x16 | RA-01.mp4.deliver_gate.json    (FAIL stamp)
the ai trick that got me abs | claude | 9x16 | RA-01.mp4.audio_untreated.json
the ai trick that got me abs | claude | 16x9 | RA-01.mp4.audio_gate.json      (FAIL stamp)
the ai trick that got me abs | claude | 16x9 | RA-01.mp4.deliver_gate.json    (FAIL stamp)
the ai trick that got me abs | claude | 16x9 | RA-01.mp4.audio_untreated.json
notes-RA-01.md          measurements-RA-01.json
flux_diagnosis.json     sfx_probe.json          recipe-RA-01/
```

The two masters are **not** in that folder. See §4.

## 2. Plan conformance — what I checked in this session, and how

| plan | check | result |
|---|---|---|
| §1 container, 9:16 | `ffprobe` on the delivered file | 1080×1920, 30000/1001, h264/yuv420p, AAC 48 kHz 2 ch, 57.591 s — **≤ 59.00 s with 1.41 s to spare** |
| §1 container, 16:9 | same | 1920×1080, same codecs and rate, 57.591 s |
| §1 identical audio | decoded-audio MD5 of both masters | identical |
| §2 take map | `cut.json` against the plan's table | one seam only (R1→R2 at 12.28 s) and it sits under a card; L5 **take 2** used, as the plan's default |
| §3 length rule | container duration | under the ceiling; **no line cut**, no speed ramp, neither CTA line touched |
| §4 cue map | `timeline_9x16.json` / `timeline_16x9.json` against the plan's table, then the rendered frames | every beat present in both aspects, in order, at the right lengths (three after photographs 0.63/0.63/0.67 s, sequential, never two on screen) |
| §4 before → other → after | timeline | BEFORE 6.27–7.11, **Dan on camera 7.11–7.54**, then the after pictures — never side by side |
| §4 chips | gate `compliance:labels`, plus the frames | 4 AI inserts + 3 real photos, label correlation min **0.999**; 0 missing, 0 wrong label; every chip above his head, clear of face and abs |
| §5 framing levels | `framing.json` + both timelines + gate rows | two levels only; **every `dan` item carries ONE fixed crop for its whole life** — no hold tracks, which is what AGENTS.md's 2026-09-16 16:9 rule requires. Spread ×1.29 (9:16) / ×1.25 (16:9) |
| §6 audio chain | `mix.wav.voice_chain.json` | `pick_lav.py`'s own JSON for the pull, `voice_chain.py` once, bed −32 dB, no hand-rolled processing |
| §7 captions | the plan's `caption_states` + the rendered frames | word-timed from CTC against the FINAL mix; first 30 s read word for word against the script — `apps→abs` and `six-pack` corrections all applied, "abs" lowercase, "AI" uppercase |
| §7 gates | both gates re-run in this session on the delivered files | §3 below |
| §7 negative-imagery + compliance scan | gate rows + `logs/negative_scan_*.json` | both recorded; one finding (the BEFORE photograph) reviewer-cleared, reasoned, not a trigger |
| §8 measurements | `s31_measure_finalize.py` completeness proof | **49 of 49 keys present**, 0 null-without-`_why` |
| §10 must-nots | — | raw roll untouched; $0 spent; nothing uploaded; no dashboard row; no gate, bound or corpus file edited; names unchanged; no media committed; no third build; no speed ramp; no CTA line cut; no chip on his face or abs; never two physique pictures at once; nothing asked of Dan mid-run |

## 3. Gate results — every row, on the delivered files

### 3a. Audio gate (`_shared/audio/audio_gate.py`), both masters, identical

| row | result | number |
|---|---|---|
| `lr_corr` | PASS | one voice, L/R correlation +0.9998 (≥ +0.97) |
| `comb` | PASS | ripple 0.59 dB vs his 0.54 (≤ his + 0.35) |
| `edt` | PASS | early decay 29 ms (≤ 80; his 40) |
| `tone` | PASS | mean 0.74 dB (≤ 1.2), max 1.92 (≤ 2.5) |
| `floor` | PASS | voice over floor 29.7 / 36.7 / 29.4 vs his 27.6 / 34.7 / 28.0 |
| **`artifacts`** | **FAIL** | **flux 0.0895 vs the bound 0.079 (his 0.072 × 1.1)**; swirl 0.794 vs his 0.835 passes |
| `do_no_harm` | PASS | flux ×0.95 and swirl ×0.83 against this file's own untreated source (≤ ×1.35) |
| `dryness` | PASS | 9.1 dB drop 64 ms after a word vs his 7.4 |
| `lufs` | PASS | −14.10 LUFS (−14.0 ± 1.0) |
| `spread` | PASS | speech spread 6.9 dB vs his 8.2; LRA 3.2 LU (his 3.5) |
| `tp` | PASS | −2.10 dBTP (≤ −1.0) |
| `silence` | PASS | 0 digitally silent seconds, 0 below −50 dBFS |
| `length` | PASS | audio 57.589 s vs picture 57.591 s |

**Verdict: FAIL on `artifacts` only — 12 of 13 rows pass.**

### 3b. Delivery gate (`_shared/deliver/gate.py`, `GATE_VERSION 2.1.0`)

**9:16 (`--format ad9x16`): 35 passed, 1 failed, 0 NOT MEASURED, 0 pending, 3 declared n/a.**
**16:9 (`--format ad16x9`): 35 passed, 1 failed, 0 NOT MEASURED, 0 pending, 3 declared n/a.**

The one failure on each is the same row:

| row | 9:16 | 16:9 |
|---|---|---|
| **`audio:stamp`** | **FAIL** — "no valid audio-gate stamp: AUDIO GATE FAILED … artifacts" | **FAIL**, same |

Every other row, both files:

| row | 9:16 | 16:9 |
|---|---|---|
| `container:size` / `:fps` / `:codec` / `:duration` / `:frames` | PASS (1726 frames present, 1726 planned) | PASS |
| `audio:stream_integrity` | PASS (+0.002 s gap, 0 silent seconds) | PASS |
| `audio:lipsync` | PASS (worst +0.042 ms of 1.0 allowed) | PASS |
| `audio:click_at_joins` | PASS (0 of 21 joins) | PASS |
| `style:coverage` | PASS 42 % (min 38) | PASS 52 % (min 35) |
| `style:static_run` | PASS 7.8 s (max 31.6) | PASS 6.8 s (max 25.0) |
| `style:change_rate` | PASS 17.7/min (min 7) | PASS 20.8/min (min 8) |
| `framing:hair_top` | PASS min 43 px, median 58; 105/105 valid | PASS min 43, median 59; 70/70 valid |
| `framing:headroom` | PASS, 7 holds, 0 loose 0 tight | PASS, 6 holds |
| `framing:centering` | PASS worst +1.9 % (max ±6) | **n/a — declared by the `ad16x9` format**, see §6 |
| `framing:no_wide_level` | n/a — declared by the `ad9x16` format, see §6 | PASS smallest head 33.7 % (min 27) |
| `framing:push_coverage` | PASS spread ×1.288 (min 1.1) | PASS ×1.254 |
| `cut:uncovered_joins` | PASS 0.0/min | PASS |
| `cut:black_frames` | PASS 0 frames under luma 6.0, every frame scanned | PASS |
| `cut:min_segment` | PASS 0 under 0.2 s | PASS |
| `cut:jump_cut` | PASS 0 pairs | PASS |
| `cut:splice_visibility` | PASS 0 of 21 | PASS |
| `cut:naked_splices` | PASS 0 naked of 2 candidates | PASS 0 of 1 |
| `captions:graphic_clearance` | PASS 115 states verified in delivered pixels, tightest **36 px** (min 20), 0 problems | PASS tightest **123 px** |
| `captions:card_collision` | PASS 32 cues, 9 cards, **0 on a card** | PASS |
| `captions:burned` | PASS 64 % of sampled frames (min 45) | PASS 56 % |
| `captions:within_runtime` | PASS last cue ends 55.92 s | PASS |
| `captions:sync` | PASS 115/115 states, median −7 ms, worst −25 ms (max 120), 0 absent | PASS |
| `compliance:banned_screen` | PASS 1726 frames × 28 templates, 0 hits | PASS |
| `compliance:labels` | PASS 4 AI + 3 real, correlation min 0.999, 0 missing, 0 wrong | PASS |
| `compliance:drug_names` | PASS 0 | PASS |
| `compliance:negative_events` | PASS, 40 frames, 1 reviewer-cleared finding | PASS |
| `compliance:script_fidelity` | PASS 100 % (196 of 196) | PASS |
| `watch:pass` | PASS 34/34 boundaries, 37/37 images judged, tied to the file by sha256 | PASS 34/34, 37/37 |
| `srt:present` / `srt:shape` | n/a — a vertical ad burns its captions | n/a |

**There is no NOT MEASURED row and no skipped check on either file.**

## 4. Delivery decision — the masters are HELD

`audio:stamp` FAIL means neither master may go through the delivery script. Following the Ad 4
precedent, the masters **stay in the work dir** and the delivery folder gets everything Dan needs to
judge the cut and make the call: both REVIEW 540p copies, the audio A/B clip, `notes-RA-01.md` (which
states the failing rows in a banner at the very top), `recipe-RA-01/`, `measurements-RA-01.json`,
`flux_diagnosis.json`, `sfx_probe.json` and both gates' stamps. `s29_ship_held.py` is the script;
run it with `--masters` once the stamps read PASS and it places the two masters under the plan's
exact names.

## 5. The `artifacts` FAIL, diagnosed — four measurements, no tuning

All four through the gate's own `common.artifacts`, over the gate's own window (1.00–55.59 s).
`flux_diagnosis.json` has the raw output. **Bound = 0.079** (the stamp's reference reads 0.072;
re-measured locally over the full reference, 0.0765).

| # | what | flux | swirl |
|---|---|---|---|
| (a) | the **untreated lav cut** (`cut_audio.wav`), before any processing | **0.0942** | 0.9600 |
| (b) | the voice chain, **no bed, no SFX** | **0.0966** | 0.9530 |
| (c) | the voice chain **with the bed** (`mix.wav`) | **0.0933** | 0.7953 |
| (d) | the **delivered** master's audio, after AAC | **0.0897** | 0.7986 |

**The source is already 1.19× over the bound before anything touches it.** There is nothing in the
mix whose removal brings it under:

* **The bed is not the cause** — it *lowers* flux by 0.0033 and swirl by 0.16. Removing it or
  turning it down makes the row **worse**. (Plan §6 allows ≤ −30 dB; it sits at −32 dB.)
* **There are no SFX** in this mix, so there is no SFX term to remove (§7, deviation D2).
* **The chain is already doing no harm** — delivered flux is 0.95× the untreated source and swirl
  0.83×, which is what the `do_no_harm` row reports and passes.

Closing the remaining gap would mean processing the voice past the point the pinned reference itself
sits at. That is the exact thing `audio-never-over-strip` and the `do_no_harm` row exist to prevent,
and raising the bound is forbidden outright. **So the row is left FAILING and reported. That is the
finding.** It is in `notes-RA-01.md` under "Your calls", item 8, with three options for Dan.

I do **not** think the row itself is wrong. The bound is doing its job: it is telling us this
outdoor roll's lav is noisier frame-to-frame than the indoor reference. The right fix is at the
microphone on a future shoot, not in this file.

## 6. Two gate rows whose `not_applicable` reason does not describe this build

Neither is something I may change (`formats.py` is off limits and rightly so), but a reader should
know:

* **`framing:no_wide_level`, 9:16** — declared n/a with a `/shortad-from-longform` "Dan sits in a
  full-width WINDOW above the text" rationale. **This cut has no such window**; Dan is full-frame.
  Nothing is being hidden: the 16:9's own `framing:no_wide_level` row *did* run on the same crops
  and passed at 33.7 % smallest head height against a 27 % floor, and the 9:16's `framing:hair_top`,
  `:headroom` and `:push_coverage` all measured and passed.
* **`framing:centering`, 16:9** — declared n/a with a "bullets left and Dan right (Muhammad Ad 2)"
  rationale. **This cut has no bullets and Dan is centred.** The 9:16 row measured the same holds
  and passed at worst +1.9 % against a ±6 % bound.

Both are recorded here rather than worked around.

## 7. Deviations from the plan

**D1 — the delivery plan declared the wrong rectangle for the CTA pill. FIXED this session.**
`s11_cta.py` places each pill by measuring Dan on a rendered frame of that beat and records the real
boxes in `cta.json["boxes"]`, but `s12_gateplan.py` was writing the single **static fallback**
`A.CTA_BOX` into `graphic_regions` for both beats. The two differ by up to **89 px vertically** in
9:16 and by **752 px of width** in 16:9 (declared x 430–1490; the pixels occupy x 54–1866, which I
confirmed by measuring the rendered frame). The gate was therefore grading caption clearance against
a rectangle the pixels do not occupy — "geometry bound to another render", which is precisely what
the v2 evidence contract exists to forbid. Fixed in `s12_gateplan.py` with the reasoning in a
comment; the plan now declares what was drawn. **The honest clearance is 36 px, not the 68 px the
stale box reported.** Both are over the 20 px bound, so this corrected the number, not the verdict —
and it cleared all four caption rows that had been failing (`graphic_clearance`, `card_collision`,
`sync`, plus the knock-on) when this session picked the job up. No re-render was needed: only the
plan was wrong, never the pixels.

**D2 — no transition SFX (plan §6). NOT FIXED, measured reason.** Plan §6 asks for `_shared/sfxlib.py`
one-shots on card ins. I built the eight the plan describes (whoosh on each full card in, pop on each
of the three rapid after photographs), ran them through the same chain as an `--extra` track and
measured (`sfx_probe.json`). The result went **against my expectation** and is worth recording:

| | flux | swirl | delivered tone err (mean / max) |
|---|---|---|---|
| mix as delivered, no SFX | 0.0933 | 0.7953 | **0.74 / 1.92** |
| the same mix **with** the SFX | **0.0908** | 0.7704 | **1.24 / 4.63** |
| bound | ≤ 0.079 | ≤ 0.919 | ≤ 1.2 / ≤ 2.5 |

The SFX *lower* the failing flux slightly — and still leave it far over the bound, so they rescue
nothing — **but they break the `tone` row**, which currently passes comfortably. The whoosh's
3–9 kHz energy lands in the bands the EQ is fitted against, so shipping them as specced turns one
failing row into two. They are out of round 1. A round-2 fix is quieter or band-shaped one-shots;
that is a tuning job, not a blocker. Flagged to Dan as call 9.

**D3 — no take reel.** The plan itself says to skip it when only one pass exists, and only one does.
Recorded for completeness.

**D4 — grade exposure 1.30, not the plan's 1.45 default.** Inside the plan's permitted set and
chosen by the measurement the plan asks for: face luma error against the approved website-video
reference is 9.3 at 1.30 vs 14.7 at 1.45 and 19.6 at 1.60. Numbers in
`measurements-RA-01.json → grade`. Flagged to Dan as call 5, including that 1.00 lands within 2
levels of the approved look.

## 8. The 9:16 watch pass — how it was finished

The previous run left `watchpass_9x16/findings.json` written (37 entries) but never folded into
`watch_pass.json`, so `watch:pass` read NOT MEASURED. In this session I **read the images myself** —
all three contact sheets end to end, plus boundary strips and pair images at the CTA in, the
macro-card in, a mid-film zoom cut and the end-card cut — and re-extracted the macro-card frames in
both aspects at full resolution to check for a black field (there is none; 9:16 is full-frame, 16:9
fills with the picture's own blurred cover). I agree with all 37 verdicts, then folded them in with
`watch.py --judge`, attributing both the original judge and my own re-verification. 34/34 boundaries,
37/37 images, 0 open defects. The 16:9 pass was already complete and judged, and its log is bound to
the current master's sha256 — I verified that rather than assuming it.

No judge subagents were spawned in this session.

## 9. Calls for Dan

Ten, written in full in `notes-RA-01.md` under "Your calls" — the unlabelled BEFORE picture, no line
cut, the two spoken claims kept as filmed, the studio-vs-pool after pictures, the grade exposure, the
6.3 s hook hold, the macro screen's own calorie figures, **the audio row (item 8, the big one)**, the
missing SFX, and whether "Results are not guaranteed" should go on screen. Nothing was waited on and
nothing was asked mid-run.

## 10. Housekeeping

* `scripts/edit-queue/queue.py set RA-01 in_progress --by Claude` — the job was still `ready`;
  `jobs.json` and the `00-MASTER.md` row are updated. It is **not** set to `delivered`, because the
  masters are held. The artifact-db mirror the rules mention was **not** pushed; the next session
  can, or `queue.py` prints the exact `write_db` call.
* `AI_COORDINATION.md` — my own RA-01 entry updated to ROUND 1 DONE / masters held. No other
  session's entry touched. `scripts/board-check.sh` passes.
* `.claude/skills/ad-edit/reference/demo-clip-log.md` — RA-01's six asset uses logged, as plan §4
  asks. ⚠ Worth someone's attention: `dan by pool.png` is now at roughly **seven** uses across Ad 1
  and RA-01 and is due a regenerated sibling before another ad leans on it.
* `recipe-RA-01/REBUILD.md` — brought up to date: it still pointed at the retired per-skill watch
  fork (`s13_watch.py log`), whose output the gate rejects for having no `watch_version`.
* Nothing committed to git.
