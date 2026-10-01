# RO-10 "Calories: The Reason You're Not Losing Weight" (9/23 C1704): recipe (Claude Opus 5.5, 2026-09-30)

The first film with every lower third, fact card, 3A side list and cycle diagram built from the approved HyperFrames
templates (`_shared/hyperframes/`: `from_plan.py` -> renders, `composite.py` inside the frame loop, `checks.py`).
Work dir and media: `/Volumes/Extreme/_edit_work/ro10/` (never commit media; the repo is public). Starts from RO-16's
recipe (same set, same locked look).

Order: lav (`pick_lav.py`) -> medium.en words on the roll -> Gemini verbatim listen (`gemini_listen.py`, model
`gemini-3.1-pro-preview`; 2.5-pro is gone) -> `verify_asr.py` on every restart window -> `edl.py` -> `shots.py` ->
`assemble_audio.py` + medium.en on the assembled cut -> `words_out.py` -> `plan.py` -> `resolve.py` ->
`from_plan.py --render` -> `stills.py` -> `review_media.py first|context|verify` -> `hair_first.py` -> `page_extra.py` -> `page.py`.

Traps this build paid for:
- **Global W/T alternation cannot place side cards.** Fixing one card's exit flips the next shot too. `build.py
  all_segments()` solves every picture segment at once (a join within 1.2x in size is a jump unless a full-screen item
  covers it); cards prefer W4S (W4 slid left) and fall back to W2 + stretch.
- **Pure reframe cuts** (`shots.py`): C1704 had few pauses over 0.7 s (25 shots, one 68 s long). Shots over 18 s split at
  sentence gaps every 9-14 s; the audio runs straight through (no fades, no room-tone fill at those joins).
- **The copied EQ failed the tone row** (3.5 kHz +3.9, 5.5 kHz -5.2): re-fit on the roll (`FIT.mp4.voice_chain.json`) + the
  approved +0.9 dB at 150 Hz (RO-12 trap 4 again).
- **Fidelity through an encode lies.** The render reads 39 dB against its own graded base, exactly like a plain re-encode
  with no graphics. Prove the compositor in RGB before encoding: 964 M untouched pixels, 0 changed.
- **Phrase matching:** Whisper writes "1.5mg" as "1" + ".5mg" and "o'clock" as "o" + "'clock"; anchor on neighbouring words.
- A snapped in-point can land in the dip inside a word ("I've"): check every in-point's envelope, not only the flagged ones.
