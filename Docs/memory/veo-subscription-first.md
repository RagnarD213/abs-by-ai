---
name: veo-subscription-first
description: "Veo clips default to Google Flow on Dan's AI Pro credits via the flow-veo background agent; paid API only on \"rush\" or approved after credits run out"
metadata:
  node_type: memory
  type: feedback
  originSessionId: f9114820-144b-4b8f-9850-bb7616940457
  modified: 2026-10-17T19:10:01.135Z
---

Every Veo motion clip is generated in Google Flow (flow.google.com) on Dan's Google AI Pro credits by a background sub-agent driving his Chrome (`.claude/agents/flow-veo.md`, runbook `_shared/veo/FLOW-RUNBOOK.md`, helper `_shared/veo/veo.py`) while the main agent keeps editing. The paid Replicate API only when Dan says rush, accelerate or as fast as possible; when credits run out, ask him before paying.

**Why:** Dan, 2026-10-17: "Default to the subscription; switch to the paid API only when I say rush, accelerate, or as fast as possible. If the subscription credits run out, ask me before paying."

**How to apply:** queue clips with `veo.py add`, spawn flow-veo in the background, gate the takes as usual. Flow's "Visible watermarking" switch stays off (no visible mark on 1080p downloads, verified 2026-10-17). Flow's frame picker re-sorts during uploads: pick frames by exact name; `veo.py collect` rejects takes that do not open on START. Related: [[model-routing-plan]], [[frame-approval-before-motion]].
