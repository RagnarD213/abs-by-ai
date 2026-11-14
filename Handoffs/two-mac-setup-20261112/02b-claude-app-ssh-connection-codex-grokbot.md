# 02b: Add the M2 as an SSH connection in the Claude app on the M6 (Codex or Grokbot, on the M6)

Category: ops. Written by Claude on 2026-11-14 because this step is a click inside the Claude desktop app's own settings, which Claude cannot reach from its session (no computer use, and the app keeps its SSH list in internal storage, not in a file). Dan authorizes the whole step, including any password or approval prompt. Do it all; do not stop to ask Dan.

## Why

Handoff 03 (edit routing) starts Claude edits on the M2 from the M6 through the Claude app's SSH connection, so the session shows in Dan's M6 sidebar but works on the M2. Today the app has **no saved SSH connections** (checked 2026-11-14 11:15 a.m. with Claude's `list_start_targets`: `ssh: []`). Everything else for the link already works.

## Facts (verified 2026-11-14)

- The M6 reaches the M2 at `10.66.0.2` over the Thunderbolt Bridge, ping about 0.4 ms.
- `~/.ssh/config` on the M6 already has the alias: `Host m2`, `HostName 10.66.0.2`, `User danielrose`, `IdentityFile ~/.ssh/id_ed25519`. `ssh m2 hostname` returns `m2` with no password.
- Claude Code is installed on the M2 at `~/.local/bin/claude` (not on the non-interactive PATH; the app normally installs its own remote helper anyway).
- M2 project folder: `/Users/danielrose/Projects/Claude/Projects/Abs By AI`.

## Steps (on the M6, in the Claude desktop app)

1. Open the Claude app, Code tab. Start a new session and open the place/folder picker (or Settings, if it lists SSH connections there).
2. Choose **SSH** and **add a connection**:
   - Name: `m2` (exactly; handoff 03 refers to it by this name)
   - Host: `m2` if the app reads `~/.ssh/config`, otherwise `10.66.0.2`
   - User: `danielrose`
   - Key: `~/.ssh/id_ed25519` (the M6's key, already in the M2's `authorized_keys`)
   - Default folder: `/Users/danielrose/Projects/Claude/Projects/Abs By AI`
3. Connect once. Accept the host key and let the app install whatever it needs on the M2. If it asks to trust the folder, trust it. If it asks Claude Code on the M2 to sign in, sign in with Dan's Claude account.
4. Do not start an edit on it. Close that test session (do not archive or delete any other session).

## Verify, then report

- The new-session picker lists `m2` with its folder, and a test session there runs `hostname` and gets `m2`.
- Append a short "02b" section to `Docs/TWO_MAC_M6_SETUP_RECEIPT_20261113.md` (what was entered, what the app installed on the M2, anything refused). Push with `scripts/git/safe-push.sh`. Mark 02b done in the two-Mac line of `Handoffs/README.md`.

Done looks like: Claude's `list_start_targets` shows an SSH connection named `m2`, so handoff 03 can start Claude sessions on the M2 from the M6.

## Status note (Claude, 2026-11-14)

Claude tried this step from a Code session on the M6 and could not do it. Dan turned Computer use on, but it permanently refuses to let Claude control the Claude app itself (by design, it cannot be granted), and the SSH list lives in the app's internal storage (not safe to hand-edit). Re-checked just now: `ssh m2 hostname` returns `m2` with no password, and `list_start_targets` still shows `ssh: []`. This handoff is still open for Codex or Grokbot, steps unchanged.


## Completed by Codex, 2026-11-14

**DONE.** Added and tested the `m2` SSH connection and saved an `m2` environment with the requested project folder. The desktop test session returned `m2` from `hostname`; its integrated terminal returned the exact requested folder from `pwd`. Claude installed its remote helper and CLI automatically, without a sign-in prompt. Archived only the disposable test session; no edit started. Details and installed versions: [02b receipt](../../Docs/TWO_MAC_M6_SETUP_RECEIPT_20261113.md#02b-claude-desktop-ssh-connection-completed-codex-november-14-2026). This supersedes the earlier open status note.
