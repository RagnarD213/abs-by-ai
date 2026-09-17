# Overnight edit queue

Keeps up to two video edits running from `Handoffs/video-editing/jobs.json` with nobody at the keyboard, and hands
Dan a short review page. Design and Dan's decisions: `Handoffs/handoff-20260917-overnight-edit-queue.md`.
Built 2026-09-17 (Phases 0–1). **Phase 2 (placeholder flow for AI-clip slots) is not built.**

## For Dan, in plain language

* **What runs on its own:** every 15 minutes a small script (not an AI, costs nothing) looks at the job list. If a
  build slot is free and nothing says stop, it starts the next job with the right tool (the table below), lets a
  *different* AI review the result, allows one automatic fix round, then puts the video on your review page.
* **Your review page:** http://127.0.0.1:8830 (on the Mac mini). Watch, then Approve, Send back, or Reject. Your words
  are saved exactly as you say them.
* **Pause everything:** `python3 scripts/edit-queue/dispatcher.py pause`. Or create an empty file named `PAUSE` in
  `scripts/edit-queue/`. A job that is already running finishes; nothing new starts. Undo with `... dispatcher.py resume`
  (or delete the file).
* **Remove it completely:** `scripts/edit-queue/install.sh uninstall`.
* **See what it would do right now, without doing it:** `python3 scripts/edit-queue/dispatcher.py status`.

It will never launch anything when: the PAUSE file exists · 4 videos are already waiting for your review ·
the Extreme drive is unplugged or under 150 GB free · both build slots are busy (your own sessions count) · it
already started 3 jobs tonight · the tool it needs is signed out or hit its usage limit in the last 2 hours.
While you are using the Mac (keyboard or mouse in the last 10 minutes) it uses one slot, not two.

## Who edits what (`config.json` → `routing`; Dan, 2026-09-17)

| jobs | tool | reviewer |
|---|---|---|
| `RA` raw ads, `RO` organic long-form, `DS` dedicated shorts (all raw-footage first cuts) | **Codex** | Claude `ra-reviewer` |
| `AV` ad verticals, `AS` ad squares, `SL` shorts from a long-form (all secondary cuts) | **Claude** | a fresh Codex session |
| `RX` | never queued | |

Flip a row by editing `config.json`. Nothing re-routes itself; the scoreboard only records.
**Pilot limits (`config.json` → `unattended`):** groups `AV/AS/SL`, size `S`, 3 launches a night. Raw cuts (`RA/RO/DS`)
join after Phase 2, because most of them have AI-clip slots that need Dan's frame approval.

## Files

| file | what it is |
|---|---|
| `queue.py` | the only writer of job state. New: `claim`, `heartbeat`, `release`, `stall`, the `stalled` state, a write lock |
| `config.json` | routing table and every number |
| `dispatcher.py` | the 15-minute tick: `tick`, `tick --dry-run`, `status`, `pause`, `resume`, `pause-group`, `resume-group`, `launch-one` |
| `runner.py` | runs one job inside its slot: edit → cross-review → one revision → `delivered` or parked |
| `preamble.md`, `reviewer-brief.md` | the fixed text put in front of every unattended edit / review |
| `review_page.py` | the review page server (port 8830) and a static snapshot |
| `scoreboard.json` | one row per run: tool, reviewer verdicts, gate, revision rounds, hours, spend, Dan's verdict and words |
| `launchd/`, `install.sh` | the two background jobs: `com.absbyai.edit-queue` (tick) and `com.absbyai.edit-queue-review` (page) |
| `tests/` | `python3 scripts/edit-queue/tests/test_edit_queue.py` and `test_runner_end_to_end.py` (fake editor, spends nothing) |

Logs: `~/Library/Logs/absbyai-edit-queue/`; per job `/Volumes/Extreme/_edit_work/<JOB>/queue-run.log`.

## How a slot is counted

By **claims**, not processes: an editing session spends most of its time thinking, so counting ffmpeg would start a
third build. `claim: {by, pid, started, heartbeat}` sits on the job record; the runner touches the heartbeat every
5 minutes and holds the claim through the review. Builds that belong to nobody's claim (Dan's sessions, hand-fired
jobs) are counted from the `00-RULES.md` §1.3 process pattern, grouped by parent process; over-counting is the safe side.
A claim with no heartbeat for 45 minutes **and** a dead pid becomes `stalled`. A stalled job is **never restarted
automatically**: look at its work directory, then `queue.py release <ID>` and `queue.py set <ID> ready`.

A job is skipped when: its state isn't `ready`; it has an open "Your calls" row in `00-MASTER.md`; its ID appears in
`AI_COORDINATION.md` ACTIVE; a work directory with a build in it already exists (`ra01`, `ds-17`, `AV-01` spellings);
a source file named above the doc's `## Deliver` heading is missing; it carries `"unattended": false`; or its group is
paused. `dispatcher.py status` prints the reason per job.

## The contract with a launched session (`preamble.md`)

Work in `/Volumes/Extreme/_edit_work/<JOB>/`. Finish by writing `DELIVERY.json` there, or `BLOCKED.md` for a real
blocker. Do **not** set `delivered`: the runner does that only after the independent reviewer writes
`QUEUE-REVIEW-<n>.md` with a first line of `VERDICT: SHIP`. `DOES NOT SHIP` buys one automatic revision; after that
the job parks as `needs` with the review attached. No verdict line = the review did not run = parked.

## Exactly how the sessions are launched (Phase 0 findings, 2026-09-17)

**Codex: PROVEN headless with no prompt.** Smoke test wrote to the work drive, ran the project ffmpeg, ran
`queue.py`, and listed Drive through rclone:

```
/Applications/ChatGPT.app/Contents/Resources/codex exec -C <repo> -s workspace-write \
  -c 'approval_policy="never"' -c sandbox_workspace_write.network_access=true \
  --add-dir /Volumes/Extreme/_edit_work/<JOB> --add-dir ~/.config/rclone --add-dir ~/.cache  -   # prompt on stdin
```
codex-cli 0.154.0-alpha.6.2, already signed in. ⚠ Without `--add-dir ~/.config/rclone`, rclone lists Drive but cannot
save its refreshed token (`operation not permitted`). If a full edit hits another sandbox wall, set
`executors.codex.sandbox` to `danger-full-access`: that is what Dan's own `~/.codex/config.toml` already uses.

**Claude: NOT PROVEN. The program is signed out.** `claude auth status` → `"loggedIn": false`; `claude -p` →
`Not logged in · Please run /login`. Dan signs in once (only he can):
`~/Library/Application\ Support/Claude/claude-code/2.1.270/claude.app/Contents/MacOS/claude`, then `/login`.
The dispatcher checks `claude auth status` every tick (free) and launches no Claude job while it is signed out. The
flags it will use are **untested on a real job**:

```
<newest claude-code/*/claude.app/Contents/MacOS/claude> -p --permission-mode bypassPermissions \
  --add-dir <work dir> --model fable --effort high --strict-mcp-config \
  --disallowedTools "Bash(node scripts/youtube/*),Bash(python3 scripts/blotato/*),Bash(node scripts/ads/*)"
  [--agent ra-reviewer for a review]                                     # prompt on stdin
```
`bypassPermissions` is what this project's `.claude/settings.local.json` already grants. `--strict-mcp-config` with
no MCP config means no connectors at all (no Blotato, Gmail or Drive tools to post or send with). The versioned
folder changes when the desktop app updates, so the newest one is resolved at launch.

**launchd:** a background job started from `~/Library/LaunchAgents` reads `~/Documents`, `/Volumes/Extreme`, `ps` and
`ioreg` with no macOS privacy prompt (checked on the first tick).

## Not built yet (Phase 2 and the open ends)

* Placeholder flow: `draft_review` / `frames_approved` states, `placeholders.json`, the frame picker, night-2
  finishing, the `compliance:placeholder` gate row (corpus run + `GATE_VERSION` bump), the approved-clip library.
  `launch_states` already lists `frames_approved` first so the ordering is ready.
* Dan's pinned Edit Queue artifact does not know `stalled` (it prints the raw word). Teach it `stalled`,
  `draft_review` and `frames_approved` together in Phase 2.
* A verdict on the review page marks the scoreboard row `corpus_entry: owed`. The revision session is told to record
  Dan's words in `qc_corpus` first; an approval's corpus entry still needs a session to write it.
* Acceptance still owed: a full Claude job headless, and three consecutive clean nights.
