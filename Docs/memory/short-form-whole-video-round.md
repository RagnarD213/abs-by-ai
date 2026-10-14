---
name: short-form-whole-video-round
description: "Shorts and ads nearly approved: build the whole video in the round, not just the first 30 s (Dan, 2026-10-14)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 1fa9d9a5-e3fc-423e-9bb7-1d46b82f6205
  modified: 2026-10-14T18:54:58.508Z
---

For a Short or an ad, when most assets are approved and nothing in the rest is likely to be turned down, the round that would
deliver the finished first 30 seconds builds and shows the WHOLE video instead. Keep the 30-second step only when the rest holds
something genuinely uncertain (an AI clip he has not seen moving, a new graphic type, an unpicked look). Long-form is unchanged.

**Why:** RA-14 round 3 (Dan, 2026-10-14): "it would have been better in this round to build out the full video because it would be
only another 30 seconds... if we had to regenerate or re-render the video, then it wouldn't take that many resources."
The first 30 s came back fully approved and he had to spend another round on 20 s of already-seen items.

**How to apply:** at PRE-RENDER-APPROVAL step 5 on a short video, check the remaining items; if all are approved or already shown
moving, render the full video for the page. Exact-file gates and the independent review still come before delivery to the ad folder.
Rule text: `.claude/skills/_shared/VIDEO-RULES.md`, first section. Related: [[decision-budget-per-video]], [[edit-queue-artifact-is-working-list]].
