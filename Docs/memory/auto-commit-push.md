---
name: auto-commit-push
description: "Dan wants new builds committed and pushed automatically, without asking"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 16edf403-e1df-4efa-ab8c-abbb0e77d1a4
---

Dan (July 7, 2026): "commit and push. always do that with new builds from now on until I tell you not to."

**Why:** The site has no users yet and nobody sees it except Dan, so there's no risk in shipping straight to main (which auto-deploys via [[railway-deploy-workflow]]).

**How to apply:** After finishing and verifying a build in this project, commit and push to main without asking. Revisit this once the site has real users.

**How to push from the main folder (2026-10-01, replaces all rebase advice):** `scripts/git/safe-push.sh -m "message" -- <your files>`. It commits only the named files, merges origin/main (never rebases or stashes), clears files byte-identical to GitHub's, lets GitHub win on root `*-data.json`, retries a push race 3 times. Exit 2 = another session's edits are in the way, exit 3 = hand merge, exit 4 = push failed: report the files, one board entry, no more commits on top. Alarm: `scripts/git/drift-check.sh` (PostToolUse hook + morning brief; WARN at ahead 3 or behind 40). Worktrees push with plain git. Rule lives in `AGENTS.md`, Delivery and deployment.

**Shared files and stale blockers (Dan, 2026-10-05):** a shared file (`.claude/skills/_shared/`, `AGENTS.md`, `CLAUDE.md`, `Docs/`, `scripts/`, any skill file another job uses) is pushed with `safe-push.sh` the moment it is edited, never left for the end of the task. When the script stops on exit 2 it prints each blocking file's age. All older than 2 hours: re-run with `--adopt-stale` (backs up to `tmp/`, commits them as "Commit pending edits from earlier sessions so main can merge", pushes). Any newer than 2 hours: the owner is live, so board note and retry at the end of the task. `drift-check.sh` exits 2 (`JAM`) when the oldest unpushed commit is over 24 hours old; the morning brief clears it. Tests: `scripts/git/tests/test_git_scripts.sh`. **Why:** 41 commits sat on the Mac from 10-02 to 10-05 because unsaved shared-file edits blocked the merge and each session left them.

**Why the script exists:** every session commits from the SAME folder, so at push time GitHub has usually moved and the folder holds other sessions' uncommitted edits. `git pull --rebase` refuses there, the commit stays on the Mac, and 34 commits were stranded by 2026-10-01 (333 session transcripts hit "cannot pull with rebase"). `--autostash` is also banned: it stashes other sessions' live work.

**NEVER `git stash push -u` to get past a rejected push (2026-09-17, cost real work).** Faced with
`! [rejected] main -> main (fetch first)` and "cannot pull with rebase: You have unstaged changes",
the reflex of stash → pull → push → `stash pop` is WRONG in this shared checkout: the stash silently
takes every OTHER live session's uncommitted work off disk, and if `pop` then hits a conflict (very
likely — the commits you just pulled are those same sessions') it fails, is swallowed by `2>/dev/null`,
and their work is left orphaned in a stash while they keep running against files that no longer hold
their edits. That happened here: 20 files including AGENTS.md, CLAUDE.md and the qc_corpus (336 lines)
vanished from the tree and nobody noticed until a later `git status` showed 0 modified files.

**Do this instead:** `scripts/git/safe-push.sh` (above). A rejected push is fixed by merging, never by clearing the folder.

**If it already happened:** the stash is kept, so recovery is mechanical. `git stash show --name-only`,
then for each file compare three versions — BASE (`git rev-parse 'stash@{0}^1'`), STASH, and HEAD.
Where HEAD still equals BASE, `git show 'stash@{0}:<f>' > <f>` restores it outright. Where HEAD moved
(another session committed it), do NOT hand-resolve their code: leave HEAD's version on disk, keep the
stash, and tell them what is in it. Verify with a conflict-marker grep and a JSON parse of every
restored `.json`. ⚠ zsh does not word-split unquoted `$VARS` — a `for f in $LIST` loop silently runs
once with the whole string as one filename, which is how the merge step here looked like it passed
when it had not run at all.
