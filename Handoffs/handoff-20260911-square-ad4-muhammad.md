# Handoff — Ad 4 "Stop Wasting Money on Supplements" (Muhammad V4 HD) — SQUARE 1:1 version

**Written 2026-09-11. Fire FOURTH — AFTER the Ad 4 vertical (in progress in another session on 09-11, build dir
`ad4-vert/`) is delivered AND Dan approves it.** Read `Handoffs/handoff-20260911-square-ads-00-shared-rules.md` first,
then this doc, then `/shortad-from-longform` **[A7]** (the a7 pipeline this vertical uses) and the vertical's own
`notes-vertical.md` once it exists.

## What exists

| | |
|---|---|
| editor final | `Muhammad Ad Videos/stop wasting money on supplements - ad 4/stop wasting money on supplements \| muhammad \| 16x9 \| ad 4.mp4` — 1920×1080, 29.97, **7,160 frames, 3:58.9**; `hd_vs_draft.py` VERDICT IDENTICAL to the approved round-3 draft (0 changed windows, TP −0.9) |
| vertical | being built 2026-09-11 in `/Volumes/Extreme/_edit_work/ad4-vert/` (a7 pipeline, Dan's 09-11 label + full-bleed-portrait rules applied up front). **Do not enter that dir while its session is live**; copy it to `ad4-sq/` only after delivery. |
| audio | **Muhammad's, untouched** (md5-asserted at mux); the cutdown his mix cut at the seams |
| YouTube / Ads | 16:9 `R08TPEtkjuQ` (unlisted, thumbnail white-57); Demand Gen ad groups `202812319169` (/start) + `203842477407` (home) in `24243839443` |
| raw roll | C1594 (8/28 shoot, S-Log3 — memory `shoot-828-slog3-format`) — only needed if a beat has to be re-lifted |

## Ad 4 specifics

* Follow the vertical's `beats.py` beat for beat; the supplement-stack screens (the Supplement Audit photo demo) are
  portrait phone recordings → **side-by-side family**; the bullet screens → stacked; real after pictures → shared rule 4
  with the real-picture chip, the goal image AI-GENERATED.
* Anything the vertical's notes record as a Dan-instructed deviation from Muhammad's layout is carried into the
  square unchanged and re-listed in `notes-square.md`.
* If Dan's review of the vertical adds revisions, apply them to the vertical first (its own handoff), then copy.

## Deliver

`… \| claude \| 1x1 \| ad 4.mp4` + `… \| claude \| 1x1 59s \| ad 4.mp4` in the Ad 4 folder (a `deliver4.py`/`deliver5.py`
variant), review copies, A/B, stamps, `notes-square.md`, `recipe-square/`; shared "After the build" steps; board entry.

## Starter prompt (Fable 5.1, high)

> Execute `Handoffs/handoff-20260911-square-ad4-muhammad.md` after reading
> `Handoffs/handoff-20260911-square-ads-00-shared-rules.md` and `/shortad-from-longform` [A7]: build the 1:1 square of
> Ad 4 from the APPROVED vertical build (`/Volumes/Extreme/_edit_work/ad4-vert/` copied to `ad4-sq/`) — same EDL,
> beats, pictures and labels, geometry re-derived for 1080×1080, Muhammad's audio untouched (md5 asserted), plus the
> ≤0:59 square from its `cut_plan.json`. Every gate, the independent audit, deliver, send Dan the review copies.
> Model: Fable 5.1, effort high.
