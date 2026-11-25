---
name: ask-before-codex-fast-mode
description: "2026-11-24 standing rule: never turn on Codex fast mode (priority service tier) without asking Dan first, especially when his Codex usage is low"
metadata:
  node_type: memory
  type: feedback
  originSessionId: db8500f5-e462-44dd-903c-71047b6a5649
  modified: 2026-11-24T22:33:53.739Z
---

Never use Codex fast mode (`-c service_tier="priority"` on `codex exec`) without asking Dan first. Default every Codex run to the standard tier.

**Why:** Fast mode burns Codex usage faster. On 2026-11-20 it was switched on for the Joint Vigor job after a single "can you use fast mode?" message, and on 2026-11-24 Dan wrote: "DO NOT USE FAST MODE! I NEED TO CONSERVE USAGE IN CODEX" and "ask me before using fast mode in the future, especially if usage is low."

**How to apply:** Ask in one line before any run that would use the priority tier, giving the reason and the usage cost. Don't treat an earlier yes, or "use as much Codex as you need", as permission for later runs. Never kill a run that's already going just to change its tier, because that wastes what it has already spent. Related: [[delegate-to-codex-until-nov-26]].
