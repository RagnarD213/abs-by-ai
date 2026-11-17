# Finish the internal drives cleanup (leftovers), 2026-11-17

For Codex and Grokbot (either; Codex newest Sol, medium). Dan's authorization: the original handoff `handoff-20261117-clear-internal-drives.md` already covers every move below; no new approval is needed. Receipt to update: `Docs/INTERNAL_DRIVES_CLEANUP_RECEIPT_20261117.md`. Free space on 2026-11-17 15:45: M6 173 GB, M2 114 GB (goal was 250 GB each, not reached).

## Why this exists
Two steps ran longer than the Claude session could wait. Both have background jobs running that may already have finished; check before redoing anything.

## 1. M6 `~/M2-transfer/staging` (27 GB): verify the Seagate copy, then delete
- Copy runs over SSH into the M2 (the SMB route hung for six hours; do not use it): `rsync -a -e ssh staging/ m2:/Volumes/Expansion/_m6_staging_archive/m2-transfer-20261117/staging/`. Logs on M6: `/tmp/claude-501/m6-staging-ssh.log` (ends "copy done 0") and `/tmp/claude-501/m6-staging-ssh-verify.log` (checksum dry-run, ends "verify done 0").
- Delete `~/M2-transfer/staging` on M6 only when the verify log lists nothing but permission-flag lines (`.f...p...`), meaning no content, size or new-file differences. If the logs are missing, rerun both commands (second one: `rsync -anc --itemize-changes -e ssh ...`) from `~/M2-transfer`.

## 2. M2 test folders (about 28 GB): CHROMA-FABLE-TEST and GRAPHICS-FABLE-TEST
- A retry loop on the M2 runs `jobarchive.py run --approved CHROMA-FABLE-TEST,GRAPHICS-FABLE-TEST` every 2 minutes (log `/tmp/dl/ja-m2.log`) and was blocked by the Extreme cleanup's cleanup lock (a long jobarchive run on the M2). If the log says "moved", nothing to do. If the loop is gone, rerun the command once the other run exits. Do not edit `jobarchive.py`. Never move WV/GAT, JV, DS-98, RO-39, REALDEMOS-B04 or anything on the board as active.

## Finish
Update the receipt (free space per Mac, what was moved), push with `scripts/git/safe-push.sh`, and remove this entry from `Handoffs/README.md` OPEN.

## Starter prompts
- Codex: "Execute Handoffs/handoff-20261117-finish-internal-drives-cleanup.md." (newest Sol, medium)
- Grokbot: same sentence plus: the repo is on the M6 at /Users/danrrose/Projects/Claude/Projects/Abs By AI; the M2 is reached with `ssh m2`; the instructions above are complete.
