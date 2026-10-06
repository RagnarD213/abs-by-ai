---
name: ads-never-organic
description: An ad video is never published organically (Blotato/FB/IG/TikTok/YouTube Public), however the request is phrased — enforced by scripts/blotato/ad_guard.py
metadata:
  type: feedback
---

**An ad video never goes out organically** — not Facebook, not Instagram (either account), not TikTok, not
Blotato, not YouTube Public. Ads live as an UNLISTED YouTube upload that Google Ads points at (`/ad-setup`)
and nowhere else. Organic distribution is for content videos (`/video-setup`).

**Why:** Ad 5 "Every Diet You've Tried Failed for the Same Reason" ran free on four organic accounts on
2026-09-16/17 and went Public on YouTube. Nothing malfunctioned — on 2026-09-10 Dan wrote *"This video is
finalized… upload it to YouTube and set it up on all other platforms in the Blotato queue"* (the sentence he
uses for content videos) and the session executed it literally. `/ad-setup` positively permitted organic
distribution at the time. The rule simply did not exist, so no agent was at fault and a prose-only fix would
have been written around the same way.

**How to apply:** "Set it up on all platforms" / "put it in the Blotato queue" attached to an AD is not
authorization — stop and say "this is an ad — ads don't go organic, do you want it posted anyway?" and wait.
Do the paid setup meanwhile; only the organic half blocks. Dan's per-video yes is the only override and is
recorded in `ORGANIC_OVERRIDES` in `scripts/blotato/ad_guard.py` with the date and his words. The guard blocks
three ways: missing `"content_type": "organic"`, a source path under `<Editor> Ad Videos/`, or a caption/slug
matching a known ad title or ad YouTube id. Audit any time with `python3 scripts/blotato/ad_guard.py --scan`.
Never hand-roll a Blotato queue script that skips the guard. Related: [[youtube-upload-capability]],
[[handoffs-not-auto-added-to-dashboard]].
