---
name: review-pages-retire-idle
description: Review-page login services are retired after 3 idle days (max 40 active); a dead old review link is restored with review_retire.py --restore PORT
metadata:
  node_type: memory
  type: project
  originSessionId: 928bf908-793e-4e53-8aec-116d45fee46a
  modified: 2026-11-02T23:37:39.831Z
---

On 2026-11-02 the Mac froze twice (once during boot) because 136 `com.absbyai.review.PORT` launch agents had piled up and launchd ran out of file handles ("Too many open files", errno 24), so it could not start any process.

`.claude/skills/_shared/review_retire.py` now runs every 30 minutes from `~/bin/claude-cleanup.sh`: reviews idle more than 3 days are retired (plist moved to the review's own folder as `launchagent.plist.retired`, page kept), at most 40 stay active, and ports linked on the board are always kept.

**Why:** an uncapped agent count can freeze the whole Mac again.
**How to apply:** if Dan says an old review link no longer opens, run `python3 .claude/skills/_shared/review_retire.py --restore PORT`. Never raise the cap above ~60 without checking launchd for errno 24 errors. Full backup of the 135 plists from that day: `~/Library/Application Support/AbsByAI Reviews/_agent-backup-20261102/`.
