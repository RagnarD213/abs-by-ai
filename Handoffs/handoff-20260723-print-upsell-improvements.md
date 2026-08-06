# Handoff — Printify upsell improvements (member hub link, poster-on-wall mockup, post-purchase return)

**Created:** 2026-07-23 · **Requested by:** Dan · **Owner on pickup:** Claude Code
**Scope:** client-side only (`public/index.html`). No server, Stripe, or Printify changes.
**Risk:** low. Nothing in this task touches pricing, fulfillment, or the security fixes in `create-checkout` / `fulfillProductOrder`.

---

## Why we're doing this

Three specific complaints from Dan about the print upsell inside the members area:

1. **Members can't find the print offer.** The print entry point (`#hubPrintUpsell` tile) is only shown to hub-**preview** users (`public/index.html:4585` — `style.display = preview ? '' : 'none'`). A logged-in paying member sees the before/after hero images and no way to buy a print from that screen. Dan wants a small centered "Print My Future Self" link/button directly under the hero images so it reads as attached to that image.
2. **The product mockup looks bad and is misleading.** White bars appear above and below the photo, and the 9×11" and 11×14" posters render at identical size, so size selection means nothing visually. Dan wants it to look like a poster hanging on a wall, with a reference object for scale.
3. **After purchase, users land on the Macro Tracker.** Should return to the member hub home screen.

---

## Current-state findings (already verified in code — do not re-derive)

### Item 1 — hub hero + print entry points

- Hero markup: `public/index.html:2023-2031` (`#hubHero`, two `.hub-hero-col` columns with `#hubBeforeImg` / `#hubAfterImg` and "Today" / "Your Goal" labels). Shown/hidden at `4743-4745`.
- `#hubPrintUpsell` tile: markup `2035`, visibility `4585`, click wiring `5375` → `showHubPrintUpsell()` at `4564-4569`.
- `showHubPrintUpsell()` already does the right thing: sets `upsell.imageDataUrl` from `LAST_AFTER_KEY`, sets `upsell.returnScreen = 'hub'`, fires PostHog `print_upsell_clicked`, then `showProductSection()`. **Reuse it — do not write a second path.**
- Note there is a third entry point from the gallery at `5181` (`upsell.returnScreen = 'transformations'`).

### Item 2 — the white bars and the identical poster sizes

Root cause, in `public/index.html` CSS at `746-765`:

```
.full-canvas { width: 170px; height: 170px; ... }      /* fixed square */
.full-canvas img { object-fit: contain; background: #fff; }
.full-poster { width: 146px; height: 204px; ... }      /* fixed, one size for all posters */
.full-poster img { object-fit: contain; background: #fff; }
```

- `object-fit: contain` + `background:#fff` inside a fixed box = the white letterbox bars, because the generated photo is portrait 3:4 and the box is a different ratio.
- The box dimensions are hardcoded per product type, not per **size**, which is why 9×11 and 11×14 look identical. `selectProduct()` (`3678-3726`) renders the mockup once and never re-renders it when a size chip is clicked (`3702-3709`).
- Same issue in the thumbnails `.mini-canvas` / `.mini-poster` (`720-738`) — lower priority, but fix the `background:#fff` letterbox there too if it's cheap.

**Critical accuracy point:** the real printed placement is computed server-side by `computePrintPlacement()` (`server.js:7550`) with `productAspectFromSize()` (`server.js:7532`). Its behavior for our portrait artwork on any of these products: **artwork width fills the print area at scale 1, and the vertical position is biased upward (3% top margin) so the crop is taken from the bottom (feet), never the head.** The mockup must match that, i.e. CSS equivalent is:

```
object-fit: cover; object-position: 50% 0%;   /* approximately — top-biased, no bars */
```

That single change kills the white bars **and** makes the on-screen preview an honest representation of what ships. Do not "fix" the bars by padding or by a white mat — that hides the real crop.

Real print sizes (from `UPSELL_PRICES`, `public/index.html:2856-2867`, matching `PRODUCT_CONFIG` in `server.js:7500`):

| product | sizes |
|---|---|
| canvas | 8×10, 11×14, 16×20 (11×14 and 16×20 support framed) |
| poster | 9×11, 11×14 |

### Item 3 — post-purchase destination

- `#confirmContinueBtn` wiring, `public/index.html:4061`:
  `(upsell.returnScreen === 'hub' ? showHub() : showMacroScreen())`
- **The real bug:** Stripe embedded checkout returns via a full page load with `?session_id=…`, handled by `checkOrderSession()` (`3826-3837`) inside `DOMContentLoaded` (`3946`, `checkOrderSession()` call at ~`3960`). A page load resets the in-memory `upsell` object (`2880-2894`), so `upsell.returnScreen` is `null` by the time the confirmation screen renders — which is exactly why Dan lands on the Macro Tracker. Changing only line `4061` will fix it for the (rare) no-reload path but not the real one.

---

## The work

Each item = its own commit + local browser verification + push + live-verify on absbyai.com, per `AGENTS.md`.

### Item 1 — "Print My Future Self" link under the hub hero

- Add a centered text-button immediately below `#hubHero` (inside the same wrapper so it visually belongs to the images), id `hubHeroPrintLink`, label **"Print My Future Self"**. Small and understated — a link-style button, not a full CTA bar. Suggested style: accent color, ~13.5px, 600 weight, centered, ~10px top margin.
- Wire it to the existing `showHubPrintUpsell()`.
- Show/hide it in lockstep with `#hubHero` (`4743-4745`) — it must never appear when there is no goal image to print.
- **Native-app gating:** printed products are *physical* goods and are allowed in the iOS/Android wrappers (this is why the existing print card is the one purchase surface not carrying `app-hide-purchase`). Confirm the existing print flow is visible in-app before deciding — but the default is: do **not** add `app-hide-purchase` to this link.
- Keep the existing `#hubPrintUpsell` preview tile as-is; this is an addition for members, not a replacement.
- Add a `source` property to the existing `print_upsell_clicked` PostHog capture (`'hero_link'` vs `'tile'`) so Dan can see which entry point converts.

### Item 2 — poster-on-a-wall mockup with true relative sizing

Rewrite the customize-screen mockup (`selectProduct()` mockup render, `3687-3693`, plus CSS `741-765`) as a small **wall scene**:

- **Scene:** a subtle wall background (soft neutral gradient), a faint floor/baseboard line, and a drop shadow under the frame so it reads as hanging on a wall. Keep it tasteful and on-brand — this is a $18–87 product, the scene should make it feel worth it, not cartoonish.
- **Reference object for scale:** something unambiguous and simple, drawn as **inline SVG or pure CSS** (no external image files — the app must stay self-contained and works inside the native wrappers). Recommended: a simple side-table or console with a small plant, or a doorway edge. A human silhouette is an acceptable alternative but risks looking odd next to the user's own photo. Pick one, keep it low-contrast/greyed so it never competes with the artwork.
- **True relative sizing (the important part):** derive the mockup box from the actual print dimensions in inches, at a fixed pixels-per-inch scale shared by the whole scene, so 11×14 is visibly larger than 9×11 and 16×20 is clearly the big one. Parse inches from the size key (same `(\d+)x(\d+)` shape as `productAspectFromSize`) or add an explicit inches map next to `UPSELL_PRICES`. Cap the largest size to fit a 375px-wide viewport and let the others scale down proportionally from there.
- **Re-render on size change:** the size chip click handler (`3702-3709`) currently only updates price. It must also re-render the mockup so the size change is visible. Extract a `renderMockup()` and call it from both `selectProduct()` and the chip handler.
- **Artwork fit:** `object-fit: cover` with a top-biased `object-position`, mirroring `computePrintPlacement()`. Remove `background:#fff` from the img rules so no bars can appear.
- **Canvas vs poster:** keep the distinction — canvas gets the wrapped-edge/thick-frame treatment (existing inset box-shadow idea is fine), poster gets a thin flush print. The framed canvas toggle (`#frameToggleWrap`, `3714-3724`) should also update the mockup (add a visible frame border when framed) — nice-to-have, not required.
- Optionally apply the same `cover` fix to `.mini-canvas` / `.mini-poster` thumbnails (`720-738`) so the product-list screen loses its bars too.
- **Verify on mobile width (375×812) first** — that's where nearly all traffic is. Also check 16×20 canvas doesn't overflow, and that the scene doesn't push the price + checkout button below the fold.

### Item 3 — return to the member hub after purchase

- **Persist the return destination across the Stripe reload.** Before `handleCheckout()` opens the embedded checkout (`3742-3810`), write `upsell.returnScreen` to `sessionStorage` (e.g. `absbyai_upsell_return`). In `checkOrderSession()` (`3826-3837`), read it back into `upsell.returnScreen` before `showScreen('confirmation')`, then clear the key.
- **Change the default.** At `4061`, a logged-in user with no recorded return screen should go to `showHub()`, not `showMacroScreen()`. Keep `showMacroScreen()` only for the logged-out/no-account path if that's still the desired first stop there — confirm by reading `showMacroScreen()`'s gating; if it works for logged-out users, leaving it as the logged-out fallback is fine.
- Apply the same default to `#productSkipBtn` (`4015-4018`), which has the identical "fall through to macro" behavior — a member who skips the print should also land back on the hub.
- Keep `transformations` as a return destination when it was set (`5181`).

---

## Verification checklist

Local (browser, 375×812 and desktop):
- [ ] Hub hero link appears for a member with a goal image, absent when `#hubHero` is hidden, opens the print selector, and the back button returns to the hub.
- [ ] No white bars on any product/size, canvas or poster, in the customize mockup or the product-card thumbnails.
- [ ] Selecting 9×11 then 11×14 (and 8×10 → 16×20 on canvas) visibly changes the mockup size relative to the reference object.
- [ ] Price and Proceed-to-Checkout remain reachable without scrolling past the fold on mobile.
- [ ] No console errors; `node --check` on any extracted inline JS.

Live on absbyai.com (required before the task is done):
- [ ] Log in as a member, confirm the hero link renders and routes.
- [ ] Walk to the Stripe checkout screen for a poster and a canvas and confirm the mockup (stop before paying).
- [ ] **One real end-to-end purchase is the only way to fully verify item 3** (the Stripe return path). Dan's call whether to spend ~$18 on a real poster order — this would also close the still-open verification of the `images-api.printify.com/<id>` artwork form noted in `AI_COORDINATION.md`, so there's a second reason to do it. If Dan declines, verify by simulating the return: load `absbyai.com/?session_id=<a real completed session id>` or temporarily stub `checkOrderSession` locally.

---

## Cautions

- Do **not** touch `/api/stripe/create-checkout`, `fulfillProductOrder`, `PRODUCT_CONFIG`, `productVariant`, or `computePrintPlacement`. The server-side price gate and the imageId-only artwork rebuild are the July 17 N1 security fix — leave them alone.
- Do not change `UPSELL_PRICES` values; they must stay in sync with `PRODUCT_CONFIG` prices in `server.js`.
- `AI_COORDINATION.md` currently has an active Claude Code task (ensemble bake-off). Record this task there before starting, and reset per the working rules when done.
- Repo has many untracked local files; commit only `public/index.html` (and this handoff) for this task.

---

## Model and effort recommendation

**If usage budget is comfortable:** Claude **Opus 4.8**, effort **high** for item 2 (it's a visual design task with real judgment — wall scene, scale metaphor, mobile fit — and a bad result is immediately obvious to Dan), and **medium** for items 1 and 3, which are small and mechanical. Doing all three in one session on Opus/high is fine and probably simplest.

**If conserving usage:** Claude **Sonnet 5**, effort **medium**, is adequate for items 1 and 3 — both are a handful of lines in known locations, fully specified above. Still prefer **Opus 4.8 / high** for item 2; a downgraded model tends to produce a generic grey box rather than something that reads as a poster on a wall, and this is the piece meant to increase conversion.

Not recommended for Codex here: the valuable part of this task is visual taste plus live in-browser verification against a production site, which is the Claude Code workflow already established for this project.

---

## Starter prompt for the next session

> Execute `handoff-20260723-print-upsell-improvements.md` in the Abs By AI project root. Three client-side changes to `public/index.html`, each its own commit + local browser verification at 375×812 + push + live-verify on absbyai.com: (1) a small centered "Print My Future Self" link under the member hub hero images wired to the existing `showHubPrintUpsell()`; (2) rebuild the customize-screen product mockup as a poster-on-a-wall scene with a scale reference object, true relative sizing per print size, and `object-fit: cover` with a top-biased position so the white letterbox bars are gone and the preview matches the real Printify placement; (3) return the user to the member hub after purchase instead of the Macro Tracker, persisting `upsell.returnScreen` across the Stripe page reload. All file/line pointers and the root causes are in the handoff — don't re-derive them. Update `AI_COORDINATION.md` when you start and when you finish.
