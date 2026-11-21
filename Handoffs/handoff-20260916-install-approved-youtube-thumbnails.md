# Install the approved YouTube and Blotato thumbnails

Prepared September 16, 2026. **Ready for a new installation task. Nothing installed in the design task.**

## Goal and authorization

Install the six exact approved JPGs below on their existing YouTube videos and on matching queued Blotato full-length posts wherever a custom cover is supported. Do not redesign, retouch, change text, start an A/B test, or generate new options.

Dan's final selection: “Let's go with C2: the stronger abry touch, stronger ab definition. That looks very good.” This finalizes Video 6 as **C2**, superseding C, C1 and all earlier candidates. Earlier instruction: “All the rest are finalized.” Video 8's final is the requested adaptation of Video 6B, not the earlier light-blue or standing alternatives. Starting this installation task with the prompt below authorizes installation; do not ask again for routine thumbnail replacement.

Project: `/Users/danielrose/Documents/Claude/Projects/Abs By AI`

## Exact assets and destinations

**Video numbers refer to the thumbnail review gallery, not production-project numbering. Use IDs to avoid title confusion.**

Canonical approved folder: `/Users/danielrose/Documents/Claude/Projects/Abs By AI/output/thumbnails/channel-refresh-20260916/approved-installation`

`manifest.json` contains the six exact filenames, SHA-256 checksums, dimensions, original sources and exclusions. All six were verified as 1280×720 JPEGs below 2 MB and copied byte-for-byte from the approved source files.

| Review video | YouTube ID and title | Approved choice | Filename in approved folder |
|---|---|---|---|
| 1 | `UghqHEH8yho` — Welcome to Abs by AI! | A — natural pool | `V1-UghqHEH8yho-APPROVED.jpg` |
| 3 | `Sv5wZha_a8c` — 1 Minute Ab Workout That Hits All 4 Ab Muscle Groups (At Home) | Approved medicine-ball pool revision | `V3-Sv5wZha_a8c-APPROVED.jpg` |
| 5 | `27vZC4xVkms` — 3 Minute Total Body Home Workout - Follow Along (No Talking) | Approved kettlebell pool revision | `V5-27vZC4xVkms-APPROVED.jpg` |
| 6 | `bkzT-3ENpoU` — Ab Wheel: Most Underrated Ab Exercise | C2 — stronger ab definition; FINAL | `V6-bkzT-3ENpoU-APPROVED.jpg` |
| 7 | `bwfSQopZy1w` — Every Diet You've Tried Failed for the Same Reason | Approved frowning studio revision | `V7-bwfSQopZy1w-APPROVED.jpg` |
| 8 | `b_bS9NdmL-g` — Ab Wheel Workout: 3 Sets For Stronger Abs (Do It With Me) | Exact Video 6B screenshot; white ABWHEEL WORKOUT on inset black | `V8-b_bS9NdmL-g-APPROVED.jpg` |

**Keep unchanged:**
- Video 2: `0zspIJVrv08` — Use AI To Get REAL Six Pack Abs - 6 Strategies That Work.
- Video 4: `8BaCYcGhRPY` — The Ultimate 1 Minute Ab Workout - Follow Along (No Talking).
- Excluded: `2T4LrQrmz9s` — My Top 10 Tips For Getting Six Pack Abs (At 40 Years Old), the high-view posing-trunks thumbnail.
- Shorts, other uploads, and unrelated queued posts are outside this approved set.

Video 6 C2 is an intentionally approved ab retouch. Keep the exact delivered image, including its existing text and treatment. Do not reapply general photo-edit defaults. Video 8 intentionally reuses the older 6B screenshot at Dan's explicit direction; do not swap it to the final Video 6 C2 screenshot.

## Assets and recovery

Local review: `http://127.0.0.1:8817/` if its server is still running; the files work independently of that server.
Private backup folder: https://drive.google.com/drive/folders/1SrUQHd2ksCyOg5cvlhqcfYtBh163lX6H . Use the newest **approved-thumbnail-installation-20260916.zip** package. Older review ZIPs contain rejected options; they are not the installation manifest.

Original design-time thumbnails: `/Users/danielrose/Documents/Claude/Projects/Abs By AI/output/thumbnails/channel-refresh-20260916/<youtube-id>-original.jpg`. Still capture fresh live originals before installation, since accounts may have changed.

Historical inventories: `/Users/danielrose/Documents/Claude/Projects/Abs By AI/output/thumbnails/channel-refresh-20260916/youtube-inventory.json`, `videos.json`, and `blotato-inventory.json`. These are September 16 snapshots, **not current account state**.

## Installation procedure

1. Read `AGENTS.md`, `AI_COORDINATION.md`, this handoff and the approved manifest. Claim this installation work on the board without touching other sessions. Verify the six file hashes before writing externally. Save all installation evidence under `/Users/danielrose/Documents/Claude/Projects/Abs By AI/output/thumbnails/channel-refresh-20260916/installation/`.
2. Read fresh YouTube details for all six replacements and three protected IDs. Save current thumbnails and metadata (title, description, visibility and schedule). Open Studio where needed to check thumbnail tests; preserve available A/B results/screenshots before replacing a thumbnail or removing an old/completed test. Standing authorization permits this without another approval request. Do not start another test.
3. Use the existing thumbnail setter, inspecting its current source first: `scripts/youtube/set-thumbnail.js`. It loads credentials from `~/.absbyai-secrets.env`; never print credentials. Example from the project root:

   ```sh
   node scripts/youtube/set-thumbnail.js --video bkzT-3ENpoU --file output/thumbnails/channel-refresh-20260916/approved-installation/V6-bkzT-3ENpoU-APPROVED.jpg --out output/thumbnails/channel-refresh-20260916/installation/V6-readback.jpg
   ```

   Repeat only for the six manifest IDs. `--read-only --out <path>` captures a served thumbnail without changing it. If API/Studio test handling blocks a swap, use supported browser controls as necessary; do not reupload or recreate the video.
4. Verify every YouTube change with a fresh read and rendered thumbnail inspection. A successful API response or “bytes changed” flag is insufficient. YouTube resizes/recompresses thumbnails, so do not demand a byte-for-byte match to the upload. Allow CDN propagation, retry a cache-busted image/another served size, and confirm the approved composition and text visually. Preserve titles, descriptions, visibility and schedules. Recheck all protected thumbnails unchanged.
5. Fetch a fresh Blotato schedule. Match full-length counterparts by content, media, account and campaign, not by generic words such as “ab wheel.” `scripts/blotato/danrosefit_migration.py` contains existing `api_key()` and `fetch_schedules()` helpers. Use current supported connector/API/browser cover editing; inspect its schema before writes. Back up every full scheduled record first. Change only the platform's supported cover/thumbnail field, preserving video `mediaUrls`, caption, account, target options, first comment and scheduled time. Never substitute a JPG for the video itself.
6. Re-read each modified Blotato record and verify the saved cover image and preview. If a platform cannot accept a separate custom cover, record that precise limitation; do not delete/recreate posts, bake the image into video or alter video content. If a previously queued post has already published, report its current state rather than publishing a duplicate. The approved set does not authorize editing unrelated Shorts.
7. Write `installation/INSTALLATION_REPORT.md` with per-ID result, old/new image evidence, preserved A/B results, matched Blotato post IDs/platforms, unchanged protected items, any unsupported cover limitations, and rollback paths. Back up report and evidence privately. Update the board and handoff index to reflect actual completion, leaving any genuinely blocked work explicit. Report completion to Dan with links.

## Blotato matching hints — refresh before use

These historical full-length records are also saved in `approved-installation/blotato-snapshot-hints.json` with full content/media/target fields:

| Video | Scheduled post ID | Platform / account | Snapshot scheduled time (UTC) |
|---|---|---|---|
| 7 | `4327375` | Instagram / `65632` | 2026-09-17 14:00 |
| 8 | `4413699` | Facebook / `47105` | 2026-09-20 14:00 |
| 8 | `4413701` | Instagram / `67203` | 2026-09-20 14:00 |
| 8 | `4413702` | TikTok / `58181` | 2026-09-20 14:00 |
| 8 | `4413703` | Instagram / `65632` | 2026-09-21 14:00 |

Instagram snapshots use `draft.target.coverImageUrl`. Facebook/TikTok snapshots have no separate cover field; inspect current platform support rather than inventing a field. Search fresh schedules for other matching counterparts of the six approved videos; the table is a lead, not an exhaustive current inventory. Never blanket-update all ab-wheel posts: there are many separate Shorts in the queue.

## Boundaries and verification

No new video upload, new public post, native YouTube scheduling, metadata rewrite, or app deployment is needed. Existing public videos stay public; existing private/unlisted videos keep their saved visibility. Initial Video 7 was unlisted and Video 8 private; read fresh state and preserve it. The no-Public-upload rule remains in force should an unrelated workflow arise; this task requires no uploads of video media.

Personal photos stay out of public Git repositories. Use the private Drive folder for thumbnail/evidence packages. Do not create a dashboard task automatically. Do not modify work owned by another session.

Completion means all six approved YouTube thumbnails are visibly verified; supported matching queued covers are verified; Videos 2/4/Top 10 are unchanged; preserved metadata and any limitations are documented. Do not claim unsupported or failed destinations completed.

## Recommended new task

**Model: GPT-5.6 Sol. Effort: High.** The design decisions are settled; the work is careful account updates and verification.

Starter prompt:

> Read `Handoffs/handoff-20260916-install-approved-youtube-thumbnails.md` in the Abs By AI project and install the six approved thumbnails on the specified YouTube videos and matching queued Blotato posts wherever custom covers are supported. Use the exact approved manifest, including Video 6 C2. Keep Videos 2 and 4 and Top 10 Ab Tips unchanged. Preserve existing video/post metadata and schedules, verify every saved result, and finish the installation report. The selections are final; proceed with installation.
