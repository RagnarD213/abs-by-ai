---
name: categorize-before-editing
description: "Dan 2026-10-04 - every video is categorized CONTENT or AD before any edit; long-form content gets Shorts only, ads get vertical/square/1-minute only"
metadata:
  node_type: memory
  type: feedback
  originSessionId: dbd690fb-09a7-4e1f-a33a-a12324d233c5
  modified: 2026-10-04T14:59:45.172Z
---

Dan, 2026-10-04 (his words): "From now on, we have to have everything categorized before we edit it. If it's a content video, if it's long-form content, then we want to cut it into shorts. If it's an ad, that's when we need the vertical and square version and the 1-minute version." He asked for it in both directions: no ad-style edits of content videos, and no content-style edits of ads "such as making 5 shorts out of an ad".

- Long-form content (LFC): Shorts cut from it (`/shorts`), nothing else. No full vertical, square or 1-minute version.
- Ad (AD): vertical, square and 1-minute versions (`/shortad-from-longform`), nothing else. No batch of organic Shorts from an ad.
- Dedicated Short (SFC): nothing derived (my reading; he did not mention it).

**Why:** on 2026-10-03 I followed a handoff that used RO-10 (the Calories long-form) as the proof run for the vertical kit: about seven hours and 1.6M judge tokens for a full 9:16 and a 52 s cut nobody needed. The earlier session had read his "one handoff to continue the edit in the next task" as picking that option; he never chose it. His reaction: he did not understand why those cuts existed, and called it wasted tokens.

**How to apply:** state the category on the first line of every video task and handoff. If a prompt, handoff, queue job or pipeline test asks for the wrong kind, stop before spending and tell Dan in one line. Only his own words naming that video and that format override it; an ambiguous reply ("continue the edit") is not a choice. Prove a pipeline on a video of the right category. Rule lives in `AGENTS.md` and `_shared/VIDEO-RULES.md`; `kit_run.py` refuses a content edit sheet without `--dan-asked`. Related: [[ad-vs-organic-classification]], [[ads-never-organic]], [[decision-budget-per-video]].
