# Overnight batch repairs: receipt (November 18, 2026)

Owner: Claude (Opus 5.5), by Dan's request; Codex built the system. Handoff: [handoff-20261118-overnight-batch-start-and-permission-fixes.md](../Handoffs/handoff-20261118-overnight-batch-start-and-permission-fixes.md).
Commits: `ac39cbd` (six fixes and tests), `34a1497` (stable alert identity). Pushed from a clean worktree; both Macs synced to `34a1497`.
Live edits were not interrupted: WV-03, WV-04, RO-28 (M2) and WV-05 (M6) kept running; no editcap or renderq state was touched; `scripts/edit-queue/PAUSE` stays.

## What changed

| # | Fix | Code |
|---|---|---|
| 1 | Morning report's first line is `NOT STARTING: N queued edits will not start ... Why: ... Waiting: ...` whenever a queued round cannot start. `enqueue-chat` and `receipt` end with `CAN START` or `WILL NOT START: why`; "queued" is said only when something will launch it. | `batch.py` `start_blockers`, `headline`, `startability` |
| 2 | Source check covers only files the scheduler and workers run or read. Edit desk, tests, READMEs, benches, fixtures and snapshots no longer block. Real scheduler drift still blocks and is named. | `batch.py` `scheduler_file` |
| 3 | M2 to M6 to M2 launch removed; both Macs launch the runner directly and record its real PID. | `batch.py` `worker_command` |
| 4 | Launchd-context file probe (create, write, rename, delete) in `Videos to Review/`, the internal work folder and each mounted `/Volumes/{Extreme,Expansion}/_edit_work`, run by the agent itself every 30 minutes or on request (`batch.py drive-probe --launchd`). Preflight requires a passing, under-six-hour probe on both Macs; each tick refuses to claim on its own Mac while its probe fails. | `batch.py` `drive_probe`, `maybe_probe`, `launchd_probe_status`, `preflight`, `tick` |
| 5 | Quality dead end with nothing approved left ends `needs-dan` with finding, choices and link (editor instructions and runner). Evidence-format errors get exactly one repair session by the same editor in the same folder. A gate FAIL is never repaired away: documented against Dan's picks it becomes his question, otherwise it stays blocked. Every blocked row names an owner and a plain next action. Plus `hold`/`unhold` and a one-time `reclassify`. | `batch_runner.py`, `batch.py` `finish`, `handle` |
| 6 | One M6 notification per event (blocked, needs Dan, not starting), recorded in `~/.absbyai-batch/alerts.json`, never repeated, failed sends retried at most three times. Screen delivery cannot be confirmed from launchd, so the edit desk's M6 card shows the same lines. | `batch.py` `send_alerts`; `scripts/edit-dashboard/observe.py`, `app.js` |
| + | `editroute.py pick/wait` refuse job names starting with `-` and print help for `-h/--help`. | `editroute.py` `bad_job_name` |

## Proven with real runs on the Macs

- **Launchd probe, both Macs, 5:02 p.m.** Run by the `com.absbyai.edit-queue` agent itself. Internal work folder PASS; `Videos to Review`, Extreme and Expansion work folders FAIL with "Operation not permitted" on both Macs. This is the missing grant.
  - M6 program `/Library/Developer/CommandLineTools/usr/bin/python3`, running process `/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/Resources/Python.app/Contents/MacOS/Python`.
  - M2 program `/Applications/Xcode.app/Contents/Developer/usr/bin/python3`, running process `/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/Resources/Python.app/Contents/MacOS/Python`.
- **Preflight across both Macs with the shared checkout dirty** (another session's unsaved edit desk files and dozens of other uncommitted files): source check clean, scheduler hashes equal, canaries pass. The only problems are the two missing grants.
- **Live report and alert on the M6.** First line read `NOT STARTING: 2 queued edits ...` naming REALDEMOS-B05 R1 and WV-07 R1 with reasons. Notifications sent through `osascript` exit 0 and recorded; whether they appeared on screen cannot be confirmed from the background, hence the desk lines.
- **Ledger corrections on the M2** (backup `~/.absbyai-batch/repair-backups/20261118-claude-reclassify/`):
  - Protein Snack Can R2 (DS-106 R2): blocked → **needs Dan**. Audio row 83 ms vs 80; choices: hold for another audio pass (his current default), approve an exception, or a corpus-tested gentler dereverb. Review http://127.0.0.1:9814/ (opens).
  - Why I Sleep At 63 Degrees R2 (DS-50 R2): blocked → **needs Dan**. Complete film; gate fails 5 rows the editor documented against his picks (Fuller Bass tone row, portrait framing). The only other error was an empty cost list with $0 spend, so no repair session was spent. Review http://127.0.0.1:9815/ (opens).
  - Man Boobs SFL R2 (SL-36 R2): stays blocked, now with owner "Codex or Grokbot, then Claude" and a plain next action (grant, then a Claude chat redoes only the copy into Videos to Review).
  - 3 Ways To Lose Fat R2 (DS-51 R2): **held**. The only record that Dan paused it on Nov 17 is another session's note in the edit desk code; the hold says so and `batch.py unhold chat-DS-51-R2 DS-51-R2` releases it.
  - I Crashed My Tesla (RO-39 R1): left as Dan paused it.
- **Waiting line:** the `--help` entry (two failed routing attempts on Nov 18, no real job) removed under the editroute lock; backup `~/.absbyai-editroute/waiting.json.before-help-removal-20261118`. `editroute.py pick --bogus` now exits with a usage error.
- **WV-07:** its board line says QUEUED-ENABLED; the real state is registered, disabled, not startable. Its owner session ("GAT Upsell 4 AD R1") was told; its entry was not edited.

## Proven with fixtures only

- M2 tick claiming and launching the runner directly with every SSH call to the M6 failing; runner PID and birth recorded (`test_batch_repairs.TickLaunch`).
- Dirty desk, docs, tests, benches do not block; a changed scheduler file and a changed `preamble.md` do, by name (temporary git repo).
- Missing grant blocks preflight and the tick with the named folder; stale probe refused; probe leaves nothing behind.
- One repair session for format errors; a documented gate FAIL becomes a question; an undocumented one stays blocked; quality dead ends end `needs-dan` with choices.
- Alerts once per event, stable across wording changes, M2 never sends, failed sends retried at most three times; desk card shows the lines.

## Tests

From the main folder, each file in its own process: edit-queue 182 (`test_batch` 35, `test_batch_repairs` 21 new, `test_batch_runner` 41 incl. 6 new, `test_edit_queue` 60, `test_runner_end_to_end` 11, others 14) all OK; editroute 80 OK (3 new); editcap selftest 29/29; edit desk 20 OK plus the JS check. Not caused by this change: renderq `selftest.py` stops with "Operation not permitted" killing its own test process group in this session; two legacy `test_runner_end_to_end` cases fail only inside a scratch git worktree (core.symlinks is false), also on untouched main.

## Not done, and why

- **Full Disk Access grant:** Claude cannot change Mac privacy settings. Handed to Codex and Grokbot: [handoff-20261118-full-disk-access-grant-codex-grokbot.md](../Handoffs/handoff-20261118-full-disk-access-grant-codex-grokbot.md). Until both Macs pass, nothing starts (deliberate).
- **No real M2 job has run since the hop was removed.** That proof comes with the pilot, after the grant.
- **REALDEMOS-B05 R1 and WV-07 R1** stay registered and disabled; re-enable only after the grant passes and the owners and Dan want them.
- **Pilot (three videos):** waits for the grant, then Dan's three video names and his go.

## Independent review and fixes

Codex GPT-6.2 Sol High, read-only, started by Claude: [CODEX-REVIEW.md](overnight-batch-review-20261118/CODEX-REVIEW.md), verdict FIX FIRST, 11 findings. All 11 fixed in `90058c7`:

1. Preflight now needs each Mac's agent to answer the exact fresh request and pass every folder it needs at the same resolved path; empty, incomplete or moved records fail.
2. Each Mac's start gate travels with its tick observation; reports and receipts judge each round by its placement; a Mac silent for ten minutes counts as stuck; an unreachable ledger is named.
3. Drives count only when really mounted (a leftover folder at an unmounted `/Volumes` path never passes; an absent share does not block internal work); allocator roots are created.
4. One fixed probe folder whose leftovers are cleared next time; the probe runs in a child of the agent's own Python with a 60-second deadline.
5. The editor's submitted candidate is saved before any repair; an allowance pause or lost runner resumes the repair, never the whole edit.
6. A repair may change only the evidence fields: files, bytes and gate evidence are compared; it must exit 0; a $0 cost row needs a reason.
7. A gate FAIL becomes Dan's question only with a literal FAIL, gate evidence naming the delivered file, and a disposition for every failing row.
8. The report shows the exact finding and choices; a quality decision without both is refused; the third start failure gives a working takeover action.
9. Alerts are per-round episodes: clearing and recurring rings again, partial resolution does not; rows that ended before the rollout do not ring.
10. Only the events shown in a notification are recorded as sent; the desk's M6 card shows the alert lines with an "Open the full overnight report" link (`/batch-report`), verified live on the M6 desk.
11. New tests: a real fixture worker launched directly by an M2 tick with every SSH call failing, from start to delivered; a dirty checkout through the real start decision; the real delivery validator through the repair. Tests are fenced from the real Macs (a first draft read, never wrote, the real M2 ledger; it was confirmed unchanged).

Live recheck after `90058c7` (5:22 p.m.): both agents answered fresh requests and fail exactly the three drive folders; preflight fails only on those; the M6 report's first line and the desk card show the not-starting alert. The alert ledger migrated to episodes without ringing again.

Tests after the fixes, main folder: edit-queue 208 (`test_batch_repairs` 39, `test_batch_runner` 49), editroute 58, desk 20, editcap 29/29, all OK. `test_batch_runner`'s real-process interruption case (unchanged code, a half-second timer) failed twice in about ten runs while all six render cores were busy, and passed otherwise.

Codex verification of the fixes: [CODEX-VERIFY.md](overnight-batch-review-20261118/CODEX-VERIFY.md), verdict FIX FIRST: most items partly fixed, plus new defects. Closed in `8abd966`:

- **Repair can no longer deliver a different cut after a pause.** A repair counts only once accepted (exit 0, fresh marker, no protected change, per-file gate stamps included); an unaccepted repair is rechecked against the editor's submission on resume. Reproduced as a test (swap + allowance pause, then resume: blocked, no reviewer, editor ran once).
- **Gate questions come from each delivered file's own current FAIL stamp**, with a disposition for every failing row; a stale PASS stamp is refused.
- **Probe:** per-Mac folder, never a link, cleanup removes only its own two file names; a skipped or unmounted drive never counts; status reads only the saved record and never touches a drive; Extreme is required on both Macs, Expansion is reported but does not block; an answered request is not re-run.
- **Only an unreachable M2 ledger is global;** any other tick fault stops only that Mac's claims. Takeover actions name the exact round (`--round N`).
- **Receipts give real states** (delivered, running, later after an allowance wait, paused group). A fresh alert ledger rings the first incident; alert text leads with job, round and status.
- **The fixture worker never touches launchctl**, and proves the M6 connected at the start and dropping mid-job.
- Resumed repair time is charged only for the current claim.

Accepted limits, shown to Dan rather than proven: whether each gate disposition matches a real approval of his, and whether a "$0, no paid provider" reason is true. A change of cause during one stuck episode does not ring again. No third review was run: the pilot is the next real proof.

Final state, 5:37 p.m.: both Macs on `8abd966`. Live probe and preflight fail only on Videos to Review and the Extreme work folder on both Macs (the missing grant). Main-folder tests: edit-queue 220 (`test_batch_repairs` 49, `test_batch_runner` 51), editroute 58, desk 20, editcap 29/29, all OK. Also fixed: the edit desk's "scheduler version needs checking" warning (reviewed `editroute.py` digest added to the desk policy on both Macs, `7590c10`).
