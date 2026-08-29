---
name: photo-edit
description: Facetune-style AI retouching and editing of Dan's real personal photos (NOT the Abs By AI product pipeline). Use this skill whenever Dan asks to edit, retouch, touch up, clean up, or "Facetune" a photo of himself — for Instagram, dating apps, social media, or publication — including abs/body definition, face de-shine, wrinkle smoothing, jawline, blemish removal, clothing/bulge tweaks, or picking + polishing the best shots from a photo shoot. Also use it when he pastes/attaches a photo of himself and asks to make it look better in any way.
---

# Photo Edit — Facetune-style retouching of Dan's real photos

Retouch Dan's own photos so he looks like the best version of himself on the same day, in the same photo. The bar: the result must survive being compared to how he looks on video — a slightly imperfect real photo beats a heavy edit that drifts his face or body. These are keystone assets (IG, dating apps), so quality > speed; a full multi-candidate run costs well under $2.

## Non-negotiables

- **Identity is the product.** Same face, same person, recognizably Dan. If a candidate drifts identity, reject it yourself before he ever sees it.
- **Retouch, not re-render.** Same framing, pose, background, clothing, lighting. The model edits the photo; it does not reinterpret it.
- **Never commit personal photos** — the repo is public. `photos/` is gitignored; keep it that way. Finals go in `photos/finalized photos/`.
- **Dan's eyeball is the gate.** Always deliver candidates + before/after crop strips and let him pick. Recommend one, but he decides.
- **Run interactively by default; batch is Dan's call, never yours** — under $10 of interactive spend just run it, over $10 ask first, before editing anything. Full rule in §3b.

## Workflow

### 1. Get the true original

A chat-pasted image is a downscaled copy. Find the full-res original on disk (shoot folders live in `photos/`). To match a pasted photo against a 300-shot folder: `sips -Z 160` thumbnails → force uniform squares (`sips -z 150 150`, ffmpeg's `tile` silently drops frames on mixed sizes) → ffmpeg `tile=13x8` contact sheets → eyeball, then zoom candidates. ffmpeg binary: `ad-factory/the-upload/node_modules/ffmpeg-static/ffmpeg` (no system ffmpeg on this Mac; use `-update 1 -frames:v 1` for single-image outputs).

### 2. Get the Replicate token (no keys live on this machine)

Read `REPLICATE_API_TOKEN` from Railway → abs-by-ai service → Variables. The Chrome-extension DLP blocks secret values from passing through context, so: have Dan open/authorize a Chrome tab, click the row's copy icon, then `pbpaste > <scratchpad>/.keys.env` (as `REPLICATE_API_TOKEN=...`, `chmod 600`) — the secret never enters the conversation. Verify with a GET to `/v1/account` (expect 200).

### 3. Run the retouch — model choice is settled, don't re-derive it

**Nano Banana Pro (`google/nano-banana-pro`) is the only model that retouches in place.** Measured 2026-08-04 on the flag photo: it kept framing/pose/background/identity exactly. **Seedream 4.5 recomposes the entire shot** (new crop, new sky, changed face) — never use it for retouching. **FLUX Kontext restyles clothing.** Run:

```bash
node scripts/replicate-edit.js --image input-2048.jpg --prompt-file prompt.txt --out out/candidate.jpg --env <scratchpad>/.keys.env
```

**Prefer the Google-direct runner in §3a below** — same model, cheaper per take, and the only path with a batch tier. `replicate-edit.js` stays as the fallback (and for Seedream/FLUX comparisons); it needs the Railway token from step 2, the Google runner needs `GEMINI_API_KEY`.

Input: downscale the original to 2048 long-edge JPEG (`sips -Z 2048 -s format jpeg -s formatOptions 90`). ~40s per take. Generate **two body intensities** (subtle + strong) — Dan picks strong nearly every time, and subtle passes have come back with *less* ab contrast than the original. But run both and actually look: on one 2026-08-04 frame the strong pass returned lower global contrast (flatter abs *and* flatter background) and subtle was the better image. Don't assume the winner.

**Prompt recipe that works** (deviate only with reason):
- Open with: "Professional photo retouch of this image for social media. This is a RETOUCH of an existing photograph, not a new image: keep the exact same man, identical face and identity, same pose, same [clothing], same background, same framing, same lighting."
- **FACE block — ASK FOR LESS THAN YOU THINK. This is the settled version (Dan's call, 2026-08-28); do not go back to the old aggressive wording.** The two instructions that used to be in here — *"smooth forehead/under-eye lines"* and *"slightly sharpen the jawline"* — are **structural** asks, and they are what makes nano de-age him: they point it straight at the features that carry his age and identity. Measured, they drifted the face on **10 of 10** studio photos. Ask only for the two *local* fixes and forbid everything else, verbatim:

  > FACE — MINIMAL INTERVENTION, AND THIS IS THE MOST IMPORTANT CONSTRAINT IN THIS PROMPT: change his face as little as possible. The ONLY permitted face changes are (a) reduce hot specular shine and sweat glare on the forehead, nose and cheeks to a natural — NOT matte — finish, and (b) remove small temporary blemishes such as a spot or a scratch. Everything else about the face must be IDENTICAL to the original.
  >
  > FACE — WHAT MUST NOT CHANGE: do NOT smooth, soften, shorten or reduce his forehead lines, frown lines, crow's feet, under-eye lines or nasolabial folds — every one must stay exactly as deep, as long and as visible as in the original. Do NOT sharpen, slim, narrow or reshape the jaw, chin, cheeks or nose. Do NOT reduce skin texture or pores. Do NOT make him look younger, slimmer-faced or more symmetrical. He is a real man in his forties and must still read as exactly that age in the result. MAKING THE FACE LOOK YOUNGER, SMOOTHER OR SLIMMER IS THE SINGLE WORST FAILURE THIS EDIT CAN PRODUCE — worse than leaving a patch of shine or a blemish in place.

  ⚠ **It reduces the drift; it does not end it — this was A/B'd, not assumed.** Re-run against the old block on the two worst drifters: on `Gray-0012` it brought the forehead furrows, cheek structure and moles back and he reads his real age again (face-structure L1 vs the original **0.173 → 0.099**); on `Blue-0202` it restored the lines but **his eye direction still moved** — the original looks away to his left and both versions pull his gaze toward the lens. **So the soft block and the §4b composite are complementary, not alternatives:** soft block first so there is less to repair, then check the face at zoom and composite when anything still moved. Still scope every line to the face explicitly — see the body-sheen rule below for why.
- **Body sheen — say it, every time (Dan's call, 2026-08-04):** the de-shine instruction leaks and nano mattes the *whole body*, killing the wet/sweaty look that is the point of a shoot like this. Dan rejected a full group over it. Always pair the face block with an explicit counter-instruction: "BODY SHEEN — CRITICAL, DO NOT MATTE THE BODY: keep every specular highlight, wet gleam, oily sheen and sweat droplet on his torso, shoulders, arms and legs exactly as bright as in the original. The de-shining applies to the FACE ONLY; from the neck down the skin must remain visibly sweaty and glossy, and if anything the highlights on the abdominal muscles should read slightly crisper."
- **Mole and mark lock:** nano silently deletes moles and beauty marks — measured repeatedly, on the same face, across separate runs. Identity dies by a thousand removed freckles, and it is easy to miss unless you zoom. State it as its own critical block: every mole, freckle and beauty mark on face, neck, chest and body stays in the same place, same size, same darkness; nothing faded or removed; hairline, haircut, ears, eyebrow shape and scars unchanged.
- **Expression lock — name the actual expression, don't just lock it.** A generic "keep his expression identical" reliably fails on mid-action frames: nano closes an open mouth, opens narrowed eyes, and smooths a furrowed brow, turning a real exertion frame into a posed portrait. Describe the literal state and mark both failure directions, e.g. "his LIPS ARE PARTED and his mouth is OPEN mid-breath, eyes narrowed against the sun — a closed mouth is a FAILURE, and a wide round gaping mouth is equally a FAILURE, the opening is small." Overshoot is as common as undershoot, so bound it on both sides.
- **Skin tone match (do this every time a dedicated face-smoothing pass runs on its own):** the face-smoothing pass alone tends to lighten/brighten the face relative to the already-retouched neck/chest, leaving a visible tonal seam at the jawline. Always include: "his face must be the EXACT SAME skin tone, color, and warmth as his neck, chest, and shoulders — no visible tonal break where jaw meets neck." Check this specific seam at zoom in QC, not just identity.
- **Face pallor is SYSTEMATIC, and the in-prompt line above is not enough (Dan's call, 2026-08-06):** on a 10-photo batch the face-smoothing pass made the face visibly whiter/less tan than the body on essentially every photo, even with the skin-tone-match line present, and Dan caught it from the delivered files. Two consequences: (1) QC must include a **face+upper-chest crop of the FINAL at overview scale** (~400px, orig | final side-by-side) — the pallor is obvious there and invisible in tight face-only or seam-only zooms; (2) when it appears, run a dedicated **tone-match pass** on the face output — a single-purpose prompt whose ONLY change is "darken/warm the facial skin so it exactly matches the tan of his neck, chest and shoulders", with expression, mole, body-pixel and brightness locks. That pass fixes it reliably; re-wording the face-A prompt does not. Order: tone-match BEFORE the local warp, so the warp isn't regenerated away.
- BODY block: crisper six-pack separation with natural groove shadow, defined obliques, V-cut at the waistband, tighter waist; sharpen chest/shoulders/arms; explicitly "do NOT add size or bulk", "no airbrushed or plastic look".
- **Clothing lock** (nano quietly redesigns garment details otherwise — it once turned swim briefs' waistband into a V-cross style): name the garment and state it must stay identical in style, color, cut, waistband, and hardware (zippers, drawstrings).
- Close with: keep exact existing skin tone, NO added tan; "single photorealistic photograph filling the whole frame, no text".
- If the model returns "No images were returned", it declined the phrasing — reword the sensitive part in neutral fabric/fit terms and lead with "Generate an image that is an exact photographic copy of this photo with one small adjustment…".

### 3a. Draft at 2K, finish at 4K — the cost rule (measured 2026-08-10)

A full retouch is many takes: two body intensities, a face pass, often a tone-match pass and a re-roll or two. **Most of those exist only to decide a direction, and a 2K image decides it exactly as well as a 4K one.** 4K costs $0.24; 1K and 2K both cost $0.134 — so 2K is the correct draft tier (same price as 1K, more detail to judge).

Use the shared Google-direct runner, which takes a `--tier`:

```bash
node ../_shared/gemini-image.js generate --image input-2048.jpg --prompt-file prompt.txt \
  --out out/candidate.jpg --tier draft --env <scratchpad>/.keys.env    # 2K, $0.134
node ../_shared/gemini-image.js generate --image input-2048.jpg --prompt-file winner.txt \
  --out out/final.jpg --tier final --env <scratchpad>/.keys.env        # 4K, $0.24
```

Re-run **only the approved prompt** at `--tier final`. On a typical 6-take photo that is ~44% off five of the six takes. The 4K output is 3584×4780 (the 2K is 1792×2390), so every downstream recipe here — the `scale=2747:4096` QC upscale, the warp coordinates, the 4:5 crop — still applies to the final only.

`--env` takes the same keys file as `replicate-edit.js`; this runner reads `GEMINI_API_KEY` instead of `REPLICATE_API_TOKEN`. Google direct was verified 2026-08-10 to accept the same shirtless retouch prompts Replicate accepts (no moderation difference), and it is what unlocks batch mode below.

**Do NOT swap models to save money — this is now measured, not assumed.** `gemini-3.1-flash-image` (Nano Banana 2) is about half the price and **fails the same way Seedream and FLUX do**: on `public/img/proof/male-before.webp` it changed the subject's shorts from black to grey and shifted the framing. Nano Banana Pro held garment, background, framing and identity exactly. Resolution is the cost dial for retouching; the model is not. (Nano Banana 2 *is* fine for generating **new** images, where there is no original to preserve — see the `imagesandclips` skill.)

### 3b. INTERACTIVE IS THE DEFAULT. Batch is never your call — Dan's standing rule, 2026-08-13

**Run every photo job interactively (synchronously) unless Dan has explicitly approved batch for that job.** Speed is worth more to him than the 50% saving; he said plainly he doesn't mind paying more to have the photos now.

The one decision rule, applied to the **whole job you are about to run**:

1. Work out the interactive cost — `photos × $0.24` at `--tier final` (`× $0.134` at draft).
2. **Under $10 → just run it interactively. Do not mention batch, do not ask.**
3. **Over $10 → stop BEFORE editing anything, state the interactive cost and the batch cost, and ask.** If he approves batch, use batch. If he declines or wants it now anyway, run interactively at full price — his call, and "over budget" is not a veto you hold.

This also cleanly satisfies the `AGENTS.md` $10-per-session spend rule: any job big enough to need that conversation is the same job that triggers this one, so have it once, up front, and cover both.

**The mistake this rule exists to prevent (2026-08-13, cost a wasted ~$5).** On a 41-photo job I chose batch *silently*, reasoning that interactive would breach the $10 session cap. Two things were wrong. The spend cap is a prompt to **ask Dan**, not licence to quietly pick the slower product; and I'd made the tradeoff for him after he'd said speed mattered. He rejected it, and the switch cost real money because **there is no working way to cancel a running Google batch — `POST batches/{id}:cancel` returns 404.** The only lever is `DELETE /v1beta/batches/{id}` (200), which stops the job and discards the output but may still bill for work already done. So a batch chosen wrongly cannot be taken back for free: **decide before submitting, not after.**

Practical notes when batch IS approved: say explicitly that you've used it, so Dan knows results may not land in this session; and never promise a turnaround off the 4-minute observation below.

**Batch mode mechanics — 50% off, and usually far faster than advertised.** Google's Batch API is a flat half price ($0.24 → $0.12 at 4K, $0.134 → $0.067 at 2K). The documented SLA is "up to 24 hours", but a 2-image batch measured **under 4 minutes end to end** on 2026-08-10, and the output was byte-for-byte equivalent in quality to the synchronous call (verified side by side: same in-place retouch, garment and background preserved). **Treat the 24-hour figure as a worst case, not the expected case** — but a large batch or a busy queue can genuinely take hours, and there is no way to tell in advance:

```bash
node ../_shared/gemini-image.js batch-submit --spec jobs.json --tier final --env <keys>
node ../_shared/gemini-image.js batch-status --job batches/<id> --env <keys>
node ../_shared/gemini-image.js batch-collect --job batches/<id> --out-dir out/ --env <keys>
```

`jobs.json` is `[{ "key": "photo-44", "promptFile": "p44.txt", "image": "in44.jpg" }, ...]`. Keys become output filenames. Inline batches are capped near 20 MB of encoded payload — the runner refuses oversized specs up front rather than failing after the encode. At 2048px/q90 inputs that is **roughly 14 photos per batch** (41 photos needed splitting into 3), so size the chunks from the actual file sizes before submitting. **Say explicitly when you have used batch**, so Dan knows results may not land in this session.

### 3b. Reverse direction — making Dan look HEAVIER (verified 2026-08-06)

Same skill, opposite ask: reconstruct what he looked like at a heavier weight for ad "before" images (no real shirtless photo of him at his heaviest exists — see [[dan-before-photo-search]]). **Nano Banana Pro wins here too, and by a wider margin.** Measured on the 2022 deck-chair photo: **Seedream 4.5 recomposed the entire shot** (new crop, new sky, different face, invented shorts) and **FLUX Kontext overshot to roughly +50 lbs and added jeans** — both unusable, don't re-try them.

Prompt structure that worked: the standard identity/pose/background/framing lock, then a single "THE ONE CHANGE: he is approximately N pounds heavier, carrying it as ordinary soft body fat — not obese, not a caricature", then an anatomical breakdown of *where* it goes (belly rounder and higher with a deeper seated crease; fuller flanks/love handles; softer lower-sitting chest; modestly rounder cheeks, softer jaw, slight fullness under the chin; thicker softer arms with less definition). Naming the regions is what keeps it from just inflating everything uniformly.

**Nano overshoots the stated number** — a "+10 lb" prompt reads closer to +13–15. Bracket with three passes (+8 / +10 / +15) and let Dan pick; on this photo he chose the **+8 LIGHT** pass as most accurate to reality. Add an explicit restraint clause to the light variant ("RESTRAINT IS CRITICAL… overshooting into an obviously overweight body is a FAILURE") — without it the light pass lands on top of the mid. The heaviest pass also invented freckles on cheek and chest that aren't in the original; check for that at zoom.

Finals live in `photos/Dan Before Pictures/` (gitignored) with the prompts saved alongside for regeneration.

### 4. QC before Dan sees anything

Build before/after **crop strips** of the face and each edited region (ffmpeg `crop` + `hstack` of original | candidate(s)) and inspect them yourself at zoom. Check: identity, **mole/beauty-mark positions**, **facial expression (mouth open/closed, eye narrowing, brow)**, **body sheen still present**, clothing details unchanged, no warped straight lines, no plastic skin. Reject failures silently and re-run with the offending rule sharpened. **Check the EYES here as their own item — aperture, not contour — and open them per the squinted-eyes standing rule below; on a big smile assume they need it.**

Two crops make the alignment trivial: upscale the 2048 original to the candidate's 4K size (`scale=2747:4096`) first, then apply identical `crop` args to both. Whole-frame comparisons hide these failures — every one of the errors above was invisible at full-frame and obvious at zoom.

**The two body intensities can disagree on the FACE, and that is exploitable (2026-08-08, toe-touch frame 44).** The STRONG pass produced clearly better abs but **closed his open mouth**, turning an exertion frame into a posed one — exactly the expression failure this skill warns about — while the SUBTLE pass held the parted lips correctly. Both are re-renders of the same input and came back **geometrically aligned** (background mean abs diff 3.0; `blend=difference` on the head showed single edges, not doubled). So instead of re-rolling STRONG with a harder lock, **composite SUBTLE's face onto STRONG's body** with the same feathered ellipse used in 4b. Best of both, no extra API call, no fresh identity dice-roll. Always run the difference check first — if the edges double, don't composite.

### 4b. Face drifted / "doesn't look like me" → composite the ORIGINAL face back, don't re-roll the AI

**On a studio / hard-definition batch, expect to run this on most or all of the set — budget for it rather than treating it as an exception.** Even with the minimal-intervention FACE block above, the body pass re-renders the head and something usually moves (age, jaw, or gaze). It is deterministic, free and fast, so the cost of running it on a photo that did not need it is nil.

**The measured recipe, from the 10-photo batch Dan approved 2026-08-28** (`in/` = the 2048 original, `toned/` = the tone-matched 4K retouch):

1. **Measure the head offset instead of assuming zero.** Edge-filter (`ImageFilter.FIND_EDGES`) the face region of both, downscale the crop to ~400 px, mean-subtract, and brute-force normalised cross-correlation over ±18 px. All 10 came back **dx 0–16, dy −7–0, r 0.44–0.69** — small, but not zero, and a 16 px paste at 3368 px wide shows as a double edge. Apply the offset with an `Image.AFFINE` shift before compositing. Treat `|d| < 25 px and r > 0.25` as aligned; anything outside that, do not composite.
2. Feathered ellipse over the face, **smoothstepped between d = 0.85 and d = 1.30** of the normalised radius. Size it to run forehead → chin and stop **above the collarbone** — reaching onto the chest pastes un-hardened body back in and leaves a visible seam against the hardened torso.
3. Per-channel tone gains inside the core (`d < 0.85`), clipped to `[0.85, 1.18]`. On this batch they landed at **1.007–1.080**, i.e. nowhere near the clip, which is the sign the mask is sized right.
4. Composite `original*mask + retouch*(1−mask)`.

⚠ **Do NOT try to re-add the face de-shine algorithmically afterwards.** A luminance-percentile highlight roll-off inside the face mask was tried and is a clear failure — grey blotches on the cheek, darkened teeth, spill onto the background. Ship his own mild shine; it reads as real skin, and that is exactly the "slightly imperfect real photo beats a heavy edit" trade this skill opens with.

⚠ **A numeric face-difference score does not rank these edits — the eyeball does.** On `Blue-0202` the crude face L1 got marginally *worse* with the better prompt (0.118 → 0.124) because a gaze shift dominates the pixel metric while the restored forehead lines barely register. Use the number to flag, never to decide.

The original context for this technique: when Dan rejects a face as distorted/not-him (happened on the towel-wipe frame, 2026-08-06), another nano attempt is the wrong move — every AI pass re-renders the face and rolls the identity dice again. Instead: upscale the original to the candidate's 4K size, alpha-blend the original face over the retouched body inside a feathered ellipse (PIL, feather over d≈0.85→1.30 of the normalized ellipse), then match tone by multiplying inside the same mask with per-channel `chest_mean/face_mean` gains (clip to ~[0.85, 1.18]). Verify alignment first with an ffmpeg `blend=difference` crop — single edges mean aligned, doubled edges mean don't composite. Result is pixel-identical identity with the retouched body kept. The same local-gain trick (no paste) fixes "face slightly too dark/light" requests in seconds and is also the fallback when nano's tone-match pass keeps warming the whole scene instead of just the face (it did, on 1 of 9).

### 4c. DATING-APP edits are a DIFFERENT, MUCH LIGHTER recipe — do not use the social-media edit

Dan keeps two separate outputs from the same shoot: `photos/finalized social media photos/` (the full retouch above) and `photos/finalized dating photos/` (`photo-<N>_FINAL_DATING.jpg`). **The dating edit is deliberately conservative — the stated target is "photos that don't look edited at all", so nothing reads as catfishing and nothing gets flagged on the apps.** Established 2026-08-05, re-run at scale 2026-08-13 (all 64 pool-shoot photos).

The recipe, and the differences that matter:

- **Face only:** de-shine to a NATURAL (never matte) finish, remove temporary blemishes, very lightly soften harsh forehead/under-eye lines. Keep pores, stubble, and his real lines — he must still read as a man in his forties.
- **Body: ZERO changes.** No ab enhancement, no muscle sharpening, no waist slimming. This is the single biggest departure from the social recipe, which does the opposite.
- **No warp, ever** — the briefs/speedo bulge warp that is a *standing default* on social shots is explicitly skipped here.
- **No IG 4:5 crop** — deliver the full-res final only.
- Everything else stays locked as usual: moles, expression, clothing, props, framing, tan depth, global exposure.

**Run it as one take per photo at `--tier final`.** There is no direction to decide, so the two-body-intensity bake-off doesn't apply and drafting at 2K just adds a step. 61 photos went 59/61 clean first try.

**The two failure modes that DO survive this prompt, both caught only at zoom — check for them specifically:**
1. **Closed eyes get opened on lying-down / exertion frames** (photo-42: eyes squeezed shut → open, plus a slimmed jaw). The generic expression lock is not enough; name the literal eye state and mark opening them a FAILURE, and separately forbid slimming the face — a face compressed by lying down reads to the model as something to fix.
2. **A relaxed seated belly gets "corrected"** (photo-241: soft stomach flattened, waist crease erased, abs sharpened — a full social-level edit). When he is seated or the midsection is relaxed, add an explicit clause that the softness and the waist crease must remain and that a flatter/harder midsection is a FAILURE.

Both were fixed by re-running that single photo with the base prompt plus a photo-specific paragraph. Per-photo prompt files, not a change to the shared one.

**QC shortcut that works well here:** since the only intended change is the face, the *epicentre of the diff map is a defect detector*. Compute `|input − output|`, mask to skin tone, blur, and crop around the peak — on a good photo it lands on the face; when it lands on the torso, that photo changed the body and needs a look. That is exactly how 241 was caught. Pair it with an aspect-ratio + whole-frame mean-diff check to catch recomposition (mean diff ran 3.9–6.2 across 61 clean photos).

### 5. Geometry edits the AI refuses or botches → local warp

For pure shape changes (fuller bulge in shorts, slimming a spot), AI models either return nothing or swap the garment for a different one. Use the bundled reshape tool on the approved 4K output instead — it changes ONLY the ellipse you aim it at, pixel-identical elsewhere:

```bash
python3 scripts/local-warp.py in.jpg out.jpg CX CY RX RY 0.30   # + = bigger, − = smaller
```

Find CX/CY by cropping a zoom of the region with a grid burned in (`drawgrid=w=100:h=100:t=2:c=red@0.7`) — reading coordinates off the grid beats guessing. 0.20–0.30 reads natural; iterate one number per round ("a touch bigger" ≈ +0.08). Reference result: flag photo used center (1920,2415), rx165/ry195, strength 0.30 on the 4096×2747 frame.

**Strength scales with how snug the garment is**, measured 2026-08-04 on 4096-long-edge frames: skin-tight briefs/square-cut trunks read right at **k=0.20** (rx≈215–230, ry≈175–195); looser trunks that drape need **k≈0.27** or the effect is invisible. Always verify with a before/after crop of the region — if you can't see it, it isn't there. Subject distance matters too: shrink the radii when he's further from camera.

**Standing default (Dan's call, 2026-08-04): always apply this warp when the garment is briefs/speedo-style (skin-tight, front clearly visible) — don't ask permission.** ~rx=220–242, ry=190–203, k=0.20 on the 4096-long-edge output reads natural on that garment type. Only skip it, or offer a no-warp variant alongside, when the front isn't actually visible in frame (cropped out, obstructed) or the garment is loose (board shorts, swim trunks) where the effect reads as barely-there anyway — use judgment on those, and it's fine to ask if genuinely unsure.

### 6. Deliver

- Full-res final + **IG 4:5 portrait crop**; verify nothing important is cut. A 4K portrait frame (2747×4096) can't hold 4:5 at full height, so crop **2747×3434** and pick the y-offset per photo to protect the head and any prop (a full-body action frame may simply not fit — say so rather than clipping the subject badly). A landscape frame (4096×2747) crops to **2198×2747** on an x-offset.
- Send via SendUserFile with the comparison strips so he can judge instantly. Deliver in groups of 2–3, not one at a time.
- On approval: finals → `photos/finalized photos/` as `photo-<N>_FINAL_PRIMARY.jpg` + `photo-<N>_FINAL_PRIMARY-IG-4x5.jpg` (`<N>` = the shoot's frame number), remove superseded drafts. One-off subjects use `<subject>-FINAL.jpg` / `<subject>-FINAL-IG-4x5.jpg`.
- Offer one-variable iterations (warp strength, face smoothing amount) — each is seconds/cents.

## Photo selection from a shoot (no editing yet)

Same contact-sheet technique as step 1, then judge with Dan's platform logic: strongest-ab + best-light shots for IG hero slots; friendly/smiling "relatable guy" shots for Facebook; variety of outfits/settings across a grid. Shortlist 6–10 with a one-line reason each, then retouch only the picks he approves.

## Lessons from the 8/28 studio shoot (Snappr, 496 frames)

1. **The STRONG body pass adds tan and oil, and no prompt language stops it.** Measured on all 10 finals of 2026-08-28: every strong-block output came back visibly tanner/more orange and glossier than the original, even with a dedicated "TAN LOCK — making the skin tanner is a FAILURE" block. Don't burn re-rolls on it — fix it deterministically: **per-channel quantile histogram matching of the final back to its own original** (retouch outputs are geometrically aligned, so match 257 quantiles per RGB channel on the whole frame and LUT-interp the 4K final). This pulls the palette back to the original exactly while keeping all the added definition, and it also fixed face-vs-body pallor in the same pass. Recipe used: `np.percentile` at `linspace(0,100,257)`, `np.maximum.accumulate` on the source quantiles, `np.interp`. Judge tone on an orig | raw-final | toned strip.
2. **Write expression locks from ZOOMED face crops, never from 640px candidate thumbnails.** Two of ten expression descriptions were wrong at thumbnail scale (a toothy grin read as a "soft closed smile"), and the model obediently executed the wrong description. The failure is invisible until the QC face crop.
3. **A 2K draft can replace the person entirely and still exit 0** — one subtle-pass draft returned a completely different man (white model, tripled, recomposed background). The per-photo QC eyeball is not optional; a mean-diff check on aligned downsamples (normal band ≈ 4–7) also flags recomposition.
4. **Snappr's export filenames carry a LEADING SPACE** (" Snappr Daniel Studio Blue-1.JPG"). A plain `while read` strips it and every `cp`/`sips` then misses; use `while IFS= read -r`.
5. **This shoot's "white stripe" is a horizontal pale band under each ab row** (tan-application gap), not the vertical linea-alba band; Dan confirmed the 10 selected frames needed no fix. Keep a gentle "do not introduce or exaggerate pale horizontal banding across the abs" clause in the prompt.
6. **Studio-shoot warp placements that read natural (3368×5056 frames, k=0.20):** green retro shorts ≈ rx270/ry230, black square-cut trunks ≈ rx260–280/ry220–230, closer-framed shots up to rx300/ry250; loose white cotton shorts needed k=0.27. Muay Thai satin shorts and jeans: no warp (loose).
7. ⚠ **THE HARD-DEFINITION PASS DE-AGED THE FACE ON 10 OF 10 FRAMES — AND THE CAUSE WAS OUR OWN FACE BLOCK, NOT AN UNFIXABLE MODEL HABIT.** The first run of this batch used the old FACE wording ("smooth forehead/under-eye lines", "slightly sharpen the jawline") and nano removed his forehead furrows, smile lines and cheek moles and slimmed the jaw on **every single photo** — each face read about ten years younger — despite "do not de-age him", a KEEP-pores clause and a critical moles-and-marks block. **It is invisible at full frame and at 640px and obvious the moment you crop the face**, which is why the per-photo zoomed face crop is not optional. **The fix went into the prompt: those two structural asks are now removed** — see the minimal-intervention FACE block in "Prompt recipe that works", which A/B'd markedly closer to his real face (`Gray-0012` face-structure L1 **0.173 → 0.099**). ⚠ **It reduces the drift but does not end it** — on `Blue-0202` the soft block restored the lines yet still pulled his averted gaze back toward the lens. **So on a studio batch, still expect to run the §4b face composite on most of the set**; the two are complementary. Never re-roll to fix a drifted face — that just re-rolls the identity dice.
8. **Do NOT try to re-add the face de-shine algorithmically after that composite** — a luminance-percentile highlight roll-off produced grey blotches on the cheek, darkened the teeth and spilled onto the background. Ship his own mild shine. Full note in §4b.
9. **A BACKGROUND LOCK paragraph prevents the white-wall repaint — it did not fire once in 10 photos.** Adding an explicit clause ("must stay exactly as it is — the same flat even color and the same gradient; do NOT add texture, mottling, blotches, vignetting, shadows or gradients that are not already there") held every white and grey backdrop: measured wall standard deviation moved 17.59→17.44 and 17.69→18.39 on the two white frames, so the documented MinFilter/GaussianBlur composite fix was never needed. Include the clause by default and keep the deterministic fix as the fallback.
10. **Guard picks against a concurrent session by BURST DISTANCE, not just exact frame number** — adjacent frames in this shoot are the same pose from the same burst and would deliver as visible duplicates. Require ≥8 frames of separation on the same background from both the other session's picks and the already-finalized set. It over-fires on a genuine pose change (Gray 48 arm-extended landscape vs Gray 55 hands-behind-head portrait sit 7 apart and look nothing alike), so treat a trip as "go look", not "reject" — the visual check is decisive.

11. **Once the hard-definition rule is settled for a shoot, SKIP THE 2K DRAFT TIER.** The two-intensity bake-off exists to decide a direction; with the direction already decided there is nothing for a draft to answer, so every photo goes straight to `--tier final`. The second batch of 10 from this shoot cost **$2.64 all-in against ~$8 for the first**, same output quality. (The 2K tier is still right whenever a genuine direction question is open.)
12. **A contact sheet's CELL POSITION IS NOT THE FRAME NUMBER, and the drift is silent.** Snappr's export has gaps (this shoot has no Blue-263 and no White-87), so by sheet 6 the grid position had drifted ~8 frames from the filename. Picks read straight off a sheet grid point at the wrong photo. Always resolve position → filename through the `thumb-order.txt` written when the sheets were built. Reusing a prior session's `thumbs/` + `sheets/` is otherwise free and safe — it saved a full re-tile here.
13. **When an expression lock fails, describe the EVIDENCE, not the mood.** `Gray-0055`'s "closed-lip smile with the corners turned up… flattening it into a blank neutral face is a FAILURE" still came back stern. The re-roll that fixed it on the first attempt named the physical signs instead: corners *pulled up and back*, cheeks pushed up, nasolabial creases present, outer eye corners crinkled — plus "smoothing away the cheek and smile creases that make the smile readable" as its own failure. Nano can execute anatomy; it interprets adjectives loosely. Re-check the garment after any re-roll at this intensity.
14. **Do NOT colour-mask the garment to find the warp centre — it grabs skin and backdrop.** On five photos it put three centres on his hand or his navel. What works: burn a grid labelled in FULL-FRAME coordinates over the lower body (`ImageDraw` lines every 100px with the real x/y printed), read the front centre seam for CX, and set **CY ≈ waistband top + 0.62 × (crotch-notch y − waistband top)**. Verify with a before/after crop of the region every time; a warp you cannot see is not there.
15. **The histogram tone-match also repairs a backdrop the model recoloured.** `Blue-0109`'s raw output turned the blue backdrop gray; the tone pass pulled it back with no extra call. It cannot fix *structural* repaints (mottle, texture) — only tonal ones — so the explicit "repainting the wall is a FAILURE" clause still earns its place, and it held on the white background here. Measure it: background-corner dE orig-vs-final ran 2–5 on a clean photo, 8–13 where the model redrew the gradient falloff (harmless).
16. **Finding the head for the IG 4:5 crop: "differs from the corner background" DOES NOT WORK on these backdrops.** Both the blue and the gray carry a gradient, so row 0 already trips the test and every crop lands at y=0. The detector that works is **dark hair in the central 50% of columns**, thresholded per image at *(median luminance of the top 2% of rows) − 42* — a fixed threshold fails too, because the gray backdrop's own luminance (78–100) sits under any threshold that catches black hair on blue. 4:5 at this frame size is **full width, 3368×4210**, y-offset = hair top − 200.

## STANDING RULE — squinted eyes get opened, unasked (Dan's call, 2026-08-28)

**Whenever Dan's eyes read too squinted — above all on a BIG SMILE, which is when it happens — open them back up as part of the edit. Do not ask.** His words, lifting the hold after reviewing the first four: *"let's write in this eye modification rule: anytime my eyes are looking too squinted from a big smile."*

**The target: finish slightly ABOVE the original on height, a little above on width.** From his note on the batch that started this — *"you made them smaller than the original. I would like them a little bit larger than the original"* and, said twice, *"especially taller."* **Never deliver eyes smaller than the raw frame.**

**Two things trigger it, and they compound:** the retouch closes the aperture on its own (below), and a big smile pushes the cheeks up into the lower lid before the retouch even runs. A big-smile frame therefore needs the pass most and the *smallest* gain — see the settings below.

⚠ **THE RETOUCH DOES NOT SHRINK THE EYE, IT CLOSES THE APERTURE.** It paints the upper lid further down and takes the iris and sclera with it. That distinction decides the fix: **magnifying a closed eye just gives you a bigger closed eye.** A first attempt with `eye-warp.py` at gains up to 1.08/1.26 was visibly useless on `Blue-0145` for exactly this reason.

⚠ **VISION'S LANDMARK HEIGHT MASSIVELY UNDER-REPORTS THIS — do not gate on it.** `VNDetectFaceLandmarksRequest` fits the eye *contour*, which the retouch preserves, so it measured only a 3–5% loss on frames where the visible opening had collapsed to a slit. **Judge eyes on a zoomed crop; use the landmarks for COORDINATES, not for verdicts.**

**The fix that works — `scripts/eye-restore.py`, one call per eye, no AI:** alpha-blend the ORIGINAL eye back inside a feathered ellipse, tone-match it to the retouched skin on the mask's outer ring, then magnify anisotropically. This is §4b's composite-the-original-back trick scoped to one feature, and it keeps Dan's real eyes instead of rolling the identity dice on a fresh generation.

- **Get the centres from Vision, and pass BOTH.** Build the tiny `VNDetectFaceLandmarksRequest` CLI (`swiftc` is on this Mac; ~40 lines, prints cx/cy/w/h per eye) and run it on the original upscaled to the final's size AND on the final. **The face can shift 13–15px between the two** (`Gray-0004` did) — the script offsets the patch by that delta, which is why a blind composite ghosts and this one does not.
- **Settled gains: `1.07` wide, `1.22` tall** on 3368×5056 frames — ~6–8% over the original on landmark height, clearly taller without looking done. ⚠ **On a BIG-SMILE frame that is too much and Dan will say so: use `1.04` / `1.13` there** (he pulled `Blue-0222` back to it, landing +3.5%/+4.6% over the raw). The cheeks already push the lower lid up on a big smile, so an identical gain reads harder.
- **Iterating is FREE — no AI call anywhere in this workflow.** Two revision rounds on this batch cost $0.00. Reach for `eye-restore.py` before ever considering a re-roll.
- **Keep the mask off the crow's feet** (`rx = w*0.85`, `ry = h*1.9`): the original carries more line detail there, and a wider mask drags it back in and fights the retouch.
- **Verify two ways:** a zoomed ORIGINAL / previous / new strip, and a changed-pixel bounding box — a correct run touches ~40k pixels in a ~500×260 box per face and *nothing* else in the frame.

**Scope — apply it per photo, not per batch.** Judge every frame's eyes on a zoomed crop against its raw; treat any frame where the aperture has visibly closed, or where a big smile has squeezed it to a slit, as needing the pass. Frames whose eyes already read open are left alone — this is a correction, not a look. **Established on `Blue-0145`, `Blue-0109`, `Gray-0004` and `Blue-0222`, all approved; `Blue-0222` set the big-smile number after Dan pulled it back one step.**

## STANDING RULE — studio-shoot ab intensity (Dan's call, 2026-08-28)

**Studio photos get the HARD DEFINITION body block by default — the ordinary "strong" block undershoots what Dan wants on studio lighting.** On the 8/28 Snappr shoot he reviewed raw | strong | hard side-by-sides for all 10 picks and chose the hard pass for every single one. Use this block verbatim as the starting point for studio retouches (outdoor/pool shoots keep the two-intensity bake-off until a similar verdict exists for them):

> BODY (HARD DEFINITION PASS): Carve the abdominal definition clearly harder than the original: each of the six abs distinctly separated with deep, natural groove shadows between and beneath every ab row, the vertical midline (linea alba) reading as a clean dark line from sternum to navel, sharply etched obliques and serratus lines at the sides, and a hard, deep V-cut at the waistband. Lower body fat look: the skin should sit tighter over the muscle, as if he is 2-3% leaner than the original photo. Chest, shoulders and arms harder and more striated-looking as well. STILL A REAL BODY: do NOT add muscle size or bulk, do NOT inflate anything, no airbrushed or plastic skin, and the definition must follow his real anatomy exactly where it already shows in the original.

⚠ **TO HIT AN INTENSITY *BETWEEN* TWO RENDERS, BLEND THEM — BUT ONLY IN THE LOW FREQUENCIES.**
Measured 2026-08-28 (batch 4 rev 2), when Dan said the softened pass had gone too far and asked for
*"halfway between this one and the aggressive edit."* Both renders come from the same input, so the
halfway point can be computed deterministically for **$0.00** — no fresh prompt, and crucially **no
new identity dice-roll**, which is the main risk of a third generation.

**A straight 50/50 pixel blend is WRONG and the metric that catches it is local gradient energy.**
The two renders carry different fine skin texture, so averaging them blurs it: torso sharpness fell
**2.52/2.10 → 1.64, a 22–27 % loss** across four photos — it reads as the plasticky skin this skill
bans everywhere else. The ab shading landed correctly; the texture did not survive.

**The fix is frequency separation.** Groove/shadow depth — the thing being dialled — is LOW
frequency; skin texture is high. So average only the low band and keep the high band from one render:

```python
loA = np.asarray(v1.filter(ImageFilter.GaussianBlur(30)), float)   # r=30 at 4K
loB = np.asarray(v2.filter(ImageFilter.GaussianBlur(30)), float)
out = np.clip(0.5*loA + 0.5*loB + (np.asarray(v1,float) - loA), 0, 255)
```

Sharpness ratio came back **1.02–1.03 vs the source render** (i.e. fully preserved) at both r=20 and
r=30, while whole-frame mean-diff landed between the two parents as intended. Change the 0.5 to move
the dial anywhere on the line. **Tone-match the blend to the original afterwards as usual**, then warp.

**Verify alignment per REGION before blending, and allow ±1 px of noise in the test.** Run a shift
search on horizontal bands (head / chest / abs / shorts / legs). Three of four photos were a clean
`(0,0)` everywhere. One had **dx consistent at −3…−4 but dy drifting +2 at the head to −2 at the
legs** — not a translation but a **~0.5 % vertical scale difference** between the two renders. A
global affine (`dx` + `1+m` vertical scale, fitted by `np.polyfit` on the per-band offsets) corrected
it to `(0,0)±1`. ⚠ **A pass condition of "argmin is exactly (0,0) in every band" is TOO STRICT and
will send you to re-prompt a perfectly blendable pair** — that happened here. The real test is
whether shifting still *helps*: after registration the best-shift error was within **0.01–0.04** of
the error at `(0,0)`, which means aligned. Compare `peak` against `@0,0`, not the argmin against zero.

⚠ **THE HARD BLOCK OVERSHOOTS ON ROUGHLY HALF OF FRAMES — DAN'S CALIBRATION, 2026-08-28 (batch 4).**
He reviewed ten hard-pass finals and called **six of them "a little too unnaturally shredded"**, asking
to *"very slightly dial back the aggressiveness."* The other four he finalized as-is. **This does not
overturn the standing rule** — the hard block stays the default and he chose it 10/10 on the first
batch — but expect a dial-back pass on a meaningful share of any batch, and note the pattern: the
frames he kept at full hardness were angled/hands-on-hips or clothed, while the ones he softened were
the flatter, more front-on torsos where the deep grooves read as drawn on. **When in doubt on a
front-on torso, run this block instead** (it is a small step down, which is what he asked for — not a
return to the old "strong" block):

> BODY (NATURAL DEFINITION PASS - RESTRAINED): Improve the abdominal definition a little over the
> original, but keep it clearly believable: this is a genuinely fit man in his forties photographed in
> good studio light, NOT a competition bodybuilder in peak condition. Each ab reads as separated with a
> SOFT, natural groove shadow between the rows; the vertical midline is visible but gentle, not a hard
> drawn line; the obliques are defined but not etched or striated; a light V-cut at the waistband. The
> skin should sit only slightly tighter over the muscle, as if he is about 1% leaner than the original
> photo - no more than that. Chest, shoulders and arms very slightly crisper. CRITICAL RESTRAINT - THIS
> IS THE POINT OF THIS EDIT: do NOT carve deep, hard, black-shadowed grooves between the muscles; do
> NOT make him look shredded, ripped, striated, peeled or competition-lean; do NOT add muscle size or
> bulk; no airbrushed, waxy or plastic skin. Keep his real skin texture. The definition must follow his
> real anatomy exactly where it already shows in the original and must not invent separation that is
> not already faintly there. IF IN DOUBT, UNDER-DO IT: a result that looks slightly too natural is
> CORRECT, and a result that looks unnaturally shredded is a FAILURE.

Pair it with the silhouette lock below. Measured on the six re-rolls: mean-diff against the original
fell into 3.98-5.72 for five of them (from 4.73-5.75 on the hard pass) and every tan shift toned back
to 0.8-3.1 — i.e. **the softened block costs nothing in the checks and only changes the look.** Show
Dan **original | previous | new** side by side when delivering a dial-back, so he can judge the step
size rather than just the result.

**ADD THE SILHOUETTE LOCK ON STRAIGHT-ON FULL-BODY FRAMES (measured 2026-08-28, batch 4).** At this
intensity the hard block sometimes stops carving definition and starts *inflating the man* — on one
straight-on frame it widened the shoulders and lats, thickened both arms, glazed the skin in oil and
zoomed him slightly in frame. **The whole-frame mean-diff on aligned downsamples is what catches it:
17.45 against a 3.90-6.17 band for nine sibling frames, with a tan shift the histogram match could
not pull back (34.6 -> 19.4 residual).** A structural change reads as a diff the tone match cannot
fix; a palette change does not. Angled and hand-on-hip frames did not overshoot — it is the
straight-on, arms-down poses that do. Add this block verbatim for those, and re-roll (do not try to
fix it with the tone match):

> SILHOUETTE LOCK - THE MOST LIKELY THING TO GO WRONG IN THIS EDIT, READ IT TWICE: his OUTLINE must
> not change at all. His shoulder width, the thickness of his upper arms and forearms, the size and
> projection of his chest, the width of his waist and hips, and the thickness of his thighs must all
> measure EXACTLY the same in your output as in the input photograph. MAKING HIM BIGGER, WIDER,
> BULKIER, MORE MUSCULAR OR MORE INFLATED IS A COMPLETE FAILURE OF THIS EDIT - he must not look like
> a bodybuilder, and his arms must not thicken. You are only allowed to deepen the shadows and
> definition INSIDE the existing outline; you may not move the outline outwards anywhere. Equally,
> DO NOT add body oil, wet gloss, or a glazed shiny sheen to the skin. And do not scale, zoom or
> enlarge him within the frame: his head, shoulders and feet must sit at exactly the same pixel
> positions as the input.

**RESTORING DELETED MOLES MUST STAY HAND-VERIFIED - an automated detector was built, measured and
rejected (2026-08-28).** The mole-lock block does not always hold: one frame lost an ear stud and a
raised skin tag with the block present. Because the retouch is pixel-aligned with the original, the
fix is a feathered ellipse compositing the original pixels back (r~45-65 at 4K, GaussianBlur(9),
~0.2% of the frame, no seam) - never a re-roll, which re-rolls identity and drifts the garment.
**But do not automate the site-finding.** A black-top-hat detector ("dark in the original, faded in
the final") flags **90-119 clusters per face** - it cannot separate a mole from stubble, pores, brow
hairs or ear folds. Tightened to connected components with compactness, area and contrast filters it
drops to <=6 candidates, and **roughly half are still false positives; on one frame a candidate
landed on the mouth**, where compositing would have put the original teeth over the retouched ones.
Read the coordinates off a grid crop instead and verify each one. The detector is still useful as
*corroboration*: the genuine ear stud ranked #1 by a wide margin (strength 64 x drop 63).

**IG 4:5: compute the crop from the actual output size, don't reuse the 2747x3434 figure.** That
number is for a 2747x4096 frame. A 3368x5056 output holds 4:5 at FULL WIDTH (3368x4210), so only a
y-offset is chosen - set it per photo from the measured head top (head_top - 220, clamped) to
protect headroom, and verify the set on a contact sheet.

**The hard body block is only half the studio recipe. Run it with the minimal-intervention FACE block (§3) and expect to finish with the §4b face composite on most of the set** — the body pass re-renders the head, and at this intensity it de-aged him on 10 of 10 before the FACE block was softened. So the settled studio pipeline is: hard body block + soft face block → histogram tone-match → **zoomed face crop on every photo** → composite the original face back wherever anything moved → warp → 4:5 crop. Dan approved all 10 of the 2026-08-28 batch built exactly this way.

Pair it with the mandatory post-pass histogram tone-match (Lessons item 1) — the hard block tans and oils the body even more reliably than the strong block. Two failure modes measured at this intensity, both on clean white backgrounds: the model repaints a plain white wall into gray mottle (fix deterministically — mask the background from the aligned original at `gray>170 & chroma<28`, MinFilter(9) erode, GaussianBlur(10) feather, composite the original wall back; do NOT re-roll, a re-roll changed the garment), and re-rolls at this intensity drift clothing more readily — check the garment against the original every time.
