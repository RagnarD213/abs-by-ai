---
name: printify-print-flow
description: How Abs by AI fulfills printed-product orders (Printify) and the no-crop placement caveat
metadata: 
  node_type: memory
  type: project
  originSessionId: 75a6a3bb-935f-48f1-a6e4-0ebb99605e1d
---

Printed products (canvas/poster/keychain) are fulfilled via Printify, wired in `server.js`:
- `/api/printify/upload-image` uploads the generated PNG, returns `{imageId, previewUrl, width, height}`.
- `/api/stripe/create-checkout` makes an embedded Stripe session; stores `imageId/imagePreviewUrl/imgWidth/imgHeight/productType/size/framed` in metadata.
- Webhook + `session-status` both route by metadata: `productType` → `fulfillProductOrder()`, else credits. Idempotent via `creditsStore.fulfilled["order_"+sid]`.
- `PRODUCT_CONFIG` holds blueprint/variant IDs + hardcoded costs.

**Background:** the deployed `server.js` had drifted to a credits-only version that had *dropped* the entire Printify flow (it lived in older commit `2c06f56`). Reconciled 2026-06-22 by merging it back in.

**No-crop fix (`computePrintPlacement`):** prints were cutting off heads because a single hardcoded placement (`scale:1,x:.5,y:.5`) was used for every product aspect. Now placement is aspect-aware: wider-than-product → scale to fill height (crop sides); taller-than-product → keep width, bias `y` up so the crop comes off the feet, never the head. Also added a FRAMING lockdown to the generation prompt in `index.html` so Gemini keeps the full subject + headroom.

**CAVEAT — validate with a real order:** the placement math assumes Printify's `scale=1` = image width fills the print area and `y` = image-center fraction from the top. This was NOT live-tested (no Printify keys locally). Place one real test order per product type and confirm the head isn't cut before trusting it. See [[pay-for-generations]].
