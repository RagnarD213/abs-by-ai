# `_shared/audio` — the one audio standard for every video skill

**Every video we render takes the LAV TRACK ONLY, as mono, duplicated to centred stereo, through ONE
shared voice chain and ONE shared gate measured against Muhammad's `this picture got me abs | muhammad |
16x9.mp4` — and no QC or delivery script in any skill passes a file that does not carry that gate's
stamp.** Built 2026-09-02 from `Handoffs/handoff-20260902-audio-standard-unification.md` after
nineteen per-skill audio scripts, four SKILL.md "right channel" rules and three separate gates still
let comb-filtered and roomy audio ship four times.

| file | job |
|---|---|
| `pick_lav.py <file>` | **which track is the lav, measured per file.** Probes every stream and channel (2-ch rolls AND the 8/28 four-mono-track rolls), cross-correlates the live candidates ±20 ms, scores arrival / SNR / post-word decay / clipping, writes `<file>.audio_source.json` = `{map, filter, fc_label, lav, far, delay_ms, polarity, verdict}`. Exit 2 on ambiguity — refuse, never guess. Verdicts: `two-mics`, `single-live` (dead input), `dual-mono` (one signal → mid). |
| `voice_chain.py --in X --out Y` | **the approved chain** (website video rev 2, "you got it nailed"): pull per `audio_source.json` (refuses SILENT input — a stacked `pan`), dereverb only if EDT > 55 ms, EQ **fitted** to the reference per file (9 bands + shelf, damped, smoothed, never a pasted curve), downward expander, compressor OFF (`--comp` ≤ 1.5:1), `pan=stereo|c0=c0|c1=c0`, `--bed` ≤ −30 dB ducked, `--extra` SFX, measured gain + `alimiter` (delay measured by xcorr) to −14 LUFS / −2.5 dBTP in PCM. The EQ fit uses an adaptive per-band step (the treble shelf moves the top band ~2.4x, and a fixed step oscillated), then **verifies the tone on the DELIVERED file and folds the residual back** (up to two extra renders, best kept) — the expander, limiter and AAC encode all move the spectrum, so a fit that only converges on the intermediate ships 0.5–1 dB worse. Length-preserving; `--frame-lock <picture>`; `--finish-only` for an already-finished mix (shortad's reference-mix path). Writes `Y.voice_chain.json`. |
| `audio_gate.py <delivered> --reference-mix his_mix.wav` | **the editor's-own-mix path (shortad-from-longform).** Provenance is VERIFIED, not assumed: per-second level-normalised correlation against that mix must read ≥ 0.99 at the median (the number that separated his mix from a loudnorm'd one: 0.970) or the flag is refused. With provenance proven, comb / room / tone / floor / dryness / spread are measured and recorded but cannot fail the file — they measure HIS mixing (Ad 2's bed sits 6–7 dB hotter between words than the pinned Ad 1 reference, which is why "passes by construction" was only ever true for Ad 1). Loudness, true peak, silence, length and the L/R image still gate; the stamp carries `mode: reference-mix`, the mix's sha256 and the provenance number. Added 2026-09-03 on the Ad 2 V2 vertical. |
| `audio_gate.py <delivered>` | **the one gate, on the exact delivered file**: L/R ≥ +0.97 · comb ripple ≤ his + 0.35 dB · EDT ≤ 80 ms · tone mean ≤ 1.2 / max ≤ 2.5 dB · floor within 3 dB of his · dryness ≥ his − 1.5 · −14 ±1 LUFS · speech spread ≥ his − 3 dB · TP ≤ −1.0 dBTP · 0 silent seconds · audio length = picture ± 0.10 s. Writes `<file>.audio_gate.json` (sha256 + every number + PASS/FAIL). `--synthetic` for AI voices keeps loudness/TP/silence/length/image. `--ab out.mp4` = his three sentences, then ours. |
| `require_stamp.py <file>` / `qclib.js requireStamp()` | **the enforcement**: stamp exists, sha256 matches THIS file, verdict PASS, same pinned reference. Called by every QC and every deliver script. |
| `reference.py` + `reference/` | the reference **pinned by fingerprint**: a mono 48 k FLAC of his audio + `reference.json` (sha256, bands, floor, EDT, dryness, spread, LUFS). Regenerates from the .mp4 wherever it lives and refuses a mismatch. Moving the file cannot silently break a gate again. |
| `dereverb.py` | spectral subtraction of the late field (moved from spray-tan, unchanged) |
| `common.py` | the measurement functions, verbatim from the approved gates, so today's numbers are yesterday's numbers |
| `selftest.sh` | run before any batch: identity on the reference, PASS on Ad 2 rev 2, FAIL on a synthetic both-mics render, `pick_lav` on all four roll types, stacked-pan refusal, chain end-to-end on an 8/28 excerpt |

## The standard, measured (20–140 s window)

| what a listener hears | metric | Muhammad | Ad 2 rev 2 | gate |
|---|---|---|---|---|
| one voice, not two mics | L/R correlation | +0.993 | +0.992 | ≥ +0.97 |
| no comb | spectral ripple 300–6 k after de-tilt | 0.54 dB | 0.54 dB | ≤ his + 0.35 (a 7.5 ms sum reads 1.09–1.18) |
| a dry room | early decay after a word | 40 ms | 45 ms | ≤ 80 ms (approved website rev 2: 75; the rejected spray-tan short: 85; the chain dereverbs above 55) |
| tone | 10-band speech spectrum vs his | 0 | mean 0.33 / max 0.67 | mean ≤ 1.2, max ≤ 2.5 dB |
| clean between words | voice-over-floor 80–250 / 250–1k / 1–4k | 27.6 / 34.7 / 28.0 | −0.2 / −0.5 / −0.6 | within 3 dB |
| words stop cleanly | drop 64 ms after a word | 7.4 dB | 7.4 dB | ≥ his − 1.5 |
| loud enough | integrated loudness | −18.2 | −14.5 | −14 ±1 |
| not crushed | speech spread p90−p10 (LRA reported) | 8.2 dB (3.5 LU) | 7.6 dB (2.9 LU) | ≥ his − 3.0 dB (approved website rev 2 reads 5.5) |
| no clipping on phones | true peak, delivered file | +0.1 (his; too hot) | **−1.30** | ≤ −1.0 dBTP |
| nothing missing | silent seconds; audio vs picture | 0; equal | 0; equal | 0; ± 0.10 s |

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
  every `composite_*.py` refuses an unstamped input unless `AUDIO_UNGATED=1` (audio finished later);
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

## Calibration notes

- **Bed level (2026-09-03, 04 invest-health, roll C1511):** `--bed-db -30` failed the floor row by
  3.4 / 4.1 / 1.2 dB; **−36 passed** (+1.0 / −0.2 / +2.4) with the bed still 4.3× detectable by
  `qc_style.py`. No bed measured 47/53/46 — the expander already beats his floor by 19 dB, so on a
  quiet lav the bed IS the floor. Start at −36 on longforms; −30 is the ceiling.

## Non-negotiables

1. Selection is measured per file, never assumed — `pick_lav` output or no render.
2. One chain, one gate, one reference — extend the module with a flag; never write a new chain.
3. The gate measures the delivered file and stamps it; QC and delivery refuse an unstamped file.
4. The reference is pinned by fingerprint.
5. An A/B clip (his three sentences, then ours) ships with every review copy.
6. A metric Dan rejects on that the gate cannot see becomes a new row.
