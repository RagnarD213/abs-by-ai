# Pinned question comment on every YouTube video

Dan, 2026-10-11: every published video on the channel (Dan Rose Fitness, @danrosefit), long-form and Short, carries one
comment from the channel, pinned, that asks the viewer an easy question. The goal is replies. All 41 public videos got
theirs on 2026-10-11. Ads (unlisted uploads) get none.

## What exists

| piece | where |
|---|---|
| The record of what is pinned | `scripts/youtube/pinned_comments.json` (video id, title, comment, date) |
| The gap check | `node scripts/youtube/pinned_comment_gap.js` (`--json`; `--mark <id> "<text>"` records one) |
| The question for a video not released yet | `"pinned_comment"` in its `scripts/blotato/configs/<slug>.json`, written at setup |
| The browser steps | `scripts/youtube/pinned_comment_helper.js` |
| The daily job | Claude routine `youtube-pinned-comment-daily`, 9:40 AM Central |

## Why it cannot happen before release

Blotato creates the YouTube video at release time, so there is no video to comment on before then. The YouTube API has
no way to pin a comment at all, and our token cannot post one. So the question is written at setup and saved in the
config, and the daily routine posts and pins it in Chrome once the video is public. The gap check matches a public video
to its config by the exact YouTube title.

## Writing the question

- One question about that video's own topic, answerable in a few words: a number, a pick between two things, or yes/no
  plus one detail. "What weight kettlebell do you have at home right now?" not "What did you think?".
- 1 or 2 short sentences, under 180 characters, ends in a question mark.
- Dan's voice, written by the `dan-voice-writer` agent from a one-line content plan (what the comment asks).
- No link, no hashtag, no emoji, no "let me know in the comments". No em or en dash. No invented fact about Dan.
- A link comment (`utm_medium=comment`) is no longer the pinned comment. The description carries the link.

## Posting and pinning (Chrome, signed in as the channel)

Use the Chrome extension tools (`mcp__claude-in-chrome__*`), not the built-in browser: only Chrome is signed in to the
channel. Per video, in one `browser_batch` (three videos per batch at most, a longer batch times out):

1. `navigate` to `https://www.youtube.com/watch?v=<id>` (a Short opens as a normal watch page this way), `wait` 7 s.
2. `computer` `scroll` down 10 ticks at (500, 500). A real mouse scroll is required: the comments only load after one.
3. `javascript_exec`: the full text of `scripts/youtube/pinned_comment_helper.js`, then `await H.a("<comment>")`.
   It returns `ready`. It throws `already pinned` or `already posted` when the work is done (record it and move on),
   and a timeout when the comment box never loaded (scroll again and repeat this step).
4. `computer` `type` the comment text.
5. `H.b1()`, `await H.b2()`, `await H.b3()`, `await H.b4()`, `await H.b5()`, each its own `javascript_exec`, with a
   `screenshot` at `scale: 0.1` between them. `b5` returns `?v=<id> PINNED`.
6. `node scripts/youtube/pinned_comment_gap.js --mark <id> "<comment>"`.

Traps found on 2026-10-11:
- The tab runs in the background. Scrolling by JavaScript does not load the comments, and the menu and the confirm
  dialog do not open unless a frame is drawn, which is what the small screenshots are for. Doing post, menu, pin and
  confirm in one script posted the comment but left it unpinned.
- A scroll sent before the page settles is lost (the page jumps back to the top). Wait first; on a timeout, scroll again.
- The helper text is about 2 KB. To avoid resending it per video, save it once with
  `localStorage.setItem('__pc_helper', <text>)`, run `(0,eval)(localStorage.__pc_helper)` on each page, and remove the
  key at the end.
- A comment is pinned only when the thread shows "Pinned by @danrosefit". Never report it from the click alone.
- Pinning a new comment replaces the old pin. Never pin over a comment Dan pinned himself: `H.a` refuses when a pin exists.
