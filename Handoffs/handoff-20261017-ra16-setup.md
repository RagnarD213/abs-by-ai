AD. AI Took Job: approved R4, thumbnails and setup.

Task name: **AI Took Job AD Setup**. Recommended model: **Claude Opus 5.5, high effort**. Written October 17, 2026.

**Use the Codex subscription to generate the images.** One Claude task makes five thumbnail choices, stops for Dan's pick, then uploads both approved films and completes the Google Ads setup.

## Approval and exact masters

Dan approved both delivered R4 formats in AI Took Job AD R4 on October 17, 2026: "Everything looks good. This is approved. Give me the handoff or setup".

Authority: `Handoffs/video-editing/RA-16-R4-approval.json` and the delivery folder's `APPROVAL.json` and `APPROVAL.md`. RA-16 is finalized. This handoff has not been executed; thumbnail selection, uploads and ad creation have not started.

Delivery folder:
`/Users/danielrose/Documents/Claude/Projects/Abs By AI/Codex Ad Videos/ai took my job - RA-16/`

| Format | Exact upload filename | SHA-256 | Bytes |
|---|---|---|---|
| 9:16 | `AI Took Job AD R4 - 9x16.mp4` | `fdc6ad507531a2f5b113dea8b03c23680db4bcec4e43102c1fefc39c9749e5fb` | 100282648 |
| 16:9 | `AI Took Job AD R4 - 16x9.mp4` | `789944e4dc7ee70b2e5b0af55d5ece8c73dda446155e609c28420553e84c963d` | 85885396 |

Both are H.264/AAC, 1765 frames at 30000/1001 fps, **58.892167 seconds**. Vertical is 1080x1920; horizontal is 1920x1080. Verify both hashes before setup. Upload these native files, never the smaller REVIEW proxies or a rejected framing/caption candidate. They are already the exact approved upload masters; no new export, render, transcription or creative review is needed.

The complete ending at about 57.14-58.74 is **"Tap the button below to get started."** This is an AD. Only Unlisted YouTube plus Google Ads. No organic posting, Blotato, Public YouTube, native YouTube scheduling or pinned question comment.

## Preserve the approved films

Preserve Color B, crop pair 1, the full opening, warm bass sound, spoken edit and captions. D01 is the approved modern-phone simulation using a real sunglasses photograph of Dan and his AI pool goal. G01 is the matching Soft Blue Light analysis card; G02 and G03 are the approved plan and life-change lower thirds. These are the same person. The real photograph remains labelled real; the AI goal remains labelled AI-generated.

The last repairs are complete: vertical landings use the shared land-then-hold method; captions appear once; "And finally, AI adjusts" starts at 43.1431; the preceding horizontal caption clears before the graphic changes its position. All required assets, the opening and complete CTA were independently checked. Each format has 35/35 watch images and all 16 cut boundaries judged, with zero confirmed open film defects. AAC packets and timestamps are identical across formats and preserved through the repairs.

Both historical numerical delivery stamps remain **FAIL**, honestly recorded: each has 34/39 rows passing, four failed rows and one unmeasured row. The retained flags are approved voice tone, preset insert coverage and deliberate cut contrast; vertical also has a centering metric at 57 seconds, horizontal the approved wide head size. The highlighted-word sync test cannot measure phrase captions; a separate phrase-onset audit and picture/audio review were completed. Dan approved these exact films after those flags were reported. Do not alter sound, crops, assets or gate thresholds, or rerun checks to manufacture PASS. Approval is separate from the untouched machine stamps.

Evidence: delivery folder `R4 production/final-review-status.json`, `INDEPENDENT_REVIEW.json`, `INDEPENDENT_REVIEW.txt`, `watch/`, `independent-repair/`, `independent-extra/`, `evidence/` and `R4 notes.txt` one folder above. Work root: `/Volumes/Expansion/Abs By AI Edit Work/ra16/round4/`. Retained words: `words-native.json` and `delivered-words.json`; exact caption intervals: `captions-9x16-evidence.srt` and `captions-16x9-evidence.srt` in that work root. Reuse them for copy and chapters.

## Read first

Read `.claude/skills/ad-setup/SKILL.md`, full current `.claude/skills/_shared/VIDEO-RULES.md`, `.claude/skills/_shared/IMAGE-GENERATION.md` and `AGENTS.md`. Follow the latest five-thumbnail rule over the skill's historical two-design section, and the trial-campaign builder over the old home-versus-start pair. Current setup precedent: `Docs/RA13_SETUP_RECEIPT_20261017.md` and `.claude/skills/ad-setup/reference/ra13-setup-20261017/`.

## Execution

1. Verify the two native hashes and approval record. Check ownership, existing uploads, `Docs/AD_VIDEO_IDS.md` and any `scripts/ads/api/dgen-ads/ra16.json` and result before creating anything. Reuse saved IDs on resume.
2. Draft title, description, tags, chapters and ad copy from the approved words. Recognizable YouTube title: "AI Took My Job". Keep the first-person argument and the real-before/AI-goal provenance accurate. The spoken script is approved; do not reopen it. Do not copy the old free-generation CTA from historical ad-setup boilerplate. Use the established current description destination and UTMs, and inspect the actual Ads destination in step 5. Use the maintained lint and successful current campaign copy as the copy reference. No em dash or en dash in new writing.
3. **Make five unique thumbnail designs with Codex, then stop for Dan's pick.** Use `.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high` on Dan's subscription. Slots: one real pool-shoot photo, one real studio-shoot photo, one AI-enhanced or AI-generated image of Dan tied to this ad's subject, and two more AI-generated concepts of Codex's choice, with or without Dan. Give every option a distinct layout, type treatment, color and composition, including the real-photo options. Write a one-line design plan for each before building. Real-photo options use Dan's real cutout over a Codex background with type layered in code; never redraw him. For the AI-Dan option, use a real reference, recognizable face, lean and shredded at the reference size. Use the same headline across all five unless Dan requests copy alternatives. Keep text off face and hair, avoid frowning photos, apply the Speedo crop, and omit website marks and real-photo labels on thumbnails. Make each option in 16:9 and 9:16. Show one numbered review sheet and accessible full-size files. **Stop for his selection before any upload.** No separate Codex chat or thumbnail handoff.
4. After his pick, upload both exact masters with `scripts/youtube/upload.js`, `--privacy unlisted --category 26 --made-for-kids false --synthetic false`. This edit has real camera footage, a composited phone UI demonstration, labelled AI goal stills and code-generated graphics, with no realistic AI-generated video scene or AI music. The provenance is `Media/codex-video-trial/assets/ad/simulated-dan-sunglasses-to-pool/simulated-dan-sunglasses-to-pool-ad14-v1.provenance.json` and `/Volumes/Extreme/_edit_work/ra16/recipe/round3_demo_clean.py`. Labelled AI stills alone do not trigger the upload synthetic flag. Include the accurate AI-image disclosure in the description. Set the chosen thumbnails. Read back channel `UC236gjadarHAhEhOMYNGJ9g`, privacy Unlisted, embeddable true and processing succeeded. At most two concurrent uploads. Inspect existing channel records before retrying an upload error.
5. Add both formats to cold TRIAL campaign **24316364155** in their own RA-16 ad group with `scripts/ads/api/dgen-trial-group.js ra16`. Base `scripts/ads/api/dgen-ads/ra16.json` on the maintained current trial config; RA-13 is a completed precedent. Read target CPA, audience, campaign state and shared budget live. Preserve the budget and never enable a paused campaign. Inspect existing final URLs in the target/reference groups, including paused ads; match their top-level domain. Expected destination is `https://absbyai.com/start`, campaign UTM `dgen-trial-ra16`, with distinct format content UTMs. Verify before applying. Do not create the historical home-versus-start pair. ValidateOnly, apply, read back actual IDs and destinations, then run `node scripts/ads/api/client.js policy 24316364155` and retain its actual result.
6. Record both YouTube IDs, selected thumbnails, group/ad/asset IDs, processing, visibility, destinations, shared budget before/after and policy status. Update `Docs/AD_VIDEO_IDS.md`, `Docs/DGEN_CONVERSION_CAMPAIGN.md`, filed-master state and the RA-16 config/result. Mark RA-16 `uploaded` through `scripts/edit-queue/queue.py` only after both Unlisted read-backs and Ads entries exist; mirror the artifact under the current Claude queue instructions. Do not mark it uploaded at handoff time. Remove this handoff from the OPEN index when executed. Leave only a necessary policy follow-up on the coordination board. Commit and push only this task's files. The main checkout has had unrelated Git object/merge problems; inspect and use a clean checkout if needed, preserving other owners' work.
7. Report the two Unlisted links, selected thumbnail, ad group and destinations, actual policy result and unchanged shared budget. Use the existing policy-follow-up process, not a new per-video routine. Keep browser tests muted and end paused. The Victory Dashboard remains paused.

## Finalization housekeeping

Dan's approval is recorded and RA-16 is finalized, not uploaded. Both redundant R4 files in `Videos to Review/` were removed after checking preserved native delivery hashes. The now-unused managed review service on port 8976 was retired. Original native exports, review proxies, approval records and all evidence remain in the delivery folder and work root. No thumbnail generation, upload, Ads creation or spend occurred while preparing this handoff.

No square, shorter cut, new organic Shorts, clip generation or public posting belongs to this setup task. Both approved films are already under 59 seconds.

## Starter prompt

AD. Name this task AI Took Job AD Setup. Read `Handoffs/handoff-20261017-ra16-setup.md` and use /ad-setup for both approved AI Took Job R4 masters. Use the Codex subscription to generate the images. Make the five unique thumbnail choices, show me one review sheet and stop for my pick. After my pick, upload both exact approved films to YouTube as Unlisted, add them to trial campaign 24316364155 in their own ad group, verify processing, visibility, destinations and unchanged budget, run the policy check and record everything. Preserve the approved films and their recorded gate flags. Keep browser testing muted. No organic publishing.
