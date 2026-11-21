# Handoff: write and install the missing sixpackabs.com video articles (backlog)

Written 2026-10-10. Category: CONTENT (website articles, no video editing). Model: Opus 5.5, high effort.

## Goal

Every public YouTube video has a page at `sixpackabs.com/videos/<slug>/` whose body should be a real article in Dan's
voice, not the YouTube description. 14 public videos have no article. Write all 14, install them, verify them live.
Dan authorized this without his review (2026-10-10): write, publish, verify, then report. Do not stop to ask.

## Read first

1. `sixpackabs/articles/README.md` (the rules, build.py, publishing steps). It wins over this doc.
2. `.claude/skills/_shared/WRITING-RULES.md` and the memory entries it lists (`Docs/memory/`).
3. One finished article as the bar, e.g. `sixpackabs/articles/le2OyN3biW4.md` (short) and a long-form one such as `bkzT-3ENpoU.md`.
4. `.claude/skills/scriptfromoutline/SKILL.md` section WHAT DAN CHANGED, memory `dan-personal-facts-for-scripts`, `no-fat-pinch-belly-focus`.
5. Voice: draft every article through the `dan-voice-writer` agent (clean call, finished content plan in, draft out). Decide what each piece says yourself, then hand it the plan.

## The backlog (computed 2026-10-10 by diffing `https://absbyai.com/api/sixpackabs/channel.json` against `sixpackabs/articles/*.md`)

Long-form (800 to 1,500 words; a 20+ min video may run over):
- `v2R4QpnURqA` Your Belly Fat Is an Emergency: 7 Reasons to Take It Seriously (11:20, Oct 4). Page slug ends `-2`: confirm the right page and that no duplicate older page exists; if one does, report it, do not delete it. Chapters and a 5-move plan are in its description. Mention Zepbound and testosterone only as "talk to your doctor". Never pinch or zoom on belly fat in any image idea.
- `ZxsFnsv7mLo` Home Arm Workout: Shoulders, Biceps & Triceps With Just Dumbbells (Do It With Me) (11:01, Sep 27). Follow-along workout: write it as the exercise list with sets and reps taken from the video.

Shorts (300 to 500 words, only if the Short answers a searchable question; skip brag or teaser Shorts, and skip any Short that would compete with an existing page on the same topic):
- `PjHNyR9QJMo` How To Do Bicep Curls: One Arm or Both Arms?
- `D9v9POAKe_Q` The Deadlift Trick That Saves Your Back (check overlap with `TBD-stop-deadlifting.md`)
- `qBXYI96DSXE` Make Your Waist Look Smaller With Side Lateral Raises
- `bi_fpkW-3eE` Try To Knee Yourself In The Face (likely skip as a teaser; decide from the transcript)
- `qDvrtKbuhf4` Do This 2 Minute Arm Pump Before You Take Your Shirt Off
- `R2yNA2ZnsSU` How to Do Kettlebell Deadlifts the Right Way at Home
- `QuswpGj635A` Why Bodybuilders Suck Their Stomach In (overlaps the stomach vacuum article `le2OyN3biW4`: link to it, keep distinct)
- `o1v3wPkNI2I` 8 Hours In Bed Is Not 8 Hours Of Sleep
- `_Ep_hVPZYzE` Never Start Your Day With Carbs
- `tqURi3qdrIc` Weigh Yourself Every Single Day. Here's Why.
- `1AnxJ5JCLa0` Do This Instead Of Crunches
- `I_trw1PaMhc` The Full 1 Minute Ab Workout - Follow Along (follow-along; short article listing the moves)

Also reconcile the 11 `TBD-*.md` drafts in `sixpackabs/articles/`. Each belongs to a video that is either not public yet (leave it alone, its video-setup session publishes it) or already public under a different title. For any already public, set `id`, `post_id`, `slug`, publish it, rename the file to `<id>.md`. Re-run the diff first; the feed changes hourly, so regenerate the list rather than trusting this one.

## Steps per video

1. Get the words: local `.srt`/`.transcript.json` next to the final if present, otherwise Gemini on the public YouTube URL (`https://www.youtube.com/watch?v=<id>`). Gemini review of project media is pre-authorized under the $5 cap; this will be far under it.
2. Write the content plan, run it through `dan-voice-writer`, save `sixpackabs/articles/<id>.md` (front matter `id`, `post_id`, `slug`, `excerpt` under 155 characters).
3. Find `post_id` and `slug` through the WordPress.com MCP (site `253647467`, `post_type: spa_video`).
4. `python3 sixpackabs/articles/build.py --check <file>` must pass (no em or en dashes, one CTA with the UTM, 1 to 3 internal links, word range).
5. Publish with `content-items.update` (`post_type: spa_video`, `id`, `excerpt`, `content` = build.py output, `user_confirmed: true`).
6. `python3 sixpackabs/articles/verify.py <file>` must print OK. Spot-check three pages in the browser: article inside `.spa-notes`, meta description equals the excerpt, no dash characters, mobile reads cleanly.

## Hard rules

- Only the video's own claims. Soften or drop anything inaccurate. AI-generated imagery in the video gets the "labeled" line; every article gets "This is general fitness information, not medical advice."
- Never name the old company's owners or mention the 2019 sale. Refer to Dan's girlfriend as his girlfriend. Never call Dan a marketer or ad agency owner.
- No ad videos (the feed already excludes unlisted ads). No em dash, no en dash (grep the file for the em dash character, count must be 0).
- Do not delete posts or pages. Do not touch pages whose notes Dan edited by hand (the sync's hash check protects them; if an update fails for that reason, report it).
- Commit and push with `scripts/git/safe-push.sh -m "..." -- <your files>` and confirm the deploy as the AGENTS.md delivery rules require. The articles themselves are WordPress content, so the push is for the `.md` files.

## Done means

Every public video that deserves an article has one live and verified, every skipped Short has a one-line reason, the TBD drafts are reconciled, files are pushed. Report in chat: a table of id, title, words, live URL, or skip reason. Delete any board entry you add. Do not wait for Dan's review.

## Starter prompt (paste into a fresh task; name it `Sixpackabs Articles Backlog`)

```
Read Handoffs/handoff-20261010-sixpackabs-article-backlog.md and execute it end to end: write, install and live-verify the missing sixpackabs.com video articles with the dan-voice-writer agent. Dan pre-approved publishing without review. Regenerate the gap list from the live feed first. Report a table when done.
```

Recommended: Opus 5.5, high effort.
