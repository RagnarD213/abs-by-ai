---
name: github-push-false-failure
description: "git push can print 'remote: fatal error in commit_refs / [remote rejected]' while the push actually SUCCEEDED — always verify with fetch before retrying or re-committing"
metadata: 
  node_type: memory
  type: project
  originSessionId: 2e38e42c-56c9-43f2-99b1-70197a934707
  modified: 2026-09-09T20:54:18.973Z
---

Measured 2026-09-09. Two consecutive `git push origin main` runs printed:

```
remote: fatal error in commit_refs
 ! [remote rejected] main -> main (failure)
```

but the commit was already on `origin/main`. Retrying, re-committing or force-pushing on the
strength of that message would have created duplicate or conflicting history.

**Verify before reacting:**

```bash
git fetch origin main && git branch -r --contains <sha>   # or: git rev-list --objects origin/main..main | wc -l
```

Zero objects to push (or the sha listed under `origin/main`) means it landed and there is nothing to fix.

`git count-objects -v` on this repo also reports dozens of `tmp_obj_*` / `… 2` duplicates in
`.git/objects` — the macOS/iCloud duplicate-file pattern, since the project lives under
`~/Documents`. It is noisy but not what caused the message. Do NOT run `git gc --prune` or any
history rewrite to "fix" it without asking Dan — the repo's `.git` is ~20 GB after an old
8.3 GB video leak. Related: [[repo-is-public]], [[auto-commit-push]].
