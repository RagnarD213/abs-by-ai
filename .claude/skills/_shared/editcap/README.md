# Active edit cap (`editcap`)

At most **5 video edits doing production work at once**, Claude and Codex together (Dan, 2026-10-21). The render
queue (`../renderq/`) caps heavy STEPS; this caps how many EDITS feed it. Rule: `VIDEO-RULES.md`, "Active edit cap".

Why: on 2026-10-21 about 12 edits ran at once on the 10-core Mac, the render queue was overbooked (16-18 cores of work
on 8, ~7.8 GB swap), heavy waiters sat 3-5 hours and no video finished all day.

## For editing sessions (Claude and Codex)

`E=.claude/skills/_shared/editcap/editcap.py`

1. **Before the first production step** (render-queue job, AI generation, build) and on every resume:
   `python3 $E acquire RO-27 --title "Boring Abs At 40" --type LFC`
   - exit 0: go. Calling it again later is a harmless heartbeat; do so at each new production stage.
   - exit 3: **waiting.** Do not render, generate, build or spend. Read-only prep (reading the handoff, planning) is
     fine. Arm the auto-start, tell Dan your place in line in one line, and end the turn:
     - **Claude:** run `python3 $E wait RO-27` with `run_in_background`. It exits when the slot is yours and the
       session is re-invoked automatically; then continue the edit.
     - **Codex:** create a heartbeat automation on this thread (like those in `~/.codex/automations/`), every 10
       minutes, prompt: "Run `python3 .claude/skills/_shared/editcap/editcap.py acquire RO-27`. Exit 3: end the turn
       silently. Exit 0: pause this heartbeat, then continue the edit from its handoff." A Codex shell cannot hold a
       background waiter across turns, so the heartbeat is its auto-start.
2. **Review page up, awaiting picks, stopping for Dan:** `python3 $E release RO-27 --review`. The slot goes to the
   next edit. When Dan's notes arrive, `acquire` again: you go now if a slot is free, otherwise you wait in
   release-date order (front of the line only if your release is soonest).
3. **Edit finished** (final delivered and approved, or handed to setup): `python3 $E release RO-27`.
4. If `release` prints `WAKE claude local_...` lines, a promoted Claude waiter has no auto-start process running:
   send it that message with `mcp__ccd_session_mgmt__send_message` (or `SendMessage`). `WAKE codex <id>` lines are for
   a Codex session (`send_message_to_thread`); a Claude session cannot reach Codex threads, the Codex heartbeat
   covers it. `python3 $E wakes --claim --ai claude` lists and claims them.

Exempt (never call it): setup/upload tasks, thumbnail and cover picks, script and doc work, status checks.

**Job names:** use the video's code (`RO-27`, `SL-18`, `DS-44`, `RA-09`), the same one the render queue shows in
`[brackets]`. Render-queue groups like `work:ro27` or `DS-40-codex` map to `RO-27` / `DS-40` automatically.

Footage preparation batches use `SHOOT-YYYYMMDD` in both queues. They count as one active production job;
their render activity renews the lease even when no SFC/LFC/AD type applies.

## See it

`python3 $E status` (read-only, no permission needed): the 5 slots and who holds them, the waiting list in start order
with each release date and where it came from, and edits that are with Dan or stalled. `renderq.py status` prints a
one-line summary at the bottom.

## How it works

- Registry: `/tmp/absbyai-editcap/registry.json` (`/tmp` like renderq: Codex's sandbox can write it), changed only
  under an `flock`. A reboot clears it; edits re-register on their next `acquire` or `wait`.
- **In use** = edits marked active + waiters promoted into a free slot + **any video with a step holding or waiting
  in the render queue right now**, registered or not. So edits that never called `acquire` still count, and an edit
  already running is admitted when it registers, never stopped.
- **Order:** release date from `Docs/LONGFORM_RELEASE_CALENDAR.md` and `Docs/SHORTS_RELEASE_CALENDAR.md` (the earlier
  of the two for a long-form that also has a Short there); a Shorts batch not on the calendar takes the day after its
  parent long-form (parent read from `Handoffs/video-editing/jobs.json`); ads (`RA-`) take the nearest upcoming
  release; the "2027, tentative" list sorts after all 2026 dates; anything else is last. Ties: firing order.
  `--release YYYY-MM-DD` on `acquire` overrides (use when Dan sets a priority).
- **Freeing slots:** `release`; an active edit with no `acquire` and no render-queue activity for 3 hours is marked
  stalled and loses its slot (a render-queue grant counts as activity); a promoted waiter that does not start within
  90 minutes loses its reservation. A stalled edit that comes back simply calls `acquire` again.
- Every call settles the registry (expire, then promote), so each Claude waiter's background `wait` (polls every 30 s)
  and each Codex heartbeat keep the line moving with no central routine.
- **Fail-open:** unreadable registry is set aside and restarted; a lock held over 15 s, an unwritable folder or any
  bug prints a warning and allows the edit (exit 0). Nothing here can deadlock an edit.

Limits: a Claude waiter's background `wait` dies if the app quits; after 90 minutes its reservation passes to the
next edit and `status` shows it stalled. A Codex waiter starts up to 10 minutes late (heartbeat interval).

## Files

`editcap.py` (CLI and library), `selftest.py` (`python3 editcap.py selftest`, 26 checks, temporary registry, includes
the end-to-end dry run: five edits active, a sixth waits in a background `wait`, one finishes, the sixth starts itself).
