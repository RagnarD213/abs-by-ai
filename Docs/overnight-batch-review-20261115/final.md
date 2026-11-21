# Overnight batch: final verification and sign-off (Claude Fable 5.2, high effort)

Reviewed 2026-11-15 at commit `0865d8b` (diff `8ed194d..0865d8b` for `batch_runner.py`, `batch.py`, `runner.py` and their tests). Reviewer only; nothing was changed. The working tree was clean.

## Verdict

**Signed off. No remaining blocker.** B1 and R1 to R4 from `fable-followup.md` are fixed, and every blocker from `fable-review.md` stays resolved.

**Actual Night 1 has not run, and the deployment remains disabled.** This sign-off rests on reading the code and on unit tests with fake sessions. Real editor and reviewer sessions, the real one-hour M6 link cut and the real `kill -9` are unproven until Night 1 runs on Dan's go.

Tests at `0865d8b`: `tests/test_batch.py` 29 passed, `tests/test_batch_runner.py` 17 passed.

## What I verified

- **B1, offline review.** The backoff read in `batch_runner.py` is wrapped; on any error it falls back to the cached `snapshot.json` control, or no backoff. The new worker test cuts the M2 link after editing: the reviewer still runs, the slot is released, the `delivered` outcome is held locally, and it lands on the ledger when the link returns.
- **R1, start waits.** Capacity and storage waits are counted separately (`start_waits`) and always requeue. Only executor and infrastructure failures count toward the three-try limit. A five-wait test leaves the job queued with zero failures.
- **R2, reviewer backoff.** A pause with `attempted=False` keeps the existing executor `until` and does not rewrite it; tested.
- **R3, signal window.** `Popen` is inside the protected block and cleanup runs whenever a process exists. What remains is the few-instruction gap inside the assignment itself, which cannot be closed in Python and is negligible.
- **R4, enqueue live-check.** `job_live` refuses a job that is in `in_use` or registered as waiting, promoted, active or parked; tested for each state.
- **Also proven by the new tests:** chat batches inherit enablement only under a current, enabled preflight, and the heartbeat thread survives repeated timeouts.

## Notes, not blocking

1. **A storage wait can hold up the jobs behind it on one Mac.**
   - Trigger: the first job in start order needs more space than this Mac can give, and the other Mac is full or the job is pinned here.
   - Effect: this Mac re-claims that job every 120 seconds and never reaches smaller jobs that would fit. Nothing is lost or duplicated.
   - The morning report shows the job only as "queued", without the reason.
   - Suggested: on a storage wait, skip that job on that Mac for the backoff period rather than pausing the whole Mac, and show `last_start_error` in the report row.
2. **"editcap did not record an active slot" is classed as a capacity wait** (the default kind), so a broken slot register retries without limit. It should be `infrastructure`, so it ends `blocked` after three tries.
3. **Preflight must be rerun on both Macs** after pulling `0865d8b`. The scheduler source changed, so new starts stay blocked until it passes again. The canary is still valid: the launcher and executor configuration it is bound to were not changed in this diff.

## Addendum: final reviewed commit `4635ce4`

Verified by reading the diff `0865d8b..4635ce4` only (one commit, working tree clean). I did not rerun the tests; the owner reports 30 ledger and 18 worker tests passing.

**No blockers remain at `4635ce4`.** Notes 1 and 2 above are fixed:

- **Storage waits step aside.** A storage wait now sets a ten-minute defer for that job on that Mac only (`host_defer`), with no Mac-wide hold. `claim` skips the deferred job on that Mac, so smaller jobs start there and the other Mac can take the larger one. The new ledger test shows exactly that sequence.
- **The reason is visible.** Queued rows in the morning report now show `last_start_error`.
- **Broken slot register is bounded.** "editcap did not record an active slot" is now an `infrastructure` failure, so it counts toward the three-try limit and ends `blocked`. The new worker test shows one failure counted and the job requeued.

One cosmetic point, not blocking: a queued row keeps showing an old start error after a later allowance pause, in place of the pause time.

Note 3 still applies: rerun preflight on both Macs after pulling `4635ce4`.

**Deployment stays disabled, and actual Night 1 has not run.** The sign-off covers the code and unit tests; real sessions, the real link cut and the real `kill -9` remain unproven until Night 1 runs on Dan's go.

## Addendum 2: ordering correction, final reviewed commit `edd9b86`

Verified by reading `git show edd9b86` only (one commit on top of `4635ce4`, working tree clean). I did not rerun the tests; the owner reports 31 ledger tests passing.

**Sound. No blockers remain at `edd9b86`.**

- The change in `batch.py` `reconcile` is a pure reorder: the same four lines of the render-queue check moved below the orphan-session stop. No logic was added or removed.
- A recorded live orphan session is now signalled first, without waiting on the render queue. Before, a live render step could leave a known unsupervised editor running.
- Recovery is still held until the job has no live render-queue step, and a failed status read still means no recovery.
- The new ledger test covers the three transitions in order: the orphan is signalled with no render-status query; with the session gone and a render still live the claim is kept; once it drains the job gets exactly one resume.

Preflight must be rerun on both Macs after pulling `edd9b86`. **The batch remains disabled, and real Night 1 remains unrun.**
