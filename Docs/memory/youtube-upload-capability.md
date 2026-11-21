---
name: youtube-upload-capability
description: "Claude CAN now upload video to the Abs By AI YouTube channel — scripts/youtube/upload.js + YOUTUBE_REFRESH_TOKEN; supersedes the old \"Claude cannot upload, 10 MB cap\" blocker"
metadata: 
  node_type: memory
  type: project
  originSessionId: 2e38e42c-56c9-43f2-99b1-70197a934707
  modified: 2026-09-10T19:27:42.992Z
---

Built 2026-09-09. `scripts/youtube/upload.js` does a resumable YouTube Data API upload of any
size, so the 10 MB Chrome-extension `file_upload` cap no longer blocks video uploads. This
**supersedes** the standing "Claude cannot upload them anyway" note that blocked long-forms 02 + 03.

```bash
node scripts/youtube/upload.js --file "path/master.mp4" --title "…" \
  --description-file notes.txt --privacy unlisted --category 26 --made-for-kids false
```

- Token: `YOUTUBE_REFRESH_TOKEN` in `~/.absbyai-secrets.env` (scopes `youtube.upload` +
  `youtube.readonly`), minted through the **OAuth Playground redirect** — the ONLY redirect URI
  registered on client `768453214640-2tjpood…`. `http://localhost`, oob and absbyai.com URIs all
  return redirect_uri_mismatch, so re-minting must use
  `redirect_uri=https://developers.google.com/oauthplayground`, then exchange the `code=` out of
  the landing URL by curl before the Playground page consumes it.
- **Brand-account trap:** at consent Google shows a second chooser — pick **"Abs by AI" (YouTube)**,
  not `danroseconsulting@gmail.com`, or the token controls the personal channel and the upload lands
  on the wrong one. The script calls `channels.list?mine=true` and prints the channel BEFORE sending
  bytes for exactly this reason.
- The app is unverified, so the consent flow passes through "Google hasn't verified this app" →
  Advanced → "Go to Abs By AI (unsafe)".
- **Gate (CLEARED 2026-09-09):** the YouTube Data API v3 is now ENABLED on Cloud project `768453214640`
  (Dan clicked it). Claude is policy-blocked from the Google Cloud Console, so if a future project ever
  needs the same switch it is Dan's click at
  `console.cloud.google.com/apis/library/youtube.googleapis.com?project=768453214640`.
- First upload through it: the website conversion video, unlisted `CwEGFxpIM-E`, 423 MB in ~80 s at
  ~5.5 MB/s.
- **Scheduling + thumbnails added 2026-09-10:** `--publish-at 2026-09-13T14:00:00Z` (uploads private,
  goes public at that time), `--thumbnail file.jpg` (set after upload), `--synthetic true|false`.
  YouTube is scheduled HERE, not through Blotato: Blotato caps uploads at 400 MB and every post
  spends one of its 200 plan slots. Not possible with this token (no `youtube.force-ssl`): pinned
  comments, playlists, caption upload, thumbnail Test & Compare — those stay in Studio.
- **Daily quota is not the limit we feared:** 13 uploads went through on 2026-09-10 (6 ab-wheel + the
  7 ad masters, ~2.3 GB in ~8 min) with no quotaExceeded, so the project's quota is above the default
  10,000 units (≈6 uploads). The ad ids live in `Docs/AD_VIDEO_IDS.md`.

**How to apply:** for any "put this video on YouTube" task, use this script rather than telling Dan
he has to upload it. Related: [[longform-delivery-location]], [[deploy-drops-locked-holds]].
