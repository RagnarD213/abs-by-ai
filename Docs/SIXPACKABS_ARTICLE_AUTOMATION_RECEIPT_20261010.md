# Receipt: every new video gets its sixpackabs.com article automatically

Built 2026-10-10 by Claude (Opus 5.5) from `Handoffs/handoff-20261010-sixpackabs-article-every-new-video.md`.
Category: CONTENT infrastructure. Rules for the articles themselves: `sixpackabs/articles/README.md`.

## Who owns what

| Piece | Where | Owner |
| --- | --- | --- |
| Gap detector | `sixpackabs/articles/gap.py` (no AI, no login) | repo |
| Skip list | `sixpackabs/articles/skips.json` | whoever skips a Short adds the line |
| Transcript helper | `sixpackabs/articles/transcript.py <id>` (Gemini on the public URL, a few cents) | repo |
| Daily routine | Claude scheduled task `sixpackabs-article-gap-daily`, 10:30 AM Central (fires about 10:40) | **Claude** |
| Early warning | `scripts/sixpackabs/article-gaps.js`, called from `server.js` after each five-minute feed refresh | server |
| Check on the routine | morning brief input `sources.article_gaps` (`scripts/brief/collect_inputs.py`), `Docs/BOARD_MORNING_MAINTENANCE.md` step 8, `Docs/ROUTINES.md` | Codex brief |
| Setup rule | `/video-setup` Step 6b, plus one section each in `/shorts` and `/youtube-packaging` | skills |

## Why the routine is on Claude and not Codex

The handoff said to pick the cheaper option that works and record why.

- The goal is "no human reminder". A routine that only files a report or a board line still needs Dan to fire a
  writing session, so it does not meet the goal. The routine has to write and publish.
- The writing is Dan's voice: Opus 5.5 through the `dan-voice-writer` agent, and publishing goes through the
  WordPress.com connector. Both live on the Claude side. A Codex routine would have to hand the work back to Claude
  anyway, which is two sessions instead of one.
- Cost is kept low by putting a free script in front: the routine's first step is `gap.py`. With no gap it answers in
  one line and stops. It only spends writing tokens on days a video actually went public (about four days a week:
  the Sunday long-form, whose draft is already written at setup, and the Tuesday, Thursday and Saturday Shorts).
- Codex keeps the part that is pure ops: the morning brief reads the count and reports a failure.

## What was tested

- `gap.py` on the live site, 2026-10-10 4:02 PM Central: 39 public videos, 35 with an article, 4 skipped on purpose,
  0 gaps. The backlog handoff had finished earlier the same day (10 articles live, 4 Shorts skipped).
- Replay of the morning's state (the 14 backlog pages put back to their YouTube description, no files, no skips):
  `gap.py` listed exactly the 14 videos in `handoff-20261010-sixpackabs-article-backlog.md` and exited 1.
- `node scripts/sixpackabs/article-gaps.test.js` and `node scripts/sixpackabs/feed.test.js` pass;
  `scripts/brief/tests/test_inputs.py` passes (29 tests).
- `transcript.py PjHNyR9QJMo` returned the full spoken text of the bicep curl Short.
- First routine run: see "First run" below.

## Known limits

- The routine runs only while the Mac and the Claude app are open. A missed run fires at the next launch.
- The first run that has a real gap may stop on a permission prompt for the WordPress.com connector. Approve it once
  with "always allow" and later runs go through.
- The 11 `TBD-*.md` drafts written before this date have no `title:` line, so the routine matches them by reading the
  draft against the video. New drafts carry `title:` (video-setup Step 6b).
- The server warning is file-based (is there a `<id>.md`?). `gap.py` checks the live page and is the authority.
- A Codex release-check automation may also publish a long-form's article (Keep Your Muscle, December 6). Whichever
  runs first publishes; the other finds nothing to do.

## First run

Run by hand ("Run now") on 2026-10-10 at 4:07 PM Central, session `local_034311b8-a1a5-45f9-a98d-d042d85c6aa4`:
one script call, then the answer "sixpackabs articles: 0 gaps (35 with an article, 4 skipped on purpose)", finished in
7 seconds. The first run with real work is expected Sunday 2026-10-11, after Stop Deadlifting goes public at 9 AM
(draft `sixpackabs/articles/TBD-stop-deadlifting.md`).
