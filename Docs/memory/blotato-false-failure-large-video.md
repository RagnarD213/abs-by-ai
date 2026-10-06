---
name: blotato-false-failure-large-video
description: "Blotato marks large video posts \"failed\" on its own client timeout even when Facebook published them — always verify against the Graph API before re-posting"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 2ec3e50b-2965-49f4-a277-eed8a985c1c1
  modified: 2026-09-08T20:28:03.822Z
---

Blotato's `failed` state on a large video is **not proof the post did not publish**. Verified
2026-09-08: post `697055` (V7 long-form, 791.59s, 323 MB) was listed as failed 2026-09-06 with
"Uploading a reel to Facebook timed out", but the Graph API showed it live at 14:03:53 that same
day as `facebook.com/reel/1595086478922888` — `bytes_transferred` 323,270,763, `publish_status`
published. Blotato's client gave up while Facebook was still finishing the async upload.

**Before re-posting any Blotato "failure" that involves a video over ~100 MB, check the platform
directly.** For a Facebook page:

    curl -s "https://graph.facebook.com/v21.0/<PAGE_ID>/video_reels?fields=id,length,created_time,permalink_url,status,published&limit=6&access_token=$FACEBOOK_PAGE_ACCESS_TOKEN"

Match on `length` (video duration in seconds) — it identifies the exact file. Page id for
Abs by AI is `1294282227094660`; the token is `FACEBOOK_PAGE_ACCESS_TOKEN` in
`~/.absbyai-secrets.env`.

Two traps found the same day:
- **A duplicate Facebook reel can only be deleted, never unpublished.** Both
  `POST /<reel_id>` with `published=false` (returns `{"success":true}` and changes nothing) and
  `POST /<page_post_id>` with `is_published=false` (error #100, "not supported") fail. `DELETE
  /<reel_id>` works. Deleting is irreversible, so it is Dan's call — see [[bias-toward-action]].
- **Blotato's plan caps uploads at 400 MB.** The long-form masters are ~1.1 GB at ~11 Mbps and the
  queue's transcodes land ~322 MB, right against that ceiling — which is also why the push is slow
  enough to time out. Post `667411` (2026-08-18) is a genuine failure for exceeding it.

Facebook does accept full-length long-form as a "reel": both the 797s V6 and the 791.59s V7
published as reels with `video_status: ready`.

**The same lag hits a schedule read-back after a create (2026-09-17).** `tiktok_cover.py`
recreated 21 TikTok posts; reading `/schedules` three seconds after each `POST /posts` reported
"not found" for 6 of them. All 6 existed — the queue held exactly 21 TikTok posts, no duplicates
and no losses. Blotato's list simply lags its own writes. **Never replay a backup on a single
missing read-back**; poll the queue for ~20 s first, and confirm the post is genuinely absent
before re-creating. See [[tiktok-cover-frame-0]].

**Instagram reels: keep uploads under 300 MB (2026-09-29).** The arm-workout long-form (Blotato 739230, 313 MB,
660 s) failed on @danrosefit with "Instagram internal server error" while FB/TikTok/YouTube posted the same file.
Instagram's reel API caps files at 300 MB, the likely cause. Graph `/<ig_user>/media` confirmed it never went live
(token `META_ADS_TOKEN`; @danrosefit IG user `17841401601139982`). Fix: a two-pass x264 re-encode of the master at
~2.9 Mbps with `-c:a copy` (editor audio untouched), which came out at 266 MB. Re-queued as 4962222.
