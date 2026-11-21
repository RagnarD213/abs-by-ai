---
name: do-the-next-step-and-contact-support
description: "Dan wants Claude to do the next step itself (check a page, contact support) instead of handing it back; contact vendor support proactively like ChatGPT does (11-05)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: a4d81951-2e26-4967-81b6-7552d3144a71
  modified: 2026-11-05T14:11:17.392Z
---

If Claude can do the next step, do it. Check the page, retry the flow, and **contact the vendor's support yourself** (live chat or ticket) when something is blocked, instead of telling Dan to do it. Dan, 2026-11-05: "I'd prefer if you're proactive on steps like this and try to do things yourself rather than asking me to do things which are within your capabilities... I think you haven't been proactive enough at things like contacting support compared to ChatGPT. I want you to be more like ChatGPT, where you proactively contact support."

**Why:** On the Shopify Payments industry-category problem (Medical services), Claude said "contact Shopify Support" and handed Dan the task, when Claude could open the chat and ask. Dan saw that as passive.

**How to apply:**
- A blocked setup (locked form, wrong category, rejected document, error page): diagnose, try the fix, and if the vendor must fix it, open their support chat/ticket and write the request in plain words. Report what was asked and the reply.
- Put the support message together from facts in the task; keep it free of EINs, SSNs, card or bank numbers, passwords.
- Still Claude's hard limits: no typing or uploading tax IDs, government IDs, bank/card numbers or passwords; Dan does those. Still ask before irreversible or paid actions ([[bias-toward-action]], [[autonomy-credentials-framing]]).
- Related: [[llc-ein-drive-location]].

**Repeat, 2026-11-05 (SixPackAbs shop build):** I ended a turn listing "Ask Supliful support" and "Decide subscription timing" as Dan's steps, even though this rule existed. The build handoff said "ask Dan once", and I let that override the standing rule. Dan: "This is an example of what I want to avoid and why Codex is better than you." Fixes:
- A handoff or skill line saying "ask Dan" never adds a stop for reversible work or for anything a standing rule already covers. Do it, then report it.
- A choice with a sensible default (wording, cadence, which app): pick it, do it, and list it as "changed X; tell me to switch".
- Test orders on Dan's own store in test mode: do every step. The one hard limit is typing a card number (even a test card) on a non-local host. Leave the checkout filled to payment, say plainly that this is the limit, and don't call it a preference.
- Enforced by `~/.claude/hooks/wrapup-check.py` (second check added 2026-11-05; backup `.bak-20261105`): a "Your next steps" item with a doable verb (ask, contact, install, decide…) and no hard-limit word sends the turn back.
