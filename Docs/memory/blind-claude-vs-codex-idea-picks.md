---
name: blind-claude-vs-codex-idea-picks
description: "11-12: when Claude and Codex both make idea lists, Dan wants ONE shuffled blind pick page, authors hidden, scorecard only when he asks; next-shoot page, key and reveal steps"
metadata:
  node_type: memory
  type: project
  originSessionId: be1381c2-fa47-4d80-93c9-112e445fc9f8
  modified: 2026-11-12T19:52:01.137Z
---

Dan, 2026-11-12, after Claude and Codex each wrote 80 ideas for his next green screen shoot from the same prompt: "pull those ideas in and present me one artifact with the ideas all integrated and randomized together. Don't tell me which ones you came up with. Don't tell me which ones Codex made... I'll choose the ones to write, and then after we're done, reveal how many from each AI I chose."

**How to apply (my reading: this is his standing preference whenever both AIs answer the same idea request, like the blind image test in [[blind-google-vs-codex-images]]):**
- One page, both lists in the same card layout (title, open, outline, evidence chips, clip link), shuffled inside each format, new neutral IDs, a Pick button per idea. Never label an author in the page, the chat, a file name he will see, or a handoff. Normalize quotes, labels and outline length so the format does not give the author away; keep titles and substance unchanged.
- Keep the author key private and local. Reveal counts only when he asks for the scorecard.
- Hide (do not delete) ideas that break a decision he already made, behind a visible toggle, so the scorecard stays honest.

**The 2026-11-12 next-shoot instance:**
- Pick page (private artifact): https://claude.ai/artifact/U1FQh89tUpYwrAAet8mnqb ("Next Shoot Picks"), 159 ideas: A = long videos (60), B = Shorts (40), C = reaction Shorts (39), D = long reactions (20). His picks save to the artifact database, collection `picks`, document `main`, field `ids` (read with the ArtifactData tool). He can also paste the "MY PICKS" text.
- Same list with clips that play inside the page (artifacts cannot embed YouTube): http://127.0.0.1:11832/ , built by `blind/make_local.py`, served with `review_server.py 11832 "Research/Shoot Research Claude 2026-11-12/blind/local"`. Picks made there live in that browser's localStorage key `next-shoot-picks-v1` (read it through the built-in browser pane) and in the "MY PICKS" text. For the scorecard, union the picks from both pages.
- Key: `Research/Shoot Research Claude 2026-11-12/blind/key.json` (blind id to set and original id; set a = Claude, set b = Codex). Rebuild scripts beside it (`build.py`, `make_page.py`, seed fixed). Re-running `build.py` keeps the same IDs only if both source lists are unchanged.
- Source lists: Claude's doc https://claude.ai/artifact/TPVzyA9gEoyECbiW77nxpT and reaction clip data `Research/Shoot Research Claude 2026-11-12/reaction-shorts/ideas.json`; Codex's `Research/Shoot Ideas 2026-11-12/`.
- For the reveal: read his picks, count by set per format, and say plainly that the test was not perfectly blind (he saw part of Claude's list before the merge, and Codex's list was written before his five decisions that day: green screen only, US weighting, no app content, no natty-or-not, GLP-1 cap). 14 Codex ideas need outdoor filming and were hidden by default.
- His five decisions for this shoot are in the same folder's README and in the ideas doc. After picks, scripting follows his clips-first rule for reactions ([[reaction-clip-criteria]]).
