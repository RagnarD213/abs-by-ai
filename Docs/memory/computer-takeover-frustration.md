---
name: computer-takeover-frustration
description: Dan's machine getting hijacked by long browser/computer-use tasks interrupts higher-priority work — warn first, prefer cloud/background
metadata:
  type: feedback
---

Dan raised this on 2026-08-19: Claude Code "keeps taking over the computer and interrupting the more important work I'm doing." It was one of two reasons he was considering moving to a third-party harness entirely.

**Why:** long foreground sessions that drive Chrome or computer-use lock his machine for 20+ minutes at a stretch. He often needs Claude working AND needs his own computer at the same time, and today those are mutually exclusive. This is a real workflow cost, not a minor annoyance — it was enough to make him look at leaving.

**How to apply:**
- Say so explicitly BEFORE starting anything that will drive his browser or take over the screen, and give him the chance to defer it.
- Default long-running work that doesn't need his screen to cloud sessions (`claude --cloud "<task>"`, or the desktop app's "Continue in" menu) or to background execution.
- Cloud sessions clone from GitHub, so push first. They cannot reach his real Chrome logins (Google Ads, App Store Connect, Play Console), local media, the iOS simulator, or `~/.absbyai-secrets.env` — those genuinely have to stay local, and that's the honest boundary to tell him.
- Scheduled work (morning brief, sweeps) belongs in cloud Routines, not local scheduled tasks.

Related: [[autonomy-credentials-framing]], [[railway-deploy-workflow]]
