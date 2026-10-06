---
name: review-page-what-i-decided
description: "Dan 2026-09-30: every video approval packet uses the RO-16 page layout with a \"What I decided\" list; standard for Claude and Codex"
metadata:
  node_type: memory
  type: feedback
  originSessionId: b2d06566-870f-4758-972d-403d6c6ca76b
  modified: 2026-09-30T16:55:28.209Z
---

Every video approval packet is ONE local page in this order: first minute (player) on top, AI opener/new AI clip START+END frames below, a "What I decided (overrule anything)" list, then every graphic and clip in timeline order, three per row (still on its real frame, ID, times, copy, speech before/during/after), then one reply box.

**Why:** Dan on RO-16 round 1 (2026-09-30): "I like this 'What I Decided' section. Let's make this the standard way to do things going forward... so I can look over your decisions just in case I need to revise any of them." The layout is "significantly faster" than reviewing items one at a time in the browser panel. He called RO-16 "the best video we've ever edited... This is the process that we need."

**How to apply:** follow `.claude/skills/_shared/PRE-RENDER-APPROVAL.md` "The review page" section; generator to copy: `.claude/skills/longform-edit/reference/ro16/page.py`. Keep the decisions to genuine questions; everything Claude checked goes in "What I decided". Related: [[decision-budget-per-video]], [[codex-stepwise-editing-approach]].

**Added 2026-09-30 (RO-10 round 1):** every moving graphic gets a "Play it moving, in context" button feeding one shared player (3 s of speech either side). Dan: "I really like what you did with the review page, with the 'Play it moving in context' button. Let's lock that into the skill." He approved all 15 HyperFrames graphics with no copy changes. Generator to copy now: `.claude/skills/longform-edit/reference/ro10/page.py` + `review_media.py`. See [[hyperframes-decision]].

**2026-10-02 (Dan, Ad 13 round 2):** the shared context player floats in a fixed panel at the right on a wide screen, the page scrolls in the middle; every video must be scrubbable, so serve review pages with `.claude/skills/_shared/review_server.py PORT DIR`, never `python3 -m http.server` (no byte ranges, the timeline cannot be clicked). Rule: PRE-RENDER-APPROVAL.md.
