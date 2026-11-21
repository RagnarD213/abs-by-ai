AD. AI Took Job AD R2. Next-round editing handoff, 2026-10-14.

# Goal and executor

Use `$abs-edit-ad` to continue RA-16 from the existing preparation. Deliver a 9:16 ad at or below 59 seconds and a 16:9 version of the same edit, with the same words, timing and sound. Recommended: GPT-6 Sol, high effort. The source preparation and voice options exist; the remaining timeline, sound and graphics work needs careful editing and verification.

Start by naming the next chat `AI Took Job AD R2`. Read the current `.claude/skills/_shared/VIDEO-RULES.md` in full, `Handoffs/video-editing/00-RULES.md`, its linked Codex environment table, the abs-edit-ad skill, and `AI_COORDINATION.md`. Work in the existing RA-16 directory or a new round2 subfolder. Do not start over or touch another editor's files.

# Dan's decisions, locked on 2026-10-14

His exact instruction:

> For the opening let's go with B: "I'm a personal trainer." For the shorter cut lines just remove "and it's completely free" and while human trainers leave you confused until next week, leave everything else in. Accelerate the video as necessary to get it under 60 seconds after cutting that stuff Let's go with warm with added bass for the voice Give me that handoff for the next round

1. Keep the full opening: "I'm a personal trainer. And AI just took my job." B means the OPENING choice, not the color choice.
2. Remove only "And it's completely free" and "while human trainers leave you confused until next week." Keep every other script line, including the obsolete/everyone passage, the early free-app sentence and CTA, the comparison after the personalized plan, and the complete final CTA. Normal cleanup of false starts, repeated takes and empty pauses is allowed without removing script content.
3. Accelerate as necessary to fit under 60 seconds. Target 59.0 seconds or less to also satisfy the original master specification. This explicitly overrides the original handoff's no-speed-up instruction. Use the minimum necessary pitch-preserving speed increase after selecting and tightening complete takes; keep picture and voice synchronized. Calculate the actual rate from the finished retained duration, do not guess it from the old proposal. Preserve the approved voice tone and inspect intelligibility at the delivered speed.
4. Voice: warm with added bass, the `warm-bass.wav` audition. Do not substitute the editor's earlier preferred default or the lighter-bass option. No new voice-choice question.
5. Scripted spoken claims are approved under Dan's 2026-10-14 standing rule. Do not flag or reopen them.

The former 50.4-second proposal is SUPERSEDED. Its extra omissions were not approved. Recover all remaining script lines from the source and original script; do not use `proposed-cut.json` as the final edit map.

# Locked voice and source

Work root: `/Volumes/Extreme/_edit_work/ra16/`.

Approved audition: `audio-options/warm-bass.wav`, SHA256 `6bb6395530f01880a297a3beecea6da30f989e297246796c42357e852e176cff`. The same audition is on `round1/audio/warm-bass.wav`. Recipe: `recipe/audio_options.py`, using the shared voice chain with fixed EQ: high-pass 70 Hz, +1.5 dB at 140 Hz, -1.5 dB at 450 Hz, -1 dB at 3.2 kHz and a broad +3 dB at 120 Hz. The source is dry; no dereverb was used. Reuse this character on the final timeline.

Raw source: `/Volumes/Extreme/abs by ai 8:28 shoot | jeff | dan | ads, dedicated shorts, b roll, scripted long form content/main camera/C1668.MP4`.

Verified correction to the original handoff: this is OUTDOOR POOL, native portrait footage, stored 3840x2160 with -90 rotation and displayed 2160x3840. It has one stereo dual-mono microphone stream, not four separate tracks. Reuse its existing roll sidecar, word transcript and measured mapping: `-map 0:a:0 -af pan=mono|c0=0.5*c0+0.5*c1`. Raw footage stays read-only. Decode with the established BT.709 interpretation and source-specific daylight S-Log3 conversion.

Original script: `Media/codex-video-trial/05-recipes/candidates/shoot5-notes.txt`, section "AI Took My Job", around lines 419-429. Full transcript/roll info: work-root `source/words.json`, `source/roll.json`; original full-roll transcript folder `/Volumes/Extreme/_edit_work/_transcripts-828-full/`. The previous full-script selections measured about 73.4 seconds before the new two cuts and final pause cleanup. No new exact runtime has been measured.

# Completed preparation and what remains open

- Review page: http://127.0.0.1:8976/ ; files: work-root `round1/index.html`. It currently shows the OLD proposed cuts. Refresh it before the next review so obsolete choices are not presented as pending.
- `WORK_PACKET.json`, `cut-look.json`, `grade-options.json`, `track-look.json`, `recipe/`, `logs/`, `round1/stills/` and `cost-ledger.json` retain the preparation and evidence.
- Color B is only the editor's recommendation (exposure 1.45 daylight LUT, saturation 1.12, gamma 1.03), not Dan's approval. Color and crop choices remain unconfirmed. Show the existing useful comparisons in the next packet; do not misread opening B as color B.
- No complete ad, final master, approved opening composite or complete-candidate audit exists yet. Internal 9.943-second samples under `round1/context/` were withheld after tone/spread audio failures. They used earlier processing, not an approval of the final warm-bass mix. The current VIDEO-RULES explicitly documents fixed warm EQ versus the tone gate as a known mismatch. Preserve Dan's selected sound, inspect current shared handling, report exact results honestly and do not alter thresholds to force PASS.
- A model alleged unrelated sound/picture on one sample. Source waveform comparison found 0 ms lag and source/candidate images matched. Evidence: `source/sync-proof/comparison.jpg` and `round1/audio-checks.json`. Do not repeat the disproven allegation as a finding; still check the new accelerated timeline.
- Existing opener candidates A0147 (9:16) and A0148 (16:9), robot spotting a bench press while a fired trainer leaves with a box, are library assets. Their use here is still a proposal. No new AI motion is authorized by this handoff alone.
- Same-person app demo: `Media/codex-video-trial/assets/ad/simulated-dan-sunglasses-to-pool/`, with its approved sequence and labels. New graphics use shared Soft Blue Light HyperFrames, including the current analysis card template. No stick-figure exercise demo and no generic person merely looking at a phone. No ending AbsByAI.com mark.
- Generation spend so far: $0. Six Gemini review calls were estimated under $1; usage is in the ledger, actual billed dollars unavailable. Preserve the running totals.

# Exact next action and round scope

Reconstruct the complete spoken edit with only Dan's two requested deletions. Verify every word boundary against heard source audio, including the old provisional P5 start that may clip "And" and the transcript's duplicated "When you". Measure the retained duration, apply the minimum synchronized speed increase to meet 59 seconds, and rebuild word/caption/graphic timings from that final speed. Record the rate and measured duration.

Use the locked warm-bass voice. Complete the source look, graphics and clip review with surrounding speech. Preserve vertical land-then-hold tracking and fixed horizontal framing; verify all hair and gestures. Follow current approval rules without reopening settled decisions. When the short ad reaches the point where all remaining assets are approved and only a few seconds remain beyond the opening preview, show the whole ad under the 2026-10-14 short-form rule. Do not infer approval for unseen assets or unchosen outdoor look settings.

For final delivery, run shared exact-file audio and delivery checks, continuity/freeze checks and one independent full-candidate review. Keep any genuine failures explicit. Deliver both masters, 540p review copies, audio A/B, stamps, notes and rebuild recipe under `Codex Ad Videos/ai took my job - RA-16/`. Put any review video 45 seconds or longer in `Videos to Review/` too. Refresh port 8976 through the managed review server, verify playback/seek, send Dan the review link, and update the queue/master honestly. No upload, ad setup or publishing is part of this round.

# Starter prompt

AD. Name this chat `AI Took Job AD R2`. Use `$abs-edit-ad` and execute `Handoffs/handoff-20261014-ra16-round2-approved-cut-and-voice.md`. Keep "I'm a personal trainer. And AI just took my job." Remove only "and it's completely free" and "while human trainers leave you confused until next week"; keep everything else. Accelerate as needed to 59 seconds or less, with pitch preserved, and use the approved warm voice with added bass. Continue the existing preparation, resolve only the remaining look/assets review, and deliver 9:16 plus 16:9 from the same edit after the required checks. Do not reopen these decisions.
