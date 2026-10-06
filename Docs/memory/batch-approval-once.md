---
name: batch-approval-once
description: For batch jobs (many deletes, edits, posts) ask Dan once for the whole batch with a count, never per item
metadata:
  type: feedback
---

Ask Dan once for the whole batch, stating the count, never per item.

**Why:** 2026-09-25 he was prompted 37 times for 37 Blotato schedule deletes and called it ridiculously annoying. Also recorded in AGENTS.md.

**How to apply:** pre-approve the tool in `.claude/settings.json` (never the publishing one) or get one yes for the batch, then run it. See [[bias-toward-action]].
