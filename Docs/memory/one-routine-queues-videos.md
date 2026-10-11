---
name: one-routine-queues-videos
description: Dan 2026-10-11: never make a scheduled task to queue one video in Blotato; add it to video_waitlist.json and the daily social-queue routine queues it
metadata:
  type: feedback
---

Never create a scheduled task or routine that waits for Blotato room and queues a single video. When the queue is full, add the finished video to `scripts/blotato/video_waitlist.json`; the daily `social-queue-daily-refresh` routine runs `scripts/blotato/video_topup.py` and queues waiting videos (long-forms on Sundays, Shorts on Tue/Thu/Sat, videos before photo posts).

**Why:** Dan, 2026-10-11, after I made a per-video task for RO-07 and two others already existed: "I think some of these scheduled tasks are going to conflict with each other." He wanted one routine doing it for all videos, and had assumed the Social Queue routine already did (it only topped up photo posts until that day).

**How to apply:** in any `/video-setup` or Shorts setup that hits the 200-post cap, finish everything else, add the waitlist entry, say it will queue automatically, and stop. Long-forms need `instagram_video_url` (Instagram rejects files over about 300 MB). Related: [[blotato-false-failure-large-video]].
