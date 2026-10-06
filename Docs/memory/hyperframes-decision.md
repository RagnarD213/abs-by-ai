---
name: hyperframes-decision
description: "PILOT + 3 TEMPLATES APPROVED 2026-09-30 (cycle, lower-third, before-card, side-list in _shared/hyperframes/; text lands on words; diagrams in the left-third card beside Dan); research: adopt HyperFrames (HeyGen, Apache 2.0) as the motion-graphics layer only, Soft Blue Light stays; Remotion is the fallback; pilot handoff written; what makes Nate Herk's graphics good is method, not the tool"
metadata:
  node_type: memory
  type: project
  originSessionId: 16b33780-95dd-4175-927b-9bf3ebe8f8a9
  modified: 2026-09-30T17:16:38.226Z
---

On 2026-09-30 Dan asked for deep research on HyperFrames (the tool Nate Herk uses with Claude Code) and its
alternatives, to get motion graphics at Nate's level in ads, VSLs, content videos and Shorts. Report:
`Docs/HYPERFRAMES_RESEARCH.md`. Pilot: `Handoffs/handoff-20260930-hyperframes-pilot.md` (rebuild the C1652
"downward spiral" cycle in Soft Blue Light, old vs new for Dan; Opus 5.5 high).

Recommendation delivered: **HyperFrames as the graphics layer only.** Cut, audio chain, gates, delivery and the
Soft Blue Light lock stay; transparent ProRes 4444 overlays drop into the existing ffmpeg composite. Remotion is the
runner-up (React, licence free only to 3 people; HeyGen ships a porting skill). Motion Canvas is dead; After Effects
MCPs cannot drive MOGRTs; template clouds are per-render and template-bound.

Key finding: Nate's quality comes from five habits, not the renderer: word-level transcript timing, cut first,
plan mode beat sheet before HTML, timestamped feedback with frame verification, and turning every approved
result into a skill. His shipped design rules (MOTION_PHILOSOPHY.md in nateherkai/hyperframes-student-kit): light
over colour, 90 percent dark frame, something always drifting, arrows draw on, spring settles, one hue per meaning,
easing table. Our graphics across RO-01, RO-05, RO-16, WV-01 and C1652 are all flat rectangles with fade/slide
entrances; that is the gap.

**Pilot result (2026-09-30):** Dan approved the C1652 spiral rebuild: *"significantly better than the graphics that
we're using. This really shows me the potential."* Layout call: a diagram of short items goes in the left-third card with
him on camera beside it; full screen felt "a little bit empty". Template: `.claude/skills/_shared/hyperframes/cycle/`
(README there has word rules, easing table, reframe-by-crop-shift method). Next: `Handoffs/handoff-20260930-hyperframes-templates-round2.md`
(lower third, before card, 3A list as samples on RO-16 footage), then the first full video from templates, then Codex.

**Round 2 (2026-09-30):** Dan approved all three: *"All three approved."* Templates `lower-third/` (point in parts on
the words, optional long-vs-short counter bar, `_mask` pass for the glass blur), `before-card/` (live Soft Blue field,
count-up, chip with the photo), `side-list/` (3A exact, items on their words, superseding the fixed 0/0.25/0.50 s).
Traps: renders are untagged BT.601; launchd http.server cannot read /Volumes (serve review pages from /Users/Shared).
Next: `Handoffs/handoff-20260930-first-full-video-from-hyperframes-templates.md` (RO-10 recommended).

**How to apply:** when a video skill builds graphics after the pilot is approved, use the approved HyperFrames templates
under `.claude/skills/_shared/hyperframes/` for lower thirds, before cards, 3A lists and cycles instead of hand-coding PIL motion. Do not point
HyperFrames at raw-footage edits. Pin its version; it releases several times a day. Related:
[[graphic-lock-and-ai-frames-first]], [[codex-ds17-beat-claude-lessons]], [[video-editing-cost-quality-feedback]].
