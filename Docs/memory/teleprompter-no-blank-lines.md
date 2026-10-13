---
name: teleprompter-no-blank-lines
description: "Dan 2026-10-13: teleprompter documents have no blank lines between paragraphs (saves prompter space); script edits happen in the Filming document, not in the teleprompter copy"
metadata:
  type: feedback
---

Teleprompter documents (the Google Docs and their PromptSmart imports) are built with no blank line between paragraphs. Script writing, polish and cuts are done in the Filming document (the shoot doc), and the teleprompter documents are made from it.

Dan, 2026-10-13, after filming prep with the blank-line versions he had asked for that morning: "for this document and the other teleprompter documents, take the line breaks out. Going forward, when you generate the scripts for me, we'll just do it within the Filming document, rather than doing the edits in the teleprompter like we did here. I want to change back to your teleprompter documents not having line breaks to conserve space on the teleprompter... Going forward, keep doing the teleprompter documents without line breaks between paragraphs."

**Why:** blank lines cost prompter space (Teleprompter 1 went from 32 pages to 22 without them). He only wanted them while he was editing scripts inside the teleprompter document, and he does not plan to edit there again.

**How to apply:**
- `tp_from_shoot_doc.py` writes no blank paragraphs (one stays where a round cue stood in a follow-along workout).
- To change an existing teleprompter document without losing anything typed in it: `.claude/skills/teleprompterscripts/reference/tp_reflow.py`, then the rclone replace, then re-import into PromptSmart and move the old cards to its Trash.
- The Filming document keeps blank lines between paragraphs: [[scripts-blank-line-between-paragraphs]].
- If he edits a teleprompter copy himself again, it becomes the master until his words are carried into the shoot doc.

Rule text: `/teleprompterscripts`, "No blank lines between paragraphs in a teleprompter document"; `_shared/WRITING-RULES.md` section 6. Related: [[filming-docs-after-final-polish]], [[filming-scripts-first]].
