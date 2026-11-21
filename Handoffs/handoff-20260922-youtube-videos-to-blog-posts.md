# Handoff: turn every YouTube video into a real blog post on sixpackabs.com

Written 2026-09-22 by Claude (Opus 5.5). Status: EXECUTED 2026-09-22 (25 articles live, 2 Shorts skipped as duplicates; see `sixpackabs/articles/`).

## Goal

Every public YouTube video on `@absbyai` gets a real written article on sixpackabs.com that Google can rank, with
the video embedded. Then keep it that way for every new video.

## Why

- The 09-22 GA4 analysis: real traffic is about 4 to 5 engaged sessions a day, and **Google search is the only
  channel that works** (66% engaged, 33 s average). More indexable pages that answer real searches is the
  cheapest growth. Dan already makes the videos; the article is the missing piece.
- Target reader: someone who searched a question ("how to do a stomach vacuum", "is milk bad for abs") and has
  never heard of Dan.

## What already exists (do NOT rebuild it)

The live child theme (`sixpackabs/theme/sixpackabs-child/`, docs `sixpackabs/README.md`, `Docs/SIXPACKABS_SITE.md`)
already runs an hourly sync, `spa_sync`, that creates a **`spa_video` page at `/videos/<slug>/`** for every public
video from `https://absbyai.com/api/sixpackabs/channel.json` (27 public videos on 09-22, Shorts included). Those
pages are in the Yoast sitemap (`spa_video-sitemap.xml`). Their body ("notes") is just the YouTube description,
which is thin and repeats the same CTA and disclaimer text on every page.

Key sync behavior: **once the notes or excerpt are edited, the sync never overwrites that text again** (it
compares a hash of what it imported). Title, date, thumbnail and length keep following YouTube.

## Decision (made, do not re-litigate)

**Write the article INTO the existing `/videos/<slug>/` page's notes. Do not create a separate blog post.** One
URL per video avoids two pages competing for the same search, keeps the sitemap, and uses the sync's hash rule so
the article is never clobbered. First, confirm on one page that the article renders fully (headings, lists, the
embed above it) and that Yoast outputs a proper title/meta description for `spa_video`. If the template truncates
or hides the notes, fix the template in the child theme (deploy steps in `sixpackabs/README.md`: zip upload via
fetch, then Settings → Caching → Clear all) before writing more.

## Scope and order

1. **Long-forms first** (over 3:00): e.g. "My Top 10 Tips For Getting Six Pack Abs (At 40 Years Old)",
   "Use AI To Get REAL Six Pack Abs - 6 Strategies That Work", "Ab Wheel Workout: 3 Sets...", "Ab Wheel: Most
   Underrated Ab Exercise", the follow-along workouts. Full article, 800 to 1,500 words.
2. **Shorts** (3:00 or less): a short article, 300 to 500 words, only when the Short answers a searchable
   question (stomach vacuum, jump rope, milk, protein shake, breakfast). Skip pure brag or teaser Shorts and report
   which were skipped.
3. Pilot: write **2 long-forms + 1 Short**, publish, verify, show Dan the three URLs in chat, then continue with the
   rest without waiting (bias toward action; Dan can redirect).

## How to write each article

- **Source = the video's own words.** Get the transcript from, in order: a local `*.transcript.json` / `.srt`
  next to the final in the project folders; YouTube captions via the channel OAuth (Railway `GOOGLE_CLIENT_*`,
  `YOUTUBE_REFRESH_TOKEN`; see `scripts/youtube/`); or transcribe the final file. Never invent claims the video
  does not make.
- Structure: a search-style H1 is the page title (already set from YouTube; keep it), a 2-sentence answer up top,
  H2 sections that follow the video, a short "Do it yourself" or steps list where it fits, then one CTA.
- **Voice: Dan's first person**, plain, specific. Read `memory/dan-personal-facts-for-scripts.md` and
  `memory/script-zero-edit-lessons.md` first. No generic listicle filler (memory `video-outline-style`).
- **CTA:** one closing line pointing to the app using the site's convention (`try.sixpackabs.com`, per the site
  rules) with UTM `utm_source=sixpackabs&utm_medium=blog&utm_campaign=video-article&utm_content=<video-id>`.
- **Compliance:** no unbelievable claims (memory `ad-copy-no-unbelievable-claims`); keep "Not medical advice" and
  the AI-image disclaimer where AI imagery is shown; label any AI-generated image. Never call Dan a marketer or ad
  agency owner. Never "my wife" (he has a girlfriend).
- **SEO basics:** Yoast meta description (under 155 characters, answers the question), 1 to 3 internal links to
  related old posts or other `/videos/` pages, descriptive alt text on any image.
- **No em dashes, anywhere** (Dan's rule). Run `grep -c $'\u2014'` (the em dash character, U+2014) on each article before publishing: must be 0. No en
  dash substitutes either.
- Do not use the `anthropic-skills:blog-posts` skill as is: it writes about other people's videos into a .docx.
  Follow this doc.

## Publishing mechanics

- WordPress.com MCP (`wpcom-mcp-content-authoring`) can edit posts on blog id `253647467`; check it supports the
  `spa_video` post type. If not, use the wp-admin editor via Claude in Chrome (Videos menu).
- Standing authorization covers publishing content on sixpackabs.com. It does NOT cover deleting any post or
  page, or changing URLs. Old blog URLs stay as they are.
- Verify each live page: renders, embed plays, article visible, meta description present, no em dashes.

## Keep it going (phase 2 of this handoff)

Add one step to the `/video-setup` skill (`.claude/skills/video-setup/SKILL.md`): once a content video is public
and its `/videos/<slug>/` page exists (up to an hour later), write its article by this doc's rules. Only
**content** videos: ads are never organic (unlisted, and the feed already filters them out). Build the skill step,
do not run it on a new video in the same session.

## Finish

1. In chat: list of URLs written, word counts, skipped Shorts with reason.
2. Request indexing for the new pages in Google Search Console (sixpackabs.com property) if accessible.
3. Two weeks later (a morning brief item): Search Console impressions for `/videos/` pages.
4. Delete this line from `AI_COORDINATION.md` HANDOFFS and the row in `Handoffs/README.md`; commit and push. No
   dashboard row; do not add one.

## Starter prompt

```
Execute Handoffs/handoff-20260922-youtube-videos-to-blog-posts.md. Write a real article into each existing
sixpackabs.com /videos/<slug>/ page from the video's own transcript, long-forms first, pilot 3 then continue,
verify each live, then add the ongoing step to /video-setup and close the handoff.
```

Recommended: **Claude Opus 5.5, High effort** (this is writing in Dan's voice, where quality matters most).
