# Batch 6 — WAVE 2 of 4: blue backdrop, Muay Thai + white cotton + tank + heather gray (12 frames)

- **Handing off to:** Claude Code (**Opus 5, high effort**), fresh session, `/photo-edit`
- **Parent doc:** `handoff-20260828-studio-batch6-remaining-52-picks.md` — **read its "How to run
  it" section first; it is the recipe.** This doc adds only what is specific to wave 2.
- **Source:** `photos/studio shoot | 8-28-26 | dan | mindi/Portrait Shoot Thu Aug 27/`, filenames
  like ` Snappr Daniel Studio Blue-72.JPG` (⚠ leading space). Source frames are 4672×7008.
- **Deliver to:** `photos/finalized social media photos/` as `studio-blue-<n>_FINAL_PRIMARY.jpg`
  + `-IG-4x5.jpg`.

## Before editing

1. Stage a `picks.txt` in your scratchpad claiming exactly these 12 frames.
2. Re-scan other scratchpads' `picks.txt` AND the delivered folder — wave 1 (blue 5/6/9/10/14/22/
   28/33/34/43/53/63) may already be delivered; a concurrent session may have added more. Zero
   overlap required before the first edit.

## The 12 frames

| # | garment | pose | expression | flags |
|---|---|---|---|---|
| 72 | black/gold Muay Thai satin | hands on hips | serious | no warp (satin) |
| 76 | black/gold Muay Thai | tight waist-up, arms flexed at hips | big grin | no warp · overshoot watch · eye rule likely |
| 80 | black/gold Muay Thai | arms behind head | big smile | no warp · eye rule likely |
| 84 | black/gold Muay Thai | boxing guard, fists up | serious | no warp · **new pose family** · overshoot watch |
| 100 | white cotton shorts + glasses | hands on hips | big open smile | eye rule likely |
| 111 | white cotton | hand tucked in waistband | serious | check warp vs hand position |
| 127 | white cotton | arms relaxed at sides | warm big smile | |
| 132 | white tank + shorts + glasses | hand on hip | head-tilt closed smile | clothed — scope body pass to visible skin (blue-137 recipe) |
| 135 | white tank | hand on hip | chin-up serious, gaze off | clothed — same scoping |
| 139 | heather-gray trunks + glasses | hands on hips | warm smirk | |
| 150 | heather-gray | thumb in waistband | big smile | eye rule likely |
| 164 | heather-gray | arms relaxed | big laugh, squinty | eye rule likely |

## Wave-specific notes

- **Overshoot watch on B-76 (flexed arms) and B-84 (boxing guard):** these are the poses most likely
  to trip nano's "bodybuilding photo" reading (blue-66 lesson). If a take comes back tanned/oiled/
  shredded, re-roll leading with the named-failure context + absolute tan/oil lock. Remember the
  whole-frame tan residual LIES on body-local tan — eyeball the orig|toned strip.
- **Warp: k=0.34, NOT 0.20 — Dan settled this on 2026-08-29 after seeing wave 1 at 0.20, 0.27 and
  0.34 side by side.** White cotton and heather gray are eligible; Muay Thai satin never; B-111's
  tucked hand may block a clean warp — skip rather than distort. Apply it as a **single** warp from
  the pre-warp file; never invert-and-recompose an existing one (see the collision note below).
- **Clothed frames (132/135):** hard-block scoped to visible skin only, per the delivered blue-137.
- **Budget:** 12 × $0.24 ≈ **$2.90** + re-rolls. Wave 1 actually cost **$3.84** for 12 (2 pose/framing
  re-rolls + 2 extra renders on one frame Dan wanted harder), so budget ~**$4**.
- **Delivery:** before/after strips in chat, `v1_backup/`, update `AI_COORDINATION.md`.
- **Dashboard:** do NOT check off the batch-6 Key task — it covers all four waves and Dan's approval.

---

# ⚠ READ THIS FIRST — WHAT WAVE 1 CHANGED (executed 2026-08-28/29, all 12 approved)

Wave 1's full recipe, prompts and tools are saved **outside the scratchpads** at
`photos/finalized social media photos/_recipes/studio-8-27-26-batch6-wave1/`
(MANIFEST.md, warp-params.tsv, prompts/, evenskin.py, blendabs.py). **Copy the two .py tools into
your scratchpad and reuse them — do not rewrite them.**

### 1. Warp is k=0.34. The 0.20 in the parent doc is superseded.
Dan reviewed 0.20 / 0.27 / 0.34 built from clean sources and chose **0.34**. All 30 previously
finalized picks were bumped to it by a separate session. Centres still come from a **burned
coordinate grid** — colour-masking the garment fails on this set, and a connected-component version
failed too (it returned garment widths of 136–2150 px). Burn the grid at 200 px with ~34 pt labels,
**one image per photo**; a montage downscales the labels into illegibility.

### 2. NEW TOOL — `evenskin.py`. Expect to need it; Dan flagged this unprompted on 3 of 12.
He rejected a "different colour" band on three frames ("the middle tab is a different color than the
top and the bottom"). **The banding is in the ORIGINAL and the definition pass widens it** — measured
torso tan spread orig→delivered 13.2→15.1, 5.8→7.5, 10.7→11.1. The whole-frame histogram tone-match
cannot fix it: the match is already correct globally, the error is local.

**The fix, and why it is safe:** ab definition is broad **LUMA** shading; tan banding is broad
**CHROMA** at the same spatial scale. Per-channel/luma ratios separate them, so the colour flattens
with the definition provably untouched (**measured luma shift mean 0.0000**). Free, local, no
identity roll. Usage:
`evenskin.py in.jpg out.jpg CX TOPFRAC BOTFRAC HALFW ALPHA` — CX = the warp centre, alpha **1.0**,
clip [0.88, 1.13] (that is `evenskin10.py`).
**How to spot it:** build a low-frequency tan heat-map (GaussianBlur 70, R−B, skin only, percentile-
normalised) — the band shows as a cool/purple region inside a warm torso. ⚠ **The band-spread number
is noisy and self-contradicting; judge on the map and the photo.**

### 3. TWO OF TWELVE CAME BACK STRUCTURALLY WRONG, AND ONLY THE GEOMETRY GUARD SAW IT.
`blue-28` was **silently re-posed** (side-lean + arm behind head → generic front-on, arms down) — it
looked like a perfectly good photo of Dan; the **mean-diff of 32.66 against a 3.4–8.7 sibling band**
is what caught it. `blue-22` was **re-cropped to a different aspect ratio** (1.50 → 1.79).
**Run both checks on every frame before any other QC:** aspect delta, and mean-diff on aligned 512px
downsamples. Both re-rolls succeeded by **leading with the named failure and then describing the pose
limb by limb** — `prompts/p22r.txt` and `p28r.txt` in the recipe folder are those prompts.
**Wave 2 is higher risk here than wave 1: B-84 (boxing guard), B-80 (arms behind head) and B-76
(flexed) are all complex asymmetric poses.**

### 4. B-84 IS A BOXING GUARD — USE THE TORSO-SCOPE FIX, NOT A STRONGER WARNING.
The skill's lesson 17 (`blue-266`) is directly on point and was learned the expensive way: naming the
arm-inflation failure did NOT stop it; **re-scoping the edit did.** Declare the arms untouchable and
name the only region that may change ("the front of his torso, bounded by his collarbones, the
waistband and the outer edges of his ribcage"). Wave 1 put a lighter **ARM LOCK** on its four
arms-up frames pre-emptively and measured no inflation, so include it from the first take.

### 5. VERIFY THE EXPRESSION TABLE ABOVE FROM ZOOMED FACE CROPS — IT HAD AN ERROR IN WAVE 1.
The wave-1 table called blue-9 a "playful closed smile"; it is a **broad OPEN smile with upper teeth
showing**. Written from a thumbnail, the model executes the wrong description faithfully. Crop each
face at ~0.235 × frame height off the detected head top and write the lock from that.

### 6. Standing steps that ran on all 12 and should again.
§4b **face composite on every frame** (wave 1: offsets 0/0, NCC r 0.46–0.77, tone gains 0.985–1.061 —
all inside the clip) · histogram tone-match (tan residuals landed **0.4–0.6**) · **eye pass at
1.04/1.13** on the big-smile frames (7 of 12 in wave 1; wave 2 flags 5) · mole / **ear-stud** /
necklace check at zoom — Dan wears a thin chain in many of these and there is a stud in his left ear.
⚠ **Vision's landmark eye height under-reports badly** — it read **−9.3%** on a frame the crop shows
is clearly more open. Coordinates from landmarks; verdict from the zoomed crop, always.

### 7. IF A FRAME NEEDS REAL HARDNESS, RE-GENERATE — DO NOT KEEP BLENDING.
Dan twice said blue-53's abs were not defined enough. Blending further toward the hard endpoint was
**exhausted** (t=0.55 / 1.00 / 1.35 were visually near-identical) because that frame's hard render was
barely stronger than its balanced one. A new **MAXIMUM DEFINITION** block — which opens by naming the
prior under-shoots as the failure to avoid — took fine ab detail **3.54 → 5.52**. Reuse
`prompts/p53max.txt`. `blendabs.py` is still the right tool for a *small* dial between two existing
renders (low band only, registered on the ab region).

### 8. ⚠ CONCURRENT SESSIONS ARE WRITING THESE SAME FILES. MEASURE, NEVER ASSUME.
During wave 1 another session bumped warps across the finalized picks and **its baseline assumption was
wrong**, compounding five frames to 0.34 while reporting 0.27. Two rules from that:
- **To learn a file's warp strength, rebuild it from its true pre-warp base at several k and diff
  inside the ellipse — the exact 0.000 is the answer.** Do not trust a recorded k.
- **The pre-warp base is not always the obvious one** — after `evenskin.py` or an ab blend, the
  correct base is the evened/blended file, not the plain retouch.
That session was **not reachable via SendMessage/ListAgents**, so `AI_COORDINATION.md` is the channel.
Before delivering, re-check the delivered folder for frames that changed under you.

### 9. Warp skip rules confirmed in wave 1.
Skip on **landscape frames whose front is cropped at the frame edge**, and on **3/4 turns showing hip
rather than front** — a test warp on such a frame measured **invisible**, which is the evidence for
the skip rather than a bare judgement call. Wave 2 has no landscape frames; B-111's tucked hand is
the one to check.
