# Finished ads on YouTube: video ids for ad campaigns

Every finished ad master in `Muhammad Ad Videos/` and `Zeeshan Ad Videos/` is on the **Abs by AI**
channel (`UC236gjadarHAhEhOMYNGJ9g`) as an **unlisted** video. Paste the link into Google Ads,
which only takes videos that are on YouTube. Uploaded 2026-09-10 with `scripts/youtube/upload.js`,
category 26, not made for kids, "altered or synthetic content" = yes (the ads show AI-generated
goal images of Dan). Every video was read back after upload: processed, HD, embeddable.

| Ad | Version | Aspect | Length | Link | Approved? | Thumbnail |
|---|---|---|---|---|---|---|
| Ad 2 Stop Wasting Money On Nutritionists | Claude vertical of Muhammad's V2 | 9:16 | 4:37 | https://youtu.be/7XgHxn59Tsg | yes (09-08) | `ad2-vertical-7XgHxn59Tsg_C-jeans-black-9x16-FINAL.jpg` (set + read back 09-10) |
| Ad 2 Stop Wasting Money On Nutritionists | Muhammad V2 HD | 16:9 | 4:37 | https://youtu.be/Dtk5knWM7c8 | editor final | `ad2-muhammad-16x9-Dtk5knWM7c8_C-jeans-black-FINAL.jpg` (set + read back 09-10) |
| Ad 1 This Picture Got Me Abs | Muhammad | 16:9 | 3:53 | https://youtu.be/lf46ytHacss | editor final — **also the interim video on `absbyai.com/start` since 2026-09-10** (`ABS_START_VIDEO` in `public/site-video.js`) | O1 dark studio (set + read back 09-10) |
| Ad 1 This Picture Got Me Abs | Zeeshan (4K master) | 16:9 | 4:10 | https://youtu.be/1oEcwdp21Fg | editor final | O1 dark studio (set + read back 09-10) |
| Ad 1 This Picture Got Me Abs | Claude vertical of Muhammad's | 9:16 | 3:53 | https://youtu.be/Iz0u8KHRbyE | yes (09-10) | O1 dark studio (set + read back 09-10) |
| ~~Ad 1 This Picture Got Me Abs~~ | Claude vertical of Zeeshan's | 9:16 | 4:10 | ~~https://youtu.be/rimBWjT9-oo~~ | **REJECTED 09-10 — do not use** | — |
| ~~Ad 1 This Picture Got Me Abs~~ | Claude vertical of Zeeshan's, cutdown | 9:16 | 0:56 | ~~https://youtu.be/JOZVk4_HDwQ~~ | **REJECTED 09-10 — do not use** | — |

Thumbnail files live in `social media graphics/youtube/thumbnails/<Ad folder>/` (git-ignored). Swap one with
`node scripts/youtube/set-thumbnail.js --video <id> --file <jpg> --out readback.jpg` — it sets, waits for the
new image to serve, and saves the read-back. A 9:16 thumbnail is served as 1280×720 with a blurred copy of
itself filling the sides (not black bars).

⚠ The two struck rows are byte-identical (sha256) to the files Dan rejected for processed audio on 2026-09-10
(corpus entries `ad1zee-vertical-processed-audio` and `…-59s-…`). They were uploaded before that rejection
was known. The upload token cannot delete videos, so Dan removes them in Studio. When the rebuild is
approved, upload it as a NEW video and add a row here.

Each description links `absbyai.com/start` with `utm_source=youtube&utm_medium=video_ad&utm_campaign=<slug>`
(`ad2-claude-9x16`, `ad2-muhammad-16x9`, `ad1-muhammad-16x9`, `ad1-zeeshan-16x9`, `ad1-muhammad-claude-9x16`,
`ad1-zeeshan-claude-9x16`, `ad1-zeeshan-claude-9x16-59s`). The ad's own final URL in Google Ads is what
counts. The description link only matters if a viewer opens the video page.

⚠ Known compliance flags (from the review notes): Muhammad's Ad 2 shows the app's email-capture
screen at 3:12 and 3:22, and Zeeshan's Ad 1 at 3:09. Our 9:16 rebuilds inherit whatever their
source shows.

When a new ad goes final, upload it the same way and add a row here. Replacing a video means a
new id, so the ads pointing at the old id have to be updated in Google Ads.
