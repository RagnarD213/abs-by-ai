# Existing edits: automatic original-chat resume, November 14, 2026

Owner: Codex on the M6. Dan requested that he can continue existing edits in their original chats without adding Mac-routing instructions.

## Installed behavior

- Every resume checks which Mac holds the edit. The original chat remains the sole editor and sends commands to that Mac through `.claude/skills/_shared/editroute/resume.py run JOB -- COMMAND`. It does not launch another AI, move work folders, copy approvals or start a new editing round by itself.
- The existing mandatory `editcap.py acquire`, `heartbeat` and `wait` CLI commands now perform the ownership check before changing the local slot registry. Exit 5 identifies a remote edit and prints the automatic continuation command for the editor. Exit 6 reports unavailable/unverified ownership and does not acquire a local slot. Old chats therefore receive the continuation instructions from the tool even if their earlier context predates this update.
- The helper uses the owning Mac's project checkout by default, supports an explicit remote working folder, streams stdout/stderr and stdin into the original chat, and preserves command exit codes. It never retries an uncertain build. The editing AI must read/write build code on the owner too, acquire the edit slot there, and follow the normal render queue, review mirroring and delivery workflow.
- Named-Mac recommendations and explicit-move rules remain in force. The overnight queue remains paused. Programmatic callers of `editcap.acquire()` are unchanged and must explicitly use the resume check; the new guard covers the CLI used by the editing skills. This is automatic routing within the editing workflow, not an OS-level interception of arbitrary commands.

## Files installed on both Macs

`editroute/resume.py`, its tests, the `editcap.py` CLI guard, AGENTS.md, VIDEO-RULES.md, editroute/README.md, the video-rounds runbook, and the Shorts/long-form/ad skills. Pushed with `scripts/git/safe-push.sh` in commits `84a1066`, `19cfbf8`, `bbd03c0`, and `dd6e7ba`.

The active Claude handoff-03 task is independently changing routing code and its README on the M2. Those changes were preserved: the resume section was inserted into the live file, and no unrelated router code or session was overwritten. The M2 README therefore also contains that task's queue and sleeping-drive additions.

## Verification

- New resume tests: **9 pass on each Mac**. They cover existing ownership, an unreachable Mac, new-job routing, literal command arguments, stdin isolation, working folders, command failure codes, no AI launch/retry, and preventing local acquire/wait on the wrong Mac.
- Full routing suite after the stdin fix: **39 pass on M6; 53 pass on M2** (the M2 has additional tests from the active routing task). Existing editcap selftests: **27 pass on each Mac**.
- Live CLI proof: `editcap.py acquire DS-39` on the M6 returned **5**, identified M2, and printed the original-chat remote path without acquiring a local slot.
- Live read-only command proof from this M6 chat:
  - **DS-42**: host `m2`, working folder `/Volumes/Extreme/_edit_work/DS-42`, `GATE_GROUP=DS-42`, exit 0.
  - **DS-39**: host `m2`, working folder `/Users/danielrose/Projects/_edit_work/DS-39/round2`, `GATE_GROUP=DS-39`, exit 0.
- Live M2 stdin/exit-code proof: a harmless command received the exact piped text including literal `$()` and returned its deliberate exit code **17**. An initial test caught the ownership SSH probe consuming stdin; fixed by isolating probes with `/dev/null`, then repeated successfully.
- Real edit files, rendered videos and approval checkpoints were not changed; neither edit was resumed for production. A full render through these two old chats has not been claimed or performed.

## Dan's next action

Reply with normal feedback or continuation in the original edit chats. No extra Mac instructions or separate routing prompt is needed. The editor follows the ownership result and uses the remote command helper. A persistent connection/ownership problem is reported as a blocker instead of starting a duplicate local edit.
