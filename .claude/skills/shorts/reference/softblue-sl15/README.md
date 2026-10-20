# `softblue-sl15/`: SL-15 My First Spray Tan shorts (R2, 2026-10-18)

The SL-07 batch renderer (`softblue-sl07/`, read its README first) adapted to RO-19, a film cut from ONE 1080p roll (C1512, the 8/3
shoot) with the per-roll grade curve "look F" instead of a 4K roll and a LUT. Work folder: `/Volumes/Extreme/_edit_work/SL-15/`
(these are copies kept in git; run from there). Order: `snap.py` -> `batch.py audio, words, plan, track, gfx, proof, render` ->
`deliver.py copy` -> `runwatch.sh S` -> judge + `ra-reviewer` -> `rungate.sh S`. Heavy steps wait for a slot (`buildcap.wait`).

## What is different from SL-07

- **1080p source.** `batch.cam` reads the roll at 1920x1080 through `lib.GRADE` (RO-19 `grades.json` C1512 look F, 16 bit) and
  `Short.picture` upscales the 724 / 604 window to 1080 wide with Lanczos (1.49x). No 4K exists for this shoot.
- **Hair at the top row on every shot** (`shot_framing.json` hair_min 0): `Y0` is 0 for both windows. There is no room to give.
- **Real-photo displays** (`scenes.py`): the film's P02 single photo and P05 before/after pair, rebuilt for the 1080 x 1610 picture
  with `softblue.photo_card` (rise in, slow push), glass tabs, and the real-photo chip ABOVE the cards (inside the card it touched
  his hair). `deliver.plan` declares them as `real_photos` with each chip image and position, plus the chip and tab regions.
- **`plans.WORDFIX`**: CTC put "takes" on "an" (0.65 s late); a word can be pinned from measured levels and Whisper.
- **Dry voice for silences**: `ro19/round4/film/RO-19 round 4 - full film.mp4.untreated.wav` (film clock, lag 0.0 ms at 9 points).

## What this round learned

- **`fx` is the crop POSITION, not the centre.** In `clip_seq` a fill crop sits at `(iw - w) * fx`; for a 16:9 clip in the 1080 x 1610
  picture the source window is 724 px wide at x0 = 1196 * fx. Briefing a reviewer "centred at 22 %" for fx 0.22 was wrong twice: the
  vampire's face is at x 985 and the window was 263-987. Render the exact crop (`clips/cropview/`) and give the reviewer that.
- **Old approved AI clips fail today's checks.** RO-19's A4 (the appointment) changes his hair and stubble from frame 86; A1 (vampires)
  turns the open umbrella see-through over frames 100-110 and pops the cloud onto the island at frame 28. Fixes: A4 ends at frame 85
  (1.05x), A1 is two shots joined by a cut (f7-49, f146-182; a time jump is a cut), crops moved onto the subjects. Each range then
  passed `clipcheck.py` and a fresh `frame-reviewer`.
- **Read a word's levels before trusting the word list.** The "But" thought to sit at 59.18 was the end of "did"; the real "But" was
  kept in piece 2 and only the delivered transcript showed the captions lacked it. Diff caption text against `delivered_asr.json`.
- **An "Um" Whisper misses with no prompt**: transcribing with `initial_prompt="Um, uh, so, like."` found it (10:04.84).
