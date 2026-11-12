---
name: review-pages-select-not-kill
description: "11-12: on pick pages Dan clicks the items he WANTS (Select or Pick); untouched = out. No Kill buttons, no 'kill L07' instructions"
metadata:
  node_type: memory
  type: feedback
  originSessionId: be1381c2-fa47-4d80-93c9-112e445fc9f8
  modified: 2026-11-12T20:03:02.827Z
---

Dan, 2026-11-12, looking at the reaction clips review page (19 clips, a Kill button on each, untouched cards counted as keeps): "Change a page so that I click on the ones that I want to select rather than the ones I want to kill, because most of them I'm going to be killing."

**Why:** he keeps a minority of what he is shown (7 of 20 and 8 of 20 in the earlier clip rounds), so killing means clicking most of the page.

**How to apply:**
- Any page or doc where he chooses from a list (clips, ideas, covers, outlines): the control selects. Label it Select or Pick, default is not selected, and the reply text lists what he selected. Do not ask him to say or click what to kill, and do not write "anything you don't kill counts as a keep".
- The reaction clips template is changed: `.claude/skills/reaction-clips/reference/page_template.html` now gives pick sections Select buttons (`"mode": "kill"` on a section restores the old behavior). Skill text and `data-format.md` updated the same day.
- My reading, not his words: this applies to every future pick page, not only the one he was looking at. Pages where he approves nearly everything (a short list of finished assets) could still default to keep; ask only if that case comes up.

Related: [[blind-claude-vs-codex-idea-picks]], [[reaction-clip-criteria]], [[review-page-what-i-decided]].
