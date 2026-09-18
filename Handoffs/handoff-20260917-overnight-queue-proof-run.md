# Overnight edit queue — Phase 0 proof run (AV-01 on Claude), then un-pause

**EXECUTED 2026-09-18 (Claude, Fable 5.1).** Try 1 (09-17 20:14, fired from outside this task) hit the account usage
limit after 9 min; runner misfiled it (`session_failed`), config had drifted to Fable/Sol-medium — both fixed. Try 2
(09-18 03:13–04:15, Opus/high) ran clean unattended and parked honestly on the master's own faults; review leg proven
by hand (Codex, `DOES NOT SHIP`, same faults). Queue resumed. Findings: `scripts/edit-queue/README.md`. AV-01 waits
for Dan's call on the review page (accept the approved master's faults, or fix the master first).

**Written 2026-09-17 (Claude, Fable 5.1). Dan's instruction: "go ahead and run the proof run" — as its own task.**
Parent design: `Handoffs/handoff-20260917-overnight-edit-queue.md`. Queue operations: `scripts/edit-queue/README.md`.

## 1. Goal

Prove that the queue can take one real job from `ready` to `delivered` **with nobody at the keyboard**, through the
exact launch path the 15-minute dispatcher uses. Then un-pause the queue. The job is **AV-01** (Muhammad's Ad 1 → 9:16
≤0:59), Claude-routed. If it passes, Dan gets a real vertical to review; nothing about it is throwaway.

The Codex half already ran once (DS-01, 2026-09-17: its sandbox blocked `ps`, fixed to `danger-full-access`). The
Claude half has never run a full job. This session finds out.

## 2. State on 2026-09-17 18:05

* **Headless Claude is signed in** (Dan did `/login` at ~18:00; `claude auth status` → `loggedIn: true`, `claude.ai`
  method = Max subscription). A one-line `-p` prompt on `--model opus --effort high` answered.
* **Queue is PAUSED** (`scripts/edit-queue/PAUSE`). `launch-one` ignores the pause and the nightly cap on purpose.
* **Models (Dan, 2026-09-17):** edits run Claude **Opus / high**, Codex **Sol / high**; reviews keep their own
  `review_model`/`review_effort` (Fable / high, Sol / medium). Set in `scripts/edit-queue/config.json` — **uncommitted**,
  on top of the Codex "video editing efficiency" session's uncommitted work in the same folder. Tests: 48/48.
* **Cross-review question is OPEN.** Dan doubts the other AI needs to review each edit. Claude's recommendation: keep one
  review per video, same-AI fresh session (`reviewer_for: {"codex": "codex", "claude": "claude"}`). Dan has not answered.
  Leave `reviewer_for` as it is unless he has; the runner already falls back to same-AI when the other is signed out.
* **⚠ AV-01 is currently NOT eligible**, and the reason is a self-inflicted trap: `dispatcher.py status` says
  `skip AV-01: named in AI_COORDINATION.md ACTIVE (another session owns it)`. The only board line naming AV-01 is the
  queue's own entry ("Next: … `launch-one AV-01`"). The eligibility check (`dispatcher.py` ~line 168) reads job IDs
  out of the ACTIVE section. Fix: reword that board entry so it doesn't contain the literal ID (this handoff already
  did, if the board check passed), and consider making the check ignore the queue's own entry.
* **⚠ No free slot right now:** 3 foreign ffmpeg builds (VQC Phase 4 kit render, Grok AV-05, Codex R4 work) and Dan at
  the machine → `free: 0`. `launch-one` refuses without a free slot; it does not queue. Wait for one.
* Fallback proof jobs if AV-01 stays blocked for a non-trap reason: `SL-01`, `SL-02` (Claude, eligible now).

## 3. Steps

1. Read `AGENTS.md`, `scripts/edit-queue/README.md`, and `dispatcher.py --help`. Do not add a board entry naming the
   job ID (see the trap above). Add one ACTIVE line for this task without "AV-01" in it.
2. `cd` to the repo. Confirm the settings before launching:
   * `python3 -c "import json;c=json.load(open('scripts/edit-queue/config.json'))['executors'];print(c['claude']['model'],c['claude']['effort'],c['codex']['model'],c['codex']['effort'])"`
     → `opus high gpt-5.6-sol high`. If not, restore them (Dan's 2026-09-17 decision) before anything else.
   * `"$(ls -d ~/Library/Application\ Support/Claude/claude-code/*/claude.app/Contents/MacOS/claude | tail -1)" auth status`
     → `loggedIn: true`.
   * `python3 -m unittest discover -s scripts/edit-queue/tests` → OK.
3. `python3 scripts/edit-queue/dispatcher.py status`. Need: AV-01 not in the skip list and `free ≥ 1`. If AV-01 is
   skipped for the board-name reason, fix the board line (own entry only, re-read from disk first, `scripts/board-check.sh`).
   If `free: 0`, wait; re-check every 15 min (a Monitor or a loop). Do not kill anyone's build to make room.
4. Launch: `python3 scripts/edit-queue/dispatcher.py launch-one AV-01`. It prints the run id and detaches the runner
   under `caffeinate` (`start_new_session=True`), so this session can keep going. Max job time: 10 h (`max_job_hours`).
5. Watch, don't help. Log: `/Volumes/Extreme/_edit_work/AV-01/queue-run.log`. Check it every ~20 min. What "pass" and
   "fail" look like:
   * The session must **never wait on a prompt**. A log that goes quiet with a question in its last lines is a FAIL
     (permission gap): note the exact tool/command that asked, and stop the run.
   * Editor done → `DELIVERY.json` in the work dir → reviewer runs → `QUEUE-REVIEW-1.md` (first line `VERDICT: SHIP`
     or `VERDICT: DOES NOT SHIP`) → job state `delivered` (`python3 scripts/edit-queue/queue.py show AV-01`) →
     scoreboard row (`scripts/edit-queue/scoreboard.json`) with model usage → review page
     (http://127.0.0.1:8830, `review_page.py`) shows the item.
   * `BLOCKED.md` in the work dir = the editor parked itself with a reason: read it; that's a finding, not a fail of
     the queue itself.
   * No `DELIVERY.json` and no `BLOCKED.md` at exit = `stalled`/`session_failed`: read the tail of the log; this is
     the Phase 0 finding to fix.
   **Never intervene inside the work dir while the run is live** (AGENTS: no scripts in another session's build dir).
6. Verify the delivered file yourself, the way any delivery is verified: `.deliver_gate.json` + `.audio_gate.json`
   stamps present at current `GATE_VERSION`, `--verbatim` audio (Muhammad's mix cut at the seams only), review copy in
   `Muhammad Ad Videos/<Ad 1 folder>/`, real-picture labels off face and abs. Watch the review copy.
7. Report to Dan in plain language: pass/fail, where the review copy is, the reviewer's verdict, how long it took,
   the model-usage row, and every place the unattended run needed something (that list is the deliverable).
8. **On PASS:** `python3 scripts/edit-queue/dispatcher.py resume` (deletes `PAUSE`); confirm the launchd job is loaded
   (`launchctl list | grep edit-queue`); run `dispatcher.py tick --dry-run` and paste what it would launch next. Tell Dan
   the queue is live, what it will pick first, and how to pause (`dispatcher.py pause`).
   **On FAIL:** leave the queue paused, write the finding into `scripts/edit-queue/README.md` (Phase 0 table) and
   `Handoffs/handoff-20260917-overnight-edit-queue.md` §3, fix it if it's a config/flag matter, re-run.
9. Commit: `scripts/edit-queue/` config/tests/README changes (check the board first — if the Codex efficiency session
   still owns uncommitted work in that folder, commit only your own hunks or coordinate; never sweep its work in),
   the board line, this doc's status. Push. No dashboard row. Delete this doc's OPEN row in `Handoffs/README.md` and its
   board line when done.

## 4. Do not

* Do not upload, publish or touch Blotato/YouTube/Google Ads (the launch already disallows those tools).
* Do not lower the models or effort to save allowance. Do not raise a gate threshold to make the file pass.
* Do not start a third build. Do not run anything inside `/Volumes/Extreme/_edit_work/AV-01/` while the runner is live.

## Starter prompt (Claude, Fable 5.1, effort high)

> Read `AGENTS.md`, then `Handoffs/handoff-20260917-overnight-queue-proof-run.md` in full, then
> `scripts/edit-queue/README.md`. Run the Phase 0 proof: launch AV-01 through `dispatcher.py launch-one` once a build
> slot is free (check `status`; fix the board-name trap if AV-01 is skipped for it; never kill another build), watch
> `queue-run.log` without intervening, verify the delivered file and the reviewer's verdict, and report to me in plain
> language what passed and every place the unattended run needed something. On a pass, `dispatcher.py resume` and
> tell me what the queue will launch next and how I pause it. On a fail, leave it paused, record the finding, fix it if
> it's a settings matter, and re-run. Commit only this task's changes; never upload or publish anything.

Alternative executor: Codex GPT-6 Astra / high with the same prompt (it's ops work), but this run exercises the Claude
launch path, so a Claude session reading its own log is the better fit.
