# Overnight batch scheduling: independent review (Claude Fable 5.2, high effort)

Reviewed 2026-11-15 at commit `4cc7c97` against the approved merged plan. Reviewer only: no code, claims, launchd, running edits or production data were changed.

**Verdict: four blockers. Do not start Night 1 until findings 1 to 4 are fixed.** Findings 5 and 6 should go in the same pass. The ledger design itself (single flock, pull claims, token-fenced outcomes, idempotent outbox replay, no reassignment of an unreachable owner) held up.

Line numbers are from `4cc7c97` and may be off by a few lines; function names are given for each. Changes after `4cc7c97` were not re-read.

## Blockers

### 1. A signalled worker leaves its editor running, then forgets it
- **Where:** `runner.py` `run_session` lines 62-82 (the outer `except Exception` at 81); `batch_runner.py` lines 92-99 (`interrupted`, `session`) and 161.
- **Trigger:** any SIGTERM or SIGINT to the worker during a session. `batch.py` `reconcile` lines 369-377 sends one itself when `progress.json` and the heartbeat are both 10 minutes stale. That happens whenever the `pulse` thread dies (`batch_runner.py` 86-90), and it dies on any uncaught error: a 35 s `editcap heartbeat` timeout, a `ValueError` from `handle` on the M2, or a `JSONDecodeError` in `remote` (`batch.py` 71). A plain `kill` does the same.
- **Confirmed by experiment** (temp folder, fake executor): after SIGTERM, `run_session` returned code -1 with the session process still alive, and `classify_failure` returned `usage_limited` because the log tail contained "rate limit".
- **Consequence:** `session()` then writes `session={}`, so the orphan can never be found or stopped. The row becomes `blocked` (takeover is now allowed, giving two editors in one folder) or `paused-for-allowance` (a second editor starts in the same folder after 2 hours). The slot is released while the orphan keeps rendering and may repeat paid requests.
- **Repair:** in `run_session`, wrap `communicate` in `except BaseException`: `killpg` TERM, wait, KILL, wait, then re-raise. In `batch_runner.session`, clear the session record only after confirming the group is gone. Never classify an interrupted session as a usage limit. Make `pulse` catch `Exception` per iteration so one slow call cannot stop heartbeats.

### 2. A successful editor run can be thrown away as a "usage limit"
- **Where:** `batch_runner.py` line 161 (editor) and 208 (reviewer).
- **Trigger:** `classify_failure` runs on every editor exit, including exit 0 with a valid candidate marker. Any of the 12 patterns in the last 6,000 log characters matches ("rate limit", "try again at", "limit reached", "session limit"). `runner.py` line 89 warns about exactly this. Confirmed: exit 0 plus "rate limit" in the tail returns `usage_limited`.
- **Consequence:** the finished candidate is never checkpointed. The job is requeued for 2 hours, the whole edit runs again (paid steps included), and after three such passes it ends `blocked: allowance exhausted`.
- **Repair:** read the marker first. Call `classify_failure` only when the exit code is non-zero and there is no fresh marker with this token. Apply the same non-zero-exit condition at line 208.

### 3. A stale review file can report an unreviewed cut as Checked
- **Where:** `batch_runner.py` lines 195 and 206.
- **Trigger:** `BATCH-REVIEW-<n>.md` is never cleared before a reviewer session, and the work folder is reused across rounds and re-enqueues. If the new reviewer exits 0 without writing its report, `review_verdict` reads the old file.
- **Consequence:** an old `VERDICT: SHIP` becomes `delivered` for a candidate nobody reviewed. This defeats the "no verdict, one retry, then unreviewed" rule. The legacy runner archives its review files for this reason (`runner.py` 535-537).
- **Repair:** move any existing report aside before each session. Accept a verdict only from a file modified after that session started. Have the reviewer echo the candidate SHA-256 and check it.

### 4. Temporary start failures become permanent "blocked" and drain the queue
- **Where:** `batch_runner.py` lines 103-113 and 221-222.
- **Trigger:** anything that fails before the first session: `editcap acquire` returning wait (a dedicated-M6 reservation, `editcap.py` 473-476, or unreadable priority controls; a chat taking the slot between the tick's status read and the worker's acquire), `renderq workdir` "no eligible work storage; wait in place", a signed-out or missing executor.
- **Consequence:** the row is finished as `blocked`, which is terminal. The slot frees, the next tick claims the next job and it fails the same way: one job burned per tick. During an M6 reservation every `any` or `m6` job ends blocked within minutes. Nothing is lost from the report, but nothing runs either, and each job needs a manual takeover or re-enqueue.
- **Repair:** for failures before a session has started, return the row to `queued` with a `not_before` backoff and a bounded `start_failures` counter, and hold further claims on that Mac for the same period. Only exhausting the counter ends in `blocked`.

## High

### 5. Narrow error handling can wedge a Mac's tick silently, or strand a claimed row
- **Where:** `batch.py` `flush_outbox` 329-338, `tick` 480, `update` 344, `remote` 71, `finish` 112-119; `batch_runner.py` 167, 173, 222, 234.
- **Trigger and consequence:**
  - Only `OSError`, `RuntimeError` and `SubprocessError` are caught. A `ValueError` in `flush_outbox` (review folder no longer present, or `finish` rejecting the outcome on the M2) crashes every later tick at the same file. `dispatcher.tick` dies before the legacy logic too. The morning report simply stops updating with no error on it: a silent stop.
  - On the M6 the same rejection arrives as `RuntimeError` and is retried forever. Because `reconcile` skips any claim with an outbox file (line 365), the row stays `claimed` permanently.
  - An outcome that fails `finish` validation (empty `reason`, `next_action` or `question`; `str(exc)` is empty for some exceptions at line 222) raises inside the worker's `finally` on the M2. No outcome is recorded, recovery fires, and the editor runs a second time.
- **Repair:** catch `Exception` per outbox item and per tick stage and put the error in the report. Quarantine an outbox item after N failures and surface it as Blocked. Validate the outcome locally with the `finish` rules before sending, falling back to `blocked` with `reason=str(exc) or type(exc).__name__`.

### 6. Chat waits have no working path from the moment of install
- **Where:** `editroute.py` `main` lines 1240-1242; `batch.py` 541-546 (`enqueue-chat`) and the `start` op.
- **Trigger:** `editroute.py wait` now always exits 3, although the queue is "installed disabled". Its replacement registers a batch named `chat-JOB-Rn` that is disabled, and only a per-batch `batch.py start` with full preflight enables it. `cmd_pick` still prints "run editroute.py wait".
- **Consequence:** a chat edit told to wait is parked "registered, disabled" indefinitely, and its own `editcap acquire` is then refused as batch-owned. This is the DS-109 failure in a new form, and it affects live chat work today.
- **Repair:** keep `editroute.py wait` working while `control.enabled` is false. Once enabled, let `chat-*` batches inherit enablement when the preflight digest is current. Update the `cmd_pick` message.

## Medium

7. **Allowance backoff is per job, not per executor** (`batch.py` 235-242). Every queued job using the same model starts, hits the same limit and burns one of its three tries. Tries at 0, 2 and 4 hours can all land inside one 5-hour limit window, so the whole batch for that model ends blocked. **Repair:** record an executor-level `not_before` in `control.json`; `claim` skips rows whose next session (editor, or reviewer when resuming at review) uses that executor.

8. **A rejection without the required citation is treated as "no verdict"** (`batch_runner.py` 27-28, 206-216). A fresh second reviewer then runs and can ship it as Checked, or two rejections are reported as "no valid verdict". The retry is meant only for a timeout or a missing verdict. **Repair:** when the first line is `VERDICT: DOES NOT SHIP` but the citation check fails, do not retry; finish `delivered-unreviewed` with reason "reviewer rejected without rule and timestamp; findings attached".

9. **Slot accounting leaks** (`batch.py` 185-188, 244-251, 391). When recovery ends in `blocked`, the dead worker's editcap entry stays active for up to 3 hours. A finished job whose outcome is waiting in the outbox for the review mirror still counts as an occupied slot, so the M2 stops claiming after three finishes while the M6 is unreachable (the planned one-hour link cut). **Repair:** `reconcile` runs `editcap release` when `recover` returns a terminal row; exclude claims in phase "outcome waiting for review mirror" from the `unregistered` count.

10. **Enqueue checks only jobs holding a slot** (`batch.py` 501-502). A job that is `waiting` with an armed `editcap.py wait` passes, and `editcap.py` `wait()` (574-582) calls `acquire` without the batch guard, so the chat and the batch worker can both start. **Repair:** refuse enqueue for any editcap entry in waiting, promoted or active; re-check registrations inside `wait()` before its final acquire.

11. **Re-enqueueing the same job, round and brief reuses the old checkpoint** (`batch_runner.py` 118-120, 156, 193). With `review_attempts` already 2 it reports `delivered-unreviewed` instantly with no session, and a cut the reviewer rejected is relabelled Unreviewed. **Repair:** on the first attempt of a new registration, reset `review_attempts`, archive old reports and re-verify the candidate hashes and stamps.

12. **`review_root` and `review_port` are validated only after the review** (`batch_runner.py` 180-183 versus 218-222). A missing value turns a gated, reviewer-shipped candidate into `blocked` and drops the verdict. **Repair:** check both right after the editor exits, before spending the reviewer session.

## Low

13. **Preflight hashes include tests and docs.** Observed live at 10:02: "New starts blocked: installed source differs from pushed main: batch.py, tests/test_batch.py". Any push under the five roots halts new starts on both Macs until a pull and a fresh preflight. It fails closed and shows in the report. Repair: exclude `tests/` and `.md`, or state it in the runbook.
14. **`queue.py set JOB finalized|uploaded` now exits non-zero** when the other Mac is unreachable (`sync_review_handoff` 203-224), after the state is already saved. Make the `forget` best effort.
15. **Stale owner-review cleanup.** `editcap.py` `settle` 398-400 deletes a with-Dan entry for any finalized or uploaded job, including a review newer than the finalization; compare against the entry's `since`. SL-13, SL-12, RO-15, DS-38, DS-36 and DS-34 are gone from both registers. Still listed on the M2: EXDEMO-CODEX3 (115 h), EXDEMO-FLOW2 (213 h), SRM-JV-R2 (40 h); the plan says to check these with their owners.
16. **`cmd_pick` (line 711) now routes with one Mac down**, but every chat `editcap acquire` still returns 6 from `resume.check`, so chat starts stay blocked while a route and storage commitment are recorded. Not unsafe; the plan item is only half fixed for chats.
17. **Candidate files are not re-hashed after the reviewer session** (`batch_runner.py` 187-188 run only before it).
18. **`takeover` overwrites a terminal outcome** (`batch.py` 219); keep it as `prior_outcome`.
19. **Job IDs with a suffix** (for example `DS-40-CODEX`) are shortened by `editcap.job_code`, so the worker's registry check fails. Validate at enqueue.
20. **The LOST check** (`batch.py` 419-429) flags jobs that released within 24 hours, and is moot now that `wait` is disabled.
21. **On a link error the report marks every row Unknown**, including already terminal ones (`batch.py` 403).
22. **Orphan stop kills only the recorded process group** (`batch.py` 386). Child processes in other groups could survive into the resumed run. Lower confidence; not verified.
23. **`kick` does not catch a local `launchctl` timeout** (`batch.py` 304).

## Resolved by changes after I began

- **Stopping, then starting a different batch, re-enabled the stopped one.** Fixed in `4cc7c97`; verified in the diff and its new test.
- **Claims continuing after a failed preflight.** Fixed in `13185cf`; verified.
- **Checked rows showing "queued" and the disclosed-uncertainty verdict not appearing in the report.** I had this as a finding. Reported fixed; I did not re-read it.
- **Idle metrics while disabled.** Not one of my findings; not re-read.

## Checked and sound

- One claim per job under competing processes; claim tokens fence stale writers; outcome replay is idempotent.
- Takeover is refused on any claimed row, including an unreachable owner.
- An unreachable owner is never reassigned; a disconnected M6 worker is protected by its local `progress.json`.
- A `kill -9` worker: the recorded orphan session is stopped and confirmed gone before the single resume, in the original folder, reusing its slot.
- Exit 0 without a fresh token-matched outcome is a failure.
- Gate evidence is bound to the exact file (stamp, gate version, SHA-256, PASS).
- A valid DOES NOT SHIP parks the cut and findings with no fix loop.
- Canary hashes match the installed launcher and executor config on the M6 (4 of 4 rows passed).
- The legacy queue stays behind its PAUSE file.

**Test coverage note:** `tests/test_batch.py` passes (16 tests) but covers only the ledger and `review_verdict`. Nothing exercises `batch_runner.main`, which is where findings 1 to 4, 8, 11 and 12 live.
