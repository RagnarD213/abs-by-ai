---
name: my-transformations
description: "shipped July 2026 — before/after gallery with sliders, share composite, hero swap + program rebuild, per-card print; endpoints and design decisions"
metadata: 
  node_type: memory
  type: project
  originSessionId: ae5bf0de-f0f5-4a89-96f3-e297140d2f51
---

My Transformations shipped July 10, 2026 (commit 584f998, live on absbyai.com; 28-test API suite passed on prod).

- New `transformations` table (30-row cap/user, oldest dropped on insert). One `is_hero` row = the hub-hero pair, always mirrored into legacy `users.before_image/after_image` so [[accounts-member-hub]] hero + trainer photo path stay consistent.
- Endpoints (all requireAuth): `GET /api/transformations?before=<id>` (pages of 10, lazy-migrates the legacy users pair on first call), `POST /api/transformations` (dedupes when newest row has identical after image — the login/hub repeat-fire), `POST /api/transformations/:id/hero`, `DELETE /api/transformations/:id` (hero delete promotes newest remaining; last delete nulls users cols).
- Legacy `POST /api/account/transformation` still works and now also inserts into the gallery.
- Frontend: `#transformationsSection`, side-by-side before/after cards with BEFORE/AFTER pills (Dan rejected the drag sliders — removed in b76c05a; don't reintroduce), share = 1200×900 branded canvas composite (Web Share API → download fallback), print reuses Printify upsell via `upsell.imageDataUrl`/`upsell.returnScreen` (cleared in showEmailScreen), set-as-goal offers members-only program rebuild using the saved program intake + new photo pair.
- Untested on prod: actual program rebuild call (needs Claude key — see [[load-time-optimizations]]) and a real Stripe print checkout from a gallery card (see [[printify-print-flow]]).
- Dev fix in same commit: BACKEND_URL on localhost now uses the page's own origin instead of hardcoded port 3000 (multiple local dev servers no longer cross-talk).
