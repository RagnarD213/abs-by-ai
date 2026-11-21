# CONTENT, long-form: Top 1 Percent LFC Setup

Written 2026-10-17 by Codex. **Start now:** make five thumbnail choices, show them together, and stop for Dan's pick. After that pick, run `/video-setup`. Do not edit the approved film or produce full-film vertical/square adaptations. Shorts extraction is a separate job.

**Recommended model:** Claude Opus 5.5, High effort, for this combined design, packaging and setup task. Use the Codex subscription to generate the images. Every generated still uses `.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high`. Sidebar name: **Top 1 Percent LFC Setup**.

## Approval and exact state

Dan approved the complete R5 film as-is on 2026-10-17:

> All right this looks great. This is approved. Go ahead and finalize this and give me the handoff for setup

Approval record: `Handoffs/video-editing/RO-26-R5-approval.json`. R5 is finalized, not uploaded, scheduled or published. The edit queue is `finalized`, rev 23, and its Drive status JSON was uploaded. That status sync did not upload the film. Claude's artifact-db mirror remains to be updated from the current queue export with its version guard, then mark-synced if applicable. No thumbnail is selected and no release date has been chosen. The editing task has finished; this handoff does not authorize another revision round.

## Exact approved files

Project primary folder:
`/Users/danielrose/Documents/Claude/Projects/Abs By AI/Codex Content Videos/Top 1 Percent - RO-26/`

Verified byte-identical backup folder:
`/Volumes/Extreme/Codex Content Videos/Top 1 Percent - RO-26/`

Master: `Top 1 Percent | codex | 16x9 | RO-26.mp4`
- SHA256: `395cd8fb4c99d0c235e9df691c8256e333d21a0f4efa09b60be53126fd6d24ce`
- 169,874,229 bytes; 5:03.7367667; 1920x1080; H.264; 9103 frames at 30000/1001; AAC stereo 48 kHz.
- Re-hash the master before setup. Preserve it exactly. It is already below the current 400 MB Blotato and 300 MB Instagram media caps; check current platform requirements before making any needed derivative.

Subtitle sidecars, all adjacent:
- `Top 1 Percent | codex | 16x9 | RO-26.srt`, 111 cues, SHA256 `149d655016e8e82a5401e5c4ddef39f004a677dc14b21003d5fb9580a30d2a08`.
- `Top 1 Percent | codex | 16x9 | RO-26 - positioned.ass`, SHA256 `01f654472445b3fc9ab8ff00bad239572442e813da2cfaf90c1e0a93c196d698`.
- `Top 1 Percent | codex | 16x9 | RO-26 - positioned.vtt`, SHA256 `aed1da86f09dab564b73e38cffd2bc529c003a8a6d84593c7b3f0c6f630e0082`.

SRT cannot preserve positions. ASS/VTT keep the opening cue above the photo and recap captions below the card. Do not burn subtitles into the master. Preserve the audible "can't" correction.

The same folder includes `FINALIZATION.md`, `approval.json`, `finalization-manifest.json`, the approved edit sheet, historical exact-file gate stamps, `Top 1 Percent LFC R5 - quality report.md`, `Top 1 Percent LFC R5 - independent review.md`, `Top 1 Percent LFC R5 - QA evidence.zip`, and `recipe/` with the cut map, word map, configs, scripts, finished ASR and final work packet. The original delivery receipt describes the pre-approval review filenames; the finalization manifest maps final names and hashes. The old review service on port 8982 is retired after approval. Use the final delivery folder.

Work and full evidence: `/Volumes/Extreme/_edit_work/ro26/round5/`. Original R2/R3/R4 masters and graded segment caches remain unchanged. Superseded `candidate-01` is not the approved film. Reproduction source: `Media/codex-video-trial/artifacts/ro26-round5-recipe/` and its delivery-folder copy. Media stays out of git.

## Read before work

Read live `AGENTS.md`, `.claude/skills/_shared/VIDEO-RULES.md` in full, `.claude/skills/video-setup/SKILL.md`, `.claude/skills/youtube-packaging/SKILL.md`, `.claude/skills/_shared/IMAGE-GENERATION.md`, `Docs/memory/model-routing-plan.md`, and the current Blotato queue/waitlist/rules. Current rules supersede older skill recipes. Run `scripts/git/drift-check.sh` first. Do not access the paused Victory Dashboard, restart the edit dispatcher, or create a per-video automation.

## Five thumbnail choices, then stop

Follow VIDEO-RULES, "Thumbnails: the five, each its own design, always made by Codex." Generate every image through the Codex subscription helper above. Make five genuinely distinct compositions, type treatments and palettes. State a one-line design plan per option before building; the two real-photo options must also differ from each other. Use the same concise headline across all five unless Dan asks for copy alternatives. Choose packaging from the actual film, without inventing claims.

1. A real pool-shoot photo of Dan from `photos/pool shoot | 7-31-26 | dan | mindi/`, with finalized picks/cutouts under `photos/finalized social media photos/` and `_cutouts/`.
2. A real studio-shoot photo from `photos/studio shoot | 8-28-26 | dan | mindi/`, using the same finalized real-photo sources.
3. An AI-enhanced or AI-generated Dan, tied to this film's transformation/story. Supply a real face/body reference; keep him lean and the same size as the reference. Inspect identity before delivery.
4. An AI-generated concept of Codex's choice, Dan or not.
5. A second AI-generated concept of Codex's choice, Dan or not.

For the first two, preserve the actual person and body pixels using the real cutout, generate the background, and set type in code. Do not redraw him. Follow waistband crop rules for pool photos and the packaging skill's face/hair clearance. Real pool/studio images are not the film's labeled AI clips. Thumbnails carry no AI/real-photo label or AbsByAI.com watermark. Follow current packaging rules if newer.

Save sources, build scripts, five options and a single comparison sheet under `social media graphics/youtube/thumbnails/Top 1 Percent/`. Inspect the rendered options and text clearance yourself. Show all five with short descriptions and **STOP for Dan's pick before any media upload or scheduling**. He can choose one or two for a later YouTube A/B test. Final selected JPEG: 1280x720, under 2 MB.

## Content and previous-video dependency

This is organic content. The film tells Dan's story of improving his life through four actions: working out every morning, taking nutrition seriously, starting a business, and learning martial arts. The closing thanks viewers, asks them to subscribe, and directs them to the previous video. There is no tap-the-button ad CTA. Still perform setup Step 0 and run `python3 scripts/blotato/ad_guard.py --scan` before and after Blotato changes. Set `content_type` to organic and retain the actual source path.

Working title: **I'm 41. My Life Is Top 1%. How I Did It.** The working title is context for packaging, not a new promise or an instruction to skip the packaging workflow.

**Promised previous video:** both the opening and closing refer to **"I'm 41. I Wasted My Life" (RO-25)**. Recheck its actual final title, public URL and live release status. At handoff writing its board entry still described R6 components building, not a released full film. Prepare the thumbnail and package now, but do not publish RO-26 ahead of RO-25 or invent the promised URL. If it is not public/queued ahead of this film, record release ordering as the remaining setup dependency and resolve it against the live queue. The edit approval remains complete.

Read `recipe/finished-asr.json`, `recipe/cut_map.json` and the exact final film for description and chapters. Draft anchors to verify against speech: 0:00 introduction; about 0:38 workout, 1:27 nutrition, 2:12 business, 3:31 martial arts; 4:18 four-action recap; 4:44 previous video/closing. These are draft chapter anchors, not approved final chapter copy.

Approved graphic text/design remains locked. The recap says **THE FOUR THINGS I DID RIGHT**, subtitle **Four action steps to start today**, and its four approved actions. The animation is continuous Soft Blue Light HyperFrames 0.8.97 at 4:18.158–4:43.817. The cleaned repeated-take join is 4:10.283. Do not change any graphic, voice C, grade B, real-photo label, approved AI clip or original G01–G04 asset.

Realistic generated workout and nutrition clips and the Hinge illustration are in the film. Preserve provenance and existing AI labels. Use `ai_generated: true` for TikTok/Blotato and YouTube's altered/synthetic flag under current rules. Three real photographs remain real; do not reclassify them because earlier internal provenance metadata was corrected. Consult the approved edit sheet for exact sources and the description's disclosure sentence.

## Quality review and approval are separate records

The complete exact-file gate 2.6.1 remains **FAIL: 31 PASS / 8 FAIL / 0 unmeasured, 39 rows**. Strict audio 2.0 tone/artifact measures fail; matching untreated do-no-harm comparison passes. No numeric result was changed on approval. Other flags cover style coverage/static run, loose headroom, two cut metadata flags, numeric splice flags, plain-SRT card placement and the three inherited crop flashes. The sheet validator separately flags P06, an actual moving ab-wheel shot that falls under the existing real-moving-footage label exception.

Fresh independent GPT-6 Sol High review completed 19 scenes, all 9 freeze flags, 44 native boundary strips/pairs and 100 image verdicts. It also assessed the complete 68-frame workout and 150-frame nutrition action sequences; no concrete retained action defect was found. Three inherited three-frame crop flashes remain at 2:02.823, 2:49.536 and 3:31.178. Full private audio-listener coverage and final AAC packet identity are documented. No continuous human audiovisual watch is claimed. Read the actual reports for limits and findings.

Dan saw the complete review disclosure and approved the exact film as-is. Do not reopen these disclosed creative findings or claim they were fixed. Do not relabel FAIL stamps as PASS, invent a waiver stamp, or bypass a setup script. If a setup tool actually refuses an existing stamp, record the exact refusal and ask only for the concrete necessary resolution. Do not run another whole editing/gating cycle just to overwrite known results.

## After the thumbnail pick: run current /video-setup

- Verify project and Extreme files, then make the standard Google Drive backup under `Codex Content Videos/Top 1 Percent - RO-26/`, anyone-with-link view access. Film backup to Drive has not happened yet. Preserve the master hash and record all backup links.
- Finish title, description, verified chapters, tags, AI disclosure and pinned question comment. Put `pinned_comment` in the Blotato config for the existing routine. Use the root `https://absbyai.com` with the current platform UTMs, not `/start`. Include the real previous-video link once available.
- Write the 800–1500 word sixpackabs.com article draft now through the current Dan-voice writing workflow, run its build check, and record it in the receipt. Existing routines publish it after YouTube is public. No new automation.
- Query the live queue and current limits. **YouTube first: an unoccupied Sunday at 9 AM America/Chicago, one long-form per week, after RO-25.** Facebook, Instagram @danrosefit and TikTok no earlier than the following Monday 9 AM and only after YouTube is verified public. Use `scripts/blotato/longform_queue.py` and live current rules. No date is reserved here.
- **Never make a YouTube Private holding upload, upload Public manually, or use native YouTube scheduling.** Blotato creates the single public video at release time. Any captions, optional thumbnail A/B and end-screen work requiring the YouTube ID are post-release tasks in the existing routine/receipt.
- If Blotato is full, finish the package, required media uploads/config/article/receipt and add it to `scripts/blotato/video_waitlist.json`. The existing daily refresh routine queues it when room opens. Do not delete queued posts or create a per-video reminder/routine. Mark the edit queue `uploaded` only once actually queued, following current queue rules.
- Preserve the master. If TikTok needs its cover baked into frame zero, make a separate cover-first platform copy, set cover timestamp 0 and inspect the actual first frame. Do not mistake that derivative for the approved source master.
- Run cover audit before and after. Download/decode the exact YouTube/Instagram cover URL and compare to Dan's selected asset; YouTube JPEG must be under 2 MB. Register/install the Facebook cover and exact caption prefix via the current registry. Queue/API success is not actual public-tile verification. Use the existing cross-platform monitor for post-release verification and repair; record any unobserved checks honestly.
- Write `Docs/RO26_SETUP_RECEIPT_<date>.md` with exact files/hashes, selected covers, live media URLs/config, title/slug, previous-video URL/dependency, scheduled or waitlist state, backups, article check, subtitle plan and post-release checks. Update the existing queue/board records for actual actions. Register the separate SFL extraction job under current rules; do not render Shorts within this setup task.

## Coordination and sync

Other sessions have live edits in shared queue/index/board/QC files. The R5 edit code and receipt are committed locally; safe-push was blocked by live owners. Do not adopt their work or use whole-repo staging. Use `scripts/git/safe-push.sh -m "message" -- <your files>` only, inspect ownership and retry under current two-hour rule. Local final files and exact approval record are authoritative while sync is blocked. The local QC corpus records this approval without changing the gate's FAIL result. No threshold changes were made.

This finalization did not upload media to Drive/platforms, choose a thumbnail/date, create a new task or start setup. The setup handoff is ready to start now with thumbnails and waits for Dan's pick before uploads.

## Starter prompt

Read Handoffs/handoff-20261017-ro26-thumbnails-and-video-setup.md in the Abs By AI project. Name this task "Top 1 Percent LFC Setup". This is CONTENT long-form; I approved the exact R5 film. Use the Codex subscription to generate the images. Start now with five thumbnail choices, each a unique design: one real pool photo, one real studio photo, one AI-enhanced or AI-generated image of me, and two other AI images of Codex's choice. Show all five together and stop for my pick. After I choose, run /video-setup. Preserve the approved film, verify the promised RO-25 previous-video link and release order, and follow the current Blotato rules.
