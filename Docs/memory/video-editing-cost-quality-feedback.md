---
name: video-editing-cost-quality-feedback
description: "Dan's 2026-09-14 feedback that Claude/Fable video editing is too expensive and not publishable quality; he is trialing Codex and Grok as alternatives"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: bac19e3b-66d0-47cc-8460-618b9fe342ab
  modified: 2026-09-14T13:43:20.985Z
---

Claude's own video-editing pipeline (Fable-driven ad/longform builds via the `/ad-edit`, `/longform-edit`, `/shortad-from-longform` etc. skills) is not meeting the bar on either axis Dan cares about: the finished quality isn't something he can publish, and the sessions burn his whole usage limit for what he gets back — mostly just square/vertical reformats of existing cuts, not new usable finished video.

**Why:** Dan's own words (2026-09-14, /prioritize): "Claude isn't producing good enough videos. The quality just isn't something I could publish, and it's also too expensive. I use my whole limit, and I'm not really getting much usable other than the square and vertical versions." This lands on top of [[video-editing-strategy-report]] (the "Muhammad Standard" finding that approvals only ever came where the design was fixed/copied from an approved master, never from open-ended builds).

**How to apply:**
- Don't default to recommending another big Fable-driven video-editing session as the plan for "more content" — the cost/quality tradeoff is currently failing Dan's own bar.
- He is running parallel trials of **Codex** (tracked: `Handoffs/codex-video-trial/`, numbered steps 01–09, decision due ~Oct 9–11) and **Grok/Grokbot** (as of 2026-09-14 this trial is real and running but NOT YET recorded anywhere in `AI_COORDINATION.md` or `Handoffs/` — the first session that gets details from Dan should write it up alongside the Codex trial so it isn't lost).
- When Dan asks to prioritize or asks what to build next, prefer steering him toward finishing/evaluating these external-tool trials over spinning up more native Fable video builds, until a trial produces a cheaper and/or higher-quality alternative.
- Reformats of an already-approved master (squares/verticals from a locked cut) are the one category still working reasonably — that's consistent with the Muhammad Standard finding, not a contradiction of this note.
