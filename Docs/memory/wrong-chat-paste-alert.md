---
name: wrong-chat-paste-alert
description: "If Dan pastes something clearly meant for a different task into a chat, alert him in one line before doing any work on it"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 8ec10db3-9f61-4dee-9a37-55ae865ec219
  modified: 2026-11-16T15:25:36.097Z
---

Dan, 2026-11-16: "alert me in the future if I paste something grossly out of context into a chat that is likely intended for another task so i avoid wasting tokens and corrupting context."

**Why:** on 2026-11-16 he pasted Eric's Joint Vigor VSL reply (client work) into the Great Again T VSL chat. That chat opened a side session, which wrote the handoff and then opened a duplicate edit chat next to the one Dan started himself. Nothing was damaged, but it cost tokens and a cleanup check.

**How to apply:** when a message is about a different video, client or project than the chat's task and builds on nothing in it, stop before any tool call or side session. Say in one or two lines: this looks meant for another task, name the chat it likely belongs to (link it if an existing session is found cheaply), and ask whether to do it here anyway. Do not read files, draft, or start sessions first. Small related asides and genuine new requests he clearly means for this chat are not this case. My reading: this outranks the app's "offer a new session" card for an obvious mis-paste, because the right home is usually an existing chat, not a new one. See [[pasted-text-is-dans]], [[bias-toward-action]].
