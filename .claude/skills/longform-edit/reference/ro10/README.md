# RO-10 "Calories: The Reason You're Not Losing Weight" (9/23 C1704): recipe (Claude Opus 5.5, 2026-09-30)

The first film with every lower third, fact card, 3A side list and cycle diagram built from the approved HyperFrames
templates (`_shared/hyperframes/`: `from_plan.py` -> renders, `composite.py` inside the frame loop, `checks.py`).
Work dir and media: `/Volumes/Extreme/_edit_work/ro10/` (never commit media; the repo is public). Starts from RO-16's
recipe (same set, same locked look).

Order: lav (`pick_lav.py`) -> medium.en words on the roll -> Gemini verbatim listen (`gemini_listen.py`, model
`gemini-3.1-pro-preview`; 2.5-pro is gone) -> `verify_asr.py` on every restart window -> `edl.py` -> `shots.py` ->
`assemble_audio.py` + medium.en on the assembled cut -> `words_out.py` -> `plan.py` -> `resolve.py` ->
`from_plan.py --render` -> `stills.py` -> `review_media.py first|context|verify` -> `hair_first.py` -> `page_extra.py` -> `page.py`.
Full film (round 2, delivered 2026-10-01, independent review SHIP on the first candidate): `clipscan.py` -> `build.render_range(0, total)` ->
`finish_chain.sh` (audio gate, transcript, `finish.py`, watch pass, `haircheck.py`, hyperframes `checks.py`) -> reviewer -> `watch.py --judge` -> delivery gate.

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

Traps the full-film round paid for (2026-10-01):
- **A segment can open on a repeated frame.** `render_seg` seeked to the frame's exact time rounded to 4 places; when that
  lands just past the frame, ffmpeg drops it and repeats the next one (16 of 53 segments). The output seek is now 0.4 frame
  early. `dupscan.py` lists any cached segment whose first two frames are identical; run it before the full render.
- **Whisper invents doubled words on the finished audio** ("eating eating", "carbs. Carbs.", "AI, God, fast"). Settle each by
  re-transcribing 5 s alone and reading the level between the words before calling it junk.
- **The label row needs the chip as the HyperFrames template draws it.** A `softblue.py` reference chip reads 0.83 against
  a fact card's chip (needs 0.85); a crop of the scene's own render reads 0.975. Build the gate plan's chip for a
  HyperFrames scene from `hf/renders/<id>.mov`.
- **`framing:push_coverage` measured only the wide holds on this film** (x1.088) although W2 and T2 alternate as on RO-16
  (x1.345). Reported as a measuring gap; not tuned.
- **Check what follows the last word before promising an end hold.** C1704 has none: Dan looks down and leaves at once.
- **The delivery gate takes about 35 minutes on an 8-minute film** (banned-screen row). Run it in the background and do not
  restart the session under it.
