# `softblue-sl19/`: SL-19 3 Healthy Foods That Made Me Fat shorts (R1, 2026-10-20/21)

The SL-15 batch renderer (`softblue-sl15/`, read it and `softblue-sl07/` first) adapted to RO-17, a 4K roll (C1713, 9/23 studio set)
graded with the locked grade-C lut: `lib.py` and `batch.cam` take SL-07's 4K windows (no upscale), with the film's exact chain (no
`out_range`). Work folder `/Volumes/Extreme/_edit_work/SL-19/` (build/ is a link to the Expansion drive). Three shorts, all gate PASS 39/39
and audit SHIP on the second pass.

## New here
- **`scenes_hf.py`**: the film's approved fact cards (before-card template: photo, AI chip, glass card, count-up) re-laid at 1080 x 1610 for
  the picture area, everything above y 1066 so captions land on the field. Covers with `hf=<mov>`; `batch.picture` reads them (BT.601 decode).
  `deliver.plan` declares each card's region and its own AI chip (cropped from the card's render, per-insert `chip`/`pos`).
- **`haircheck.py`**: VIDEO-RULES 2026-10-20 head clearance on the DELIVERED file, every 0.25 s plus each talking shot's first/last frame,
  person-mask top vs the picture top (>= 20 px). Imports deliver.py by path (`import deliver` picks up `_shared/deliver`).
- **`FADE_IN`** (plans): a shorter first fade where a short opens a few ms before a word (D: 4 ms).
- **Bar eyebrows stay in CAPITALS** (GRAPHICS-STANDARDS eyebrow exception, Dan 2026-10-20): `cmd_gfx` no longer passes `topic_case`.

## What this batch learned (each cost a rebuild)
- **Run the whole build as ONE render-queue step** (`renderq.py run --group SL-19 -- zsh chain8.sh`). Run step by step, `track` queued
  each of ~22 inner ffmpeg calls separately and waited over an hour; background waiters started with the Bash tool were killed while queued.
- **A word's END can sit on the next sentence's first sound.** Short 1 cut at film 240.84 kept a quick "but" (240.86-240.94): the -30 dB
  burst before it was the end of "channel," not "but". Transcribe the cut from 2-3 candidate starts with a filler prompt; take the first
  start where Whisper does not hear the dropped word.
- **Widening a pause moves a piece edge past its cover clip.** Covers are in film time; when a piece end grows, grow the cover's `b`
  (and a later cover's `a`/`t`), or a 0.2-0.5 s sliver of Dan appears. Check `shots.json` for any talk shot under 1 s after every edit.
- **Removed lines leave rushed joins.** Keep about 0.35-0.55 s between sentences at a join (the film's own pause is the guide).
- **Dropping a cover can merge two talking shots** and put a key-point bar on the tight window: re-check `win` under every bar.
- **A bar's `a = -0.2` can start it on the previous shot** when the phrase follows a cut closely; use `a = -0.02 to -0.05` there.
- **Old approved AI clips: check the exact used range AND crop.** A10 failed clipcheck on 0-97 (the tin set on the sofa back, outside
  the crop), then the frame-reviewer failed 0-59 (the tin swings across his chin); 0-46 passed both.
- **A card clip in the picture area must clear the captions** (A3 at y 750 met them; y 480 is clear).
- **The Extreme drive filled to 0 bytes mid-render** (other sessions). Delete your own `trk/` frame dumps after tracking; keep `build/` on Expansion.

## Title band descender fix (2026-10-22)

`lib.band()` now draws the title at y 86 with a 96 px line step (was 96 / 100). With title-case titles, a second line with g, j, p, q or y at 88 px ran its descenders to row 312, cut by the glass line at 309 and the picture at 310 (SL-17 reviewer B5; 11 delivered Shorts were affected, `Docs/SHORTS_TITLE_BAND_AUDIT_20261022.md`). The lowest glyph row is now 298. `batch.py gfx|proof|render` runs `_shared/softblue_titlecheck.py` on every TITLE first and stops if any lowest white row is 299 or lower down. Check a batch by hand: `python3 .claude/skills/_shared/softblue_titlecheck.py titles <batch dir>`.
