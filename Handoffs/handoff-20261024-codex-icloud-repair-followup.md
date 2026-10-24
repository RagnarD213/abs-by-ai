# Codex after the iCloud move: finish the morning brief recovery (Codex)

Written 2026-10-24 by Claude Opus 5.5. Tooling / ops, not a video. Recommended: **Codex, GPT-6.1 Sol, high.**
Run it in the existing Codex chat "Recover morning brief collection", or a new chat in the Abs By AI project.

## What broke (diagnosed 2026-10-24)

1. **Codex's own folder never left iCloud.** On 2026-10-21 Dan turned off iCloud Desktop & Documents. Every
   `~/Documents` entry became a symlink into `~/Library/Mobile Documents/com~apple~CloudDocs/Documents/`. On
   2026-10-23 Claude moved only its own folder out (`~/Projects/Claude`). `~/Documents/Codex` (7.3 GB, 45,920 files,
   holding the morning-brief code and private proofs: `2026-09-30/task/*`, `2026-10-08/task-2/{clean,private}`) stayed
   in iCloud with **3,162 cloud-only files**, including `clean/.git/objects`, `clean/scripts/ads`, `clean/node_modules`
   and several brief proof JSONs. Opening them hangs or fails. The last brief edition is 2026-10-21 07:35.
2. **The brief collector matched sessions letter for letter.** `scripts/brief/planning.py` compared Claude session
   `cwd` to `Path(...).resolve()`. After the move the resolved project is `~/Projects/Claude/...`, while 1,582 of 1,586
   desktop session records say `~/Documents/Claude/...`. It matched **0**. It also looked for transcripts only in
   `~/.claude/projects/-Users-danielrose-Projects-Claude-Projects-Abs-By-AI`, but older ones are under the
   `-Documents-` and `-Library-Mobile-Documents-` folders.
3. Codex **project** chats were not broken: `codex exec` in the Abs By AI project from both the old and new path read
   git status and wrote a file (verified 2026-10-24 09:53). Config is `danger-full-access`, so no sandbox block there.

## Done by Claude (2026-10-24)

- Commit `ef5d7a3` on `main`: `planning.py` compares real paths (`same_project`) and looks up each session's
  transcript under the folder named after that session's own cwd (`transcript_for`). New test
  `test_session_recorded_under_old_symlinked_project_path`; all 30 tests in `scripts/brief/tests/test_inputs.py` pass.
  Live check: 0 → 1,582 sessions matched; 4 planning sessions in the last week examined, status `partial`
  (one transcript not found).
- Commit `9d058a9`: `scripts/icloud-move/rename.sh` takes a folder name. **`rename.sh Codex` is running in the
  background (nohup)**: it re-requests the 3,162 downloads every 10 min (restarting `bird` when stalled), then moves
  the folder with `evacuate.py` to `~/Projects/Codex`, leaves a symlink at every old path and points
  `~/Documents/Codex` straight at it. Log: `~/Projects/.icloud-move.log` (look for `DONE` or `INCOMPLETE`).
  iCloud reported its last sync as 2026-10-23 09:22, so downloads may take hours.
- `~/.codex/config.toml` is unchanged (backup `config.toml.bak-20261024-icloud`).

## Your steps (Codex)

1. **Do not use `~/Downloads/Start-Morning-Brief-Repair.command`.** It points a workspace-write sandbox at
   `2026-10-08/task-2/clean`, an Oct 8 clone with cloud-only git objects. Run the brief from the main project instead
   (`/Users/danielrose/Projects/Claude/Projects/Abs By AI`, `git pull` first so `ef5d7a3` is present), or `git pull`
   inside `clean` once its files are local.
2. Run the collector once (`python3 scripts/brief/collect_inputs.py ...` with the brief's usual state dir under
   `2026-09-30/task/.private-brief-proof`) and confirm `sources.planning.status` is `ok` or explain `partial`.
   Confirm the next brief edition generates and publishes.
3. Check `tail ~/Projects/.icloud-move.log`. If `DONE`: confirm `ls -l ~/Documents/Codex` points at
   `~/Projects/Codex`, `find ~/Projects/Codex -flags +dataless | wc -l` is 0, `git -C ~/Projects/Codex/2026-10-08/task-2/clean status`
   works, and add `[projects."/Users/danielrose/Projects/Codex"] trust_level = "trusted"` to `~/.codex/config.toml`
   (keep the old entries). If cloud-only files are stuck for a day: `brctl download <file>` on a few, `killall bird`,
   and as a last resort recreate `clean` and `node_modules` from GitHub/npm (both are rebuildable) instead of waiting.
4. Never re-enable iCloud Desktop & Documents. Never `rm -rf` a symlinked folder with a trailing slash.
5. Report to Dan in plain words, with the two wrap-up boxes.

Lesson recorded in memory `protect-codex-and-other-ais`: test machine-level changes on Codex too.
