---
name: meta-ads-instagram-identity
description: "Ads Manager cannot set the Instagram identity for @danrosefit ads (defaults to @abs.by.ai); the working API creative shape, and that the Meta app is Live since 2026-09-02"
metadata: 
  node_type: memory
  type: project
  originSessionId: 93cc83d3-95ce-4cec-a9f3-12ee60afb66e
  modified: 2026-09-02T22:55:35.876Z
---

**Ads on the ad account `act_2143998876461525` silently run as @abs.by.ai**, even when the Page is
Daniel Rose Fitness and every asset link points to @danrosefit. For the Traffic / Instagram-profile
objective the ad set's Identity card is a read-only Page field and the ad editor has no Identity
section, so picking a @danrosefit post always fails with #2238052. Two sessions were burned on this
before 2026-09-02.

**The only way to run an ad as @danrosefit on an existing post is the API**, with the top-level
creative shape (no `object_story_spec`, no `call_to_action`):
`POST /act_…/adcreatives object_id=<page> instagram_user_id=17841401601139982 source_instagram_media_id=<ig media id>`.
Script: `scripts/ads/boost_danrosefit_posts.py` in the repo. Adding a CTA brings back "link field is
required".

**Meta app `1598463548528030` has been LIVE since 2026-09-02.** Development mode blocked every API
ad creative (subcode 1885183). Claude is platform-blocked from filling the app-settings form (Dan
fills Basic: privacy/terms/domain/category) but can click Publish.

**Why:** the ad account was built around @abs.by.ai, then the audience consolidated on @danrosefit
(see [[instagram-account-state]]); Ads Manager never caught up.

**How to apply:** never try the Ads Manager UI or in-app Boost for @danrosefit ads; use the script.
The same shape works for engagement-objective ad sets, which is the basis for the planned auto-boost
job (new reel → $10/day ad on the real post → digest kill/scale rules). Dan prefers the automated
road; he called the manual setup "a mistake" and only wants it if it becomes hands-off.
