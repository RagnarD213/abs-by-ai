---
name: three-role-video-pipeline
description: Dan's 2026-09-16 process for video edits — Fable plans, Opus edits, a fresh Fable instance reviews blind, rulings appended to the plan, max three rounds; first run RA-01 reached ship-clean in 3 rounds
metadata:
  type: project
---

**Dan's requested edit process (2026-09-16, first used on RA-01):** a Fable 5.1 (high) session writes the build plan
(`Handoffs/video-editing/<job>-plan.md`: measured source facts, take map, cue map with asset paths, framing, audio,
gates, round protocol, reviewer report format). An **Opus 5 (high) subagent** builds to it (`.claude/agents/ra-editor.md`).
A **fresh Fable (high) subagent** reviews blind — only the plan, the rules and the delivered files, never the editor's
notes (`.claude/agents/ra-reviewer.md`) — and reports SHIP / DOES NOT SHIP with a numbered defect list. The planner
turns each review into rulings appended to the plan (§12, §13…) and re-sends Opus. Cap three rounds, then Dan.

**Why:** Dan wants Opus doing the token-heavy render loop and an independent check before he watches anything.

**How to apply:** agent definitions in `.claude/agents/` load only at session start (a mid-session `Agent` call with
`subagent_type: general-purpose, model: opus` inherits the parent's effort). Tell the editor not to spawn judge
subagents (the first run died on the monthly spend limit). RA-01 result: three rounds, ship-clean except the
outdoor-audio row that is Dan's exception; measured cost per round in `.claude/skills/ad-edit/SKILL.md` "RA-01 lessons".
Related: [[shoot-828-slog3-format]], [[video-editing-master-list]].

**Dan APPROVED the result as the template (2026-09-18):** "I think you nailed it. Audio sounded good, and color
correction looks good. The way you cut it… transitions… this was a template for future videos." The approved hook
grammar, card rules and kit are in `.claude/skills/ad-edit/SKILL.md` "RA-01 lessons" and `_shared/adkit/`. See
[[analysis-card-reusable-graphic]].
