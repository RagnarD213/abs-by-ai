# Overnight batch: make queued edits start, fix background file access, surface blockers

**Handoff, November 18, 2026 | Ops/infrastructure, not a video edit | Owner: Claude, by Dan's explicit request on Nov 18 (Codex built the system; this handoff transfers the repair) | Recommended: Claude Fable 5.2, high effort | Independent review of the diff afterwards: Codex GPT-6.2 Sol, High**

## Goal

Dan queues named edits, leaves, and finds them started and accounted for with no chat supervising. Today the batch system cannot start anything, and Night 1 (Nov 15-16) only worked because a chat ran the M2 ticks by hand. Fix the six defects below, prove them, then run the three-video pilot at the end. No ten-video night until that pilot passes.

Dan's authorization: do every step without asking him. Stop only for the pilot's start (he names the three videos and says go). The one step Claude cannot do is the system permission grant in fixes 3 and 4 (a Mac privacy setting): do all the code and tests first, then hand that step off as described in "Permission grant step" below, and carry on with everything that does not depend on it.

## Background to read first

- Fable's Nov 18 critique of the as-built system: this file summarizes it; the chat that wrote it is the "overnight batch Fable review" session.
- [Implementation record](../Docs/OVERNIGHT_BATCH_IMPLEMENTATION_20261115.md), [Night 1 result](../Docs/OVERNIGHT_BATCH_NIGHT1_20261116.md), [three earlier Fable reviews](../Docs/overnight-batch-review-20261115/), [operating notes](../scripts/edit-queue/README.md).
- Code: `scripts/edit-queue/batch.py`, `batch_runner.py`, `runner.py`; `.claude/skills/_shared/editroute/editroute.py`.

## State observed November 18, about 4:30 p.m. Central (recheck, it will have moved)

- `~/.absbyai-batch/snapshot.json` on the M6: `control.enabled` false. Starts were on from 1:41 to 1:56 p.m. today, then stopped. Every `chat-*` batch shows enabled false.
- Preflight failed at 2:36 p.m.: "m6 source differs from pushed main: scripts/edit-dashboard/desk_records.py, scripts/edit-dashboard/test_dashboard.py" and "scheduler hashes differ between Macs". Those two files have another session's uncommitted edits in the M6 checkout.
- Queued and unable to start: Fat Not Muscle SFC R2 (DS-51 R2), Real Exercise Demos Batch 5 (REALDEMOS-B05 R1), GAT Upsell 4 (WV-07 R1). WV-07 is not in `~/.absbyai-editroute/waiting.json` either, while the board calls it "QUEUED-ENABLED".
- Blocked rows in `~/.absbyai-batch/morning-report.md`: Protein Snack Can R2 (DS-106 R2, audio early decay 83 ms against 80), Why I Sleep At 63 Degrees R2 (DS-50 R2, delivery evidence missing a non-empty `paid_provider_costs` list and a FAIL gate), Man Boobs SFL R2 (SL-36 R2 on the M6, `[Errno 1] Operation not permitted` writing into `Videos to Review/`), I Crashed My Tesla (RO-39 R1, paused by Dan: leave it).
- `waiting.json` holds a junk entry whose job name is `--help`.

## Fixes

1. **Queued work with starts off must be loud.** When any row is queued and `control.enabled` is false, or preflight is failing, the morning report's first line says so in plain words with the count and the exact reason, and item 6's alert fires. `batch.py enqueue-chat` must print, as its last line, whether the job can actually start now and, if not, why. A chat that registers a wait must never be told "queued" when nothing will launch it.
2. **Narrow the source check.** `SOURCE_ROOTS` (`batch.py` line 27) covers `scripts/edit-dashboard` and every test and doc under the roots. Compare only files the scheduler and workers execute: drop `scripts/edit-dashboard`, `tests/`, `*.md`, fixtures and snapshots. Keep failing closed for real scheduler drift. Do not commit, stash or overwrite the other session's dashboard edits to get a pass.
3. **Remove the M2 to M6 to M2 launch.** `worker_command()` (commit `2cfc208`) makes every M2 edit depend on the M6 being awake and reachable for the whole job. Give the M2's launchd Python real access to the external drives (Full Disk Access for the exact interpreter the LaunchAgent runs, then reload the agent), verify with the same exact-folder probe used on Nov 17, and return M2 launches to direct. If the grant truly cannot hold, the fallback is an M2 self-login (`ssh localhost` with its own key), never a hop through the M6. Record the worker's real PID either way.
4. **Fix the same fault on the M6.** The M6 background worker could not write into the project's `Videos to Review/` folder (it resolves to the Expansion drive). Same class of grant; probe create, write, rename and delete in that folder and in an Extreme work folder from the launchd context on both Macs. Add this probe to preflight so a missing grant blocks starts with a named reason before the night begins.
5. **Blocked must not be a dead end.**
   - A failed mandatory quality check with nothing left to try (DS-106 R2's audio row) ends `needs-dan` with the exact finding, the choices and the review link, not `blocked`. Thresholds stay as they are. Dan's current default for DS-106 R2: hold for another audio pass.
   - A delivery-evidence format error (DS-50 R2's `paid_provider_costs`) gets one automatic repair attempt by the same editor in the same folder before it can end `blocked`. A real gate FAIL is still a FAIL.
   - Every `blocked` row carries an owner and a next action a non-coder can read.
6. **One alert that reaches Dan.** A local Mac notification on the M6 that opens the persistent report, sent once per event and recorded: a job blocks, a job needs Dan, or item 1's condition holds. No email, no customer-facing channel. If a notification cannot be verified as delivered from the background context, say so and show the condition at the top of the edit desk instead.

Also: reject job names beginning with `-` in `editroute.py wait` and remove the `--help` entry from the waiting line (confirm first that no real job is behind it). Tell the owner of the WV-07 board entry what its real state is; do not edit another session's entry. After the fixes, re-register or re-enable DS-51 R2, REALDEMOS-B05 R1 and WV-07 R1 only if their owners still want them queued and Dan's priorities allow (RO-39 and WV-06 are paused by Dan; REALDEMOS-B04 is paused by Dan).

## Permission grant step (for Codex and Grokbot, not Claude)

Claude prepares everything up to the grant: identify the exact interpreter path each LaunchAgent runs on each Mac (`launchctl print gui/$(id -u)/com.absbyai.edit-queue`), write the launchd-context probe script, and run it to capture the failing result. Then, per AGENTS.md "A step Claude can't do goes to Codex and Grokbot", give Dan two ready-to-paste starter prompts in chat, both stating his authorization plainly:

- **Codex (GPT-6.2 Sol, High):** on the M6 and on the M2 (`ssh m2`), grant Full Disk Access to the exact interpreter path named in this handoff's receipt, reload `com.absbyai.edit-queue`, run the probe script from the launchd context, and report pass or fail per Mac per folder.
- **Grokbot:** the same task, self-contained, with the interpreter paths, the probe command and the expected output written into the prompt.

Until the probe passes on the M2, keep the existing M6 hop in place so nothing regresses; switch M2 launches to direct in the same change that preflight starts requiring the probe.

## Tests to add and pass

- Start a named batch while the shared checkout has unrelated uncommitted edits (dashboard, docs, tests): starts proceed. With a real scheduler file changed: starts block and the report names the file.
- Queue a job with starts off: report headline, enqueue output and alert all say it will not start.
- M2 launch with the M6 unreachable: an M2 worker starts and finishes a fixture job. Drop the M6 mid-job: the M2 worker is unaffected.
- Launchd-context file probe on each Mac passes for the work drive and `Videos to Review/`; with the grant missing, preflight blocks with that reason.
- A mandatory check that fails with no repair left ends `needs-dan` with a question; an evidence-format error triggers exactly one repair attempt.
- Alert sent once per event, recorded, not repeated on later ticks.
- Existing suites still pass (ledger, worker, routing, editcap, dashboard). Run them in separate processes as the README says.

## Pilot (only after all of the above, on Dan's go)

Three videos, no chat supervising, submitting chat closed: two second-round films whose colour and voice picks are already made, one first-round video. Pass means both finished films open, checked and independently reviewed, on the M6; the first-round video ends with one clear question; nothing stops silently, nothing runs twice, nothing is reported done that is not. Record queue wait, edit time, review time and time ready. This is also the first real proof of the reviewer retry, the final delivery chain and a closed submitting chat.

## Constraints

- Live edits must not be interrupted: check `editcap.py status` and `renderq.py status` on both Macs first (GAT VSL WV-03, Upsell 1 WV-04 and Upsell 2 WV-05 were running on Nov 18).
- `scripts/edit-queue/PAUSE` stays: general backlog discovery remains off. Only named batches start.
- No new Abs By AI ad jobs in any batch. No approval, upload, publish or schedule by this task.
- Push scheduler changes from a clean checkout as before, pull on both Macs, rerun preflight on both.
- The board entry `OvernightBatch` belongs to Codex. Add your own short entry for this repair (under 80 words) that names this handoff as the transfer; do not rewrite Codex's entry.
- Check for a live Codex session on the overnight batch before touching `scripts/edit-queue` (git log, the board, `ps` on both Macs). If one is mid-change, tell Dan in one line and wait for it to finish.

## Done looks like

Preflight passes on both Macs with the shared checkout dirty; an M2 fixture job runs with the M6 offline; both Macs pass the launchd file probe; the report and an alert flag anything that cannot start; the two blocked R2 rows are reclassified correctly; tests pass; a short receipt in `Docs/` lists what changed, what was proven with real runs versus fixtures, and what the pilot still has to prove. Then start a Codex GPT-6.2 Sol High review of the diff with the Codex CLI in the background (AGENTS.md, "Claude calls Codex itself"), fix what it finds, and only then ask Dan for the pilot's three videos.
