# Handoff — Ad 1 "This Picture Got Me Abs" (Muhammad) — SQUARE 1:1 version

**Written 2026-09-11. Fire SECOND: the vertical is approved, nothing blocks it.** Read
`Handoffs/handoff-20260911-square-ads-00-shared-rules.md` first, then this doc, then `/shortad-from-longform`
**[A3]** and **[A3 rev 1]** (the Ad 1 attempt-3 lessons).

## What exists

| | |
|---|---|
| editor final | `Muhammad Ad Videos/this picture got me abs - ad 1/this picture got me abs \| muhammad \| 16x9 \| ad 1.mp4` — 1920×1080, 29.97, **6,976 frames, 3:52.77** |
| approved vertical | `… \| claude \| 9x16 \| ad 1.mp4` — **6,977 frames (one MORE than his — attempt 3 predates the frame-count assert; the square must land on 6,976 = his, and note the fix)**; approved by Dan 09-10 (`Docs/AD_VIDEO_IDS.md`) |
| build dir | `/Volumes/Extreme/_edit_work/ad1-8-14/vert9x16/` — the original attempt-3 pipeline (`render.py` + `vlib.py`, `beats.py`, `build_audio.py`, `cutdown.py`, `qc.py`); Muhammad's reference at `_edit_work/ad1-8-14/reference/muhammad_final.mp4`. Copy `vert9x16/` to `_edit_work/ad1-sq/`. This is the oldest of the vertical pipelines — no `zcrop`/`zhairgate`; the shared doc's gates still apply, so bring `zhairgate2.py` and `caption_sync_check.py` in from `reference/a7/` and `reference/`. |
| audio | attempt 3 built **our own mix from the lav, EQ-fitted to his** (pre-09-10 rule) and Dan approved it. Default for the square: **the approved vertical's stream bit for bit** (the shared rule). If the frame-count fix shifts the timeline by that one frame, re-cut the SAME stream at the seam rather than rebuilding audio. |
| YouTube / Ads | 16:9 `lf46ytHacss` (also the interim `/start` video), vertical `Iz0u8KHRbyE`; Demand Gen ad groups "Ad 1" ×2 in `24243839443` — Ad 1's ads were "Approved (limited) — CLICKBAIT" on the original copy; the square inherits whatever copy is live, do not touch copy here |
| cutdown | `REVIEW_540p_vertical_59s.mp4` exists in the dir → a `cut_plan`/`cutdown.py` selection exists; rebuild the ≤0:59 square from it |

## Ad 1 specifics

* This ad is the before-photo → AI goal image → real after pictures story: the deckchair before picture, the app
  upload/generate recording (variably retimed, rule 13), the goal image (AI-GENERATED chip), then the real
  photo-shoot afters. **Every real after picture gets the "Real picture of me — not AI-generated" chip** and follows
  rule 4 (side-by-side pairs / full-height single); the vertical predates this label, so the square is the first
  Ad 1 version to carry it — say so in `notes-square.md`.
* The app recording is portrait → **side-by-side family** (Dan left, phone right), his own 16:9 arrangement.
* [A3] lessons that bite again at 1:1: mute b-roll never shows Dan talking (rule 9); SFX at his measured count
  (21 events in 3:53, none on flashes); captions PIL not libass.

## Deliver

`… \| claude \| 1x1 \| ad 1.mp4` + `… \| 1x1 59s \| ad 1.mp4` in `Muhammad Ad Videos/this picture got me abs - ad 1/`,
review copies, stamps, `notes-square.md`, `recipe-square/`; shared "After the build" steps; board entry.

## Starter prompt (Fable 5.1, high)

> Execute `Handoffs/handoff-20260911-square-ad1-muhammad.md` after reading
> `Handoffs/handoff-20260911-square-ads-00-shared-rules.md` and `/shortad-from-longform`: build the 1:1 square of Ad 1
> from the approved attempt-3 vertical build (`/Volumes/Extreme/_edit_work/ad1-8-14/vert9x16/` copied to `ad1-sq/`),
> landing on Muhammad's 6,976 frames, the vertical's audio bit for bit, the real-picture label on every real after
> picture, plus the ≤0:59 square from the existing cut plan. Every gate, the independent audit, deliver, send Dan the
> review copies. Model: Fable 5.1, effort high.
