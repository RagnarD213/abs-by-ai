---
name: drive-backup-capability
description: "Claude can back up large footage folders to Dan's Google Drive with rclone; how to run and verify it, and the shared-client_id quota trap"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4cd4ccff-3c2f-4ffa-add3-376a0bbb4907
  modified: 2026-09-13T15:15:00.189Z
---

Claude can copy arbitrarily large local folders to Dan's Google Drive and prove the copy
is real. Set up 2026-09-11; first use was the 8/28 shoot (259 files, 286 GB).

**Tools, both already in place:**
- `~/bin/rclone` — remote `gdrive` is authorized against danroseconsulting@gmail.com.
  Not from Homebrew (this Mac has none); it is the official static binary, checksum-verified.
- `scripts/backup/verify-drive-copy.sh <local-dir> <drive-folder-id>` — MD5-checks every file
  and compares counts and total bytes. Exit 0 only on a full pass.

**Copy recipe.** Create the destination folder with the Drive MCP (it handles `/` in folder
names, which rclone treats as a path separator), then upload into it by id:

    caffeinate -i ~/bin/rclone copy "<src>" gdrive: \
      --drive-root-folder-id=<FOLDER_ID> --exclude ".DS_Store" \
      --transfers 4 --drive-chunk-size 128M \
      --log-file <log> --log-level INFO --stats 30s --stats-one-line

`caffeinate` stops the Mac idle-sleeping mid-transfer. Resumable — a dropped run picks up
from the last completed file.

⚠ **Set up a personal Google client_id before any further big upload.** rclone's shared one
hit `403 Quota exceeded ... Requests per minute` on the 8/28 run, failed 2 files, forced a
whole-job retry, and turned a 14-hour job into 32 hours (562 GiB of wire traffic for 267 GB
of data — the byte counter accumulates across attempts, it is not duplicate data). It is
also being retired during 2026. Recipe: https://rclone.org/drive/#making-your-own-client-id

⚠ **Never run the verify script mid-transfer** — it reports a false FAIL on an incomplete copy.

**Storage facts:** Dan's Drive is a 5 TB plan, ~4.5 TB free as of 2026-09-13. His raw shoot
folders live under Drive parent `1wyG_tWdUPnMsGYqrfluORcL2k8hWZIPD`. Roughly 770 GB of the
Extreme drive is irreplaceable (shoot footage + photo shoots); the screen recordings (631 GB)
and `_edit_work` scratch (664 GB) are reproducible and deliberately stay out of the cloud.

See [[repo-is-public]] before putting anything of Dan's in the repo itself.

Done so far: the 8/28 shoot (259 files, 286,123,768,096 bytes) → Drive folder `1gzGtstw-WGjo4fK4QL11UMbwST9YFw37`,
MD5-verified 2026-09-13 (PASS, 0 differences). Open question for Dan: the welcome-video first shoot (114 GB,
`/Volumes/Extreme/abs by ai welcome-video first shoot`) is the last irreplaceable folder with no second copy. Never run
the verify script mid-transfer (false FAIL).
