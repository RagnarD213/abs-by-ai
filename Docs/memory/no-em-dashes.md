---
name: no-em-dashes
description: Dan's standing rule, 2026-09-18 - never use an em dash in any writing, anywhere, for any reason
metadata:
  type: feedback
---

Never use an em dash (—) in anything written for Dan or for this project: revision docs, editor messages, scripts,
on-screen graphics, website and ad copy, handoffs, board entries, commit messages, and chat replies to Dan. Do not
substitute an en dash (–) either. Rewrite with a comma, a colon, parentheses, or two sentences. Hyphens in compound
words and numeric ranges are fine.

**Why:** Dan, 2026-09-18, on a message written for him to send to an editor: *"Em dashes are a major giveaway of Claude
output. I want you to have a standing rule for all of our writing that we never, ever, ever use an em dash in any
writing. No em dashes ever."* Dan does not use them himself, so a document carrying his name that is full of them reads
to the recipient as pasted AI output. Same reason as [[revision-docs-in-dans-voice]].

**Scope: new writing only.** Dan, 2026-09-18: *"we don't need to edit the existing copy. I just want to make sure
that going forward, new copy doesn't use em dashes in any writing."* There are about 13,900 in the back catalogue,
445 of them in readable copy on the live site, and they stay. Do not propose or run a cleanup sweep.

**How to apply:** write without them from the start, then `grep -c '—' <file>` before anything goes out. It must be 0.
The rule is also in `AGENTS.md`. Related: [[revision-docs-in-dans-voice]], [[explain-simply]].
