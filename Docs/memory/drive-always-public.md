---
name: drive-always-public
description: Dan 2026-09-24: everything Claude puts on Google Drive gets "anyone with the link can view" at creation; never leave it private
metadata:
  type: feedback
---

Every file or folder Claude creates or uploads on Google Drive is shared "anyone with the link, viewer" immediately, before the link goes anywhere. Never leave a work file private.

**Why:** Muhammad was blocked on B-roll links (09-24) because the "Muhammad Shorts Batch - Extra Assets" folder was private. Dan: private files slow everything down.

**How to apply:** after any Drive create/upload, POST permission {"type":"anyone","role":"reader"} (the Drive MCP share_file only takes an email, so use the Drive API with rclone's token, or share the parent folder, which children inherit). The rclone shared client_id rate-limits hard: space calls ~6s apart and retry on 403 Quota. Exception: plainly personal/sensitive docs (API keys, EIN, legal, recovery codes) stay as they are. See [[drive-backup-capability]].

**Client work too (Dan, 2026-11-26):** the same default applies to review copies and finals for client jobs (SRM clients such as Joint Vigor's Eric): make them "anyone with the link, viewer" AND share with the client's email as a viewer, by default, without asking. Dan: "Always do that by default for client work going forward." The Drive MCP `share_file` worked for `anyoneWithLink` but returned "The caller does not have permission" for a named external email (2026-11-26); for an email grant use the Drive API with rclone's token (POST permissions type user, role reader, sendNotificationEmail=false). Still never send the client any message: Dan sends those.

**Never put internal or unreviewed work in a client-shared folder (2026-11-26):** the R26 build brief reused the Joint Vigor folder that is public and shared with Eric, and a new unreviewed film started uploading there (stopped before anything landed). Each internal round gets its own unshared folder; only the version Dan chose to send goes in the client folder.
