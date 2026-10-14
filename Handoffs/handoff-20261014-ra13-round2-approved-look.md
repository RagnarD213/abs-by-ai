AD: Why Do Most Guys Never Get Abs? RA-13, round 2

Task name: **Most Guys Abs AD R2**. Recommended model: **GPT-6.1 Sol, high effort**.

## Goal and authority

Continue the existing ad edit with `$abs-edit-ad`. Read `Handoffs/video-editing/00-RULES.md`, the original RA-13 job, and the current `.claude/skills/_shared/VIDEO-RULES.md` in full. This handoff supersedes the pending look decisions and next actions in `handoff-20261013-ra13-round1-look.md`. Deliver a 9:16 master at most 0:59 and 16:9 from the same edit, with all required gates and an independent audit. This is an editing task; upload/setup follows separately.

## Dan's locked choices, October 14

- **B: Brighter natural** color, not C. Preserve the 8/28 S-Log3 conversion. Exact filter is in the decisions file.
- **Vertical framing approved**, wide 738x1312 and close 630x1120 at source resolution. Preserve these sizes and use shared landing/tracking.
- **Horizontal close: remove about 30% of the empty space above his head.** Keep the 1728x972 close crop and fixed horizontal center 1080. This means leave 70% of the current headroom, not zoom in 30%. Measure the hair top in the approved example: new crop top = old crop top + 0.30 times the existing headroom. Verify clearance across the actual shot; keep each horizontal shot static. Horizontal wide remains 2144x1206.
- **Lighter bass voice approved.** Dan's dictated “letter base” refers to the named lighter bass option. Preserve `audio-options/lighter-bass.wav` and its shared voice-chain settings; no dereverb or repeat audio bakeoff.

Verbatim request, exact reference paths and SHA-256 fingerprints are saved in `Handoffs/video-editing/RA-13-round2-decisions.json`, mirrored at `/Volumes/Extreme/_edit_work/ra13/round2-plan/decisions.json`. These are look and voice decisions, not blanket approval of every asset or final motion. The headroom revision still needs implementing.

Scripted claims are pre-approved under Dan's October 14 instruction. Do not reflag them or ask again. Keep believable graphics without invented figures.

## Saved work and actual status

Work root: `/Volumes/Extreme/_edit_work/ra13/`. Review: http://127.0.0.1:8973/. Existing source code backup: `.claude/skills/ad-edit/reference/ra13/`; working scripts: `recipe/`. The review-page generator is historical and would restore stale decision/claim text if run unchanged; apply the current decisions when regenerating it.

`cut.json`, `edl_spec.json` and `cut_audio.wav` hold a tentative **54.5205-second** best-take edit, including the 0.6-second ending. No speech speed change or filmed line removal. Hook starts at source 254.38, problem at 265.25, solution at 286.185 through 325.97. Preserve the spelling corrections in cut.json; rerunning recipe/edl.py loses them. Cover the tiny 0.34-second piece before “First” rather than flashing a presenter frame.

Actual raw source is outdoor pool footage, native portrait 2160x3840 after rotation, 29.97 fps:
`/Volumes/Extreme/abs by ai 8:28 shoot | jeff | dan | ads, dedicated shorts, b roll, scripted long form content/main camera/C1667.MP4`.

Per-file lav is recorded in `source/lav_selection.json`: 0:a:0 averaged to mono, `pan=mono|c0=0.5*c0+0.5*c1`. Raw files are read-only. Do not print env.json, which contains a huge waveform array.

The four 14.95-second look samples **finished rendering**: `round1/context/look-{A,B,C}-9x16.mp4` and `look-B-16x9.mp4`. `logs/track-look.log` confirms completion. They still need technical inspection. Only the first two pieces have tracking measurements. The horizontal moving sample shows the wide crop; no revised close moving sample exists. `round1/context/L1-source.mp4` and `P3-source.mp4` also exist and need inspection.

Shared audio self-test passed. `logs/cut-listen.txt` is **invalid** because the reviewer evaluated text instead of hearing audio. Retry with the actual attached media and verify what was evaluated. No complete film, final gate pass, complete watch/listen or independent complete-film audit exists yet.

## Assets and next execution

Preserve the same-person sunglasses-before to Dan pool-goal demo at `Media/codex-video-trial/assets/ad/simulated-dan-sunglasses-to-pool/simulated-dan-sunglasses-to-pool-ad14-v1.mp4`, with its provenance sidecar and appropriate disclosures. This reusable source has prior approval; its exact RA-13 timing still needs review. Proposed timeline: P1 17.0-25.7, phone lockscreen L1 25.7-28.8, analysis A1 28.8-34.3, app features P2 34.3-39.4, workout swap P3 40.3-47.2, CTA 51.8-54.5.

Inspect L1 (A0074) and P3 (B0037) in motion. P2 uses approved B0544 workout instruction and food analysis; check that the selected scene matches the spoken referent. **Rebuild A1 with the current shared Soft Blue Light HyperFrames analysis template.** The old recolored Pillow/adkit still is superseded by the October 14 rule. Keep the same Dan picture, scan, three bars and plan, without numeric measurements. CTA stays “Tap The Button Below / Get Started,” no ending URL. Final overlays use shared HyperFrames and spoken-word timing. `plan_resolved.json` is a preliminary object, not the final integration array.

First apply the horizontal headroom change, inspect the chosen look in motion and validate the speech joins. Then complete the required asset review. Follow the October 14 short-ad rule: when assets are sufficiently approved, show the whole short ad instead of forcing a first-30-seconds round. If genuinely uncertain new assets remain, use the prescribed preliminary review. Preserve all earlier approval gates. Any AI motion requires the current editor sense checks and fresh independent asset review before showing it; final complete-film audit is separate.

Finish both masters with the same edit/audio, exact-file gates, full watch/listen and independent audit. Put final media in `Codex Ad Videos/why do most guys never get abs - RA-13/`. Full review copies of 45 seconds or longer also go into `Videos to Review/`. Send the actual 9:16 review copy and update RA-13 through `scripts/edit-queue/queue.py`. Include precise full-film timestamps and short watch ranges for the headroom change and any other revisions. Estimated prior review spend was under $2; `cost-ledger.json` holds usage, actual billing unavailable. No new generation was purchased for this handoff.

## Starter prompt

AD. Name this task Most Guys Abs AD R2. Read Handoffs/handoff-20261014-ra13-round2-approved-look.md and continue with $abs-edit-ad. Use my locked brighter natural B color, approved vertical framing and lighter bass voice. Reduce the horizontal close shot's existing headroom by about 30% without changing its shot size. Continue the review gates under the current short-ad rules, then finish both masters, all exact-file checks and the independent audit. Send me the review copy and update the master list.
