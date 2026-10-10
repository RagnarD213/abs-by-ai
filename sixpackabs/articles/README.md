# Video-page articles on sixpackabs.com

> **Shared writing rules (2026-10-06):** before writing, read `.claude/skills/_shared/WRITING-RULES.md`. It holds the rules every writing skill follows and the list of memory entries (`Docs/memory/`) to read. Where it and this skill disagree, the newer dated line wins.

Every public YouTube video already has a page at `sixpackabs.com/videos/<slug>/` (the five-minute `spa_sync`
creates it about 15 minutes after release, see `sixpackabs/README.md`). Its body starts as the YouTube description. We replace that body
with a real article written from the video's own words, so the page can rank in Google. One URL per video:
never a separate blog post for the same video.

Once the notes are edited, the sync never overwrites them again (hash check in `inc/sync.php`). Title, date,
thumbnail and length keep following YouTube.

## Files

- `<youtube-id>.md`: one article. Front matter `id`, `post_id`, `slug`, `excerpt`; body in the small markdown
  dialect `build.py` understands (`## `, `### `, `- `, `1. `, `**bold**`, `[text](url)`, a `_..._` line = italic
  note). `{CTA}` in a link URL becomes the app link with the UTM.
- `build.py --check *.md`: word counts plus the rule checks. `build.py <file>` prints the update payload.
- `TBD-<slug>.md`: a draft written at setup, before the video is public. Front matter `id: TBD`, `post_id: TBD`,
  `slug: TBD`, plus `title:` = the exact YouTube title queued in Blotato, so the draft can be matched to its video.
- `gap.py`: lists every public video whose LIVE page has no article (`--json` for a routine). Exit 1 when a gap is
  older than 24 hours. A file here does not count as done; the live page does.
- `skips.json`: Shorts that get no article on purpose, `{"<youtube-id>": "reason"}`. `gap.py` and the server's
  early warning (`scripts/sixpackabs/article-gaps.js`) both read it.

## Rules

- **Source = the video's words.** Transcript from a local `.srt`/`.transcript.json` next to the final, or
  Gemini on the public YouTube URL: `python3 transcript.py <youtube-id>` (the YouTube OAuth token has no captions
  scope; a few cents per video). Never invent a claim the
  video does not make. If the video states something inaccurate, soften or drop it rather than repeat it.
- **Voice: Dan, first person**, plain and specific, talking to "you". Opening line = the strongest true claim or
  the answer, then the answer in two sentences. Never "Today we're talking about". Paragraphs end on the payoff.
  Read `.claude/skills/scriptfromoutline/SKILL.md` (WHAT DAN CHANGED) and memory `dan-personal-facts-for-scripts`.
- **Structure:** title stays the YouTube title (it is the H1). Answer up top, H2 sections that follow the video,
  a steps list where it fits, one CTA line, then the italic note.
- **Length:** long-form 800 to 1,500 words (a 20+ minute video may run a bit over). Short: 300 to 500 words,
  and only when it answers a searchable question. Skip brag/teaser Shorts and Shorts that would compete with a
  page on the same topic.
- **CTA:** exactly one, `[...]({CTA})` → `absbyai.com/start` with `utm_source=sixpackabs&utm_medium=blog&
  utm_campaign=video-article&utm_content=<video-id>`.
- **CTA wording (2026-10-10):** the link goes to the /start sales page, so the ask is the 7-day free trial
  ("try Abs By AI free for 7 days"), not a free AI image. Older articles keep the wording they have.
- **Links:** 1 to 3 internal links (`/videos/...` pages or old posts). `build.py` enforces this.
- **Excerpt = the meta description** (the theme feeds it to Yoast): under 155 characters, answers the question.
- **Compliance:** "This is general fitness information, not medical advice." on every article; add "Some images in
  the video are AI-generated visualizations, and they're labeled." when the video shows AI imagery. No
  unbelievable claims. Never call Dan a marketer or ad agency owner. Never "my wife" (girlfriend). Swears aim
  at advice, never at people. No slurs or shock comparisons even if said on camera.
- **No names of the old company's owners, partners or staff (e.g. Mike Chang) and nothing about the 2019 sale**,
  even when the video says it: the sale agreement has an open-ended clause on naming them in apps and
  presentations, and a confidentiality covenant on the transaction (the background is in a private memory entry that is not in the repo; this bullet is the whole rule). "One of the
  original founders of Six Pack Shortcuts and SixPackAbs.com" is fine.
- **No em dashes and no en dashes.** `build.py` refuses a file containing either.
- Ads are never organic: only public content videos get articles (the feed already excludes unlisted ads).

## Publishing

WordPress.com MCP, site `253647467`: `content-items.update` with `post_type: spa_video`, `id: <post_id>`,
`excerpt`, `content` (the `build.py` output), `user_confirmed: true`. Then verify the live page: the article is
in `.spa-notes`, `<meta name="description">` equals the excerpt, no em dash inside the notes. Updates purge the
edge cache for that page; no manual cache clear is needed.

## Every new video gets its article automatically (2026-10-10)

Nobody has to remember to publish. Three layers, cheapest first:

1. **Early warning (free, minutes):** after each five-minute feed refresh the server logs one line per public video
   with no article file: `railway logs --service abs-by-ai | grep "article gap"`.
2. **The daily routine (does the work):** Claude scheduled task `sixpackabs-article-gap-daily`, 10:30 AM Central.
   It runs `gap.py` and stops in one line when there is no gap. Otherwise, per gap:
   - `publish`: the file exists, so build, publish, verify.
   - `write` (long-form): use the `TBD-*.md` draft whose `title:` matches (the filename match `gap.py` prints is only
     a hint: read the draft against the video's description before using it). Set `id`, `post_id`, `slug` from the
     `gap.py --json` row, `git mv` it to `<id>.md`, replace any `/videos/TBD-...` placeholder link with a real slug,
     then build, publish, verify. No draft: transcribe and write it per the rules above.
   - `needs judgment` (Short): write 300 to 500 words through `dan-voice-writer`, or add the id to `skips.json` with
     a one-line reason. Either one closes the gap.
   - `hand-edited`: someone changed the notes by hand. Do not overwrite; report it.
   - `no page yet`: normal for 15 minutes after release. Older than an hour means the sync is failing: report it.
3. **The check on the system:** the morning brief reads `article_gaps` (from `gap.py`) and reports the count. A gap
   older than 24 hours means layer 2 failed, and the brief says so.

Dan authorized publishing these articles without his review on 2026-10-10. Receipt and owner:
`Docs/SIXPACKABS_ARTICLE_AUTOMATION_RECEIPT_20261010.md`.

## Shorts skipped on purpose (no article; the page keeps its YouTube description)

The list lives in `skips.json` with a one-line reason each (same topic as a page that already has an article, or a
brag or teaser with no searchable question). `gap.py` does not count them as missing. To skip a Short, add it there.
