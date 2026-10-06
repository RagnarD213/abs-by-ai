---
name: evening-planning-process
description: Since 2026-09-10 Dan runs /prioritize at END of day for the next day; the morning brief links back to that chat via next-day-plan.json
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 3592d80b-1f6d-4569-96b9-d686d04e0072
  modified: 2026-09-10T23:55:41.832Z
---

Dan moved daily planning from the morning to the evening (2026-09-10, trial): he runs `/prioritize` at the end of the day to plan TOMORROW, and the 6 AM morning brief links him back to that chat so he can copy the starter prompts and fire the sessions.

**Why:** he wants to wake up to a decided day rather than spend the morning deciding; Claude-intensive sessions go first thing in the morning (his standing preference), his own offline/physical work in the afternoon.

**How to apply:**
- An evening /prioritize plans for tomorrow's date: write `~/.claude/scheduled-tasks/abs-by-ai-morning-brief/next-day-plan.json` (forDate, sessionId, sessionTitle, link, oneThing, fire, dan), set `/api/plan` to tomorrow, rename the chat "Plan for <Day MM-DD>".
- The link is `claude://code/continue?session=<local_… id from get_session self>` — verified against the Claude app's handler 2026-09-10 (`^local_[A-Za-z0-9-]{1,64}$`, looked up among NON-archived sessions). Never archive a planning chat before its day is over.
- The brief renders it as element 1b and uses `oneThing` as its one thing.
- Still no execution in the planning chat ([[bias-toward-action]] exception); mechanics live in the /prioritize skill.
