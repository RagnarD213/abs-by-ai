# Batch 6 — WAVE 4 of 4: gray + white backdrops (15 frames) — closes the shoot

- **Handing off to:** Claude Code (**Opus 5, high effort**), fresh session, `/photo-edit`
- **Parent doc:** `handoff-20260828-studio-batch6-remaining-52-picks.md` — **read its "How to run
  it" section first; it is the recipe.** This doc adds only what is specific to wave 4.
- **Source:** `photos/studio shoot | 8-28-26 | dan | mindi/Portrait Shoot Thu Aug 27/`, filenames
  like ` Snappr Daniel Studio Gray-2.JPG` / ` Snappr Daniel Studio White-2.JPG` (⚠ leading space).
  Source frames are 4672×7008 (landscape ones 7008×4672).
- **Deliver to:** `photos/finalized social media photos/` as `studio-<gray|white>-<n>_FINAL_PRIMARY.jpg`
  + `-IG-4x5.jpg` (portrait frames only).

## Before editing

1. Stage a `picks.txt` in your scratchpad claiming exactly these 15 frames.
2. Re-scan other scratchpads' `picks.txt` AND the delivered folder — waves 1–3 (blue) may already be
   delivered; a concurrent session may have added more. Zero overlap required before the first edit.

## The 15 frames

### Gray backdrop (7)

| # | garment | pose | expression | flags |
|---|---|---|---|---|
| 2 | white cotton shorts | arms at sides, mid-stride stance | big open smile | eye rule likely |
| 9 | white cotton | one-arm-behind-head stretch | warm big smile | smiling variant of delivered G-12 (serious) |
| 21 | white tank + shorts | arms at sides | open laugh | clothed · eye rule likely |
| 26 | white tank | arms behind head | warm smile | **LANDSCAPE** — full-frame only · clothed |
| 31 | white tank | hands on hips | big smile | ⚠adj (delivered G-30 = serious) · clothed |
| 63 | red Muay Thai | boxing guard | serious, lowered brow | no warp · **new pose family** · overshoot watch |
| 90 | green retro | arms behind head | smirk, direct | |

### White backdrop (8)

| # | garment | pose | expression | flags |
|---|---|---|---|---|
| 2 | green retro | hands on hips | serious | (delivered W-1 is a different garment — unrelated) |
| 4 | green retro + glasses | hands on hips | big open smile | eye rule likely |
| 25 | jeans + glasses | hand on hip | big open smile | no warp · eye rule likely |
| 34 | jeans | arms behind head | direct gaze, slight smile | no warp |
| 49 | black trunks + glasses | hands on hips | big open smile | eye rule likely |
| 62 | black trunks | arms behind head | big smile | eye rule likely |
| 84 | yellow trunks + glasses | hands at hips | big open smile | eye rule likely |
| 99 | yellow | arms behind head | big smile | ⚠adj (delivered W-100 = serious) · eye rule likely |

## Wave-specific notes

- **White-backdrop trap (documented):** nano has repainted the white seamless into gray mottling
  before. Keep the BACKGROUND LOCK clause in, and check wall std-dev deltas orig-vs-final on every
  white frame (batch-3/4 recipe: within ±0.55 passed with no composite needed).
- **Gray-41 lesson applies to this wave's gray frames:** nano deleted an **ear stud** and a raised
  skin tag through the mole-lock. Check ears/marks at zoom against the original on every frame; fix
  deterministically by compositing original pixels, never by re-rolling.
- **Clothed tank frames (G-21/26/31):** hard-block scoped to visible skin only.
- **Warp:** green retro / black trunks / yellow / white cotton warp-eligible at k=0.20; jeans and
  satin never; skip G-26 (landscape) if the frame edge cuts the body.
- **Overshoot watch on G-63 (guard pose):** blue-66 recipe if it comes back a bodybuilder.
- **Budget:** 15 × $0.24 ≈ **$3.60** + re-rolls.
- **Delivery:** before/after strips in chat, `v1_backup/`, update `AI_COORDINATION.md`.
- **This wave closes batch 6.** After delivery, remind Dan the shoot's full sweep is complete
  (45 + 52 = 97 finals). **Check off the dashboard Key task
  (`money::Execute handoff: studio batch 6 — retouch the remaining 52 picks (/photo-edit, Opus)`)
  only when Dan has approved all four waves** — mechanics in `/dashboard-tasks`. If earlier waves
  have unresolved revision questions, leave it unchecked and say why.
