---
name: no-next-round-until-review-finished
description: "Do not start the next round's chat while Dan is still reviewing or a decision is open; write the handoff and wait for his word"
metadata:
  node_type: memory
  type: feedback
  originSessionId: c0133ff8-9ddc-4c28-9324-1a3c7bc0a44a
  modified: 2026-11-16T15:49:38.148Z
---

On 2026-11-16, in the Great Again T VSL (WV-03) round 6 chat, Dan dictated a first batch of review notes and asked for my opinion on one character versus a variety of people. I recorded the notes, gave the opinion, and in the same turn started the round 7 chat (Opus 5.5 high) under the "video rounds start automatically" rule. He was not finished: a second batch of per-clip approvals and the character decision came minutes later, he stopped the new chat, and its work was discarded. Dan: "I don't like how you started that new task before we finished reviewing everything here. In the future, just make sure you don't start new tasks so aggressively like this. If there's still more to review and I haven't given you feedback, especially on the priority edit like this, that was a significant waste of tokens... Remember that in the future, if there are decisions to make and things, don't start the new task yet. Be a little more cautious with doing that." He then asked: "Give me a new handoff to incorporate all this feedback."

**Why:** a round started on partial feedback gets redone, and tokens matter most while a priority edit is running. A question I asked him (or he asked me) that changes the work means the review is still open.

**How to apply:** when Dan's review notes arrive, record them and answer his questions, but do NOT start the next round's chat or any production if (a) he asked me a question whose answer changes the work, (b) I asked him one, (c) he has not said he is done or pasted the review page's full reply, or (d) parts of what was sent for review have no feedback yet. Write or update the handoff, give him the starter prompt, and wait for his word that the review is finished. This narrows the automatic-rounds rule in AGENTS.md (2026-10-20), which still applies once his review is clearly complete; that reconciliation is my reading, not his wording. Related: [[prepare-only-handoff-fire-on-go]], [[bias-toward-action]].
