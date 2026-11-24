# M6 internal + Extreme space cleanup (Codex and Grokbot, 2026-11-24)

Dan's authorization: do the whole job, including the deletions listed below once their backups are verified. No asking Dan again.

## State (M6, 2026-11-24)
- M6 internal: 7 GB free; `~/Projects/_edit_work` = 408 GB. Extreme: 14 GB free of 3.6 TB (`_edit_work` 2.5 TB + ~1 TB raw shoot folders).
- No Google Drive desktop folder on the M6. Upload via Drive web/browser (Grokbot has the logins) or the M2 if it has Drive sync. Drive sharing: anyone with link can view.
- Seagate (Expansion) is in Austin with the M2; Dan is away. Seagate steps wait until he is back.

## Step 1: back up to Google Drive (keep-list only, no regenerable intermediates)
Per job: approved finals/masters, receipts, and irreplaceable sources. Verify each upload by size + hash.
- WV-07: `round2`, `film` (keep); source `src` (10 GB). Skip `key` (21 GB, regenerable).
- RO-41: `src` (11 GB), `cut`, `key`, `film`.
- WV-03: final + latest round (`round9`); older rounds not needed.
- DS-98-blind: after Dan picks a winner, back up the winner's folder; `footage` (16 GB) only if not already on Extreme/Drive.
- Extreme: for each of DS-106, DS-107, DS-108, DS-109: approved master + setup receipt only.

## Step 2: delete on M6 (only after Step 1 verified, and never SRM-JV-R5, which is active)
- `SRM-JV-R5-head` (42 GB) and `SRM-JV-R5-clean` (5 GB) when R5 is delivered.
- `WV-05.moved-to-m2-20261119` (39 GB) after confirming the M2 copy matches (file count + bytes).
- `WV-07/key` (21 GB) and `WV-07/src` (10 GB) after Drive verification and Codex confirms.
- `WV-03` older rounds, `RO-41/src` after backup. Expect about 120-145 GB freed.
Use `renderq.py`/`editcap.py status` first; skip any job in use.

## Step 3: delete on Extreme (after verification, never RO-39, WV-03, WV-05, WV-06)
- Check `SRM-goldenroots-jointvigor` (558 GB) against the M6 JV copy; delete only if a duplicate.
- Finished/scheduled setups DS-106..109 (~490 GB): keep masters + receipts, delete the rest.
- Intermediates after confirming finals are saved: kit9x16 160, DS-40-codex 83, RO-15 82, RO-22 81, wv01-edit 68, RO-23 61, _asset_library_stage 41, DS-98-blind-storage 41 (GB).
- Raw shoot folders last, and only if on Seagate with matching SHA-256.

## Step 4: Seagate (waits for Dan in Austin, on the M2)
Back up everything kept above to the Seagate with checksums (it corrupted copies 11-01 to 11-03; never the only copy). Jobarchive LaunchAgent handles idle finished folders.

## Done =
Receipt in `Docs/` listing each folder, backup location, hash check, GB freed, and free space on both drives.
