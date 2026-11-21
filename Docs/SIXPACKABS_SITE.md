# sixpackabs.com — how the site works now

Live since **2026-09-11**: the homepage is Dan's **Abs by AI** YouTube channel, every public video has its
own page, and the 165 legacy articles and 46 pages are untouched at their original URLs.

Design spec: `Docs/sixpackabs-redesign/DESIGN_HANDOFF.md` (#2a mobile, #2b desktop).
Theme + tooling: `sixpackabs/` (README there covers deploy, rollback and the traps).

## The two halves

```
absbyai.com (Railway — holds the tokens)              sixpackabs.com (WordPress.com Atomic)
GET /api/sixpackabs/channel.json   ─── hourly ──►     theme sixpackabs-child (child of Twenty Twenty-Five)
    PUBLIC videos only                                   WP-Cron `spa_sync` → `spa_video` posts + media
GET /api/sixpackabs/instagram.json ─── hourly ──►        6 latest @danrosefit photos → media library
```

WordPress never talks to Google or Meta. The feed filters to `privacyStatus === 'public'`; the uploads
playlist also contains unlisted ads and private drafts. `scripts/sixpackabs/feed.test.js` asserts it,
including the real unlisted ids.

| thing | where |
|---|---|
| theme source | `sixpackabs/theme/sixpackabs-child/` |
| feed endpoints + tests | `scripts/sixpackabs/feed.js`, `feed.test.js`; wired near the end of `server.js` |
| tokens | Railway `abs-by-ai`: `GOOGLE_CLIENT_ID/SECRET`, `YOUTUBE_REFRESH_TOKEN`, `META_ADS_TOKEN` |
| URL baseline | `sixpackabs/url-baseline-20260910.txt` (219 URLs) + `sixpackabs/url-check.sh` |
| staging | https://staging-cac5-danroseconsulting-fedqa.wpcomstaging.com (robots-blocked) |

## Deploying a theme change

SSH was never needed. `SPA_SSH_*` is still unset and SFTP/SSH is disabled on both sites; `deploy.sh`
stays in the repo for the day credentials exist.

1. `cd sixpackabs/theme && zip -r /tmp/sixpackabs-child.zip sixpackabs-child -x '*.DS_Store'`
2. wp-admin → Appearance → Themes → Add Theme → Upload Theme, choose the ZIP.
3. **Submit the form from the page** (`fetch(form.action, {method:'POST', body:new FormData(form)})`) — a
   normal click on "Install Now" is redirected to the WordPress.com dashboard and installs nothing. On an
   update WordPress answers "already exists": follow its `overwrite=update-theme` link.
4. **Settings → Caching → Clear all.** WordPress.com serves cached pages to normal visitors; without this
   the site looks unchanged to everyone except requests carrying a query string.
5. Re-run `sixpackabs/url-check.sh https://sixpackabs.com` — 219/219 must be 200 with no redirect.

Theme activation can also be done through the WordPress.com connector (`theme.set`), which is how
production was switched when the Chrome extension dropped mid-deploy.

## Rollback

Re-activate **Twenty Twenty-Five**. The July customisations (header with PostHog, footer form, the old
front page, the article template with its CTAs) are database overrides stored against that theme: they are
ignored while the child theme is active and come back untouched. Do not delete them.

## What the sync does

- New public video → published page, dated like YouTube, notes = the description, featured image = Dan's
  cover art downloaded into the media library.
- Short = 3:00 or less; override per video in the "YouTube sync" box on the edit screen.
- Dan edits the notes → the sync never touches that text again (it compares a hash of what it imported).
  Title, date, thumbnail and length keep following YouTube.
- Video goes private/unlisted/deleted → its page goes to draft, never deleted, and returns if it comes back.
  A video Dan drafted or trashed himself stays that way.
- Instagram images are downloaded once (the Graph CDN links expire) — nothing is hotlinked.
- Shorts cards use Dan's 16:9 cover art cropped server-side to 405x720 (`spa-short`). YouTube's vertical
  thumbnail is a frame grabbed from the video — mid-sentence, burned captions — so it is not used.

## Traps

- **Activating a child theme abandons the parent's database template overrides** — that is why
  `templates/single.html` ports the article template (CTA card, end-post form, comments) into files.
- **The WordPress.com MCP cannot deploy code**; its template writes are disabled on this account.
- **Never hotlink Instagram `media_url`** — the links expire.
- **YouTube's uploads playlist drifts**: on 2026-09-11 a 55-item listing returned one video twice and
  skipped a public one. The feed lists it at two page sizes, unions the ids and re-checks everything that
  was public last time (`7dee0bb`).
- Nav and footer links live in `inc/blocks.php` / `inc/render.php` (`spa_url()`), not in a wp-admin menu.
