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

## Round 2 reviews (2026-10-20): what four independent reviews caught

- **Hair: a camera limit is Dan's call, not a crop fix.** C1512 framed his hair at the top row (`hairtop.py`: 72 % / 47 % of talking
  samples). The 2026-10-20 headroom rule cannot be met by any crop; the Short never crops further than the film. Put it to Dan first.
- **Land-then-hold, calmer on a swaying presenter.** Fixed per-shot crops let him sit 15-20 % off centre; the shared preset (3.3 % band,
  28 %/s) then panned at up to 300 px/s and reversed inside shots. `batch.window_path` now uses `landing.track` on the FACE-BOX centre
  (the mask's head outline moved 40-45 % less than his face), an 8 % band (10 %, 12 % if a shot still reverses) and 120 px/s on the
  delivered frame. Where he leans 600 px on one line, cover it (library B0223 over "the mirror") rather than pan.
- **Captions over a real photo of his physique go below the navel** (`SHOTS[...]["cap"] = 1650`), and the photo fills the picture with
  the label above it; a boxed card on an empty field was a defect.
- **An AI payoff can contradict the line.** The vampire's spray-tan payoff under "this is the reason why" (he stays pale) failed; only
  the pale opening (f5-26) is used. The chip touched his raised hand at f0-3: check chip clearance on every used frame.
- **Disfluency pass**: transcribe kept windows with `initial_prompt="Um, uh, ..."`; it found "he, uh, takes" that CTC had hidden, and
  round 1's `WORDFIX` had pinned "takes" onto the "uh".
- **Eyebrows in CAPITALS** (Dan, 2026-10-20): the small label line (title band eyebrow, bar topic) is typed in capitals; main lines
  title case; `topic_case="preserve"` so code never uppercases.
- **The render queue routes every ffmpeg separately** (`renderq/ffshim.py`): a chain of six commands waited hours. `batch.py render`
  now delivers (audio gate, review copy, transcript, gate plan) and runs the watch pass in the same process; `deliver.py copy` and
  `runwatch.sh` skip when `build/<S>/delivered.sha` is newer than the render.
- **Run the whole build step through the queue as ONE step:** `renderq.py run --group SL-15 -- bash chain_r2.sh A C` (render, deliver,
  watch in one slot, about 5 minutes for both Shorts) instead of a chain of queued commands; checks go `--light` (`rungate.sh`).
- **Delivery gate 2.6.1 result on R2:** 37 of 39 pass on each Short; `framing:hair_top` and `framing:headroom` fail on the camera's
  own framing (hair at the raw roll's top row), which is Dan's decision, never a threshold change. `framing:centering` wants each hold's
  median head offset within 6 %: `window_path` keeps it within 4.5 % (a quicker 160 px/s follow where he leans fast).
- **Real-photo chip references must be drawn with the same anchor as the frame** (`chip_png(..., anchor="mt")`): a half-pixel offset
  read 0.833 against the gate's 0.85.
- **A prompted disfluency sweep after every cut change** (`initial_prompt="Um, uh, mm."`, 10 s windows): a late reviewer found an "um" before
  "He's trying to avoid cancer" that two sweeps missed; the first cut left 55 ms of its "m" (cut where the pitch rises into the next word).

## Title band descender fix (2026-10-22)

`lib.band()` now draws the title at y 86 with a 96 px line step (was 96 / 100). With title-case titles, a second line with g, j, p, q or y at 88 px ran its descenders to row 312, cut by the glass line at 309 and the picture at 310 (SL-17 reviewer B5; 11 delivered Shorts were affected, `Docs/SHORTS_TITLE_BAND_AUDIT_20261022.md`). The lowest glyph row is now 298. `batch.py gfx|proof|render` runs `_shared/softblue_titlecheck.py` on every TITLE first and stops if any lowest white row is 299 or lower down. Check a batch by hand: `python3 .claude/skills/_shared/softblue_titlecheck.py titles <batch dir>`.
