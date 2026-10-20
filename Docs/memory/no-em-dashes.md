---
name: no-em-dashes
description: Dan's rule - no em dashes in outward-facing writing (customer text, teleprompter scripts, copy, messages in his name); fine in chat to him and internal docs. Narrowed 2026-10-20
metadata:
  type: feedback
---

No em dash (—) in anything a customer, viewer, editor or business contact reads or hears: teleprompter scripts, on-screen graphics and captions, website/ad/email/social copy, titles and descriptions, revision docs and messages written in Dan's name, emails to business contacts. Do not substitute an en dash. Rewrite with a comma, colon, parentheses or two sentences.

**Allowed:** chat replies to Dan, handoffs, board entries, commit messages, memory, skills, internal notes.

**Why:** Dan, 2026-09-18: em dashes are a major giveaway of Claude output, and he does not use them, so outward text carrying his name reads as pasted AI. On 2026-10-20 he narrowed the rule: *"no em dashes in customer-facing text writing only,"* because in chats and internal notes they improve readability.

**How to apply:** `grep -c '—' <file>` must be 0 on outward-facing text only. Forward-looking, no cleanup sweep of existing copy. Rule also in `AGENTS.md`. Related: [[revision-docs-in-dans-voice]].
