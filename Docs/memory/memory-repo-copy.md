---
name: memory-repo-copy
description: Memory is mirrored to Docs/memory/ in the PUBLIC repo for cloud sessions; private entries are held back by a local list; run scripts/sync-memory-to-repo.sh after writing a memory
metadata:
  type: reference
---

Since 2026-10-06 the memory folder is copied into `Docs/memory/` in the repo so cloud sessions can read it. The repo is public.

- After writing or changing a memory entry: `scripts/sync-memory-to-repo.sh`, then `scripts/git/safe-push.sh -m "Sync memory to repo" -- Docs/memory`.
- **Before syncing a new entry, decide if it is private.** Private = Dan's private life, health beyond what he says on camera, money, legal matters, other people's names or emails, logins, open weaknesses in the live product. Add its name to `.repo-private` in this memory folder and it never leaves the Mac.
- An entry that scripts need but that holds private detail: name it in `.repo-redacted` and hand-write a clean `Docs/memory/<name>.md`.
- `type: user` entries are held back unless published with `--add <name>`.
- The script's scan stops on keys, phone numbers, unknown emails, street addresses and the terms in `.repo-blocked-terms`.

Related: [[repo-is-public]], [[auto-commit-push]].
