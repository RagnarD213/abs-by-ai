# Batch 6 — WAVE 4 of 4: gray + white backdrops (15 frames) — CLOSES THE SHOOT

- **Handing off to:** Claude Code (**Opus 5, high effort, fast mode OFF**), fresh session, `/photo-edit`
- **Rewritten 2026-08-31** after wave 3 shipped and was finalized. **This supersedes the earlier
  version, which carried a stale warp strength and an unreconciled pick list.**
- **Canonical recipe:** `photos/finalized social media photos/_recipes/studio-8-27-26-batch6-wave3/MANIFEST.md`
  — read that first, it is current and shorter than the parent doc. Wave 2's folder has the
  originals of `abcomp.py` / `blendabs.py` / `evenskin.py`; wave 1's has `p53max.txt`.
- **Source:** `photos/studio shoot | 8-28-26 | dan | mindi/Portrait Shoot Thu Aug 27/`, filenames
  like ` Snappr Daniel Studio Gray-2.JPG` (⚠ **leading space** — use `while IFS= read -r`).
  Portrait frames are 4672×7008; **G-26 is landscape** 7008×4672.
- **Deliver to:** `photos/finalized social media photos/` as
  `studio-<gray|white>-<n>_FINAL_PRIMARY.jpg` + `-IG-4x5.jpg`.
  **G-26 ships full-frame only, no IG crop** (the blue-66 rule: never clip the subject to force 4:5).

---

## RECONCILIATION — done 2026-08-31, against the delivered library. **All 15 stand.**

Waves 1–3 each needed a reconciliation and each found something. This one was run before the doc
was rewritten, so the executing session does not have to repeat it:

- **All 15 source frames verified present** at the expected dimensions.
- **None is already delivered.** Delivered gray: 4, 12, 30, 38, 41, 48, 55, 67, 79, 87.
  Delivered white: 1, 13, 23, 31, 32, 42, 57, 59, 70, 90, 100, 113. No overlap.
- **The open flag from the "5 more" session is RESOLVED: W-62 does NOT duplicate the delivered
  W-70.** Built side by side: W-62 is front-on with **both** arms behind the head; W-70 is a 3/4
  turn with **one** arm up and the other hand at the hip. Different body angle, different arm count.
  **Keep both.**

**Six adjacency pairs were built and looked at rather than assumed. Two are real risks:**

| pick | delivered neighbour | verdict |
|---|---|---|
| **G-31** | **gray-30** | ⚠ **CLOSEST IN THE WAVE.** Identical white ribbed tank + white trunks, hands on hips, same framing, same backdrop. Differs **only** in expression (G-31 big open smile, gray-30 serious). |
| **W-99** | **white-100** | ⚠ **SECOND CLOSEST.** Identical yellow trunks, both arms behind head, front-on, same framing. Differs **only** in expression (W-99 big smile, white-100 serious). |
| G-9 | gray-12 | Moderate. Same white trunks, same one-arm-behind-head. Smile vs serious. |
| G-2 | gray-4 | Fine. Same garment and register, but arms-at-sides mid-stride vs hands-on-hips, and gray-4 is framed tighter. |
| W-62 | white-70 | Fine — see above. |
| W-2 | white-90 | Fine. Different garment (green retro vs yellow) and different register. |

**Do NOT strike G-31 or W-99 on your own.** Dan reviewed the same class of pair in wave 3 (B-240 vs
the delivered blue-241, glasses/pose/expression all matching) and ruled *"all the adjacent pictures
are different enough"* — he kept every one. **Build the two pairs, ship them, and list them
explicitly in the delivery message** so he can kill either.

**Two library-level crowding notes, neither blocking, both worth one line to Dan at delivery:**
- **Arms-behind-head is 6 of these 15** (G-9, G-26, G-90, W-34, W-62, W-99) on top of the just-
  delivered B-201 and B-275 and the already-delivered white-70 and white-100. It is becoming the
  most-repeated pose in the whole library.
- **G-63 is a fourth red/gold Muay Thai frame** — wave 3 delivered B-269, B-271 and B-275 in that
  exact garment. The pose (boxing guard) and backdrop are new, so it earns its place, but the
  garment is now four deep.

---

## The 15 frames

Garments and poses below were **read off the actual raws on 2026-08-31**, not carried forward.

### Gray backdrop (7)

| # | garment | pose | expression | flags |
|---|---|---|---|---|
| 2 | white cotton trunks | arms at sides, slight mid-stride | big open smile | eye rule likely |
| 9 | white cotton trunks | ONE arm behind head, other at side | big open smile | ⚠adj (gray-12 = serious) · **ARM LOCK** · eye rule likely |
| 21 | white ribbed tank + white trunks | arms at sides | big open smile | **clothed** · eye rule likely |
| 26 | white ribbed tank | both arms behind head | warm smile | **LANDSCAPE — no IG crop** · **clothed** · **ARM LOCK** |
| 31 | white ribbed tank + white trunks | hands on hips | big open smile | ⚠**adj, closest in wave** (gray-30 = serious) · **clothed** |
| 63 | red/gold Muay Thai satin | **boxing guard, fists up** | serious, lowered brow | **no warp** · **TORSO-SCOPE BLOCK** · 4th red-MT frame |
| 90 | green retro (white trim) | both arms behind head | direct gaze, slight smirk | **warp** · **ARM LOCK** |

### White backdrop (8)

| # | garment | pose | expression | flags |
|---|---|---|---|---|
| 2 | green retro (white trim) | hands on hips | serious, direct | **warp** |
| 4 | green retro + glasses | hands on hips | big open smile | **warp** · eye rule likely · 2 frames from W-2 |
| 25 | light-wash jeans + belt + glasses | one hand on hip | big open smile | **no warp** (jeans) · eye rule likely |
| 34 | light-wash jeans + belt | both arms behind head | direct gaze, slight smile | **no warp** (jeans) · **ARM LOCK** |
| 49 | black trunks + glasses | hands on hips | big open smile | **warp** · eye rule likely |
| 62 | black trunks | both arms behind head | big smile | **warp** · **ARM LOCK** · eye rule likely |
| 84 | yellow trunks + glasses | hands on hips | big open smile | **warp at 0.41** · eye rule likely |
| 99 | yellow trunks | both arms behind head | big smile | ⚠**adj** (white-100 = serious) · **warp at 0.41** · **ARM LOCK** · eye rule likely |

⚠ **VERIFY EVERY EXPRESSION FROM A ZOOMED FACE CROP BEFORE WRITING ITS LOCK — AND VERIFY THE
DELIVERED NEIGHBOUR'S TOO.** This table has been wrong once per wave. Wave 1 called a broad
open-teeth smile a "playful closed smile"; wave 2's B-80 was called a "big smile" when his eyes are
nearly shut; **and in wave 3 the errors were on the DELIVERED neighbours** — blue-188 was called a
"closed smirk" and blue-241 "serious" when both are big open smiles, which is exactly what made the
adjacency ranking wrong. Crop each face at ~1750 px tall off the detected head top, build one sheet,
and write the locks from that.

---

## What waves 1–3 settled — do not re-derive any of this

1. **BODY (BALANCED DEFINITION PASS) is canonical.** Single take, straight to `--tier final` (4K).
   No bake-off, no 2K draft. Verify against the calibration table in `/photo-edit`.
2. ⚠ **WARP IS k = 0.34, NOT 0.20.** The earlier version of this doc said 0.20 and that is stale by
   two calibration steps — Dan settled 0.34 on 2026-08-29. **Radii rx 270 / ry 230** worked on every
   frame of waves 2 and 3. Centres from a **burned 200 px coordinate grid, one readable image per
   photo** — colour-mask and connected-component detection both fail on this set.
   `CY ≈ waistband_top + 0.62 × (crotch_notch − waistband_top)`. Apply as a **single warp from the
   pre-warp file**; never invert-and-recompose.
   ⚠ **YELLOW TRUNKS GO TO 0.41.** On 2026-08-31 Dan said *"for all images in the yellow shorts, I
   want you to increase the size of the warp a little bit"* and approved 0.34 → 0.41 on B-187 and
   B-201. His wording is **garment-scoped**, so start **W-84 and W-99 at 0.41** — and say so at
   delivery so he can correct it if he meant only the two frames in front of him.
3. **§4b face composite on EVERY frame**, standing procedure. Wave 3: offsets 0/0, NCC r 0.48–0.62,
   tone gains 0.975–1.066.
   ⚠ **DERIVE THE ELLIPSE, DON'T HAND-READ IT.** Wave 3 added `facelm.swift` (Vision
   `VNDetectFaceLandmarksRequest` → bbox + eyes + outerLips + faceContour + medianLine) and
   `mkell.py`, both in the wave-3 recipe folder. The formula reproduces wave 2's hand-read values and
   is rotation-robust, which matters on a tilted head:
   ```
   eye_mid = midpoint(leftEye, rightEye);  chin = medianLine.maxy;  d = chin − eye_mid_y
   top = eye_mid_y − 0.78*d      bottom = chin + 0.12*d
   cy = (top+bottom)/2           ry = (bottom−top)/2
   cx = 0.5*eye_mid_x + 0.5*outerLips_cx
   rx = max(1.34 * eye_separation, 0.52 * faceContour_width)
   ```
   `mkell.py` draws the ellipse on the image and writes `ellcheck.jpg` — **look at it before
   compositing**, that check costs one image and catches a whole class of error.
4. **Histogram tone-match to the original on every frame** (`tonematch.py`). Wave 3 landed tan
   residuals 0.21–0.98. **Check the HAIR R-bias on the orig|raw|toned strip, not just the tan** —
   drift stayed within −3.7 to +0.5; the `blue-213` maroon failure was +12.7 and positive.
5. **Big-smile eye rule** at **1.04 / 1.13** (`eye-restore.py`), judged **per photo** from a zoomed
   crop, never per batch. Wave 3 used it on 7 of 11 and skipped 4 that already read open.
6. **Mole / ear-stud / necklace check at zoom.** He wears a fine silver rope chain in most frames.
   ⚠ **The gray-41 lesson belongs to THIS wave: nano deleted an ear stud and a raised skin tag
   through the mole-lock on a GRAY frame.** Check ears and marks at zoom against the original on
   every gray frame; fix deterministically by compositing original pixels, never by re-rolling.
7. **IG 4:5 = full width 3368×4210**, y-offset = measured head top − 220. Head detector = dark hair
   in the central 50 % of columns, threshold *(median luminance of the top 2 % of rows) − 42*.
8. **Clothed frames (G-21, G-26, G-31): scope the definition block to visible skin only.**
9. **White-backdrop repaint trap:** nano has repainted white seamless into gray mottling. Keep the
   BACKGROUND LOCK clause and check wall std-dev deltas orig-vs-final on all 8 white frames
   (within ±0.55 passed with no composite needed on the last two batches).

---

## ⚠ RUN THE GEOMETRY GUARD FIRST, BEFORE ANY OTHER QC

**In wave 3 it caught 2 of 11 frames coming back structurally wrong, in two different ways, and
nothing else would have seen either.** Nine frames sat in a 4.02–5.43 aligned-512 mean-diff band:

- **B-173 read 22.70 — silently RE-POSED.** Hands taken out of the pockets, arms hanging at his
  sides, the frame zoomed in, and the belt buckle redesigned. A plausible photograph of Dan.
- **B-271 read 15.50 — INFLATED.** Shoulders, delts, lats, arms and chest all pushed outward, with a
  **33.7 tan shift**. Elevated mean-diff **plus** a tan shift the histogram match cannot pull back is
  the signature of a structural change rather than a palette one.

Compute aspect delta and aligned mean-diff on all 15 before anything else, and treat any frame
outside the sibling band as guilty until inspected.

**Then use the DIFF MAP to adjudicate, never an edge scan.** Amplify `|orig − final|` ×6 and look.
A clean retouch shows a uniform **1–2 px hairline** with the change concentrated in the abs interior;
a real widening draws a **thick, TWO-SIDED band** around the whole silhouette. Wave 2 had three
separate silhouette metrics flag phantom inflation and **all were false** (their tell: one edge moves
76–133 px while the opposite edge is pinned to 1–3 px). The diff map also positively confirms a scope
block — on an ARM LOCK frame the arms come out visibly **dark**.

**The two re-roll recipes, and they are different in kind:**
- **A RE-POSE needs the POSE spelled out.** Lead with the named failures enumerated, then describe
  the pose **limb by limb** (which hand, where, thumb outside/fingers inside, elbows at the sides)
  and pin the framing to a stated head-to-frame proportion. B-173: 22.70 → **7.44**, first try.
- **AN INFLATION needs the OUTLINE spelled out.** Lead with the one failure, then convert the
  SILHOUETTE LOCK into an **outline trace**: enumerate every edge — outer deltoid, upper arm,
  forearm, lat, widest chest, waist, hips, thighs, head, neck — and require each at the same pixel
  position. B-271: 15.50 → **6.86**, first try.
- Escalating adjectives fixes neither. Prompts for both are in the wave-3 recipe folder
  (`prompts/p173r2.txt`, `prompts/p271r2.txt`).

**Guards applied pre-emptively are free and they work.** Wave 3's ARM LOCK went into B-201 and B-275
from the first take and both landed in band; neither of the two failures was on a flagged-risk pose.
**This wave has six arms-behind-head frames and one boxing guard — put ARM LOCK on all six and the
TORSO-SCOPE BLOCK on G-63 from take one.**

---

## ⚠ Traps that cost time in waves 2–3

- **The Google-direct endpoint can be down.** Wave 3's revision round hit **HTTP 503 "high demand"**
  on all four renders and kept returning it through four retries each with backoff.
  **`replicate-edit.js --model google/nano-banana-pro --resolution 4K --env ~/.absbyai-secrets.env`
  succeeded on all four first try — same model, independent path.** Try it before concluding a
  prompt was refused. ⚠ It returns **2747×4096**, not Google's 3368×5056, and its aspect is 0.7 %
  off the input's; a face composite absorbs that inside the feather, but a **whole-frame delivery
  from that path would need a re-crop**.
- **`sips -Z N` sets the LONG edge.** On a portrait frame that is the HEIGHT, so a 3368×5056 file
  becomes **1364×2048**, not 2048 wide. Any fraction divided by "2048 as width" is silently wrong.
  Read the real dimensions back with `Image.open(...).size`.
- **Shell env does not persist between Bash calls.** A `SP=...` set in one call is empty in the next,
  and a runner invoked with an empty path fails in a way that looks like a model refusal.
- **If Dan asks to change an EXPRESSION, invert §4b** (lesson 40): render the new expression from the
  **current approved final**, then composite the **candidate's face INTO the approved frame** through
  a tightened ellipse (**rx ×0.90, ry ×0.88, cy +0.004H**). Measured max **4–6 levels outside the
  face ellipse**, so any warp already applied is provably untouched. Diagnose the expression in
  **nameable parts** first and lock anything that is POSE (a raised chin, an averted gaze) separately.
  ⚠ **For a SMIRK specifically: the asymmetry that reads as a smirk lives in the MOUTH and CHEEK
  only. Do NOT also ask for a raised eyebrow** — wave 3 did, and Dan rejected that variant with
  *"I don't like the weird eyebrow raise."*
  ⚠ **And a serious frame is not automatically a frown to be fixed.** The identical smirk treatment
  improved B-221 and made B-271 worse; Dan kept B-271's original. Ask per photo.
- **A smile reads as an optical re-pose.** Four good expression renders *looked* like the head had
  been enlarged; landmarks said head scale was within −1.8 % to +2.7 %, eye-centre shift 0–10 px,
  tilt under 2°. **Measure eye separation, eye-centre and eye-line tilt before rejecting.**

---

## Before editing

1. Stage a `picks.txt` in your scratchpad claiming exactly these 15 frames.
2. **Re-scan every other scratchpad's `picks.txt` AND the delivered folder** —
   `find <scratchpad root> -name picks.txt`. Zero overlap required before the first edit.
3. **Take an md5 baseline of the whole delivery folder, and re-check it immediately before you
   write** (lesson 33 — stage, then re-check, then write; a concurrent session overwrote an approved
   final once and only md5 caught it). Re-check again at the end.
   ⚠ Files from **other shoots** have appeared in that folder mid-session (`photo-29_FINAL_PRIMARY.jpg`
   turned up during wave 3's revision round). A changed count is not by itself a collision — compare
   md5s, not counts.

## Budget

**15 × $0.24 ≈ $3.60**, plus re-rolls. Waves 1–3 cost $3.84, $4.08 and ~$4.12 all-in.
**Realistic: $4–5.** State the estimate before the batch run. Well under the $25 session cap, so run
interactively at `--tier final`; do not raise batch mode.

## Delivery

- **Before/after strips in chat, ONE LARGE IMAGE PER PHOTO** — not a contact sheet. Dan asked for
  this explicitly and repeated it. Send in groups of 3–4.
- **Build the G-31 and W-99 adjacency pairs against their delivered neighbours and send those too**,
  with the two crowding notes above.
- Keep pre-rev files in `v1_backup/`; on any revision round keep `rev1_backup/` too.
- Save the recipe **outside the scratchpad** at
  `photos/finalized social media photos/_recipes/studio-8-27-26-batch6-wave4/` — MANIFEST, prompts,
  warp params, face ellipses, crop offsets.
- Update `AI_COORDINATION.md` (re-read it from disk first; edit only your own section).
  ⚠ Another session commits dashboard JSON to `main` frequently — expect a rejected push and use
  `git pull --rebase --autostash`, since the working tree usually carries other sessions' unstaged
  edits that block a plain rebase.
- **Repo is PUBLIC** — re-confirm `photos/` is gitignored and 0 files are tracked under it.

## Dashboard — THIS WAVE CAN FINALLY CHECK THE TASK OFF

`money::Execute handoff: studio batch 6 — retouch the remaining 52 picks (/photo-edit, Opus)` covers
**all four waves and Dan's approval**. Waves 1, 2 and 3 are delivered **and finalized by Dan**
(35 of 49). **Check it off once wave 4 is delivered AND Dan has approved it** — mechanics in the
`/dashboard-tasks` skill (gated endpoints, `X-Dash-Key`, and the `money`-vs-`business` id trap).
If he leaves any wave-4 revision question open, leave it unchecked and say why.
No new dashboard task is needed for this doc.

## When this wave lands

The shoot's full sweep is complete: **85 finished picks today, 100 after wave 4**, out of 496 frames.
Tell Dan that plainly — it is the end of the batch-6 programme, not just another wave.
