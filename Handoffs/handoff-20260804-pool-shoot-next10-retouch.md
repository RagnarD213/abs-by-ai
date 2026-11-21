# Handoff: Retouch the next 10 pool-shoot photos (batch 2)

**Date:** 2026-08-04
**Project:** Abs By AI (Dan's personal brand photos — feeds marketing/being-the-face strategy)
**Business goal this serves:** Marketing (keystone IG/social assets of Dan as the face of the brand)

## Objective

Retouch 10 newly selected photos from the 7-31-26 pool shoot (302 shots, folder `photos/pool shoot | 7-31-26 | dan | mindi/`) to finalized social-ready quality, using the `photo-edit` skill end to end: Nano Banana Pro retouch passes, QC crop strips, the standing bulge-warp rule where the garment calls for it, Dan's approval per photo, then finals + IG 4:5 crops into `photos/finalized photos/`. This is batch 2 — batch 1 (10 photos + the flag photo + a towel-smile lounger shot) is already finalized and Dan was very happy with it ("really, really love what you did").

## Current State

- **Selection is DONE and approved.** Dan reviewed a labeled contact board and said "Good picks." The 10 shots (numbers = `SNAPPR Dan Rose Fitness-<N>.JPG` in the shoot folder):

| # | Shot | Why it was picked | Garment → warp rule |
|---|---|---|---|
| 1 | **17** | Towel wipe by tree, chin up, sunlit abs — editorial post-workout | Snug black square-cut shorts, front visible → **apply warp** |
| 2 | **49** | Med-ball overhead press on lawn, abs elongated, action | Snug black shorts, front visible → **apply warp** |
| 3 | **71** | Seated poolside, natural smile — relatable/Facebook energy | Seated, front not clearly visible → skip or judgment call |
| 4 | **84** | Jump rope mid-air, both feet off ground, rope arc visible | Snug black trunks, front visible → **apply warp** |
| 5 | **138** | Red/gold Muay Thai shorts, hands on hips, big smile — new outfit | Loose Muay Thai shorts → **skip warp** |
| 6 | **149** | Boxing guard in Muay Thai shorts — sharp athletic action | Loose → **skip warp** |
| 7 | **207** | Bolt-style point pose on lawn, smiling — pure personality | Black briefs/speedo-style → **apply warp (standing default)** |
| 8 | **258** | Pool ladder lean, teal shorts, strong ab light + warm smile | Loose teal board shorts → **skip warp** |
| 9 | **289** | Sitting on pool edge, feet in water, laughing — most joyful frame | Loose teal shorts, seated → **skip warp** |
| 10 | **298** | Maroon briefs on waterfall ledge, knee up, relaxed smile | Maroon briefs BUT seated/knee-up — front partly obscured → judgment; offer no-warp variant if unclear |

- **Approved swap options if any pick fails in retouch:** #41 (floor med-ball crunch — on-brand abs, but a shoe dominates foreground) can replace #49; #147 (waterfall sit in red Muay Thai shorts, huge smile) can replace #298. Red outfit was deliberately capped at 2 frames (138, 149) for grid variety — keep that cap if swapping.
- **No retouching has started on these 10.** Batch 1 finals live in `photos/finalized photos/` (`photo-<N>_FINAL_PRIMARY.jpg` naming) — use them as the quality/style reference.
- Selection working artifacts (contact sheets, zoom strips, the approved board `final/next10-board.jpg`) are in this session's scratchpad — disposable, everything needed is in this doc.

## Key Decisions Already Made

- **These 10 exact shots** — chosen for diversity vs batch 1 (batch 1 was heavy on standing physique poses: tree/lawn hands-on-hips, kettlebell squat, dusk flexes, speedo hands-on-hips, in-pool standing). Don't re-run selection.
- **Nano Banana Pro is the only retouch model** — Seedream recomposes the shot, FLUX restyles clothing. Settled by measurement 2026-08-04; do not re-derive.
- **Two body intensities per photo (subtle + strong)** — Dan has always picked strong, but generate both.
- **Warp standing default (Dan's call, 2026-08-04):** always apply the local bulge warp on briefs/speedo-style garments with the front visible — don't ask. Skip on loose shorts. Per-photo calls in the table above.
- **Dan's eyeball is the gate** — deliver candidates + before/after crop strips per photo; recommend one, he decides.
- **Never commit personal photos** — the repo is public; `photos/` is gitignored and must stay that way. This handoff doc is committable; the photos are not.

## Detailed Plan

1. Read the skill: `.claude/skills/photo-edit/SKILL.md` — follow it exactly (prompt recipe, QC, skin-tone seam check, delivery format).
2. Get the Replicate token per the skill's step 2 (Railway → abs-by-ai → Variables → clipboard → `.keys.env` in scratchpad; DLP means Dan must click the copy icon — the secret never enters chat). Verify with GET `/v1/account`.
3. For each of the 10 shots, working in approved-list order (17, 49, 71, 84, 138, 149, 207, 258, 289, 298):
   a. Downscale original to 2048 long-edge JPEG (`sips -Z 2048 -s format jpeg -s formatOptions 90`).
   b. Build the retouch prompt per the skill recipe — face de-shine/smooth + skin-tone-seam lock, ab/oblique sharpening with "do NOT add size," explicit clothing lock naming the exact garment (critical on the Muay Thai shorts — ornate gold trim is exactly the detail nano quietly redesigns), no added tan, single photograph.
   c. Run `node scripts/replicate-edit.js` twice (subtle + strong body intensity), ~$0.13–0.25/take, ~40s each.
   d. QC yourself with before/after crop strips (face + each edited region + garment) — reject identity drift or garment changes silently and re-run.
   e. Apply the warp (`python3 scripts/local-warp.py`) per the table above on the winning candidate (~rx 220–242, ry 190–203, k=0.20 at 4096 long edge; find CX/CY by cropping a zoom first).
   f. Deliver per photo (or in small groups of 2–3): candidates + comparison strips via SendUserFile; recommend one.
   g. On approval: full-res final + IG 4:5 crop → `photos/finalized photos/` as `photo-<N>_FINAL_PRIMARY.jpg` / `photo-<N>_FINAL_PRIMARY-IG-4x5.jpg` (match batch-1 naming). Remove superseded drafts.
4. Batch cost estimate: 10 photos × 2 intensities ≈ 20 nano calls ≈ $3–5 plus a few re-runs — well within normal; no approval needed at that level.
5. OPEN: whether Dan wants a combined "batch 2 grid preview" (all 10 finals tiled) at the end for IG planning — offer it, it's one ffmpeg call.

## Things to Avoid / Lessons Learned

- **Seedream/FLUX for retouching — never** (recompose/restyle; measured).
- **Subtle-intensity passes have come back with LESS ab contrast than the original** — that's why both intensities run but strong usually wins.
- The dedicated face-smoothing pass lightens the face vs neck/chest — always include the skin-tone-seam line in the prompt and check the jawline seam at zoom in QC.
- Nano quietly redesigns garment details (it once changed a waistband style) — clothing lock in every prompt, and QC the garment specifically. Highest risk here: the Muay Thai shorts' embroidery (138, 149) and the neon drawstrings on the teal shorts (258, 289).
- "No images were returned" = the model declined the phrasing — reword the sensitive part in neutral fabric/fit terms and lead with "exact photographic copy with one small adjustment."
- ffmpeg is at `ad-factory/the-upload/node_modules/ffmpeg-static/ffmpeg` (no system ffmpeg); use `-update 1 -frames:v 1` for single-image outputs. `sips -z` (square) distorts — pad with ffmpeg instead when tiling.
- Jump-rope shot #84 has a thin rope arc through the frame — check in QC that the retouch doesn't erase or warp the rope (fine detail near the body edges).

## Relevant Files & Locations

- Originals: `photos/pool shoot | 7-31-26 | dan | mindi/SNAPPR Dan Rose Fitness-<N>.JPG`
- Finals destination + batch-1 reference: `photos/finalized photos/`
- Skill: `.claude/skills/photo-edit/SKILL.md`
- Tools: `scripts/replicate-edit.js`, `scripts/local-warp.py` (both referenced by the skill)
- Token source: Railway → abs-by-ai service → Variables → `REPLICATE_API_TOKEN` (never paste the value into chat)

## Model & Effort Recommendation

This task **requires Claude Code on Dan's Mac** (local files, sips/ffmpeg, the photo-edit skill, SendUserFile delivery) and its core judgment is **visual QC of identity drift on keystone personal photos** — Codex is not a fit regardless of usage.

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | Claude Fable/Opus-tier, standard thinking — matches the model that produced batch 1, and identity/garment QC is the one place a subtler eye pays for itself on keystone assets |
| **If Claude usage is high / approaching a limit** | Claude Sonnet 5, standard thinking — the workflow is fully scripted by the skill; escalate an individual photo to Opus only if its QC keeps failing |

Override note: always-Claude applies here (visual judgment + local skill environment); the choice is only which Claude tier.

## Starter Prompt for the Next Task

> Retouch batch 2 of my pool-shoot photos using the photo-edit skill. The 10 approved shots and all decisions are in `handoff-20260804-pool-shoot-next10-retouch.md` (project root) — read it and `.claude/skills/photo-edit/SKILL.md` first, don't re-run selection. Start with the Replicate token step (I'll click the copy icon in Railway when you have the tab ready), then work through the shots in order: 17, 49, 71, 84, 138, 149, 207, 258, 289, 298. Deliver candidates with before/after strips in groups of 2–3 for my approval; finals go in `photos/finalized photos/` with the same naming as batch 1.
