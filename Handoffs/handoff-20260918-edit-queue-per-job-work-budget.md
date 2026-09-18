# Handoff — Overnight edit queue: a work budget on every job (2026-09-18)

**Source:** Edit Pipeline Watchlist, entry 07 (https://claude.ai/artifact/NEfYBTQPo2raMmfZnaoE9v — Lydia Linzi's Codex
workflow; watch from 7:00, "where the agent overbuilds and burns through credits"). Dan asked for this handoff on
2026-09-18. **Queue plumbing only — no video is edited, and no gate, threshold, master or routing row changes.**

## Goal, in plain language

The overnight queue starts up to three edits a night with nobody watching, and it shares the same usage allowance Dan
uses during the day. Today the only limit on a single job is a flat **10-hour** kill switch. Nothing stops one job from
wandering — rebuilding tools it didn't need, re-rendering the full video six times, polishing past the brief — and
eating the whole night's allowance. Add a **budget per job**: the session is told its budget up front, warned as it
runs down, and stopped cleanly with its work kept when it runs out.

## What exists today (read before changing anything)

`scripts/edit-queue/README.md` first. Then:
* `config.json` → `claims.max_job_hours: 10` (flat, every size), `unattended.nightly_launch_cap: 3`,
  `review.reviews_per_candidate: 1` (no fix/re-review loop — keep it that way), `stop.usage_backoff_hours: 2`.
* `runner.py` → `run_session(..., timeout_h)` (line ~37) kills at the timeout and returns `"timeout"`; the edit call
  (line ~299) passes `max_job_hours`. A timeout currently lands the job in `stalled`.
* `pre_render_check.py` — every full render already has to pass through it. **This is the natural place to count renders.**
* `preamble.md` — the fixed text in front of every unattended edit; `WORK_PACKET.json` is written by the runner.
* `scoreboard.json` — one row per run with hours and model usage where the tool reports it. Only 4 rows exist
  (DS-01 ×2 parked, AV-01 session_failed + parked), so **there is no history to calibrate from yet — start with the
  numbers below and make them config, not code.**

## Design (decided — build this)

1. **Budget by job size, in `config.json`** (new `budget` block; every number editable by Dan without touching code):

   | size | edit wall-clock | full renders | review wall-clock |
   |---|---|---|---|
   | S | 2.5 h | 2 | 0.75 h |
   | M | 5 h | 3 | 1 h |
   | L | 8 h | 3 | 1.5 h |

   `claims.max_job_hours` stays as the absolute outer ceiling. A job doc may carry `"budget": {...}` in `jobs.json` to
   override its size row (so Dan can grant one hard job more room on purpose).
2. **Tell the session.** The runner writes `BUDGET.json` into the work dir at launch: `started`, `deadline`,
   `soft_deadline` (70 %), `max_full_renders`, `renders_used`. Add a short section to `preamble.md`:
   * build only what `WORK_PACKET.json` lists; no new tools, no refactors, no "while I'm here" fixes — write those to
     `FOLLOWUPS.md` instead;
   * check `BUDGET.json` before each full render and at each stage boundary;
   * past the soft deadline: stop exploring, finish the current candidate, write `DELIVERY.json` — or `BLOCKED.md` with
     what is left. A parked honest partial beats a killed session.
3. **Count full renders where they already pass.** `pre_render_check.py` increments `renders_used` in `BUDGET.json`
   each time it clears a full render, and **refuses** (non-zero exit, clear message) once the cap is reached. Short
   moving previews (the 0.5–15 s checks) do not count.
4. **Enforce the clock in the runner.** `run_session` uses the size budget instead of the flat 10 h for the edit, and
   the review budget for the review. On expiry: terminate the process group, then
   * outcome `budget_exceeded` (new; distinct from `timeout` and `session_failed`);
   * job → `needs` with reason "budget exceeded after X h, N renders — see queue-run.log" (**not** `stalled`, and
     **never auto-restarted**); claim released; work dir kept intact;
   * scoreboard row carries `budget: {hours_allowed, hours_used, renders_allowed, renders_used, exceeded: true}`.
   Every row gets the `budget` block (exceeded or not), so the numbers can be tuned from real data later.
5. **Show it.** `dispatcher.py status` prints each running job's budget used (e.g. `AV-05  1.4/2.5 h · 1/2 renders`);
   the review page shows a small "stopped at budget" label on a parked job, with the reason.
6. **Token/credit cap: record, don't enforce (yet).** Neither CLI exposes remaining allowance before or during a run
   (README, Phase 0 findings); Codex prints a total only in its footer. Keep recording usage per session as today. If
   the executor finds Codex's `exec --json` stream reports running token counts reliably, add an **optional**
   `budget.max_tokens` that is `null` by default — and say so in the report. Do not guess usage from account totals.
7. **Hand-fired jobs** (`dispatcher.py launch-one`) get the same budget by default; `--no-budget` lifts it and is logged.

## Tests (spend nothing — extend the existing fake-editor suite)

`scripts/edit-queue/tests/test_edit_queue.py` and `test_runner_end_to_end.py`:
* a fake editor that sleeps past a tiny budget → `budget_exceeded`, job `needs`, claim released, work dir kept, scoreboard row correct;
* a fake editor that finishes inside budget → unchanged behaviour, row carries `exceeded: false`;
* `pre_render_check.py` refuses render N+1 and leaves `BUDGET.json` consistent; previews don't count;
* per-job override in `jobs.json` beats the size row; `--no-budget` works and is logged;
* a usage-limit message still routes to `usage_limited` → `ready` with the 2-hour back-off (no regression on the 09-18 fix).

## Proof required before calling it done

* All queue tests pass. `python3 scripts/edit-queue/dispatcher.py tick --dry-run` and `status` run clean.
* One printed `BUDGET.json` and one scoreboard row from the fake-editor run, in the chat report.
* **Routing untouched:** diff of `config.json` shows only the new `budget` block. Every group still resolves to Codex
  until 2026-09-24 11:00 CT; Opus/high + Sol/high model rows unchanged (commit `3403c6b` overwrote these once by
  accident — check the diff).
* README updated: a plain-language paragraph for Dan ("each job now has a time and render budget; a job that runs out
  is parked with its work kept, never restarted on its own; change the numbers in `config.json` → `budget`") and the
  new outcome in the state notes.

## Out of scope / guardrails

Phase 2 (placeholder flow) is a separate handoff — don't start it. No change to `nightly_launch_cap`, slots, the
review count, reviewer routing, gates or any video file. Don't launch a real edit to test this; the fake editor is the
test. If a queue job is running when you start, don't restart the launchd jobs under it — wait for the claim to clear
or make only changes the next tick picks up. Commit and push the queue files only; nothing deploys to absbyai.com.
Re-read `AI_COORDINATION.md` from disk before finishing; when done, delete this handoff's line there and its row in
`Handoffs/README.md`, and report in chat. After ~10 real scoreboard rows exist, a follow-up can tighten the table from
data (suggest it in the report; don't schedule it).

## Recommended executor

* **Codex GPT-5.6 Sol / Medium** (recommended — small, well-specified change to ~4 files with an existing test
  harness; Codex owns ops tooling and already wrote recent queue changes).
* If Codex usage is tight: Claude **Sonnet 5 / Medium** after the 2026-09-24 reset. Neither Fable nor Opus is warranted.

## Starter prompt

> Read `Handoffs/handoff-20260918-edit-queue-per-job-work-budget.md` and `scripts/edit-queue/README.md`, then execute
> the handoff end to end: add the per-size `budget` block to `config.json`, write `BUDGET.json` at launch, add the
> scope-fence and soft-deadline section to `preamble.md`, count and cap full renders in `pre_render_check.py`, enforce
> the clock in `runner.py` with the new `budget_exceeded` outcome (job → `needs`, work kept, never auto-restarted),
> surface it in `dispatcher.py status` and the review page, and extend the fake-editor tests. Do not launch a real
> edit, do not change routing, models, caps, gates or any video file. Prove it with the test suite and a dry-run tick,
> update the README in plain language, commit and push only the queue files.
