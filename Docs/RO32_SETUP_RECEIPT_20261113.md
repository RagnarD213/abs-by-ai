# RO-32 setup receipt, 2026-11-13

**Setup complete and scheduled on all four destinations. Not yet published.** Live Blotato queue was176/200 before,180/200 after. No waitlist entry needed. Dan’s exact approved film and thumbnail remain unchanged. All schedules were read back and their actual saved media URLs fully downloaded and SHA256-verified. Edit Queue RO-32 is uploaded and the Drive status update succeeded.

## Approved files and consent

- Film approval 2026-11-13: “Okay, it looks good. This is approved. Proceed to setup.” Includes retaining unblurred red-cap man in the approved chest-fly shot. No film/audio changes.
- Master: `/Users/danielrose/Projects/Claude/Projects/Abs By AI/claude edited long form content/31 - I'm 41. Here Are The 10 Exercises I Do Every Week/FINAL_RO-32_Im-41-10-Exercises.mp4`; SHA256 `414b54da03280c49683dbe8d7bc4962ebceae13ab5bea16a6bbcffb3f03ef10d`, 766,808,132bytes,1920x1080,30000/1001fps,8307frames,4:37.177.
- Dan’s original round2 pick2 with revision was logged exactly once by `blind.py pick` on `_round2-real`, non-comparison real selection. Original key/exports retained.
- Revised-file approval: **“Approve it”**, replying to **“Approve the revised thumbnail 2?”**, expressly bound to `2-revised.jpg` hash below. Approval in package `setup-state.json`, `_round2-real/manifest.json` and `approval-2-revised.json`.
- FINAL thumbnail: `social media graphics/youtube/thumbnails/I'm 41. Here Are The 10 Exercises I Do Every Week/I'm 41. Here Are The 10 Exercises I Do Every Week - thumbnail FINAL.jpg`.
- **FINAL SHA256 `a144e20a6ea4b003439516a61317b83b208aa82452b55b3156226ec0b06cf6e9`**,1280x720 JPEG,474,224bytes. Exact copy of approved export. All real footage pixels; no AI generation/redraw. Headline “10 Exercises I Do Every Week”; original blue rule and all pixels below header retained. Pixel proof in `_round2-real/2-revised-pixel-proof.json`.
- Existing film/SRT backups verified in prior setup on Extreme and [Drive](https://drive.google.com/open?id=1I4l1wLycGVVfO3XGYF5bUF6RK0vmu_Iu). FINAL thumbnail additionally copied to same Extreme/Drive archives; full download SHA256 matches (`scripts/covers/ro32-20261113/setup/final-thumbnail-backups.json`).

## Verified schedule readback

| Platform | Account | Saved schedule | Central time | UTC |
|---|---|---|---|---|
| YouTube | 46963 | 6913482 | Fri Jan 29, 2027, 9 AM America/Chicago | 2027-01-29T15:00:00.000Z |
| Facebook | 47105 | 6913478 | Sat Jan 30, 2027, noon America/Chicago | 2027-01-30T18:00:00.000Z |
| Instagram @danrosefit | 67203 | 6913479 | Sat Jan 30, 2027, noon America/Chicago | 2027-01-30T18:00:00.000Z |
| TikTok | 58181 | 6913481 | Sat Jan 30, 2027, noon America/Chicago | 2027-01-30T18:00:00.000Z |


Config: `scripts/blotato/configs/ro32-ten-exercises.json`. Complete saved caption, target fields, times, account IDs, media/cover URLs and full hashes: `scripts/covers/ro32-20261113/setup/schedule-readback.json`. No duplicate RO-32 schedule; exactly four. Instagram account67203 is the shared @danrosefit destination; retired @abs.by.ai not used. Optional account-list API returned401; profile lookup is not claimed, saved target/account IDs are verified against the established shared configuration.

**Release dependency:** verify actual public YouTube release onJan29 before Jan30 noon socials. If YouTube is not public, postpone all three socials before they release. This rule is saved in config, calendar and handoff for the existing shared release checks. Scheduling today does not establish future YouTube public status. No per-video routine, native YouTube upload, Private holding upload or native scheduling. Blotato’s scheduled YouTube target creates the public release at its scheduled time; no immediate Public upload was made. No public YouTube ID exists yet.

## Metadata

Title: **I'm 41. Here Are The 10 Exercises I Do Every Week**.

Description: approved film’s actual words and routine, all13 chapters, organic root UTM `https://absbyai.com/?utm_source=youtube&utm_medium=video&utm_campaign=longform&utm_content=ro32-ten-exercises`, subscribe/SixPackAbs.com close and four hashtags. No em or en dashes. Filed at source folder `youtube-description.md` and in config. Weekly rotation is distinguished from five exercises in each workout. Voice drafted with clean `scripts/voice/write.py` calls seeded with the final transcript; only invalid internal link removed from article.

Keyword tags saved in config and source `youtube-tags.txt`: exercises I do every week, full body workout, gym workout over 40, cable crunches, leg press, hamstring curls, glute bridge machine, side lateral raises, pull-ups, T-bar rows, chest flies, cable curls, tricep pushdowns, Dan Rose Fitness. Blotato’s YouTube target has no native keyword-tags field, so native tag application waits for the public YouTube ID; not claimed applied now.

Pinned comment: **“Which of these 10 exercises are you already doing every week?”**. Saved in config; existing `youtube-pinned-comment-daily` workflow posts/pins after release. Not posted now.

Article: `sixpackabs/articles/TBD-ro32-ten-exercises.md`,1127words, `build.py --check` OK; one CTA to organic root and one verified internal link. Exact title matches config. Existing `sixpackabs-article-gap-daily` publishes after release; draft not yet public.

English SRT: `/Users/danielrose/Projects/Claude/Projects/Abs By AI/claude edited long form content/31 - I'm 41. Here Are The 10 Exercises I Do Every Week/FINAL_RO-32_Im-41-10-Exercises.srt`. Filed and backed up; apply through Studio Subtitles only after public ID exists. No burned-caption version or film change.

## Media and cover verification

Approved source admitted by `scripts/covers/ro32-20261113/setup/exact_file_gate.py`. Exact master SHA256 matches current gate2.6.3 stamp. Original stamp remains FAIL,35passing/4explained rows; no invented blanket PASS. Overrides preserved and explicitly authorized: approved bass-lift tone, continuous-take lower-third boundaries at4:13/4:19, optional sidecar/card overlap, and graphics detected as burned captions. No threshold/gate changes or new film render to clear them. Original delivery/audio stamps retained beside setup evidence.

Main YouTube/Facebook upload:163,248,308bytes, SHA256 `df21407c90a94ab4df1f86506020ea54d54fe6239b9e7ce0c1ee8f349c43b691`. Separate1080p4.5Mbps upload copy to satisfy Blotato’s size cap; approved766MB master is preserved. Same8307frames/277.1769seconds and bit-identical AAC payload,12994packets. Sampled640px picture SSIM0.992041 versus master.

Instagram:69,763,802bytes, SHA256 `f574a33f0edeac75ace8a5f725ff87171230822701e86c95e281a66c094bd394`; separate1080p1.8Mbps copy, same frames/duration and exact AAC payload, sampled SSIM0.983879. Under300MB. Portrait cover SHA256 `371827c7cfeeaaa90b0e7a5619692d0358c33678293bea2ccf181dc293d9b344` fits the full approved artwork on a1080x1920 dark real-pixel blur canvas; no text/design/subject edits or cropping. Checked at390px and for center3:4 safety; original FINAL unchanged.

TikTok:163,348,415bytes, SHA256 `da0d8c0018add02c6a5f247074dc927b87c1893d68f601ea45845e87deeee03c`. One designed frame prepended,8308frames; all8307source VCL picture payloads and12994audio packet payloads preserved. Complete decode zero errors, cover PSNR51.55dB; actual first frame visually checked. `videoCoverTimestamp:0`, AI false. Landscape cover is aspect-preserved within the center grid window with dark blurred real-pixel sides. No silent/audio re-encode or film edit.

YouTube uses exact FINAL thumbnail URL/hash. Facebook approved FINAL registered both in repository registry and live installer, schedule6913478; image hashes match. Instagram uses the fitted portrait cover. All five uploaded assets fully downloaded and SHA256/byte-count checked, and every actual saved schedule URL rechecked independently. Source cover dimensions/size decode verified.

Organic/ad guard clean before176 and after180posts; RO-32 config directly passes. No AI imagery or footage, synthetic flags false. Before/after cover audit: zero issues. TikTok queue audit recognizes6913481 as done. No speaker playback or audible listening claimed.

## Shared records and remaining release work

- Long-form calendar updated to verified four-platform schedules, exact Jan29/30 dates.
- RO-32 Edit Queue: uploaded, Drive status upload succeeded. Codex cannot write the Claude artifact fallback database; its mirror revision remains pending for the next native Claude sync, per the queue instructions. Live Drive status path is updated.
- SL-38 registered for three separate later Shorts; no production launched. Dan chooses proposed standalone lessons first; no Short before parent is public.
- Handoff and index remain OPEN for release checks only: verify YouTube public before socials, real public cover tiles, English SRT/native keyword tags, then confirm pinned comment/article routines. No thumbnail approval or setup action remains for Dan.
- Shared files are pushed using `scripts/git/safe-push.sh`; media excluded. Push outcome recorded in local setup-state.json and the delivery reply after the command completes.
