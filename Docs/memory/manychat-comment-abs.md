---
name: manychat-comment-abs
description: ManyChat comment-to-DM on @danrosefit — the six per-topic keywords, the plan gate, and the counters/quick-reply traps
metadata:
  type: project
---

ManyChat comment-to-DM went live 2026-09-02 on @danrosefit (ManyChat account `fb5531746`).
Comment containing a keyword → rotating public reply → DM with a `[Send me the link]` button →
second DM with `[Get my free preview]` → absbyai.com with a UTM.

**Split into six per-topic keywords on 2026-09-08**, because one keyword and one
`utm_campaign` across ~60 queued posts made attribution impossible: **ABS** (ab training),
**FOOD** (nutrition), **TRAIN** (non-ab workouts), **TRACK** (scale/photos), **SLEEP**,
**COACH** (AI tools). Each has its own DM copy and `comment-<keyword>` campaign. Automation
ids, DM copy and the caption rewriter: `Docs/MANYCHAT_KEYWORDS.md` and
`scripts/manychat/keyword_split.py` in the repo.

**Keywords match CONTAINS, not equals** — so a keyword that is a substring of a common comment
cross-wires the DMs. `EAT` is unusable (fires on "great"), and so is `AI` (fires inside "train",
"again", "wait"). That is why the topics are FOOD and COACH.

**Plan gate:** "any post or reel" is **Pro**. Essential watches ONE post per automation. The
account has shown a **TRIAL** badge since the upgrade — if it lapses, all six break at once.

**Trap that cost a session:** ManyChat's Sends/Clicks counters and Inbox lag several minutes, and
a new contact shows status "Visitor" with no conversation even after a successful send. **Do not
read 0 as a failure** — open the recipient's real Instagram DM inbox instead.

**Two-beat DM is required:** Instagram blocks a bare link in an automated DM, so the first
message must carry a button.

**Instagram WEB never renders the quick-reply button** — it shows only the message text, and
typing that same text does NOT fire the next step (the button is a postback payload). Testing the
second beat needs the phone app. The first beat (comment → public reply → topic DM) is fully
testable on web.

Testing needs a commenter that is not the connected account; @abs.by.ai works, and is switchable
from the web account switcher. See [[instagram-account-state]].

**Editing the easy builder in a browser:** its fields are React-controlled and synthetic typing
drops characters — set values with the native value setter plus an `input` event. The link URL sits
behind the 🔗 icon and has its own Save, separate from the automation's Update. The SPA also wedges
the Claude-in-Chrome extension after a handful of page loads (every tool call then times out, even
on unrelated sites); recovery is to close the ManyChat tabs and have Dan bring Chrome to the front.
