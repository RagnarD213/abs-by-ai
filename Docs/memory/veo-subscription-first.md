---
name: veo-subscription-first
description: "AI clips: Google Flow subscription first via flow-veo; Fast by default, Quality only when Dan names it; any paid run needs his yes each time, his rush counts as the yes"
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

## Veo Quality only when Dan names it (10-25) (merged 2026-11-01)

Use Veo 3.1 Fast for every AI clip. Veo 3.1 Quality only when Dan asks for it by name: never "just in case", never as a twin take, never in an unrequested bake-off.

**Why:** the 10,000-credit Ultra allowance ran out in three days (2026-10-20 to 10-23); 48 Quality clips used two-thirds of the logged credits, and Fast won or tied every blind test. Dan, 2026-10-25: "let's make that the standing rule."

**How to apply:** `veo.py add --model quality` refuses without `--dan-asked "<his words>"`. Rule text: `.claude/skills/_shared/veo/README.md`. Related: [[veo-subscription-first]], [[ai-clips-subscription-ask-before-paying]].

## Ask before any paid generation (10-20) (merged 2026-11-01)

Dan, 2026-10-20, answering the audit's budget question: "default to generating everything on subscription and default to asking for authorization every time it needs to go outside subscription. If it's a rush, I'll authorize the pay."

**Why:** the per-video dollar caps (VIDEO-RULES "Video clip generation budget") were being read as standing permission to use the paid Replicate API; he wants paid runs to be a conscious yes each time.

**How to apply:** queue every clip through `_shared/veo/veo.py add` and the `flow-veo` agent (Claude) or the Flow runbook (Codex). Credits out or a slow queue: stop and ask once, with the clip count and the dollar estimate; proceed only on his yes. "Rush", "accelerate" or "as fast as possible" in his own words for that video is the yes. The dollar caps bound an authorized paid run; they never pre-authorize one. Rule text: VIDEO-RULES "AI video clips: Google Flow subscription first" and the budget section. Related: [[model-routing-plan]], [[audio-joins-smooth-before-ship]].
