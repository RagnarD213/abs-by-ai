AD. AI Took Job AD R3. Continue the existing edit and required review.

# State and next action

Use the exact `Media/codex-video-trial/skills/abs-edit-ad/SKILL.md` Dan named. Read current VIDEO-RULES and the coordination board. Work root stays `/Volumes/Extreme/_edit_work/ra16/`; R2 materials are in `round2/`. Do not start over. Recommended model: GPT-6 Sol, high effort.

The R2 look page is live at http://127.0.0.1:8976/ through the managed review service. It shows both opening formats, three colors, two crop pairs, the complete accelerated voice and its audio results. It deliberately withholds unreviewed asset previews. There is no full ad, no final master and no complete-candidate audit. Dan was asked asynchronously to pick color B/A/C and crop pair 1/2. At handoff writing, no reply had arrived. Read the chat for later answers; do not infer approval.

Exact next action: record any look choices, then check `round2/logs/preview-queue.log` and the running `round2_preview_queue.py` process before launching anything. The isolated graphics, demo and contexts are being built sequentially, respecting the shared build-cap wait. R2 has not generated or authorized new AI motion. Keep the global dispatcher paused. Never launch a second copy of this preview queue while one is alive.

# Locked decisions and completed speech

- Full opening: "I'm a personal trainer. And AI just took my job."
- Delete only "And it's completely free" and "while human trainers leave you confused until next week." Every other filmed script passage remains, including obsolete/everyone, the early free-app CTA and the full human-plan comparison.
- Voice is warm with added bass. Original selected audition `audio-options/warm-bass.wav` was rehashed to `6bb6395530f01880a297a3beecea6da30f989e297246796c42357e852e176cff`.
- Speed-up is explicitly authorized. R2 retained source duration is **65.66 seconds**, with rate **1.1147707979626484** for a **58.9-second** target. The produced voice measures **58.919 seconds**. Use one synchronized edit and identical sound for 9:16 and 16:9.
- `round2/cut.json` has all 12 source pieces. `round2/words_out.json` is the retimed word map. `round2/speech-and-source-evidence.json` records source identity and voice hashes. The old `proposed-cut.json` is superseded and must never become the final edit map.
- R2 keeps the second clean early-CTA take and the third complete fat/muscle explanation. "And finally" is inside an uninterrupted piece. Zero-duration duplicated "When you" transcript entries were excluded, with no audio removed for that transcript artifact.
- Shared audio self-test passed. The fixed approved warm EQ was applied through `voice_chain.py`, without dereverb. `round2/audio/warm-bass-final-timing.wav` hash is `00eef07fc0028d1a1632151f740207366a27ecc9b3d6e7b346f8c39f1b8922d1`.
- Audio gate: **FAIL on tone only**, 11/12 other audio measurements passed. Mean tone error 2.721 dB, max 5.27 dB, loudness -14.30 LUFS, true peak -2.30 dBTP. This is the documented fixed warm EQ mismatch. Preserve Dan's sound and report exact findings. Never change thresholds or call the stamp PASS.
- Gemini listened to the complete native selected cut and the complete processed cut, confirmed retained speech, and rated intelligibility 9/10. A slightly rushed "where" was noted, still intelligible. No chopped opening or "And finally" was reported. This was an audio check, not a complete picture/lip-sync audit. See `round2/logs/speech-listen.txt`.

# Look, assets and pending render packet

The look page recommends B (e1.45 daylight LUT, saturation 1.12, gamma 1.03) and crop pair 1. These remain choices, not approvals. Pair 1 has 800x1422 / 612x1088 vertical source windows. Pair 2 is looser, 900x1600 / 750x1334. The horizontal examples use fixed 2160x1216 / 1728x972 windows. Every head position was sampled about every 0.2 seconds. Face-box-derived hair estimates are preparation, not a final native hair-clearance pass.

The source is native portrait pool footage C1668, encoded 3840x2160 with -90 rotation, displayed 2160x3840. The existing sidecar's 5,100,640,127 byte identity matches the source size. Its microphone is stereo dual-mono, extracted with `pan=mono|c0=0.5*c0+0.5*c1`. Preserve BT.709 interpretation and source daylight S-Log3 conversion. Raw media stays read-only.

Planned assets, with mapped spoken anchors:

- D01 app demo, approximately 19.40-24.19: reuse the approved sunglasses-to-pool simulated same-person sequence. `recipe/round2_demo.py` rebuilds the approved modern shell in both formats. It carries the REAL chip through source demo frames 0-107, the AI chip from 108 onward, then the original AI pool picture. Labels are outside the photo/person and separate from captions. No phone-scrolling filler or stick figures.
- G01 analysis card, 26.07-32.81, `That shows` to `Next`: shared HyperFrames `analysis-card`, original AI pool picture, no printed numbers, three bars and plan band. Title-case row copy, one AI label below the photo.
- G02 Motivation lower third, 32.81-38.11, `Next` to `It's far better`: "A Plan Built Around Your Goal."
- G03 Motivation lower third, 42.66-47.42, `And finally` to `when you can't make`: "Keep Progress Going When Life Changes." Parts land on `AI adjusts` and `when life gets`.
- Opening is Dan on camera. The previously proposed robot clip is unused. No ending URL mark.

`round2/plan_resolved.json`, `edit-sheet.json`, `hf16/`, `hf9/`, `track.json`, `crop-metrics.json` and `join-inventory.json` preserve preparation. The current `edit-sheet.json` is a graphics preparation sheet, not the complete validated final delivery sheet. There are 11 source joins, still awaiting the exact final native boundary audit.

The helper recipes are in work-root `recipe/`:

- `round2_cut.py`: speech selection, pitch-preserving rate, shared voice processing and audio check. Do not rerun merely to rebuild picture.
- `round2_visuals.py`: source sampling and isolated graded plates. Existing source plates were built before the last tracker correction. The recipe now passes `FPS * speed` to shared landing, preserving 0.75-second easing and speed caps in delivered time. Final picture must use this corrected timing; do not describe old look plates as a native final centering PASS. Crop sizes and color choices are unaffected.
- `round2_graphics.py`: shared `from_plan.py` phrase resolution and shared horizontal/vertical template builds. G01 was rendered; remaining builds may still be waiting or running. Reuse matching configs/render stamps.
- `round2_demo.py`: approved app/goal context in both formats.
- `round2_context.py`: shared RGB compositor, exact-duration contexts and 540p copies. Updated captions use balanced three/four-word phrases, Manrope ExtraBold, and lift above horizontal lower thirds. App labels clear the captions. This avoids an internal earlier horizontal caption overlap.
- `round2_preview_queue.py`: waits for the base-plate process to finish, then builds graphics, demo and contexts sequentially. The running queue was launched with completed source PID 56206. Observe the log and process; do not duplicate it.
- `round2_stills.py`: earlier independent template snapshots. **Existing G02/G03 stills are stale relative to the shortened graphic spans and caption repair. Do not show them.** The context renderer will replace them with exact fresh composite frames.
- `round2_page.py`: publishes look choices only until `round2/asset-preview-QA.json` exists. Do not create that file before checking all asset previews and binding the checks to their hashes. Then regenerate the page and refresh the same managed port.

# Required review and delivery

Once queued contexts exist, inspect both formats, including the whole phone sequence, labels, hair, every framing boundary, graphic reveals/exits, caption placement and audio sync. Obtain the appropriate independent asset check. Fix actual defects before showing them. Store evidence and exact hashes in `asset-preview-QA.json`, then run the page generator and managed `review_server.py 8976 <round2>` to add checked contexts. The service sometimes returns bootstrap exit 5 immediately after bootout; a second invocation after the old worker has left succeeded. Do not replace the service with a terminal server.

Record Dan's look and asset decisions with exact files/hashes. Full assembly is still unauthorized while those choices remain pending under the handoff and skill. Use the current short-ad rule to show the whole short ad at the opening-composite stage when all remaining assets are approved. Then exact final audio/delivery gates, complete chronological picture/audio watch, continuity/freeze dispositions and one independent full-candidate review. Preserve known FAIL rows honestly.

Final build should target 1765 frames at 30000/1001 (58.892 seconds), leaving the small finishing pad beyond the last complete word. Rebuild final word/caption timings on the actual native timeline. The full gate plan, renderer-emitted caption/label states, delivered ASR, complete edit sheet and final watch evidence remain to be produced. `round2/verification-preparation.json` explicitly records pending inputs, not a gate stamp.

Deliver both masters, 540p copies, A/B, stamps, notes and rebuild recipe to `Codex Ad Videos/ai took my job - RA-16/`. Full review videos >=45 s also go in `Videos to Review/`. No full review video yet exists. After the final candidate, give exact revision/watch timestamps from that delivered film. No upload or ad setup is part of this task.

# Records and spend

Generation spend remains $0. R2 has one Gemini audio-listening call, estimated below $0.50: 3316 input, 418 output and 2068 thought tokens. The cumulative prior estimate plus R2 is below $1.50. Billed dollars and subscription editor token usage are unavailable, not zero. Full independent candidate review has not happened.

Task records were committed to main through a clean worktree so unrelated live sessions' shared-file edits were not included. R2 initial build status commit: `fdff7a5`. The clean records worktree is `/Users/danielrose/.codex/worktrees/ra16-r2-records/Abs By AI`. Later record commits may follow. The main checkout safe-push stopped on live `Handoffs/video-editing/00-MASTER.md`, `Handoffs/video-editing/jobs.json`, staged `.claude/skills/_shared/framecheck/tapir_cpu.py`, and staged deletion of `.claude/skills/_shared/framecheck/tapir_mps.py`. None was adopted or reset. Own records reached main through the clean worktree. Railway's read-only API returned `Not Authorized`; no application code was changed or manual deployment performed.

# Starter prompt

AD. Name this chat AI Took Job AD R3. Use the exact abs-edit-ad skill in Media/codex-video-trial/skills/abs-edit-ad/SKILL.md and execute Handoffs/handoff-20261014-ra16-round3-look-and-assets.md. Record my color/crop choices from the prior chat, inspect the existing queued asset previews, and finish the remaining review before both masters. Preserve the full opening, only the two approved deletions, all other words, the 58.9-second target and the approved warm bass voice. Reuse preparation and do not launch a duplicate preview build. No publishing.
