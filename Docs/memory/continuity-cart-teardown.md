---
name: continuity-cart-teardown
description: "10-02 screenshot-led cart research (HBI, V Shred, Gundry, NativePath, Stansberry, BODi) + how to capture carts; quiz apps blocked on consent boxes"
metadata:
  node_type: memory
  type: project
  originSessionId: cc8d248b-2cd9-46a6-bad0-cb66c205b667
  modified: 2026-10-02T18:35:13.241Z
---

Artifact "Continuity Cart Teardown" (2026-10-02): https://claude.ai/artifact/SCgHKoUcyN5mik1NvZLfmD. Builds on the 09-10 Cart Teardown ([[web-cart-pay-first]]). Screenshots: `Docs/cart-research-20261002/` (local only, not committed). Source HTML + notes were in the session scratchpad.

**Dan ran ads for Healthy Back Institute.** The cart he used and trusts from first-hand results is the Heal-n-Soothe free-trial cart on shop.healthandwellnesstools.com (`/funnels/hns/op-heal-n-soothe-free-trial.html`; two-option version `...-free-trial-ot.html` with "Buy 1 Get 1 Free $59" above a pre-selected "Free Trial Bottle $9.95 S&H"). Free bottle for $9.95 shipping, auto-enrolled at $49.95 + $3.95 every 30 days, a titled "How this FREE Trial Offer Works" box plus a required empty tick box directly above the button. In VidTao the spend sits under company "SW Management" / brand "Dr. Brian Paris" (brandId 15259), not under "The Healthy Back Institute".

**How to capture (what worked):**
- VidTao direct URLs: `/dashboard/brands?keyword=X&selectedCategoryIds=%5B0%5D&selectedCountryId=0&selectedSoftwareIds=%5B%5D&selectedDurationIds=%5B%5D&resultsPerPage=25&page=1`, brand page `/dashboard/entity-info?brandId=N`. Clicking an ad row opens a modal that lists "Landing pages".
- Full-length cart image: headless Chrome from Bash (`--headless=new --screenshot --window-size=1100,H --user-data-dir=<scratch>`); it does not exit by itself, so wait for the file then `pkill -f` on the scratch profile path only. Cloudflare-protected pages (V Shred) return a verification screen; leave them.
- When Dan's Chrome window is in the background, pages report `visibilityState: hidden`: timers throttle and screenshots come back blank. Quiz loaders can be advanced by replacing setTimeout/setInterval/rAF with a manual queue and pumping it from `javascript_tool`.
- Chrome `javascript_tool` output is cut near 1,000 characters and is blocked when it contains `?`, `&`, `=` URL fragments.

**Why:** Dan wants his own cart modelled on proven direct-response carts ([[proven-direct-response-only]]).
**How to apply:** MadMuscles and Muscle Booster paywalls were walked on 10-02 after Dan gave a standing OK for consent boxes ([[research-funnel-consent-standing-ok]]); BetterMe and Noom were not walked. Quiz funnels: use the built-in Browser pane at the mobile preset; Muscle Booster needs touch events dispatched on the elementFromPoint target. The artifact ends with a top-to-bottom recommended cart and five decisions for Dan before the design task.
