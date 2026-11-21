# RO-12 "Top 5 Zepbound Tips": YouTube thumbnail options (Codex half)

**Written 2026-10-01 by Claude (Opus 5.5) for Codex.** Standing split for every organic content video (Dan, 2026-09-30):
**Codex makes the thumbnail, Claude uploads and sets up.** This task is the thumbnail only. Do not upload, schedule, post or touch
YouTube, Blotato or any social account. Dan hands the finalized thumbnail to the Claude setup task
(`Handoffs/handoff-20261001-ro12-video-setup.md`) himself. Name this session `Top 5 Zepbound Tips LFC thumbnails`.

## 1. The video
- Finalized by Dan 2026-10-01 ("I think this video looks good... Go ahead and finalize this"). Organic content video, 9:11.
- Master: `claude edited long form content/09 - Top 5 Zepbound Tips/Top 5 Zepbound Tips | claude | 16x9 | RO-12.mp4`
  (sha256 `7f6766c5e1d82881...`). Chapters: `Top 5 Zepbound Tips - chapters.txt` in the same folder.
- What it is: Dan's five tips for getting the most out of a GLP-1 (he names Zepbound throughout): 1 use needles and vials, not
  pens; 2 how to actually inject (outer front thigh); 3 inject on Thursday evening so it peaks on the weekend; 4 ramp on slowly,
  taper off even slower; 5 focus on protein so you keep your muscle. He shows his real before and now photos at 0:11 to 0:20.
- In the footage he wears a black tank top against a green wall, so **no talking frame shows his abs**. Useful frames for the
  screenshot slot: Dan to camera 0:00 to 0:10 and 8:45 to 9:05 (tight framing), the real NOW photo card at 0:18.

## 2. Rules (read these files first)
- `.claude/skills/_shared/VIDEO-RULES.md`, "Five cover and thumbnail choices per video" (Dan, 2026-09-30). The five slots, one
  different image or design each, same headline on all five:
  1. One pool-shoot photo.
  2. A real studio photo composited into a bold, topic-specific photographic environment in the Jelly Beans cover family (crisp
     white cutout outline, large subject-related props, heavy type, one accent colour).
  3. A second, different studio photo in a second, different Jelly Beans style environment.
  4. One authentic screenshot from the approved master, enhanced for clarity while preserving Dan's identity and physique.
  5. One designer's choice: the image and design that best sells this topic.
  Reference: `Short-form video content/covers/review/jelly-bean-refresh/B3-jelly-beans-beat-soda-tight.png`.
- `.claude/skills/video-setup/SKILL.md` Step 2 and `.claude/skills/youtube-packaging/SKILL.md` (type system, frowning-photos
  rule, waistline crop on Speedo photos, text never on Dan's face, hair or abs).
- Topic props for the Jelly Beans slots (your call): a syringe and vial, a weekly calendar with Thursday circled, a plate of
  protein. Keep needles tasteful: capped or resting, never in skin.
- Headline direction (keep it short, two lines beat three, no result numbers): e.g. `5 ZEPBOUND TIPS` or `ZEPBOUND: 5 TIPS`.
  Dan ruled 2026-09-30 that organic videos may name the drug in speech and subtitles; brand names in on-screen graphics are not
  ruled yet, so make the review sheet with the drug name and add ONE alternate of your strongest option reading `5 GLP-1 TIPS`
  so Dan can choose.
- Never the bathroom standing before photo; never a frowning photo; rotate photos away from the last few long-form thumbnails
  (`social media graphics/youtube/thumbnails/`).
- Cost: AI generation up to $5 for this task is authorized; over that needs Dan first.

## 3. Deliver
1. Build in `social media graphics/youtube/thumbnails/Top 5 Zepbound Tips/_build-2026-10-01/` (recipe + outputs).
2. QC each on the rendered file: text clear of his face, hair and abs, nothing clipped, legible at feed size (320 px wide).
3. One review sheet `REVIEW_ro12_thumbnails.jpg` with the five labelled 1 to 5 (plus the GLP-1 alternate); send it to Dan and
   stop for his pick (he may pick two for an A/B test).
4. After the pick: export `Top 5 Zepbound Tips - thumbnail FINAL.jpg` (and `... FINAL B.jpg` if he picks two) in
   `social media graphics/youtube/thumbnails/Top 5 Zepbound Tips/`: 1280x720, JPEG, under 2 MB. Give Dan the exact path(s); he
   pastes them into the Claude setup task.
5. Update `Handoffs/README.md` (this row: executed, with the final path) and your board entry; commit only your files. The shared
   checkout has other sessions' uncommitted work: never `git stash -u`.

## 4. Model and starter prompt
Codex (GPT-6 Astra), effort medium.

> Read `Handoffs/handoff-20261001-ro12-thumbnails-codex.md` in full and do only what it asks: build five YouTube thumbnail options for RO-12 "Top 5 Zepbound Tips", send me the review sheet and stop for my pick, then export the final 1280x720 JPEG and give me its path. Do not upload or schedule anything. Name this session "Top 5 Zepbound Tips LFC thumbnails".
