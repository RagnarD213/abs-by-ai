---
name: vsl-landing-page
description: "The /start paid-traffic page: Dan's sales letter (letter-v1) built by build_live.py; since 2026-10-10 a 50/50 video test, WV-01 A against B, split in the page head (B_SHARE), scored by scripts/posthog/vsl_video_test.py; older history of the page below"
metadata: 
  node_type: memory
  type: project
  originSessionId: 9bf6bf80-4aab-422e-aeae-97e07d7a09ac
  modified: 2026-09-10T14:58:06.015Z
---

`absbyai.com/start` is the ad landing page (`public/start.html`); `/` stays organic. Two variants in one file,
`control` (image-led, video in the hero) and `analysis` (numbers-led, video below the proof), forced with `?v=a|b`,
placeholder video with `?vp=1`. Operating doc: `Docs/VSL_LANDING.md`.

- **PostHog flag `vsl-landing-variant` is NOT created in PostHog** — both stored keys lack `feature_flag:*`
  scopes (verified 2026-09-09). The page runs its own sticky 50/50 and fires `$feature_flag_called` + registers
  `landing_variant` on every event, so analysis works without the flag; once Dan (or a scoped key) creates it,
  the flag overrides the coin from a browser's next visit.
- **The website video IS hosted** since 2026-09-09 (another session uploaded it unlisted via `scripts/youtube/upload.js`,
  id `CwEGFxpIM-E`, set in `public/site-video.js` — the one config for `/start` and the analysis page).
- Hand-off: `/start` parks the downsized photo in `sessionStorage.absbyai_vsl_handoff` → `/?from=vsl&v=…`
  → `applyVslHandoff()` in index.html loads it and scrolls to the body-type question (Dan removed the landing
  page's body-type chips 2026-09-09, so Generate is tapped in the app). `generation_started` now exists.
- Dan's round-1 review (2026-09-09): no eyebrow, no boxed AI-disclosure paragraph in the hero, Title Case all-black
  headline in his words. Round 2: headline sized with `clamp(…6.9vw…)` so it wraps to three lines on every phone,
  examples ordered male2 → female → male, founder card = hair-to-shorts crop of pool-shoot photo-180
  (`public/img/dan-founder.jpg`, abs visible — Dan's ask); the face circle `dan-avatar.jpg` stays on the video caption.

- **The dedicated /start VSL is SCRIPTED, not recorded (2026-09-10):** Google Doc
  `1DL2V34wePN75m1XxAuhpC2nghvobgr4C9RnTyszqqlA` — hero cut (demo-first, "I'll go first", ~1:15), full cut ("This
  picture got me abs", ~3:15), four hooks, shot list. When it's recorded, /start needs its OWN video slot — the shared
  `site-video.js` must keep feeding `CwEGFxpIM-E` to the analysis page. Edit + install:
  `Handoffs/handoff-20260910-start-vsl-edit-and-install.md`.

**Why:** the 2026-09-09 funnel pull showed 90 % of visitors (516 of 571) never upload a photo; the page and the
test target that drop. **How to apply:** point new ad campaigns at `/start`, read funnels by `landing_variant`,
and don't rebuild the flag logic — create the flag. Related: [[deploy-drops-locked-holds]],
[[ad-suspension-prevention]].

**2026-09-10 update:** `/start` has its own video config, `window.ABS_START_VIDEO` in `public/site-video.js` (falls back to
`ABS_SITE_VIDEO` when empty; the analysis page never reads it). Interim content = Muhammad's Ad 1 16:9 `lf46ytHacss`, Dan's
pick because no VSL footage existed. The dedicated VSL is still unrecorded; installing it later = edit that one object.

**2026-09-28 VSL page redesign, round 1:** five straight-VSL concepts (Classic Reveal, Video + Offer Hybrid, Founder Story,
Membership Tour, Straight Talk) built on a private Design canvas https://claude.ai/artifact/Fe4wvyvUWBFrQRzQyPJFXF, generator
+ assets in `Media/research/vsl-landing-mockups-20260928/` (`_build.py`). Choices a build session must keep: before/after is
shown one after the other, never side by side (Dan's ad rule, the page is a paid-traffic destination); the "before" is the
REAL 2022 deck-chair photo (`00_ORIGINAL_deckchair`), not the AI heavier reconstruction; `dan by pool.png` is AI and only ever
appears labeled AI-GENERATED as the goal picture. Awaiting Dan's pick; the build replaces /start for paid traffic.
**2026-09-28 decision (Dan):** C2 "Video + Offer Hybrid" is LOCKED as the one landing design. Not enough traffic to test designs,
so the A/B tests will be between VIDEOS on this page (WV-01 A vs B etc.), never between page designs. Color versions pending his pick.

**2026-09-30 final letter installed (mockup only):** Dan's final sales letter (Google Doc `1zCLn6pIuxGv4H1hkyieCk2T4NoYAQBnaNKMEFMcYV9o`)
is on page Round 2 of canvas https://claude.ai/artifact/GM8Han9hMfSHNf625vqtyu, verbatim: phone boards `R2-Letter`, `-2`, `-3`, `-4`
and desktop boards `R2-Desktop-1..4` (a canvas board caps at 8000 px, the page is ~24,000 px). Version B and the 7-day list are
gone (not in the letter). No buttons inside the story (every section ends on a cliffhanger into the next heading); buttons after
AI Hacks 2 and 4, the Try close, S10, S11 and the end. Generator + verbatim doc blocks: `Media/research/vsl-landing-mockups-20260928/round2-letter/`.
Open for Dan: sound box color, the two back-to-back plan pickers, the doc's bottom sticky bar vs the locked top-stripe-only.
**2026-09-30 Dan's round-2 revisions (applied):** white Abs By AI logo top-left in the black stripe; eyebrow "40-Year-Old Dad And
Business Owner" removed; headline right under the stripe (phone video now starts at 262 px); S10 plan card has NO "Today $0 / Day 5
reminder email / Day 7" timeline (Dan: "I don't plan on sending a day 5 reminder email"; keep it off the live page too; NOTE the
code still sends a trial-ending email 48 h before the charge via trialReminderSweep in server.js, so keeping or killing it is an open Dan decision); closing = last button, "I'll see you inside. Dan", then
his @abs.by.ai Instagram avatar (square Speedo shot cropped as shorts, smiling), then the footer. All doc images final. APPROVED
2026-09-30 ("looking excellent"); process locked in skill /design-sales-page; build = Handoffs/handoff-20260930-sales-page-build.md.

**2026-09-30 SHIPPED as /start (letter-v1):** built by `.claude/skills/design-sales-page/reference/round2-letter/build_live.py`
(never hand-edit `public/start.html`; rebuild + `verify_live.py`). Old two-variant page at `/start-v1` for rollback. Dan cut
both plan pickers (plan choice happens in the cart) and the FAQ note. WV-01 A 1.2x self-hosted in `public/video/` (1080p
ships as .part1/.part2, joined by `server.js` `/video/:name`: GitHub rejects files over 100 MB). Buttons go to
`/?join=1&from=vsl&v=letter-v1` plus click ids. Events and details: `Docs/VSL_LANDING.md`.

**2026-10-10 VIDEO TEST RUNNING (live 3:43 PM Central): WV-01 Version A against Version B ("Fired Them All", R6 = the finalized
R5 film at 1.2x).** Dan's plan: split on the page (no new software, no second URL, no ad changes), PostHog scores it, 50/50.
- The split is `B_SHARE` and `VIDEOS` in `build_live.py`, run in the page head: `?vid=a|b` forces a film (QA, never counted),
  else the film stored in `localStorage.absbyai_vsl_video`, else a stored coin. Rollback = `B_SHARE = 0`, rollout = `1`, rebuild,
  `verify_live.py`, push.
- B's web files (`/video/wv01-b-720.mp4` in 2 parts, `wv01-b-1080.mp4` in 3) match A's settings. A's audio encoder is Apple's
  (`-c:a aac_at`); ffmpeg's own AAC overshot the peak at 96k. Recipe: `/Volumes/Extreme/_edit_work/wv01-edit/version-b/web/encode.sh`.
- Both films use the page's approved poster: it is the design's still, not a frame of film A (the handoff assumed it was).
- Events: `video_variant`, `video_forced`, `video_sticky` on every `vsl_` event and on the cart events; new `vsl_video_watch {sec}`
  and `vsl_opening_done` (A 2:22.1, B 3:32.4). Compare seconds, not percent: the films differ in length.
- Scoreboard: `python3 scripts/posthog/vsl_video_test.py [--trials]`. QA: `qa_video_test.py` beside the generator (real Chrome;
  PostHog drops events from automated browsers unless `navigator.webdriver` is hidden).
- Read rules: no winner before day 21 (10-31); day 14 (10-24) or 500 visitors per film: B's sound-on rate a third or more behind
  A's means set `B_SHARE` to 0 and tell Dan; winner on about 20 real Stripe trial starts with the leader holding about 15.
  /start, the cart and the ads are frozen meanwhile; the search-campaigns handoff waits.
- NOT done: the PostHog dashboard and launch annotation. Both stored keys are query-only and no browser was signed in to PostHog.

**Why:** Dan wants to know which film sells more trials before putting more budget behind /start. **How to apply:** do not touch
/start, the cart or its ads while the test runs; read it with the script on the two dates; never call it early.
