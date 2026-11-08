---
name: veo-subscription-first
description: "11-08: Claude and Codex use Google AI/Flow for video first, attempt images there too; paid API fallback only after recorded subscription failure"
metadata:
  node_type: memory
  type: feedback
  modified: 2026-11-08
---

## Google AI subscription first for video and images (Dan, 2026-11-08)

Applies to both Claude and Codex, including exercise demos, editing, marketing and ad hoc generation.
- **Video:** always try Dan's existing Google AI subscription through Flow first. Check its current generation/export options and the actual result; an old note about Flow quality or resolution is not evidence that it fails now.
- **Images:** make an attempt through the Google AI subscription too. Keep required Codex subscription comparisons and blind picks; Codex's subscription remains a cost-saving alternative when needed.
- **Paid API fallback:** only after subscription generation actually fails for the requested asset, is unavailable/out of credits, or produces an output that fails the required quality checks. Save the attempt/result and specific failure before switching. A spending cap, an old API recipe, or the word "rush" alone does not skip the subscription attempt. Dan can explicitly override this rule for a particular job.
- Fallback stays within existing task/session spending limits. State the estimate, track actual spend and explain the fallback; ask only if the applicable authorization or cap does not cover it. No subscription upgrades or credit purchases are implied.
- This supersedes older Codex-only image routing, paid-1080p-first exercise recipes and rush-only API routing in skills, memory and unexecuted handoffs. Preserve required quality gates, source-blind reviews, real-photo pixels and existing approved assets. It does not change the live app's generation for visitors or narration/audio providers.


Dan, 2026-11-08: "we always use a Google AI subscription to save on costs for the video generation. We make an attempt to use it for the images and we only fall back to API if subscription generation fails ... for both Claude and Codex."

Procedure: `.claude/skills/_shared/veo/README.md`, `FLOW-RUNBOOK.md`, and `_shared/blind-image/FLOW-IMAGE-RUNBOOK.md`. Preserve START/END and motion gates, independent reviews, real-photo pixels and required blind comparison sets. Google Flow plan limits and export options must be checked live; old exercise-demo paid1080p recipes do not establish subscription failure. Live app visitor generation and narration providers stay outside this rule.

Veo Fast remains the default; use Quality only when Dan requests it by name. Keep the existing model/take comparison rules in the Veo README. This replaces the October 17/20 rush-only and ask-for-every-fallback rules; budget alone never skips subscription generation. Existing authorizations and caps still limit a paid fallback.
