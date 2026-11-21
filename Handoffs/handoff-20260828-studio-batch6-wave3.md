# Batch 6 — WAVE 3 of 4: blue backdrop, jeans + yellow + green + olive + red Muay Thai (11 frames)

- **Handing off to:** Claude Code (**Opus 5, high effort, fast mode OFF**), fresh session, `/photo-edit`
- **Rewritten 2026-08-30** after wave 2 shipped, with the reconciliation applied and everything
  waves 1–2 learned folded in. **This supersedes the 13-frame version.**
- **Parent doc:** `handoff-20260828-studio-batch6-remaining-52-picks.md` — its "How to run it"
  section is the recipe. **The canonical recipe is now the wave-2 MANIFEST** (see below); read that
  first, it is shorter and current.
- **Source:** `photos/studio shoot | 8-28-26 | dan | mindi/Portrait Shoot Thu Aug 27/`, filenames
  like ` Snappr Daniel Studio Blue-169.JPG` (⚠ **leading space** — use `while IFS= read -r`).
  Portrait frames are 4672×7008; **B-275 is landscape** 7008×4672.
- **Deliver to:** `photos/finalized social media photos/` as `studio-blue-<n>_FINAL_PRIMARY.jpg`
  + `-IG-4x5.jpg`. **B-275 ships full-frame only, no IG crop** (blue-66 rule: never clip the subject
  to force 4:5).
- **Prior art to copy, not re-derive:**
  `photos/finalized social media photos/_recipes/studio-8-27-26-batch6-wave2/` — MANIFEST.md (the
  full pipeline + rev-1 findings), all 12 wave-2 prompts, `rev1-prompts/` (the harder-abs and the two
  expression prompts), `abcomp.py`, `warpparams.tsv`, `faceell.json`, `igcrop.json`.
  Wave 1's folder (`…-wave1/`) has `evenskin.py`, `blendabs.py`, `p53max.txt`.

## ⚠ RECONCILIATION — THIS WAVE IS 11 FRAMES, NOT 13. Both strikes are verified, not assumed.

- **B-266 STRUCK — already delivered.** `studio-blue-266_FINAL_PRIMARY.jpg` exists on disk (shipped
  in the "5 more" batch, 2026-08-28/29, and finalized by Dan). Do not re-edit it.
- **B-212 DROPPED — it duplicates the delivered B-213.** Verified side by side this session: same
  plain green shorts, same glasses, same hands-on-hips front-on pose, same big open smile. Shipping
  both would be a visible duplicate in the grid.

## The 11 frames

Garments and framing below were **read off the actual raws on 2026-08-30**, not copied forward —
the previous version of this table called B-221 "green retro", which is wrong.

| # | garment | pose | expression | flags |
|---|---|---|---|---|
| 169 | light-wash blue jeans + glasses | hands on hips | big open smile | ⚠adj-2 (delivered 171 = smirk) · **no warp** · eye rule likely |
| 173 | light-wash blue jeans | thumb in pocket | open laugh, head tilt | ⚠adj-2 (delivered 175 = wink) · **no warp** · eye rule likely |
| 187 | bright yellow trunks + glasses | hands on hips | big open smile | ⚠adj (delivered 188 = closed smirk) · **warp** · eye rule likely |
| 201 | bright yellow trunks | arms behind head | big grin | ⚠adj (delivered 202 = serious) · **warp** · **ARM LOCK** · eye rule likely |
| 221 | **plain green shorts** (NOT the white-trimmed retro) | hands on hips | chin-up serious, gaze off | ⚠adj (delivered 222 = cheeky grin) · **warp** |
| 240 | olive loose shorts + glasses | thumbs in pockets | big smile | ⚠adj (delivered 241 = serious) · **no warp** (loose) |
| 247 | olive loose shorts | thumbs in pockets | big smile, head tilt | **no warp** (loose) |
| 249 | olive loose shorts | hands on hips | warm smile | **no warp** (loose) |
| 269 | red/gold Muay Thai satin | hands on hips | big smile, head tilt | **no warp** (satin) · eye rule likely |
| 271 | red/gold Muay Thai satin | hands on hips | serious | **no warp** (satin) |
| 275 | red/gold Muay Thai satin | arms behind head | direct gaze, slight smirk | **LANDSCAPE** — no IG crop · **no warp** · **ARM LOCK** |

⚠ **VERIFY EVERY EXPRESSION FROM A ZOOMED FACE CROP BEFORE WRITING ITS LOCK.** This table has now
been wrong once per wave: wave 1 called a broad open-teeth smile a "playful closed smile", and
wave 2's B-80 was described as a "big smile" when his eyes are in fact nearly shut (the strongest
squint in that wave). Crop each face at ~0.235 × frame height off the detected head top, build one
sheet, and write the locks from that.

## What waves 1–2 settled — do not re-derive any of this

1. **BODY (BALANCED DEFINITION PASS) is canonical**, single take, straight to `--tier final` (4K).
   No bake-off. Verify against the calibration table in `/photo-edit`, don't re-measure it.
2. **Warp is k=0.34** (Dan settled it 2026-08-29). Centres from a **burned 200 px coordinate grid,
   one image per photo** — colour-mask and connected-component detection both fail on this set, and
   labels do not survive a montage downscale. `CY ≈ waistband_top + 0.62 × (crotch_notch − waistband_top)`.
   Radii **rx 270 / ry 230** worked on every wave-2 frame. Apply as a **single** warp from the
   pre-warp file; never invert-and-recompose.
3. **§4b face composite on EVERY frame** as standing procedure (wave 2: offsets 0/0, NCC r 0.43–0.65,
   tone gains 0.962–1.066). Reuse `facecomp.py` + the ellipse recipe in wave 2's `faceell.json`.
4. **Histogram tone-match to the original on every frame** (`tonematch.py`). Wave 2 landed tan
   residuals **0.3–0.6**. Also check the **hair** R-bias on the orig|raw|toned strip, not just the tan.
5. **Big-smile eye rule** at **1.04 / 1.13** (`eye-restore.py`), judged per photo from a zoomed crop.
   Wave 2 used it on 6 of 12; this wave flags ~5.
6. **Mole / ear-stud / necklace check at zoom.** He wears a fine silver rope chain in most of these.
   **No ear stud exists in this shoot's frames** — the dark spots near the lobes are neck moles.
7. **IG 4:5 = full width 3368×4210**, y-offset = measured head top − 220. Head detector = **dark hair
   in the central 50 % of columns**, threshold *(median luminance of the top 2 % of rows) − 42*.

## Wave-specific notes

- **⚠ THIS IS THE ADJACENT-FRAME WAVE. Five of the eleven sit 1–2 frames from a delivered final in
  the same setup** (169/173/187/201/221/240 against delivered 171/175/188/202/222/241), differing in
  expression. Dan blessed "similar is OK", **but list them explicitly in the delivery message** so he
  can kill any that read too close. Build a side-by-side of each pick against its delivered neighbour
  before editing — that check killed one pick in wave 2 and is cheap.
- **Warp on only 3 of 11** (187, 201, 221). Jeans, olive loose shorts and Muay Thai satin never take
  one — all confirmed standing rules. That makes this the lightest wave for warp work.
- **ARM LOCK from the first take on 201 and 275** (both arms behind head). Wave 2 proved this is free
  and eliminates re-rolls: its three highest-risk poses all landed in band first try *because* the
  guards went in pre-emptively.
- **Glasses on 169, 187, 240** — name them in the prompt ("dark navy rectangular eyeglasses,
  identical in shape, colour and position") and re-check the frame at zoom on any re-roll.
- **B-275 is landscape**: full-frame delivery only, and check whether the warp region is even in
  frame before considering one (it is satin here, so the question is moot — but the rule matters for
  wave 4).
- **Budget: 11 × $0.24 ≈ $2.64**, plus re-rolls. Waves 1–2 cost $3.84 and $4.08 all-in.
  **Realistic: $3–4.** State the estimate before the batch run. Well under the $25 session cap, so
  run interactively at `--tier final` and do not raise batch mode.

## Before editing

1. Stage a `picks.txt` in your scratchpad claiming exactly these 11 frames.
2. **Re-scan every other scratchpad's `picks.txt` AND the delivered folder** for collisions —
   `find <scratchpad root> -name picks.txt`. Zero overlap required before the first edit.
3. **Take an md5 baseline of the whole delivery folder** and diff it again before you finish
   (lesson 33 — a concurrent session overwrote an approved final once, and only md5 caught it).

## ⚠ Traps that cost time in wave 2 — read these, they are not in the skill's older lessons

- **`sips -Z N` sets the LONG edge.** On a portrait frame that is the HEIGHT, so a 3368×5056 file
  becomes **1364×2048**, not 2048 wide. Any fraction divided by "2048 as width" is silently wrong —
  it put wave 2's face ellipses ~190 px off his face. **Read the real dimensions back, and draw the
  ellipse on the image and look at it before compositing.**
- **Silhouette edge scans do not work on this backdrop.** Three separate metrics flagged phantom
  inflation on wave 2 (a bounded-window scan, a gradient-argmax locator, a rim/interior ratio) and
  **all were false** — they trip on slow backdrop-gradient drift and internal muscle shadows.
  **Use the amplified diff map instead:** a real outline move draws a thick one-sided band; a clean
  retouch shows a uniform 1–2 px hairline with the change concentrated in the abs. Tell-tale of a
  false alarm: **one edge moves 76–133 px while the opposite edge is pinned to within 1–3 px.**
- **A "push it harder" re-roll always overshoots somewhere, but not where it did last time.** On the
  guard pose it inflated the ARMS once (blue-266) and the **PECS** the next time (blue-84). The
  remedy generalises even when the location does not: **composite only the region Dan asked about**,
  and dial it with the low band only (`wl`), taking the high band wholly from the approved frame so
  texture is provably preserved.
- **If Dan asks to change an EXPRESSION, invert §4b** — render the new expression from the CURRENT
  APPROVED FINAL, then composite the **candidate's face INTO the approved frame** through a tightened
  ellipse (**rx × 0.90, ry × 0.88**). Identity cannot be repaired the usual way when the face is the
  thing that must change; this removes outline drift by construction (measured max 4–6 levels outside
  the ellipse). Diagnose the expression in **nameable parts** — wave 2's "sad" was *corners turned
  down + inner brows lifted and drawn together + flat lidded eyes* — and lock anything that is POSE
  (a raised chin, an off-camera gaze) separately. Prompts: wave 2's `rev1-prompts/p111a.txt`.
- **A smile reads as an optical re-pose.** Four good expression renders *looked* like the head had
  been enlarged; landmarks said scale was within ±2.4 % and tilt under 2°. **Measure eye separation
  and eye-line tilt before rejecting an expression render.**

## Delivery

- **Before/after strips in chat, ONE LARGE IMAGE PER PHOTO** — not a contact sheet. Dan asked for
  this explicitly on wave 2. Send in groups of 3–4.
- Keep pre-rev files in `v1_backup/`; on any revision round keep `rev1_backup/` too.
- Save the recipe **outside the scratchpad** at
  `photos/finalized social media photos/_recipes/studio-8-27-26-batch6-wave3/` — MANIFEST, prompts,
  warp params, crop offsets. The scratchpad is temporary.
- Update `AI_COORDINATION.md` (re-read it from disk first; edit only your own section).
- **Repo is PUBLIC** — re-confirm `photos/` is gitignored and 0 files are tracked under it.

## Dashboard

**Do NOT check off the batch-6 Key task** (`money::Execute handoff: studio batch 6 — retouch the
remaining 52 picks (/photo-edit, Opus)`). It covers all four waves *and* Dan's approval. After
wave 3 the count is **35 of 49 delivered** (the batch is 49, not 52, after B-266 and B-212 were
struck and one wave-2 duplicate check). Wave 4 closes it.
No new dashboard task is needed for this doc — the existing Key task already covers it.

## ⚠ One open item Dan may raise

**60 conflict copies (`<name> 2.jpg`) are sitting in the delivery folder** — 30 photos × 2 files,
exactly the set the warp-bump session touched. They are **not duplicates**: they differ by
0.36–1.14 % of frame and are the pre-warp-bump / pre-vein-fix versions, left by a sync conflict when
three sessions wrote the same files on 8/28. One click from being the file that gets uploaded.
Left in place deliberately — deleting them is Dan's call. If he says go, `ls *" 2.jpg"` lists them.
