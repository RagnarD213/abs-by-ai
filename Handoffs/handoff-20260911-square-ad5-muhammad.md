# Handoff — Ad 5 "Every Diet You've Tried Failed for the Same Reason" (Muhammad V3) — SQUARE 1:1 version

**Written 2026-09-11. Fire THIRD — AFTER `Handoffs/handoff-20260911-ad5-vertical-revisions.md` has run and Dan has
approved the revised vertical**, so the square inherits its six picture changes and the new label instead of
re-deciding them. Read `Handoffs/handoff-20260911-square-ads-00-shared-rules.md` first, then this doc, then
`/shortad-from-longform` **[A7]** (the Ad 5 lessons) and `reference/a7/README.md`.

## What exists

| | |
|---|---|
| editor final | `Muhammad Ad Videos/every diet you've tried failed for the same reason - ad 5/… \| muhammad \| 16x9 \| ad 5.mp4` — 1920×1080, 29.97, **7,036 frames, 3:54.77**; verified frame-identical to the approved round-5 draft |
| vertical | `… \| claude \| 9x16 \| ad 5.mp4` (7,036 = his) + `… \| claude \| 9x16 59s \| ad 5.mp4` (54.99 s, 1,648 frames) — approved overall 09-11 with three revisions (that handoff) |
| build dir | `/Volumes/Extreme/_edit_work/ad5-vert/` — the **a7 compositor** (`beats.py` → `render5.py` → `zmux.py`; `g5.py` per-frame graphics; `zcrop_ad5.py`, `zhairgate2.py`, `zcutdown_ad5.py`/`zcut_build_ad5.py`, `deliver5.py`). Copy it to `ad5-sq/` AFTER the revisions land, so `beats.py` already has the six changed beats and `g5.real_chip_bleed`. |
| audio | **Muhammad's, untouched** — `zmux.py` asserts the md5 of his AAC stream; the cutdown carries his mix cut at the seams (`cut/his_mix.wav`). Same for the square. |
| YouTube / Ads | 16:9 `bwfSQopZy1w` (**public Wed 09-16 9 AM CT**, every platform) + unlisted ad copy `Yo-6TQik3qY`; Demand Gen ad groups `200151423317` (/start) + `200151529597` (home). ⚠ the *Why My Diets Kept Failing* headline was DISAPPROVED (clickbait) — the square inherits whatever copy is live; do not touch copy here |

## Ad 5 specifics

* **The six revised beats** (frames 439–500 four full-bleed portraits, 3549–3616 the pair replacing the panels,
  6360–6425): at 1:1 they become the shared rule 4 — the 439–500 run as two side-by-side pairs (540×1080 each) or
  four full-height singles on the field, the 3549 pair side by side, 6360 a full-height single — each with the
  real-picture chip. Take the exact pictures the revised vertical chose; do not re-pick.
* `g5.py` renders everything per frame at fixed 1080×1920 coordinates — every builder (note+title, bullets window,
  lower thirds, Day chips, CTA pill, why card, title card, lock screen, phone mockups) needs a 1080×1080 geometry;
  make `W,H` module constants and re-derive positions from them rather than editing numbers in place.
* [A7] traps that carry over: odd-width frames shear (keep every media size even); `-ss` seeks land wrong on these
  masters — extract by frame index; the plate/overlay caches settle on their last element.
* The app recording's result screen (his goal image alone) → AI-GENERATED chip stays; the stranger's before picture
  in the app demo is an editor-side issue (lesson 40), not fixed here.
* Cutdown: `cut_plan.json` from the vertical, frame for frame; mux with `cut/his_mix.wav`.

## Deliver

`… \| claude \| 1x1 \| ad 5.mp4` + `… \| claude \| 1x1 59s \| ad 5.mp4` via a `deliver5.py` variant (`--aspect 1x1`),
review copies, A/B, stamps, `notes-square.md`, `recipe-square/`; shared "After the build" steps; board entry.

## Starter prompt (Fable 5.1, high)

> Execute `Handoffs/handoff-20260911-square-ad5-muhammad.md` after reading
> `Handoffs/handoff-20260911-square-ads-00-shared-rules.md` and `/shortad-from-longform` [A7]: build the 1:1 square of
> Ad 5 from the REVISED vertical build (`/Volumes/Extreme/_edit_work/ad5-vert/` copied to `ad5-sq/`) — same beats,
> pictures and labels as the revised vertical, `g5.py` re-derived for 1080×1080, Muhammad's audio untouched (md5
> asserted), plus the 59 s square from `cut_plan.json`. Every gate, the independent audit, deliver, send Dan the
> review copies. Model: Fable 5.1, effort high.
