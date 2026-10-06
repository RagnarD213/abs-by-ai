---
name: qc-corpus-worktree-trap
description: qc_corpus/run.py in a git worktree reports fake BLIND/TIGHT mismatches unless untracked assets are symlinked in
metadata:
  node_type: memory
  type: project
  originSessionId: 754b4108-4871-4541-8503-ee4cc668a9f9
  modified: 2026-09-28T21:39:52.027Z
---

Running `.claude/skills/_shared/qc_corpus/run.py` from a git worktree (2026-09-28) gave 10 false mismatches. The causes were three things git doesn't carry: the git-ignored `qc_corpus/excerpts/` cache, the compiled `shorts/reference/recentre/personmask` Apple Vision binary (without it the framing rows read NOT MEASURED), and untracked media folders at the repo root. The audio selftest also fails there because some media folders are only partly tracked, so symlinking the top-level folder does not work.

**Why:** a clean worktree off origin/main is the safe way to edit the gate while another session has uncommitted gate edits.
**How to apply:** symlink `excerpts/`, `personmask` and the missing top-level folders into the worktree. Run the selftest in the main checkout (valid when `_shared/audio` is identical there), then compare any mismatch against unmodified origin/main before blaming the change. `ds17-r4-final-approved` was red on main 2026-09-28; fixed 2026-09-29 (audio gate 2.0.0 attribution + its `--untreated` baseline). Related: [[shared-fix-may-not-reach-the-pipeline]]
