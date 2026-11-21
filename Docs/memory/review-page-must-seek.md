---
name: review-page-must-seek
description: Review pages must be served by review_server.py so Dan can drag the video timeline; python http.server cannot seek (Dan 2026-10-16)
metadata:
  type: feedback
---

Dan could not drag the video slider on the RA-15 round 4 review page: it was served with `python3 -m http.server`, which ignores HTTP byte ranges.

**Why:** a click on the timeline does nothing without a 206 response. The rule existed (VIDEO-RULES, PRE-RENDER-APPROVAL) and was missed.
**How to apply:** serve every review page with `python3 .claude/skills/_shared/review_server.py PORT DIR`; check `curl -r 0-99` returns 206; seek a video in the browser before sending the link. The project hook `scripts/review/hook_no_plain_http_server.py` now blocks `http.server` commands. See [[review-page-what-i-decided]].
