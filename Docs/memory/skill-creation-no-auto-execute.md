---
name: skill-creation-no-auto-execute
description: "After creating a new skill, do not immediately execute it on the task that prompted it — stop and let Dan start a fresh session"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2fd04753-55d4-4683-ad0f-09adbca66811
  modified: 2026-09-01T00:44:26.261Z
---

After building a new skill, do not go on to run/execute that skill on the next part of the
current task in the same session.

**Why:** Dan wants to start execution of a newly-created skill as a **separate session**, so he
can pick a different model and effort level for it (e.g., build the skill on a stronger model,
then run the batch/task on a cheaper one) and to save tokens in the session that authored the
skill. Said explicitly 2026-08-31, right after `/background-removal` was created, tested end-to-
end on one image, AND then immediately run as a 100-photo batch in the same turn — the batch
execution is the part he wants split off.

**How to apply:** When a session's deliverable is "create a skill for X," stop once the skill is
written and minimally verified (e.g., one test run to prove the script/recipe works — that's fine
and expected). Do NOT then proceed to run the skill over the user's real batch/backlog/full task
in that same session, even if the natural next step is obvious and low-risk. Tell Dan the skill is
ready and give him the invocation (e.g., "invoke `/skill-name` in a new session"), then stop —
mirrors the standing brainstorming-session rule ([[bias-toward-action]] has the general
bias-toward-action default; this is a carve-out specific to skill creation, not brainstorming).
This applies to skill creation regardless of how the skill was built (via skill-creator or
directly).
