# Handoff: SixPackAbs.com homepage redesign (video-first, mobile-first)

**Date:** 2026-09-10
**Project:** sixpackabs.com (WordPress.com) + one small addition to the Abs By AI server
**Business goal this serves:** marketing → adoption. Goals in Dan's priority order: (1) views and subscribers on the
Abs by AI YouTube channel, (2) traffic to the AI app, (3) a credible personal-brand site to show people while networking.
**Written by:** Fable 5.1, after a planning interview with Dan on 2026-09-10. **NOT EXECUTED.**

## Objective

Rebuild the sixpackabs.com homepage to the locked design in `Docs/sixpackabs-redesign/` (mobile `#2a` at 430 px is the
primary design, desktop `#2b` at 1280 px), fed automatically by the Abs by AI YouTube channel and @danrosefit on
Instagram, with a page per video on the site, the new header and footer on every page, the newsletter form feeding the
existing list, and every one of the 165 existing blog posts and 46 pages untouched at its original URL. Build it on a
preview first; it goes onto the live homepage only when Dan says go.

Read `Docs/sixpackabs-redesign/DESIGN_HANDOFF.md` in full before writing any code — it is the pixel spec (tokens,
type scale, spacing, copy that is final and must be verbatim, interactions, focus states, empty states). This document
covers everything the design handoff does not: the stack, the data plumbing, Dan's decisions, and the traps.

## Current State (verified 2026-09-10)

**The site.** WordPress.com **Atomic** (Business tier; SSH/SFTP-capable), blog id `253647467`, theme **Twenty
Twenty-Five** (block theme, no child theme), 165 posts / 46 pages, ~540 views/month, timezone America/Chicago.
Permalinks are `/%postname%/`. `/blog/` returns 200 and is the archive of the AI-written articles. Yoast SEO runs the
sitemaps (`sitemap_index.xml` → post, page, category, author). Active plugins that matter: **WPCode Lite**, **Yoast
SEO**, **Site Kit by Google**, **Jetpack**, **Page Optimize**, **MailPoet + MailPoet Premium** (installed and active
but not what the site's forms use — see email below), WPForms Lite, Layout Grid, Gutenberg plugin.

**Everything built on the site so far was done through the WordPress.com MCP** (`wpcom-mcp-site-editing`
`templates.update` / `template-parts.update`) as **database overrides of the parent theme's templates**. These are
what exists today and what the new theme must carry forward or deliberately replace:

- `twentytwentyfive//header` part: full-width logo (`/wp-content/uploads/2026/04/sixpackabs-current-logo-symbol50-text130.webp`,
  1189×147), the **PostHog snippet** (project key `phc_s3ZXKWHRFQVqK6pYRBRBKtc2ex7LL78CFMHtCfENEQrU`, host
  `https://us.posthog.com`), and the navigation block (`ref: 4`, with a black pill `spa-nav-cta` item).
- `twentytwentyfive//footer` part: logo, tagline, links (About, Contact Us, FAQ, Partner With Us), and the
  **"Get the ab blueprint + your free AI after-photo" email form**.
- `twentytwentyfive//front-page`: the July "See yourself with abs — free" hero + the default post list. **Replaced
  entirely by this work.**
- `twentytwentyfive//single`: the article template with the inline Abs By AI CTA card after the byline, the dark
  "Stop imagining. See it." end-of-post block with the second email form, tags, prev/next, comments, "More posts".
  **Keep this behaviour** — the old articles keep their CTAs and forms.
- `twentytwentyfive//page-no-title`: used by the Abs Calculator page. Keep.
- `newsletter` / `email-general` templates belong to MailPoet; leave them.

**Email.** Both existing forms `fetch('https://absbyai.com/api/subscribe', {email, source:'sixpackabs'})`; the server
(`server.js` ~line 4383) stores the subscriber with first-touch `source` and pushes to **MailerLite**
(`MAILERLITE_GROUP_ID` on Railway). CORS is open. Live-tested from `sixpackabs.com` in July. The newsletter block
in the new design uses exactly this.

**YouTube.** Channel **Abs by AI**, handle `@absbyai`, id `UC236gjadarHAhEhOMYNGJ9g`, uploads playlist
`UU236gjadarHAhEhOMYNGJ9g`. 3,030 subscribers, **18 public videos** out of **53 uploads** — the other 35 are unlisted
ads / website videos and private drafts. Public inventory on 09-10: **6 long-form** (245–2305 s; a 7th, the $17 Ab
Wheel `bkzT-3ENpoU`, goes public Sun 09-13 9 AM CT) and **11 Shorts** (44–82 s). One playlist ("Ab Workouts", 1 item)
— not usable for the Shorts split. Working OAuth for the channel already exists **on Railway**: `GOOGLE_CLIENT_ID`,
`GOOGLE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN` (the token-refresh recipe is the top of `scripts/youtube/upload.js`).
No API key exists and none is needed.

**Instagram.** The audience account is **`@danrosefit`** (IG business id `17841401601139982`, 35 posts, 580
followers) — NOT `@absbyai` as the design handoff guesses. `META_ADS_TOKEN` (in `~/.absbyai-secrets.env`, system
user, never expires, has `instagram_basic`) reads its media today:
`GET graph.facebook.com/v21.0/17841401601139982/media?fields=id,media_type,media_url,permalink,thumbnail_url,timestamp`.
Recent feed is ~half `VIDEO` (reels) and half `IMAGE`. **`META_ADS_TOKEN` is not on Railway yet.**

**Design bundle** at `Docs/sixpackabs-redesign/`: `DESIGN_HANDOFF.md` (the spec), `Homepage Mockups.dc.html` +
`support.js` (open the HTML in a browser to see all five options; build only `#2a` and `#2b`), `public/img/`
(`sixpackabs-logo.webp`, `dan-founder.jpg` = the bio photo Dan confirmed, `sixpackabs-icon-192.png` favicon,
`logo.png` Abs by AI mark; `dan-avatar.jpg` and `video-poster.jpg` are not in the locked design).

**Analytics on the live homepage today:** PostHog and Site Kit's gtag only. The design handoff says a Meta pixel and a
TikTok pixel run on the site — **they do not appear in the served homepage HTML** (grep for `fbq(` / `ttq.` = 0). Carry
over what is actually there; do not add pixels that were never installed.

## Key Decisions Already Made (Dan, 2026-09-10 — do not re-open)

- **Code goes onto the site as a child theme over SFTP.** Dan chose this over WPCode snippets and over a no-code
  JS-rendered page. Dan enables SFTP/SSH in WordPress.com → Hosting → Server Settings and puts the credentials in
  `~/.absbyai-secrets.env` (see "What Dan does" below). Never paste PHP into WPCode for this.
- **Newsletter = capture only.** The form feeds the same `/api/subscribe` + MailerLite list as today's forms,
  `source: "sixpackabs"`. The "one email per new video" automation is a **separate follow-up handoff**, not this one.
  The block copy ("New video, new notes. One email each.") stays verbatim because the design says all copy is final.
- **Instagram = `@danrosefit`, images only, automatic.** The 6 most recent posts whose `media_type` is `IMAGE` or
  `CAROUSEL_ALBUM` (skip `VIDEO`). Grid heading link reads `@danrosefit →` and goes to `https://www.instagram.com/danrosefit/`.
- **The three unmocked page types get built in the same design system:** `/videos/` (long-form archive), `/shorts/`
  (Shorts archive) and `/videos/<slug>/` (one page per video: player, the notes, Subscribe CTA, more videos). Dan
  reviews them on the preview before anything ships.
- **App links go to `try.sixpackabs.com`** (the SixPackAbs-skinned Abs By AI app, live since August), not
  absbyai.com — this overrides the `absbyai.com/?utm_…` example in the design handoff. Keep the UTM pattern:
  `https://try.sixpackabs.com/?utm_source=sixpackabs&utm_medium=homepage&utm_campaign=<header|bio|footer|menu>`.
  PostHog's `brand` super-property already segments that traffic.
- **New header and footer on the whole site**, including all 165 old articles (which keep their in-post CTAs and forms).
- **Bio photo = `dan-founder.jpg`** as drawn.
- **Launch = preview first.** Build on a WordPress.com **staging site**, send Dan screenshots + the staging URL, and
  put it on production only when he approves. Old homepage restorable in one step.
- **All existing blog posts and pages stay on their original URLs — no redirects, no deletions, no slug changes**
  (Dan's explicit instruction, 09-10). The homepage links to the article archive (`/blog/`) — the footer's
  "Article archive" link in the locked design is that link; it is an acceptance check, not optional.
- Defaults Dan did not object to (from the design handoff): homepage counts stay **4 long-form on mobile / 5 on
  desktop + 6 Shorts**; **Short = public video ≤ 180 s** with a per-video override; **written notes = the YouTube
  description**, editable in WordPress, and the hourly sync stops overwriting a video's text once Dan edits it.

## Architecture (recommended; deviate only with a reason written in the commit)

```
absbyai.com (Railway, already has every token)        sixpackabs.com (WordPress.com Atomic)
┌──────────────────────────────────────────┐          ┌──────────────────────────────────────────────┐
│ GET /api/sixpackabs/channel.json          │  hourly  │ child theme  sixpackabs-child (of TT5)        │
│   YouTube Data API v3 via OAuth refresh   │ ◄────── │   WP-Cron spa_sync (wp_remote_get both JSONs) │
│   public videos only, cached 1 h          │          │   CPT spa_video + tax spa_video_type          │
│ GET /api/sixpackabs/instagram.json        │          │   sideloads thumbnails + IG images into media  │
│   6 latest IMAGE/CAROUSEL posts, cached   │          │   block templates + PHP-rendered dynamic blocks│
└──────────────────────────────────────────┘          │   theme.json (Manrope self-hosted, palette)    │
                                                      └──────────────────────────────────────────────┘
```

Why this split: the tokens stay on Railway where they already live; WordPress never talks to Google or Meta; the
site keeps rendering from its own database if absbyai.com is down; and the Node side gets a unit test like every
other server feature.

## Detailed Plan

### Phase 0 — access (Dan's part, ~5 minutes; everything else is Claude's)

1. Dan: WordPress.com → sixpackabs.com → **Hosting → Server Settings** → enable **SSH** (this also enables SFTP) →
   **Add SFTP user** → copy the generated password. Also create a **staging site** (Hosting → Staging site → Add) and
   enable SSH/SFTP on the staging site the same way.
2. Dan puts these in `~/.absbyai-secrets.env` (names, not values, are what the scripts expect):
   `SPA_SSH_HOST=sftp.wp.com`, `SPA_SSH_PORT=22`, `SPA_SSH_USER`, `SPA_SSH_PASS`, and the staging equivalents
   `SPA_STAGING_SSH_USER`, `SPA_STAGING_SSH_PASS`. If Dan added an SSH public key instead, `SPA_SSH_KEY` = path.
   Verify the host/port and the web root on first connect — expected web root is `/htdocs` with the theme dir at
   `/htdocs/wp-content/themes/`, and `wp` (WP-CLI) is available over SSH on Atomic.
3. Claude: add `META_ADS_TOKEN` to Railway (`railway variables --service abs-by-ai --set META_ADS_TOKEN=…` — reading
   the value from the secrets file, never into chat). Standing authorization covers Railway env vars. Every push
   redeploys and wipes in-memory locked generation holds (memory `deploy-drops-locked-holds`), so batch the
   server change into one push.

### Phase 1 — the feed endpoints on absbyai.com (`server.js`, plus tests)

4. `GET /api/sixpackabs/channel.json` — public, `Cache-Control: public, max-age=300`, served from an in-memory cache
   refreshed by a `setInterval` every 60 min (`.unref()`, same pattern as the other sweeps near the bottom of
   `server.js`) and on first request. Build: refresh the access token (recipe in `scripts/youtube/upload.js`),
   page `playlistItems` on the uploads playlist, then `videos?part=snippet,contentDetails,status` in batches of 50.
   **Keep only `status.privacyStatus === 'public'`** and `snippet.liveBroadcastContent !== 'upcoming'`. Emit per video:
   `{ id, title, description, publishedAt, durationSeconds, thumbnails:{maxres,high,portrait}, type }` where
   `type = durationSeconds <= 180 ? 'short' : 'long'` and `portrait = https://i.ytimg.com/vi/<id>/oardefault.jpg`
   (YouTube's vertical thumbnail for Shorts — it returned 200 for `GVNzvm5sUbk` on 09-10; verify per video with a
   HEAD and fall back to `maxresdefault.jpg`, which is 16:9 with the vertical frame centred, so `object-fit: cover`
   on a 9:16 box crops to exactly the video). Plus `{ channel: {id, handle, subscriberCount, videoCount}, fetchedAt }`.
   On upstream failure serve the last good cache and set `stale: true`; never 500 while a cache exists.
5. `GET /api/sixpackabs/instagram.json` — same caching; Graph call above with `limit=24`, filter to `IMAGE` /
   `CAROUSEL_ALBUM`, take 6, emit `{ id, permalink, imageUrl (media_url), timestamp }`. **`media_url` is a signed CDN
   URL that expires** — WordPress must download the image at sync time, never hotlink it.
6. Tests: `scripts/sixpackabs/feed.test.js` with fixture responses (a private video, an unlisted one, an upcoming
   premiere, a 180-s and a 181-s video, a reel in the IG list) asserting the filters and the type split. Run with
   `node scripts/sixpackabs/feed.test.js`. Verify live with `curl` after the deploy: no unlisted id
   (`lf46ytHacss`, `CwEGFxpIM-E`, `rimBWjT9-oo`) may ever appear in the JSON.

### Phase 2 — the child theme (`sixpackabs/theme/sixpackabs-child/` in this repo; deploy script beside it)

7. **Skeleton**: `style.css` (`Template: twentytwentyfive`), `theme.json` (palette from the design tokens; Manrope
   400/500/600/700/800 **self-hosted** in `assets/fonts/` via `fontFace` — Page Optimize will bundle the CSS; do not
   depend on fonts.googleapis.com), `functions.php`, `templates/`, `parts/`, `patterns/` if useful, `assets/`.
   Include `public/img/*` from the design bundle under `assets/img/`. Set the favicon to `sixpackabs-icon-192.png`.
8. **Content model** in `functions.php`: CPT `spa_video` (public, `has_archive: 'videos'`, `rewrite.slug: 'videos'`,
   `show_in_rest`, supports title/editor/excerpt/thumbnail, `menu_icon: dashicons-video-alt3`) and taxonomy
   `spa_video_type` (terms `long`, `short`; `rewrite.slug: 'type'`). Add `add_rewrite_rule('^shorts/?$',
   'index.php?spa_video_type=short', 'top')` (and paged variant) so `/shorts/` is the Shorts archive. Meta (all
   `show_in_rest`, registered): `_spa_youtube_id`, `_spa_duration`, `_spa_published_at`, `_spa_thumb_url`,
   `_spa_portrait_url`, `_spa_type_override` (`''|long|short`), `_spa_imported_hash`. Expose the override and the
   YouTube id in a small meta box so Dan can flip a video's type from wp-admin.
9. **Sync** (`inc/sync.php`): `spa_sync` WP-Cron event hourly + a `wp spa sync` WP-CLI command + `?spa_sync=1` for
   admins. For each video in the feed: upsert by `_spa_youtube_id`. **Create**: `post_status publish`,
   `post_date` = `publishedAt` in site time, title = video title, content = the description converted to blocks
   (paragraphs on blank lines, URLs linked with `rel="nofollow noopener"`, hashtags kept), excerpt = first 2–3 lines,
   slug from the title, term = type, featured image sideloaded from the maxres thumbnail (`media_sideload_image`),
   `_spa_imported_hash = md5(content)`. **Update**: title, duration, thumb URLs, published date, term (unless
   `_spa_type_override`); **content only if `md5(current content) === _spa_imported_hash`** — the moment Dan edits the
   notes in WordPress the hash no longer matches and the text is his. A video that disappears from the feed (went
   private/unlisted/deleted) → `post_status draft`, never deleted. Instagram: keep the 6 latest in a single option
   `spa_instagram` after sideloading each image once (keyed by IG media id; skip ones already in the media library).
   Log each run's counts to `error_log` and to an option `spa_sync_last` shown on the meta box screen.
10. **Rendering**: block templates in `templates/` + `parts/header.html` + `parts/footer.html`, with the data-driven
    sections as **server-rendered dynamic blocks** registered in PHP (`register_block_type` with `render_callback`,
    no build step; a `block.json` each so they also insert in the editor): `spa/featured-video`, `spa/video-list`
    (`count`, `type`), `spa/shorts-rail`, `spa/instagram-grid`, `spa/newsletter`, `spa/subscribe-button`. Templates:
    - `front-page.html` — the nine sections in the locked order. Every pixel value comes from `DESIGN_HANDOFF.md`.
      Long-form list renders 5 items; the 5th is hidden under 768 px. Featured = newest long-form.
    - `single-spa_video.html` — same header/footer; H1 title, eyebrow with the date and duration, a **facade embed**
      (thumbnail + red play button; the `youtube-nocookie.com` iframe is injected on click, never on load, never
      autoplay), then the notes (post content), a Subscribe CTA block, "More free videos" (4), the newsletter block.
      JSON-LD `VideoObject` (`name, description, thumbnailUrl, uploadDate, duration (ISO 8601), embedUrl,
      contentUrl = the YouTube watch URL`) + `og:video` via `wp_head`; let Yoast handle title/description/canonical.
    - `archive-spa_video.html` and `taxonomy-spa_video_type.html` — heading (`Free videos` / `Shorts`), grid of cards
      in the homepage card style (16:9 for long, 9:16 for shorts), paginated, empty state hides the grid.
    - `single.html` — port the existing article template **feature for feature** (inline CTA card, end-post dark
      block with its email form, tags, prev/next, comments, More posts), restyled with the tokens, under the new
      header/footer. `page.html`, `page-no-title.html`, `archive.html` (category archives), `index.html`, `search.html`,
      `404.html` — same header/footer, tokens applied lightly. `/blog/` must keep rendering the article list.
    - Header part: mobile = logo (`height: 22px`) + red **Subscribe** pill (`https://www.youtube.com/@absbyai?sub_confirmation=1`)
      + hamburger opening the full-screen overlay (Videos · Shorts · About Dan · Abs Calculator · Collab · Try the AI
      App · Subscribe; 200 ms ease-out, focus trapped, Escape and backdrop close). Desktop = logo 28 px, nav, outline
      **Try the AI App**, red **Subscribe**. Sticky on mobile. The PostHog snippet moves here (or to
      `wp_enqueue_scripts`), unchanged key/host. Nav targets: Videos `/videos/`, Shorts `/shorts/`, About Dan
      `/pages/about-us/`, Abs Calculator `/abs-calculator/`, Collab `/partner-with-us/`.
    - Footer part: exactly the links in the spec. Mobile: YouTube · Instagram · Try the AI App · Abs Calculator ·
      Contact / Collab (`/contact-us/`) · **Article archive (`/blog/`)**; `© 2026 SixPackAbs.com · Georgetown, TX`.
      Desktop: left YouTube · Instagram · Contact / Collab · Try the AI App; right Article archive · Abs Calculator ·
      Disclaimer (`https://absbyai.com/disclaimer`, as the old footer used).
11. **Newsletter block**: form posts to `https://absbyai.com/api/subscribe` with `{email, source:'sixpackabs'}`;
    inline validation on blur, disabled button in flight, inline success/error inside the dark block, no reload.
12. **Analytics**: PostHog `outbound_click` with `{target: 'youtube_subscribe'|'instagram'|'try_app'|'youtube_watch',
    placement: 'header'|'bio'|'footer'|'menu'|'card'}` on every Subscribe, Instagram cell, Try-the-AI-App and
    external YouTube link; `video_page_play` when the facade swaps in the iframe. Site Kit is plugin-injected and
    needs nothing.
13. **Performance and a11y**: no YouTube iframe on the homepage; `loading="lazy"` below the fold; explicit
    `aspect-ratio` on every media box; `srcset` from the sideloaded images; visible focus ring
    `outline: 2px solid #2f5fe0; outline-offset: 2px` everywhere; 44 px touch targets; the Shorts rail is native
    scroll with `scroll-snap-type: x mandatory` and hidden scrollbars — no drag JS. Never use `#a29e95` for text on a
    light background.
14. **Deploy tooling**: `sixpackabs/deploy.sh <staging|prod>` — `rsync -az --delete -e "ssh -p $PORT"` the theme dir
    to `/htdocs/wp-content/themes/sixpackabs-child/` (or `lftp` mirror over SFTP if SSH is off), then over SSH:
    `wp theme activate sixpackabs-child && wp rewrite flush && wp cron event run spa_sync`. Idempotent; prints the
    homepage HTTP status afterwards. `sixpackabs/README.md` explains the one-command deploy and the one-command
    rollback (`wp theme activate twentytwentyfive`).

### Phase 3 — staging build and Dan's review

15. Deploy to the **staging site** first. Run the sync, confirm 6/7 long-form + 11 Shorts imported, the unlisted ads
    absent, Instagram 6 images present and locally hosted. Screenshot at 430 px and 1280 px (light theme) and compare
    against `#2a` / `#2b` side by side; fix until they match. Test the mobile menu, the Shorts rail, a video page's
    facade embed, the newsletter form (a real submit with a test address — it lands in MailerLite tagged sixpackabs),
    an old article (CTA card, end-post form, comments still there), `/blog/`, one category archive, the Abs
    Calculator page, search, 404.
16. **URL preservation check (hard gate):** before touching production, fetch every `<loc>` from the production
    `post-sitemap.xml`, `page-sitemap.xml` and `category-sitemap.xml` (save the list to
    `sixpackabs/url-baseline-YYYYMMDD.txt`, commit it); on staging, request each one (host-swapped) and require 200
    with no redirect. After the production deploy, repeat against production. Any non-200 blocks the launch.
17. Send Dan: the staging URL, the two screenshots, the URL-check summary, and the list of anything you had to decide
    (Opus's own choices for the three unmocked page types). **Stop and wait for his go.**

### Phase 4 — production

18. On Dan's go: `deploy.sh prod`, run the sync, re-run step 16 against production, re-verify the homepage and one
    article live with `curl` and a real browser (see Traps for which browser). Purge Page Optimize / Jetpack caches if
    the old homepage still shows. Update Yoast's homepage title/description to the video-first positioning (keep the
    phrase "Six Pack Abs"; e.g. `SixPackAbs.com — Free Six Pack Abs Videos From Dan Rose` — Dan can edit in Yoast).
19. Retire the July database template overrides only after production is verified — they are harmless while the
    child theme is active (they belong to the parent theme's slug), and they are the rollback.
20. Close out: commit + push everything (theme, deploy script, server change, tests, URL baseline); remove this
    handoff from `AI_COORDINATION.md` (HANDOFFS) and `Handoffs/README.md` (Open table); write a short
    `Docs/SIXPACKABS_SITE.md` (stack, deploy, sync, rollback, where the tokens live); record the durable facts in
    memory. **No dashboard row exists for this and none should be added unless Dan asks.** Not a native-retest trigger
    (sixpackabs.com is not loaded by the iOS/Android apps) — but the `server.js` push is a Railway deploy, so say so
    in the report.

## Things to Avoid / Lessons Learned

- **The OAuth token sees everything.** Unlisted ads, the website video and private drafts are in the uploads playlist.
  Filter on `status.privacyStatus === 'public'` and test it. Publishing an unlisted ad on the homepage would be the
  worst outcome of this build.
- **Activating a child theme abandons the parent's database template overrides.** The July header/footer/front-page/
  single edits are stored against `twentytwentyfive`; they vanish the moment `sixpackabs-child` is active. Port
  `single` (CTAs + form) and `page-no-title` deliberately. Same reason they come back untouched on rollback.
- **The WordPress.com MCP cannot deploy code.** It edits templates, parts, posts and settings only — no PHP, no
  files, no WPCode. Its write operations also require `user_confirmed: true`. Use it for reading and for the
  Yoast/reading-settings checks; use SSH/SFTP for everything in the theme.
- **Browsing policy blocked `sixpackabs.com` in the in-app Browser pane** in an earlier session; `curl` and the Chrome
  extension worked. If the pane refuses, do not fight it.
- **Instagram `media_url` links expire.** Sideload; never hotlink. Graph API v21.0; `instagram_business_account`
  reads empty on the Pages list for all pages (false negative) — use the IG id above directly.
- **Do not create redirects, change slugs, or delete anything under `/blog/`, `/category/*`, or any existing page.**
  Content ID and SEO both depend on it; Dan said so explicitly.
- The `Homepage Mockups.dc.html` prototype is a streaming-component canvas — not markup to copy. Rebuild from the
  spec. Turn-1 options `#1a/#1b/#1c` are out of scope.
- `AI_COORDINATION.md` is auto-loaded into every session; write three or four sentences there, not a log.
- YouTube Data API quota: ~5 units per hourly refresh — nothing to manage. No AI spend in this build ($0).

## Relevant Files & Locations

- Design bundle: `Docs/sixpackabs-redesign/` (`DESIGN_HANDOFF.md`, `Homepage Mockups.dc.html`, `public/img/`).
- Server: `server.js` (`/api/subscribe` ~4383; sweep `setInterval` pattern ~10835+); token refresh recipe
  `scripts/youtube/upload.js`; new code goes in `scripts/sixpackabs/` and a `sixpackabs` section of `server.js`.
- Theme + deploy: `sixpackabs/theme/sixpackabs-child/`, `sixpackabs/deploy.sh`, `sixpackabs/README.md` (all new).
- Secrets (names only): local `~/.absbyai-secrets.env` — `META_ADS_TOKEN`, `GOOGLE_CLIENT_ID`,
  `GOOGLE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN`, new `SPA_SSH_*` / `SPA_STAGING_SSH_*`; Railway (`railway variables
  --service abs-by-ai --kv`) — `GOOGLE_CLIENT_*`, `YOUTUBE_REFRESH_TOKEN`, `MAILERLITE_GROUP_ID`, add `META_ADS_TOKEN`.
- WordPress.com: site id `253647467`; MCP tools `wpcom-mcp-site-editing` (templates), `wpcom-mcp-site`
  (settings/plugins), `wpcom-mcp-content-authoring` (posts/media).
- Channel: `https://www.youtube.com/@absbyai`, id `UC236gjadarHAhEhOMYNGJ9g`. Instagram: `https://www.instagram.com/danrosefit/`,
  IG id `17841401601139982`. App: `https://try.sixpackabs.com`. Disclaimer: `https://absbyai.com/disclaimer`.
- History of the July conversion layer and the August SixPackAbs skin: `AI_COORDINATION_ARCHIVE.md` (search "SixPackAbs").
- Memories: `repo-is-public` (the repo is public — no secrets, no personal photos beyond what is already in
  `public/img`), `deploy-drops-locked-holds`, `instagram-account-state`, `youtube-upload-capability`.

## Model & Effort Recommendation

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | **Claude Opus 5, high effort** — Dan's stated choice. Multi-file theme + PHP + Node + pixel-matching against a spec is exactly the "hard, expensive to unwind" bucket. |
| **If Claude usage is high / approaching a limit** | Codex flagship, high effort, for Phases 1–2 (well-specified code); switch to Claude (Sonnet 5 is enough) for the Phase 3 visual comparison and Dan's review loop. |

Always-Claude override: none of the always-Claude categories (copy, architecture decisions, Anthropic API code)
remain open — the copy is final and the architecture is decided above. Phase 3's visual judgement is where a Claude
model earns its cost.

## Starter Prompt for the Next Task

> Execute `Handoffs/handoff-20260910-sixpackabs-homepage-redesign.md` end to end. Read it and
> `Docs/sixpackabs-redesign/DESIGN_HANDOFF.md` fully first. I have enabled SSH/SFTP on sixpackabs.com and its staging
> site and put the `SPA_SSH_*` / `SPA_STAGING_SSH_*` credentials in `~/.absbyai-secrets.env` — verify the connection
> first. Then: add `META_ADS_TOKEN` to Railway and build + test + deploy the two feed endpoints on absbyai.com; build the
> `sixpackabs-child` theme with the video post type, hourly sync, and the locked #2a/#2b homepage; deploy it to the
> STAGING site only; run the URL-preservation check; send me the staging link, 430 px and 1280 px screenshots, and your
> decisions on the video/archive pages. Do NOT touch the production theme until I say go.
