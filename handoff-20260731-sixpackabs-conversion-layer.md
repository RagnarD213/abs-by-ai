# Handoff: SixPackABS.com conversion layer (hero, inline CTAs, email capture)

**Date:** 2026-07-31
**Project:** sixpackabs.com → Abs By AI funnel
**Business goal this serves:** Profitability (turn existing blog traffic into Abs By AI users)

## Objective

SixPackABS.com gets ~533 views/month and currently sends **zero** of them to Abs By AI — there is no mention of the product anywhere on the site, no ads, no email capture. Install a site-wide conversion layer so every current and future visitor is pointed at absbyai.com: a homepage hero promoting the app, an Abs By AI promo block injected into all posts, email capture feeding the existing Resend welcome sequence, and UTM tagging so the funnel is measurable in PostHog. This is one-time work that monetizes all future traffic before any traffic-growth effort begins.

## Current State

- **sixpackabs.com** is a WordPress.com **Atomic** site (blog_id `253647467`, theme Twenty Twenty-Five, 0 active plugins, healthy). Atomic = plugin installs, SFTP/SSH, and full WP REST API are all available. The WordPress.com MCP tools in Claude Code have confirmed site-scoped access (`wpcom-user-sites` returns `mcp_access: available`).
- Content: 113 posts, 44 pages. Categories: Ab Workouts, Nutrition & Diet, Fat Loss, Supplements. Pages include Blog, About, Contact, FAQ, partnerships. Standard blog layout, no hero, no monetization, no Abs By AI mention, ~533 monthly views (Jetpack stats).
- **absbyai.com** funnel (the destination): 3 free generations → locked 4th image paywall (server-side teaser now, leak fixed) → credit packs / $19.99 mo / $69.99 yr membership with 7-day trial. Proof before/after images live in the repo at `public/img/proof/` (male and female pairs, .webp).
- **Email:** a live 5-email Resend welcome sequence (day 0/2/4/7/10) already sells Abs By AI. Subscribers enter via `POST /api/subscribe` on the absbyai.com server (`server.js`). The blog currently feeds it nothing.
- **Analytics:** PostHog project 458833 (us.posthog.com) tracks absbyai.com. The blog has only Jetpack stats.
- Compliance context: absbyai.com's proof strip now labels example images "AI-GENERATED" with a disclosure line linking `/disclaimer` (shipped 2026-07-30 for Google Ads compliance). The blog's promo imagery should follow the same honesty standard.

## Key Decisions Already Made

- **Keep the informational content; do not convert the site to pure Abs By AI content.** The 113 posts are the only SEO surface area. The conversion layer changes, not the content.
- **Inject the in-post CTA programmatically (a `the_content` filter), not by editing 113 posts.** One snippet inserts the block after ~paragraph 3 and at end-of-post on all singles; copy stays centrally editable and applies to future posts automatically.
- **Email capture feeds the EXISTING Resend sequence** — no second list, no new email tool.
- **Hero is before/after imagery + CTA for now**; it gets swapped to Dan's video after the shoot (separate handoff: `handoff-20260731-sixpackabs-video-centerpiece.md`).
- **No display ads (AdSense etc.)** — not worth it under ~50k views/month and they'd compete with our own promos.
- UTM convention: `utm_source=sixpackabs&utm_medium=blog&utm_campaign=<unit>` where unit ∈ `hero`, `inline_cta`, `endpost_cta`, `exit_popup`, `footer`.

## Detailed Plan

1. **Confirm tooling.** Verify the WordPress.com MCP site tools work against blog_id 253647467 (list posts, read a page). If MCP editing is clumsy, fall back to the WP REST API with an application password (Dan creates it in wp-admin → Users → Profile; do not paste it into chat/commits).
2. **Assets.** Take the male + female before/after pairs from the abs-by-ai repo `public/img/proof/` and upload to the WP media library. Every "after" image must be labeled **"AI-generated example"** on or beside the image (matches the compliance treatment on absbyai.com).
3. **Homepage hero.** Twenty Twenty-Five is a block theme — edit the home template via the Site Editor (or set a static front page). Hero contents: headline ("See yourself with abs — free"), sub-line ("Upload one photo. Our AI shows you your after photo in 30 seconds. 3 free tries."), before/after image pair, button → `https://absbyai.com/?utm_source=sixpackabs&utm_medium=blog&utm_campaign=hero`, small AI-generated-example disclosure. Blog posts remain below the hero.
4. **Inline + end-of-post CTA.** Install the **WPCode** (or Code Snippets) plugin. Add a PHP snippet filtering `the_content` on single posts: (a) after the 3rd paragraph, insert a compact promo card (before/after thumbnails + one line + button, `utm_campaign=inline_cta`); (b) at the end of the post, a larger variant with different framing (`utm_campaign=endpost_cta`). Optional nice-to-have: swap the one-liner by category (Nutrition → "See what's under there"; Workouts → "See where the work leads"). Style inline with the theme's fonts; mobile-first.
5. **Email capture.** A simple form (end-of-post variant + a footer block): "Get the ab blueprint + your free AI after-photo" → email field. It should `POST` to `https://absbyai.com/api/subscribe`.
   - **OPEN (small server change in the abs-by-ai repo):** check `server.js` `/api/subscribe` for the exact payload shape and add a CORS allowance for the `https://sixpackabs.com` origin on that one endpoint (it currently serves same-origin only). Also pass a `source: "sixpackabs"` field if the endpoint stores one, so list growth is attributable. Commit, push, Railway deploy, verify live per standard delivery rules.
6. **Analytics.** Add the PostHog snippet (project 458833) to the blog via WPCode header injection so CTA clicks and pageviews are visible alongside absbyai.com data. At minimum, verify after launch that sessions with `utm_source=sixpackabs` appear in PostHog on absbyai.com.
7. **Optional, last:** exit-intent popup with the before/after slider (`utm_campaign=exit_popup`). Ship the rest first; add this only if time remains — it's the highest-friction unit and the easiest to get wrong on mobile.
8. **Verify.** Browser check at 375×812 and desktop: hero renders, CTA block appears in at least 3 different posts (short post, long post, list-style post), links carry correct UTMs, email form submits and the subscriber appears via the absbyai admin/API, no console errors, no layout breakage. Then click through from the live blog to absbyai.com and confirm the UTM session lands in PostHog.
9. **Close out:** commit/push any abs-by-ai repo changes (the CORS bit), verify Railway deploy, and check off the dashboard task per AI_COORDINATION.md Rule 9.

## Things to Avoid / Lessons Learned

- **Do not hand-edit 113 posts.** The filter approach is the whole point — reversible, centrally editable, future-proof.
- **Do not create a separate email list** (Jetpack subscriptions, Mailchimp, etc.). The Resend sequence is live and already sells the app; a second list fragments it.
- **Don't paste credentials into chat or commits.** Two tokens have had to be rotated before in this project. WP application password goes straight into the keychain/env.
- The abs-by-ai repo is **public** — the only change to it here is the CORS/source tweak; nothing sensitive.
- Any push to abs-by-ai `main` triggers a Railway deploy — batch the server change into one commit.
- Honest labeling on AI imagery is not optional — it protects the Google Ads work already shipped and the App Store listing.

## Relevant Files & Locations

- WordPress: sixpackabs.com, blog_id `253647467`, WordPress.com Atomic, wp-admin at sixpackabs.com/wp-admin (Dan's WordPress.com account)
- Abs By AI repo: `~/Documents/Claude/Projects/Abs By AI` — `server.js` (`/api/subscribe`), `public/img/proof/` (before/after assets)
- PostHog: us.posthog.com, project 458833
- Resend sequence details: `HANDOFF_resend_autoresponder.md` + memory `resend-welcome-autoresponder`
- Related handoffs: `handoff-20260731-sixpackabs-ai-keyword-content.md`, `handoff-20260731-sixpackabs-video-centerpiece.md`, `handoff-20260731-sixpackabs-paid-amplification.md`

## Model & Effort Recommendation

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | Claude Sonnet 5, standard thinking |
| **If Claude usage is high / approaching a limit** | Still Claude (Sonnet 5) for the CTA/hero copy — that's brand voice. The mechanical parts (WPCode snippet, CORS change, UTM plumbing) can go to Codex (flagship, medium effort) if the copy is written first and pasted in. |

Task-type override: the promo copy is marketing/brand-voice work → Always-Claude. Everything else is routine implementation.

## Starter Prompt for the Next Task

> Execute `handoff-20260731-sixpackabs-conversion-layer.md` in the Abs By AI project root. Goal: install the Abs By AI conversion layer on sixpackabs.com — homepage hero, programmatic inline + end-of-post CTA blocks on all posts, email capture feeding the existing Resend sequence via absbyai.com `/api/subscribe` (needs a small CORS change in server.js), PostHog + UTM tracking. First action: verify the WordPress.com MCP tools can read and edit sixpackabs.com (blog_id 253647467), then read `server.js` `/api/subscribe` to confirm the payload shape. All decisions are settled in the doc — don't relitigate them.
