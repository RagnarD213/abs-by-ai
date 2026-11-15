# Overnight batch: follow-up review of the repairs (Claude Fable 5.2, high effort)

Reviewed 2026-11-15 at commit `8ed194d` (diff `4cc7c97..8ed194d`) against `fable-review.md`. Reviewer only; nothing was changed.

## Verdict

**Safe to deploy disabled. One blocker remains before the real Night 1.** All four original blockers and findings 5 to 12 are resolved. The remaining blocker was introduced by the repair for finding 7 and is hit by the planned Night 1 link-cut test.

Tests at `8ed194d`: `tests/test_batch.py` 25 passed, `tests/test_batch_runner.py` 15 passed, including the real SIGTERM of a fake session process group.

## Remaining blocker

### B1. A finished M6 edit is thrown to "blocked" if the M2 link is down when the reviewer is due to start
- **Where:** `batch_runner.py` line 218: `executor_pause=b.rpc('snapshot')['control']...`, unguarded.
- **Exact trigger:** a worker on the M6 finishes its editor session and checkpoints the candidate while the M6 cannot reach the M2. `b.rpc` raises `TransportError`, which falls into the general `except Exception` at line 266.
- **Consequence:** the outcome is `blocked` with an ssh error as the reason. The reviewer never runs, and the gated candidate is parked. This contradicts the plan ("M6 cannot reach M2: its running jobs continue, outcomes sync when the link returns"). Night 1 cuts the M6 link for one hour after the M6's first start, and a size S edit can easily finish inside that hour. Same-round re-enqueue is now refused, so the only way forward is a chat takeover.
- **Repair:** wrap the read in `try/except Exception`. On failure use the cached `~/.absbyai-batch/snapshot.json` control if present, otherwise treat it as no backoff and run the reviewer. A reviewer limit is still caught by the existing non-zero-exit check at line 242. Add a worker test where `b.rpc` raises at this point and the reviewer still runs.

## Earlier blockers: all resolved

1. **Signalled worker leaves its editor running.** Resolved. `run_session` stops and verifies the session group on any exception, the interruption propagates, the worker reports `blocked` and never an allowance pause, and `pulse` retries. If the group cannot be confirmed gone, the claim and slot are retained.
2. **Successful editor misread as a usage limit.** Resolved. Classification runs only on a non-zero exit with no fresh marker (editor) and a non-zero exit (reviewer).
3. **Stale review file reported as Checked.** Resolved. The report path is unique per token and attempt, archived before each session, checked for a modification time after the session start, and bound to the candidate SHA-256 values.
4. **Start failures draining the queue.** Resolved as specified: `deferred-start` requeues with a host backoff and a bounded counter. See R1 for the residual.

## Findings 5 to 12: resolved

- **5.** The tick catches all errors and reports them. Outbox items are normalized, transport errors stay pending, and rejected items are quarantined after three tries with a visible error.
- **6.** `editroute.py wait` works while batch starts are disabled; chat batches inherit enablement when the digest matches.
- **7.** Executor-level backoff with doubling (tries at 0, 2 and 6 hours). See B1 and R2.
- **8.** A rejection without citation or candidate identity ends `delivered-unreviewed` with findings attached and no second reviewer.
- **9.** Terminal recovery releases the stale slot; claims waiting for the review mirror no longer consume a slot.
- **10.** Enqueue refuses waiting, promoted, active and parked entries; `acquire` itself now checks the batch guard. See R4.
- **11.** A repeated job and round is refused; the checkpoint's review attempts reset on a new registration.
- **12.** The review folder and port are validated before the reviewer, and candidate hashes and stamps are re-checked after it.

Low items also fixed: 14 (finalize cleanup is best effort), 15 (cleanup is time bound by `completed_at`), 18 (`prior_outcome` kept), 19 (ID validation), 21 (finished rows keep their group during a link error), 23 (`kick`), and part of 22 (recovery waits for the job's live render-queue steps). Unchanged by choice or still open, all low: 13, 16, 20.

## Residual, not blocking (worth doing before Night 1)

- **R1. Start-failure budget is short.** Three tries at 120 seconds means a job is terminal after about 6 minutes. A host-level condition that lasts longer (a dedicated-M6 reservation, or the M6 lacking storage for `need_gb`) while the M2 is full still blocks each `any` job in turn, roughly one per 6 minutes. Because same-round re-enqueue is refused, each then needs a takeover or a new round number. Repair: do not count capacity or storage waits toward the terminal counter, or exclude the failing Mac for that job and block only when both Macs have failed it.
- **R2. The reviewer backoff re-arms itself.** `handle` sets `executor_backoff[reviewer]` to now plus 2 hours even for `attempted=False`, so each job that arrives at review during a pause extends it. This delays, never loses. Repair: for `attempted=False`, keep the existing `until` and use it for the row's `not_before`.
- **R3.** In `run_session`, a signal landing between `Popen` and the inner `try` skips `stop_session`. The window is a few bytecodes. Repair: enter the `try` before `Popen` and stop the group whenever `proc` exists.
- **R4.** The enqueue live-check dropped the old `in_use` test. A job with live render-queue steps but no waiting or active register entry now passes. Repair: check both.
- **Coverage:** B1, the enqueue live-state refusal and chat-batch inheritance have no tests.
