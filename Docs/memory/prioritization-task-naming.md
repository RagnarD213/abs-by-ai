---
name: prioritization-task-naming
description: "Every prioritization or day-planning task is renamed \"PRIORITIES - MON D YYYY\" (Dan, 2026-10-05)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 6847a66c-3a30-413d-8c9a-c5e6a457c2f4
  modified: 2026-10-05T13:56:04.445Z
---

Every prioritization, day-planning or "what should I work on" task renames itself `PRIORITIES - MON D YYYY`: all caps, three-letter month, no leading zero, the date being planned. Example: `PRIORITIES - OCT 5 2026`.

**Why:** Dan said on 2026-10-05, after renaming that day's plan: "Going forward, always name these prioritization tasks in this format." It replaces the 2026-10-01 "Daily Priorities MM-DD-YYYY" title.

**How to apply:** call `set_session_title("self", ...)` at the start of the task without being asked, whether or not /prioritize or /plantheday was invoked. Both skills carry the rule. Video tasks keep their own format, see [[video-task-names]].
