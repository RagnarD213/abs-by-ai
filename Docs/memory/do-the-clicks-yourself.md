---
name: do-the-clicks-yourself
description: "Dan wants Claude to do every browser/UI step it can (open pages, click, add to cart) and hand over only payment/credentials; never list \"click X\" steps for him"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 2434df47-7609-49b1-9b9b-031d9def6158
  modified: 2026-11-05T14:37:42.910Z
---

When a task ends at a web page Dan has to act on, drive it as far as the safety rules allow (navigate, click Sample order, tick products, add to cart, fill non-secret fields). Hand over only the last step that truly needs him: entering payment or passwords, and the final pay/submit click.

**Why:** 2026-11-05, SixPackAbs Supliful proof order. I told him to click "Sample order" himself and pick the six products. He replied: "Stop asking me to do things that you can do yourself. I need you to be more like ChatGPT, where you can handle things like this."

**How to apply:** Never write a next step that is a click or selection I can make. Next-step boxes list only what needs Dan: payment, a decision, a review. Stop before payment and before any irreversible submit; say plainly where I stopped and what is in the cart. Related: [[bias-toward-action]], [[autonomy-credentials-framing]], [[personal-info-form-entry-ok]].
