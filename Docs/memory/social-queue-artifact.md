---
name: social-queue-artifact
description: Social Queue artifact page shows everything scheduled in Blotato by platform plus finished posts waiting for a slot; refresh recipe
metadata:
  type: reference
---
Social Queue artifact: https://claude.ai/artifact/6nsN9KPLAQAUCcXqRGvCXa (made 2026-10-03 at Dan's request, modelled on the Edit Queue). Page `output/social-queue-artifact/index.html`, data `queue.json` beside it.

**How to apply:** after any Blotato queue change (new posts, deletions, a waiting item queued), run `python3 scripts/blotato/queue_artifact_data.py` (reads the live schedule, all pages) then republish the same file path with `files: {"queue.json": ...}` and the `url` above. The "Not finished yet" list is hand-kept in the PIPELINE constant in that script. The waiting list comes from `scripts/blotato/studio27_plan.json` minus `studio27_state.json`; a new batch with unqueued items needs its own plan/state added to the script. Blotato plan cap is 200 scheduled posts (code 20010). Related: Edit Queue [[edit-queue-artifact-is-working-list]].

**Automation (Dan, 2026-10-03):** scheduled task `social-queue-daily-refresh` runs daily 6:20 AM local (Claude, needs the app open). Daily: `queue_artifact_data.py` then republish the artifact. Mondays first: `scripts/blotato/queue_topup.py --apply` fills Blotato to the 200 cap from the internal queue (studio27 plan minus state). Dan authorized the weekly Blotato writes. A different batch with unqueued items must be added to queue_topup.py and queue_artifact_data.py or it is invisible to both.
