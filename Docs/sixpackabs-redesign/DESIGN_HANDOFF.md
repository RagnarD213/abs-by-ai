# Handoff: SixPackAbs.com homepage redesign (video-first, mobile-first)

## Overview

SixPackAbs.com is being repositioned. Today it is an AI-generated blog that posts other
people's videos. The redesign makes the homepage and all featured content Dan Rose's own
YouTube content from the **Abs by AI** channel (`@AbsbyAI`, channel id
`UC236gjadarHAhEhOMYNGJ9g`), with an accompanying written post per video (the YouTube
description or a lightly edited version of it).

Goals, in priority order:
1. Get views and subscribers on the YouTube channel.
2. Drive traffic to Abs by AI (absbyai.com).
3. Showcase Dan's content and establish his personal brand — the site gets shown to people
   while networking, so it has to look credible and current.

The existing AI-generated blog archive stays published but de-emphasized: reachable only
from the footer ("Article archive"), never from the homepage body.

**Primary CTA everywhere: Subscribe on YouTube.**

## About the design files

The files in this bundle are **design references created in HTML** — prototypes that show
intended look, structure, and behavior. They are not production code to copy directly.

`Homepage Mockups.dc.html` is a streaming-component prototype: it renders a canvas holding
five design options side by side. Only the **turn-2** options are locked and in scope:

- `#2a` — **mobile, 430px wide. This is the primary design.** ~90% of traffic is mobile.
- `#2b` — **desktop, 1280px wide.** Same system, wider layout.

Turn-1 options (`#1a`, `#1b`, `#1c`) are earlier explorations kept for reference. **Do not
build them.** `#1b` was the chosen direction; `#2a`/`#2b` are its refinement.

The site runs on **WordPress**. Implement this design in that environment using its
established patterns — block theme, child theme, or custom theme, whichever fits the current
setup best. Do not ship the prototype HTML as the site. If you think a different stack is
warranted, raise it before building.

Existing structure to preserve: `/blog/`, category archives (`/category/ab-workouts/`,
`/category/nutrition-diet/`, `/category/fat-loss/`, `/category/supplements/`),
`/abs-calculator/`, `/pages/about-us/`, `/contact-us/`, `/partner-with-us/`, and the FAQ
page. The AI app lives at `https://try.sixpackabs.com` and `https://absbyai.com`.

## Fidelity

**High-fidelity.** Colors, typography, spacing, and copy are final. Recreate the UI
faithfully using the codebase's existing libraries and patterns.

Two categories of placeholder remain, and they are obvious in the file:
- Diagonal-striped boxes labelled `youtube thumbnail`, `short`, or `photo` — real
  thumbnails and Instagram images go here.
- Video titles ("Video title from the channel goes here", "Long-form video title goes
  here", "Short title goes here"), durations, and dates — real channel data goes here.

Everything else — headline, bio copy, section labels, button labels, footer links — is final
copy and must be used verbatim.

## Page structure

Same section order on mobile and desktop, top to bottom:

1. Header
2. Headline
3. Featured latest long-form video (large)
4. More free videos (long-form list)
5. Shorts
6. Instagram
7. Bio
8. Newsletter
9. Footer

### 1. Header

Sticky is fine and recommended on mobile.

**Mobile (`#2a`)** — `padding: 16px 18px`, background `#f6f5f2`,
`border-bottom: 1px solid #e7e4dd`, flex row, `space-between`, `align-items: center`.
- Left: SixPackAbs.com logo, `height: 22px`, links to `/`.
- Right, flex row `gap: 10px`:
  - **Subscribe** button — background `#e5322d`, text `#fff`, weight 800, 13px,
    `padding: 9px 14px`, `border-radius: 999px`, small white CSS play triangle (8px left
    border) before the label. Links to the channel with `?sub_confirmation=1`.
  - Hamburger — three `20px × 2px` bars, `#1b1a18`, `border-radius: 2px`, `gap: 4px`,
    `padding: 6px 2px`. Opens a menu (see Interactions).

**Desktop (`#2b`)** — `padding: 22px 64px`, `border-bottom: 1px solid #e7e4dd`, three
groups spread with `space-between`.
- Logo `height: 28px`.
- Nav: Videos · Shorts · About Dan · Abs Calculator · Collab — 14px, weight 600, `#6e6b64`,
  `gap: 30px`. Hover to `#1b1a18`.
- Right, `gap: 10px`: **Try the AI App** (outline `1px solid #d9d5cc`, weight 700, 14px,
  `padding: 11px 18px`, `border-radius: 999px`) and **Subscribe** (`#e5322d` fill, `#fff`,
  weight 800, 14px, same padding/radius, play triangle before the label).

### 2. Headline

Copy, verbatim, both breakpoints:

> Learn How To Get Six Pack Abs With Dan's Free YouTube Videos

- Mobile: `padding: 26px 18px 20px`; `font-size: 34px`, weight 800, `line-height: 1.08`,
  `letter-spacing: -0.025em`, `text-wrap: balance`, left-aligned.
- Desktop: `padding: 44px 64px 18px`; centered, `max-width: 900px`, `font-size: 52px`,
  weight 800, `line-height: 1.06`, `letter-spacing: -0.025em`, `text-wrap: balance`.

This is the only `<h1>` on the page. No subhead, no avatar, no byline line — those were
removed deliberately.

### 3. Featured latest long-form video

A card: background `#fff`, `1px solid #e7e4dd`, `border-radius: 18px` (mobile) / `20px`
(desktop), `padding: 12px 12px 16px` (mobile) / `14px 14px 20px` (desktop). The whole card
is one link.

Inside, top to bottom:
- **Thumbnail** — `aspect-ratio: 16/9`, `border-radius: 12px` (mobile) / `14px` (desktop),
  `overflow: hidden`. Centered red play button: `#e5322d` circle, 64px (mobile) / 84px
  (desktop), white CSS play triangle, `box-shadow: 0 8px 24px rgba(0,0,0,.3)` /
  `0 12px 34px rgba(0,0,0,.28)`. Duration pill bottom-right: `rgba(0,0,0,.78)`, `#fff`,
  12px/13px, weight 700, `padding: 4px 8px`, `border-radius: 6px`.
- **Eyebrow** — `LATEST VIDEO`, 12px, weight 800, `letter-spacing: 0.1em`, `#e5322d`.
- **Title** — 21px (mobile) / 30px (desktop), weight 800, `line-height: 1.22` / `1.16`,
  `letter-spacing: -0.01em` / `-0.015em`.
- **Excerpt** — first 2–3 lines of the YouTube description. 15px/16px,
  `line-height: 1.55`/`1.6`, `#6e6b64`, `max-width: 720px` on desktop.
- **Link cue** — `Watch + read the notes →`, 14px/15px, weight 700, `#2f5fe0`.

Text block: `padding: 0 4px` (mobile) / `0 8px` (desktop), `gap: 8px` / `10px`.

### 4. More free videos (long-form)

Section heading `More free videos` with an `All →` link on the right (`#2f5fe0`, 14px,
weight 700), baseline-aligned.

- **Mobile** — stacked list under the featured card, `gap: 14px`. Each row is
  `grid-template-columns: 140px 1fr`, `gap: 12px`, `align-items: start`. Thumbnail
  `aspect-ratio: 16/9`, `border-radius: 10px`, duration pill bottom-right (10px, weight
  700, `padding: 2px 5px`, `border-radius: 4px`). Title 15px, weight 700,
  `line-height: 1.3`, clamped to 2 lines. 4 rows, then a full-width outline button
  `Watch all videos` (`1px solid #d9d5cc`, `border-radius: 999px`, `padding: 14px`,
  weight 800, 15px, centered).
- **Desktop** — right-hand rail beside the featured card:
  `grid-template-columns: 1fr 400px`, `gap: 28px`, `align-items: start`, section padding
  `26px 64px 56px`. 5 rows, each `grid-template-columns: 150px 1fr`, `gap: 14px`, with a
  date line under the title (13px, `#6e6b64`). Then the same `Watch all videos` outline
  button (`padding: 13px`, 14px text).

This large-featured-plus-rail arrangement is the point of the section — Dan asked for it
specifically. Keep it.

### 5. Shorts

Full-bleed band: background `#fff`, `border-top` and `border-bottom: 1px solid #e7e4dd`.
Heading `Shorts` + `All →` (mobile) / `All shorts →` (desktop).

- **Mobile** — horizontal scroll rail, `padding: 26px 0 28px`, items `gap: 12px`, side
  padding `0 18px`. Each item `width: 124px`, thumbnail `aspect-ratio: 9/16`,
  `border-radius: 12px`, 34px `rgba(0,0,0,.6)` circular play button centered. Title 13px,
  weight 700, `line-height: 1.25`. A 60px gradient sliver
  (`linear-gradient(90deg,#f0ede6,#f6f5f2)`) sits at the end of the rail as a scroll
  affordance — in production use real overflow scrolling with
  `-webkit-overflow-scrolling: touch`, `scroll-snap-type: x mandatory`, and hidden
  scrollbars; the gradient sliver is then optional.
- **Desktop** — `padding: 56px 64px`, `grid-template-columns: repeat(6, 1fr)`, `gap: 16px`.
  Thumbnail `aspect-ratio: 9/16`, `border-radius: 14px`, 44px play circle. Title 14px,
  weight 700, `line-height: 1.28`.

### 6. Instagram

Heading `On Instagram` + `@absbyai →` link (`#2f5fe0`, 14px, weight 700). Confirm the
handle before shipping.

**Images only — no captions, no like counts, no embedded Instagram widget chrome.**

- **Mobile** — `padding: 26px 18px 28px`, `grid-template-columns: repeat(3, 1fr)`,
  `gap: 6px`, square cells, no radius.
- **Desktop** — `padding: 56px 64px`, `grid-template-columns: repeat(6, 1fr)`, `gap: 10px`,
  square cells.

Each cell links out to the post on Instagram.

### 7. Bio

Background `#fff`, `border-top: 1px solid #e7e4dd`.

Photo of Dan showing **face and abs** — `public/img/dan-founder.jpg` in this bundle,
`aspect-ratio: 4/5`, `object-fit: cover`, `object-position: top`.

- **Mobile** — photo full-bleed edge to edge at the top of the section, text below
  (`padding: 24px 18px 0`, `gap: 14px`).
- **Desktop** — `padding: 64px`, `grid-template-columns: 460px 1fr`, `gap: 56px`,
  `align-items: center`; photo `border-radius: 20px`, text on the right.

Heading, verbatim:

> Meet SixPackAbs.com CEO Daniel Rose

26px (mobile) / 44px (desktop), weight 800, `line-height: 1.12` / `1.06`,
`letter-spacing: -0.02em` / `-0.025em`. No eyebrow label above it — the "ABOUT DAN" kicker
was removed deliberately.

Body copy, verbatim:

> Hi, I'm Dan. I'm one of the original founders of Six Pack Shortcuts and SixPackAbs.com,
> and I'm back with a new YouTube channel. Subscribe to the channel to get new videos every
> week from me showing you how to lose your belly fat and get six pack abs.

16px (mobile) / 18px (desktop), `line-height: 1.6`, `#6e6b64`, `max-width: 600px` on
desktop.

Buttons: **Try Abs by AI free** (fill `#1b1a18`, `#fff`, weight 800, 15px,
`border-radius: 999px`) and **Read my story** (outline `1px solid #d9d5cc`, same
type/radius). Stacked full-width on mobile, side by side on desktop.

The Abs by AI link should carry UTM parameters, matching the pattern already on the live
site: `https://absbyai.com/?utm_source=sixpackabs&utm_medium=homepage&utm_campaign=bio`

### 8. Newsletter

Dark block: background `#1b1a18`, text `#fff`, `border-radius: 20px` (mobile, inside
`padding: 26px 18px 30px`, block `padding: 24px`) / `24px` (desktop, `margin: 64px`,
`padding: 52px`, two equal columns, `gap: 40px`, `align-items: center`).

- Heading: `New video, new notes. One email each.` — 22px (mobile) / 30px (desktop),
  weight 800, `line-height: 1.15` / `1.1`, `letter-spacing: -0.01em` / `-0.02em`.
- Sub: `Get every new video plus the written breakdown.` — 14px/15px, `#a29e95` (fine on
  this dark ground).
- Field: background `#2a2926`, `border-radius: 999px`, `padding: 14px 18px` / `15px 20px`,
  placeholder `you@email.com`, 14px. Submit `Join` — `#fff` fill, `#1b1a18` text, weight
  800, `border-radius: 999px`. Stacked on mobile, inline on desktop.

Wire to the existing email provider. Match the behavior of the current site's "Get the ab
blueprint + your free AI after-photo" opt-in and confirm which list it feeds.

### 9. Footer

- **Mobile** — `border-top: 1px solid #e7e4dd`, `padding: 22px 18px 34px`, two-column grid
  of links (`gap: 12px`, 14px, weight 600, `#6e6b64`): YouTube · Instagram · Try the AI App ·
  Abs Calculator · Contact / Collab · Article archive. Below:
  `© 2026 SixPackAbs.com · Georgetown, TX` — 12px, `#6e6b64`.
- **Desktop** — `padding: 28px 64px 44px`, `border-top: 1px solid #e7e4dd`, two link rows
  spread with `space-between`, 13px, `#6e6b64`, `gap: 24px`. Left: YouTube · Instagram ·
  Contact / Collab · Try the AI App. Right: Article archive · Abs Calculator · Disclaimer.

`Article archive` points at the legacy AI-generated blog (`/blog/`). It stays indexed but
appears nowhere except the footer.

## Interactions & behavior

- **Video cards** — clicking anywhere on a card opens the video. Preferred: an internal post
  page per video (`/videos/<slug>/`) with the embedded player plus the written notes. That
  keeps people on the site and gives each video an indexable page; the
  `Watch + read the notes →` cue implies exactly that. Play the embed in place on the post
  page; never autoplay on the homepage.
- **Lazy embeds** — do not load YouTube iframes on the homepage. Render thumbnail + play
  button and swap in the iframe on click (facade pattern), or link straight to the post page.
  The homepage must stay fast on mobile.
- **Mobile menu** — hamburger opens a full-screen overlay with the desktop nav items (Videos,
  Shorts, About Dan, Abs Calculator, Collab) plus Try the AI App and Subscribe. Slide or fade
  in, 200ms `ease-out`. Trap focus, close on Escape and on backdrop tap.
- **Shorts rail (mobile)** — native horizontal scroll with snap. No custom drag JS.
- **Hover (desktop)** — thumbnails lift subtly (`transform: translateY(-2px)`, 150ms
  `ease-out`) and/or the title takes `#2f5fe0`; nav links darken `#6e6b64` → `#1b1a18`;
  buttons darken ~6%. Keep it restrained.
- **Focus states** — visible ring on every link, button, and field:
  `outline: 2px solid #2f5fe0; outline-offset: 2px`. The prototype does not show these; they
  are required.
- **Newsletter form** — inline validation on blur, inline success and error messages inside
  the dark block, disabled submit while in flight, no page reload.
- **Loading / empty states** — if the channel feed is empty or fails, keep the headline, bio,
  and newsletter and hide the affected video section rather than rendering empty stripes.
- **Images** — `loading="lazy"` below the fold; explicit width/height or `aspect-ratio` to
  prevent layout shift; `srcset` for the bio photo and thumbnails.

## Responsive behavior

Mobile-first. Build the 430px design first, then layer up.

- **< 768px** — the `#2a` layout. Single column. Header = logo + Subscribe + hamburger.
  Stacked long-form list. Shorts as a scroll rail. Instagram 3-up. Full-bleed bio photo.
- **768px – 1023px** — transitional: full nav can appear; long-form list may go 2-up; Shorts
  4-up; Instagram 4-up or stay 3-up; bio still stacked, or side-by-side with a narrower
  photo column.
- **≥ 1024px** — the `#2b` layout. Featured video + 400px rail, Shorts 6-up, Instagram 6-up,
  bio side-by-side. Content max-width ~1280px, centered, 64px gutters.

Touch targets minimum 44px on mobile.

## Data / content model

Each **video** needs: YouTube id, title, description (used as the post body), duration,
published date, thumbnail, type (long-form or short), and a slug.

- Source: the channel RSS feed
  `https://www.youtube.com/feeds/videos.xml?channel_id=UC236gjadarHAhEhOMYNGJ9g`
  (title, id, published date — no duration) or the YouTube Data API v3 (`playlistItems` on
  the uploads playlist + `videos?part=contentDetails` for duration). Prefer the API if a key
  is available — it gives duration and lets you separate Shorts.
- **Shorts vs. long-form** — YouTube exposes no explicit flag. Split on duration
  (`≤ 180s` = short) and/or a dedicated playlist Dan maintains. A manual override field is
  worth having.
- Cache aggressively and refresh on a schedule (hourly is plenty). Never call the API on page
  render.
- In WordPress, a `video` custom post type with these fields, populated by a scheduled
  import, is the natural fit: each video becomes an indexable page with real content, and the
  homepage stays a normal template query.

**Instagram** — 6 most recent images. The Instagram Basic Display / Graph API needs a
long-lived token and periodic refresh; a curated, manually updated set of 6 images is an
acceptable v1 if that is faster. Images only.

Confirm with Dan: the exact Instagram handle, whether homepage counts should stay at 4/5
long-form and 6 shorts as drawn, and which email list the newsletter feeds.

## Design tokens

**Colors**

| Token | Hex | Use |
| --- | --- | --- |
| Page background | `#f6f5f2` | Body ground |
| Surface | `#ffffff` | Cards, Shorts band, bio band |
| Ink | `#1b1a18` | Headings, primary text, dark blocks, primary button fill |
| Ink muted | `#6e6b64` | Body copy, nav, dates, footer links (4.5:1+ on light grounds) |
| Ink faint | `#a29e95` | Placeholder labels; muted text on the dark block ONLY |
| Hairline | `#e7e4dd` | Section dividers |
| Border | `#d9d5cc` | Outline buttons |
| Dark field | `#2a2926` | Newsletter input |
| Accent red | `#e5322d` | Subscribe, play button, LATEST VIDEO eyebrow |
| Accent blue | `#2f5fe0` | Links, "All →", link cues, focus ring |

Contrast rule that came out of review: **never use `#a29e95` for real content on a light
background** (≈2.1:1). `#6e6b64` (≈5.4:1) is the muted-text token on light. `#a29e95` is
fine on `#1b1a18`.

**Typography** — Manrope (Google Fonts), weights 400/500/600/700/800. Same family as
absbyai.com, so the two properties read as one brand. Fallback:
`Manrope, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`.

| Role | Mobile | Desktop |
| --- | --- | --- |
| H1 | 34px / 800 / 1.08 / -0.025em | 52px / 800 / 1.06 / -0.025em |
| Section H2 | 19px / 800 / -0.01em | 30px / 800 / -0.02em |
| Bio H2 | 26px / 800 / 1.12 / -0.02em | 44px / 800 / 1.06 / -0.025em |
| Featured video title | 21px / 800 / 1.22 | 30px / 800 / 1.16 |
| Card title | 15px / 700 / 1.3 | 15px / 700 / 1.3 |
| Shorts title | 13px / 700 / 1.25 | 14px / 700 / 1.28 |
| Body | 15–16px / 400 / 1.55–1.6 | 16–18px / 400 / 1.6 |
| Eyebrow | 12px / 800 / 0.1–0.12em / uppercase | same |
| Button | 13–15px / 800 | 14–15px / 800 |
| Meta, footer | 12–14px / 600 | 13px / 600 |

**Spacing** — 4px base. Mobile section padding `26px 18px 28px`; desktop `56px 64px`.
Gaps in use: 6, 8, 10, 12, 14, 16, 18, 20, 22, 26, 28, 40, 56, 64.

**Radius** — `6px` duration pills · `10–14px` thumbnails · `18–20px` cards ·
`20–24px` newsletter block · `999px` all buttons and inputs · `50%` play circles ·
`0` Instagram cells.

**Shadow** — play button `0 8px 24px rgba(0,0,0,.3)` (mobile) /
`0 12px 34px rgba(0,0,0,.28)` (desktop). Cards use borders, not shadows.

## Assets

In `public/img/` in this bundle, all from the `RagnarD213/abs-by-ai` repo (`main` branch,
`public/img/`):

- `sixpackabs-logo.webp` — header/footer logo (wordmark + shield). Dark artwork; invert on
  dark grounds.
- `dan-founder.jpg` — the bio photo (face + abs). Used at `4/5`, `object-position: top`.
- `dan-avatar.jpg` — round avatar. Not in the locked design; kept for post pages.
- `logo.png` — Abs by AI logo, for AI-app CTAs.
- `video-poster.jpg` — used only in the turn-1 explorations; not part of the locked design.
- `sixpackabs-icon-192.png` — favicon / app icon.

**Still needed from Dan**: real YouTube thumbnails (automatic once the feed is wired), 6
Instagram images, and his preferred bio shot if `dan-founder.jpg` is not it. Dan has a local
folder of finalized social photos that has not been handed over yet.

Fonts: Manrope from Google Fonts. Self-host if the theme's performance budget calls for it.

## SEO and analytics notes

- Current homepage title/description are "SixPackAbs.com - Learn How To Get Six Pack Abs" /
  "The ultimate guide to six pack abs workouts, nutrition, and supplements". Revisit to
  reflect the video-first positioning.
- Per-video pages should carry `VideoObject` structured data (name, description,
  thumbnailUrl, uploadDate, duration, embedUrl) and `og:video` tags.
- Keep the legacy archive URLs live — no redirects, no deletions. They stay indexed.
- The properties already run Site Kit by Google, a Meta pixel, and a TikTok pixel. Carry over
  whatever the current theme has and add outbound-click events on Subscribe, Instagram, and
  Try the AI App so the traffic goals are measurable.

## Files in this bundle

- `Homepage Mockups.dc.html` — the design prototype. Build `#2a` (mobile) and `#2b`
  (desktop). Ignore `#1a`, `#1b`, `#1c`.
- `support.js` — runtime for the prototype file. Needed only to view it in a browser; not
  part of the deliverable.
- `public/img/*` — the assets listed above.
- `github.md` — records the associated source repo, branch, and which files the design drew
  from.

Open `Homepage Mockups.dc.html` directly in a browser to see the design.
