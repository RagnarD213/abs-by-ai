# Handoff: make every new video get its sixpackabs.com article automatically

Written 2026-10-10. Category: CONTENT infrastructure. Model: Opus 5.5 high for the design and skill edits; the recurring routine itself is ops, so it belongs to Codex Sol (model-routing rule). Run after, or alongside, `handoff-20261010-sixpackabs-article-backlog.md`.

## The problem

By 2026-10-10, 14 public videos had pages showing only the YouTube description. The process exists: `video-setup` Step 6b says write the article during setup and publish it once the video is public. It failed because publishing is a later step in a different session, depends on someone remembering a one-line coordination note, and nothing checks the result. Two cases slip through: Shorts and videos queued through paths other than `/video-setup`, and videos whose setup session ended before release day.

## Goal

A public video can never sit without an article for more than about a day, with no human reminder.

## Build this

1. **Gap detector (script).** `sixpackabs/articles/gap.py`: reads `https://absbyai.com/api/sixpackabs/channel.json`, compares ids to `sixpackabs/articles/<id>.md`, and also checks the live page body (a page whose `.spa-notes` still equals the YouTube description counts as a gap, even if a file exists, because the file may never have been published). Prints the gap list, marks Shorts that are probably skips (brag or teaser, or overlap with an existing topic) as "needs judgment". Exit code 1 if any gap is older than 24 hours.
2. **Daily routine.** A Codex Sol dot or scheduled task, daily, that runs `gap.py`. For each gap it runs the article flow in `sixpackabs/articles/README.md` (transcript, `dan-voice-writer`, `build.py --check`, publish, `verify.py`). Ops with writing inside it: keep Opus for the writing call if the routine can delegate to it; if not, the routine only files a gap report and the next Opus session clears it. State which in the receipt. One reasonable variant: the routine writes nothing and instead adds a single board line "N videos need articles" plus a ready starter prompt, so Opus does the writing. Pick the cheaper working option and record why.
3. **Move the trigger to the event.** In the Railway feed sync (or `spa_sync` report), log when a new public video appears with no article file, so the gap is visible within minutes, not at the next daily run.
4. **Fix the skill.** `.claude/skills/video-setup/SKILL.md` Step 6b: the article is written and committed in the setup session, publishing is attached to the release check, and the setup is not "done" until the article row exists in the receipt. Add the same one-liner to `shorts` and `youtube-packaging` if they can end a video's setup. Shared file: `safe-push.sh` it the moment you edit it.
5. **Close the loop.** The morning brief (or `Docs/BOARD_MORNING_MAINTENANCE.md` checklist) gets one line: run `gap.py`, report count. A nonzero count older than 24 hours is a failure of this system, reported.
6. **Test it.** Run `gap.py` today and confirm it lists exactly what the backlog handoff lists (14 plus any new). Then, after the backlog handoff finishes, confirm it returns zero.

## Rules that carry over

All writing rules in `sixpackabs/articles/README.md` and `.claude/skills/_shared/WRITING-RULES.md`. Ads never get articles. No em or en dashes. Never delete a post or page. Dan authorized unreviewed article publishing on 2026-10-10 for this system.

## Done means

`gap.py` committed and returning the right list; the routine exists and has run once; video-setup (and any other skill that ends a video's setup) updated and pushed; the morning-brief line added; a receipt in `Docs/` saying who owns the routine. Report in chat; no standing board entry beyond one line if something stays open.

## Starter prompt (paste into a fresh task; name it `Sixpackabs Article Automation`)

```
Read Handoffs/handoff-20261010-sixpackabs-article-every-new-video.md and execute it: build the gap detector, the daily routine, the video-setup skill fix and the morning-brief check so every public video gets its sixpackabs.com article within about a day. Run gap.py first and confirm it matches the backlog handoff. Push shared files with safe-push.sh as you edit them.
```

Recommended: Opus 5.5, high effort (Codex Sol high for the recurring routine itself).
