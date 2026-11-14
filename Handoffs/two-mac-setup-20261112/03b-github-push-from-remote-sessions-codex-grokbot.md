# 03b: Let remote sessions push to GitHub, and push what is waiting (Codex or Grokbot)

Category: ops. Written by Claude on 2026-11-14 because this needs a signed-in, on-screen session and a change in Dan's GitHub account, neither of which a remote Claude session can do. Dan authorizes the whole step, including the GitHub sign-in and any password or approval prompt. Do it all; do not stop to ask Dan. Do not write any token or key into a file in this repo (the repo is public).

## The problem (verified on both Macs, 2026-11-14 12:34)

Git's saved GitHub login lives in the macOS login keychain. The keychain refuses any session that is not on screen: a Claude session on the app's SSH connection `m2`, `ssh m2 codex exec`, or a plain `ssh` shell on either Mac. `git push` there fails with `failed to get: -25308` and `could not read Username for 'https://github.com'`. Fetching works (the repo is public). So every edit that runs on the M2 from the M6 (the whole point of handoff 03) can commit but cannot push its shared files, which Dan's rules require.

## Step 1: push what is waiting on the M2 (do first)

The M2 checkout (`/Users/danielrose/Projects/Claude/Projects/Abs By AI`) holds commits that are not on GitHub: `0f64c08` "Two-Mac routing follow-up ..." and whatever was committed after it (`git log --oneline origin/main..HEAD` lists them). From an on-screen Terminal on the M2 (Screen Sharing from the M6, or a Codex task running on the M2 itself, not over ssh):

```bash
cd "/Users/danielrose/Projects/Claude/Projects/Abs By AI" && git push origin main
```

If it is rejected because GitHub moved: `git fetch origin && git merge --no-edit origin/main && git push origin main`. If the merge is blocked by someone's uncommitted edit, stop and report the files it lists; do not stash or reset.

Then bring the M6 checkout level. Its copies of the routing files already equal the pushed commit:

```bash
cd "/Users/danielrose/Projects/Claude/Projects/Abs By AI" && python3 scripts/two-mac/reconcile-checkout.py --dry
```

Read what it prints, then run it again without `--dry`. It refuses if the M6 has its own unpushed commits; in that case use `scripts/git/safe-push.sh` there as usual.

## Step 2: make pushes work from remote sessions (both Macs)

Recommended: use each Mac's existing SSH key for pushes only. Fetches stay as they are.

1. On each Mac (M2 and M6): add GitHub's host key, checking the fingerprint against https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints :
   `ssh-keyscan -t ed25519 github.com >> ~/.ssh/known_hosts` then `ssh-keygen -lf ~/.ssh/known_hosts | grep github`.
2. In Dan's GitHub account (github.com, Settings, "SSH and GPG keys", "New SSH key", type Authentication): add the contents of `~/.ssh/id_ed25519.pub` from the M2 (title `M2 Pro`) and from the M6 (title `M6`). Both keys exist and have no passphrase (checked).
3. On each Mac: `git config --global url."git@github.com:".pushInsteadOf "https://github.com/"`
4. Test from a remote shell, which pushes nothing: `ssh m2 'cd "/Users/danielrose/Projects/Claude/Projects/Abs By AI" && git push --dry-run origin HEAD:refs/heads/main'` from the M6, and `ssh m6 '...same...'` from the M2. Both must end without an error. Also confirm an on-screen push still works.

If GitHub refuses the keys for any reason, the fallback is a fine-grained token limited to the `abs-by-ai` repository (Contents: read and write), stored with `git credential-store` in a file outside the repo with mode 600, added after `osxkeychain` in the helper list. Use the SSH keys unless they are refused.

## Also seen, for whoever owns the "resume" change (commits 84a1066, 19cfbf8, bbd03c0)

`python3 .claude/skills/_shared/editcap/editcap.py selftest` passes 27 of 27 on the M2 but fails 3 CLI tests on the M6 ("five go, sixth exits 3", "status shows the waiter", "finishing one edit starts the waiter"). The tests use the job code SL-18, which has real work on the M2, so the new resume hook answers REMOTE_EDIT instead of running the test. The hook needs to stay out of the selftest (or the tests need codes no real job uses).

## Verify, then report

- Both `--dry-run` pushes in step 2.4 succeed from remote shells; `git status` on both Macs says level with GitHub (apart from other sessions' uncommitted edits).
- Add a short "03b" section to `Docs/TWO_MAC_EDIT_ROUTING_RECEIPT_20261114.md` (what was added where, what was refused), push it, and mark 03b done in the two-Mac line of `Handoffs/README.md`.
- Tell the session "Metabolism Not The Reason SFC R1" (running on the M2) that pushes work now, if it is still open.
