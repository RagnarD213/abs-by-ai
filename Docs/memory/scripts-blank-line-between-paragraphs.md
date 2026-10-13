---
name: scripts-blank-line-between-paragraphs
description: "Script documents (the shoot doc, filming scripts) have a blank line between all paragraphs; teleprompter documents are the exception since 2026-10-13 evening: no blank lines"
metadata:
  node_type: memory
  type: feedback
  originSessionId: dfcd4510-3e7f-4133-bb01-62ee9099047b
  modified: 2026-10-13T21:14:21.844Z
---

**Changed the same day (2026-10-13, evening): teleprompter documents and their PromptSmart imports have NO blank lines between paragraphs.** See [[teleprompter-no-blank-lines]]. What follows still holds for the Filming document (the shoot doc) and other script documents; where it names teleprompter copies, the newer rule wins.

Every script I write or build has a blank line between all paragraphs, in every document it lands in: the shoot doc, the teleprompter-only copies, the pickups document, PromptSmart imports. Never deliver scripts as a solid block of text.

Dan, 2026-10-13, with a screenshot of "10-17 Shoot - Teleprompter 2 - Green Screen" in Google Docs, where each paragraph started on the line right under the one before: "The scripts don't have line breaks between them. They're just a clutch of text. Put line breaks between all the paragraphs. Save this to memory so that when you're writing scripts, you never write them like this, and you always have line breaks between paragraphs so they look normal." ("clutch" is Wispr Flow; my reading is "clump" or "block".)

**Why:** the teleprompter builder (`.claude/skills/teleprompterscripts/reference/tp_from_shoot_doc.py`) wrote each spoken line as its own paragraph with no space after it, so three teleprompter documents and the pickups document read as one block. The filming scripts in the shoot doc already had blank lines; the copies built from them lost them. He reads these on camera, four days before a shoot.

**How to apply:**
- A real empty paragraph between paragraphs, not paragraph spacing. In HTML built for Google Docs that is `<p><br></p>` after each paragraph; through the Docs connector it is an extra `\n`.
- The builder does this since 2026-10-13. Any new builder or one-off document (like the pickups teleprompter, which had the same fault between its repeated lines) must do it too.
- Check before delivering, in code: export the document as text and count non-empty lines that are directly followed by another non-empty line. Only a title followed by its first paragraph may touch.
- Then look at it once in the browser. He judged this by eye, and a text check alone had passed it.
- Blank lines add pages: 12,437 words went from 22 pages to 32. Re-check his 50 page limit per teleprompter document.

Rule text: `.claude/skills/_shared/WRITING-RULES.md` section 6, and `/teleprompterscripts`. Related: [[filming-scripts-first]], [[filming-docs-after-final-polish]], [[google-docs-nested-bullets]].
