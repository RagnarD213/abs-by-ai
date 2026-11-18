# Grant Full Disk Access to the edit queue's background Python on both Macs

**Handoff, November 18, 2026 | Ops, not a video edit | For: Codex (GPT-6.2 Sol, High) and Grokbot | Written by Claude, which cannot change Mac privacy settings | Parent: [overnight batch repair](handoff-20261118-overnight-batch-start-and-permission-fixes.md), receipt [Docs/OVERNIGHT_BATCH_REPAIRS_20261118.md](../Docs/OVERNIGHT_BATCH_REPAIRS_20261118.md)**

**Dan's authorization:** Dan authorized every step of the overnight batch repair, including this grant. Do the whole step on both Macs without asking him. Do not change any other privacy, security or login setting. No passwords go into repo files.

## Why

The overnight edit queue runs from a LaunchAgent (`com.absbyai.edit-queue`) on each Mac. Its Python is refused by macOS when it touches the external drives. The check was run at 5:02 p.m. Central on Nov 18 from the agent itself on both Macs:

| Mac | Videos to Review | internal work folder | Extreme work folder | Expansion work folder |
|---|---|---|---|---|
| M6 | FAIL: Operation not permitted | PASS | FAIL: Operation not permitted | FAIL: Operation not permitted |
| M2 | FAIL: Operation not permitted | PASS | FAIL: Operation not permitted | FAIL: Operation not permitted |

Until both Macs pass, the queue refuses to start any edit (this is deliberate).

## Exact programs to add to Full Disk Access

System Settings > Privacy & Security > Full Disk Access > "+" > press Cmd-Shift-G > paste the path > Open > make sure its switch is ON. Add both entries on each Mac (the agent launches the first; macOS runs the second).

**M6 (Dan's Mac, user `danrrose`):**
1. `/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9` (the real file; `/Library/Developer/CommandLineTools/usr/bin/python3` is only a shortcut to it)
2. `/Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/Resources/Python.app`

**M2 Pro (headless, user `danielrose`, reach it with Screen Sharing; from the M6 the SSH name is `m2`):**
1. `/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9` (the real file; `/Applications/Xcode.app/Contents/Developer/usr/bin/python3` is only a shortcut to it)
2. `/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/Resources/Python.app`

Full Disk Access cannot be granted from a shell command; it needs the System Settings window (Screen Sharing on the M2).

## Reload and prove it, per Mac

On each Mac, in Terminal (on the M2 through `ssh m2`):

```bash
launchctl kickstart -k gui/$(id -u)/com.absbyai.edit-queue
```

```bash
cd ~/Projects/Claude/Projects/Abs\ By\ AI && python3 -B scripts/edit-queue/batch.py drive-probe --launchd
```

Expected last line: `PASS m6 background agent: every folder: create, write, rename, delete` (or `m2`). The JSON above it lists every folder with `"passed": true`. A `FAIL` line names the folder still refused; recheck that both entries are switched on, then run the two commands again.

When both Macs pass, run once on the M6:

```bash
cd ~/Projects/Claude/Projects/Abs\ By\ AI && python3 -B scripts/edit-queue/batch.py preflight
```

Expected: `"passed": true`. **Then switch the two waiting edits on (Dan's go, Nov 18, 5:41 p.m.: "disable the block on new video starts so that videos will start once we're done with the current ones"):**

```bash
cd ~/Projects/Claude/Projects/Abs\ By\ AI && python3 -B scripts/edit-queue/batch.py start chat-WV-07-R1 && python3 -B scripts/edit-queue/batch.py start chat-REALDEMOS-B05-R1
```

Claude tried both at 5:44 p.m.; each was refused only because of the missing grant. Start nothing else.

## Report back

Per Mac and per folder: pass or fail, the time, and the last line of each `drive-probe` run, plus the preflight result. Write it to the end of this file under "Result" and tell Dan in one line. If the grant does not hold after a restart, say so; the fallback is an M2 self-login, never a hop through the M6.

## Result

- M6, Nov 18 5:49 PM Central, granted by Dan himself (Python.app and python3.9): Videos to Review PASS; internal work folder PASS; Extreme work folder PASS; Expansion work folder PASS. Last line: `PASS m6 background agent: every folder: create, write, rename, delete`.
- M2: not granted yet.
- **Nov 18, ~5:57 p.m. (Claude):** M2 still `FAIL` after Dan's grant and an agent restart. M2's Full Disk Access list holds `.../Versions/3.9/bin/python3.9` and `com.apple.python3` (Python.app), both on, but not the agent's own program `/Applications/Xcode.app/Contents/Developer/usr/bin/python3`. Add that one, restart the agent, re-probe.
