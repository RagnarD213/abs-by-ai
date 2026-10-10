# `/start` — the paid-traffic (VSL) landing page

Built 2026-09-09. Send ad clicks to **`https://absbyai.com/start`** (plus the usual UTMs / gclid); the
home page `/` stays the organic front door. File: `public/start.html`, served by the slug route in
`server.js`. It is `noindex` so it never competes with `/` in search.

## Since 2026-09-30: Dan's sales letter (`letter-v1`)

`/start` is now Dan's approved sales page ("I Fired My Personal Trainer And Used AI To Get Abs Instead"), built from the
Round 2 canvas by `.claude/skills/design-sales-page/reference/round2-letter/build_live.py` (never hand-edit
`public/start.html`: change the generator and rebuild, then run `verify_live.py`). The page below this section is the
old two-variant page, kept at **`/start-v1`** (`public/start-v1.html`) for rollback.

- **Video:** WV-01 at 1.2x, self-hosted (`public/video/`): 720p for phones, 1080p for desktop. Since 2026-10-10 the page
  runs two films, Version A and Version B, one per browser (next section). A file over GitHub's 100 MB limit ships as
  `.part1`, `.part2`, ... and `server.js` joins the parts on boot (`/video/:name`).
  Plays muted under the yellow "Tap to turn on sound" box; a tap unmutes and restarts from 0:00. The muted preview pauses
  while scrolled away. A new cut = new file name (the route caches 7 days).
- **Buttons (8):** all go to `/?join=1&from=vsl&v=letter-v1` plus `utm_*`, `gclid`, `gbraid`, `wbraid`, `fbclid`, `ttclid`,
  `msclkid`, straight into the pay-first cart. No plan picker on the page (Dan cut both, 2026-09-30); Monthly is
  pre-selected in the cart, Lifetime one tap away.
- **Guarantee (2026-10-03):** the cart's 365-day money back guarantee, in four places: a one-line row in the offer card
  and under the last button, the full card with the gold seal in the "Try Abs By AI Free For 7 Days" section, and the
  question "What if I don't like it?". Wording is the cart's, unchanged; the seal is gold on this page (Dan's call).
  A full refund covers every payment made in the 365 days after the first one. `/refunds`, `/faq`, `/terms` and the
  member hub's refund answer say the same. Two plan lines say Lifetime instead of a yearly plan (`EDITS` in `gen.py`).
  Canvas page "Round 3: guarantee".
- **Events:** `vsl_landing_seen`, `vsl_video_play` (`autoplay: true, muted: true` when the muted preview starts),
  `vsl_sound_on` (the real "started watching"), `vsl_video_progress` 25/50/75/100 counted only after sound on,
  `vsl_trial_cta_clicked {position}`. Every event carries `landing: 'vsl', landing_variant: 'letter-v1'`. The layout has
  no coin flip: tests here are between videos, never layouts. The video test's own events are in the next section.
- **Same tags as before:** one gtag loader (Ads `AW-18361229851` + GA4), Meta pixel, TikTok pixel, PostHog.
- **Inside the Android/iOS app:** buy buttons, prices lines, the stripe button and every guarantee element are hidden; "Open Abs By AI" shows instead.

## The video test: Version A against Version B (RUNNING since 2026-10-10, 3:43 PM Central)

Dan's decision (2026-10-10): one page, one URL, the same ads and the same cart. Half of visitors get WV-01 Version A and
half get Version B ("Fired Them All": the finalized R5 film at 1.2x, the same speed as A, approved by Dan as R6). The film
is the only difference. No new software: the page's own code does the split and PostHog keeps score.

- **The two films.** `a`: `/video/wv01-a-720.mp4` (phones) and `/video/wv01-a-1080.mp4` (desktop), 10:27. `b`:
  `/video/wv01-b-720.mp4` and `/video/wv01-b-1080.mp4`, 11:57. B's web files come from the approved R6 file (SHA256
  `83519c7a...`, used as delivered) with A's exact settings, so the test is not also a picture-quality test: hardware
  H.264 High, about 1.0 and 2.0 Mbps, a keyframe every 2 seconds, Apple AAC at 96k and 128k, fast start, -14.4 LUFS.
  At that bitrate both of B's files pass GitHub's limit, so they ship in parts (720p in 2, 1080p in 3). Web masters,
  the encode recipe and hashes: `/Volumes/Extreme/_edit_work/wv01-edit/version-b/web/`.
- **Poster: the same for both.** The page's still (`video-poster-wv01.jpg`) is the approved design's picture, not a frame
  of film A, so B shows it too and the film stays the only difference. `VIDEOS` holds a poster per film if that changes.
- **The split** is in `build_live.py` (`B_SHARE`, `VIDEOS`) and runs in the page head before anything is drawn. Order:
  `?vid=a` or `?vid=b` (a forced QA view: never stored, marked `video_forced: true`), then the film stored for this
  browser in `localStorage.absbyai_vsl_video`, then a coin that is stored. A browser that blocks storage gets a fresh
  coin on each load and its events say `video_sticky: false`. The browser only ever asks for the one film it was given.
- **Rollback and rollout are one number.** Set `B_SHARE` to `0` (everyone gets A) or `1` (everyone gets B), then
  `python3 build_live.py <repo>`, `verify_live.py`, push. At 0 or 1 a stored film is ignored. Never hand-edit
  `public/start.html`.
- **Events.** Every `vsl_` event carries `video_variant` (`a` or `b`), `video_forced` and `video_sticky`;
  `landing_variant` is still `letter-v1`. The film is also registered on the browser, and every buy link carries
  `vid=<film>` (plus `vf=1` on a forced view), which `index.html` registers again, so `cart_viewed` and
  `cart_checkout_completed` carry it. New events, both counted only after sound on: `vsl_video_watch {sec}` at 30, 60,
  120, 240 and 480 seconds really watched (a skip ahead adds nothing), and `vsl_opening_done` when playback passes the
  end of that film's opening (A 2:22.1, B 3:32.4; from that frame on the two films show the same picture). The films
  differ in length, so compare seconds, never the percent marks. `$feature_flag_called` fires once per view with
  `$feature_flag: 'vsl-video-variant'`; no PostHog flag exists and none is needed.
- **Scoreboard.** PostHog dashboard **"/start video test: A vs B"**, pinned:
  https://us.posthog.com/project/458833/dashboard/2195388 (built 2026-10-10 through Dan's signed-in Chrome). A note at
  the top holds the read rules. Tiles: 1 people at each step, 2 sound-on rate (the early warning number), 3 got past
  the opening, 4 trial starts per visitor (the number that decides), 5 watch time with sound on, 6 page to cart to
  trial, 7 visitors per day, 8 visitors by film and device. Every tile is split by `video_variant`, starts 2026-10-10,
  and leaves out forced views and anything not on absbyai.com. Launch annotation: 2026-10-10 20:43 UTC (id 484663).
  The same numbers from a terminal: `python3 scripts/posthog/vsl_video_test.py` (`--trials` lists every trial start
  with its film, for matching against Stripe). The stored PostHog keys still cannot edit dashboards (query only): a
  change to a tile needs Dan signed in to PostHog in Chrome (memory `posthog-api-access`).
- **How the test is read (Dan's rules).** Minimum run 21 days (to 2026-10-31): no winner before that, even with a
  lead. Early warning at day 14 (2026-10-24) or 500 visitors per film, whichever is later: if B's sound-on rate
  trails A's by a third or more (8% against 12%, say), set `B_SHARE` to 0 and tell Dan; a lead for B changes nothing.
  The winner is called on trial starts per visitor and cost per trial, never a mid-funnel number: about 20 real trial
  starts in total with the leader holding about 15, counted from live Stripe without Dan and test accounts, each
  matched to its film in PostHog. At 70 visitors a day that is about two months.
- **Frozen while it runs:** /start, the cart, and the ads feeding it.
  `Handoffs/handoff-20261001-search-campaigns-to-vsl-page.md` changes the traffic mix, so it waits for the test to end.
- **Accepted, not engineered around:** a visitor who saw A before the launch may get B on the next visit, and a person
  on two devices can see both. The scoreboard prints how many people saw both films.
- **Checks.** `verify_live.py` now fails unless both films are complete, on disk in pieces under 95 MB, and named
  nowhere in the markup. `qa_video_test.py` (same folder) drives real Chrome through both films at phone and desktop
  sizes: `python3 qa_video_test.py http://localhost:3000 --hold` locally (nothing reaches PostHog or the ad pixels),
  or against `https://absbyai.com` (only the forced views reach PostHog, and those are never counted). Both passed
  on 2026-10-10: 123 checks locally, 123 live.
- **Native apps:** nothing changes inside the Android and iOS apps except which film plays.

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

## New membership VSL selection — 2026-09-16

Dan selected [Claude's “AI Got Me Abs at Forty”](https://claude.ai/artifact/BQ98aXCrbqX9bTfQFVzrSz)
over both Codex attempts for the new membership VSL. This assignment follows
[the new outline](https://docs.google.com/document/d/1y4ZrYoehmh54IQf0Hayv_krkG1K0NZjVVN8ZNrADX8w/edit),
primarily for a new page that requires signup before generation, also usable on
`/start`. Dan requested direct ring connection to be written as available for the
planned feature. Selection does not mean the video has been recorded or installed.

Writing lessons and paired examples:
`../.claude/skills/scriptwriting/references/vsl-2026-09-16-lessons.md`.
The earlier pre-upload script below is a separate deliverable.

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
