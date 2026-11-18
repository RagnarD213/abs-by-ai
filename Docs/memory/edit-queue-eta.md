---
name: edit-queue-eta
description: "11-18 Edit Queue page shows ETAs from eta.py (sessions report plan/steps; M6 launchd refresh every 10 min, no AI); Dan wanted fewer ETA asks in chat"
metadata:
  node_type: memory
  type: project
  originSessionId: aa831d8f-e75b-4944-9dba-9a8699543850
  modified: 2026-11-18T22:54:24.494Z
---

Built 2026-11-18 at Dan's request: he asked "ETA?" in chat many times a day, wasting tokens. Editing sessions now run
`eta.py plan/step/left/retry` (rule in VIDEO-RULES.md, "Report the ETA as you go"); M6 LaunchAgent
`com.absbyai.edit-eta` builds ranges for both Macs and uploads Drive `edit-queue-eta.json`
(id 1qTfELTbTmh6jFctW0SlCeDBp-WeBvx5J), which the Edit Queue page reads. Details: `.claude/skills/_shared/eta/README.md`.

**Why:** Dan chose a script-based ETA over half-hourly AI check-ins (no tokens, no overnight noise). He accepted
that ranges are rough during creative steps and tight in final renders; stalls show as "may be stuck".

**How to apply:** report steps in every edit, never post ETAs in chat unprompted, answer /eta from `eta.py show`.
The page's status file is Drive id 1eCS26zmSuh5weNasVTrAVpHO7xfg8rAU since 11-15 (the old 1RX copy was trashed).
Related: [[edit-queue-artifact-is-working-list]], [[two-mac-edit-routing]].
