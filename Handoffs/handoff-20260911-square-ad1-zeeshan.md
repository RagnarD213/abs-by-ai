# Handoff — Ad 1 "This Picture Got Me Abs" (Zeeshan's final) — SQUARE 1:1 version

**Written 2026-09-11. Fire SIXTH — AFTER Dan approves the re-delivered Zeeshan Ad 1 vertical (re-delivered 09-10 with
his audio untouched after the first two were rejected on audio).** Read
`Handoffs/handoff-20260911-square-ads-00-shared-rules.md` first, then this doc, then `/shortad-from-longform` **[A6]**
(the Zeeshan lessons: a 24 fps editor, a quiet dynamic mix, the compositor) and `reference/a6/README.md`.

## What exists

| | |
|---|---|
| editor final | `Zeeshan Ad Videos/this picture got me abs - ad 1/this picture got me abs \| zeeshan \| 16x9 \| ad 1 \| h264.mov` (an `h265.mov` sits beside it) — 1920×1080, **24 fps, 5,980 frames, 4:09.17** |
| vertical | `… \| claude \| 9x16 \| ad 1.mp4` (5,980 = his) + `… \| claude \| 9x16 59s \| ad 1.mp4` (55.5 s, 1,332 frames) — `qc.py` 20/20 in `--verbatim` mode; **awaiting Dan's approval**. `notes-vertical.md` + `recipe-vertical/` beside them |
| build dir | `/Volumes/Extreme/_edit_work/ad1-zee-vert/` — the **a6 compositor** (`zbase.py` LUT conform on his 24 fps grid, `zcrop.py` hair-anchored NEAR/FAR, `zgfx.py` his tokens, `zrender.py`, `zmux.py`, `zcutdown.py`/`zcut_build.py`, `zhairgate.py`, `zwatch_*.py`). Copy to `ad1-zee-sq/`. |
| audio | **Zeeshan's exported track bit for bit** (md5 = his; −23.5 LUFS, dynamic — that IS the approved sound; the +9.9 dB/mono build was the rejection). Cutdown: his mix cut only. `audio_gate.py --reference-mix <his> --verbatim`. |
| YouTube / Ads | his 16:9 `1oEcwdp21Fg` (Ad 1 ads were "limited — clickbait"; r2 copy in review). ⚠ `rimBWjT9-oo` / `JOZVk4_HDwQ` carry the REJECTED audio — never reuse; upload the square only on approval |

## Zeeshan-specific

* **His cut shows the banned email-capture screen at 188.75–190.33 s**; the vertical replaced it (the after image alone,
  no confetti/heading — `notes-vertical.md` items 1 and 3) and scanned all 5,980 frames for it (worst match 0.17).
  The square must do the same and run the same scan; add it to the audit prompt.
* 24 fps everywhere: frame maths, the cut plan, the caption timings — nothing from the Muhammad builds' 29.97 numbers.
* His grade is `his.cube` (33³ LUT from pixel correspondences) — reuse; his overlays' in/out frames from `zov.py`.
* The app recording (portrait) → side-by-side family; his AI clips at their card aspect; real after pictures → shared
  rule 4 with the real-picture chip (the vertical predates the label — the square is the first Zeeshan version with it).

## Deliver

`… \| claude \| 1x1 \| ad 1.mp4` + `… \| claude \| 1x1 59s \| ad 1.mp4` in `Zeeshan Ad Videos/this picture got me abs - ad 1/`,
review copies, A/B, stamps, `notes-square.md`, `recipe-square/`; shared "After the build" steps; board entry.

## Starter prompt (Fable 5.1, high)

> Execute `Handoffs/handoff-20260911-square-ad1-zeeshan.md` after reading
> `Handoffs/handoff-20260911-square-ads-00-shared-rules.md` and `/shortad-from-longform` [A6]: build the 1:1 square of
> Zeeshan's Ad 1 from the APPROVED vertical build (`/Volumes/Extreme/_edit_work/ad1-zee-vert/` copied to
> `ad1-zee-sq/`) — 24 fps, 5,980 frames, his LUT, the email screen replaced exactly as the vertical did and scanned
> for, geometry for 1080×1080, Zeeshan's audio bit for bit (`--verbatim`), plus the ≤0:59 square from `cut_plan.json`.
> Every gate, the independent audit, deliver, send Dan the review copies. Model: Fable 5.1, effort high.
