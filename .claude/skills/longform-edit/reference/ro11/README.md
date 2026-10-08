# RO-11 "When Calories Don't Matter For Fat Loss" (9/23 C1705): round 1 recipe (Claude Opus 5.5, 2026-10-01)

Second film built on the approved HyperFrames templates. Starts from `../ro10/` (same set, same locked look, same
script order); only the files that differ are kept here. Work dir and media: `/Volumes/Extreme/_edit_work/ro11/`.

What changed from RO-10:
- `plan.py`: an `ai` item (kind `ai`, a full-screen opener slot) shows labelled START/END placeholder frames from
  `aiframes/A-start.png` / `A-end.png` until the motion is approved and generated. `stills.py` handles it.
- `gfx.py`: section titles read `FACTOR n OF 7`.
- `page.py` / `page_extra.py`: an "AI opener frames" section under the first minute; missing check files do not crash the page.

Traps this build paid for:
- **Fact card copy is one line each and short.** `from_plan.py` asserts the fit before rendering: eyebrow about 20
  characters, headline about 14, detail about 34. Run it WITHOUT `--render` first and fix the copy, then render.
- **A nohup'd Whisper run loses PATH.** `whisper_words.py` needs the project ffmpeg on PATH inside the same command.
- **`checks.py` clearance is left-to-right only.** A wide two-hand gesture that passes UNDER a side card reads as a
  fail (G20, -211 px). Look at the frame before moving the card.
- Renders, stills, first minute and 21 context clips took about 35 minutes on a quiet machine.

Round 2 (2026-10-08), before the full film:
- **Fork to mouth fails in Veo 3.1, fast and full.** Two takes from approved frames turned the fork into a spoon in his mouth
  and detached its head on the way down. Keep utensils on the plate in an AI opener, and make the start and end frames show
  the SAME food (an end frame with food already eaten forces the plate to morph). `gen_motion.py <tag> <dur> <model> <prompt file>`.
- **This copy of `build.py` lacked RO-10's repeated-first-frame fix:** 18 of 57 segments failed `dupscan.py`. Fixed here; the
  cache key does not include the seek, so delete the listed segments before re-running.
- `finish.py`, `finish_chain.sh`, `deliver.sh`: RO-11 versions of RO-10's (chapters = intro, 7 factors, recap).
