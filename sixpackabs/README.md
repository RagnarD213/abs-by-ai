# sixpackabs.com — video-first theme

The sixpackabs.com homepage is Dan's **Abs by AI** YouTube channel: the newest long-form video
large, more videos beside it, a Shorts rail, the latest @danrosefit photos, the bio and the
newsletter. Every public video also gets its own page at `/videos/<slug>/` (player + the written
notes). The 165 legacy articles and 46 pages keep their exact URLs and their in-post CTAs and
forms; they just wear the new header and footer.

Design spec: `Docs/sixpackabs-redesign/DESIGN_HANDOFF.md` (#2a mobile, #2b desktop).

## How it fits together

```
absbyai.com (Railway — holds the tokens)                 sixpackabs.com (WordPress.com Atomic)
GET /api/sixpackabs/channel.json   ──── hourly ────►     theme sixpackabs-child (child of Twenty Twenty-Five)
    public videos only (scripts/sixpackabs/feed.js)         WP-Cron `spa_sync` → `spa_video` posts + media
GET /api/sixpackabs/instagram.json ──── hourly ────►        6 latest @danrosefit photos → media library
```

WordPress never talks to Google or Meta. The feed filters to `privacyStatus === 'public'` — the
uploads playlist also holds unlisted ads and private drafts (tested in `scripts/sixpackabs/feed.test.js`).

| thing | where |
|---|---|
| theme | `sixpackabs/theme/sixpackabs-child/` |
| feed endpoints + tests | `scripts/sixpackabs/feed.js`, `feed.test.js`; wired in `server.js` |
| tokens | Railway `abs-by-ai`: `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `YOUTUBE_REFRESH_TOKEN`, `META_ADS_TOKEN` |
| SSH credentials | `~/.absbyai-secrets.env`: `SPA_SSH_HOST`, `SPA_SSH_PORT`, `SPA_SSH_USER/PASS`, `SPA_STAGING_SSH_USER/PASS` |
| URL baseline | `url-baseline-20260910.txt` (every sitemap `<loc>` on 2026-09-10, 219 URLs) |

## Deploy, check, roll back

```bash
sixpackabs/deploy.sh check staging        # connect, print site + active theme, change nothing
sixpackabs/deploy.sh staging              # upload, activate, flush rewrites, run the sync
sixpackabs/url-check.sh https://<staging-host>   # every baseline URL must be 200, no redirect
sixpackabs/deploy.sh prod                 # production — only on Dan's go
sixpackabs/deploy.sh rollback prod        # one step back to Twenty Twenty-Five
```

Rollback works because the July customisations (header with PostHog, footer form, the old
front page, the article template with its CTAs) are database overrides stored against
`twentytwentyfive`: they are ignored while the child theme is active and come back untouched
when Twenty Twenty-Five is re-activated. Don't delete them until production has run on the
child theme for a while.

## Running the sync

- Hourly by WP-Cron (`spa_sync`, scheduled on activation).
- `wp spa sync` over SSH prints the report.
- wp-admin → **Videos** → "Sync now".

What the sync does to a video:
- **New public video** → a published page, dated like YouTube, notes = the description, featured
  image = the YouTube thumbnail (downloaded into the media library; the vertical one too for Shorts).
- **Short or long-form** → Short = 3:00 or less. Override per video in the "YouTube sync" box.
- **Dan edits the notes or the excerpt** → from then on the sync never touches that text (it
  compares a hash of what it imported). Title, date, thumbnail and length keep following YouTube.
- **Thumbnail changed on YouTube** → re-downloaded (the maxres ETag changed).
- **Video made private/unlisted/deleted** → the page goes to draft, never deleted; it comes back
  if the video is public again. A video Dan drafted or trashed himself stays that way.
- Instagram images are downloaded once (Graph CDN links expire) — nothing is hotlinked.

## Local preview (no SSH needed)

`preview_start` → `sixpackabs-playground` (in `.claude/launch.json`) boots WordPress Playground on
`http://127.0.0.1:9400` with this theme mounted, seeds stand-in pages and three real articles
(`playground/seed.php`) and runs the real sync against the live feeds.

## Traps

- **Activating a child theme abandons the parent's database template overrides.** Everything the
  July work stored against `twentytwentyfive` had to be ported into files here on purpose
  (`templates/single.html` = the article template with both CTAs and the form).
- **The WordPress.com MCP cannot deploy code** — templates/settings only, and its template writes
  are disabled in this account's MCP settings. Code goes over SSH (`deploy.sh`).
- **Never hotlink `media_url` from Instagram** — the links expire.
- Nav and footer links live in `inc/blocks.php` / `inc/render.php` (`spa_url()`), not in a
  wp-admin menu: the copy is final.
