# Clear space on the Extreme drive (M2), 2026-11-17

**Model:** Claude Sonnet 5, medium effort. Run on the M6 (Claude's SSH connection `m2` for drive commands). Dan reviewed and fired this handoff; that is his approval to move verified-finished jobs to the Seagate.

## Goal
The Extreme (4 TB, on the M2) is 100% full (30 GB free). Get it to **at least 1 TB free** without losing anything: copy finished work to the Seagate (`/Volumes/Expansion`), verify every file by SHA-256, and only then remove the Extreme copy.

## Why nothing has moved on its own
The nightly `jobarchive` job (`.claude/skills/_shared/jobarchive/README.md`) has been stopping every night on both Macs:
`BLOCKED: review reference evidence incomplete: ... AbsByAI Reviews/9717/manifest.json` (the folder 9717 no longer exists).
Even unblocked, it keeps the source until an **independent second copy** is verified (`~/.absbyai-jobarchive/verified-second-copies.json`).

## Steps
1. Fix the blocker: find where jobarchive reads review 9717 (a stale review registry entry), and make the scan treat a review whose folder is gone as retired, not as unknown evidence. Run `jobarchive.py selftest`, re-install on both Macs (`install`; scp to the M2 first), then `scan` on the M2 and save the output.
2. Never touch active jobs. Keep (do not move): WV-03, WV-04 and anything `wv*`/GAT; `SRM-goldenroots-jointvigor` and any JV job; DS-98; RO-39; REALDEMOS-B04; CLIPLIB; anything in `editcap.py status`, `renderq.py status`, `AI_COORDINATION.md` ACTIVE as in-progress or waiting on review, or in `keep.txt`. If unsure, keep it and list it.
3. Candidates in `/Volumes/Extreme/_edit_work` (sizes 2026-11-17): finished/scheduled jobs such as DS-38, DS-42, DS-106, DS-107, DS-108, DS-109, RO-14, RO-15, RO-17, RO-22, RO-23, RO-32, sl09, sl06, sl08, sl03, SL-11, SL-13, ro01, ro08, ro10, ro16, ro27, RO-25, RO-30, DS-40-codex, DS-34-r2-keycache, ad1-8-14, ad2-vert-v2, ad3-vert, ads234-8-14, ra04, abwheel, website-video-828, wv01-edit (~2 TB total). Check each against step 2 first. `kit9x16` (160 GB) is a shared reference kit: keep unless nothing references it.
4. Raw shoot folders at the drive root (11:13 262 GB, 8:28 229 GB, 10:15 224 GB, 9:23 195 GB, 10:23 88 GB): first check whether each already has a verified copy on the Seagate AND Google Drive (nightly footage receipts, `Handoffs/handoff-20261005-claude-nightly-footage-offload.md`). If both copies verify by hash, they count as the second copy; record them in `verified-second-copies.json` and remove the Extreme copy. If not verified, leave them and list them.
5. Second copy for edit jobs: the Seagate is the first copy. For the independent second copy use Google Drive (the business Drive folder already used for backups) or leave the source in place. Do not invent another location. If no second copy is practical, move only enough jobs to reach the target, oldest finished first, and report that the rest wait for a second drive (Dan is buying two 4 TB SSDs).
6. Delete the stray installers at the drive root (`Install Security for Windows.exe`, `SanDisk Security Installer.dmg`, `Install Security for Mac.zip`, 30 MB): these are SanDisk's factory files, safe.
7. Report: before/after free space, every job moved with its Seagate path and hash receipt, every job kept and why. Write the receipt to `Docs/EXTREME_CLEANUP_RECEIPT_20261117.md` and push with `scripts/git/safe-push.sh`.

## Hard rules
- Never remove a source before every file is re-read from the Seagate with a matching SHA-256 (the Seagate corrupted copies Nov 1 to 3).
- Never use `rm -rf` on anything not on the verified list. Use `jobarchive.py run` where it applies instead of hand copies.
- Restoring a job: `jobarchive.py restore JOB`.
