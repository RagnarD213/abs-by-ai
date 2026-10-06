---
name: sixpackabs-site-stack
description: "sixpackabs.com facts — WP.com Atomic + TT5, MCP can't deploy code (SFTP/SSH needed), YouTube OAuth sees unlisted ads, IG audience is @danrosefit, forms feed MailerLite via absbyai.com"
metadata: 
  node_type: memory
  type: project
  originSessionId: 9fb6b474-be2a-49f8-910a-a28826d4ef12
  modified: 2026-09-11T17:21:48.048Z
---

**sixpackabs.com** = WordPress.com **Atomic** (Business tier), blog id `253647467`, Twenty Twenty-Five block theme,
Yoast sitemaps, WPCode Lite + MailPoet installed. ~540 views/month, 165 posts / 46 pages (as of 2026-09-10).

- **The WordPress.com MCP only edits templates/posts/settings — it cannot deploy code** (no PHP, no files, no
  WPCode). Real code = child theme over SSH/SFTP (Hosting → Server Settings; host `sftp.wp.com`, web root `/htdocs`,
  WP-CLI over SSH). Every pre-Sept change was a **database override of the parent theme's templates** — those
  vanish when a child theme is activated (and return on rollback).
- **Email forms** on the site POST to `absbyai.com/api/subscribe` with `source:'sixpackabs'` → the server's
  subscriber store + Resend welcome sequence. **MailerLite is retired** (2026-07-17, [[email-marketing-mailerlite]]):
  `MAILERLITE_API_KEY` is intentionally absent, so "MailerLite sync: false" in the log is normal. CORS open.
- **The redesign is LIVE on production (2026-09-11).** Theme `sixpackabs-child` (repo `sixpackabs/theme/`), video-first
  homepage, `spa_video` pages at /videos/<slug>/, hourly `spa_sync` from absbyai.com `/api/sixpackabs/channel.json` +
  `instagram.json` (public videos only). Staging kept at staging-cac5-danroseconsulting-fedqa.wpcomstaging.com.
  **SSH was never needed and `SPA_SSH_*` is still unset:** deploy = zip the theme, upload in wp-admin but SUBMIT THE FORM
  VIA fetch (a normal click is redirected to the WP.com dashboard and installs nothing; an update answers "already exists"
  → follow its `overwrite=update-theme` link), then **Settings → Caching → Clear all** or WP.com serves the old build to
  plain URLs while `?query=` requests show the new one. `theme.set` on the WP.com connector activates a theme without the
  browser. Rollback = re-activate Twenty Twenty-Five (the July DB template overrides are intact). URL gate
  `sixpackabs/url-check.sh` — 219/219 = 200 on production. Docs: `Docs/SIXPACKABS_SITE.md`, `sixpackabs/README.md`.
- **YouTube:** channel `@absbyai` / `UC236gjadarHAhEhOMYNGJ9g`; Railway already holds the OAuth
  (`GOOGLE_CLIENT_*`, `YOUTUBE_REFRESH_TOKEN`). **The token lists unlisted ads and private drafts** — filter
  `privacyStatus === 'public'` before anything is shown publicly (18 public of 53 uploads on 09-10).
- **Instagram audience account is `@danrosefit`** (IG business id `17841401601139982`), readable with
  `META_ADS_TOKEN`; `media_url` links expire, so download images rather than hotlink.
- Redesign (Sept 2026): spec at `Docs/sixpackabs-redesign/`, handoff
  `Handoffs/handoff-20260910-sixpackabs-homepage-redesign.md`. Dan's rules: app links → `absbyai.com/start` (changed 2026-10-01 from try.sixpackabs.com; UTMs kept; disclaimer link stays);
  **all old blog URLs preserved, no redirects**; staging first, production on his go.

- **Video-page articles (2026-09-22):** all 25 content videos have a Dan-voice article in their /videos/ page notes (rules `sixpackabs/articles/README.md`, `build.py` / `verify.py`; MCP `content-items.update` on `spa_video` works). New videos: /video-setup Step 6b. The theme feeds the excerpt to Yoast as the meta description. danroseconsulting@gmail.com has NO Search Console property for the site. The YouTube OAuth token lacks the captions scope, so transcripts come from Gemini on the public URL (~$0.33 for all 27).
Related: [[instagram-account-state]], [[youtube-upload-capability]], [[repo-is-public]].
