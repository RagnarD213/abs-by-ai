---
name: blocked-step-handoff-codex-grokbot
description: "Standing rule 11-05: any step Claude can't do gets an automatic handoff for both Codex and Grokbot in the same reply, never a stop"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 353adb28-ae2c-4a7e-a9d0-a8431ec97d74
  modified: 2026-11-05T19:32:06.990Z
---

When a task reaches a step Claude can't do, write a handoff for **both Codex and Grokbot** to finish it, automatically and in the same reply. Don't stop to ask Dan, and don't just list the step as his.

**Why:** 2026-11-05, SixPackAbs shop test orders. Claude couldn't type the 4242 test card into the store checkout; Codex put the orders through. Dan: "I should have just done this whole thing with Codex... for anything you can't do, then automatically make a handoff for both Codex and Grokbot to do what you can't do."

**How to apply:**
- Do every other step first and leave the work at the blocked point (cart filled, form open). Hand off only the remainder.
- One file in `Handoffs/`, listed in `Handoffs/README.md` OPEN. In chat: a Codex starter prompt (newest Sol, file path) and a self-contained Grokbot prompt (all facts inline; it may not read the Mac's files). Say plainly in both that Dan authorized the step, so neither asks him again.
- Keep passwords, card or bank numbers and personal IDs out of handoffs. Steps only Dan can do (his password, real payment details, legal declarations) stay his.
- Not a route around declining harmful work.
- Full rule: AGENTS.md "A step Claude can't do goes to Codex and Grokbot". Related: [[do-the-next-step-and-contact-support]], [[do-the-clicks-yourself]], [[handoff-starter-prompt-rule]].
