---
name: ad-vs-organic-classification
description: "Dan 09-28: classify every video as ad or organic from its closing CTA before upload; flag a handoff that disagrees and wait"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 180309aa-fcc4-4cf8-b819-3bc1a4251f11
  modified: 2026-09-28T22:15:53.243Z
---

Before uploading or setting up ANY video, decide from the finished file's own ending whether it is an ad or organic.
Ad = a definite direct-response CTA ("tap the button below"). Organic = a softer end CTA ("go to AbsByAI.com",
"leave me a comment") with no tap-the-button line. If a handoff or request labels it the other way, tell Dan (quote
the closing line) and wait before any upload.

**Why:** 2026-09-27 a handoff sent DS-18 (organic Short ending "Leave me a comment") through /ad-setup: Unlisted upload
+ two Google Ads groups that spent $0.62. Dan: "If I mistakenly give you a handoff to set up an organic video as an ad
... let me know before doing it."

**How to apply:** rule lives in `_shared/VIDEO-RULES.md` ("Ad or organic?") and Step 0 of /ad-setup and /video-setup.
Related: [[ads-never-organic]].
