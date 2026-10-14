# RO-08 "Intermittent Fasting: The Best Way To Get Abs": thumbnails, then upload and setup

**CONTENT, long-form (LFC).** It gets Shorts cut from it later (job SL-16) and nothing else: no vertical, square or 1-minute version.

**Written 2026-10-14 by Claude (Opus 5.5).** One Claude task does everything: five thumbnail choices (made by Codex in the command line),
stop for Dan's pick, then `/video-setup`. Dan approved the round 3 film on 2026-10-14 ("Okay, everything is looking good. I like how you
cleaned up those AI clips."). **Model:** Claude Opus 5.5, effort high (five unique thumbnail designs are design work per
`model-routing-plan`; the setup after his pick is checklist work in the same task).
**Sidebar name:** `Intermittent Fasting LFC Setup`. **Use the Codex subscription to generate the images.**

## 1. State

The round 3 film is delivered, gated, independently reviewed (fifth review: SHIP) and approved by Dan. Its review pages (ports 8869 to
8872) and the copy in `Videos to Review/` were removed on 10-14; the delivery folder is the record.
It is ORGANIC: it ends "if you wanna get started building six pack abs, go to AbsByAI.com... So check it out and generate an image of
your future self. Go to AbsByAI.com now. Thanks for watching this video and I'll see you guys next time." That is the soft content close,
the same kind as RO-19's, not a tap-the-button ad. Still run the skill's Step 0 classification, and
`python3 scripts/blotato/ad_guard.py --scan` before and after any Blotato write.
Edit Queue row RO-08 is `finalized` (Drive file and artifact mirror done, version 10). When the release is queued set it `uploaded`,
mirror with `ArtifactData` (artifact `https://claude.ai/artifact/1r1T8Znf96XH24zHZhybHs`, collection `jobs`, pin `if_version`), then
`python3 scripts/edit-queue/queue.py mark-synced RO-08`.

**Check first, before anything is queued:** look at the YouTube channel, the live Blotato queue and `BLOTATO_QUEUE_PROGRESS.md` for an
intermittent fasting video that is already public or queued. None is expected (this is a new video); if one is, stop and tell Dan in one line.

## 2. Files (all local)

Folder: `claude edited long form content/15 - Intermittent Fasting The Best Way To Get Abs/`
- Master: `Intermittent Fasting The Best Way To Get Abs | claude round 3 | 16x9 | RO-08.mp4`, 1.28 GB, 14:40.75, 1920x1080 29.97,
  h264 + AAC, sha256 `976b9761bc1e84553727aa599fe50e0befb7aa27e924220b4a14541bbba8867c`. Re-hash it first. The `claude round 2` files in
  the same folder are the superseded round; do not upload them.
- `... RO-08.srt` (275 cues, sidecar, never burned in) and `... RO-08.chapters.txt` (15 chapters, use as-is).
- Also there: `... REVIEW 540p.mp4`, the audio AB file, the edit sheet (approved), stamps (`.audio_gate.json`, `.deliver_gate.json`),
  `ROUND-3-REVIEW-1.md` to `-5.md`, `recipe-RO-08/` (with `dan-approval-20261014-verbatim.json`).
- Work folder (SSD): `/Volumes/Extreme/_edit_work/ro08/round3/`.

Facts for the packaging:
- **Realistic AI footage is in the film,** every clip with the AI-GENERATED chip: the workday time-lapse opener (0:00), a man knocked
  down by a boxing glove at his front door (3:23), a cartoon clean-up crew inside a cell (4:55), the donut and the food coma (6:07), a
  man whining at an empty breakfast plate (7:24), a beginner worn out on a gym floor (7:45), a midnight fridge raid (12:11), one sip of
  beer at a bar (13:35). So `ai_generated: true` in the Blotato config (TikTok) and the altered/synthetic flag on YouTube. The phone demo
  near 14:13 shows a labelled AI goal picture. Keep the one-line AI-image sentence in the description.
- **No links are promised on camera** other than AbsByAI.com. He says "GLP-1", "Zepbound" and "Ozempic" in passing (organic videos may
  name the drug). Do not invent a product link.
- What the video covers, for the description (the chapters file is the outline): why fasting is the best way he has found to get abs,
  what intermittent fasting is, the daily fast he does (black coffee, first meal a salad mid-afternoon), five reasons (the simplest way
  to eat less, what fasting does for your health, it saves your mornings, you get more done, your body adapts), how to start (just skip
  breakfast) and the first month, breaking the fast with a salad, and three mistakes (binge eating at night, eating right before bed,
  breaking the fast with alcohol).
- UTM link and call to action per `/video-setup` Step 3. Write the pinned question comment into the Blotato config as
  `"pinned_comment"` (`Docs/PINNED_COMMENTS.md`). He asks viewers on camera to "let me know in the comments how it goes for you", so an
  easy question fits, for example whether they skip breakfast now.
- **The stamps read FAIL and that is known.** Audio gate: the tone row only, with voice 1a, the voice Dan picked. Delivery gate 2.6.0:
  32 rows pass, 7 fail (audio:stamp, style:coverage 22 %, framing:hair_top, framing:headroom, cut:splice_visibility 20 of 149, a
  burned-captions false alarm on the lower thirds, a repeated-take false alarm at 10:51). Watch pass 494 of 494 images judged, 0 open
  defects. No bound was changed. Do not reopen any of them; he approved the film.

## 3. Thumbnails first: five choices, five unique designs, all made by Codex, then STOP

Rule: `.claude/skills/_shared/VIDEO-RULES.md`, first section (Dan, 2026-10-13). Read it, `/youtube-packaging` for the photo, crop and
text-clearance rules, and `_shared/IMAGE-GENERATION.md`.

1. **Pool shoot:** one real photo of Dan from `photos/pool shoot | 7-31-26 | dan | mindi/` (finalized picks and cutouts:
   `photos/finalized social media photos/`, `_cutouts/`). His real cutout over a Codex background; type set in code. Crop at the
   waistband (Speedo rule). Not a photo from `Frowning Photos/`.
2. **Studio shoot:** one real photo from `photos/studio shoot | 8-28-26 | dan | mindi/`, built the same way.
3. **An AI-enhanced or AI-generated image of Dan** that fits fasting: for example Dan with a black coffee and an empty plate, or at a
   desk with a wall clock at noon. Either enhance a real photo of him (give Codex the photo as the reference) or generate him. Prompt:
   "lean and shredded, not bulky, same size as the reference"; swim shorts or a tank top, not briefs. Look at the face before it goes on
   the sheet: it has to read as him.
4. and 5. **Two more AI-generated images of Codex's choice**, Dan or not. Ideas from the film, only as a starting point: a wall clock
   with the hours from 8 AM to 2 PM shaded as the fast; an empty breakfast plate beside a black coffee; a man asleep on his keyboard
   beside an empty donut box (the food coma); a salad as the first meal at 2 PM. Thumbnails carry no AI label, no "Real picture" label
   and no AbsByAI.com.

**Five unique designs.** Before building, write one line per option naming its layout, type treatment, colour and composition, and check
that no two share them. Same copy on all five unless Dan asks for alternatives; short and big (two lines beats three). The video's own
lines: "Intermittent Fasting", "The Best Way To Get Abs", "Skip Breakfast". No result claims. `.claude/skills/_shared/codex-image.sh
--model gpt-6.1-sol --effort high` for every generated image; no outside image model. QC on the RENDERED files: person-mask clearance of
every text block from his face and hair of at least 25 px, and look at the sheet yourself before sending it. Save the finals in
`social media graphics/youtube/thumbnails/Intermittent Fasting/`. Show all five on one review sheet (`SendUserFile`, display render),
list them in plain words with each one's design line, and **STOP for Dan's pick.** He may pick one, or two for an A/B test. Final file:
`<title> - thumbnail FINAL.jpg`, 1280x720 JPEG, under 2 MB.

## 4. Then `/video-setup`

Backups (Extreme, Drive with anyone-with-link), packaging (title, description with the UTM link and the chapters, tags, pinned comment in
the config), then the release: **YouTube first on a Sunday at 9 AM America/Chicago, one long-form per week**, then Facebook, Instagram
@danrosefit and TikTok no earlier than the following Monday 9 AM, only after the YouTube video is verified public. Read the live Blotato
YouTube queue first. As of the 10-14 board, Sundays from Oct 18 to Jan 3 2027 are taken, and RO-07 and RO-19 are approved and waiting
behind them (Blotato full), so RO-08 goes after RO-19: expect late January at the earliest.
**If Blotato is at its cap, do not make a scheduled task for this video** (Dan, 2026-10-11): finish everything else (thumbnail, backups,
packaging copy, platform copy, config, receipt draft), put the video on `scripts/blotato/video_waitlist.json`, and the daily
`social-queue-daily-refresh` routine queues it on the next free Sunday. Do not delete queued posts to make room without his word.
Use `scripts/blotato/longform_queue.py`, which refuses an off-Sunday or occupied slot. Never upload to YouTube yourself; Blotato creates
the public video at release time. Receipt in `Docs/RO08_SETUP_RECEIPT_<date>.md`, a board entry for the queued or waiting release, Edit
Queue `uploaded` only once it is queued. The sixpackabs.com article is written now and published once the video is public.

## 5. Already done at finalization (do not repeat)

Clip library: the seven AI clips the film uses are registered as used in RO-08, each with notes on which part is safe to reuse (A0169
time-lapse opener, A0170 donut two-shot, A0171 whining man with lip sync, A0172 gym floor, A0173 fridge raid, A0174 beer, A0175 cell
cartoon). The approval is in the QC corpus (`ro08-r3-final-approved-20261014`). The edit sheet carries his approval. Dan's new standing
rule from this approval (AI clip checks before his FIRST look, retakes over describing faults) is in the first section of VIDEO-RULES.
The Shorts job is on the list as SL-16 (`Handoffs/video-editing/SL-16-intermittent-fasting-shorts.md`). The lessons are in
`.claude/skills/longform-edit/reference/ro08/README.md` (Round 3).

## 6. Open items (not blocking)

- Not done at finalization: the footage ranges of roll C1486 were not marked used in the roll index, and the boxing glove library clip
  A0158 and the stock clips the film uses were not marked "used in RO-08" in the clip library. Do both if the setup task has time; they
  change nothing in the film.
- Hair touches the top edge through the roll (camera framing). He accepted it in round 1 and approved the film. Do not reopen it.
- Dan has not answered whether the long-form AI budget is $15 per video or $15 per clip. Not needed for setup.
- `/Volumes/Extreme/_edit_work/ro08/round3/review`, `review2` to `review5` hold about 30 GB of the reviewers' stills. Safe to delete.
- The Shorts job (SL-16) is separate, after the release is queued.
- Run `scripts/git/drift-check.sh` first; push with `scripts/git/safe-push.sh` only.

## Starter prompt (Claude Opus 5.5, effort high)

```
Read Handoffs/handoff-20261014-ro08-thumbnails-and-video-setup.md. Name this session "Intermittent Fasting LFC Setup". This is a CONTENT long-form and I approved the round 3 film. Use the Codex subscription to generate the images. Have Codex make my five thumbnail choices, five unique designs: 1 pool shoot photo, 1 studio shoot photo, 1 AI-enhanced or AI-generated image of me, and 2 other AI-generated images of Codex's choice (me or not, its judgment). Show me the sheet and stop for my pick, then run /video-setup.
```
