---
name: google-ads-ga4-link
description: GA4 property "Abs By AI" (G-1M1SY7GGKF) rides the existing Ads gtag loader and is linked to Ads 342-717-0837; imports no conversions
metadata:
  type: project
---

Set up 2026-09-11 for the Google Ads rep. **Measurement ID `G-1M1SY7GGKF`**, property **Abs By AI `553864929`**,
web stream **absbyai.com `15763007741`**, inside GA account **SixPackAbs.com `145219380`** (the only GA account
Dan has). Linked to Google Ads **342-717-0837**, personalized advertising on.

- **One gtag.js, two destinations.** GA4 is a second `gtag('config', …)` beside `AW-18361229851` on all 11
  pages in `public/` that carry the loader. Never add a second loader script.
- **Never accept GA4's "Use the Google tag found on your website"** — it warns it will overwrite that tag's
  settings, and the Ads tag carries `allow_enhanced_conversions`. Install manually and add the config in code.
- **GA4 imports no conversions, deliberately.** The gtag conversion actions stay primary and a GA4 import would
  double-count. Any key event the rep wants goes in as secondary/observation-only.
- `fireAdVirtualPageview()` sends to both destinations. Without that GA4 sees one page_view per session — the
  SPA changes screens without touching history.
- The property is in the SixPackAbs account only because creating a *new* GA account forces a Terms-of-Service
  click, which Claude may not do for Dan. A property inside an existing account raises no prompt.

Related: [[google-ads-api-client]], [[vsl-landing-page]], [[cross-platform-retest-rule]].
