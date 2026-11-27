CONTENT · long-form (LFC) · RO-15 · Gemini audition, practice setup graded against the real one

# Gemini Setup Test 2 (practice run): Sleep Better With Glycine (RO-15)

**OPEN. Written by Claude 2026-11-27 for Gemini. Nothing live changes in this test.**

**Second run (Dan, Nov 27): redo in the Antigravity app to test the real process.** A first run through the Terminal command finished the same day with Gemini-only pictures. This run uses the real cover process (five Codex designs plus three Google options, blind) and a new folder and report name. Everything the first run produced is off limits (list below).

Dan is deciding whether Gemini takes over video setup from Codex. This is audition 2 of 2.

Why a practice run: on Nov 27 only one approved video with no setup had its files on this Mac (the Blended Oats Short, test 1). Great Again T Upsell 1 (WV-04) is a checkout funnel job, not a video setup, and Got Abs? You Need To See This. (RO-28) is already scheduled. So test 2 rebuilds the setup package for a long-form that is already set up and waiting for Dec 23, **without looking at the existing package**, and is then graded against what Dan actually approved. It tests the long-form shape test 1 does not: 16:9 thumbnails, a YouTube description with chapters, tags and the site article.

## Where to run it

The Antigravity app on the M6, with the project folder open as the workspace, model Gemini 4 Neon, High. Not Gemini Desktop Task Mode. The app window itself is not yet verified (the Terminal command was), so report any permission or path wall as a scorecard item. Same reasons and the same travel traps as test 1 (`handoff-20261127-gemini-setup-test-1-ds38-blended-oats.md`, sections "Where to run it" and "Travel traps"): Seagate and M2 offline, broken `Short-form video content` link, `ffprobe` at `Media/video_edit/bin/ffprobe`, write to absolute paths, little free disk.

It can run at the same time as test 1. The two tests share no files.

## Verified inputs (checked by Claude on the M6, 2026-11-27)

| | |
|---|---|
| Approved master | `/Volumes/Extreme/Claude Content Videos/Sleep Better With Glycine - RO-15/FINAL - Sleep Better With Glycine.mp4` |
| | 1,784,296,329 bytes, 5:23.99, 1920x1080, 30000/1001 fps, H.264 + AAC |
| | SHA-256 `46dfc4240eeb08cb5a1e4c3e0d20680d1d0d03813fb1402a599d3e7aa13e290e` |
| Captions file | same folder, `FINAL - Sleep Better With Glycine.srt`, 9,423 bytes, SHA-256 `99969ede25f8488f9e64708ee52a0fe6320de155a41b253f65ee72f6d67dc19c` |

Read only. Never copy the 1.7 GB master; grab frames from it in place.

## Blind rule (the test is void if broken)

Until your package is finished, hashed and listed in `PACKAGE-MANIFEST.json`, do not open, list, search or read any of these:

- `scripts/blotato/configs/ro15-glycine.json`
- `Docs/RO15_SETUP_RECEIPT_20261106.md`, `Docs/RO15_SETUP_RECHECK_20261114.md`
- `social media graphics/youtube/thumbnails/Sleep Better With Glycine/`
- In the master's folder: `Sleep Better With Glycine - thumbnail FINAL.jpg` and `chapters.txt`
- Everything from the first run: `/Volumes/Extreme/_edit_work/GEMINI-SETUP-TEST-2/`, `Docs/GEMINI_SETUP_TEST_2_RO15_20261127.md` (and its git history), the review page on port 9640 and `~/Library/Application Support/AbsByAI Reviews/9640/`, `tmp/gemini-setup-tests/`, and any earlier Antigravity or `agy` conversation about this video
- Any `sixpackabs/articles/` file about glycine, and the glycine lines in `BLOTATO_QUEUE_PROGRESS.md`, `AI_COORDINATION.md`, `Docs/LONGFORM_RELEASE_CALENDAR.md` and `scripts/blotato/video_waitlist.json`

State in the report that you kept this rule, the way the Nov 24 chroma test did.

## Read first

`AGENTS.md` in full; `.claude/skills/_shared/VIDEO-RULES.md` ("Thumbnails: the five", publishing and AI-disclosure sections); `.claude/skills/video-setup/SKILL.md` Steps 2, 3, 5 and 6b and `Docs/PINNED_COMMENTS.md` as they are on disk today (uncommitted live edits; read, never edit or commit); `.claude/skills/youtube-packaging/SKILL.md`; `.claude/skills/coverimage/SKILL.md`; `.claude/skills/_shared/IMAGE-GENERATION.md`; `.claude/skills/_shared/WRITING-RULES.md`; `.claude/skills/_shared/DAN-VOICE.md`; `sixpackabs/articles/README.md` plus one finished article there that is not about glycine. Use other videos' receipts and thumbnails as the quality bar, never RO-15's.

You are the setup owner where a skill says "Codex owns setup". For the five Codex designs you call `.claude/skills/_shared/codex-image.sh` yourself, with the model and effort the image rules name.

## What to build, all inside `/Volumes/Extreme/_edit_work/GEMINI-SETUP-TEST-2B/`

1. `/usage` reading and start time saved first.
2. **Eight thumbnails, 1280x720 JPEG, each under 2 MB: five Codex designs plus three Google options of your own, all different.** The five Codex designs follow this mix: two different AI pictures of Dan acting out the topic (identity reference `social media graphics/youtube/thumbnails/I'm 41. Here Are The 10 Exercises I Do Every Week/_build-20261113/identity-reference.jpg`, inspect every face), one real photo of Dan with original person pixels from `photos/finalized social media photos/_cutouts/`, two guided by Dan's recent approved thumbnails for other videos. Headlines set in code, every word capitalized. Good sleep is shown as good sleep (memory `ai-clip-gags-injury-and-sense`). The five Codex designs come from `codex-image.sh` (state the count first, no spares); your three come from your built-in image generation and follow the same guidance without copying the five. Shuffle all eight with `.claude/skills/_shared/blind-image/blind.py` under labels X1 to X8, no source named anywhere Dan can see. Zero paid API. Record any refusal and make a different concept instead.
3. **Packaging from the real words in the captions file:** three title options with one recommended, the YouTube description with a UTM link and chapters timed from the SRT, tags, hashtags, `engagement_prompt` under 180 characters, the Facebook/Instagram/TikTok caption. Zero em dashes.
4. **The same packaging a second time, written by Claude Opus 5.5 inside your own subscription.** Run a sub-call such as `agy -p --model claude-opus-5-5-high` with the captions file and the two voice rule files, and save its title options, description and article draft beside yours, clearly named. Read `/usage` before and after this step alone, so Dan learns what the "Claude and GPT models" allowance inside Gemini costs per job. If the sub-call fails or is refused, record the exact error and carry on.
5. **Site article draft** to the `sixpackabs/articles/README.md` format, saved in the test folder only: one by you, one from the Opus sub-call.
6. **Draft config** `ro15-glycine.DRAFT.json` in the test folder (never in `scripts/blotato/configs/`), fields per the top of `scripts/blotato/longform_queue.py`. No uploads to Blotato in this test; use placeholder URLs and say so.
7. A phone-first review page via `.claude/skills/_shared/review_server.py` showing the eight thumbnails with blind labels X1 to X8 and both sets of copy labeled only "Set A" and "Set B" (keep which is Gemini and which is Opus in a separate key file, not on the page). Give Dan the `http://127.0.0.1:PORT/` link.
8. `PACKAGE-MANIFEST.json` with the SHA-256 of every file you made. **Only after this exists**, open the real RO-15 package and write the comparison.

## The comparison and the report

Write `Docs/GEMINI_SETUP_TEST_2B_RO15_ANTIGRAVITY_20261127.md`: a table of yours versus the approved package (title, description length and structure, each chapter time against the real `chapters.txt`, tags, thumbnail concept against the one Dan approved, schedule fields), what the real package had that yours missed, what yours had that it lacked, and the audition numbers: `/usage` before and after for Gemini models and for Claude models, pictures generated, refusals, wall-clock time, every time Dan had to step in. Do not reveal on the review page which thumbnail is closest to the approved one or which copy set is whose; Dan picks first, then reads the report. Push only that one Docs file with `scripts/git/safe-push.sh`. If it stops on other sessions' files, leave the commit local and say so.

## Stop lines

- Nothing live: no Blotato calls of any kind, no config in `scripts/blotato/configs/`, no waitlist or calendar edits, no site publishing, no YouTube.
- Do not touch `AI_COORDINATION.md`, `BLOTATO_QUEUE_PROGRESS.md`, `.claude/skills/video-setup/SKILL.md`, `Docs/PINNED_COMMENTS.md`, `Handoffs/README.md`, or any Joint Vigor file (client deadline Saturday 9 AM ET).
- Never modify, move or re-encode the RO-15 master or anything in its folder.
- `GEMINI_API_KEY`, `GOOGLE_API_KEY`, `ALLOW_API_IMAGE` stay unset.

## Scorecard (pass needs all five)

| # | Area | Pass |
|---|---|---|
| 1 | Copy and voice | Dan, picking blind between Set A and Set B, would ship one of them with at most light edits. Chapters within 2 seconds of the real ones. Zero em dashes, zero AI stock phrases. |
| 2 | Thumbnails | Five Codex designs plus three Google options, all clearly different, 1280x720 under 2 MB, blind; at least one that Dan rates as good as or better than the thumbnail he approved. |
| 3 | Technical accuracy | Draft config has every required field with correct types; comparison table is honest about misses. |
| 4 | Small Codex footprint | Codex used only for the five thumbnail pictures (count reported), no Claude Code, no paid API. Both `/usage` readings reported. |
| 5 | Ran on its own | Blind rule kept, one session, no rescue from Dan, no stop line crossed. |

## Starter prompt (paste into Antigravity, project folder open, Gemini 4 Neon High)

```text
Start Sleep Better With Glycine LFC Setup practice run (Gemini setup test 2, second run in Antigravity). Read and execute Handoffs/handoff-20261127-gemini-setup-test-2-ro15-glycine-shadow.md exactly, including the blind rule. Nothing live changes. Codex only for the five Codex thumbnail pictures through the image script, zero Claude Code, zero paid API. Work to the end without asking Dan anything, then give him the review page link and the report.
```
