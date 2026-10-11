---
name: youtube-pinned-question-comment
description: Every public YouTube video gets one pinned question comment from the channel; written at setup, posted and pinned in Chrome after release by a daily routine
metadata:
  type: project
---

Dan, 2026-10-11 (from a YouTube analytics tip): every published video, long-form and Short, carries one pinned comment
from the channel that asks the viewer an easy question about that video. Goal: replies. All 41 public videos were done
that day. Ads (unlisted) get none.

**Why:** most videos had zero comments; a pinned question gives viewers something to answer.

**How to apply:** at setup, write the question into the Blotato config as `"pinned_comment"` (through `dan-voice-writer`,
under 180 characters, no link, no em dash). Nothing can be posted before release because Blotato creates the YouTube
video at release, and the API cannot pin. The Claude routine `youtube-pinned-comment-daily` (9:40 AM) runs
`node scripts/youtube/pinned_comment_gap.js`, posts and pins in Chrome, and records it in
`scripts/youtube/pinned_comments.json`. Procedure and traps: `Docs/PINNED_COMMENTS.md`. Related: [[youtube-upload-capability]].
My choice, not Dan's words: the pinned comment has no link (the older packaging rule put a `utm_medium=comment` link there).
