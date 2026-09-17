# DS-17 finalized — upload and organic setup

Updated: 2026-09-17. **Ready for a new task. Model: GPT-5.6 Sol, High effort.**

## Goal and authorization

Upload and set up the finalized dedicated Short **How To Jump Rope**, job **DS-17**, through the existing organic publishing workflow. This is instructional organic content, not an ad. Editing is complete; do not reopen the opening selection or audio treatment.

Dan approved the entire R4 on 2026-09-17:

> All right this works and this is finalized. That wasn't the jump rope clip I was thinking of but that works fine in that place and that's good. Finalize this video. Mark this as finalized in our AbsByAI edit queue and create a handoff document for Soul to upload and set this video up this in a new task

“Soul” means Sol. The edit queue is already **FINALIZED** and its Drive status file was uploaded. No upload or scheduling has happened in the edit task. This handoff authorizes the new task to perform upload/setup; do not ask again whether the video itself is approved.

## Exact approved asset

Project root: `/Users/danielrose/Documents/Claude/Projects/Abs By AI`.

- **Upload master:** `/Users/danielrose/Documents/Claude/Projects/Abs By AI/Short-form video content/ds-17_how-to-jump-rope.mp4`
- SHA256: `ad4f7b464faf588909c880de7afddf703921e84e3c597ef8bdb4333bee12dc89`
- 50,854,072 bytes; 1080×1920; 30000/1001 fps; 1,354 frames; 45.178467 seconds. H.264 with AAC. Captions already burned in.
- Frozen approved backup: `Short-form video content/ds-17-support/revisions/r4-finalized/ds-17_how-to-jump-rope.mp4`.
- Approval: `Short-form video content/ds-17-support/records/dan-final-approval-20260917.json`.
- Notes: `Short-form video content/notes-ds-17.md`.
- Full evidence and recipe: `Short-form video content/ds-17-support/`.
- Do **not** upload the `_REVIEW_540p` file, audio comparison, proposed C audio alternative, or earlier R3/toe-clip trial.

The opener is finished real sunny footage: 75 side-angle frames from source5.8s, then67 front-angle frames from16.3s. It covers the first4.738s with no header/footer. The remaining lesson is preserved. There is no AI image/clip, before/after comparison, or music in this video. Use the real-content/synthetic setting accordingly; the AbsByAI brand name does not make the footage AI-generated.

## Verification and approval boundary

Independent Astra visual review found zero defects. All50 caption onsets passed within34ms. Audio is the exact R3 AAC that Dan heard and approved. The audio artifact comparison with Muhammad remains a measured FAIL; delivery shows35 PASS/1 FAIL (`audio:stamp`)/0 NOT MEASURED/3 N/A. These results remain recorded honestly. **Dan's subsequent explicit finalization is the authority to use this exact approved file; it does not turn a failed measurement into a PASS.** Do not process the audio again, change a threshold, forge a stamp, or restart editing to pursue the old numerical failure. If an upload helper refuses it, use its documented approval route or report the precise implementation blocker; retain the approval and failed report together.

## Read and adapt the established setup workflow

Read the current project `AGENTS.md`, `AI_COORDINATION.md`, `.claude/skills/video-setup/SKILL.md`, `.claude/skills/shorts/SKILL.md` (especially cover installation), `.claude/skills/_shared/edit-queue/README.md`, `BLOTATO_QUEUE_PROGRESS.md`, and `Docs/TIKTOK_COVERS.md`.

Use the organic setup workflow for this **single dedicated Short**. Its long-form-specific steps (16:9 filing, chapters, long-form schedule and a new five-thumbnail design round) are not this task. Use current Shorts scheduling conventions and actual free queue slots. Inspect existing uploads/schedules before writing to prevent duplicates. No long-form parent release is required for this standalone tutorial.

Existing finished covers are in:

- `Short-form video content/ds-17-support/covers/instagram/ds-17_how-to-jump-rope_cover-A.png` and `...cover-B.png`
- `Short-form video content/ds-17-support/covers/youtube/ds-17_how-to-jump-rope_cover-A.png` and `...cover-B.png`

A says **HOW TO JUMP ROPE**; B says **JUMP ROPE LIKE A BOXER**. They use the same smiling studio-blue-10 photo. These assets are already built, but Dan did not separately select A versus B in his finalization. Prefer A for direct topic clarity using normal setup discretion; if a platform-specific unresolved choice truly requires Dan, prepare everything else first and ask only for that choice. Do not infer cover approval or invent a prior pick. No domain/real-photo disclosure belongs on these covers under the current thumbnail rule. Verify the installed cover, not just the file on disk.

## Execution and completion

1. Verify the master hash and saved approval. Claim only the upload/setup work on the board; leave the edit job FINALIZED until setup is actually complete.
2. Prepare a concise searchable title, description and platform captions using the real tutorial. Suggested title: **How to Jump Rope Without Tripping — Skip Like a Boxer**. Use existing organic UTM conventions and the root `https://absbyai.com`, not `/start`. Avoid adding health/result claims, AI disclosures for nonexistent AI imagery, or chapters to this45s Short.
3. Upload the full-quality YouTube holding copy **Private**. Read back `privacyStatus: private`. Never upload Public, set `publishAt`, or use YouTube native scheduling. Preserve upload receipts; do not retry a merely slow upload.
4. Queue organic release through Blotato for YouTube, Facebook, Instagram @danrosefit, TikTok and the @abs.by.ai mirror per current Shorts conventions. Blotato owns YouTube release. Inspect current capacity and collisions; do not delete someone else's scheduled posts to create room. If capacity is full, complete all independent setup, keep YouTube Private and record the remaining queue blocker.
5. Every queue config carries `content_type: organic` and the actual master source path. Run `python3 scripts/blotato/ad_guard.py --scan` before and after writes; use the established guarded queue tools. Install and verify covers, including TikTok's cover-at-upload requirement and the actual YouTube Shorts grid cover. Any platform-only derivative must preserve the approved sound and content; keep it separate from the approved master and record its provenance.
6. Read back saved visibility, accounts, schedules, captions, media and cover settings. Record YouTube URL/ID, all schedule IDs, dates/times in America/Chicago, and any genuine outstanding blocker in a setup receipt and `BLOTATO_QUEUE_PROGRESS.md`.
7. Only after the Private YouTube upload and required Blotato schedules are verified, run `python3 scripts/edit-queue/queue.py set DS-17 uploaded --by Codex --note '<YouTube ID, release date, setup receipt>'`. Verify the Drive upload message. If setup is incomplete, retain FINALIZED with a precise note; do not falsely mark UPLOADED.
8. Commit/push only this task's docs/scripts/configs, never media or credentials. Preserve concurrent changes. Follow the normal deployment verification rule. Remove this handoff's open-index entry and its setup board entry when complete; do not add a dashboard row. Tell Dan where and when the video will release.

## Starter prompt

Read and execute `Handoffs/handoff-20260917-ds17-finalized-upload-and-setup.md`. DS-17 R4 is finalized by Dan. Upload the approved full-quality master and complete its organic YouTube/Blotato setup, preserving the approved edit and audio. YouTube holding upload must be Private, with release through Blotato. Verify covers, schedules and saved visibility, then mark DS-17 uploaded only when setup is complete.
