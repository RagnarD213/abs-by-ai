---
name: revisions-zero-edit-goal
description: "Dan's goal for /revisions is a doc he forwards unread — when he edits one, diff the Doc against our markdown copy and fold every change into the skill's calibration section"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 3c39cd48-cae0-4a31-a123-7f8bb39d4d15
  modified: 2026-09-03T15:46:14.619Z
---

Dan wants editor revision docs reviewed fully autonomously: he should not have to re-watch the cut
or change anything in the doc before forwarding it (stated 2026-09-03).

**Why:** Re-reviewing costs him the time the skill was supposed to save, and his edits are the only
ground truth for what the reviews get wrong. On 2026-09-03 he asked for the skill itself to be
recalibrated from his edits to the Muhammad batch-2 doc (Ads 3–5).

**How to apply:** Whenever Dan has touched a revision doc, read it back with the Drive connector,
diff it against the byte-exact markdown copy in `revision docs/`, and turn each addition (missed
defect), rewrite (mis-calibrated direction) and deletion (item that should not exist) into a rule in
the "Calibration from Dan's edits" section of `.claude/skills/revisions/SKILL.md`. Run that
section as a self-check before every delivery. See [[revision-docs-in-dans-voice]].

Three passes so far (09-03 rules 1–11, 09-08 rules 12–21, 09-10 rules 22–30). The 09-10 pass added
Dan's three format asks — bold `STANDING RULE:` sub-bullets in canonical wording under every violating
item (Muhammad edits with an AI tool, so identical wording gets learned), bold the key change in each
item, and `APPROVED - FINALIZED - READY FOR HIGH QUALITY EXPORT` for a finished ad — plus his biggest
correction: on round ≥ 2, audio that measures in the window is never re-itemised for tone/NR/−0.8 dBTP.
