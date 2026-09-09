# `/start` — the paid-traffic (VSL) landing page

Built 2026-09-09. Send ad clicks to **`https://absbyai.com/start`** (plus the usual UTMs / gclid); the
home page `/` stays the organic front door. File: `public/start.html`, served by the slug route in
`server.js`. It is `noindex` so it never competes with `/` in search.

## Why it exists — the funnel on 2026-09-09 (PostHog, last 30 days, absbyai.com only)

| step | event | people | of previous step |
|---|---|---|---|
| landing (`/`) | `$pageview` | 571 | — |
| completed a generation | `generation_verifier` | 55 | **9.6 %** |
| lock-in → analysis page | `analysis_page_seen` | 1 (test traffic; page shipped 09-08) | — |
| trial sign-up started | `trial_signup_started` | 6 | 10.9 % of generators |
| trial started (Stripe) | `membership_subscribed` | 4 | |
| paid conversion | `paid_conversion_reported` | 2 | |

**The biggest drop is the first one: 516 of 571 visitors (90 %) leave without ever uploading a photo.**
Everything below that is small numbers. So the page is built to get a photo uploaded in one tap, and the
A/B tests two ways of asking for it. (There was no "generation started" event before this build — only
the completion telemetry — so `generation_started` was added to the app; expect it to show in the funnel
from 09-09 on.)

Side note from the same pull: `storage_anomaly` fires for ~every first visit (`device_id_minted_fresh`,
598 of 612). It is a first-visit marker, not an anomaly; ignore it in dashboards or rename it later.

## The two variants

| variant | key value | hero | video's home |
|---|---|---|---|
| A · image-led (control) | `control` | "See yourself with abs. Then get the plan to get there." + video (else the male proof pair) | in the hero |
| B · numbers-led | `analysis` | "Find out how far you are from abs — from one photo." + a sample analysis card (body fat, lean muscle, fat to lose, goal weight, focus chips) | a section under the proof pairs |

Everything else is identical: AI disclosure above the fold, "Where you are now" chips, the one-tap upload
CTA, three proof pairs, what-you-get tiles, how it works, founder card, the trial card (`/?join=1`), FAQ,
the legal footer, and a sticky mobile CTA.

Force a variant for QA or a specific ad: `/start?v=a` / `/start?v=b` (also `control` / `analysis`).
`/start?vp=1` renders the video placeholder so the layout can be reviewed before the video is hosted.

## How the split works (and the PostHog flag)

Flag key: **`vsl-landing-variant`**, variants `control` and `analysis`.

1. `?v=` override → 2. the value PostHog's flag gave this browser last time (`localStorage.absbyai_vsl_variant`)
→ 3. a sticky 50/50 coin. The variant is decided before first paint (no flicker) and stored.
The page fires `$feature_flag_called` (`$feature_flag` = key, `$feature_flag_response` = variant) — the
exposure event a PostHog **experiment** on that flag reads — and `posthog.register({ landing: 'vsl',
landing_variant })`, so every later event from that browser, on `/start` AND in the app, carries the
variant. Break any funnel down by `landing_variant`.

**The flag does not exist in PostHog yet.** Both stored keys (`POSTHOG_API_KEY`, `POSTHOG_PERSONAL_KEY`)
lack the `feature_flag:read/write` scopes, so it could not be created from a session. Until it exists the
page's own coin does the split and the data is complete either way. To create it (1 minute, PostHog UI):
Feature flags → New → key `vsl-landing-variant` → "Multiple variants" → `control` 50 / `analysis` 50 →
Save. Then Experiments → New → pick that flag → goal metric: funnel `$pageview` (`/start`) →
`generation_started` (or `trial_signup_started`) → Launch. From then on the flag's value overrides the coin
on a browser's next visit; the winner is rolled out by setting the flag to 100 % of one variant.

## The one-tap hand-off into the app

The CTA opens the photo picker directly (one tap). On choose, the page downsizes the photo (max 1024 px,
JPEG 0.85 — the app's own settings), parks `{ dataUrl, condition, intensity, variant, at }` in
`sessionStorage.absbyai_vsl_handoff`, and navigates to `/?from=vsl&v=<variant>` forwarding `utm_*`,
`gclid`, `gbraid`, `wbraid`, `fbclid`, `ttclid`, `msclkid` so the app's own click-id capture sees them.
`index.html`'s `applyVslHandoff()` (end of boot for logged-out visitors; inside `restoreSession()` for members, who
then skip the hub) loads the photo into the form,
selects the body type, runs the clothing/sex check, and calls `generate()` when it clears — so the visitor
lands on a loading generation, never an empty form. A blocked photo shows the normal warning. Payloads
older than 15 minutes are ignored.

Events on `/start`: `vsl_landing_seen` {variant, forced, video_live}, `vsl_condition_chosen`,
`vsl_cta_clicked` {cta: hero | sticky | trial_card}, `vsl_photo_chosen`, `vsl_handoff` {stored},
`vsl_trial_cta_clicked`, `vsl_video_play`, `vsl_video_progress`. In the app: `vsl_handoff_received`,
then `generation_started` {source: 'vsl' | 'home'} and the existing funnel.

## The video slot — ONE config for both pages

`public/site-video.js` → `window.ABS_SITE_VIDEO = { youtubeId, mp4, poster }`. Read by `/start` and by
the post-lock-in analysis page (`ANALYSIS_VIDEO` in `index.html`). Poster: `public/img/video-poster.jpg`
(a caption-free frame at 0.05 s of the rev-5 master, 1280×720).

**Not hosted yet.** The master is `claude edited long form content/06 - Website Conversion Video
(post-generation)/website_video_16x9.mp4` (rev 5, 3:50, 315 MB) — too big for the repo and for the
Chrome extension's 10 MB upload cap, and the stored Google token is calendar-scoped. **Dan's one step:
upload it to YouTube as Unlisted, then paste the 11-character id into `youtubeId` in
`public/site-video.js`** (or hand the id to a session). Until then both pages simply hide the slot
(variant A shows the proof pair in its place); nothing broken is visible to a visitor. Pushing that
one-line change redeploys and wipes in-memory locked holds — bundle it with other code when possible.

## Compliance (memory: ad-suspension-prevention)

The AI disclosure is in the hero above the fold, every proof image is labelled "AI-generated" on the
image and below it, the "Fictional examples" line follows every pair, the numbers carry the
visual-estimate qualifier + `/sources`, and the copy sells the visualization and the plan — never a body
result. Keep it that way when editing headlines.
