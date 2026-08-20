# reference/ — working scripts

Copy and adapt; do not rewrite. Media stays out of git, code lives here — the original
`/shorts` V4 pipeline was lost once by keeping code beside the media.

## Generic (2026-08-20, built on the 3-video 8/3 batch) — START HERE

These take a per-video `ranges.py` / `chips.py` and work on any roll. They supersede the
one-off scripts below.

| file | what it does |
|---|---|
| `probe_identify.py` | transcribe 100 s audio probes to identify WHICH VIDEO each clip is |
| `tx_runner.py` | full Whisper `small` word-timestamp pass over the chosen rolls |
| `dump_segments.py` | whisper json → readable `start-end text` list with `[GAP n.ns]` markers |
| `silences.py` | `silencedetect` → `silences.json` (−30 dB / 0.10 s), prints 3 thresholds |
| `words.py` | word timestamps in a window; `*` = zero-length, `~` = stretched (>0.8 s) |
| `diag.py` | nearest silences + words around any timestamp — use on every builder flag |
| `build_edl_generic.py` | ranges.py → `edl.json`, all six cut-placement rules, flags every unplaceable edge |
| `build_gfx_generic.py` | J2 chips (SOURCE time → OUTPUT time via the EDL) + Manrope watermark |
| `composite_generic.py` | chips with 0.35 s alpha fades over the graded cut, CRF 18, audio copied |
| `make_srt_generic.py` | SRT timed to the FINAL edit; punctuation-aware joins, balanced 2-line wrap |
| `qc_generic.py` | duration, stream spec, LUFS, splice discontinuity, graphics on/off, joint re-transcription |
| `parse_grade.py` | run color-grade-ai's auto_grade over N frames, print the medians |
| `make_chapters.py` | YouTube chapter markers from the chip timings |
| `onscreen_callouts.py` | find every "I'm going to show you…" moment, in FINAL-EDIT time |
| `content_flags.py` | locate profanity / named people / risky lines, in FINAL-EDIT time |

**Worked inputs from the 8/3 batch** — read these for how a keep-list is actually written,
every cut carries a comment saying what it removes:
`ranges_spraytan.py` · `ranges_zepbound.py` · `ranges_supplements.py`
`chips_spraytan.py` · `chips_zepbound.py` · `chips_supplements.py`

Order: `probe_identify` → `tx_runner` → `silences` → `dump_segments` → (write `ranges.py`)
→ `build_edl_generic` → fix flags with `words`/`diag` → `render.py` → `build_gfx_generic`
→ `composite_generic` → `make_srt_generic` → `qc_generic`.

## One-off originals (2026-08-03 meal-prep, 2026-08-19 invest-health)

| file | what it does |
|---|---|
| `whisper_run.py` | local Whisper, word timestamps (41 s for 5:45) |
| `whisper_to_scribe.py` | Whisper JSON → ElevenLabs Scribe shape, so video-use never calls Scribe |
| `build_split.py` / `build_graded.py` | per-beat SPLIT-SCREEN segments (the only screen-recording build) |
| `build_edl_investhealth.py` | the first 98-range EDL builder (generic version supersedes it) |
| `build_gfx.py` / `build_gfx_investhealth.py` | earlier chip builders |
| `composite.py` / `composite_v2.py` | earlier overlay passes |
| `make_srt.py` / `make_srt_v2.py` | earlier SRT builders (no punctuation-aware join) |
| `qc_investhealth.py` | earlier QC |
| `edl_videouse.json`, `ground_truth.json` | the approved 20-beat EDL and its scoring fixture |
