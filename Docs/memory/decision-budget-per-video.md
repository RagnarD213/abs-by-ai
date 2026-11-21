---
name: decision-budget-per-video
description: "Dan 2026-09-29: at most 10-15 decisions per video in total; Claude decides and locks everything it can check, asks only real taste calls"
metadata:
  node_type: memory
  type: feedback
  originSessionId: a70446de-2b37-49ed-a90b-1231d2dd727e
  modified: 2026-09-29T19:07:37.974Z
---

On 2026-09-29, shown RO-05 round 3 (about 50 per-item approvals: every graphic and clip as a moving preview), Dan said: *"This is way too complicated... I can't be approving this much stuff per video... Just go with what you think is best for most of this and reduce it to 10 to 15 decisions max. Only for things that legitimately need my decision, just make most of the decisions yourself here."*

**Why:** per-item approval of work Claude already checked costs Dan hours and adds nothing; he still judges the first minute and the finished film.

**How to apply:** keep building in steps ([[codex-stepwise-editing-approach]]), but Claude approves what it can verify (sync, face/hair clearance, copy vs speech, standing rules). Ask Dan only genuine taste calls, facts only he knows, or changes to something he locked: 10 to 15 per video in total, fewer is better. Open every packet with a one-line-each "what I decided" list he can overrule. Rule text: `.claude/skills/_shared/PRE-RENDER-APPROVAL.md` (Decision budget section). Related: [[batch-approval-once]].

**Note 2026-10-20 (skills audit):** VIDEO-RULES "Organic content approval budget" (also dated 2026-09-29) records a different figure, at most 20 decisions in round 1 and 10 or fewer in each later round, and says it replaces the 10 to 15 per video above. The shared files now point at the VIDEO-RULES figure; Dan is asked in `Docs/DAN_DECISIONS.md` which he means. Either way: Claude decides what it can check and asks only real taste calls.

**Dan answered, 2026-10-20 evening:** keep the current page: the major decisions up top (first minute, colour correction, audio, chroma key when it applies), every graphic and small item below for a quick scan, even fifty of them. The numeric caps bound the questions asked, not what is shown.
