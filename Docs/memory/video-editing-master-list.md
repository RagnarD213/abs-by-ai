---
name: video-editing-master-list
description: "Since 2026-09-16 all owed video-editing work lives in Handoffs/video-editing/00-MASTER.md (one job doc each, Claude + Codex prompts); Dan picks the order"
metadata: 
  node_type: memory
  type: project
  originSessionId: 666f8ca0-4f5d-4407-9544-2f48c8a523ba
  modified: 2026-09-16T20:03:27.069Z
---

Dan's master list of video-editing work is `Handoffs/video-editing/00-MASTER.md` (built 2026-09-16), with shared rules in `00-RULES.md` and one job doc per video: RA (raw short-form ads), DS (dedicated shorts), RO (organic long-form), RX (footage audit), SL (shorts from long-forms), AV/AS (ad verticals/squares). Each doc has a Claude and a Codex starter prompt. The pinned page https://claude.ai/artifact/1r1T8Znf96XH24zHZhybHs reads live status from its `jobs` db collection; `Handoffs/video-editing/jobs.json` is the git copy, and `scripts/edit-queue/queue.py` changes both (states ready/needs/blocked/in_progress/delivered/finalized/uploaded; procedure `.claude/skills/_shared/edit-queue/README.md`). Dan's rule 09-16: finalized = when he says so; uploaded = after /ad-setup or /video-setup uploads it. queue.py also uploads `Abs By AI automation/edit-queue-status.json` to Drive via rclone (file id 1RX-GqepEKqB1LgJqJFRyRU2lOJMnRFgg); the page reads it through the Google Drive connector every minute, so Codex and Grok Bot (which runs local commands too) update the page live without Claude. The db mirror is written by Claude sessions only. It superseded the J1–J18 ad-variants queue.

**Why:** Dan wanted one organized thread of every editing task so he can fire handoffs when the machine has room and re-prioritize (he may move dedicated shorts and short ads up).

**How to apply:** when a new video goes final (e.g. Muhammad's Ads 8/9/13/15, Zeeshan's batch, any RO job), add its AV/AS or SL row and doc there instead of writing a standalone handoff. Don't write handoffs for work Codex or an Upwork editor holds. Full 8/28 + 7/8 roll transcripts: `/Volumes/Extreme/_edit_work/_transcripts-828-full/`. The 8/28 rolls hold several scripts each, so earlier first-100-second maps missed most of them. Related: [[codex-owns-non-core-work]], [[editor-deliveries-filing]].
