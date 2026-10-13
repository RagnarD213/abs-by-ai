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

**Recipe that passed from a worktree (2026-10-13, gate 2.6.0, CORPUS PASS 178 entries):**
- For each corpus entry under the repo root: link the first missing folder on its path to the main folder's copy; where the folder exists but is partly tracked, link each missing child. Also link every missing child of `Media/` (ffmpeg and the Whisper cache live there).
- `qc_corpus/excerpts` is a tracked link, and a worktree checks it out as a 46-byte text file (`core.symlinks` is false). Swap it for a real link to `/Volumes/Extreme/_edit_work/qc_corpus/excerpts` for the run, then put the text file back.
- Remove the links afterwards with `find . -type l -lname "<main folder>/*"`; never `git add -A`.
- The audio selftest passes in a worktree with those links. It used to share `/tmp/audio_selftest` with every other session and fail at random when two ran at once; fixed 2026-10-13 (own folder per run).
- Under load the run took 68 minutes, and its per-entry lines stay buffered for a long time: check the child process, not the log.
- If the app's sync tool refuses to merge main into the worktree (protected `.claude/skills` files, origin not confirmed), Dan confirms the origin once at Help, Troubleshooting, Review Pinned Git Origins. Until then: build the commit on top of `origin/main` with a three-way merge per file and push that, without merging into the worktree.
