AD. Most Guys Abs: approved R3, thumbnails and setup.

Task name: **Most Guys Abs AD Setup**. Recommended model: **Claude Opus 5.5, high effort**, because this task includes thumbnail choices and customer-facing ad copy. Written October 17, 2026.

**Use the Codex subscription to generate the images.** One Claude task makes the five choices, stops for Dan's pick, then uploads and completes Google Ads setup.

## Approval and exact masters

Dan approved both delivered R3 formats in the Most Guys Abs AD R3 chat on October 17, 2026: "All right this looks good. Give me the handoff for setup".

Approval record: `Handoffs/video-editing/RA-13-R3-approval.json` and `Codex Ad Videos/why do most guys never get abs - RA-13/APPROVAL.md` plus `APPROVAL.json`. RA-13 is finalized, not uploaded. This request is for the handoff; setup has not begun.

Delivery folder, absolute path:
`/Users/danielrose/Documents/Claude/Projects/Abs By AI/Codex Ad Videos/why do most guys never get abs - RA-13/`

| Format | Exact upload file in that folder | SHA-256 | Size |
|---|---|---|---|
| 9:16 | `why do most guys never get abs \| codex \| 9x16 \| RA-13 R3.mp4` | `6bb5d4767de0e5b922e08b90c43eba9b66c1b4af78ea60b7ce4ea78ea648ce2a` | 116,949,752 bytes |
| 16:9 | `why do most guys never get abs \| codex \| 16x9 \| RA-13 R3.mp4` | `0a58d484df06a7a076dd03b74944c64b498425e1c3462cd766ddfc51a3e6510b` | 110,712,956 bytes |

Both are H.264/AAC, 1616 frames at 30000/1001 fps, 53.920533 seconds. Vertical is 1080x1920; horizontal is 1920x1080. Verify both hashes before setup. Upload these native files, never the smaller REVIEW540p proxies or an R2 export. These are the exact approved native exports, so no replacement HD export, fresh render or repeat review is needed. If any hash differs, locate the matching approved file before proceeding.

Closing words at 51.379-53.180 seconds: **"Tap the button below to get started."** It is an AD. Only Unlisted YouTube plus Google Ads; no organic distribution, Blotato, Public YouTube, native YouTube scheduling or pinned question comment.

## Preserve what is approved

R3 centers all six vertical presenter landings with the shared land-then-hold method. The white-man demo B0550 generates and reveals his own settled result inside the same unchanged phone at 14.348-25.158, internal screen cut 20.587. The matching after photo appears in the existing analysis graphic at 28.362-33.767. Both source before and after pictures are AI-generated, not real photos of Dan. Horizontal static framing, color, lighter-bass voice, spoken cut, captions, P2 workout/food tour and repaired CTA are approved. Rejected lockscreen and stick figures stay absent.

All exact-file checks are already complete. Fresh independent picture/audio review found zero open media defects; both watch reviews inspected 35 images and all 16 boundaries. Shared graphics checks and edit-sheet hash validation passed. Historical numerical gates remain honestly FAIL: vertical 37/39, horizontal 36/39. Retained failures are the approved outdoor voice tone/floor comparison, deliberate wide/tight cut metrics, and approved horizontal wide head size. No thresholds or stamps were changed. Dan approved the delivered films after these were reported. Preserve the exact files; do not reopen accepted choices or rerun gates to manufacture PASS.

Evidence in the delivery folder: `R3 QC/`, `R3 Rebuild/`, `delivery-status-r3.json`, `Most Guys Abs AD R3 - review notes.txt`, and `cost-ledger-r3.json`. Work root: `/Volumes/Expansion/Abs By AI Edit Work/ra13/round3/`; R2/raw remain on Extreme. Transcript/word timing: `build-record.json` and `words_individual.json` in the R3 work root; subtitles in `cap9/captions.srt` and `cap16/captions.srt`. Reuse these instead of another transcription. Recipe backup: `.claude/skills/ad-edit/reference/ra13/round3/`.

## Read first

Read `.claude/skills/ad-setup/SKILL.md`, the full current `.claude/skills/_shared/VIDEO-RULES.md`, `AGENTS.md`, and `.claude/skills/_shared/IMAGE-GENERATION.md`. Follow the latest five-thumbnail rule over the older two-design section of ad-setup. Follow the current trial-campaign builder over its historical two-landing-page builder. Nearest setup precedent: `Handoffs/handoff-20261016-ra15-setup.md`.

## Execution

1. Confirm the two master hashes, approval record, AD closing line and no other RA-13 setup owner. Check existing YouTube uploads, `Docs/AD_VIDEO_IDS.md`, campaign records and `scripts/ads/api/dgen-ads/ra13.json` before creating anything, so a resumed task reuses saved IDs.
2. Draft the description, tags and ad copy from the approved words. Recognizable YouTube title: "Why Do Most Guys Never Get Abs?" Google Ads copy follows the maintained lint and current campaign examples. Scripted claim lines are already approved; do not request approval again. Keep descriptions accurate to this edit: the generating man and result are not Dan, and both of his source photos are AI. Do not paste the skill's old boilerplate claiming a real before photograph or an AI future picture of Dan. A suitable disclosure is: "Some images and exercise demonstrations shown in the app are AI-generated. Goal images illustrate a possible result, not a guarantee." Use the established description destination and UTMs; verify the actual ad destination in step 5. No em dash or en dash in new copy.
3. **Make five thumbnail choices with Codex, then stop for Dan's pick.** Call `.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high` on Dan's subscription. The five slots: one real pool-shoot photo, one real studio-shoot photo, one AI-enhanced or AI-generated image of Dan on this ad's subject, and two additional AI-generated images of Codex's choice, with or without Dan. Every option has a unique design, including layout, type treatment, color and composition. Write one line describing each design first. Options 1 and 2 use a real cutout layered over a Codex background with type in code; never redraw Dan. Option 3 uses his real photo as reference, lean and shredded at the reference size, with a recognizable face. Same headline across all five unless Dan requests copy alternatives. Keep text clear of face and hair, avoid frowning photos, crop standing Speedo images at the shorts line, and omit website marks and real-photo labels on thumbnails. Produce each choice for both 16:9 and 9:16. Show one numbered review sheet with clear full-size files. **Stop here for his selection before any upload.** Do not create another thumbnail handoff or another Codex chat.
4. After the pick, upload both exact masters with `scripts/youtube/upload.js`, `--privacy unlisted --category 26 --made-for-kids false --synthetic true`. The realistic AI exercise demo inside P2's phone at about 33.77-35.77 makes synthetic=true appropriate; the labeled goal stills alone would not. Set the selected thumbnails. Read back channel `UC236gjadarHAhEhOMYNGJ9g`, `privacyStatus: unlisted`, `embeddable: true` and `processingStatus: succeeded`. At most two concurrent uploads. Inspect saved uploads before retrying an error, which can leave a partially processed duplicate.
5. Add both videos to the existing cold TRIAL campaign **24316364155** using `scripts/ads/api/dgen-trial-group.js ra13`, with a `scripts/ads/api/dgen-ads/ra13.json` based on maintained `ra05.json`. Use one RA-13 ad group containing both formats, or reuse it if it already exists. Read target CPA and audience from the live reference groups configured by the maintained template; do not hardcode an old CPA. Use the existing logo, CTA and business name. Read the live campaign state and shared budget before and after; preserve budget and never enable a paused campaign. Check all existing ad final URLs in the target/reference group, including paused ads, and keep the same top-level domain. Expected destination is `https://absbyai.com/start` with campaign `dgen-trial-ra13` and distinct `codex-9x16-vsl` / `codex-16x9-vsl` content UTMs. Verify live before applying. Do not create the historical home-versus-start pair of groups. Run validateOnly, apply, then read back the actual IDs and URLs. Run `node scripts/ads/api/client.js policy 24316364155` and retain its actual findings.
6. Record both YouTube IDs, selected thumbnails, ad group/ad/asset IDs, saved visibility, processing, destinations, budget before/after and policy status. Update `Docs/AD_VIDEO_IDS.md`, `Docs/DGEN_CONVERSION_CAMPAIGN.md`, the filed-master state, and the ra13 config/result. Mark RA-13 `uploaded` through `scripts/edit-queue/queue.py` only after both YouTube read-backs and Ads entries exist; Claude mirrors the printed write to the artifact DB under the current queue instructions. Leave a short policy-recheck board entry only while needed. Remove this handoff from the OPEN index once executed. Commit and push only this task's files under the project Git rules. The main checkout currently has other sessions' pending edits/merge issues; inspect before touching it and use a clean checkout if necessary. Do not adopt live work from other owners.
7. Report the two Unlisted video links, selected thumbnails, ad group and landing page, the unchanged budget now shared with another ad group, and actual policy status. Use the existing policy-follow-up process; do not create another per-video routine. All browser testing stays muted and ends paused. The Victory Dashboard remains paused.

## Finalization housekeeping already done

RA-13 was marked finalized on October 17. All four redundant Most Guys Abs R2/R3 copies in `Videos to Review/` were removed only after verifying matching preserved delivery masters. The now-unused RA-13 review service on port 8973 was removed. Native delivery files, review proxies, evidence and approval records remain in the delivery folder. No upload, thumbnail generation, ad creation or spend occurred while writing this handoff.

No square, shorter edit, new organic Shorts, clip regeneration or public posting belongs to this setup task. Both approved films are already under 59 seconds.

## Starter prompt

AD. Name this task Most Guys Abs AD Setup. Read `Handoffs/handoff-20261017-ra13-setup.md` and use /ad-setup for the approved Most Guys Abs R3 vertical and horizontal masters. Use the Codex subscription to generate the images. Make the five unique thumbnail choices, show me one review sheet and stop for my pick. After my pick, upload both exact approved films to YouTube as Unlisted, add them to trial campaign 24316364155 in their own ad group, verify processing, visibility, destinations and unchanged budget, run the policy check and record everything. Preserve the approved films and their recorded gate flags. Keep browser testing muted.
