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
- FACE block: remove sweat shine → matte natural finish; smooth forehead/under-eye lines while KEEPING real skin texture and pores; remove blemishes; slightly sharpen jawline. **Scope every line of this block to the face explicitly** ("FACE ONLY — every instruction in this paragraph applies to his face and nothing else") — see the body-sheen rule below for why.
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

Build before/after **crop strips** of the face and each edited region (ffmpeg `crop` + `hstack` of original | candidate(s)) and inspect them yourself at zoom. Check: identity, **mole/beauty-mark positions**, **facial expression (mouth open/closed, eye narrowing, brow)**, **body sheen still present**, clothing details unchanged, no warped straight lines, no plastic skin. Reject failures silently and re-run with the offending rule sharpened.

Two crops make the alignment trivial: upscale the 2048 original to the candidate's 4K size (`scale=2747:4096`) first, then apply identical `crop` args to both. Whole-frame comparisons hide these failures — every one of the errors above was invisible at full-frame and obvious at zoom.

**The two body intensities can disagree on the FACE, and that is exploitable (2026-08-08, toe-touch frame 44).** The STRONG pass produced clearly better abs but **closed his open mouth**, turning an exertion frame into a posed one — exactly the expression failure this skill warns about — while the SUBTLE pass held the parted lips correctly. Both are re-renders of the same input and came back **geometrically aligned** (background mean abs diff 3.0; `blend=difference` on the head showed single edges, not doubled). So instead of re-rolling STRONG with a harder lock, **composite SUBTLE's face onto STRONG's body** with the same feathered ellipse used in 4b. Best of both, no extra API call, no fresh identity dice-roll. Always run the difference check first — if the edges double, don't composite.

### 4b. Face drifted / "doesn't look like me" → composite the ORIGINAL face back, don't re-roll the AI

When Dan rejects a face as distorted/not-him (happened on the towel-wipe frame, 2026-08-06), another nano attempt is the wrong move — every AI pass re-renders the face and rolls the identity dice again. Instead: upscale the original to the candidate's 4K size, alpha-blend the original face over the retouched body inside a feathered ellipse (PIL, feather over d≈0.85→1.30 of the normalized ellipse), then match tone by multiplying inside the same mask with per-channel `chest_mean/face_mean` gains (clip to ~[0.85, 1.18]). Verify alignment first with an ffmpeg `blend=difference` crop — single edges mean aligned, doubled edges mean don't composite. Result is pixel-identical identity with the retouched body kept. The same local-gain trick (no paste) fixes "face slightly too dark/light" requests in seconds and is also the fallback when nano's tone-match pass keeps warming the whole scene instead of just the face (it did, on 1 of 9).

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
7. ⚠ **THE HARD-DEFINITION PASS DE-AGES THE FACE ON EVERY SINGLE FRAME, AND THE PROMPT CANNOT STOP IT.** Measured on all 10 finals of the second 8/28 batch: despite "do not de-age him", "KEEP real skin texture and pores" and a critical MOLES AND MARKS block, nano removed his forehead furrows, smile lines and cheek moles and slimmed the jaw on **10 of 10** — every face read roughly ten years younger. It is invisible at full-frame and at 640px; it is obvious the moment you crop the face. **Treat a face composite as a routine step of the studio recipe, not an exception.** Do NOT re-roll (that re-rolls the identity dice again) — use §4b: measure the head offset by edge cross-correlation (all 10 came in at 0–16 px, r 0.44–0.69), then alpha-blend the ORIGINAL face over the retouched body in a feathered ellipse with per-channel in-mask tone gains (they land ≈1.01–1.08, well inside the [0.85, 1.18] clip). Result keeps the hard body and restores his real face with no seam.
8. **Do NOT try to re-add the face de-shine algorithmically after that composite.** A luminance-percentile highlight roll-off inside the face mask was tried and is a clear failure — it produced gray blotches on the cheek, darkened the teeth, and spilled onto the background. The original face's own mild shine reads as real skin and is the correct thing to ship; it is exactly the "slightly imperfect real photo beats a heavy edit" trade.
9. **A BACKGROUND LOCK paragraph prevents the white-wall repaint — it did not fire once in 10 photos.** Adding an explicit clause ("must stay exactly as it is — the same flat even color and the same gradient; do NOT add texture, mottling, blotches, vignetting, shadows or gradients that are not already there") held every white and grey backdrop: measured wall standard deviation moved 17.59→17.44 and 17.69→18.39 on the two white frames, so the documented MinFilter/GaussianBlur composite fix was never needed. Include the clause by default and keep the deterministic fix as the fallback.
10. **Guard picks against a concurrent session by BURST DISTANCE, not just exact frame number** — adjacent frames in this shoot are the same pose from the same burst and would deliver as visible duplicates. Require ≥8 frames of separation on the same background from both the other session's picks and the already-finalized set. It over-fires on a genuine pose change (Gray 48 arm-extended landscape vs Gray 55 hands-behind-head portrait sit 7 apart and look nothing alike), so treat a trip as "go look", not "reject" — the visual check is decisive.

## STANDING RULE — studio-shoot ab intensity (Dan's call, 2026-08-28)

**Studio photos get the HARD DEFINITION body block by default — the ordinary "strong" block undershoots what Dan wants on studio lighting.** On the 8/28 Snappr shoot he reviewed raw | strong | hard side-by-sides for all 10 picks and chose the hard pass for every single one. Use this block verbatim as the starting point for studio retouches (outdoor/pool shoots keep the two-intensity bake-off until a similar verdict exists for them):

> BODY (HARD DEFINITION PASS): Carve the abdominal definition clearly harder than the original: each of the six abs distinctly separated with deep, natural groove shadows between and beneath every ab row, the vertical midline (linea alba) reading as a clean dark line from sternum to navel, sharply etched obliques and serratus lines at the sides, and a hard, deep V-cut at the waistband. Lower body fat look: the skin should sit tighter over the muscle, as if he is 2-3% leaner than the original photo. Chest, shoulders and arms harder and more striated-looking as well. STILL A REAL BODY: do NOT add muscle size or bulk, do NOT inflate anything, no airbrushed or plastic skin, and the definition must follow his real anatomy exactly where it already shows in the original.

Pair it with the mandatory post-pass histogram tone-match (Lessons item 1) — the hard block tans and oils the body even more reliably than the strong block. Two failure modes measured at this intensity, both on clean white backgrounds: the model repaints a plain white wall into gray mottle (fix deterministically — mask the background from the aligned original at `gray>170 & chroma<28`, MinFilter(9) erode, GaussianBlur(10) feather, composite the original wall back; do NOT re-roll, a re-roll changed the garment), and re-rolls at this intensity drift clothing more readily — check the garment against the original every time.
