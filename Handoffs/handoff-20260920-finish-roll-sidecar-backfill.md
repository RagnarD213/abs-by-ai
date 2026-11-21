# Handoff: finish the footage sidecar backfill (2026-09-20)

## Goal

Finish indexing the remaining raw footage so editors can search what Dan says and what appears on screen without rechecking every clip. The tool and 8/28 main-camera pilot are already complete. This task is a continuation, not a rebuild of the tool or an edit of any video.

## Current state, checked 2026-09-20

- Tool: `.claude/skills/_shared/rolls/roll_sidecar.py`, README and tests beside it. Code was pushed to `main` in commit `aacb4bb` on 2026-09-18.
- The 8/28 main-camera pilot indexed 42 clips, 151.093 minutes. It harvested 3 existing transcripts, ran Whisper on 24, and indexed 15 silent or unresolved-lav clips visually. Gemini descriptions cost an estimated $0.037984. All three required real search examples were checked against frames, including the front vacuum candidate C1677 at 8.0-13.0 seconds, passed to the DS-04 task owner.
- The local mirror currently contains 284 sidecars total. `roll_sidecar.py verify` reports 284, 0 warnings, 0 errors. The three synthetic tests pass. Total Gemini cost recorded in those sidecars is an estimated $0.278432, including the pilot. These are calculated token charges, not a provider invoice.
- The background process is no longer running. Its log stopped on 2026-09-18 at 22:28 CDT during the 8/3 shoot. No detached `screen` session exists. The cause of that stop is unknown; do not assume the batch finished.
- The log is `/Volumes/Extreme/_edit_work/roll-sidecar-backfill-20260918.log`. It shows the 8/14 folder completed with status 1, then started 8/3. It has no completion line for 8/3 or later roots.
- Existing drive sidecars are beside the clips. The text-only mirror is `Media/footage-index/`, which is gitignored because the repository is public. Do not commit sidecars, transcripts, or contact images.

## Four logged failures

1. In the 8/14 shoot, `EDITED LONGFORM 8-20-26/abwheel-17-dollar-ab-wheel/AUDIOFIX_ab-wheel-beats-every-crunch.mp4`: Gemini returned extra JSON data.
2. In the same edited-export folder, `MSTYLE_ab-wheel-reproduction.mp4`: Gemini JSON had an unterminated string.
3. In the same edited-export folder, `REVIEW_720p_MSTYLE.mp4`: Gemini JSON had an unterminated string.
4. In the 8/3 shoot's `main camera`, `C1579.MP4`: Gemini returned an empty or invalid JSON response.

The first three are finished edited exports inside a shoot directory, not raw camera rolls. Do not modify or try to repair those video files. Exclude edited-export folders from the raw-roll inventory unless a separate use case explicitly calls for them. C1579 is a real source roll and should be retried. The JSON errors point to description-response parsing, not proven damage to the video files. Diagnose before changing code or retrying paid calls.

## Exact next actions

1. Re-read `.claude/skills/_shared/VIDEO-RULES.md`, this handoff, the original `Handoffs/handoff-20260918-roll-sidecars-footage-index.md`, `AI_COORDINATION.md`, and the tool README. Check Git status and do not overwrite another session's changes.
2. Inventory the intended raw footage folders and compare their real video files with the mirror by content key. Do not use a broad recursive shoot root that includes `EDITED LONGFORM` or other finished exports. Recalculate the remaining clip count and Gemini estimate before the next description batch. The original full-backfill estimate was about $0.48 at the pilot rate, with a $2.22 conservative ceiling, but the actual remaining scope must be measured afresh.
3. Diagnose C1579's empty Gemini response. Make the description step retry a bounded number of transient empty or malformed responses, while logging attempts and preserving recorded spend. Add a test for the failure. Do not change any gate, threshold, master, or footage filename.
4. Retry C1579, then resume only unindexed raw rolls. The `build` command is content-key idempotent, so completed clips should be skipped. Harvest existing transcripts from `/Volumes/Extreme/_edit_work/` before Whisper. Work through the remaining 8/3, 7/8, welcome-video, GoPro, screen-recording and asset-library folders listed in the original handoff. Include supported Insta360 `.insv` sources, not tiny `.lrv` previews. Do not index the quarantined asset-library folder 08.
5. Keep the worker low priority and outside the edit queue. Check `python3 scripts/edit-queue/dispatcher.py status` before launch. The queue must show 0 claimed jobs from this task. The tool waits when two other video builds are active. Use a persistent supervisor with a clear log and confirmed running process; the prior detached `screen` process stopped without a final status.
6. At completion, prove the expected raw-roll count equals the indexed content-key count, list any genuine exceptions, run the tool tests and `verify`, and repeat representative transcript and visual searches with the source drive treated as offline. Report actual estimated Gemini charges from the sidecars. Confirm no sidecars entered Git.
7. Commit and push only any necessary tool/test/README changes, plus this handoff's normal index cleanup if in scope. The footage index is tooling only, so no video upload or absbyai.com deployment is needed. Re-read the coordination board before closing your entry.

## Guardrails

- Never edit, rename, move, re-encode, or delete source footage or finished masters. Do not touch video gates or thresholds.
- Do not claim an edit-queue slot. Respect the two-build machine cap. `dispatcher.py status` may count active Whisper or ffmpeg work as an external build for safety; that is not a claimed queue job.
- Do not commit anything from `Media/footage-index/` or the Extreme drive. The public repository must contain only code and small text instructions.
- State the Gemini estimate before any new batch. Keep the session's actual and projected cost below the standing authorization, and ask first if any single batch is projected above $15 or session spend above $25.
- The original `Handoffs/README.md` and `AI_COORDINATION.md` entries still describe the 2026-09-18 work as unexecuted. Replace those stale pointers with this continuation when preparing the new task, preserving other sessions' concurrent edits.

## Ready-to-paste starter prompt

Read `Handoffs/handoff-20260920-finish-roll-sidecar-backfill.md` and finish the raw-footage sidecar backfill. First diagnose the stopped 2026-09-18 run and C1579's invalid Gemini response; exclude the three finished edited exports from the raw-roll scope. Recalculate the remaining clip count and Gemini estimate, then resume idempotently in a persistent low-priority background job without claiming an edit-queue slot. Verify every intended source roll, the local mirror, tests, searches with the drive offline, and total cost. Do not touch footage, masters, gates, thresholds, or file names. Never commit sidecars. Commit and push only necessary tool or test changes and the small handoff-index cleanup.

Recommended model and effort: Codex GPT-5.6 Sol, High.
