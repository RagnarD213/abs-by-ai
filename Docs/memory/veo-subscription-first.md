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

**Update 2026-10-21:** Dan upgraded to Google AI Ultra 5x ($99.99/mo, 10,000 Flow credits + 50/day; Veo 3.1 Fast 10 credits, Lite 5, Omni 1.1 Flash 12). Blind bake-off Omni vs Veo Fast on 5 approved pairs: 2 ties, Veo preferred 3, Omni 0, and Omni refused a shirtless shot of Dan ("reputational risk"). Keep Veo 3.1 Fast as the default. Dan, 2026-10-21: generate BOTH Veo and Omni for clips over 8 s, 4/6 s clips, one-detail fixes and multi-reference shots, and whenever in doubt ("I prefer you generate with both"); two Veo takes for hooks/openers; Dan's body shirtless is Veo only. Rule: `_shared/veo/README.md`, "Which model and how many takes".
