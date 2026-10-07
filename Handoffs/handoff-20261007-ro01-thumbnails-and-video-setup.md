CONTENT | RO-01 | Keep Your Muscle LFC Setup

# RO-01: thumbnails, upload and setup

Written 2026-10-07. Dan approved the complete R10 film: "All right this is looking good. This is finalized and approved." The edit is locked. Edit Queue job `RO-01` is `finalized` (revision 7). This is one Claude `/video-setup` task: make five thumbnail choices, show them to Dan and stop for his pick, then finish the upload and setup. The overnight edit dispatcher stays paused.

**Recommended model:** Claude Opus 5.5, medium effort. **Sidebar name:** `Keep Your Muscle LFC Setup`. **Use the Codex subscription to generate the images.** Every generated still uses `.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high`; no paid image API.

## Approved files

All paths are local and already final. Verify the master hash before making copies. Do not re-edit or re-render the film.

| Item | Exact file |
| --- | --- |
| Master | `/Volumes/Extreme/_edit_work/ro01/revision10/full/RO01_MASTER_R10_REVIEW_1080p.mp4` |
| Subtitles | `/Volumes/Extreme/_edit_work/ro01/revision10/full/RO01_R10_FINAL.srt` |
| Chapters | `/Volumes/Extreme/_edit_work/ro01/revision10/full/RO01_R10_CHAPTERS.txt` |
| QA report | `/Volumes/Extreme/_edit_work/ro01/revision10/full/RO01_R10_QA_REPORT.md` |
| Checksums | `/Volumes/Extreme/_edit_work/ro01/revision10/full/SHA256SUMS.txt` |

The master is 1920x1080, 30000/1001 fps, 11:52.812, 802,596,301 bytes. SHA256: `fa99ac5b8b7dfdd704d3256aa54c156acc842b54e77e3814e2f149579c7b631f`. The SRT has 248 cues and the chapters have 9 entries. Keep their timing with this exact master.

The audio gate passes all 13 rows. The general delivery gate retains three raw flags for the preserved ending fade, deliberate picture cuts and teaching graphics mistaken for burned captions. The exact-file QA and independent review visually cleared those flags. Dan approved this file with that report available. Do not change a gate threshold or quietly substitute another master. If a setup script refuses its gate stamp, report the exact refusal and stop that dependent step.

## Classification and thumbnail approval

This is organic long-form CONTENT. The ending says, "So go to AbsByAI.com right now and generate a picture of yourself with abs." It does not tell viewers to tap an ad button. Confirm classification against the final audio before any scheduling. H04 at 0:00 and B01 later in the film are realistic AI motion from Kling, with an on-screen `AI-GENERATED` label. Set the platform synthetic-media flag to true.

Read `.claude/skills/_shared/VIDEO-RULES.md`, `.claude/skills/_shared/IMAGE-GENERATION.md`, the current `/video-setup` skill and `/youtube-packaging` before building the thumbnails. Make exactly five distinct 16:9 options for this film: one real pool-shoot photo, one real studio-shoot photo and three different AI-generated designs of Codex's choice. For a real photo of Dan, generate the background only and composite his unchanged real cutout and type in code. Follow the Speedo crop, face and hair clearance, photo-selection and no-end-mark rules. Use a single concise thumbnail line across the options unless Dan asks for copy variations. Show all five on one review sheet and **stop for Dan's pick**. If he picks two, preserve both for a YouTube thumbnail test after release.

## After Dan picks

1. Follow `/video-setup`: file the approved master and SRT in the project, on Extreme and on Google Drive. Set the new Drive folder to anyone-with-link view. Re-hash copies against the original.
2. Prepare a searchable title, description and social copy grounded in the approved film. Use the nine exact chapters, an organic AbsByAI.com link with UTM tags, and the appropriate AI-footage disclosure. Read the current writing rules before drafting. Do not introduce claims or offers that the current site does not support.
3. Check `BLOTATO_QUEUE_PROGRESS.md` and the live schedule, then use the next open long-form slot. Organic YouTube is created by Blotato at release. Do not make a direct YouTube upload or native YouTube schedule. Queue YouTube, Facebook, Instagram `@danrosefit` and TikTok, and read back every saved schedule. Do not queue `@abs.by.ai`.
4. The 765 MiB master exceeds Blotato's 400 MB cap. Make a platform copy under that cap using the skill's VideoToolbox method at low priority, keeping the approved audio. Compare duration, frame count and sound against the master. Give TikTok its cover-first copy before scheduling. Check that each account accepts the full 11:52 film; report a refused platform instead of claiming it is queued.
5. Write the setup receipt with file hashes, approved thumbnail, schedule IDs, release time, account list and Drive folder link. Set Edit Queue `RO-01` to `uploaded` only after the Blotato schedules read back. Mirror the queue row to the Edit Queue artifact if its data tool is available. Add the RO-01 organic Shorts job to List 2 as the setup skill requires; do not make an ad vertical, square or one-minute cut.
6. Prepare the sixpackabs.com article from the finished film in this setup task. After release, confirm the public YouTube thumbnail, upload the English SRT in Studio, run a thumbnail test if Dan picked two, and publish and verify the article. Record those post-release steps on the coordination board if they cannot occur yet. Check RO-12's outstanding WATCH NEXT link to RO-01 once this video is public.

The Edit Queue's previous `How To Keep Your Muscle On Zepbound` title is its original working title. Package the final film under its approved `How To Keep Your Muscle While You Lose Fat` title unless Dan chooses another title during thumbnail review. Preserve the film itself unchanged.

## Starter prompt

Name this task `Keep Your Muscle LFC Setup`. This is CONTENT, RO-01 long-form. Read `Handoffs/handoff-20261007-ro01-thumbnails-and-video-setup.md` and run `/video-setup` on the approved R10 master with the exact SRT and chapters. Use the Codex subscription to generate the images. Make five thumbnail choices: one real pool photo, one real studio photo and three distinct AI designs. Show me the five on one sheet and stop for my pick. Then file and back up the master, prepare the packaging, schedule the organic video through Blotato on YouTube, Facebook, Instagram `@danrosefit` and TikTok, verify the saved schedules, and record the setup. Keep the approved R10 film unchanged.
