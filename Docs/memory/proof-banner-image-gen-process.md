---
name: proof-banner-image-gen-process
description: "For male marketing/proof images, use the live product pipeline (real UI flow), not ad hoc direct API prompt engineering"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f03cb3db-cb55-43c0-86ac-0c8107c80c0f
---

When generating male before/after marketing images (e.g. proof-banner slides), use Abs By AI's actual live/real generation process (the real product flow a user goes through) rather than crafting custom one-off prompts directly against the Gemini API outside that flow.

**Why:** During the [proof-banner-upgrade](proof-banner-upgrade.md) slide-3 work (2026-07-19), Claude tried a custom ad hoc approach (hand-written prompts, generate-after-then-add-weight ordering, various forceful retries) calling `/api/generate-image` directly, and got weak/no-op results on the male heavy-body direction after ~15 attempts. Dan then generated a matching before/after pair himself using "the real process" (the live product) and it came out dramatically better — same identity, convincing dramatic overweight-to-fitness-model-abs transformation in a believable beach setting. Dan's explicit instruction: "in the future, this process of going outside our real process isn't the best for men. Let's just use the live process for men because it produced way better images than your process."

**How to apply:** For future male marketing/test image generation, drive it through the actual app UI (or the exact same request shape a real user's browser sends — full system prompt via `/api/generate-prompt` + `/api/generate-image` with the real client-built prompt) rather than substituting a hand-written custom prompt. If a custom direct-API approach is being considered for male images, default to using the live process instead, or check with Dan first. (This finding was specifically about the male direction; the female heavy-body ceiling documented in `AI_COORDINATION.md` A3.1 was investigated separately and led to Option A there.)
