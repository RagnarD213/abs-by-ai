# Stall watchdog (`stallwatch`)

A video job that dies while its session is idle gets noticed and restarted instead of sitting dead for hours
(built 2026-11-05). Rule: `VIDEO-RULES.md`, render queue section, "Chains are watched by their EXIT".

**Why:** on 2026-11-04 the Man Boobs LFC R3 chain (RO-31) died at 8:22 PM on a Python SyntaxError in its finish step.
The error went to `final/logs/finish.log`, not the chain log. The session's background watcher only grepped the chain
log for DONE/error strings, so it never fired, and the job sat dead 11 hours until Dan asked at 7:20 AM.

## Layer 1, for every editing session: watch the exit

Chain script header and footer (bash):

```bash
#!/bin/bash
set -Eeuo pipefail
trap 'echo "CHAIN_FAILED at line $LINENO: $BASH_COMMAND"' ERR
cd "$(dirname "$0")/.."          # run from the job folder
# ... steps, each logging wherever it likes ...
echo CHAIN_DONE
```

Start it from the job folder with `run_in_background` (Claude) or `nohup` (Codex):

```bash
python3 .claude/skills/_shared/stallwatch/stallwatch.py run RO-31 -- bash recipe/chain_r3c.sh
# with the render queue:
python3 .claude/skills/_shared/stallwatch/stallwatch.py run RO-31 -- python3 .claude/skills/_shared/renderq/renderq.py run --group RO-31 -- bash recipe/chain_r3c.sh
```

The background task ends when the chain ends, whatever it printed, so Claude is re-invoked on any exit, crash or
`kill`. The wrapper passes the exit code through and prints `CHAIN_DONE <JOB>` or `CHAIN_FAILED <JOB> exit N` plus
the last 20 lines of the newest `*.log` in the folder (that is where the SyntaxError was). It also records the run
(pid, folder, session) in `/tmp/absbyai-stallwatch/runs/`, so the watchdog knows the job even when it holds no edit
slot. `--log FILE` names the log when the chain does not run from a job folder.

Never arm a watcher that greps one log for DONE or error strings. If you must wait on something already running,
wait on the process: `while kill -0 $PID 2>/dev/null; do sleep 30; done; tail -40 <newest logs>`.

## Layer 2, the backstop: the 15-minute routine

`edit-stall-watchdog` (Claude scheduled task, every 15 minutes, `~/.claude/scheduled-tasks/edit-stall-watchdog/`)
runs `stallwatch.py scan --claim --json`. No AI work when nothing is stalled: one script call, one line.

**Watched jobs:** edits holding a slot in the edit cap (`editcap.py`: active, promoted, or stalled by its 3-hour lease)
plus every chain recorded by `stallwatch.py run` in the last 24 hours. Edits with Dan or waiting for a slot are not.

**A job is STALLED when all three hold:**
1. nothing for it is alive: no render-queue step, no recorded run still running, and no working process in `ps`
   whose folder or command line is in the job's work folder (`/Volumes/*/_edit_work/<JOB>*`). Watch loops (`tail`,
   `grep`, `sleep` loops, a `bash -c` whose children are only those) and review servers do not count as life;
2. its newest log changed 20+ minutes ago (and within the last 24 hours, and after the edit took its current slot,
   so last round's logs never count);
3. no DONE: the newest log has no `CHAIN_DONE` after its last `CHAIN_FAILED`, does not end on a `DONE` line, and the
   last recorded run did not exit 0.

**Then:** the owning Claude session (the one recorded at `editcap.py acquire` or `stallwatch.py run`) gets a message
naming the job, the newest log and its last error line, and asking it to restart the failed step from its checkpoint.
At most 2 nudges, 30 minutes apart; if it is still dead 30 minutes after the second, Dan gets a phone notification
and a Mac notification instead. A new log line, a new run or a live process resets the count.

**Codex-owned jobs** go straight to Dan with the Codex thread id: nothing on the Claude side can post into a Codex
thread. A Codex heartbeat automation (see `../editcap/README.md`) can call
`python3 .claude/skills/_shared/stallwatch/stallwatch.py check <JOB>` (exit 5 = stalled, with the reason).

**Flagged but fine** (planning, waiting on Dan without releasing the slot): `stallwatch.py ok <JOB>` silences that
stall until the job's logs or runs change. Better: `editcap.py release <JOB> --review` when waiting on Dan.

## Commands

`S=.claude/skills/_shared/stallwatch/stallwatch.py`

| command | what |
|---|---|
| `python3 $S scan` | every watched job and its state (read-only) |
| `python3 $S scan --claim --json` | the routine's call: also records the nudges it returns as sent |
| `python3 $S check RO-31` | one job; exit 5 if stalled |
| `python3 $S ok RO-31` | silence the current stall |
| `python3 $S unsent RO-31` | undo the last claimed nudge (the message could not be delivered) |
| `python3 $S selftest` | 27 checks, real processes, temporary folders, about 10 s |

It never kills, restarts or edits a job. State: `/tmp/absbyai-stallwatch/` (`STALLWATCH_DIR`), cleared by a reboot.
Tuning: `STALLWATCH_QUIET_MIN` (default 20), `NUDGE_GAP_S`, `MAX_NUDGES` at the top of `stallwatch.py`.

## Files

`stallwatch.py` (CLI and library), `selftest.py` (the 2026-11-04 incident replayed: crashed chain detected after
20 min, its session nudged once, second nudge after 30 min, then Dan once; a healthy render quiet for 2 hours never
flagged; a run still alive; the grep/sleep watcher and a review server not counted as life; CHAIN_DONE, CHAIN_R3_DONE and per-step DONE lines; old-round
logs ignored; with-Dan edits skipped; Codex to Dan; `ok`; `check` exit 5).
