---
name: iphone-mirroring-standing-authorization
description: Dan 2026-09-25 - always authorized to use iPhone Mirroring; never ask permission each time
metadata:
  node_type: memory
  type: feedback
  originSessionId: 4d253341-46a0-4679-ad8e-0f2c2fa34b82
  modified: 2026-09-25T22:38:24.312Z
---

Dan said 2026-09-25: Claude is always authorized to use iPhone Mirroring whenever it wants; do not ask him for permission each time.

**Why:** he is tired of per-use approval stops. The tool's own request_access dialog still appears; that is the harness, not a question to Dan in chat.
**How to apply:** just call request_access and drive the phone. Do not ask "may I use iPhone Mirroring?" in chat. See [[iphone-mirroring-control]].
Trap: Wispr Flow overlay blocks display-scope drags near the bottom of the phone; use scroll (right, amount 50) on the share sheet row instead.
