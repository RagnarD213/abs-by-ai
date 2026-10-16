---
name: action-items-at-bottom
description: "Every finished task or stop-for-Dan ends with two boxes, What was done + Your next steps (task-wrapup mod, 2026-10-16); files sent last"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 920a8b4f-ee37-46a0-8a25-fecb42125c74
  modified: 2026-09-24T22:54:41.180Z
---

**Updated 2026-10-16:** the format is now the `task-wrapup` mod's two closing boxes, **What was done** (one or two plain sentences) and **Your next steps** (at most 4 numbered commands with links, saying whether Dan has reviewed each yet). Dan, 2026-10-16: *"Why aren't you using our recently made modification for action steps and simple language summary?... make all tasks going forward use that modification."* The mod lives at `~/.claude/mods/task-wrapup` (user scope, every session on this Mac); `CLAUDE.md` carries the same rule for sessions that do not load it. Older wording below still holds where it does not conflict.

When Dan has to decide or review something, end the message with a short numbered **Your action items** list. Each item stands alone: say what the thing is in plain words (never a bare letter code like "C or D" or "B1-B4" that points back to an earlier message), give the options and my recommendation, and say exactly how to answer. If he has to watch or look at a file, send it with SendUserFile as the LAST thing in the turn so it sits at the bottom of the chat, right next to the action items.

**Why:** Dan, 2026-09-24 (SL-04 shorts): "This just turned into a cludge of thinking where I can't even find what you want me to look at... going forward, make my action items. Show me the video at the bottom of the chat." A status message had mixed progress notes with questions, referred to options by letters from an earlier message, and the preview video had been sent mid-turn where it scrolled away.

**How to apply:** Progress notes first (short), then the action items, then the file(s). Re-describe every option in full each time it is asked. Relates to [[explain-simply]].
