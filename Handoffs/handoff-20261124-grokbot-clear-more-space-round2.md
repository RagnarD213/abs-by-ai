# Clear more space on the M6 internal drive and the Extreme, round 2 (Grokbot, 2026-11-24)

Follow-up to [handoff-20261124-m6-extreme-space-cleanup.md](handoff-20261124-m6-extreme-space-cleanup.md) (round 1, done by Grokbot tonight: WV-07 src/key, WV-03 older rounds and RO-41 extras deleted after Drive match) and [handoff-20261124-grokbot-agy-ds107-workdir-space.md](handoff-20261124-grokbot-agy-ds107-workdir-space.md) (Claude cleared ~24 GB of ad scratch on the Extreme so the AGY-DS107 gate passes).

Dan's authorization: do the whole job, including deleting the folders below once each has a verified second copy. Do not ask Dan again. Passwords and Drive logins are yours (vault); never write secrets into repo files. Drive sharing: anyone with the link can view.

## State, measured 2026-11-24 about 8 PM Central
- M6 internal: **38 GB free** (926 GB disk). `~/Projects/_edit_work` = 368 GB: SRM-JV-R5 206, SRM-JV-R5-head 42, WV-05.moved-to-m2-20261119 39, DS-98-blind 27.5, WV-07 22, WV-03 9, SL-36 6, SRM-JV-R5-clean 5.
- Extreme: **43 GB free** of 3.6 TB (99% full). `_edit_work` biggest: SRM-goldenroots-jointvigor 571, WV-03 227, RO-39 227, kit9x16 160, DS-109 159, DS-106 124, DS-107 103, DS-108 101, DS-40-codex 83, RO-15 82, RO-22 81, wv01-edit 68, RO-23 61, SHOOT-20261023 50, RO-32 43, DS-98-blind-storage 41, DS-34-r2-keycache 34, WV-06 34, REALDEMOS-B08 24.
- Seagate (Expansion) is in Austin with the M2, not mounted. So the second copy for every deletion is **Google Drive** (size + SHA-256 or Drive md5 match) or the M2 (file count + bytes + hash on the finals).
- Edit cap: SRM-JV-R5 (Joint Vigor, Claude) is the only active job and holds the slot. AGY-RO24 is waiting on Dan.

## Targets
1. M6 internal: **at least 100 GB free** (so any 15 GB edit passes the 80 GB reserve without waiting).
2. Extreme: **at least 150 GB free**.
Stop as soon as both are met; do not delete more than needed.

## Order of work (safest and biggest first), delete only after the check named

### A. Extreme (biggest wins, mostly duplicates)
1. `SRM-goldenroots-jointvigor` (571 GB): compare with the Joint Vigor copy on the M6 (`~/Projects/_edit_work/SRM-JV-R5*`, `SRM-goldenroots-jointvigor` 1 GB there) and the M2/Drive. Delete only the part that is a verified duplicate (file count + bytes + hashes, or the client's original footage confirmed in Drive/the client delivery). Client footage that exists nowhere else stays. Joint Vigor is active: never touch anything SRM-JV-R5 reads.
2. Finished and waitlisted setups DS-106, DS-107, DS-108, DS-109 (about 490 GB together): keep approved master, covers/thumbnails, setup receipt and `RESUME.md`; delete intermediates (graded copies, segment/key caches, frame dumps, review exports) after confirming the master is in Drive. **DS-107 is the control for the Antigravity blind test: keep its inputs, cut, and master untouched.** Delete nothing in DS-107 beyond clearly regenerable frame dumps, and only after the DS-107 test is no longer running (check the test handoff).
3. Intermediates, after confirming each finished master exists in Drive: `RO-15` 82 (waitlisted Dec 23), `RO-22` 81 (technical hold, Dan's as-is/repair decision is open in `Docs/DAN_DECISIONS.md`: keep its final and `setup/RESUME.md`), `RO-23` 61 (queued Nov 22), `RO-32` 43, `wv01-edit` 68, `DS-98-blind-storage` 41 (only if Dan has not picked from DS-98 Round 2; otherwise ask in chat first), `DS-34-r2-keycache` 34, `REALDEMOS-B08` 24, `kit9x16` 160 (keep every `*-master` folder and `approved_crops`; the skill `shortad-from-longform` references it, so never delete the whole folder), `ads234-8-14`, `ad1-8-14`, `SL-13` 15, `SL-12` 12.
4. Raw shoot folders (`SHOOT-20261023` and the dated shoot folders) last, and only if a matching SHA-256 copy is on Drive or the Seagate. Normally leave them.

### B. M6 internal
1. `WV-05.moved-to-m2-20261119` (39 GB): delete after proving the M2 copy matches (`ssh m2`, file count + total bytes, plus hashes on the finals).
2. `SRM-JV-R5-head` (42 GB) and `SRM-JV-R5-clean` (5 GB): only when Joint Vigor R5 is delivered and Claude says the job is finished. Not before.
3. `DS-98-blind` (27.5 GB): not before Dan picks a winner from the Round 2 films (waiting on him). Then back up the winner and delete the rest.
4. `WV-07` (22 GB, Round 3 is with Dan) and `WV-03` (9 GB, VSL revisions on the M6): keep what remains.
5. Clean the three stale reservations in `~/.absbyai-editroute/storage.json` (`--help`, `WV-05`, `DS-41-setup`, 43 GB committed). Use a supported command if `editroute.py`/`storage.py` has one (`storage.consume(job)` exists); otherwise back the file up first, remove only those three keys, validate the JSON. This changes the gate math the most: it removes 43 GB of phantom commitments on the internal drive.

## Never touch
`SRM-JV-R5*` (active), `DS-40-codex` (locked reference), `RO-39` (in progress on M2), `WV-06`, `WV-05` (on Extreme), `AGY-RO24`, `AGY-DS107`, `DS-107` masters and inputs, anything listed in `.claude/skills/_shared/jobarchive/keep.txt`, AI clip sources (`rev/gen2*` style folders, anything under the clip library or `07 AI Generation Source Archive`), approved masters, and any folder a running process, the render queue or the edit cap uses (`python3 .claude/skills/_shared/renderq/renderq.py status`, `.../editcap/editcap.py status`, `lsof +D <folder>`).
Before each delete also run `grep -R "<folder>" .claude/skills Docs scripts` and keep anything a live skill, catalog or script points at.

## Method
1. Build a delete manifest first: folder, size, what stays, where its second copy lives, and the check (size/hash/count). Save it to `Docs/SPACE_CLEANUP_ROUND2_MANIFEST_20261124.md`.
2. Execute the manifest top to bottom, re-measuring free space after each folder (`df -h ~ /Volumes/Extreme`). Stop when both targets are met.
3. Use the least destructive removal that frees space. The Extreme keeps trashed files on the same volume, so empty the Trash if you used it.
4. After finishing, run `python3 .claude/skills/_shared/renderq/renderq.py workdir TEST-SPACE --need 15 2>&1 | tail -2` (dry check: remove any folder it creates) to prove both drives pass, and record the result.

## Done =
Reply in chat and write `Docs/SPACE_CLEANUP_ROUND2_RECEIPT_20261124.md` listing every folder or reservation removed, its size, where the verified second copy is and the check used, what you deliberately kept and why, and free GB on both drives. Push with `scripts/git/safe-push.sh -m "Space cleanup round 2 receipt" -- <files>`.

## Starter prompt for Grokbot (self-contained)
> You are working on Dan Rose's Mac (the M6) in the project folder `/Users/danrrose/Projects/Claude/Projects/Abs By AI`. Read `Handoffs/handoff-20261124-grokbot-clear-more-space-round2.md` and do the whole job. Dan has authorized deleting the folders it lists once each has a verified second copy (Google Drive with size and SHA-256 or md5 match, using your own Drive login, files set to anyone-with-link can view; or the M2 with matching file count, bytes and hashes). Goal: M6 internal at least 100 GB free (now 38) and the Extreme at least 150 GB free (now 43). Start with the Extreme: the 571 GB `SRM-goldenroots-jointvigor` if a verified duplicate, then intermediates of finished DS-106..109, RO-15, RO-23, RO-32, wv01-edit and kit9x16 (keep masters, receipts, `RESUME.md`). On the M6: clear the stale reservations in `~/.absbyai-editroute/storage.json` and delete `WV-05.moved-to-m2-20261119` after matching it to the M2. Never touch `SRM-JV-R5*`, `DS-40-codex`, `RO-39`, `WV-06`, `WV-05` on the Extreme, `AGY-DS107`, DS-107 masters/inputs, AI clip sources or approved masters; skip `DS-98-blind` unless Dan has picked a winner. Write the manifest first, then execute, then report free GB on both drives.
