---
name: setup-encodes-low-priority
description: "Upload/setup platform copies never wait for a build slot; run nice -n 20 on the VideoToolbox hardware encoder (Dan, 2026-09-30)"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 74341f1e-ae06-4d78-85e1-ddb3da3a0bea
  modified: 2026-09-30T20:33:12.886Z
---

When a /video-setup or /ad-setup task needs a platform copy (Blotato 400 MB copy, TikTok cover-first copy) and the Mac is already busy with two or more video builds, run the encode anyway: `nice -n 20`, `-hwaccel videotoolbox`, `-c:v h264_videotoolbox`, audio stream-copied. Do not wait for a slot.

**Why:** On RO-05 (2026-09-30) other sessions held 3 to 4 builds at load ~300 for over half an hour; waiting could have taken hours. The hardware media engine barely touches the CPU the two-build cap protects. Dan: agreed, make it the standard for upload and setup tasks.

**How to apply:** Setup/upload copies only. Editing renders, QC, transcription and x264 encodes still obey the two-build cap. Written into `_shared/VIDEO-RULES.md` and `video-setup/SKILL.md`. Related: [[blotato-false-failure-large-video]].
