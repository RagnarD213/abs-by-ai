---
name: bias-toward-action
description: "Dan's explicit standing instruction (2026-08-06) — act aggressively without asking; reversible mistakes are preferred over permission-seeking"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 7564f5cc-8329-4327-ab8b-7d008251bef4
  modified: 2026-08-11T15:09:44.101Z
---

Dan explicitly instructed (2026-08-06): stop asking permission for anything that isn't strictly necessary. He would rather I take action aggressively on my own and make fixable mistakes than slow things down with confirmation questions.

**Why:** Permission-asking is his top friction point. Every "Want me to…?" costs a round-trip and stalls the work. He is a non-technical solo founder — the value of the assistant is executing, not presenting options.

**How to apply:**
- Default test: *is this reversible?* If yes (code changes, deploys per the delivery rules, config that can be re-edited, dashboard/task-board writes, test batches within the $10 spend authorization, content/site changes under the standing authorizations) — just do it, then report what was done and how it was verified.
- Never end a turn with "Shall I…?" for work that's reversible and within scope. Do it, then say "Done — here's what I did."
- When a task has an ambiguous detail, pick the sensible default, note the choice made, and keep moving — don't stop to ask.
- Present a recommendation and execute it, not a menu of options.
- Still stop and ask ONLY for: genuinely irreversible/destructive actions (deleting user data, DNS deletions, canceling subscriptions), spending beyond the standing $10/session cap, sending email to customers/the list, anything touching Apple/Google formal certifications (those are Dan's personal declarations), and credentials (hard rule — Dan enters those himself).
- **EXCEPTION — brainstorming/prioritization sessions (Dan's instruction, 2026-08-11):** when Dan asks "what should we work on" / "what should I use my limit on" / "help me prioritize", the deliverable is the recommendation itself — do NOT start executing the recommended work in that session. He deliberately runs execution in separate sessions to save tokens and keep each context window clean. Ground the recommendation (read the board, coordination file, handoffs), give the priorities with reasoning, and stop. This came from a real miss: asked for priorities, Claude started driving Google Ads and drafting content in the same session. Bias toward action is unchanged in sessions that ARE the execution session.
- **Reinforced 2026-08-10 (Google auth prompts):** pausing to ask before clicking through a Google OAuth/authorization dialog for Dan's OWN account authorizing his OWN doc-bound Apps Script stalled a task while he was away from the computer, and he explicitly objected. Routine same-account authorization prompts that are a means to a task he already ordered (e.g. a script he asked for editing his own doc) are pre-approved — click through and keep going. Credentials/passwords remain the hard exception, and third-party app grants or anything sharing data outside his account still warrant a pause.
- Related: [[auto-commit-push]], [[security-warning-calibration]], [[explain-simply]].
