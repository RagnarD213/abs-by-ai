# reference/ — working scripts from the 2026-08-03 meal-prep video

Copy and adapt; do not rewrite. Paths inside assume the shoot folder
`Media/longform-raw/<slug>/`. Fix those first.

| file | what it does |
|---|---|
| `whisper_run.py` | local Whisper, word timestamps (free; 41s for 5:45) |
| `whisper_to_scribe.py` | Whisper JSON → ElevenLabs Scribe shape, so video-use never calls Scribe |
| `parse_grade.py` | run color-grade-ai's auto_grade over N frames, print the medians |
| `build_split.py` | per-beat split-screen segments (ungraded) — the v1 build |
| `build_graded.py` | same + the corrective grade on the CAMERA side only — the v2 build |
| `build_gfx.py` | J2 chips + AbsByAI.com watermark as PNGs (PIL; drawtext is broken) |
| `composite.py` | overlay pass: chips with alpha fades + watermark — the v3 build |
| `make_srt.py` | SRT timed to the FINAL edit by mapping words through the EDL |
| `edl_videouse.json` | the approved 20-beat EDL (video-use schema) |
| `ground_truth.json` | retakes / slate / dead air, for scoring a cut objectively |

Order: whisper_run → whisper_to_scribe → (Dan picks beats) → build_graded →
composite → make_srt.
