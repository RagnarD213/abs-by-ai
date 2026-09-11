# Handoff — Ad 3 "Stop Paying Human Trainers" (Muhammad) — SQUARE 1:1 version

**Written 2026-09-11. Fire FIFTH — two blockers first: (1) Muhammad re-exports Ad 3 so the HD matches the approved
round-5 draft, and (2) the Ad 3 vertical (in progress 09-11, `ad3-vert/`) is delivered and approved by Dan.** Read
`Handoffs/handoff-20260911-square-ads-00-shared-rules.md` first, then this doc, then `/shortad-from-longform`
(Step 0b and **[A7]**).

## ⚠ The HD on disk is NOT the approved cut

`Muhammad Ad Videos/stop paying human trainers - ad 3/stop paying human trainers | muhammad | 16x9 | ad 3.mp4` (his v6 HD,
1920×1080, 29.97, **7,948 frames, 4:25.2**) lost text at 2:14.1–2:23.1: the "Because even though I was a personal
trainer…" bullet is missing "back in my 20s, as a 38 year old dad running a successful ad agency." (proof
`ad3-vert/hdcheck/w4_hd_vs_draft.png`, sent to Dan 09-11 14:38). **It was nevertheless uploaded as `QWW1oumpNg4` and put
in the Demand Gen campaign on 09-11** (ad groups `199782847163` /start + `199360345839` home) — the executing session
should check whether that video has since been replaced; if not, flag it on the board again. The vertical rebuilds that
graphic with the full text, so the square (built from the vertical) carries the correct text regardless.

## What exists

| | |
|---|---|
| vertical | being built in `/Volumes/Extreme/_edit_work/ad3-vert/` (a7 pipeline: `beats.py`, `g3.py`, `edl_*.json`, `fit.json`, `crop.json`, `cut_plan.json`, `deliver3.py`). **Do not enter while its session is live**; copy to `ad3-sq/` after delivery + approval. |
| audio | **Muhammad's, untouched** — but from WHICH export: if he delivers a corrected HD, its mix is the one to carry (verify by `hd_vs_draft.py` VERDICT IDENTICAL against the approved draft first, and re-check the vertical was muxed from the same export) |
| raw roll | C1593 (8/14 shoot) |
| YouTube / Ads | 16:9 `QWW1oumpNg4` (see the warning), thumbnail gray-87; Demand Gen ad groups above |

## Ad 3 specifics

* The "what a trainer costs / what the AI trainer does" bullets → stacked family; the AI Trainer app recording
  (portrait) → side-by-side; real after pictures → shared rule 4 with the real-picture chip.
* The 2:14 bullet must carry the FULL sentence (the vertical's version) — add it to the audit prompt explicitly.
* Carry every Dan-instructed deviation recorded in the vertical's `notes-vertical.md`.

## Deliver

`… \| claude \| 1x1 \| ad 3.mp4` + `… \| claude \| 1x1 59s \| ad 3.mp4` in the Ad 3 folder, review copies, A/B, stamps,
`notes-square.md`, `recipe-square/`; shared "After the build" steps; board entry.

## Starter prompt (Fable 5.1, high)

> Execute `Handoffs/handoff-20260911-square-ad3-muhammad.md` after reading
> `Handoffs/handoff-20260911-square-ads-00-shared-rules.md` and `/shortad-from-longform`: first confirm Muhammad's
> corrected Ad 3 HD is IDENTICAL to the approved draft (`hd_vs_draft.py`) and that the vertical in
> `/Volumes/Extreme/_edit_work/ad3-vert/` is delivered and approved; then build the 1:1 square from that vertical build
> (copied to `ad3-sq/`) — same EDL, beats, pictures, labels and the full 2:14 bullet text, geometry for 1080×1080,
> Muhammad's audio untouched (md5 asserted), plus the ≤0:59 square from `cut_plan.json`. Every gate, the independent
> audit, deliver, send Dan the review copies. Model: Fable 5.1, effort high.
