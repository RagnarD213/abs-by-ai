---
name: revision-status-check-live-doc
description: "Any status check on editor revisions reads the LIVE Google Doc first — Dan deletes and adds items, so our local revision docs and summaries are not the ask"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 0796628c-3979-44d1-be50-f37c0c2a66ac
  modified: 2026-09-18T19:35:42.311Z
---

When Dan asks whether an editor's revisions were made — a status check, "did he do this?", "what's
left?" — the source of truth is the **current shared Google Doc**, never the markdown in
`revision docs/` and never the `.summary.md` files. He deletes items he does not want and adds items
of his own after the doc is written, so our copy is a draft, not the request. Read the live doc,
then check the delivered files against **only the items still in it**.

**Why:** On 2026-09-18 a check on Muhammad's Ads 8/9/13/15 was built from the local summaries and
told him to fix an empty green card, a beach-clip artifact, a SIXPACKSHORTCUTS watermark and a
robot-arm fusion — every one of which Dan had deleted from the doc. It also missed that Dan's own
edits had cut Ad 13 down to a single item. Dan: "The current document is a source of truth on this
going forward."

**How to apply:** Read the doc with the Drive connector (`read_file_content` on the doc id; the
Muhammad batch doc is 200k+ characters, so it lands in a tool-results file — slice the round sections
out with python rather than reading it whole). Diff what's there against our local copy and say
plainly which items Dan removed, because the deleted ones may still be real defects he has chosen to
accept. Then verify each surviving item against the delivered file at its timestamp. Also check
whether the editor's newest export is a LATER version than the cut we reviewed — on 09-18 Muhammad's
HD exports already satisfied most of the list. See [[revisions-zero-edit-goal]] and
[[editor-message-voice]].
