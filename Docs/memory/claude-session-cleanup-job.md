---
name: claude-session-cleanup-job
description: launchd job that auto-closes idle Claude Code session processes every 30 min; closes only on 12h conversation inactivity + zero child processes; never kill sessions by process age
metadata: 
  node_type: memory
  type: reference
  originSessionId: d9eb0211-bb9b-4e5f-9c94-983ec4809b30
  modified: 2026-09-13T19:19:35.939Z
---

Set up 2026-09-13 at Dan's request after 33 idle sessions held ~4.5 GB.

- Script: `~/bin/claude-cleanup.sh` (`--dry-run` to preview). Plist: `~/Library/LaunchAgents/com.danrose.claude-cleanup.plist`, every 30 min. Log: `~/Library/Logs/claude-cleanup.log`.
- Closes a session ONLY if: its transcript `.jsonl` untouched 12h (4h when free memory < 15%), it has NO child process at all, and its transcript is uniquely identified (`--resume=<id>` in args, else a transcript born 0–5 s after process start). Anything uncertain is kept.
- **Why not process age:** the one-off manual cleanup on 09-13 killed by age >12h with no child check and stopped the Ad 3 vertical session's 2 background render tasks (session started 09-11, still working). Running background tasks are children of the session process; killing the session kills them.
- Traps: `pgrep -P` misses these children on this Mac — use `ps -axo ppid=`. Don't read `ps eww` on session processes: the environment carries the OAuth token.
- Disable: `launchctl unload ~/Library/LaunchAgents/com.danrose.claude-cleanup.plist`.
