---
name: antigravity-memory-and-improvement-loop
description: "2026-11-24: Google Antigravity is wired into the shared Abs By AI memory and rules via GEMINI.md and .agents/hooks.json (SessionStart); do not delete them or create a separate memory silo"
metadata:
  node_type: memory
  type: project
  modified: 2026-11-24T21:38:00Z
---

Google Antigravity 2.0 is wired into the same shared memory and rules system used by Claude Code and Codex for Abs By AI:

- **`GEMINI.md`** (project root, always active in Antigravity, ignored by Claude Code and Codex): defines the read/write shared-memory protocol, public-repo privacy guard (`.repo-private` + `scripts/sync-memory-to-repo.sh`), and cross-AI safety rules.
- **`.agents/hooks.json` + `.agents/hooks/session_start_memory.py`**: Antigravity `SessionStart` hook that live-loads two things at the start of every new Antigravity chat:
  1. The remainder of `AGENTS.md` past Antigravity's 24 KB per-file rule cap (so nothing in `AGENTS.md` is silently truncated or stale).
  2. The merged `MEMORY.md` index from Claude's local memory directory plus any repo-only entries in `Docs/memory/MEMORY.md`.

**Why:** Antigravity has a 24 KB per-file cap on `AGENTS.md` (which cut off ~71% of the 82 KB file) and did not load `MEMORY.md` or write lessons back to the shared memory folder by default.

**How to apply:** Keep `GEMINI.md` and `.agents/` intact; do not split Antigravity onto a separate Obsidian vault or separate memory folder. When Antigravity saves new lessons, it writes to the same local memory folder + `AGENTS.md` and syncs safe entries to `Docs/memory/` via `scripts/sync-memory-to-repo.sh`. Related: [[memory-repo-copy]], [[protect-codex-and-other-ais]], [[repo-is-public]].
