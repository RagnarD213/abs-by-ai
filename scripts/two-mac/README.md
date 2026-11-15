# Two Macs, one GitHub: how the project folders stay level

Two Macs (M6, M2 Pro) each hold their own copy of this repo at `~/Projects/Claude/Projects/Abs By AI`, and many
Claude and Codex sessions work in each copy at once. Since 2026-11-15 a small job on each Mac keeps both copies
level with GitHub. History: `Docs/TWO_MAC_EDIT_ROUTING_RECEIPT_20261114.md`.

## What a session does

Nothing new. Commit and push your own files with `scripts/git/safe-push.sh -m "message" -- <files>`.
If it stops because another session's unsaved edits are in the way (exit 2), your commit is safe on this Mac and
the job below pushes it within 30 minutes. Do not wait, retry in a loop or ship the same change again from a
clean checkout (that is what created duplicate commits).

## What the job does (`checkout-sync.py`, every 30 minutes on each Mac)

1. **Push.** Commits GitHub lacks are merged with GitHub's `main` inside git's object store
   (`git merge-tree --write-tree`), with no working folder involved, so unsaved edits cannot block it. The merge
   commit is pushed with the Mac's SSH key.
2. **Level.** `reconcile-checkout.py` then updates the folder to GitHub's version and keeps every unsaved edit
   (three-way merge; a copy of each touched file goes to `tmp/checkout-reconcile-<date>-<time>/`).
3. `AI_COORDINATION.md` and `Handoffs/README.md` are marked `merge=union` in `.gitattributes`: when both sides
   add or change entries at the same spot, both sides' lines are kept. A changed entry can show twice (old and
   new); its owner deletes the old line.
4. `Handoffs/video-editing/jobs.json` is merged job by job and field by field (`jobsmerge.py`): when both sides
   changed the same field of one job, the higher `rev` wins and the job is marked to sync again. Equal `rev` with
   different content is a real conflict and stops the job (cause A or B below).
5. In other record files (`.md`, `.txt`, `.json`) three kinds of collision are settled by rule (`textmerge.py`),
   never dropping a line either side wrote: one side's lines contain the other's; both sides changed different
   lines of one block (neighbouring table rows); both sides added different lines at the same spot (`.md`/`.txt`
   only); a `.json` file that is one list of entries (waitlist, cover registry) is merged entry by entry. The
   same line or entry changed two ways, and every code file, still stops the job for a person or session.

Commands (either Mac):

```bash
python3 scripts/two-mac/checkout-sync.py --status
```

```bash
python3 scripts/two-mac/checkout-sync.py --dry
```

```bash
python3 scripts/two-mac/checkout-sync.py
```

`--install` installs or refreshes the job (LaunchAgent `com.absbyai.checkout-sync`; it runs its own copy in
`~/.absbyai-checkout-sync/bin/`, refreshed from GitHub each run). Log: `~/.absbyai-checkout-sync/sync.log`.
Tests: `python3 scripts/two-mac/test_checkout_sync.py`.

## When the sync stops

`--status` (and the drift notice sessions see) starts with `STOPPED` and names the cause. Nothing is ever lost or
overwritten in that state. Two causes need a session:

**A. "cannot be merged with GitHub automatically"**: a commit here and a commit on GitHub changed the same lines.
Merge by hand in the clean checkout, never in the project folder:

```bash
W=~/Library/Caches/absbyai-git-sync/integration; cd "/Users/danielrose/Projects/Claude/Projects/Abs By AI" && git fetch origin && { [ -d "$W" ] || git worktree add --detach "$W" origin/main; } && cd "$W" && git checkout --detach origin/main && git merge --no-ff main
```

Read both sides of every conflict. Records (master edit list, jobs.json, waitlist, covers map): both sides'
entries survive, and for one entry changed twice the newer status wins. Code: check first whether the local commit
already shipped from another checkout (`git log origin/main -- <file>`); then GitHub's side wins. Run the tests of
any code you merged, commit, then `C=$(git rev-parse HEAD); git push origin "${C}:refs/heads/main"`. The next sync
run levels the folder.

**B. "edited here and on GitHub in the same lines"**: commits are on GitHub, but the folder cannot move forward
because an unsaved edit collides with GitHub's change to the same file. The file's owner commits it with
`safe-push.sh` (it will stop; the job then pushes it, or reports cause A). A file untouched for 2 hours has no
live owner: any session may commit it as it is (`safe-push.sh --adopt-stale` rule in `AGENTS.md`), or, for a stale
generated file such as `output/social-queue-artifact/queue.json`, run
`python3 scripts/two-mac/reconcile-checkout.py --take-github=<path>` (the local copy goes to the backup folder).
Never copy GitHub's version over a file another session edited in the last 2 hours.

Never in the project folder: `git stash`, `git reset --hard`, `git rebase`, `git pull`, `git add -A`, force-push.
