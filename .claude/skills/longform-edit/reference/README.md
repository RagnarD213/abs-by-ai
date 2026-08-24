# reference/ — working scripts

Copy and adapt; do not rewrite. Media stays out of git, code lives here — the original
`/shorts` V4 pipeline was lost once by keeping code beside the media.

## THE STYLE PASS (2026-08-24, the ab-wheel rebuild) — READ SKILL.md STEP 2.5 FIRST

These are the ones that were missing when an outside editor beat this pipeline on the same
footage. Every file here backs a **hard failure** in `qc_style.py`.

| file | what it does |
|---|---|
| **`qc_style.py`** | **THE GATE.** Measures the FINISHED FILE — channels, bed, pace, dead air, cuts/min, longest static stretch, coverage, captions, splices, loudness, true peak. Every failure names its fix and step number. Calibrated on three cuts of the same footage. |
| `HOUSE_STYLE.md` | the measured colour / type / layout / timing spec. Do not re-interpret it per video. |
| `subject.py` | where the subject is, frame by frame, from a median plate of the locked set |
| `plan_punchins.py` | the cut plan: pause removal (word-guarded), set trims, and a crop level per kept piece |
| `render_tight.py` | per-piece render with exact frame counts (`-frames:v N`, never `-t`) |
| `build_tight_audio.py` | the matching audio cut in ONE graph, so nothing rounds per piece |
| `repcut.py` | pose-matched trim points inside a repetitive movement |
| `segmap.py` | map EDL ranges to their already-rendered segments in `clips_graded/` |
| `tmap.py` / `timeline_outputmap.py` | source ↔ output time, words and beats on the cut timeline |
| `find_cue.py` | locate a phrase on the output timeline, searching AFTER a time |
| `build_voice_singlemic.py` | rebuild the voice from the good channel, frame-locked |
| `fitvoice_bedaware.py` | fit the voice EQ against a reference that HAS a music bed (subtracts it) |
| `pick_bed.py` | choose the music bed by measurement against a reference edit's own bed |
| `audio_final.py` | voice + ducked bed + synthesised SFX + corrective loudnorm |
| `build_gfx_motion.py` | render every graphic to an alpha QTRLE `.mov` via `_shared/motionlib.py` |
| `build_inserts_motion.py` | pre-render cutaways: full-frame, or inside a bracketed inset window |
| `build_endcard.py` | end card with a real app screen in a phone-shaped window |
| `composite_motion.py` | two overlay passes — cutaways, then graphics + watermark |
| `captions_burn.py` | phrase-chunked burned captions + `.srt`, suppressed over full-screen cards |
| `spec_example_abwheel.py` | a worked plan: 26 cutaways + 27 graphics authored against the transcript |

**These carry the ab-wheel paths.** They are templates, like everything else here: copy one
into the video's working dir and change `BASE`. The animated-graphics and SFX packs are
shared with `/ad-edit` at `.claude/skills/_shared/motionlib.py` and `sfxlib.py` — a fix in
one now reaches both, which is the point.

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
| `joints.py` | re-transcribe 6s of the FINISHED render around named beats |
| `srt_validate.py` | re-transcribe N windows of the FINISHED render, measure SRT overlap |
| `qc_generic.py` | duration, stream spec, LUFS, splice discontinuity, graphics on/off, joint re-transcription |
| `parse_grade.py` | run color-grade-ai's auto_grade over N frames, print the medians |
| `make_chapters.py` | YouTube chapter markers from the chip timings |
| `onscreen_callouts.py` | find every "I'm going to show you…" moment, in FINAL-EDIT time |
| `content_flags.py` | locate profanity / named people / risky lines, in FINAL-EDIT time |

## Revision pass — clips, cards and surgical fixes (2026-08-21, spray-tan rev 1)

Built for Dan's "no more than 30 seconds without a clip or a graphic" note. They take a
per-video `inserts.py` (see `inserts_spraytan.py` for the shape: `(start, dur, kind, key,
note)` plus a `STOCK` map of Pexels file → seek point).

| file | what it does |
|---|---|
| `plan_map.py` | output timeline + chip windows + every gap, WITH the transcript text inside it |
| `out_transcript.py` | sentence-level transcript on the OUTPUT timeline, for placing an insert on the word |
| `inserts_spraytan.py` | the 95-insert list for the spray-tan revision — the data-file shape to copy |
| `verify_cover.py` | asserts Dan's ≤30 s rule and that no full-frame insert hides a chip |
| `build_inserts.py` | stock → exact-duration 1920×1080 29.97 MP4; blurred fill for vertical sources |
| `composite_inserts.py` | pass 1: the video cutaways, alpha fades built in the graph, audio copied |
| `build_cards.py` | J2 fact cards, viewer-LEFT, asserted clear of the chip band; full-frame app cards |
| `build_photos.py` | before/after panels — matched crops, olive frame, BEFORE/AFTER eyebrows |
| `composite_gfx.py` | pass 2: cards + panels + chips + watermark, with the chip-collision assertion |
| `build_edl_rawedges.py` | `build_edl_generic.py` + `rawin`/`rawout` per-range edge overrides |
| `apply_vf.py` | per-range `vf`: alternating 10 % zoom cuts (skipping joins a cutaway hides) + the alpha-masked blemish patch |
| `deo_detect.py` | find the arms-spread shots by forearm skin in the outer thirds — 20× separation |
| `deo_verify.py` | LOSSLESS A/B of a blemish patch: proves zero change outside the box, writes the before/after sheet |
| `make_srt_declump.py` | `make_srt_generic.py` + drops hallucinated zero-length clumps, ties break on reading order |
| `qc_with_inserts.py` | `qc_generic.py` + off-chip samples chosen from overlay-free time + "every cutaway is really on screen" |

## Audio: channels first, then tone (2026-08-22, spray-tan rev 2)

| file | what it does |
|---|---|
| `chan_analyse.py` | **run this on every new roll first** — inter-channel delay + polarity, per-channel SNR, clipping and mono-fold comb ripple. Catches a two-microphone roll masquerading as stereo |
| `build_audio_singlemic.py` | rebuild the programme audio from ONE channel, frame-locked to a picture you are not re-rendering (locks to each cached segment's VIDEO duration, asserts against the finished file before muxing) |
| `fitvoice_longform.py` | score a candidate voice chain against a reference voice over 10 bands × 5 windows |
| `finish_audio.py` | the fitted chain + two-pass loudnorm, muxed with `-c:v copy` |

**Sourcing stock:** Pexels download URLs work with plain `curl`; the SEARCH pages are
Cloudflare-gated. Load a Pexels page in the in-app browser and `fetch('/search/videos/
<term>/')` same-origin — one `javascript_tool` call sweeps a dozen terms and returns
slug+id for each.

**Worked inputs from the 8/3 batch** — read these for how a keep-list is actually written,
every cut carries a comment saying what it removes:
`ranges_spraytan.py` · `ranges_zepbound.py` · `ranges_supplements.py`
`chips_spraytan.py` · `chips_zepbound.py` · `chips_supplements.py`

Order: `probe_identify` → `tx_runner` → `silences` → `dump_segments` → (write `ranges.py`)
→ `build_edl_generic` → fix flags with `words`/`diag` → `render.py` → `build_gfx_generic`
→ `composite_generic` → `make_srt_generic` → `qc_generic`.

## Multi-source (2026-08-20, built on the 8/14 ab-wheel video) — a video cut from SEVERAL ROLLS

The 8/14 outdoor shoot recorded one video across **four separate rolls**, not one long take.
Every generic script above assumes a single source and silently breaks: identical timecodes
exist in all four rolls, so a chip, an SRT word or a "mid-speech split" check can match the
wrong roll. These take a `ranges.py` whose entries are `(source, start, end, beat[, mode])`
plus `SOURCES` / `GRADES` dicts, and resolve everything **inside** the owning roll.

| file | what it does |
|---|---|
| `build_edl_multisource.py` | per-roll words + silences; adds `raw` / `rawin` / `rawout` modes |
| `build_gfx_multisource.py` | chips carry their roll, so `src_to_out` cannot match the wrong one |
| `composite_multisource.py` | chips + watermark + **video PiP inserts** (see `pip_abwheel.py`) |
| `make_srt_multisource.py` | per-roll word mapping + a brand re-spell pass |
| `tailcheck.py` | re-transcribes EVERY beat's tail from the FINISHED render — the only test that catches a clipped trailing fricative |
| `sil45.py` | re-measures silence at −45 dB (a −30 dB pass calls a trailing fricative "silent") |
| `ranges_abwheel.py` · `chips_abwheel.py` · `pip_abwheel.py` | the worked 4-roll inputs |

**`raw` / `rawin` / `rawout` exist because a SILENT range has no words to snap to.** A 60-second
live workout set would otherwise have its in-point resolved forward to the next spoken word,
deleting the whole set. `rawout` is also the fix for a clipped fricative.

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
