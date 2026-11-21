---
name: deploy-drops-locked-holds
description: Every push to main redeploys Railway and wipes the in-memory held (locked) images and the body-analysis cache — never push docs-only commits while someone is mid-funnel; a 410 "no longer available" on unlock/analysis right after a deploy is this, not a bug
metadata:
  type: project
---

Measured 2026-09-08 23:38 UTC: Dan's out-of-credits generation lost its analysis read with
`410 This result is no longer available to analyze` 244 ms after the call — a coordination-file-only
commit pushed two minutes earlier had redeployed Railway, and `heldImages` (locked results, 1 h TTL),
`bodyAnalysisCache` and `attemptCache` in `server.js` all live in process memory.

**Why:** Railway auto-deploys on every push to `main`, docs included; the app is a single replica with
in-memory holds by design.

**How to apply:** batch doc edits into the code commit, or push them when nobody is testing the funnel.
After any deploy, a locked result made before it cannot be unlocked or analyzed — regenerate. If this
bites real users, the fix is a Railway watch-path ignore for `*.md` / `Handoffs/` (a config change, ask
Dan) or moving the holds to Postgres. Related: [[railway-deploy-workflow]], [[local-funnel-test-recipe]].
