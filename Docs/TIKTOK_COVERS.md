# TikTok covers — why they break and the one fix that works

**Measured 2026-09-17 on @absbyai.** Dan: *"A lot of my TikTok videos are not showing the
proper thumbnail… A lot of them are just showing a screenshot."*

## The cause

TikTok's Content Posting API — everything Blotato can drive — has **no field for a cover
image**. Its only cover control is `video_cover_timestamp_ms`, a *timestamp into the video*.
Blotato exposes it on the TikTok target as `videoCoverTimestamp`.

Instagram's API *does* take a real image (`coverImageUrl`), which is why the same short shows
a designed cover on Reels and a mid-sentence screenshot on TikTok.

**With no timestamp sent, TikTok uses frame 0.** Proven: three published videos were
downloaded and their frame 0 matched the profile-grid tile exactly. No queue script had ever
sent a cover field, so every TikTok post fell back to frame 0 — and our shorts open on Dan
mid-word with a burned caption across the middle. The few tiles that *do* look designed
("The Truth About Supplements", "Home Ab Workout") are older videos that happen to open on a
title card.

## The fix

Since only a timestamp can be sent, **frame 0 has to BE the designed cover.**
`scripts/blotato/tiktok_cover.py` prepends the post's existing Instagram cover PNG as a single
frame (1/24 s) and pins `videoCoverTimestamp: 0`.

One frame is below the threshold of perception in playback, so **the viewer's experience is
unchanged — only the grid tile changes.** `--hold-frames N` makes the card a visible beat
instead, if that is ever wanted.

The prepend is **lossless**: video is stream-copied through the concat demuxer (`-c copy`) and
the original audio is mapped with `-itsoffset`, so the audio stream is bit-identical and never
re-encoded or re-muxed at a join — which keeps it inside AGENTS.md's "an editor's mix is
delivered untouched" rule. Every build is verified before upload: video frames must be
`src + 1`, audio packets must be unchanged, and a full decode must report zero errors.

    python3 scripts/blotato/tiktok_cover.py                        # audit the queue
    python3 scripts/blotato/tiktok_cover.py --build                # build + verify
    python3 scripts/blotato/tiktok_cover.py --apply --urls U.json  # rebuild the schedules

Covers are found on the Instagram twin by campaign key (`utm_content`) or media url — both are
needed, because Blotato re-hosts the same file under a new uuid per post so the twins usually
carry *different* media urls.

## Standing rule for every future TikTok post

**Any script that queues a TikTok post runs `tiktok_cover.py` afterwards.** The plan output is
the audit: a queued TikTok post with no `videoCoverTimestamp` is a defect, not a default.
`tiktok_mirror.py`, `abwheel_queue.py`, the `/video-setup` skill and any new queue script all
inherit this — they copy the media url straight off the Instagram post, which is exactly the
uncovered file.

## Already-published videos — mostly unfixable

TikTok allows a posted video's cover to be changed **only within 7 days of posting, and only
in the mobile app** (three dots → Edit post → Edit cover → Upload). There is no API for it,
and TikTok Studio on the web does not expose it (the per-post pencil does not open a cover
editor). Past 7 days the only route is delete + re-upload, which throws away the video's views,
likes and comments.

So the backlog splits:

* **within 7 days** — fixable by hand on the phone, one at a time
* **older** — permanently stuck with the frame-0 screenshot unless Dan is willing to lose the
  engagement on that post

This is why the fix matters going forward more than backward: every post that goes out
uncovered is permanently uncovered a week later.

## Uploading (the awkward bit)

Blotato has no REST route for a presigned upload — probed 2026-09-17:
`/media/presigned-upload-url`, `/media/upload-url`, `/media/presign`, `/media/signed-url`,
`/uploads/presigned-url` all 404, and `POST /v2/media {"url": …}` only re-hosts an
already-public url. Minting a presigned PUT is only exposed through the Blotato **MCP** tool
`blotato_create_presigned_upload_url`, so `--build` writes `cover_work/UPLOAD.md` listing the
files, and `--apply` takes the resulting `{schedule id: publicUrl}` map.

Blotato also cannot edit a scheduled post, so `--apply` is create-then-delete (same shape as
`swap_media.py`), with the old post's full body saved to `cover_backup/` before the delete.
