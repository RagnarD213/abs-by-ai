# Handoff — Ad 2 "Stop Wasting Money on Nutritionists" (Muhammad V2) — SQUARE 1:1 version

**Written 2026-09-11. Fire FIRST of the six square handoffs: nothing blocks it.** Read
`Handoffs/handoff-20260911-square-ads-00-shared-rules.md` first — it holds the rules, gates, naming and the after-build
steps; this doc holds only what is specific to Ad 2. Then `/shortad-from-longform`, especially **[A4]** and **[A5]**
(the two Ad 2 lessons) and Step 7.

## What exists

| | |
|---|---|
| editor final | `Muhammad Ad Videos/stop wasting money on nutritionists - ad 2/stop wasting money on nutritionists \| muhammad \| 16x9 \| ad 2.mp4` — 1920×1080, 29.97, **8,275 frames, 4:36.1** (his V2 HD, Dan's six round-1 notes applied by him) |
| approved vertical | `… \| claude \| 9x16 \| ad 2.mp4` — 8,275 frames = his; **approved by Dan 09-08** ("excellent job"), rev 1 fixed the captions (CTC alignment). `notes-vertical-v2.md` + `recipe-vertical-v2/` beside it |
| build dir | `/Volumes/Extreme/_edit_work/ad2-vert-v2/` — the a4/a5-era pipeline (`build_base.py` → `beats.py` → `render.py` + `vlib.py` → `build_audio.py` → `captions.py`; `qc_ad2v2.py`; `beats_ad2v2.py` is committed in the skill's `reference/`). Copy it to `ad2-sq/`. |
| audio | the vertical carries **his V2 mix with one constant +5.2 dB + limiter → −14.7 LUFS, −1.1 dBTP** (approved 09-08, before the 09-10 untouched rule). **Carry the vertical's AAC stream bit for bit** — Dan approved that sound; do not re-derive it and do not lift further. |
| YouTube / Ads | 16:9 `Dtk5knWM7c8`, vertical `7XgHxn59Tsg`; Demand Gen ad groups "Ad 2" ×2 (start / home) in campaign `24243839443` — Ad 2 took ~80 % of the campaign's spend in its first days, which is why it goes first |
| cutdown | none was delivered for Ad 2's vertical — build the ≤0:59 square only if a `cut_plan.json` exists in the dir; otherwise deliver the full length and note it (a cutdown from Dan's edited script is a separate ask) |

## Ad 2 specifics

* His layout is the text-left / Dan-right window for the bullets ("what a nutritionist actually gives you"), the meal
  photo → macro card demo (`build_meal_clip.py`, the real meal analysis recorded 09-08, $0.03), the goal-image card,
  and the lower thirds. Stacked family for the bullets; **side-by-side for the meal-photo demo** (portrait phone beside
  Dan is exactly his 16:9 arrangement).
* **[A4] centring:** rev 0 of the vertical was rejected on centring — the head-band face track (rule 5/11) is in
  `crop.json`; reuse it, and verify centrelines on the extremes again at 1080 wide (a wider crop hides less).
* Real after pictures in this ad: the ones the vertical shows in cards → rule 4 of the shared doc (side-by-side pairs
  / full-height single), each with the **"Real picture of me — not AI-generated"** chip; the goal image keeps AI-GENERATED.
* Captions: from the rev-1 `words_ctc.json` (Whisper starts ran 128 ms early — never re-time from Whisper).

## Deliver

`… \| claude \| 1x1 \| ad 2.mp4` (+ 59s if built), review copies, stamps, `notes-square.md`, `recipe-square/` in the
Ad 2 folder; the shared doc's "After the build" steps; board entry "Ad 2 square — DELIVERED, Dan reviews".

## Starter prompt (Fable 5.1, high)

> Execute `Handoffs/handoff-20260911-square-ad2-muhammad.md` after reading
> `Handoffs/handoff-20260911-square-ads-00-shared-rules.md` and `/shortad-from-longform`: build the 1:1 square version
> of Ad 2 from the approved vertical build (`/Volumes/Extreme/_edit_work/ad2-vert-v2/` copied to `ad2-sq/`) — same EDL,
> grade, face track, beats and captions, re-laid out for 1080×1080 per the shared rules; the vertical's audio stream
> bit for bit. Every gate on the exact delivered file, the independent audit, then deliver into the Ad 2 folder and
> send Dan the review copy. Model: Fable 5.1, effort high.
