---
name: sonnet-for-assembled-rounds
description: 10-05 evidence and recommendation: Sonnet 5.5 built RO-13 round 2 (full film from a locked plan) to a SHIP verdict; when Sonnet is fine for video rounds and when it is not
metadata:
  type: project
---

RO-13 round 2 (a full film built from a locked, approved plan) was run on Sonnet 5.5 on 2026-10-05 at Dan's request and ended SHIP on the second candidate (Opus ra-reviewer both times). Dan asked whether Sonnet can take rounds 2 to 4 going forward.

**Recommendation given (Dan has not yet changed AGENTS.md routing):** Sonnet for assembly rounds where the plan, graphics, clips and look are already locked and approved: full-film build, gates, SRT/chapters, delivery, bookkeeping, and revision rounds whose notes are specific timestamped fixes. Opus for round 1 (creative choices, first minute, frames), for every independent review, and for revision rounds whose notes are judgment calls or touch several systems. Escalate to Opus after one failed review caused by something other than a newly written rule.

**Why / what went wrong on Sonnet:** (1) the 10-04 belly rule was written after the session read VIDEO-RULES.md, so review 1 failed; a rule-change check would have caught it on any model. (2) HyperFrames shared code changed under the locked renders (side-list drift default) and the audio EQ fit from the first minute failed the whole-film tone row; both were caught and fixed. (3) one false claim ("sidecar built", the job had been killed) was caught and corrected. Mechanical steps (render, chain, gates, delivery) went cleanly.

**How to apply:** every round-2+ handoff should tell the executor to `git log --since=<approval date> -- .claude/skills/_shared/VIDEO-RULES.md` and re-read new rules before building, pin shared-template defaults that the approval depended on, and verify a background job's end marker before reporting it done.
