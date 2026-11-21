---
name: tiktok-cover-frame-0
description: "TikTok's API takes no cover image — only a timestamp — so a designed cover must be built into frame 0 of the video; a posted video's cover is only editable for 7 days, in the phone app"
metadata: 
  node_type: memory
  type: reference
  originSessionId: c6c20195-c463-494e-afa8-3cf77e84b1a9
  modified: 2026-09-17T20:21:23.490Z
---

**TikTok's Content Posting API has no cover-image field.** Its only cover control is
`video_cover_timestamp_ms`, a timestamp *into the video* (Blotato target field:
`videoCoverTimestamp`). Instagram's API *does* take a real image (`coverImageUrl`), which is why
the same short can show a designed cover on Reels and a mid-sentence screenshot on TikTok.

**Send nothing and TikTok uses frame 0.** Measured 2026-09-17 on @absbyai: three published
videos were downloaded and their frame 0 matched their profile-grid tile exactly. No queue
script had ever sent a cover field, so every TikTok post fell back to frame 0 — Dan mid-word
under a burned caption. That is what Dan flagged as "just showing a screenshot".

**So the cover has to BE frame 0.** `scripts/blotato/tiktok_cover.py` prepends the post's
designed cover PNG as a single frame (1/24 s — imperceptible in playback, so the viewer's
experience is unchanged) and pins `videoCoverTimestamp: 0`. The prepend is lossless: video
stream-copied through the concat demuxer, original audio mapped with `-itsoffset` so the mix is
never re-encoded or re-muxed at a join — which keeps it inside [[editor-audio-untouched]].

**A posted video's cover can only be changed within 7 days, and only in the phone app**
(⋯ → Edit post → Edit cover → Upload). No API, and TikTok Studio on the web does not expose it —
its per-post pencil does not respond at all under browser automation. Past 7 days the only route
is delete + re-upload, which throws away the post's views and comments. **So cover a post before
it goes out, never after** — same shape as the Instagram cover trap in `/coverimage`.

**16:9 long-forms (2026-09-22):** the first build stretched the tall cover to 1920x1080 (two skewed
tiles). `cover_filter()` now centres it in the grid's 3:4 window with blurred sides; long-forms need a
9:16 cover, not the wide YouTube thumbnail.

Full reasoning and the queue/upload mechanics: `Docs/TIKTOK_COVERS.md`. Blotato's schedule list
lags its own writes, which matters when rebuilding posts — see
[[blotato-false-failure-large-video]].
