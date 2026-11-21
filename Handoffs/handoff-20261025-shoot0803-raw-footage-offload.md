# OPS: August 3 raw footage, Extreme to Expansion

Date: October 25, 2026. Task name: **August 3 Footage Offload**.
Recommended: **Codex GPT-6.1 Sol, high effort**, the newest supported stable GPT verified in the runtime catalog.

**Ready to start now for dependency checks and verified copying.** The approved full workout export and project/Extreme backup are complete. Nothing has been moved or removed by the editor. Source removal still requires every check below, including the final master's Google Drive copy.

## Authorization and start condition

Dan asked to confirm whether Arms & Shoulders Workout Only is the last edit from this shoot and, if so, provide a handoff to move the raw footage from Extreme to Expansion.

**Start source removal only after the approved RO-04 full file is assembled, checked, filed and backed up.** Check `Media/video-edits/RO-04/round5/finalization-state.json` is `completed`, then verify its actual canonical finalization manifest and project/Extreme/Drive copies. The export is now completed and its project/Extreme copies are verified. Readiness details: `Media/video-edits/RO-04/round5/finalization-state.json`; final hash `140fd719899dc17d9d8d4217326a73dbdba6150fb1012c89eae7105518f8b7df`. The offload task must confirm/copy the final master to Drive if setup has not yet done so, then complete fresh raw-file verification before removal.

This authorizes the verified move of this one shoot. It does not authorize changes to the global offload pause, unrelated shoots, paid plans, new credentials or deletion of edited content.

## Dependency audit

Read `Docs/SHOOT_20260803_EDIT_COMPLETION_AUDIT_20261025.md` and `Media/video-edits/RO-04/round5/shoot-0803-audit-evidence.json`, then refresh the live coordination board, jobs/master list and active handoffs.

RO-04 is the last original raw-footage film found needing completion. Salad, Home Budget, Spray Tan and all three Invest In Your Health parts are finalized/uploaded. RO-20C's stale R5 job note is superseded by its approved R6 full master and October 21 setup receipt. Zeeshan's Arms & Shoulders explainer and its SL-04 Shorts are finished.

SL-20/21/22 remain unbuilt, but their handoffs explicitly use the finished parent masters outside this raw folder.

**An older audio repair for eight Zepbound Update Shorts and eight Supplements Shorts remains unresolved. Do not mark it finished.** All 16 pre-fix MP4s exist in `Short-form video content/_pre-audiofix-20260902/`; clean picture masters remain in `claude edited long form content/02 - My Honest Zepbound Update/` and `03 - The Supplements I Actually Take/`. Preserve those files and reconcile the repair's future audio-source requirements before removing originals. The verified Expansion copy must remain usable if a raw excerpt is later required. This task does not repair or publish those Shorts.

If a new active cut still needs an Extreme original, copy and verify it but leave that original until the dependency clears. Do not interrupt another editor.

## Source and destination

Source: `/Volumes/Extreme/abs by ai 8:3 jeff chagrin shoot/`.
Move only these three raw subfolders, including all ancillary files, roll sidecars, indexes and proxies:
- `main camera/`
- `gopro 1/`
- `gopro 2/`

Leave `claude edited long form content/` and unrelated top-level content on Extreme.

Destination: `/Volumes/Expansion/Abs By AI Raw Footage/abs by ai 8:3 jeff chagrin shoot/`.
The archive already exists. Reuse and compare it. Never overwrite a conflicting file or delete unrelated archive content.

The raw-media/XML/proxy snapshot was 523 files and 178,642,661,117 bytes, about 178.6 GB or 166.4 GiB. Additional metadata was outside that suffix-based count and must also be copied. Build a fresh complete inventory.

Old nightly receipts recorded Expansion verification October 7 and Drive verification October 9, fingerprint `7df81db54eb9f4177b20c5fae0f5b72f975305ea9add3812ba7a1d864ed6a209`. Those historical receipts do not replace fresh verification.

## Execute

1. Read current AGENTS.md, VIDEO-RULES.md, `scripts/backup/README.md`, `nightly_footage.py` and the older nightly-offload handoff. Check the Expansion identity marker `.absbyai-footage-archive-id`, free space, resolved paths and active file handles. Inventory every current source file with relative path, size and checksum.
2. Copy missing files to the existing Expansion archive and existing Google Drive backup using `gdrive_backup:`. The existing Drive shoot name is `abs by ai 8／3 jeff chagrin shoot`; reuse the mapping in the nightly script. Use existing credentials without changing sharing. Compare every file against both copies by checksum, size and count. Confirm the source inventory stayed unchanged. Also verify the new RO-04 final master and matching SRT have their own independent backups.
3. Extreme is **ExFAT**, verified October 25. Unix directory symlinks will not solve old source paths on that drive. Write an archive-path mapping and restoration receipt. Preserve approved historical recipes and hashes byte-for-byte; future edits use a copied/adapted recipe with the archive path. Update only this shoot's active writable pointers or library indexes when needed. Never perform a blind global path replacement. Check shared clip-library references and the unfinished Shorts audio inputs. If a live reader cannot use the archive, retain its original until the owner finishes.
4. After all dependencies and copies pass, remove only the exact verified source files listed in the move manifest. Recheck checksums immediately before removal. Dan already authorized this verified move, so do not ask for the same removal approval again. Do not use broad `rm -rf` on the shoot root or remove unverified/conflicting/changed files. Keep the global `seagate-offload-paused` flag in place.
5. Leave `RAW_FOOTAGE_ARCHIVED.txt` in the original shoot root with actual archive/Drive locations, manifest hash, date, exact counts/bytes and restoration instructions. Record actual space recovered and any files left behind. Update backup state only through maintained tooling when its semantics match; never forge readiness flags or old verification fingerprints.
6. Save `Docs/SHOOT_20260803_OFFLOAD_RECEIPT_<date>.md`. Verify excluded edited content is unchanged, then close only this handoff. Do not relocate `_edit_work`, finished masters, review media, other shoots or chats.

Any failed copy, checksum or dependency check leaves the corresponding source intact. Report the exact blocker without calling the move complete.

## Starter prompt

Read Handoffs/handoff-20261025-shoot0803-raw-footage-offload.md. Name this task August 3 Footage Offload. After the approved Arms & Shoulders final full file is completed and backed up, recheck this shoot's remaining raw dependencies, preserve the older Shorts audio-repair sources, and move only the August 3 raw footage from Extreme to its existing Expansion archive. Verify every file and the Drive backup before removing any Extreme originals. Keep edited videos and other shoots untouched; Extreme is ExFAT, so preserve old recipes and document the archive paths rather than relying on symlinks.
