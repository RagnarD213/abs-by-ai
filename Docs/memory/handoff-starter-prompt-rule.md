---
name: handoff-starter-prompt-rule
description: Every handoff doc delivered to Dan must come with a ready-to-paste starter prompt plus a model + effort recommendation, ALWAYS stated in chat, no exceptions
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 788b1a9f-caac-40d1-95be-5be431bd62ea
  modified: 2026-09-14T23:51:26.144Z
---

Whenever a handoff document is created for Dan (2026-08-31 instruction, reaffirmed 2026-09-14),
the chat message that delivers it must ALWAYS include, with no exceptions: (1) a ready-to-paste
starter prompt for the fresh session, and (2) a recommended model and effort level for running it.
This applies to every handoff, every time — a `Handoffs/*.md` file written by hand, a fired
handoff, and a run of the built-in `/handoff` (anthropic-skills) plugin skill alike. That plugin
skill already writes a starter prompt and a model/effort recommendation INTO the downloadable
doc — that is not sufficient on its own. Both must also be restated directly in the chat message,
so Dan can act without opening the file.

**Why:** Dan executes handoffs in separate sessions to keep context clean and tokens cheap; he
wants to paste one line and go, not open a doc, not compose the kickoff himself, and not guess
which model fits. This was reaffirmed 2026-09-14 after Dan asked to make sure it was applied
consistently — treat any handoff delivery that omits either piece from the chat message as
incomplete, not just informal.

**How to apply:** End every handoff delivery message with a fenced starter prompt (name the
handoff file and the skill to invoke if one applies) and one line of model/effort reasoning — e.g.
Opus 5 high for flaky-UI or judgment-heavy work, Sonnet 5 for mechanical measured work (the
build-timings handoff precedent). Do this even for a one-line/simple handoff — never skip it as
"obvious." Related: [[bias-toward-action]].
