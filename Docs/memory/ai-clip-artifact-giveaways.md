---
name: ai-clip-artifact-giveaways
description: Dan rejects AI clips with giveaway artifacts (breath smoke, fogging mirrors, melting hands) even when labelled; check every AI shot frame by frame
metadata:
  type: feedback
---

Dan, 2026-09-14, on the Ad 3 vertical (otherwise approved): at 1:16 the AI story clip shows a man exhaling and the bathroom
mirror fogging with breath smoke — *"a weird AI artifact… things that just give away that this is AI-generated and make it
seem like it's not a real clip."* It had passed five of Muhammad's revision rounds, our rebuild, five audits and a full
watch pass, because it sits in one corner and grows over 1.5 s.

**Why:** an AI-GENERATED label discloses the clip but does not excuse it looking fake; a giveaway breaks the ad's credibility.

**How to apply:** in any review or build that contains AI shots, read each shot as consecutive full-resolution frames (all of
its last 2 s — Kling/Veo image-to-video degrades toward the end), cropping mirrors, mouths, hands, held objects, backgrounds
and screens. The checklist and item wording live in `/revisions` step 3b; the Ad 3 fix is
`Handoffs/handoff-20260914-ad3-ai-smoke-artifact-fix.md`. When generating new AI clips, run the same check before handing
them over. Related: [[untagged-video-bt601-trap]].
