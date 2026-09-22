# Video-page articles on sixpackabs.com

Every public YouTube video already has a page at `sixpackabs.com/videos/<slug>/` (the hourly `spa_sync`
creates it, see `sixpackabs/README.md`). Its body starts as the YouTube description. We replace that body
with a real article written from the video's own words, so the page can rank in Google. One URL per video:
never a separate blog post for the same video.

Once the notes are edited, the sync never overwrites them again (hash check in `inc/sync.php`). Title, date,
thumbnail and length keep following YouTube.

## Files

- `<youtube-id>.md`: one article. Front matter `id`, `post_id`, `slug`, `excerpt`; body in the small markdown
  dialect `build.py` understands (`## `, `### `, `- `, `1. `, `**bold**`, `[text](url)`, a `_..._` line = italic
  note). `{CTA}` in a link URL becomes the app link with the UTM.
- `build.py --check *.md`: word counts plus the rule checks. `build.py <file>` prints the update payload.

## Rules

- **Source = the video's words.** Transcript from a local `.srt`/`.transcript.json` next to the final, or
  Gemini on the public YouTube URL (the YouTube OAuth token has no captions scope). Never invent a claim the
  video does not make. If the video states something inaccurate, soften or drop it rather than repeat it.
- **Voice: Dan, first person**, plain and specific, talking to "you". Opening line = the strongest true claim or
  the answer, then the answer in two sentences. Never "Today we're talking about". Paragraphs end on the payoff.
  Read `.claude/skills/scriptfromoutline/SKILL.md` (WHAT DAN CHANGED) and memory `dan-personal-facts-for-scripts`.
- **Structure:** title stays the YouTube title (it is the H1). Answer up top, H2 sections that follow the video,
  a steps list where it fits, one CTA line, then the italic note.
- **Length:** long-form 800 to 1,500 words (a 20+ minute video may run a bit over). Short: 300 to 500 words,
  and only when it answers a searchable question. Skip brag/teaser Shorts and Shorts that would compete with a
  page on the same topic.
- **CTA:** exactly one, `[...]({CTA})` → `try.sixpackabs.com` with `utm_source=sixpackabs&utm_medium=blog&
  utm_campaign=video-article&utm_content=<video-id>`.
- **Links:** 1 to 3 internal links (`/videos/...` pages or old posts). `build.py` enforces this.
- **Excerpt = the meta description** (the theme feeds it to Yoast): under 155 characters, answers the question.
- **Compliance:** "This is general fitness information, not medical advice." on every article; add "Some images in
  the video are AI-generated visualizations, and they're labeled." when the video shows AI imagery. No
  unbelievable claims. Never call Dan a marketer or ad agency owner. Never "my wife" (girlfriend). Swears aim
  at advice, never at people. No slurs or shock comparisons even if said on camera.
- **No names of the old company's owners, partners or staff (e.g. Mike Chang) and nothing about the 2019 sale**,
  even when the video says it: the sale agreement has an open-ended clause on naming them in apps and
  presentations, and a confidentiality covenant on the transaction (memory `harter-sixpackabs-dispute`). "One of the
  original founders of Six Pack Shortcuts and SixPackAbs.com" is fine.
- **No em dashes and no en dashes.** `build.py` refuses a file containing either.
- Ads are never organic: only public content videos get articles (the feed already excludes unlisted ads).

## Publishing

WordPress.com MCP, site `253647467`: `content-items.update` with `post_type: spa_video`, `id: <post_id>`,
`excerpt`, `content` (the `build.py` output), `user_confirmed: true`. Then verify the live page: the article is
in `.spa-notes`, `<meta name="description">` equals the excerpt, no em dash inside the notes. Updates purge the
edge cache for that page; no manual cache clear is needed.
