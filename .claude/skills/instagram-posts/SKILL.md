---
name: instagram-posts
description: Make @danrosefit Instagram/Facebook image posts (carousels and single cheat sheets) in Dan's approved template - The Fix, Receipts, Steal My Workout, cheat sheet - from a JSON content file and one render command, then queue picks in the Mon/Wed/Fri 5 PM image slots. Use whenever Dan asks for Instagram posts, carousels, image posts, photo posts, cheat sheets, "more like C1/C2/C3", or to queue image posts, even if he doesn't say "/instagram-posts". Reels and Shorts are /shorts; video covers are /coverimage.
---

# Instagram posts (@danrosefit image posts)

Every post is a content JSON file plus one command:

```bash
python3 .claude/skills/instagram-posts/reference/render.py .claude/skills/instagram-posts/reference/content/<id>.json [more.json ...] --sheet <name>
```

Output (git-ignored, it holds shirtless photos): `Short-form video content/instagram-danrosefit/posts/<id>/<id>-01.jpg ...`,
`contact.jpg` (the post at phone-feed size, 270 px a slide) and `qa.json`. Exit code 1 = a QA problem; fix it before
anyone sees the post. Queue picks with `scripts/blotato/igtemplate_queue.py` (add them to `igtemplate_batch.json`).

## Dan's picks (2026-10-21)

- **Approved formats:** The Fix (C1), Receipts (C2), Steal My Workout (C3), and the cheat-sheet single (P2) with a small
  real photo of Dan. Reference files: `reference/content/fix-01-jump-rope.json`, `receipts-01-crunches.json`,
  `workout-01-home-abs.json`. Source mockups: `Short-form video content/instagram-danrosefit/template-r1-mockups/`.
- **Rejected:** Swaps (too boring), Timeline (too much about Dan, no reason for the viewer to care), and the singles
  Proof, Straight Talk, The Math, Routine. **Lesson: every post gives the viewer something to use. Dan's own story
  appears only where it proves the viewer's takeaway.**
- The old green Codex "studio" posts and the pool-photo posts are retired. Never make posts like them.

## The look (locked)

Ink `#0E1013`, bone `#F2EEE6`, red `#D33A2C` (mistakes, "old", the series square), yellow `#FFD23F` (fixes,
highlights, last-slide asks). Anton headlines, Manrope everything else. 1080 x 1350 JPEG. Series tag top left, page
count, @danrosefit on every slide. Posted sizes: headlines 70 px and up, body 36 px and up, nothing under 32 px; no text
in the outer 34 px (the profile grid crops to 3:4). `render.py` checks all of this and auto-shrinks text to fit.

**Labels:** a real photo of Dan carries "Real photo of me, not AI-generated" (off face and abs); an AI image carries
"AI-generated image"; a phone screenshot "Real screenshot". Slide 1 is exempt. The template places the label from the
image's `label` field (`real`, `ai`, `screenshot`, `none`); QA fails a slide whose image has no label.

**Last slide asks for one thing:** save, send, comment on a specific question, or follow.

## Content rules

- **Facts only from Dan** (memory `dan-personal-facts-for-scripts`, his own scripts and transcripts) **or from a source
  named on the slide.** Never invent a number. A study is checked before use: authors, journal, year, what was
  measured, and the result stated the way the paper states it.
- **The Fix:** the mistake and the fix are both real footage of Dan. Never fake a mistake: no AI image of Dan, no stick
  figure, no other person. No footage yet = an image placeholder (`{"placeholder": "exact shot to film"}`) plus a line on
  the shoot list. Clip library first: `python3 .claude/skills/_shared/cliplib/clip_library.py find "..."`.
  B0430 is the only mistake demo filmed so far (jump rope, MISTAKE DEMO ONLY).
- **Receipts:** one popular belief per post, one real study; verdict slide; "what actually works"; Dan's photo or fact
  only where it proves the point.
- **Steal My Workout:** only routines Dan really does: his 10 weekly gym exercises, his 3-exercise ab workout (spiderman
  planks and V-sit twists are in it), his Gymboss timer home workouts, his gym rep scheme (one warm-up set of 12 to 15,
  then two working sets of 6 to 10). Gym moves have no footage yet: placeholders plus the shoot list.
- **Images:** real footage and photos first (stills from library clips with `Media/video_edit/bin/ffmpeg`). Codex
  (`.claude/skills/_shared/codex-image.sh`) for objects and food only, labelled AI. State the Codex count before
  generating. Put each post's images in `Short-form video content/instagram-danrosefit/assets/<id>/`.
- Copy in Dan's voice (the `dan-voice-writer` agent for captions). No long dashes anywhere (QA checks the slides).
- Captions: first line repeats the hook plus one fact from the post; the ask matches the last slide; at most 5 hashtags.

## Content file schema

Common: `format`, `id` (`fix-02-...`, `receipts-02-...`, `workout-02-...`), `tag` ("The Fix · 02", "Receipts · 02",
"Steal my workout"), optional `avatar`. Text fields accept `[y]yellow[/y]`, `[r]red[/r]`, `[hl]highlighter[/hl]`,
`[em]yellow bold[/em]`, and `\n` for a line break. An image is
`{"src": "path from project root", "pos": "50% 40%", "zoom": 1.0, "label": "real", "alt": "..."}` or
`{"placeholder": "Side-on: Dan rounding his back on the kettlebell deadlift, bell at shins"}`.
Optional `size` on a headline sets its starting font size (it still auto-shrinks to fit).

- **the-fix:** `cover {headline, image, ring?[x,y,w,h], callout?, callout_at?[x,y], swipe?}`,
  `mistake {image, headline, body, pill?}`, `fix {image, headline, body, pill?}`,
  `cues {image, title?, subtitle?, items[3]}`, `cta {blocks[{icon: save|send|comment|shot, title, text}], follow?}`.
  Ring/callout coordinates are css px inside the 540 x 479 cover image box.
- **receipts:** `cover {headline, sub, polaroid {image, caption}, swipe?}`,
  `study {stamp?, headline, stats[{n, label}]?, rows[{label, result, tone: good|bad|neutral}], note?, source}`,
  `exhibit_b {stamp, image, caption, headline}`, `verdict {stamp?, headline, body, image (a cutout, height?)}`,
  `works {stamp?, items[3], side? {image, caption?}, headline, save}`.
- **steal-my-workout:** `cover {headline, cutout {src | placeholder, height?, right?}, swipe?}`,
  `moves[2..4] {name, dose ("1:00", "3 x 6-10"), dose_icon? (clock|none), image, cues[3], thumb_pos?}`,
  `recap {title?, note?, text, follow?, label?}`.
- **cheat-sheet:** see `reference/content/cheat-01-protein-per-100-calories.json`.

## Before Dan sees a batch

Render every post, read `qa.json`, look at each `contact.jpg` at phone size, rank the posts in each format and fix the
weak ones first (memory `self-bakeoff-before-dan-reviews`). Show Dan a plain image review page (one swipeable row per
post), never a Design canvas (it rendered black in his side panel on 2026-10-21).
