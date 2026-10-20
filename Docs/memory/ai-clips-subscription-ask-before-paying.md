---
name: ai-clips-subscription-ask-before-paying
description: "Dan 2026-10-20: every AI video clip is generated on the Google Flow subscription by default; any paid generation is asked for every time; his 'rush' is the authorization"
metadata:
  type: feedback
---
Dan, 2026-10-20, answering the audit's budget question: "default to generating everything on subscription and default to asking for authorization every time it needs to go outside subscription. If it's a rush, I'll authorize the pay."

**Why:** the per-video dollar caps (VIDEO-RULES "Video clip generation budget") were being read as standing permission to use the paid Replicate API; he wants paid runs to be a conscious yes each time.

**How to apply:** queue every clip through `_shared/veo/veo.py add` and the `flow-veo` agent (Claude) or the Flow runbook (Codex). Credits out or a slow queue: stop and ask once, with the clip count and the dollar estimate; proceed only on his yes. "Rush", "accelerate" or "as fast as possible" in his own words for that video is the yes. The dollar caps bound an authorized paid run; they never pre-authorize one. Rule text: VIDEO-RULES "AI video clips: Google Flow subscription first" and the budget section. Related: [[model-routing-plan]], [[audio-joins-smooth-before-ship]].
