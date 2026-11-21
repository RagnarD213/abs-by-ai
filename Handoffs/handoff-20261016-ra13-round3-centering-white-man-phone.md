AD. RA-13, Most Guys Abs, round 3.

Next task name: **Most Guys Abs AD R3**. Recommended model: **GPT-6.1 Sol, high effort** for this scoped Codex revision.

## Goal and current authority

Execute Dan's October 16 review notes with `$abs-edit-ad`. Read the current `.claude/skills/_shared/VIDEO-RULES.md`, `Handoffs/video-editing/00-RULES.md`, RA-13's job, and the skill before editing. This handoff supersedes the R2 asset choices only where stated below. It authorizes the R3 edit, both complete review copies, required checks and fresh independent review. No upload/setup or public publishing.

Dan asked for this handoff, not for R3 to run in the R2 chat. R3 has not been built. Recorded choices and screenshot locators: `Handoffs/video-editing/RA-13-round3-decisions.json`. Original screenshots are copied under `/Volumes/Extreme/_edit_work/ra13/round3-plan/references/` as `Dan-R3-note-1.png` through `Dan-R3-note-4.png`.

## Exact changes

1. **Vertical presenter centering:** Dan is off-center in the opening frame. Fix that and inspect every other presenter hold, deliberate scale cut and return from an insert throughout the vertical for the same problem. Preserve approved crop sizes. Land on his actual head center at the first delivered frame of each shot, then use shared `cut/landing.py` land-then-hold. Verify the rendered face/hair position, not just the tracking settings. Do not add constant chasing movement. Keep hair in frame.
2. **Replace the generation demo:** use the existing white man's sequence, not Dan's sunglasses photo or Dan's AI pool goal. Show his generating screen, then his own settled after-only results screen. **Both stay inside the same phone frame.** Keep that phone's scale, position, shell and screen opening consistent through the internal cut. Do not expand the goal photo to a full-screen picture or substitute a separate photo card for the results screen.
3. **Analysis graphic:** use that exact white man's matching after picture in the scan/graph graphic. Remove Dan's AI picture there. Preserve the current shared Soft Blue Light HyperFrames analysis treatment, scan, three bars, plan and absence of invented numbers.
4. **Horizontal:** apply the same generation/results and analysis-photo changes. Dan explicitly says horizontal centering looks good. Preserve horizontal presenter positioning, static shots and the R2 headroom correction. Do not redo horizontal tracking or crop sizes.

The generation/results phone requirement concerns the two screens in the generation sequence. The analysis graphic retains its approved layout with the subject photo replaced. Do not reinterpret this as a request to put the whole analysis graphic inside a phone.

## Verified existing white-man source

**Library B0550**, used in RA-04's latest Top 3 Tips ad, is the existing real app recording of the AI-generated white man by the lake dock. No new image generation or live product call is needed.

- Recording: `/Volumes/Extreme/_edit_work/ra04/round5/gen_white_man_rec.mp4`, 1320x2868, 60 fps, 42.033 s. SHA-256: `108e0b9b9eaf17c6268c11aa62ad8f2745e92f0dc7c2a118438ffddb790b6d84`.
- Matching after picture: `/Volumes/Extreme/_edit_work/ra04/round5/after_white_man.jpg`. SHA-256: `dd9e88b936db9216163a8e3396669f976e388f185cb096113598e06ebb388763`.
- Before source used by that generation: `/Volumes/Extreme/_edit_work/ra04/round5/before_white_man_45.png`. It is AI-generated too. Never label this as a real photo of Dan.
- Recording timing reference: loader around 3.40-5.80 s, settled results from about 36.60 s. `.claude/skills/ad-edit/reference/ra04/round5/r5_cards.py` documents these source windows. Recheck the chosen moving frames. Its old cropped media-card presentation is a source locator, not the requested R3 layout. Rebuild inside RA-13's consistent phone shell instead of copying its card or push-in.
- Keep appropriate AI disclosure on the sequence and analysis image. The catalog's generic `needs_ai_label: false` does not override its explicit note that the before photo is AI-generated. Never show the app's before/after pair or email form. Check every selected frame around the loader-to-results cut.

## R2 baseline and preservation

Work root: `/Volumes/Extreme/_edit_work/ra13/`. R2: `round2/`. Start an isolated `round3/` and protect R2 as the baseline.

R2 native files in `round2/final/` and `Codex Ad Videos/why do most guys never get abs - RA-13/`:

- `why do most guys never get abs | codex | 9x16 | RA-13 R2.mp4`, SHA `2f10b36412e1890c8618161c628725876cce1f794e329bc5c31e7f49abaa90ed`.
- `why do most guys never get abs | codex | 16x9 | RA-13 R2.mp4`, SHA `453c6f10bcb7142f6065c7344e8b91fa0b29a088b301d245a450f4a9a4752d5a`.

Both are 1616 frames, 53.9205 s, 30000/1001 fps, with identical audio. Preserve the full spoken edit, captions, Brighter Natural B color and approved lighter bass audio. No dereverb or repeat look/voice audition. Vertical wide/close source sizes: 738x1312 and 630x1120. Horizontal: 2144x1206 and 1728x972; fixed center 1080; close crop top 1260, retaining R2's approximately 30% headroom reduction.

R2 timeline locators, to be verified against R3 before delivery:

- Opening 0.00; close presenter holds 2.27-14.35, 25.16-28.36 and 42.61-46.58.
- P1 generation/goal sequence 14.35-25.16. Replace the content/layout as requested above; retime loader/result portions to the narration while preserving spoken duration.
- A1 analysis 28.36-33.77. Replace the subject photo.
- P2 workout/food tour 33.77-38.97, internal cut 35.769. Preserve.
- CTA 51.38-53.92. Preserve repaired clearance: vertical over shorts, horizontal in left pool, never over abs or captions.
- Rejected A0074 lockscreen and B0037 stick figures remain removed. The white-man results request does not ask to reinsert either rejected clip.

Recipe backup: `.claude/skills/ad-edit/reference/ra13/round2/` (scripts are directly here, not in a nested `recipe/`). Working scripts: `round2/recipe/`. Read `README.txt`, `build-record.json`, `framing.json`, `cta-layout.json` and the edit sheet. `build_full.py` uses source measurements plus exact-cut measurements only on some paths; investigate every landing, including the opening, instead of trusting this old condition. Original `cut.json` is unchanged; R2 subtracts 0.6006 s of empty lead in its build. Use R2's actual cut and word map, not raw-source or R1 times.

## Verification, review page and delivery

R2 independent media review passed after CTA repair, but that verdict does not clear the newly rejected vertical centering. R2 automated gates honestly remain FAIL for voice tone/floor against the studio reference, approved horizontal wide head size, and some deliberate scale cuts. Preserve unchanged approved choices, rerun exact-file checks for R3, record every result, and do not change thresholds or invent PASS stamps.

Inspect every vertical landing and every changed phone/result/analysis frame, shell consistency, same-person identity, label placement and transitions. Complete editor self-QA, all required exact-file gates/watch/listen checks, edit-sheet validation with hashes, and one fresh independent complete-candidate review. Give that reviewer Dan's centering rejection and required phone scenes, with approved source assets for comparison. Do not carry the old centering judgment forward. Respect the shared two-build cap and raw-source read-only rule.

**All browser review-panel testing stays silent.** Mute before pressing play and keep it muted through seeking, format switches and speed tests. Leave playback paused afterward. Do not play sound unless Dan explicitly asks. Model/file audio review can still run without audible browser playback.

Keep the working review URL `http://127.0.0.1:8973/`. Refresh it through `.claude/skills/_shared/review_server.py` after packaging. Preserve the October 16 recovery button and inactive-tab reset in `review_page_r2.py`; do not restore the older blue-box-prone page. Verify visible picture, HTTP 200, media byte-range 206, seeking and format switches with muted playback. Preserve local review notes.

Deliver complete 9:16 and 16:9 R3 candidates to the existing Codex Ad Videos folder, plus physical full-quality `Videos to Review/Most Guys Abs AD R3 - vertical.mp4` and `... - horizontal.mp4`. Send the actual vertical review copy and horizontal link. Include exact timestamps in the NEW full film and short watch ranges for centering, the generation-to-results sequence and analysis photo. Keep any unchanged gate flags separate from new revisions. Update RA-13 through `scripts/edit-queue/queue.py`; do not mark finalized without Dan's approval. Remove this entry from the OPEN handoff index when executed. No thumbnails or setup in this edit round.

Previous R2 review estimate was under $3, actual billing unavailable; receipts and unavailable editor/reviewer usage are documented in `round2/cost-ledger-r2.json`. This handoff spent nothing on generation or review. Use the standing review budget and report new usage honestly.

## Ready-to-paste starter prompt

AD. Name this task Most Guys Abs AD R3. Read Handoffs/handoff-20261016-ra13-round3-centering-white-man-phone.md and execute it with $abs-edit-ad. Fix vertical opening centering and any other vertical centering errors. Keep approved horizontal presenter framing. Replace Dan's generation demo with existing white-man recording B0550, keeping generation and his after-only results screen inside the same unchanged phone frame. Use his matching after picture in the analysis graphic in both formats. Preserve the approved color, voice, edit and other scenes. Complete all required checks and a fresh independent audit, deliver both full review copies, update the master list, and keep every browser test muted.
