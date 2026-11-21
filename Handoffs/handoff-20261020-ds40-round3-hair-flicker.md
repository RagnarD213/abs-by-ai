**CONTENT SFC. Task name: `Bill Maher Fat 90-Year-Old SFC R3`. Start now.**

# Bill Maher Asks If You've Ever Seen A Fat 90-Year-Old. He's Right. (DS-40): reduce fine-hair flicker

Recommended model: **GPT-6 Sol, high**. This is a new 10-second calibration round, not the full Short. Dan returned the following morning and requested another material hair-key revision, so the standing round rule moves it to a fresh task. Keep the originating task pinned; Dan unpins it. Do not begin the full edit before he accepts the calibration.

## Read first

- `AGENTS.md`, `.claude/skills/_shared/VIDEO-RULES.md`, `Handoffs/video-editing/00-RULES.md`.
- `Handoffs/video-editing/DS-40-bill-maher-asks-if-youve-ever-seen-a-fat-90-year-old-hes-rig.md`.
- `Handoffs/video-editing/ds40-codex-r3-plan/decisions.json` for exact Dan feedback, approvals and hashes.
- `Handoffs/video-editing/ds40-codex-r2/README.md`, `audit-INDEPENDENT_AUDIT.md`, `receipt.json`, `player-repair-20261020.json`.
- Codex `$long-form-content-edit` for source, key, audio and color; `.claude/skills/shorts/SKILL.md` for the eventual vertical finish. No captions or graphics in this sample.

## Dan's latest request and locked choices

Dan: "Okay let's go with the balance voice." This is R2 **B, Balanced**, now approved. He then described distracting flickering where the background shows through his moving hair and asked whether it can be made cleaner. The warmer color remains selected from the preceding round. Full exact words are in decisions.json. The screenshot composer contained a different unsubmitted audio draft; it is not authority. Use the explicitly selected B.

Re-hash these before starting; never alter the locked source files:

| Item | Path under `/Volumes/Extreme/_edit_work/DS-40-codex/round2/` | SHA256 |
|---|---|---|
| Approved voice | `voice-balanced.wav` | `089264175840f8aa4956d98a7e8bd82d93bd8c1dcee73493d4733ae224df2a6f` |
| R2 B comparison | `review/media/balanced.mp4` | `622ec8a71b344a13496277ce3e7c3de17a8229d6d7d71bcea1084256273d0100` |
| Grade recipe | `grade.py` | `d6d2c4cd854088f4383649f4b9929631a7f2c3d409c8dd08d1db41a916f600ce` |

Keep the warm grade, body/arm matte and widest native framing. The portrait camera only recorded head to waist plus laptop. It cannot show legs. Keep the laptop for this edge-inspection sample. Full edit later crops it as appropriate.

## Existing work and exact source

Build only in a NEW `/Volumes/Extreme/_edit_work/DS-40-codex/round3/`. R1 and R2 remain available. Do not run a script in another session's build directory. Claude's parallel competition is authorized but separate; do not read or modify its build.

Read-only raw source:
`/Volumes/Extreme/10:15 dan rose fitness shoot - green screen, outdoor shorts, outdoor b roll, studio backdrop/C1730.MP4`

Use the same continuous interval, 1413.0116-1423.0216 seconds, 300 frames at 30000/1001. Native auto-oriented decode is 2160x3840; no extra transpose. Sony S-Cinetone is BT.709, not log. Reuse existing roll sidecar, left lav already established. Words begin "That's why you need to treat your belly fat as an emergency" and end "to see how awesome it will be." There are no edit joins. No full take selection or final mark-used has occurred.

R2 recipes are in its external directory and archived under `Handoffs/video-editing/ds40-codex-r2/`: key_v2.py, r1_key.py, render.py, grade.py, package.py, page.py. Read before copying into round3. render.py uses script-relative output paths but hardcodes the raw source. package.py may depend on R1 audio/reference assets. Preserve exact B audio, not the older A default. Do not execute archive scripts in place.

## The problem to solve

R2 improved green/gray fringe and the silhouette, but Dan still sees flicker within semi-transparent fine hair. The independent auditor noted residual purple/gray top-right strands near 8-9 seconds. Review especially 1-3 seconds, 4-6 seconds and 7.9-9.1 seconds at normal speed and enlarged. Judge both edge and internal gaps, not only a contact sheet.

Current method fits a green-screen color field separately each frame, estimates alpha against the nearest opaque foreground, refines a hair zone with a guided filter, then averages aligned previous/current/next alpha. Optical flow is computed at half native resolution. The averaging rejects alpha differences over about .22; nearest opaque hair colors and hard core/distance classifications can also change abruptly between frames. These are hypotheses for the observed flicker, not proved causes.

Suggested first experiments, inside the same source interval:

1. Diagnose a short moving native-resolution loop around the worst hair motion. Separate changing alpha from changing reconstructed edge color. Stabilize the screen fit across the short shot; test robust local hair-color estimates instead of a different nearest opaque pixel on each frame.
2. Test stronger motion-compensated consistency only in fine semi-transparent hair, with occlusion checks and soft thresholds. A wider temporal neighborhood or better local alignment may help. Avoid simple frame blending, a dark helmet, missing strands, smeared details and motion trails.
3. Compare R2 and candidates on identical light and dark fields, at the same crop and time. Choose by moving native pixels, not a low-resolution video-model score. Then render the best 10-second wide sample with approved Balanced audio and warm grade. Include a matched enlarged R2/R3 hair comparison.

Do not promise these experiments will eliminate every strand artifact. Retain natural texture. If no meaningful improvement is possible without damage, state that honestly and show the best comparison.

## Checks, audit and delivery

- Check buildcap before any render or gate. Maximum two machine-wide builds. Raw footage remains read-only.
- All numeric checks remain unchanged. R2 B passes speech decay and variation but still FAILS comb/resonance and tone. Dan selected its sound; do not reopen the voice choice or overprocess it to chase those numbers.
- R2 exact A full gate: 37 PASS, 1 FAIL (audio), 1 NOT MEASURED (watch), 18 declared N/A. B has an exact audio gate. A truly continuous clip has zero boundaries and exposes the shared watch gate's nonzero-boundary requirement. Do not invent boundaries or claim an all-pass result.
- New exact MP4s need their own audio and delivery gates, hash-bound watch scan and fresh independent motion audit. Authorize a fresh Sol reviewer explicitly. Audit moving fine-hair opacity, edge color, glasses, arms and hands, preserved detail, ghosting and audio sync. Standalone stills are insufficient.
- User hair rejection and voice approval are recorded in corpus entry `ds40-codex-r2-hair-flicker-20261020`. `key:hair_temporal_edges` remains an unimplemented measurement. Do not treat a clean watch sheet as proof it passed.
- Deliver a 10-second wide preview, 540p phone copy and moving hair comparison. Show only the new hair decision; audio B and warmer color are locked. No covers, full edit, upload for publication or scheduling.
- R2 review is http://127.0.0.1:9021/. Keep it intact. Choose an unused managed port for R3. Start with `.claude/skills/_shared/review_server.py PORT DIR`, verify HTTP 206, muted playback/seek and Reload video, then leave paused.
- The shared review tool now injects recovery after idle/sleep/stalls and a Reload video button. It retains position, rate, volume and mute. Local cached media and the launchd service survive the chat, drive disconnection and next Mac login. New services receive the helper automatically. Do not use a temporary server.
- Public Drive R2 folder: https://drive.google.com/drive/folders/1K52GrFaKbqWnoTORTR9bfdQt__IjHCX5. A/B/C, hair comparison, dark check and phone are public. Rclone hit a shared-client quota on Oct19; the connected Google Drive upload tool accepts an absolute local file path and completed the uploads. Use that fallback if needed, set anyone-with-link sharing and verify permissions.
- Record review state in master/jobs via queue.py; Codex commits it. If rclone is blocked, `EDIT_QUEUE_NO_DRIVE=1` still writes the status export, which the connected Drive update_file tool can replace in existing file ID `1RX-GqepEKqB1LgJqJFRyRU2lOJMnRFgg`. Read back to verify. Do not touch the paused Victory Dashboard.
- Commit/push named files with safe-push. Shared code changes must be pushed immediately. No media in Git. Preserve other sessions' entries.

## Current repair and costs

The Oct20 page failure was a stale browser video display. The server remained alive and all six cached movies matched originals. Reloading the source restored the picture. The underlying browser fault is not proven. Repair checked HTTP ranges, injected helper, retained playback state and silent full playback. Killing the owned server process verified automatic restart. No media was re-rendered. Balanced is now the initial player choice, and Download sample follows the selected option. Shared code commits include e38ccb2 and a180222.

External review charges: R1 $0.2491; R2 $0.0517; Oct20 player repair $0. No new generation. Subscription token usage unavailable. Any new paid review batch must be estimated in advance, with the standing $5 review approval threshold.

## Exact next action and starter prompt

Start now: rename the new task, read the decisions, verify the three hashes, copy only needed recipes into round3 and inspect the moving 7.9-9.1-second hair region before changing the key. Do not ask Dan to repeat his audio/color choice.

> CONTENT SFC. Name this task `Bill Maher Fat 90-Year-Old SFC R3`. Read `Handoffs/handoff-20261020-ds40-round3-hair-flicker.md` and execute it now. Keep the approved Balanced voice B, warmer color and wide framing. Reduce flicker in the semi-transparent moving hair, verify against R2 with an independent motion audit, and deliver another 10-second sample before starting the full edit. Use GPT-6 Sol at high effort.
