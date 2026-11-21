---
name: private-video-comes-off-the-site
description: "11-18 standing rule: when a video is made private/unlisted/deleted on YouTube, set its sixpackabs.com page to draft the same day and verify"
metadata:
  node_type: memory
  type: feedback
  originSessionId: b0b6350c-0424-4ebf-9cc8-8d43e799858a
  modified: 2026-11-18T23:06:08.344Z
---

Dan, 2026-11-18: the Zepbound RO-28 video (yt eLV6EluvyD0) was showing as the "latest video" on sixpackabs.com while private, so visitors saw a broken player. Rule: anytime a video is made private (or unlisted/deleted), take it off sixpackabs.com in the same step.

**Why:** a private video's player only works for Dan; every other visitor sees a dead embed on the home page and /videos/.

**How to apply:** set the `spa_video` post (WordPress.com MCP `wpcom-content-items-update`, post_type spa_video, status draft, never delete) and any article post to draft, then curl the home page and the page URL (expect no title and 404). Check real YouTube privacy first with the oEmbed URL (200 public or unlisted, 401 private). The hourly sync drafts pages whose video leaves the public feed, but do it by hand now; a hand-drafted page stays draft until the video is public again. 2026-11-18 case: post 1238 drafted by hand, yet YouTube still reported the video reachable (oEmbed 200) and in the public feed, so confirm privacy actually saved. Related: [[ads-no-drug-terms-in-metadata]].
