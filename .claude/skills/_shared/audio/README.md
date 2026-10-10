> # ⚠ 2026-09-29: THE DEREVERB IS OPT-IN. THE DEFAULT IS CODEX'S LIGHT TOUCH.
>
> Dan, 2026-09-28: *Codex's audio approach works better than Claude's; copy it.* Measured, the one setting
> that separates them is the **dereverb**. Everything else Codex ran was this chain's own defaults.
>
> | file | Dan | dereverb | EQ | comp / bed |
> |---|---|---|---|---|
> | DS-17 R4 (C1670) | "All right this works and this is finalized" | none (room 29 ms) | fitted (default) | off / none |
> | C1652 voice, candidate D | "The voice is sounding good" | **none, on a room reading 61-83 ms** | gentle fixed warm EQ | off / none |
> | website rev 2 | "you got it nailed" | none (room 75 ms) | fitted | off / -44 dB |
> | website rev 6 | "you nailed it" | alpha 0.30, **after Dan heard rev 5's room** | fitted | off / -44 dB |
> | C1652 R1 | "Muhammad's audio is significantly, significantly better" | **auto**, alpha 0.30 | fitted, +2 dB treble | 1.5:1 / bed |
> | spray-tan shorts, invest-health | "underwater" | alpha 0.62 / floor -24 | fitted | off |
>
> Every dereverb Dan rejected was applied because a number (EDT > 55 ms) said so; the one he approved was
> applied because he heard the room. So `voice_chain.py` no longer dereverbs by itself. To opt in you need
> **both halves**: the raw room measures wet (EDT > 55 ms, checked by the chain) **and** a listener heard
> the room on an A/B, written as `--dereverb-because "<what, on which A/B>"` (it goes in the sidecar).
> `--no-dereverb` still works and is now a no-op. Oversample, EQ fit, expander and the finish were the
> same on both sides and are unchanged.
>
> ⚠ **The `edt` row (≤ 80 ms) was not changed and now bites harder.** C1652 R4 (approved, "Audio sounds
> good") reads EDT 88 ms with no dereverb and fails it; the 09-02 spray-tan short Dan rejected read 85. A
> wet room that fails `edt` is the *measured* half of the opt-in, never a reason to dereverb unheard.
>
> **`artifacts` now attributes (audio gate 2.0.0, 2026-09-29).** flux and swirl past his ×1.10 still FAIL,
> unless this file's own untreated recording already carried at least that much, i.e. processing added
> none of it. Untreated lav tracks straight off the camera read flux 0.066 to 0.104 across rolls (his
> 0.072); DS-17 read 0.104 untreated and 0.090 delivered, so the old row blamed the chain for the
> microphone. The bound is unchanged; with no baseline there is nothing to attribute and the absolute
> bound stands. The underwater file still fails with its real baseline (0.094 delivered vs 0.075
> untreated: added). Stamps now carry `gate_version`.

> # ⚠ THE DEREVERB WAS RE-TUNED ON 2026-09-09 — DO NOT CHASE EDT AGAIN
>
> The first settings (alpha 0.62, d2 150, floor -24) were rejected by Dan as "underwater": they hit
> EDT 32 ms, PAST Muhammad's 40, and paid for it with 1.41x his spectral flux and 1.15x his HF
> swirl. Measured, the UNTREATED right channel was closer to him than that output on every damage
> metric. He then picked the gentler build by ear from a four-way A/B:
> **alpha 0.30, d1 22, d2 70, floor_db -10, smooth 0.45** (EDT ~48 ms, flux 1.04x his, swirl 0.81x).
>
> `audio_gate.py` now has TWO counterweights to `edt`/`dryness`/`floor` (which all reward MORE
> suppression and between them scored the rejected build as *better*):
>
> * **`artifacts`** — flux and swirl ≤ **his × 1.10**. Bounds us against HIS room.
> * **`do_no_harm`** — flux and swirl ≤ **× 1.35 of THIS FILE UNTREATED**. Bounds us against
>   doing nothing. Added 2026-09-09; it blocks **16 of 16** of the shipped 09-02 Zepbound and
>   supplements shorts, and the rejected spray-tan setting through the shared chain.
>
> **Never raise `artifact_x` or `harm_x` to make a build pass** — that is the failure mode these
> rows exist to stop.
>
> Re-renders of the three affected batches: `Handoffs/handoff-20260909-audio-match-muhammad.md`.
> ✅ `selftest.sh` passes **19/19 in ~90 s** (2026-09-09). It was never broken: it is a **zsh**
> script, and `bash selftest.sh` dies on `${0:A:h}` with *"A: unbound variable"* — which reads
> exactly like a bug. It now refuses the wrong shell with a message instead. **Run `zsh selftest.sh`.**

# `_shared/audio` — the one audio standard for every video skill

**Every video we render takes the LAV TRACK ONLY, as mono, duplicated to centred stereo, through ONE
shared voice chain and ONE shared gate measured against Muhammad's `this picture got me abs | muhammad |
16x9.mp4` — and no QC or delivery script in any skill passes a file that does not carry that gate's
stamp.** Built 2026-09-02 from `Handoffs/handoff-20260902-audio-standard-unification.md` after
nineteen per-skill audio scripts, four SKILL.md "right channel" rules and three separate gates still
let comb-filtered and roomy audio ship four times.

| file | job |
|---|---|
| `pick_lav.py <file>` | **which track is the lav, measured per file.** Probes every stream and channel (2-ch rolls AND the 8/28 four-mono-track rolls), cross-correlates the live candidates ±20 ms, scores arrival / SNR / post-word decay / clipping, writes `<file>.audio_source.json` = `{map, filter, fc_label, lav, far, delay_ms, polarity, verdict, window, window_source}`. With no `--ss` the window slides to where the subject talks most (see "The window trap" below). Exit 2 on ambiguity: refuse, never guess. Verdicts: `two-mics`, `single-live` (dead input), `dual-mono` (one signal → mid). |
| `voice_chain.py --in X --out Y` | **the approved chain** (website video rev 2, "you got it nailed"): pull per `audio_source.json` (refuses SILENT input, a stacked `pan`), **no dereverb unless `--dereverb-because` on a room measuring EDT > 55 ms** (opt-in since 2026-09-29), EQ **fitted** to the reference per file (9 bands + shelf, damped, smoothed, never a pasted curve), downward expander, compressor OFF (`--comp` ≤ 1.5:1), `pan=stereo|c0=c0|c1=c0`, `--bed` ≤ −30 dB ducked, `--extra` SFX, measured gain + `alimiter` (delay measured by xcorr) to −14 LUFS / −2.5 dBTP in PCM. The EQ fit uses an adaptive per-band step (the treble shelf moves the top band ~2.4x, and a fixed step oscillated), then **verifies the tone on the DELIVERED file and folds the residual back** (up to two extra renders, best kept): the expander, limiter and AAC encode all move the spectrum, so a fit that only converges on the intermediate ships 0.5–1 dB worse. Length-preserving; `--frame-lock <picture>`; `--finish-only` for an already-finished mix (shortad's reference-mix path). Writes `Y.voice_chain.json`. |
| `audio_gate.py <delivered> --reference-mix his_mix.wav` | **the editor's-own-mix path (shortad-from-longform).** Provenance is VERIFIED, not assumed: per-second level-normalised correlation against that mix must read ≥ 0.99 at the median (the number that separated his mix from a loudnorm'd one: 0.970) or the flag is refused. With provenance proven, comb / room / tone / floor / dryness / spread are measured and recorded but cannot fail the file — they measure HIS mixing (Ad 2's bed sits 6–7 dB hotter between words than the pinned Ad 1 reference, which is why "passes by construction" was only ever true for Ad 1). Loudness, true peak, silence, length and the L/R image still gate; the stamp carries `mode: reference-mix`, the mix's sha256 and the provenance number. Added 2026-09-03 on the Ad 2 V2 vertical. |
| `audio_gate.py <delivered>` | **the one gate, on the exact delivered file**: L/R ≥ +0.97 · comb ripple ≤ his + 0.35 dB · EDT ≤ 80 ms · tone mean ≤ 1.2 / max ≤ 2.5 dB · floor within 3 dB of his · dryness ≥ his − 1.5 · −14 ±1 LUFS · speech spread ≥ his − 3 dB · TP ≤ −1.0 dBTP · 0 silent seconds · audio length = picture ± 0.10 s. Writes `<file>.audio_gate.json` (sha256 + every number + PASS/FAIL). `--synthetic` for AI voices keeps loudness/TP/silence/length/image. `--ab out.mp4` = his three sentences, then ours. |
| `require_stamp.py <file>` / `qclib.js requireStamp()` | **the enforcement**: stamp exists, sha256 matches THIS file, verdict PASS, same pinned reference. Called by every QC and every deliver script. **Strict since 2026-09-09**: a `--synthetic` stamp no longer satisfies a camera-audio caller — the three AI-voice skills (`make-ad`, `exercisegeneration`, `findassets`) pass `--allow-synthetic` where a reader can see it. The old opt-IN `--strict` was passed by no SKILL.md anywhere, which is what made it useless. |
| `reference.py` + `reference/` | the reference **pinned by fingerprint**: a mono 48 k FLAC of his audio + `reference.json` (sha256, bands, floor, EDT, dryness, spread, LUFS). Regenerates from the .mp4 wherever it lives and refuses a mismatch. Moving the file cannot silently break a gate again. |
| `dereverb.py` | spectral subtraction of the late field. Defaults are the 2026-09-09 approved setting. Its CLI records the do-no-harm baseline on its INPUT; `stash=<delivered path>` parks it where the gate looks. |
| `common.py` | the measurement functions, verbatim from the approved gates, so today's numbers are yesterday's numbers |
| `selftest.sh` | **`zsh selftest.sh`** before any batch: identity on the reference, PASS on the Ad 1 vertical and the approved website rev 2, FAIL on rev 1 and on a synthetic both-mics render, `pick_lav` on all four roll types plus the C1484 window trap, stacked-pan refusal, the DEFAULT chain end-to-end on the DS-17 roll (C1670, no dereverb, gate PASS incl. artifacts), **step 6b: no dereverb by default on the wet C1650, none without a reason, none on a dry room**, **step 7: the dereverb Dan rejected must FAIL `do_no_harm` while still passing the dry-room row, and a file with no baseline must FAIL**, and **step 8: a `--synthetic` stamp must not satisfy the default `require_stamp`** |

## The standard, measured (20–140 s window)

| what a listener hears | metric | Muhammad | Ad 2 rev 2 | gate |
|---|---|---|---|---|
| one voice, not two mics | L/R correlation | +0.993 | +0.992 | ≥ +0.97 |
| no comb | spectral ripple 300–6 k after de-tilt | 0.54 dB | 0.54 dB | ≤ his + 0.35 (a 7.5 ms sum reads 1.09–1.18) |
| a dry room | early decay after a word | 40 ms | 45 ms | ≤ 80 ms (approved website rev 2: 75; the rejected spray-tan short: 85; ⚠ approved C1652 R4: 88. The chain no longer dereverbs by itself) |
| tone | 10-band speech spectrum vs his | 0 | mean 0.33 / max 0.67 | mean ≤ 1.2, max ≤ 2.5 dB |
| clean between words | voice-over-floor 80–250 / 250–1k / 1–4k | 27.6 / 34.7 / 28.0 | −0.2 / −0.5 / −0.6 | within 3 dB |
| words stop cleanly | drop 64 ms after a word | 7.4 dB | 7.4 dB | ≥ his − 1.5 |
| loud enough | integrated loudness | −18.2 | −14.5 | −14 ±1 |
| not crushed | speech spread p90−p10 (LRA reported) | 8.2 dB (3.5 LU) | 7.6 dB (2.9 LU) | ≥ his − 3.0 dB (approved website rev 2 reads 5.5) |
| no clipping on phones | true peak, delivered file | +0.1 (his; too hot) | **−1.30** | ≤ −1.0 dBTP |
| nothing missing | silent seconds; audio vs picture | 0; equal | 0; equal | 0; ± 0.10 s |
| no processing damage | spectral flux / 3–9 k swirl | 0.072 / 0.835 | n/a | ≤ his × 1.10, unless the untreated recording already carried it (2.0.0) |
| **no worse than doing nothing** | the same two, vs **this file untreated** | — | — | **≤ × 1.35** (see below) |

**Every limit traces to a file Dan approved or rejected** (see the comment above `LIM` in `audio_gate.py`).
The website video rev 2 (approved) measured EDT 75 ms and spread 5.5 dB against the handoff's proposed 55 ms
and "his − 1.5", so those two rows were recalibrated to the approved/rejected boundary rather than to "his
number + margin". Two more rows differ from the handoff's table, also from measurement: Ad 2 rev 2's true peak is −1.30 not
−1.5 (so the delivered-file limit is the platform's −1.0; the chain still lands −2.5 in PCM), and
"not crushed" gates the speech spread rather than LRA (Ad 2's LRA is 2.9, under the proposed 3.0, and
Dan approved it). The comb row was added because a pure two-mic sum of a dry voice passes every other
row — non-negotiable 6: a defect the gate cannot see becomes a row.

## Wiring (who calls what)

- **ad-edit**: `base.py` reads `audio_source.json`; `audio3.py`, `audio.py`, `audio2.py`, `audio5.py`,
  `audio_modern.py` → shims to `voice_chain.py`; `voice_ref_check.py` → shim to the gate; `qc.py`/`qc5.py`
  `require_stamp`; `deliver.sh` gates + stamps.
- **longform-edit**: `build_graded.py`/`build_split.py`/`build_*_singlemic.py` pull per the JSON;
  every `composite_*.py` refuses an unstamped input, **with no override** (the `AUDIO_UNGATED=1`
  escape was removed 2026-09-09 — finish and gate the audio before compositing);
  `finish_audio.py`/`audio_final.py`/`chan_analyse.py` → shims; `qc_style.py check_channels`, `qc_generic`,
  `qc_investhealth*`, `cutdown_final_gate` and `deliver.sh` require the stamp.
- **shorts**: `render.js` (all four) pull per the JSON of the source master / raw roll — no `VOICE`
  in the render; `finishaudio.py` (clean-master, zepbound, spray-tan) = `pick_lav` → `voice_chain` →
  `audio_gate` per short; `qc.js` ×4 and `deliver.js` ×2 `requireStamp`.
- **shortad-from-longform**: `build_audio.py` + `a2/edl_verify.py` pull per the JSON; `finish_audio.py`
  → `voice_chain.py --finish-only` (⚠ pass `--tp -1.4` on an editor's brickwalled master — the default −2.5 shaves
  it harder for nothing; the approved Ad-1/Ad-2 files sit at −1.3 dBTP); the gate runs with `--reference-mix his_mix.wav`;
  `qc.py` checks 16 (integrity) + 17 (stamp) + `gain_flatness.py` (one-sided constant-gain proof).

- **findassets / revisions / editor-brief / youtube-packaging / make-ad / exercisegeneration** (Phase 3):
  clips cut with audio pull the lav per `pick_lav` and are gated `--synthetic`; editor reviews quote
  `pick_lav --analyse` + the gate; the editor brief's audio paragraph is generated from `pick_lav` on the
  shoot's rolls and the spec is "must pass `audio_gate.py`"; AI-voice videos gate `--synthetic`.
- **Phase 4 (2026-09-02):** the 8 Zepbound and 8 supplements Shorts were re-muxed through the chain
  (room 67–93 ms → 29–48 ms), every delivered file carries a PASS stamp; the pre-fix files are in
  `Short-form video content/_pre-audiofix-20260902/`.

## Do no harm — the row that would have stopped all of it (2026-09-09)

`edt`, `dryness` and `floor` all improve as suppression increases, so for eight days the gate
graded a dereverb on the one number it was aimed at and nothing else. The missing comparison was
never the reference — it was **the file's own untreated signal**. Measured, our raw right channel
was closer to Muhammad than our processed output on every damage metric.

So whichever stage still holds the untreated audio records it — `voice_chain` right after the
pull, `dereverb.py`'s CLI on its input (`stash=<delivered path>`) — as
`<delivered>.audio_untreated.json`, and the gate refuses an output that scores worse than it.

| ratio to the same file untreated | flux | swirl |
|---|---|---|
| the chain with **no dereverb at all** | 0.98 | 0.96 |
| **alpha 0.30 / floor −10** (approved by ear) | 1.05 – 1.21 | 1.21 – 1.29 |
| limit `harm_x` | **1.35** | **1.35** |
| alpha 0.62 / floor −24 (rejected, "underwater") | 1.30 – 1.61 | 1.57 – 1.94 |

The chain minus the dereverb costs *nothing* (0.96–0.98), which is what makes this row fair: it
charges the dereverb, not the EQ, expander, limiter or AAC encode.

**`gap` and `sfm` are measured and printed but NOT gated.** `gap` (speech over floor) cannot
separate damage from intent — the downward expander alone costs 1.22×, and that is exactly what
the `floor` row rewards. `sfm` moves the *wrong way* on this material: the rejected build's sfm is
LOWER than untreated. A metric that cannot fail a bad build does not belong in a gated row.

**A missing baseline is a FAILURE** (2026-09-09, Phase 0). It used to be recorded as
`ok=True, not_measured=True` — visible, but passing, so "nobody looked" read as "it is fine" to every
downstream caller. That is the exact shape of the defect this row exists to stop. The fix is one line in
the producing stage: `common.stash_untreated()` while the untreated audio still exists, or
`--untreated <that file>.audio_untreated.json` at the gate. ⚠ **Every file gated before 2026-09-09 fails
this row on a re-gate** — that is correct, and it is the input to the regression corpus
(`_shared/qc_corpus/`). In `--reference-mix` mode the row is informational like the other damage rows:
the delivered audio is the editor's own mix, which our chain never touched.

## The window trap: pick_lav is only as good as the stretch it measures (2026-10-10)

The pick is a vote of three scores: who arrives first, who has the higher voice-over-floor (SNR), and
whose words stop more cleanly (decay). On the 7/8 shoot the arrival point always goes to the FAR mic
(about 1 ms, polarity inverted) and SNR always goes to the lav, so **decay casts the deciding vote**,
and decay is only meaningful where the subject is actually talking.

Roll C1484 was measured on the old fixed window (a quarter of the way in: 46.7 s + 45 s). That stretch
holds a 17 s pause with a plane and the crew talking. Decay read 3.81 vs 3.76 dB, which is noise, and
the far mic (channel 0) won 2 to 1. On three clean windows (`--ss 111 --t 60`, `--ss 8 --t 40`,
`--ss 27 --t 22`) the lav is channel 1: SNR 39 to 45 dB against 28 to 30, decay 7.5 against 4.0.

What changed:

- **The default window now follows the speech.** With no `--ss`, `pick_lav` scans the whole file
  (level per 0.1 s on every channel, a few seconds even on a 27-minute roll) and slides the window to
  the highest *speech duty cycle*: the share of frames that are loud on **every** live channel at once.
  The subject reaches both mics; a crew voice or a plane reaches the far mic and barely reaches the
  lav, so those frames do not count. The old fixed window is kept unless another stretch has at least
  0.10 more speech, so rolls that were measured on a good stretch keep the same window and pick.
  C1484 now lands on 123 s (duty 0.81 against 0.38) and picks channel 1 unaided.
- The JSON records `window_source`: `given (--ss)`, `fixed (...)` or `speech (...)`, with the duty numbers.
- `roll_sidecar.py build --force --lav-ss S --lav-t D` re-measures one clip on a window you name.

Checked against the 197 indexed main-camera rolls that were measured on the old window: 191 keep the
same pick (66 windows moved, 60 of those with no change of pick). Four talking rolls move to their
shoot's usual channel by wide margins, the same fault as C1484: **7/8 C1486, 8/14 C1593, 8/3 C1538,
8/3 C1550** (decay 8.7 to 9.8 dB on the new pick). Their roll sidecars keep the old pick until rebuilt
with `--force`. Two B-roll rolls with almost no speech (7/8 C1490, 8/3 C1545) flip on a coin toss.
`selftest.sh` step 4 now includes C1484 with no window given.

What it does not fix, so still check:

- **A pick that disagrees with the rest of its shoot is suspect.** One rig, one channel layout. Compare
  against the neighbouring rolls before trusting an odd one out, then re-measure on a window where only
  the subject talks.
- A decay vote closer than about 1 dB is a coin toss. Read the `why` line, not just the verdict.
- A roll with no clean stretch at all (B-roll, exercise takes, crew chatter throughout) can still be
  wrong on any window. Measure by hand or copy the pick from a talking roll of the same setup.
- Existing `audio_source.json` files and roll sidecars were measured on the old window and are not
  re-measured by this change.

## Calibration notes

- **Bed level (2026-09-03, 04 invest-health, roll C1511):** `--bed-db -30` failed the floor row by
  3.4 / 4.1 / 1.2 dB; **−36 passed** (+1.0 / −0.2 / +2.4) with the bed still 4.3× detectable by
  `qc_style.py`. No bed measured 47/53/46 — the expander already beats his floor by 19 dB, so on a
  quiet lav the bed IS the floor. Start at −36 on longforms; −30 is the ceiling.

## The regression corpus — run it before changing any limit here

`python3 ../qc_corpus/run.py` (**`_shared/qc_corpus/`**, added 2026-09-09) re-runs this gate over every
file Dan rejected and every file he approved, with his own words recorded, and asserts the verdicts
match. **No change to a row, a limit or a setting in this module ships without it passing** — it is a
standing rule in `AGENTS.md`. `selftest.sh` runs as its step 0 and proves the module still measures what
it claims; the corpus then asks it about specific files. The corpus is where the "underwater" dereverb,
the approved website rev 2 and Muhammad's own reference all live side by side, so a limit change that
wins one and loses another cannot ship quietly.

## Non-negotiables

1. Selection is measured per file, never assumed — `pick_lav` output or no render.
2. One chain, one gate, one reference — extend the module with a flag; never write a new chain.
3. The gate measures the delivered file and stamps it; QC and delivery refuse an unstamped file —
   and refuse a `--synthetic` stamp unless the caller says `--allow-synthetic` out loud.
4. The reference is pinned by fingerprint.
5. An A/B clip (his three sentences, then ours) ships with every review copy.
6. A metric Dan rejects on that the gate cannot see becomes a new row.
7. **Processing may never leave a file worse than doing nothing.** If a row rewards suppression,
   a row bounding its damage ships with it, in the same commit.
8. **A check that did not run is a FAILURE, never a pass, and never a silent skip.** A missing flag,
   a missing baseline, a missing plan, a script that is not on disk — each one FAILS and says what is
   missing. Every bypass Phase 0 closed had the same shape: silence that read as approval. If a check
   genuinely does not apply, it is declared explicitly, on the command line or in a config, with a
   reason a reader can audit.
9. **No skill keeps its own copy of the maths.** The spray-tan pipeline held a forked
   `work/dereverb.py` AND passed the rejected parameters on the command line, so correcting the
   shared module changed nothing there. It is a shim now; `render.js` calls this module with no
   overrides. Grep for forks before assuming a shared fix has landed.
