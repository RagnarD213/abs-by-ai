# Handoff: code and ship Dan's approved sales page (replaces /start for paid traffic)

Written 2026-09-30 by Claude (Opus 5.5). Not executed. Dan approved the mockup on 2026-09-30 ("this is looking excellent...
I am very optimistic about this page"). This task turns it into the real, working page on absbyai.com.

## 1. Goal

A live, fast, fully working page at `https://absbyai.com/start` that matches the approved mockup exactly: Dan's letter word
for word, the WV-01 video playing muted with a tap-for-sound box, every button taking the visitor into the existing web
checkout with the right plan and all ad click IDs, and the same tracking as today. Then tell the ad campaign task it is live.

## 2. The spec (source of truth)

| item | where |
|---|---|
| Approved mockup (private canvas) | https://claude.ai/artifact/GM8Han9hMfSHNf625vqtyu, page **Round 2** |
| Phone boards, top to bottom | `project/R2-Letter.dc.html`, `R2-Letter-2`, `R2-Letter-3`, `R2-Letter-4` (390 wide) |
| Desktop boards, top to bottom | `project/R2-Desktop-1.dc.html` to `R2-Desktop-4` (1280 wide, one 720 px column) |
| Generator that built them (exact markup per section) | `.claude/skills/design-sales-page/reference/round2-letter/gen.py` |
| Design rules and why | `.claude/skills/design-sales-page/SKILL.md` ("The locked layout", "Design system", "Dan's content rules") |
| Dan's letter (copy source) | Google Doc `1zCLn6pIuxGv4H1hkyieCk2T4NoYAQBnaNKMEFMcYV9o` |
| Final images (asset session) | Drive folder `1FullVwvuRxdbbaKhpy1_KLdAGLlG3XnC` (anyone with the link) |
| Today's /start (to replace) | `public/start.html` (served by the slug loop near `server.js:11037`), `Docs/VSL_LANDING.md` |
| Web checkout | `Docs/WEB_CART.md`; `applyPurchaseDeepLink()` and `showCartScreen()` in `public/index.html` |

Read the boards with the Artifact tool (`action: "read"`, `paths` = the eight board files). They are plain HTML with inline
styles and a few classes in `<helmet><style>`: port that markup and CSS. The four boards per device are ONE continuous page
(split only because a canvas board caps at 8000 px). Canvas-only parts to drop: sticky notes, Tweaks, `{{holes}}` (use the
defaults: button green `#15803D`, sound box yellow `#FFD23F`), the fixed board heights, the `x-dc` wrapper and script.

Build one responsive page: the phone boards are the layout under ~900 px, the desktop boards above it (720 px column,
larger type, the two plan options side by side, bigger phone images). The generator's `D` flag shows every size that differs.

## 3. What the page must do

1. **Copy verbatim.** Re-export the doc first (`rclone backend copyid gdrive: <id> ./x/ --drive-export-formats zip`) and
   parse it (`.claude/skills/design-sales-page/scripts/parse_doc.py`); diff against
   `reference/round2-letter/blocks.json` (via `rebuild_blocks.py`) to catch any change Dan made after 2026-09-30. After the
   build, run the copy check from `scripts/verify_boards.py` against the live HTML (adapt it: it expects canvas boards).
   Zero em or en dashes.
2. **Top stripe pinned** (`position: sticky; top: env(safe-area-inset-top, 0px)`): white logo left, "7-Day Free Trial /
   $0 today" and "Start Free Trial" right. No bottom sticky bar. No eyebrow. Headline right under the stripe; on a phone
   the whole video sits above the fold.
3. **Video: WV-01 version A, self-hosted MP4, no YouTube.** The C2 design rule is that the player never sends people to
   YouTube, and the sound box needs muted autoplay you control. Use `<video muted autoplay playsinline preload="metadata"
   poster=...>`; the "Tap to turn on sound" box unmutes and restarts from 0:00, then hides; normal controls after that.
   Source (default, Dan approved it last): `/Volumes/Extreme/_edit_work/wv01-edit/speed-1p2/WV-01 Website VSL A 1.2x 1080p.mp4`
   (SHA-256 `54d55235…`); the 1.0x original is `…/round17/final/WV-01 FINAL Website VSL A 1080p.mp4`. Encode a web copy
   (H.264 High, `+faststart`, about 2.5 Mbps 1080p plus a 720p source for phones) into `public/video/`. `public/` already
   serves MP4s (exercise demos, ad assets). Poster: the canvas asset `818cf8f3f239f5e2a1a071908f085ba2` (Artifact `read`
   with that id as `path` saves it), or a frame from the video. Keep `site-video.js` untouched: the analysis page still
   uses `ABS_SITE_VIDEO`.
4. **Every buy button** (stripe, offer card, the letter's buttons, both plan cards, final) goes to
   `/?join=1&from=vsl&v=letter-v1&plan=<monthly|annual>` and forwards `utm_*`, `gclid`, `gbraid`, `wbraid`, `fbclid`,
   `ttclid`, `msclkid` (reuse `appUrl()` from today's `start.html`). Trial conversions fire in `index.html`
   (`handleCartComplete`), so this hand-off is what keeps Google Ads, Meta and TikTok attribution working.
5. **Plan choice reaches checkout.** Both plan pickers on the page share one state (Monthly pre-selected; Annual shows
   SAVE 71%) and set `plan=` on every button. Today `index.html` hard-codes `selectedPlan = 'monthly'` (around line 8046)
   and reads no `plan` parameter: add `?plan=annual` support so the cart opens with Annual selected. Prices already exist
   (`MEMBERSHIP_PLANS` in `server.js`: 1999 / 6999 cents; `POST /api/stripe/create-cart-checkout` takes `plan`).
6. **Tracking identical to today.** Copy the head block from `start.html` (lines ~18 to 92): Manrope, PostHog, ONE gtag
   loader (`AW-18361229851` + `G-1M1SY7GGKF`), Meta pixel, TikTok pixel. Keep the event names (`vsl_landing_seen`,
   `vsl_video_play`, `vsl_video_progress` at 25/50/75/100, `vsl_trial_cta_clicked` with `{position, plan}`) and add
   `vsl_plan_selected`, `vsl_sound_on`. `posthog.register({landing: 'vsl', landing_variant: 'letter-v1'})` so funnels
   separate the new page from the old variants. No A/B coin flip: tests on this page are videos, never layouts.
7. **Native apps.** The Android TWA claims every absbyai.com path, so an ad click on a phone with the app can open this page
   inside the app. Mirror `index.html`'s `IS_NATIVE_APP` check (Capacitor, or `sessionStorage.absbyai_twa` / the
   `android-app://com.absbyai.app` referrer) and hide the purchase UI the same way (`.app-hide-purchase` pattern, memory
   `native-app-iap-gating`). Flag the native retest in the report (memory `cross-platform-retest-rule`).
8. **Images** at natural shape (labels burned into the real and AI images must never be cropped), lazy-loaded below the
   fold, web-sized (about 1200 px wide JPEG/WebP; phone screenshots as delivered; the salmon GIF as delivered or as a looping
   muted MP4 if smaller). Slot to file: `reference/round2-letter/assets.json` (canvas ids) and the Drive folder names:
   01 avatar, 02a deck-chair shirtless / 02b standing / 02c ride (never the bathroom shot), 03 M-100s YouTube screenshot,
   04 Crazy 3 Min Ab Workout screenshot, 05 ChatGPT laptop, 07 five AI models, 08 goal lock screen, 11 home screen phone,
   13a (the red-circled version) + 13b, 14 salmon GIF, 15a + 15b, 16a Oura graphic + 16b briefing. Closing photo = Dan's
   @abs.by.ai Instagram avatar (canvas asset `0e6fd18b166ed2820cb46ffa43351cc0`, 1080 square).
9. **Keep `noindex`**, like today's /start. Old page moves to `/start-v1` (noindex) for rollback; add the slug to the
   `server.js` loop. Replacing /start in place means the Search RSAs and Demand Gen ads (all pointing at /start) get the new
   page with no final-URL change and no new policy review.

## 4. Open decisions (ask Dan ONCE, in one message, at the start; use the defaults for anything he doesn't answer)

1. **Photos in the public repo.** Serving images means committing web-size copies to `public/`, and the GitHub repo is
   public (memory `repo-is-public`): this includes the before pictures with his daughter. They will be public on the page
   anyway. Needs a yes before commit. (Alternative only if he says no: keep them out of git and host elsewhere.)
2. **Video speed:** 1.2x (default, his latest approval) or the 1.0x original.
3. **FAQ line** "(Change when the stores list the app.)": looks like a note to himself. Default: it stays verbatim unless
   he says to cut it.
4. **Two plan pickers in a row** (end of "Try Abs By AI Free For 7 Days" and S10 right after). Default: keep both, as
   approved on the canvas.
5. **Day-5 email.** Dan said he doesn't plan to send a day-5 reminder email, but `trialReminderSweep` (`server.js`, hourly)
   emails every trial 48 hours before the charge, and the cart timeline says "Day 5" (`index.html` ~3013). Default: leave
   both untouched in this task and ask; turning the email off is a separate one-line change if he wants it.

## 5. Steps

1. Read this doc, the skill, and the eight boards. Send Dan the one decisions message (section 4).
2. Re-export the doc and confirm the copy (section 3.1).
3. Build `public/start.html` (new) and move today's to `public/start-v1.html`; add the `?plan=` support to `index.html`.
4. Encode and add the video; add the images (after decision 1).
5. Test locally with the preview server (`.claude/launch.json`): phone and desktop widths; muted autoplay, sound box, pinned
   stripe, both pickers, every button's URL (plan + click IDs), the cart opening on the chosen plan, PostHog events in the
   network log, one gtag loader, no console errors.
6. Commit only this task's files (the shared checkout has other sessions' dirty files: work in a fresh worktree off
   `origin/main` if the checkout still cannot push), push to `main`, confirm the Railway deploy, verify on
   `https://absbyai.com/start` (200, video plays, a button reaches checkout with the right plan). Batch into one push: every
   deploy drops locked image holds (memory `deploy-drops-locked-holds`).
7. Report to Dan in plain words with the live link and the native retest list. Check off the dashboard row "Ship the VSL
   sales page live: C2 design + WV-01 video + sales letter, replacing /start for paid traffic" (`/dashboard-tasks`).
8. Unblock the ad task: `handoff-20260930-ad-performance-pick-5-for-vsl-campaign.md` waits for "the page-build session
   reports the URL returns 200 and plays WV-01"; put that on its board line. Delete this handoff's lines from
   `AI_COORDINATION.md` and `Handoffs/README.md`.

## 6. Out of scope

Changing ad campaigns or budgets (the pick-5 task does that), PostHog feature flags, the analysis page and `site-video.js`,
the day-5 email (unless Dan says so), any copy change Dan hasn't made in his doc.

## Starter prompt

> Read `Handoffs/handoff-20260930-sales-page-build.md` in full, then build and ship my approved sales page from the Round 2
> canvas at https://claude.ai/artifact/GM8Han9hMfSHNf625vqtyu as the new absbyai.com/start: my letter word for word, WV-01
> as a self-hosted video with the tap-for-sound box, every button into the web checkout with the chosen plan and all ad
> click IDs, same tracking as today. Ask me the section 4 decisions once at the start, then go.

Recommended model: **Claude Opus 5.5, high effort.** It touches checkout, attribution and the main paid-traffic page, and
must match an approved design exactly.
