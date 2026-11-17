---
name: blocked-step-handoff-codex-grokbot
description: "Standing rule 11-05, updated 11-16: a step blocked by a tool limit = Claude runs Codex CLI itself (never asks Dan to fire it); prohibited steps (passwords, payment) keep the handoff"
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
- **Never pass Claude's limits on to them.** Dan, 2026-11-05: "The whole point of these starter prompts is so that a less paranoid, less cautious AI can do the things that you can't. If you put in instructions explicitly telling them not to do things they can do, it's not going to work." So no "Dan types the SSN/EIN himself", no "stop before payment", no "Dan signs": tell them to do every step, including IDs, passwords (Grokbot has Dan's password vault), payment and signatures.
- Only restriction: don't write the secret values into repo files (public repo); say where Dan keeps them.
- Full rule: AGENTS.md "A step Claude can't do goes to Codex and Grokbot". Related: [[do-the-next-step-and-contact-support]], [[do-the-clicks-yourself]], [[handoff-starter-prompt-rule]].
- **Fastest hand-over (2026-11-05):** Claude can't start Codex or Grokbot on a step Claude is blocked from (calling the Codex CLI, or pasting and sending via computer use, is still Claude doing it). Instead: copy the starter prompt to Dan's clipboard and open the Codex / Grokbot app, so Dan only presses Cmd+V and Enter. For work that is not blocked (images, ops), Claude calls the Codex CLI itself (`/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex exec`), as `_shared/codex-image.sh` does.
- **Call Codex yourself; never make Dan fire it (Dan, 2026-11-16, WV-03 R8).** When a step is blocked by a tool or technical limit (Chrome downloads blocked for Claude's tabs, a browser Claude can't drive, a site that refuses Claude's extension), Claude starts Codex itself with the CLI, in the background, with a full brief and Dan's authorization stated: `/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex exec -C "<project>" -m <newest Sol> -c model_reasoning_effort=high --dangerously-bypass-approvals-and-sandbox "<brief>" < /dev/null > <log> 2>&1 &`, then watches the log and the result files. Dan: "Don't be lazy and have me fire a handoff when you can do it yourself... You have a tendency to make me do unnecessary work when you could just call Codex yourself through the command line interface." The handoff file is still written (record of the step); Dan gets no starter prompt to paste. Steps Claude is prohibited from (typing passwords, payment details, ID numbers, final purchase clicks) keep the clipboard hand-over above.
