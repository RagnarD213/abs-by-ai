# Queue How To Do M100s (DS-25) once the M2 answers (2026-11-26, Claude)

**For Codex (newest Sol, medium) and Grokbot. Dan authorizes this whole step; do not stop to ask him.**

## Why it is blocked
On 2026-11-26 the M2 (`ssh m2`, 10.66.0.2) answered neither ssh, ping nor mDNS; its mirrored review pages are ~115 h old (down since about Nov 21). `resume.py check DS-25` and `editcap.py acquire` return 6 (ownership unresolved) and `batch.py enqueue-chat` says both Macs must be reachable. M6 storage is also tight: internal 21 GB free, Extreme (now plugged into the M6 directly) 48 GB free. No DS-25 folder exists anywhere visible; nothing was built and no slot was taken.

## What to do
1. Confirm the M2 answers: `ssh -o ConnectTimeout=10 m2 hostname`. If not, stop; only Dan can power it on or reseat the cable.
2. From the main project folder on the M6:
   `python3 scripts/edit-queue/batch.py enqueue-chat DS-25 --round 1 --brief "$PWD/Handoffs/video-editing/DS-25-how-to-do-m100s.md" --title 'How To Do M100s' --size S --kind SFC --executor codex --need-gb 10 --target 'first review'`
3. Relay its last line (CAN START / WILL NOT START) to Dan word for word, then delete this handoff's OPEN line in `Handoffs/README.md`.

Footage: talking takes `/Volumes/Extreme/abs by ai 8:28 shoot | jeff | dan | ads, dedicated shorts, b roll, scripted long form content/main camera/C1672.MP4`; M100 moves `/Volumes/Extreme/10:15 dan rose fitness shoot - green screen, outdoor shorts, outdoor b roll, studio backdrop/C1736.MP4` (in the folder root, not `main camera/`). The Extreme may move back to the M2; use `editroute.py` paths, not these, if so.
