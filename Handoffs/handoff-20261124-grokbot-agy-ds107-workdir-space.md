# Free space so `renderq.py workdir AGY-DS107 --need 15` passes (Grokbot, 2026-11-24)

Narrow, urgent slice of [handoff-20261124-m6-extreme-space-cleanup.md](handoff-20261124-m6-extreme-space-cleanup.md). That handoff is the broad cleanup; this one is only what the Antigravity DS-107 edit test needs ([handoff-20261124-antigravity-m6-edit-test.md](handoff-20261124-antigravity-m6-edit-test.md)). Do not duplicate work: if Codex already ran Step 2 or 3 of the broad handoff, start by re-running the gate command below.

Dan's authorization: do the whole job, including deleting the folders below once each has a verified backup. Do not ask Dan again. Passwords and Drive logins are yours (you have the vault). Do not write secrets into repo files.

## The goal (single pass/fail check)
Run on the M6, from the project folder:

```
cd "/Users/danrrose/Projects/Claude/Projects/Abs By AI"
python3 .claude/skills/_shared/renderq/renderq.py workdir AGY-DS107 --need 15
```

It must print a valid workdir path instead of `RuntimeError: no eligible work storage`. If your first try prints a path, it created or reserved nothing you need to keep; remove any empty `AGY-DS107` folder it made and any reservation it added unless the DS-107 test starts right away.

## Why it fails today (measured 2026-11-24)
The rule per drive is: free - committed - need >= reserve.
- M6 internal: 41.3 GB free, 43.0 GB committed, reserve 80 GB. Fails.
- Extreme (`/Volumes/Extreme`): 20.7 GB free, 0 committed, reserve 30 GB. Fails; needs about +24.3 GB free (aim for +30 GB margin). `df` shows 19 GB free, so free more than 26 GB to be safe.
- The 43.0 GB "committed" is `~/.absbyai-editroute/storage.json`: `--help` 20 GB (a bad job name, certainly junk), `WV-05` 20 GB (that job moved to the M2), `DS-41-setup` 3 GB.

## Fastest, safest route: Extreme
Only ~25-30 GB is needed there, and the best candidates are old October 4 ad scratch folders. Dan said on 2026-11-15 he wants no more Abs By AI ads, so these are not being reworked.

Candidates on `/Volumes/Extreme/_edit_work/` (sizes today): `ad1-8-14` 21 GB, `ad2-vert-v2` 21 GB, `ad3-vert` 15 GB, `SL-13` 15 GB (setup done, waitlisted for Jan 28, 6 PM Central; keep its masters), `kit9x16` 160 GB (shared ad kit; the skill `shortad-from-longform` points at it, so do NOT delete it whole).
Deleting `ad1-8-14` plus `ad2-vert-v2` (42 GB) clears the Extreme gate by itself.

Do this, in order:
1. For each folder, find what is irreplaceable: the finished ad exports (look for `*_graded.mp4`, `ad*_vertical_9x16.mp4`, `ad*_square*.mp4`, `CUT_*`, `_approved_*` folders, `SCRIPT_FOR_DAN.md`, receipts). Check whether each is already on Google Drive and on YouTube (the ads were set up unlisted, see `Docs/DGEN_CONVERSION_CAMPAIGN.md` and `Docs/AD*_SETUP_RECEIPT_*.md`). If not on Drive, upload the finals to the shared Drive folder, anyone with link can view, then verify by size and SHA-256 (download or Drive's reported md5).
2. Never delete the only copy. The Seagate (Expansion) is in Austin with the M2 and is not mounted, so it cannot be your second copy today. Drive is the second copy.
3. Before deleting, confirm nothing uses the folder: `python3 .claude/skills/_shared/renderq/renderq.py status`, `python3 .claude/skills/_shared/editcap/editcap.py status`, `lsof +D <folder>`, and `grep -R "<folder name>" .claude/skills Docs scripts` for live references (clip library catalogs, skills). A folder referenced by a skill or catalog stays.
4. Delete only the verified folders, using the least destructive step that frees the space (delete the regenerable intermediates and the verified-backed-up files; empty the Trash if you used it, since the Extreme keeps trashed files on the same volume).
5. Re-run `df -h /Volumes/Extreme` and the gate command.

If the two ad folders are not enough or cannot be verified, add `ad3-vert` (15 GB), then `SL-13` intermediates only (keep `round2` finals and `RESUME.md`).

## Internal drive route (optional second source, do after Extreme passes or if Extreme is blocked)
1. Clean the stale reservations in `~/.absbyai-editroute/storage.json`. Look in `.claude/skills/_shared/editroute/editroute.py` and `renderq.py` for the supported release/clear command (grep `storage.json`, `release`, `reserve`) and use it. Do not hand-edit the file while a job might be writing it; if there is no command, back the file up first, remove only `--help`, `WV-05` (confirm `WV-05` now lives on the M2: `ssh m2 'ls /Volumes/Extreme/_edit_work/WV-05'`) and `DS-41-setup` (confirm DS-41 setup is done and its folder is not in use), and validate the JSON afterwards.
2. After clearing, internal math is 41.3 - 0 - 15 = 26.3 GB against an 80 GB reserve, so it needs about +54 GB freed. `WV-05.moved-to-m2-20261119` (39 GB) alone is not enough. Delete it only after proving the M2 copy matches (file count and total bytes, ideally SHA-256 on the finals).
3. DO NOT delete `DS-98-blind` (28 GB) on your own: the DS-98 three-way blind edit is waiting on Dan's review of its Round 2 films, and the broad handoff keeps it until he picks a winner. Only delete it if Dan says so in chat.
4. Do not delete WV-07 `key` or `src` yet: WV-07 Round 3 is still with Dan.

## Never touch
- `SRM-JV-R5*` (active Joint Vigor, holds the only edit slot), `DS-107` (the control for the blind test), `DS-40-codex` and any other locked reference or approved master, `RO-39`, `WV-03`, `WV-05`, `WV-06`, `AGY-RO24`, anything in `keep.txt` (`.claude/skills/_shared/jobarchive/keep.txt`), and any raw shoot folder (SHOOT-20261023 etc.).
- Anything a running process, the render queue or the edit cap lists as in use.

## Done = (report back in chat, and write a short receipt)
1. The gate command output showing a valid workdir path.
2. A list of every folder or reservation removed, with its size, where its backup or second copy lives, and the hash/size check you used.
3. Free GB now on M6 internal and on `/Volumes/Extreme`.
4. Anything you chose not to delete and why.
Put the receipt at `Docs/AGY_DS107_SPACE_RECEIPT_20261124.md`, then push with `scripts/git/safe-push.sh -m "AGY-DS107 workdir space receipt" -- <your files>`. Do not leave junk (empty workdir, test reservations) behind.

## Then
Tell Dan the gate passes. The DS-107 Antigravity edit test starts only after this and must stay strictly below Joint Vigor (see the test handoff).

## Starter prompt for Grokbot (self-contained)
> You are working on Dan Rose's Mac (the M6) in the project folder `/Users/danrrose/Projects/Claude/Projects/Abs By AI`. Read `Handoffs/handoff-20261124-grokbot-agy-ds107-workdir-space.md` and do the whole job; Dan has authorized the deletions listed there once each folder has a verified backup (Google Drive upload with size and SHA-256 check; use your own Drive login; set files to anyone-with-link can view). Goal: free enough verified disk space that `python3 .claude/skills/_shared/renderq/renderq.py workdir AGY-DS107 --need 15` prints a workdir path. Fastest route: free about 30 GB on `/Volumes/Extreme/_edit_work` by deleting the verified October 4 ad scratch folders `ad1-8-14` and `ad2-vert-v2` after saving their finished ad exports to Drive. Also clean the stale reservations in `~/.absbyai-editroute/storage.json` (`--help`, `WV-05`, `DS-41-setup`). Never touch `SRM-JV-R5*`, `DS-107`, `DS-40-codex`, `DS-98-blind`, `RO-39`, `WV-03`, `WV-05`, `WV-06`, or any raw shoot folder. Report the gate output, what you removed, backups used, and free GB on both drives.
