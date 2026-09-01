---
name: background-removal
description: Remove the background from finished Abs By AI photos, producing full-resolution transparent PNG cutouts for thumbnails, covers, and composites. Use whenever Dan asks to remove a background, cut him out of a photo, make a transparent PNG, key out a backdrop, build cutouts for thumbnails, or extend the _cutouts folder with newly finalized photos — even if he doesn't say "/background-removal". Retouching the photo itself is /photo-edit; building the thumbnail that USES a cutout is /youtube-packaging or /coverimage.
---

# Background Removal — finished photos to transparent cutouts

Turn finalized photos into full-res RGBA PNGs with the background removed, clean
enough to composite into thumbnails. Validated 2026-08-31 on all three studio
backdrops (blue gradient, gray gradient, white seamless) — armpit gaps,
hands-on-hips holes, glasses rims, and a fine necklace chain all keyed correctly.

**Cost: ~$0.002/image** (Replicate `851-labs/background-remover`, BiRefNet —
31M+ runs, the settled model). A full ~100-photo batch is ~$0.20. State the
estimate before a batch per the standing spend rule, but this never approaches
the cap.

## The pipeline — run `scripts/removebg.py`, don't rebuild it

```
python3 .claude/skills/background-removal/scripts/removebg.py \
    <images...> --out "<delivery>/_cutouts" --sheet
```

What it does, and why each step is the way it is:

1. **Downscale a COPY to 2048 long edge** for the model. BiRefNet works at
   ~1024 internally; sending the 3368x5056 original buys nothing and slows the
   upload. The original is never modified.
2. **Replicate files API -> BiRefNet.** The model's only job is the MASK.
3. **Upscale the ALPHA ONLY back to full res** (LANCZOS) and apply it to the
   **ORIGINAL pixels**. The subject is never re-rendered — no identity
   dice-roll, no loss of an approved retouch. This is the core of the recipe.
4. **Contract the edge 2px** (`MinFilter(5)` + `GaussianBlur(1)`, the
   `--contract 2` default). The studio lights wrap around hair and leave a
   1-2px bright halo — systematic on every frame, worst on the white backdrop.
   2px kills most of it while keeping hair texture; 3px opens tiny pinholes in
   semi-transparent wisps for little extra gain. `--contract 0` gives the raw
   key if a job needs maximum hair detail over a light background.
5. **Save as `<base>_CUTOUT.png`** (input `studio-white-4_FINAL_PRIMARY.jpg`
   -> `studio-white-4_CUTOUT.png`). Skips existing outputs — safe to re-run a
   batch after a partial failure; `--force` rebuilds.

## Delivery conventions

- **Studio finals go to `photos/finalized social media photos/_cutouts/`** —
  sibling of `_recipes/`, one folder, same base names as the finals.
- **`git check-ignore` the output path before finishing** — the repo is PUBLIC
  and these are personal photos. `photos/` is ignored; any new delivery
  location must be verified, not assumed.
- A cutout is derived from a specific final. **If a final is revised, its
  cutout is stale** — regenerate it (the skip logic means you must delete or
  `--force` it). When delivering revised finals in /photo-edit sessions, check
  whether `_cutouts/` holds that frame.

## QC — judge at usage scale, prove at 1:1

`--sheet` writes a per-image QC sheet: original | checker | magenta overview,
plus automatic 1:1 zooms (top-of-head + the densest soft-edge regions, which is
where keying fails: flyaways, enclosed holes, chains, glasses).

- **Magenta is the fringe check** — a leftover backdrop rim reads instantly
  against it. Checker alone hides light fringes.
- **The verdict scale is the USAGE scale.** A 1px halo that's visible at 1:1
  vanishes at thumbnail size. Before rejecting a cutout, composite it at
  ~700px tall on a dark canvas (what a thumbnail actually does) and look.
- The script flags any frame whose subject covers an implausible fraction of
  frame (<10% or >85%) — that's the "model keyed the wrong thing" tell.
- For a big batch, don't build 100 sheets: sheet a sample of ~6 (hardest
  cases: arms up, glasses, landscape frames) plus every flagged frame.

**Stress cases proven to work** (don't re-test these categories): enclosed
background holes (hands on hips, arms behind head), glasses rims and lenses,
fine chain necklaces, black satin garments against dark backdrop bottoms.
**Watch for**: hair flyaways over white (the halo), and any NEW backdrop or
outdoor shots — this recipe is validated on studio seamless only; re-run the
three-frame stress test before trusting it on a new setting.

## Traps (all paid for on 2026-08-31)

1. **`source ~/.absbyai-secrets.env` silently sets NOTHING** — a line in that
   file breaks shell sourcing and `2>/dev/null` hides the error. Grep the key
   out directly (the script does).
2. **Never reconstruct a Replicate version hash from a truncated prefix** —
   fetch `latest_version.id` whole. A guessed hash fails with an unhelpful
   generic error on every prediction.
3. **The model output is the mask, not the deliverable.** Compositing the
   model's own RGBA at 2048 would ship a 2048px cutout and re-encoded pixels.
   Always alpha-upscale onto the original (step 3 above).
4. **Don't "fix" the halo by re-rolling the model** — it's not noise, it's the
   physical light wrap, and every roll has it. The contraction is the fix.
5. **Soft-edge sanity**: a healthy key has ~0.7-1.2% of pixels at intermediate
   alpha (real anti-aliasing + hair). Near-zero means a jagged binary mask;
   several percent means the model was unsure — eyeball that frame's sheet.

## Definition of done

- Cutouts in the delivery folder, full source resolution, RGBA, readable.
- Gitignore verified on the output path.
- QC sheets (sample + flagged) reviewed; sheets for anything borderline sent
  to Dan in chat with the thumbnail-scale composite so he judges at usage size.
- Coordination file updated; nothing checked off on the dashboard unless a
  task row covers the batch.
