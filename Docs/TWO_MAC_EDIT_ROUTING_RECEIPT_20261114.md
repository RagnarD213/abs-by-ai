# Two-Mac edit routing receipt (handoff 03)

Executed: November 14, 2026, about 11:10 a.m. to 11:55 a.m. America/Chicago, on the M6.
Owner: Claude (Opus 5.5), a side session started from Dan's handoff session.
Source: `Handoffs/two-mac-setup-20261112/03-two-mac-edit-routing.md`. Code commit: `5701b23` (pushed).

**Status: built, unit-tested, live on both Macs. The real end-to-end test is routed but not yet started**: it needs
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

## For Dan: add the M2 to the Claude app (one time, about 2 minutes)

1. In the Claude app on the M6, open the **Code** tab and start a **new session**.
2. Click the folder/place picker at the top of the new session and choose **SSH** > **Add connection**
   (or Settings > SSH connections if the picker does not show it).
3. Name: `m2`. Host: `m2` (or `10.66.0.2`). User: `danielrose`. Key: `~/.ssh/id_ed25519`.
   Folder: `/Users/danielrose/Projects/Claude/Projects/Abs By AI`.
4. Click **Connect**. Accept the host key and let the app install its helper on the M2. If it asks you to sign in to
   Claude there, sign in.
5. Close that test session and tell this session "m2 is added".
