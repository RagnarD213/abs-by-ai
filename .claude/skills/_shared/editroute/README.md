# Two-Mac edit routing (`editroute`)

Dan has two Mac minis on a Thunderbolt cable (handoff `Handoffs/two-mac-setup-20261112/03-two-mac-edit-routing.md`,
built 2026-11-14, receipt `Docs/TWO_MAC_EDIT_ROUTING_RECEIPT_20261114.md`):

| | M6 (Dan's Mac) `m6`, 10.66.0.1 | M2 Pro (edit machine) `m2`, 10.66.0.2 |
|---|---|---|
| Edit slots | 2 | 3 |
| Cores for edits while Dan is at the Mac | 6 of 12 | 8 of 10 |
| Cores when Dan is away 30+ min, or 10 PM to 7 AM | 10 (all but 2) | 8 |
| Goes here first | Shorts (SFC, SFL), ad cutdowns, later-round revisions | long-form R1, full chroma key, exercise-demo batches |
| Footage | copied from the M2 with `editroute.py fetch` (internal SSD only) | read in place on the Extreme / Seagate |
| New work folders | internal SSD | Extreme first (internal has ~54 GB free), then internal, then Seagate |
| Review pages | served here | served here AND on the M6, same link (automatic) |

All the numbers are in `hosts.json`. Change one there and `editcap.py` (slots), `renderq.py` (cores, work-folder
order) and `editroute.py` follow on the next call. The M2 has its own checkout: copy a changed `hosts.json` to it too
(see "Keeping the M2 in step" below).

## For an editing session (Claude or Codex)

1. **Before the first `editcap.py acquire` of a NEW edit:**
   `python3 .claude/skills/_shared/editroute/editroute.py pick <JOB> --kind <SFC|SFL|LFC|AD|ADCUT|VSL|EXDEMO> --round <N>`
   (`--chroma` when this run does a full chroma key; `--host m6|m2` only when Dan names a Mac). It prints `m6`, `m2`
   or `wait` on the first line, then the rule and the numbers behind it, and records the decision.
2. **If it names this Mac:** carry on (`editcap.py acquire <JOB>` as always).
3. **If it names the other Mac:** do no production here. Start the edit there:
   * Claude: a new session on the Claude app's SSH connection `m2` (`start_session` with `target: "ssh"`, `host: "m2"`;
     `list_start_targets` shows it). It works on the M2 and shows in Dan's M6 sidebar.
   * Codex: `ssh m2 /Applications/ChatGPT.app/Contents/Resources/codex-cli/CodexCLI.app/Contents/MacOS/codex exec -C "/Users/danielrose/Projects/Claude/Projects/Abs By AI" "<starter prompt>"`
     (verified 2026-11-14). That run lives on the M2's Codex, not in the M6 ChatGPT sidebar.
4. **`wait`** (both Macs full): run `editroute.py wait <JOB>` in the background; it exits 0 and prints the Mac when a
   slot frees on either, oldest first. Then step 2 or 3.
5. **Review pages on the M2:** `review_server.py PORT DIR` as always. On the M2 it also copies the page (only the files
   it links) to the M6 and serves it there on the same port, and prints `Also open on the M6 (Dan's Mac): http://127.0.0.1:PORT/`.
   Give Dan that link: it is the same address on both Macs. Pick a port free on both with `editroute.py free-port`.
   Silent-check and owner-handoff audio rules are unchanged (same server code on both Macs).
6. **Finished files from an M2 edit:** `editroute.py push <file or folder> ...` copies them into the M6's project
   folder at the same place (`Videos to Review/...`, delivery folders). A different file already there is kept as
   `NAME.m6-before-<time>`. Nothing is deleted on either Mac. Git changes (master list, queue) are committed and
   pushed from the M2's own checkout as usual.
7. **Footage for an M6 edit:** `editroute.py fetch <JOB> "/Volumes/Extreme/<shoot folder>/C1730.MP4" ...` copies it
   from the M2 into this Mac's job folder (`~/Projects/_edit_work/<JOB>/footage/`). The originals are only read.
   Archive moves to the Seagate are done on the M2, where the drive is plugged in.

## Commands

| Command | What it does |
|---|---|
| `pick JOB [--kind K] [--round N] [--chroma] [--host m6\|m2 [--move]] [--dry-run] [--json]` | where the next edit goes, and why |
| `wait JOB` | block until either Mac has a slot for JOB (combined line, oldest first) |
| `where JOB` | which Mac holds JOB's work folder or edit slot |
| `status [--json]` | one table for both Macs: slots, edits, cores, queue, load, memory, free space, git, M2 review pages |
| `fetch JOB SRC...` | M6: copy footage from the M2 |
| `push PATH...` | M2: copy finished files into the M6 project folder |
| `mirror-review PORT DIR` | M2: re-mirror a review page by hand |
| `free-port [--from 9800]` | a review port free on both Macs |
| `whoami` | this Mac's name, slots and core budget now |
| `selftest` | the unit tests (`tests/test_editroute.py`) |

## The rules (from the handoff; `decide()` in `editroute.py`)

1. A job with a work folder (or a live edit slot) on one Mac goes back there. Never moved mid-flight. If both Macs
   have a folder: the one with a live slot, else the one with Dan, else the bigger folder (a mirrored review folder
   on the M6 does not count against the M2's real one). `--host X --move` moves it only when Dan says so.
2. Dan names a Mac: that Mac (it waits there if full).
3. Shorts (SFC, SFL), ad cutdowns, later-round revisions (`--round 2+`): the M6 first.
4. Long-form R1, a full chroma key (`--chroma`), exercise-demo batches: the M2 first.
5. The preferred Mac full: the other. The M6 under Dan's own load (memory pressure not normal, or the 5-minute load
   above its 12 cores) counts as full for new edits.
6. Anything else (an ad, a VSL, unknown): the Mac with the smaller share of its slots in use, the M6 on a tie. From
   idle: M6, M2, M2, M6, M2.
7. Both full: the combined line, oldest first. A waiter whose `wait` loop stopped looking 5 minutes ago is skipped.

Counted as used on a Mac: its active and promoted edits, its edit-cap waiters, anything in its render queue, and jobs
routed there in the last 30 minutes that have not started yet. An unreachable Mac counts as full and is named in the
reasons. The same job asked again within 30 minutes gets the same Mac.

## How it works

- Each Mac knows itself from its host name (`m6`, `m2`). `editroute.py local-status --json` reports one Mac; the
  other Mac is read with `ssh m2 ...` (connect timeout 3 s, whole call 8 s: the Seagate is a hard disk and can take a
  few seconds to wake). On the M2, `pick` and `wait` run on the M6 over ssh, so the decision log and the combined line
  are in one place: `~/.absbyai-editroute/` on the M6 (`decisions.jsonl`, `waiting.json`, `reviews.json`); if the home
  folder is not writable (Codex sandbox) it uses `/tmp/absbyai-editroute`.
- `hostcfg.py` is the shared reader. It fails open: a missing or broken `hosts.json`, or an unknown Mac, gives the old
  numbers (5 slots, all cores but 2) and never blocks an edit.
- Idle time is `ioreg -c IOHIDSystem` `HIDIdleTime`, cached 15 s in `/tmp/absbyai-editroute-idle.json`.
- The edit-cap and render-queue state folders stay in `/tmp` (`/tmp/absbyai-editcap`, `/tmp/absbyai-renderq`): moving
  them while WV-03 held slots would have split the line in two, and Codex's sandbox can only write `/tmp`. A restart
  clears them, which only forgets edits that were idle anyway (a running edit re-acquires on resume).

## Keeping the M2 in step

The M2 has its own git checkout (`/Users/danielrose/Projects/Claude/Projects/Abs By AI`), not a share of the M6
folder (SMB cannot serve the exFAT drives, and six live sessions there work in that checkout). On 2026-11-14 it could
not `git pull` because its `AI_COORDINATION.md` had a local edit that upstream also changed, so the routing files were
copied to it directly (older copies kept as `*.before-editroute-20261114`). When the M2 next pulls, git will list
those files as "would be overwritten"; they are identical to GitHub's, so `git checkout -- <file>` (tracked) or moving
the untracked `editroute/` folder aside, then pulling, is safe.
