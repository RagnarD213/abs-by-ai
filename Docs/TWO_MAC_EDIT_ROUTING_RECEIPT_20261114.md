# Two-Mac edit routing receipt (handoff 03)

Executed: November 14, 2026, about 11:10 a.m. to 11:55 a.m. America/Chicago, on the M6.
Owner: Claude (Opus 5.5), a side session started from Dan's handoff session.
Source: `Handoffs/two-mac-setup-20261112/03-two-mac-edit-routing.md`. Code commit: `5701b23` (pushed).

**Status at 11:55 a.m.: built, unit-tested, live on both Macs; the real end-to-end test routed but not yet started (afternoon follow-up below: started, timeouts fixed, M2 checkout reconciled, dispatcher routed)**: it needs
the Claude app's SSH connection `m2`, which does not exist yet (`list_start_targets` showed `ssh: []` at 11:15 and
again at 11:45). Nothing was deleted on either Mac. The running WV-03 edit on the M6 was not stopped.

## What Dan gets

| | M6 (Dan's Mac) | M2 Pro (edit machine) |
|---|---|---|
| Edit slots | 2 | 3 (total 5) |
| Cores for edits, Dan at the Mac | 6 of 12 | 8 of 10 |
| Cores, Dan away 30+ min or 10 PM to 7 AM | 10 | 8 |
| Goes here first | Shorts (SFC, SFL), ad cutdowns, later-round revisions | long-form R1, full chroma key, exercise-demo batches |
| Footage | copied from the M2 with `editroute.py fetch` | read in place on the Extreme / Seagate |
| New work folders | internal SSD | Extreme first, then internal, then Seagate |
| Review pages | served here | served there AND here, same link, automatically |

All numbers: `.claude/skills/_shared/editroute/hosts.json`. Guide: `.claude/skills/_shared/editroute/README.md`.

## Changed precondition (from the starting brief)

The handoff assumed the drives would be mounted on the M6. They are not and cannot be: both are exFAT under FSKit
on the M2, which cannot serve them over SMB. Since Dan's 7:37 a.m. change, `ssh m2 ls /Volumes/Extreme` works. So:
M2 edits use the drives locally; M6 edits use the M6's internal SSD and pull footage over the cable
(`editroute.py fetch`, measured 145 MB/s: a 6.4 GB roll in 45 s, checksums equal); Seagate archive moves stay on the
M2. Written into `hosts.json`, the routing rules and `VIDEO-RULES.md`.

## Build, step by step

| Handoff step | Result |
|---|---|
| 1. Per-host queues | `renderq.core_budget()` reads `hosts.json` (`hostcfg.py`): M6 6 present / 10 away or night (idle from `ioreg -c IOHIDSystem` HIDIdleTime, cached 15 s; hour from the clock), M2 8. `editcap.CAP` = 2 on the M6, 3 on the M2. `EDITCAP_MAX` / `GATE_BUDGET` still override; a broken or missing `hosts.json` or unknown Mac falls back to 5 slots / all cores but 2. **State folders stay in `/tmp`**: WV-03 held slots in `/tmp/absbyai-renderq` all session, so moving it would have split the line, and Codex's sandbox can write only `/tmp`. Not moved. |
| 2. `editroute.py` | `pick`, `wait`, `where`, `status`, plus `fetch`, `push`, `mirror-review`, `free-port`, `whoami`, `selftest`. Reads both Macs (local + `ssh`, connect timeout 3 s, whole call 8 s because the Seagate hard disk can take seconds to wake; a status round trip measured 0.22 s). An unreachable Mac counts as full and is named. Decisions in `~/.absbyai-editroute/decisions.jsonl` on the M6 (on the M2, `pick` and `wait` run on the M6 over ssh). Combined waiting line `waiting.json`, oldest first, only for jobs with no work folder yet. |
| 3. Starting an edit on the M2 | **Claude:** the app's SSH connection, not yet added (see "For Dan"). **Codex, verified:** `ssh m2 .../CodexCLI.app/Contents/MacOS/codex exec` ran on the M2 (read-only test, answered `m2` in 8 s, 15k tokens). Not verified: the Codex app's own remote option (a click inside ChatGPT; not reachable from here) and Screen Sharing to the M2 (fallback only). A `codex exec` run lives in the M2's Codex history, not in the M6 ChatGPT sidebar. |
| 4. Shared project folder | **Fallback used: the M2 keeps its own git checkout.** Not shared: SMB cannot serve the drives anyway, six Claude sessions and Codex automations work inside the M2 checkout now (renaming it under them would break them), and File Sharing is off on the M6. No benchmark over a share was possible. Untracked media move with `editroute.py push` (M2 to M6) and `fetch` (M6 from M2) over ssh. **Found:** the M2 checkout cannot `git pull` (17 behind) because its `AI_COORDINATION.md` has a local edit (08:07) that GitHub also changed. Not touched. The routing files were copied to the M2 directly, only where its copy was byte-identical to the M6's pre-edit copy; replaced copies kept as `*.before-editroute-20261114`. `review_server.py` there is now GitHub's 0a5d54e plus the mirror hook. |
| 5. Work folders | M6: internal SSD (`~/Projects/_edit_work`), no drives. M2: new folders on the Extreme before the internal drive (58 GB free), then the Seagate; an existing folder is always reused. |
| 6. Review pages | `review_server.py PORT DIR` on the M2 now also copies the page's cached files (only what it links) to the M6 and serves them on the same port: the link `http://127.0.0.1:PORT/` opens on Dan's Mac. Test page made on the M2: served on the M6 in 1.4 s, `<video muted>` default and the shared audio helper injected (silent-check and owner-handoff rules unchanged); then removed from both. Chosen over binding the M2 hub to 10.66.0.2: no restart of the M2 hub serving Dan's open reviews, no Chrome local-network prompt, one link for Dan. `editroute.py status` lists the M2 pages mirrored to the M6. The M2's own hub still binds only localhost. |
| 7. Skills and rules | `VIDEO-RULES.md` "Two Macs"; `AGENTS.md` one paragraph; `/shorts`, `/longform-edit`, `/ad-edit` one paragraph each in "Edit slot first"; video-rounds README one line; editcap and renderq READMEs; memory `two-mac-edit-routing` (synced to `Docs/memory`). |
| 8. Scheduled tasks | Checked: 8 recurring tasks enabled on the M6, **0 enabled on the M2**; nothing on both. edit-stall-watchdog stays off (it watches edits, which now run on both Macs; needs a two-Mac version before it is turned on). |
| 9. Tests | `editroute.py selftest`: 30 of 30 pass on both Macs (every rule, unreachable M2, per-Mac numbers, M2 work folder on the Extreme, combined line, broken config fails open). `editcap.py selftest` 27 of 27 on both. `renderq.py selftest` 61 of 61 on the M6 (it now pins the old core rule with `GATE_NO_HOSTCFG=1`, because one drive-order check assumed 10 cores). |

## Live state at the end

```
                     M6 (Dan's Mac)                    M2 Pro (edit machine)
Edit slots           1 of 2 in use (WV-03)             1 of 3 (DS-107 routed, not started)
Cores for edits      6 of 12 (Dan at the Mac)          8 of 10
Next dedicated Short m6;  next long-form R1 m2;  next other edit m2
```

Effect on WV-03: its later heavy steps now get 6 cores while Dan is at the Mac instead of 10 (one heavy step at a
time instead of two). It is not stopped; it speeds up again when Dan is away or after 10 PM. Measured at 11:33: Dan's
own apps used under 1 core; the WV-03 key used about 4.

## Real test (handoff step 9)

- **Picked:** DS-107 "Your Metabolism Is Not The Reason You're Fat" (queued SFC, 11/13 green-screen roll C1908 on the
  M2's Extreme, house chroma key). `editroute.py pick DS-107 --kind SFC --chroma` printed **`m2`, rule 4: a full
  chroma key goes to the M2 first; it has a free slot**, by itself, without naming a Mac.
- **Not yet done:** start it on the M2 from the M6 (needs the SSH connection), render there, review page on the M6,
  finals into the M6 project folder (`editroute.py push`, after Dan approves the cut). The first review page comes
  before any full render (pre-render approval), so finals need Dan's review regardless.
- **Same render step on both Macs** (40 s of a 4K 10-bit roll scaled to 1080p, x264 medium, CRF 18, through each Mac's
  render queue, 4 cores, same output on both, 28,820,247 bytes):

  | | Ran | Waited for a slot first | Conditions |
  |---|---|---|---|
  | M6 | **32.8 s** | 6 min | WV-03 running beside it (6-core budget, Dan at the Mac) |
  | M2 | **39.5 s** | 3 s | otherwise idle |

  Per 4-core step the M6 is about 17% faster even while busy. The M6's wait is the 6-core budget doing its job
  (WV-03 held 6 of 6). Tuning hint: Dan's own apps used under 1 core during the session, so `cores_present` 8 on the
  M6 would still leave him 4 cores; that is Dan's call (one number in `hosts.json`).

## Leftovers

- Dan: add the SSH connection `m2` in the Claude app (steps below), then the DS-107 session starts on the M2.
- Dan's decision (in `Docs/DAN_DECISIONS.md`): freeing the M2's internal drive. The "240 GB of old local copies" is
  really 196 GB of old edit folders; the M2 checkout is live and stays.
- The M2 checkout's blocked pull (`AI_COORDINATION.md`), for whoever owns the M2 sessions. When it pulls, the routing
  files will show as "would be overwritten": they equal GitHub's, so `git checkout -- <file>` (and moving the
  untracked `editroute/` aside) then pulling is safe.
- `com.absbyai.nightly-footage` on the M2 is installed but explicitly **disabled** (`launchctl print-disabled`), not
  just unloaded. Left as is: someone turned it off on purpose; Dan decides whether it runs.
- The edit-queue dispatcher `com.absbyai.edit-queue` runs on the M2 only (disabled on the M6), so jobs it launches
  start on the M2 without `editroute.py pick`. Fine as one place; teach it to route before it is moved.

## Follow-up, November 14 afternoon (Claude Fable 5.2, a session running ON the M2 through the new `m2` connection)

Codex finished 02b (the Claude app's SSH connection and environment `m2`), so the steps "For Dan" below are done
and the first three Leftovers above are closed or changed. Nothing was deleted on either Mac, WV-03 was not
touched, and the overnight queue is still paused on both Macs (`scripts/edit-queue/PAUSE`, dated October 17).

**1. Real test: started, running.** `editroute.py pick DS-107 --kind SFC --chroma` again printed `m2` (rule 4) by
itself. The edit was started from the M6 app as its own session on the SSH connection `m2`: "Metabolism Not The
Reason SFC R1" (Opus 5.5, high). Within minutes `editroute.py status` showed `Active edits: DS-107` under the M2 and
its work folder on the M2's Extreme (`/Volumes/Extreme/_edit_work/DS-107`). Still to come from that session: the
review page opening on the M6, step timings (`ROUTING-PROOF.md` in the work folder), and, after Dan approves the
cut, the finals copied into the M6 project folder with `editroute.py push`.

**2. Intermittent routing timeouts: cause found and fixed.** Evidence: at 12:11:44 a `pick` on the M6 reported
"m2 unreachable ... timed out after 8.0 seconds ... counted as full". The M2's ssh log shows the login finished in
0.06 s, so the cable and ssh were fine; the 8 s went inside the M2's status answer. That answer read the work
folders on every drive, including the Seagate, a 24 TB hard disk that spins down when idle and takes 10 s or more
to wake. Awake, the same call takes 0.08 s (measured 16 times). Fix in `editroute.py`:
- each external drive gets 2 s to answer; past that the status call answers from the drive's last saved free space
  and folder list (`drives-cache.json`), so it never waits on a sleeping disk and rule 1 still finds a job whose
  folder is on that drive. The table shows `(asleep)`; `pick` adds a note;
- a connection that fails fast is tried once more; a Mac that takes the full 8 s is not asked twice; the error
  now reads "no answer within 8 s" instead of a Python command dump;
- found on the way: since the drives became network shares on the M6 this morning, the M6 saw every job folder
  on the Extreme as its own, so rule 1 could see a job "on both Macs". A drive that reaches a Mac as a network
  share now counts as the other Mac's; the M6 reports only its free space, marked `(shared)`.
Not changed, for Dan to know: the same 12:11 answer also counted the M6 as full because its 5-minute load (12.5)
was above its 12 cores while WV-03 was rendering there. That is rule 5 as written.

**3. M2 checkout reconciled.** It was 28 commits behind with 1,230 uncommitted entries, and `git pull` refused.
Of the 82 files GitHub had changed, 61 were untouched locally (updated), 20 were hand copies already identical to
GitHub's (left alone), and 1 (`AI_COORDINATION.md`, the nightly-footage owner's edit) was three-way merged with the
local edit kept as an uncommitted change. Run again 11 minutes later for 6 more commits pushed by another session
(one old local edit to the chroma-key guide was already inside GitHub's version; the live edits to the queue
files stayed). Result: the M2 is level with GitHub, no local edit lost, backups in `tmp/m2-reconcile-20261114-*/`.
The tool is kept: `scripts/two-mac/reconcile-checkout.py` (`--dry` first). The untracked
`*.before-editroute-20261114` copies are still there (nothing is deleted without Dan).

**4. The overnight dispatcher uses the router.** `scripts/edit-queue/dispatcher.py` now asks
`editroute.py pick JOB --queue` before every launch and launches a job only when the router names the Mac it runs
on. A job sent to the other Mac (its work is there, or this Mac's slots are full) or to `wait` stays for a later
tick and the next eligible job is asked; no router answer launches nothing. Unattended launches are their own
routing class, QUEUE, sent to the M2 first (`hosts.json`, one word to change). `launch-one` asks too
(`--ignore-router` when Dan names this Mac). The pause is checked first: a paused queue never calls the router,
and a dry run today still says "STOP: PAUSE file present ... launching nothing". Not built: starting a queue job
on the other Mac remotely; with the queue's own limit of two jobs on a three-slot M2 it is not needed yet.

**Tests.** `editroute.py selftest`: 53 of 53 (30 before; new: sleeping drive, network share, retry, queue class,
plus the other session's 8 resume tests). `editcap.py selftest` 27 of 27, `renderq.py selftest` 61 of 61.
`scripts/edit-queue/tests/test_edit_queue.py`: 59 run, the 8 new `TwoMacRouting` tests pass; 3 older tests fail
exactly as they did before this change (they expect a routing table Dan changed on October 2).

**Seen, not changed.** The paused dispatcher's log on the M2 says "claude: program not found" and "codex: program
not found" (program paths in `config.json` are out of date), and its review queue is over its limit (5 of 4).
Both must be fixed before Dan resumes the queue.

## For Dan: add the M2 to the Claude app (one time, about 2 minutes)

1. In the Claude app on the M6, open the **Code** tab and start a **new session**.
2. Click the folder/place picker at the top of the new session and choose **SSH** > **Add connection**
   (or Settings > SSH connections if the picker does not show it).
3. Name: `m2`. Host: `m2` (or `10.66.0.2`). User: `danielrose`. Key: `~/.ssh/id_ed25519`.
   Folder: `/Users/danielrose/Projects/Claude/Projects/Abs By AI`.
4. Click **Connect**. Accept the host key and let the app install its helper on the M2. If it asks you to sign in to
   Claude there, sign in.
5. Close that test session and tell this session "m2 is added".
