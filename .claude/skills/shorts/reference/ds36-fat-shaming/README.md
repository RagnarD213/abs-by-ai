# DS-36 Fat Shaming SFC R1: two-version reaction build and lessons

Reaction Short in the locked Codex R5 format (Bill Maher, Real Time "New Rule: The Fudge Report", 5:55-6:11), cut twice from roll
C1730 (scripted 9:26, off the cuff 10:33) with a shared opening. Built from the DS-43 Terry Crews recipe (`../ds43-terry-crews/`).
Work folder: `/Volumes/Expansion/_edit_work/DS-36/r1/` (recipe/, key/, src/, scripted/, offcuff/, review/). `chain2.sh VERSION` runs
prep -> shot times -> graphics -> framing -> `build.sh` (render + gates) in the right order; `AUDIO_ONLY=1 build.sh VERSION` remixes
and re-burns captions on the existing picture; `gates.sh VERSION` reruns the gate tail. Key: `run_key.sh watchF|S|O` (house key,
DS-44 plate reused: this part of the roll measured screen/plate 0.998-1.018). Page: `page.py` + `review/notes.json`.

## Lessons (each cost a rebuild or a review round)

- **A clip with audience sound running into the next line has no clean audio cut.** Bill's "comeback" is followed by murmur that runs
  straight into "Some". Play the quote as ONE continuous piece and put the full-screen -> panel picture cut inside the murmur
  (`LAYOUT_CUT` in prep.py, `layout_cut_film` in edl.json). A cut there started "Some" hard.
- **Start every talk piece in the quiet before the word, measured at 2 ms.** Whisper's word start plus a 10 ms envelope put two
  in-points 80-110 ms into "Instead" and "Then". The reviewer caught it from the raw lav.
- **A raised hand is not the top of the hair.** Dan's "20 or 30 pounds" gesture lifted the measured hair top 120 px for 7 frames, which
  loosened the crop and dragged the tracking 622 px toward the hand. `framing.measure` now reads the hair top only within +-330 cache
  px of a 31-frame running median of the head column (column tops cached as `framing-cache/c_*.npy`).
- **Graphics read `shots.json` before `shots-times.json`.** After re-timing, a stale `shots.json` put two lower thirds at the old
  times, and `build.sh` then "kept" them because the new framing matched the new shot times. Delete `shots.json` before regenerating
  graphics, or use `chain2.sh`.
- **Copied recipe scripts carry the old job's folder.** `gates.sh` still pointed at DS-43/r2 and failed before touching it. Grep every
  copied script for the old job id before the first run.
- **`pgrep -f` in a wait loop matches the loop itself** (its own command line contains the script name). Wait on an output file.
- **Captions: Whisper stretches some word starts back into the pause** ("And here's how" 0.6 s early). `captions.py` aligns cue starts
  to the delivered film's own medium.en words (`caption_asr.json`, a copy of `finished-asr.json`; valid while the timeline is fixed).
- **`captions:sync` (energy method) can measure the previous cue.** A mid-sentence cue after a 0.3 s pause reads -0.5 s: the "speech"
  found is the previous words. Check each flagged cue against the delivered ASR before believing it.
- **A sibilant-heavy take fails the voice tone row.** About 25 "shame/shaming" pushed 3.5/5.5 kHz up 3.5-4 dB on the scripted take; the
  off-cuff take was thin at 900 Hz instead. Per-take EQ on top of the house voice (`TAKE_EQ` in prep.py), fitted with
  `audio_gate.py <voice wav> --video <master> --no-stamp --reference-rows-only`, passes every reference row. Different takes need
  different fixes: the scripted fix made the off-cuff take worse.
- **Library B0419 (Dan's poolside vacuum) has a dark title band baked into rows 0-380.** Crop below it and scale x1.247; hair keeps
  headroom. B0420 has the same band and a laugh in its draw-in.
- **Clip loudness:** Real Time's mix is peaky (PLR 17). Two compressors with a fast second stage (threshold 0.1, ratio 10, attack
  0.02 ms at 192 kHz) bring it to -14.5 LUFS beside Dan with no limiter.

Gate rows that stay failing on this format (same as DS-43 / DS-44B): full-mix tone (the clip's sound is in the measured window; the
voice alone passes), hair_top on the panel (planned overlap), splice visibility on zoom cuts.
