---
name: ad-retry-rule-and-no-trick
description: "Dan's standing ad rules (2026-09-10) — never use \"trick\" in ad copy (Google flags it as Clickbait); any disapproved/limited ad gets tamer copy, then a tamer thumbnail, then removal"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 6404e80e-aa19-42f7-86b1-84f1ae706f23
  modified: 2026-09-10T15:36:08.371Z
---

Two standing rules Dan set on 2026-09-10 after Google flagged his "late night eating" ad:

1. **Never write "trick" in ad copy** — any platform, hand-written or generated. Google marked the two lines
   that said it ("Here's the AI trick that…", "try this trick…") as **Clickbait**. Enforced for the YouTube
   engagement ads by `scripts/ads/ytads/lint.js` rule `trick`.
2. **A disapproved or limited ad is retried, not appealed**: attempt 2 = new ad with tamer copy; attempt 3 = a
   clean, text-free thumbnail (whole head, hair never cut) on the PUBLIC video + a fresh ad; if both fail, remove
   every ad in the chain (hand-made included) and put the original thumbnail back. "Limited" counts only while
   it is still $0 after 2 days. Automated in the ytads engine — spec in `Docs/YTADS.md` "The retry rule".

**Why:** limited ads in this account have never spent a cent, so a flag silently kills a video's promotion;
Dan would rather iterate the creative than wait on appeals.

**How to apply:** apply rule 1 to any ad copy you write (Meta, Google Search, scripts' on-screen text too).
For rule 2 on Google Demand Gen, the engine does it; do not hand-edit those ads — use `retry:force` events or
the manual queue. Related: [[ad-suspension-prevention]], [[framing-standard-hair-anchored]].
