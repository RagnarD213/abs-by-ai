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
| A · image-led (control) | `control` | "See Yourself With Abs, Then Get A Personalized Plan To Make It Real." (Dan's headline, 09-09) + video (else the male proof pair) | in the hero |
| B · numbers-led | `analysis` | "Find Out How Far You Are From Abs — From One Photo." + a sample analysis card (body fat, lean muscle, fat to lose, goal weight, focus chips) | a section under the proof pairs |

Everything else is identical: the one-tap upload CTA, three proof pairs, what-you-get tiles, how it works, founder card, the trial card (`/?join=1`), FAQ,
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
JPEG 0.85 — the app's own settings), parks `{ dataUrl, variant, at }` in
`sessionStorage.absbyai_vsl_handoff`, and navigates to `/?from=vsl&v=<variant>` forwarding `utm_*`,
`gclid`, `gbraid`, `wbraid`, `fbclid`, `ttclid`, `msclkid` so the app's own click-id capture sees them.
`index.html`'s `applyVslHandoff()` (end of boot for logged-out visitors; inside `restoreSession()` for members, who
then skip the hub) loads the photo into the form, runs the clothing/sex check, and scrolls the visitor to the
"Where you are now" question — body type and intensity are answered in the app, not on the landing page
(Dan removed the chips 2026-09-09). If a payload ever carries a `condition`, `generate()` runs as soon as the
check clears. A blocked photo shows the normal warning. Payloads older than 15 minutes are ignored.

Events on `/start`: `vsl_landing_seen` {variant, forced, video_live},
`vsl_cta_clicked` {cta: hero | sticky | trial_card}, `vsl_photo_chosen`, `vsl_handoff` {stored},
`vsl_trial_cta_clicked`, `vsl_video_play`, `vsl_video_progress`. In the app: `vsl_handoff_received`,
then `generation_started` {source: 'vsl' | 'home'} and the existing funnel.

## The video slot — ONE config for both pages

`public/site-video.js` → `window.ABS_SITE_VIDEO = { youtubeId, mp4, poster }`. Read by `/start` and by
the post-lock-in analysis page (`ANALYSIS_VIDEO` in `index.html`). Poster: `public/img/video-poster.jpg`
(a caption-free frame at 0.05 s of the rev-5 master, 1280×720).

**Hosted 2026-09-09.** Unlisted YouTube video **`CwEGFxpIM-E`** on the Abs by AI channel
(https://www.youtube.com/watch?v=CwEGFxpIM-E): the finalized **rev 6 version A** master (3:50, ~424 MB, captions
burned in) — `Website Videos/Website Conversion Video (post-generation)/website_video_16x9.mp4`, byte-identical to the
copy in `claude edited long form content/06 - …/`. Uploaded with `scripts/youtube/upload.js` (memory
`youtube-upload-capability`). To swap it later: upload the new master with that script and paste the new id into
`youtubeId` — one line, one deploy, which wipes in-memory locked holds, so bundle it with other code.

## The /start VSL script (written 2026-09-10, not yet recorded)

A dedicated pre-upload video for this page — its one job is getting the photo uploaded. Script, hook takes, shot list,
B-roll and the research behind it: Google Doc `1DL2V34wePN75m1XxAuhpC2nghvobgr4C9RnTyszqqlA`
("Abs By AI — /start VSL scripts (hero + full) — WITH FILMING NOTES").

- **Hero cut** (~260 words, ≈1:15, demo-first: Dan uploads his own before photo on camera — "I'll go first") is meant
  for the hero slot on both variants; **full cut** (~660 words, ≈3:15, "This picture got me abs") is the test arm.
- Four hook takes end on the same line, so any hook splices onto the hero body; hook 3 ("How far are you from abs?")
  matches variant B's headline.
- **Install needs its own slot:** `site-video.js` is shared with the analysis page, which must keep `CwEGFxpIM-E`. The
  hero caption ("…3:50") and variant B's section copy also describe the old video. Steps:
  `Handoffs/handoff-20260910-start-vsl-edit-and-install.md`.
- Judge it on `vsl_photo_chosen ÷ vsl_landing_seen`, not plays. As of 2026-09-10 /start had ~4 visitors, so the 90 %
  home-page drop above is still the baseline.

## Compliance (memory: ad-suspension-prevention)

Dan removed the boxed AI-disclosure paragraph from the hero on 2026-09-09. What still carries the disclosure
above the fold: the "AI-GENERATED" tag printed on every after-image, the label under it, and the "Fictional
example … not a real result" line directly under the hero pair (kept at Dan's request). Lower down: the
visual-estimate qualifier + `/sources` on every number, the FAQ, and the legal footer. The headline's "make it
real" is the same phrasing the home page has carried since the August reinstatement; if Google ever flags
the page, that phrase and the missing hero paragraph are the first two things to put back.

## The Search landing-page test (home vs `/start`) is OVER — every Search ad now points at `/start` (2026-09-11)

On the Google Ads rep's advice, and with Dan's agreement in the meeting, the 09-09 Search A/B ended without
being read. Each of the five Search ad groups had two byte-identical RSAs, one on the homepage and one on
`/start`, rotating indefinitely.

What was done (`Handoffs/handoff-20260911-google-ads-rep-ga4-start-urls-mcc.md`, task 2):

- The five **home** RSAs — `821203927140`, `821417868428`, `821344283230`, `821344275016` (Non-Brand; all four
  were on **`http://`**) and `818993763993` (Brand) — had `final_urls` updated to `https://absbyai.com/start`
  and were then **PAUSED**, so their history stays readable. The five `/start` copies carry the ad groups.
- Read back: **5 ENABLED Search ads, every one `["https://absbyai.com/start"]`**; 5 PAUSED.
- The homepage did not disappear from Search — it became a **sitelink**. Both Search campaigns now carry four:
  **Abs By AI Home** `419963241925` → `https://absbyai.com` (new), **How It Works** `419855564105` →
  `/how-it-works.html` (new), **FAQ** `401566853985`, **Contact Us** `419837287031`. Four is what Google wants
  before it serves the rich format, and every sitelink URL differs from the ads' final URL and from each other.
  `Terms & Conditions` `401566879386` stays unlinked, as it was removed on purpose.
- No tracking template / UTMs were added: `/start` reads `gclid` for the Ads conversion and PostHog attributes
  from referrer + gclid.

⚠ Changing a final URL re-triggers policy review. Run `node scripts/ads/api/client.js policy 24148587722` and
`… 24086091285` the next day.
