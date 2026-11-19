# Got Abs? You need to see this. | RO-28 setup receipt

November 18, 2026. Dan approved the R1 re-edit and selected X1, Studio portrait. His later picks set a one-time Thursday release. All four Blotato schedules were read back from the live queue.

| Platform | Thursday, Nov 19, America/Chicago | UTC | Blotato schedule ID |
| --- | --- | --- | --- |
| YouTube | 10:00 AM | 16:00 | 7163158 |
| Facebook | 12:00 noon | 18:00 | 7163160 |
| Instagram @danrosefit | 12:00 noon | 18:00 | 7163161 |
| TikTok | 12:00 noon | 18:00 | 7163163 |

Queue count 192 before, 196 after. No other posts moved. The four 9 AM Rear Delt Flys schedules (FB 6463978, IG 6463980, TT 6463982, YT 6463983) matched before and after. Original RO-28 socials 6213006, 6213007 and 6213008 were absent from the live queue. Confirmed exact saved caption, platform target, cover settings, account and time. The full cover and organic queue audits found zero issues.

## Film and X1

- Approved master 1920×1080, 387,228,582 bytes, 385.962 seconds, 11,567 frames. SHA-256 `d0d0fdbdb0c55ac066116d27647aeed88990812f2cfa456844972a31d297d7bc`. YouTube and Facebook use these exact bytes.
- X1 review JPEG copied byte for byte for YouTube and Facebook, 1280×720, 248,031 bytes. SHA-256 `8ef7f55e021daedd5a609c9a993be70eed07da87d37516190660f26d68bb7904`. The active Facebook installer on M2 has schedule 7163160 and a matching image. It applies the cover to the Reel after publication.
- Instagram and TikTok portrait cover 1080×1920, 973,647 bytes. The whole approved composition is fitted into the portrait with a dark background extension. SHA-256 `0885b7f838b1ac97cb9263d22a9964105b40fac38b386d6bb4ee13b60242d57d`.
- Instagram uses the 97,021,165-byte 1080p delivery copy, with the same 11,567 frames, duration and AAC content as the master. TikTok uses the 212,001,784-byte 1080p delivery copy with one approved cover frame at the start, timestamp 0 and all 18,093 audio packets. Full decode succeeded. The first frame measured 53.42 dB against the expected cover and kept the full X1 design in the central 3:4 crop. This check was silent.
- Downloaded and SHA-256 checked all intended Blotato uploads. Downloaded the URLs from the saved schedules and verified all four video hashes and both scheduled cover image hashes.
- Exact film, SRT, chapters, and platform covers filed in the project under `Claude Content Videos/Got Abs You Need To See This - RO-28` and on Extreme under `Claude Content Videos/Got Abs Zepbound reedit - RO-28 R1`. Project and Extreme file hashes matched. Drive checksum check found 10 matching files and zero differences. A separate full download from Drive confirmed the exact master and all four cover SHA-256 hashes. [Drive backup](https://drive.google.com/open?id=1hNt6fgNVtq7Y1k2GphlKmwAsU1cFMffX)

## Metadata and release checks

- Exact title, neutral description, six chapters with original timestamps, hashtags, nine YouTube keyword tags and exact engagement prompt are saved in `scripts/blotato/configs/ro28-got-abs.json`. The scheduled YouTube description and all three captions include the approved neutral treatment. The ad-related drug and imagery exclusions were checked against the public copy and X1. The film itself retains its approved words and graphics.
- Planned YouTube comment: “What was tougher for you, losing the weight or keeping it off?” The same question is in the three captions and saved Facebook/Instagram first-comment fields. The release check can post/read back the YouTube owner comment after public verification. The visible pin belongs to the existing YouTube pin routine. Blotato does not transfer native YouTube keyword tags. The release check applies the saved tags and uploads the filed English SRT once the public ID is confirmed.
- The scheduled release check is loaded on M6 as `com.absbyai.ro28-release-check`. It reads the exact title, channel, release time, tracking marker and public status through the YouTube API. If the public upload is still unconfirmed at 11:55 AM Central, it holds only these three socials, records their saved payloads, and can requeue them in a clear noon slot once the video is public. It checks the site for the exact public ID and records page and article status. Its private operational evidence is under `~/Projects/_edit_work/ro28-got-abs-setup/`.
- Article: `sixpackabs/articles/TBD-ro28-got-abs.md`, 850 words, `build.py --check` OK. The existing WordPress sync makes the video page when it sees the public video. The daily article routine uses the exact title to install the prepared copy. Preflight confirmed original `eLV6EluvyD0` is Private via owner YouTube API, absent from public site home and /videos/, and its former URL returns HTTP 404. The replacement page does not yet exist.
- The live public video, public cover tiles, native YouTube tags, subtitle track, visible pin and published article are future verification steps. The Edit Queue status reached Drive. The fallback native artifact mirror is still pending its existing writer.

## Paid engagement

Dan authorized the seven paid placements on Nov 18. M6 LaunchAgent `com.absbyai.ro28-engagement-release` starts checking at 10:00 AM Central on Thursday, Nov 19, and checks every minute until it verifies the exact public YouTube upload for Blotato schedule 7163158. It matches the title, owner channel, publication time and tracking marker before submitting ads for the returned YouTube ID.

| Suffix | Campaign | Ad group | Final URL |
| --- | --- | --- | --- |
| tier1 | 24163535721 | 206274722584 | https://absbyai.com/start |
| tier2 | 24122099676 | 197884856303 | https://absbyai.com/start |
| us | 24422704023 | 201123318425 | https://absbyai.com/start |
| rmktg-site | 24316408288 | 200887799219 | https://absbyai.com/start |
| rmktg-yt | 24316408288 | 209156230708 | https://absbyai.com/start |
| us-rmktg-site | 24437265255 | 201297112505 | https://absbyai.com/start |
| us-rmktg-yt | 24437265255 | 197223280930 | https://absbyai.com/start |

- All placements use the same 5 neutral headlines, 3 long headlines and 3 descriptions read back from the seven prior RO-28 placements. All seven use YouTube in-feed and the live /start page on the existing ad groups’ domain. The destination returned HTTP 200 and passed the copy scan.
- On Nov 18, Google Ads account `342-717-0837` accepted `dryRun` for seven enabled ad creates with an existing public video asset, and for seven enabled ad creates plus a new public video asset. The replacement ID becomes available at release. Live readback before and after both dry runs showed zero enabled ads across the five campaigns, all 45 ads on Dan’s list paused, and tier 2’s target CPA and CPC fields at 50,000 micros.
- The title was removed from the general skip list. The scheduled M6 job owns this upload. The regular worker creates fresh placements for other videos in these campaigns as paused from midnight Nov 19 through noon Nov 21 Central. If the prior worker version creates an enabled placement during the launch, the M6 job can pause that new worker-created ad as it submits RO-28.
- Live verification will add the YouTube ID, timestamp and all seven Google Ads IDs below and push the receipt. The job reads back the ad copy, asset, final URLs, enabled statuses, protected pauses and tier 2 bid. Detailed evidence is under `~/Projects/_edit_work/ro28-got-abs-setup/`. The original release check still handles the noon socials and site.
