---
name: protect-codex-and-other-ais
description: "Before any machine-level change (moving folders, paths, symlinks, config, scheduled jobs), check and test what it does to Codex and every other AI Dan uses, not just Claude."
metadata:
  node_type: memory
  type: feedback
  modified: 2026-10-24T14:53:57.605Z
  originSessionId: 472e103a-ca98-4f25-9bf7-5e54770fa23b
---

Dan, 2026-10-24: "be more careful about breaking things for Codex and other AIs I'm using in the future. This is
seriously slowing me down, and we have to avoid mistakes like this going forward."

What happened: the 2026-10-21/23 iCloud work ([[documents-symlinked-into-icloud]]) was tested only for Claude
(files, git, rendering). Codex's own working folder `~/Documents/Codex` (7.3 GB, where its morning-brief code and
proofs live) was left in iCloud with 3,000+ cloud-only files, and the morning-brief collector compared Claude session
folders letter for letter, so after the move it matched 0 of 1,586 sessions and looked for transcripts only under the
new path's log folder (`~/.claude/projects/<slug of cwd>`). The Codex morning brief produced nothing after Oct 21 and
Dan spent a morning on it with Codex. Codex project chats themselves kept working (old path is a symlink).

**Why:** Dan runs Claude and Codex side by side on the same project (plus Gemini, ChatGPT, scheduled routines).
A change that only Claude verifies can silently break the others, and he is the one who pays for it in lost time.

**How to apply:** before moving folders, renaming paths, changing symlinks, shared config, hooks or scheduled jobs:
1. List who reads that path: grep `~/.codex` (config.toml, .codex-global-state.json, automations/*.toml),
   Claude scheduled tasks, launchd agents, scripts in `scripts/` and any path-matching code (exact-string path compares
   break on symlinks; compare `realpath`).
2. Update or migrate those references in the same task, keeping the old path working as a link.
3. Test it from Codex too (a real `codex exec` in the project that reads and writes a file), not only from Claude.
4. Report to Dan which AIs were checked. If one cannot be tested, say so before calling the change done.

**Second trap (2026-10-25):** Codex keeps a per-chat permission record for its auto-resume timers in
`~/.codex/.codex-global-state.json` → `heartbeat-thread-permissions-by-id`. Chats started with the `:workspace`
profile (workspace-write, ask-first, no network) have their workspace on the old `~/Documents/Claude` link, so every
command fails the sandbox and waits for a click ("Awaiting approval" in the sidebar). Working chats show
`dangerFullAccess` / `never`. The app rewrites that file every few seconds, so fix it in the app (composer permission
menu, after Dan turns on Settings > General > Full access, a security switch only Dan flips), never by editing the
file. A running turn keeps its old policy: stop the turn, leave the composer on Full access, send "continue"; the
new turn shows `disabled`/`never` in `~/.codex/state_5.sqlite` threads.sandbox_policy (verified 2026-10-25). Cloud Codex chats cannot be given folders at all; Mac-bound work like the morning brief belongs in a local chat.
