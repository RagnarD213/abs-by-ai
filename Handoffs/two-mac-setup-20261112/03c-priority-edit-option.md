# 03c: a "priority" option for urgent client edits (Claude, after 03 is idle)

Category: code (edit routing). Written 2026-11-14 by Claude. Dan asked whether an urgent client edit should go to
the M6; the answer is yes (newer M6 chip, internal SSD, 10 cores when Dan is away), but the router cannot be told an
edit is urgent. Not built in the asking session because `editroute.py` was changed by the 03 routing session 36
minutes earlier and its live test (DS-107) was still running; one owner per file.

## What to build

In `.claude/skills/_shared/editroute/editroute.py` (and `editcap.py` where needed):

1. `editroute.py pick JOB ... --priority`: route to the M6 unless the M6 is unreachable, or its internal drive has
   less free space than the job's honest need plus a 150 GB margin (then the M2, with the reason printed).
   It ignores the usual kind-based preference and Dan's-load diversion, but still prints a note when Dan is
   working on the M6 (the render queue then gives it 6 cores, not 10).
2. If both M6 slots are taken, the priority edit takes the NEXT free M6 slot ahead of every waiter (record
   `priority: true` in the waiting line and in the editcap entry; `settle()` promotes priority waiters first).
   Never pre-empt or stop a running edit.
3. Render queue: a priority job's heavy steps go to the front of the queue on that Mac (renderq already orders
   the line; add a priority flag rather than a new queue).
4. Free-space check for every pick (not only priority): refuse to route a job to a Mac whose work drive would drop
   under 100 GB, using `--need GB`. The router already reports free space but does not act on it.
5. Tests in `editroute/tests/` and `editcap/selftest.py`; README and VIDEO-RULES "Two Macs" lines updated
   ("urgent client edit: `pick --priority`").

## Facts (2026-11-14)

- M6: Apple M6, 2 slots, 6 cores while Dan is active / 10 away, ~300 GB free internal (Great Again T VSL WV-03 uses
  184 GB of it after round 1). M2: Apple M2 Pro, 3 slots, 8 cores, 55 GB free internal, edits work on the Extreme.
- The M6 reads the Extreme over SMB at about 140 MB/s uncached; writing to it over SMB measured 1.7 MB/s while a
  cleanup was running (re-test before relying on it). M6 edits keep work folders on the M6's internal drive.

Done looks like: `editroute.py pick TEST --kind AD --priority` prints `m6` with reasons, a priority waiter starts
before older waiters in the selftest, tests pass, pushed with `scripts/git/safe-push.sh`.
