---
name: codex-image-batches-exhaust-subscription
description: "A large Codex image batch (about 150 generations in one day) used up Dan's ChatGPT subscription limit for three days; pace or route big frame batches before starting"
metadata:
  node_type: memory
  type: project
  originSessionId: c0133ff8-9ddc-4c28-9324-1a3c7bc0a44a
  modified: 2026-11-15T19:54:42.500Z
---

On 2026-11-15, round 5 of the Great Again T VSL (WV-03) generated START and END frames for 44 AI clip ideas on both
subscriptions. The Codex half (about 150 `codex-image.sh` calls at medium effort, counting retries and two character
portraits, on top of whatever other Codex tasks used that week) hit "ChatGPT subscription usage limit reached" at about
1:34 PM, resetting 2026-11-18 11:57 AM. That is the same subscription Dan's Codex setup and edit tasks run on, so the
batch blocked his other Codex work for three days. The Google subscription (Flow, Nano Banana Pro) made about 150
images the same day at 0 credits.

**Why:** the blind Codex-vs-Google rule ([[blind-google-vs-codex-images]]) doubles every frame, and nothing in the
image rules warns that the Codex side shares a usage limit with all of Dan's Codex work.

**How to apply:** before any batch of more than about 40 Codex images, tell Dan the count and that it draws on the
shared ChatGPT limit; work in film order so the important frames are made first; keep retries tight (lock static drift
with `framecheck/lockstill.py` before regenerating an END); and if the batch is large, say up front that the Codex half
may have to stop early and the Google pair go forward alone. This is my reading of what happened, not a rule Dan set;
ask him if he wants a hard cap. See also [[veo-subscription-first]].
