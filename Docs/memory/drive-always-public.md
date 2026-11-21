---
name: drive-always-public
description: Dan 2026-09-24: everything Claude puts on Google Drive gets "anyone with the link can view" at creation; never leave it private
metadata:
  type: feedback
---

Every file or folder Claude creates or uploads on Google Drive is shared "anyone with the link, viewer" immediately, before the link goes anywhere. Never leave a work file private.

**Why:** Muhammad was blocked on B-roll links (09-24) because the "Muhammad Shorts Batch - Extra Assets" folder was private. Dan: private files slow everything down.

**How to apply:** after any Drive create/upload, POST permission {"type":"anyone","role":"reader"} (the Drive MCP share_file only takes an email, so use the Drive API with rclone's token, or share the parent folder, which children inherit). The rclone shared client_id rate-limits hard: space calls ~6s apart and retry on 403 Quota. Exception: plainly personal/sensitive docs (API keys, EIN, legal, recovery codes) stay as they are. See [[drive-backup-capability]].
