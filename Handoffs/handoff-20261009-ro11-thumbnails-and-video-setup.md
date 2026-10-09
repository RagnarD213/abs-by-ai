# RO-11 "When Calories Don't Matter For Fat Loss": thumbnails, then upload and setup

**CONTENT, long-form (LFC).** It gets Shorts cut from it later and nothing else: no vertical, square or 1-minute version.

**Written 2026-10-09 by Claude.** One Claude task does everything: five thumbnail choices (images made by Codex in the command line),
stop for Dan's pick, then `/video-setup`. Dan approved the round 4 film on 2026-10-09 ("All right, this is approved").
**Model:** Claude Sonnet 5.5, effort medium (mechanical setup per `model-routing-plan`; Opus high only if Dan rejects the title or description copy).
**Sidebar name:** `Calories Don't Matter LFC Setup`. **Use the Codex subscription to generate the images.**

## 1. State

The round 4 full film is delivered, gated, independently reviewed (SHIP, 0 defects) and approved by Dan. The Dan-facing copy in
`Videos to Review/` and the review pages (ports 8871, 8872, 8802) were removed on 10-09; the delivery folder is the record.
It is ORGANIC: it ends "And subscribe for more videos like this one." with no tap-the-button call to action and no AbsByAI line.
Still run the skill's Step 0 classification, and `python3 scripts/blotato/ad_guard.py --scan` before and after the Blotato write.
Edit Queue row RO-11 is already `finalized` (artifact mirror done); when the release is queued set it `uploaded`, mirror with
`ArtifactData` (artifact `https://claude.ai/artifact/1r1T8Znf96XH24zHZhybHs`, collection `jobs`, pin `if_version`), then `queue.py mark-synced RO-11`.

## 2. Files (all local)

Folder: `claude edited long form content/11 - When Calories Don't Matter For Fat Loss/`
- Master: `When Calories Don't Matter For Fat Loss | claude round 4 | 16x9 | RO-11.mp4`, 3.13 GB, 9:58.9, 1920x1080 29.97, h264 + AAC,
  sha256 `fea0dd87ffbb37b4311feadaa5059ba69f9156df258a33f3c42540528786a8ad`. Re-hash it first.
- `... RO-11.srt` (180 cues, sidecar, never burned in) and `... RO-11.chapters.txt` (9 chapters, use as-is).
- Also there: `... REVIEW 540p.mp4`, audio AB file, stamps (`.audio_gate.json`, `.deliver_gate.json`), `notes-RO11.md` (the sources list and
  upload notes at the bottom), `ROUND-4-REVIEW.md`, `recipe-RO-11/`. The round 2 files in the same folder are the superseded cut: ignore them.
- Work folder (SSD): `/Volumes/Extreme/_edit_work/ro11/round4/`.

Facts for the packaging:
- **Realistic AI footage is in the film:** the opener (a heavy man at a kitchen table, 0:01.8 to 0:04.5, with the AI-GENERATED chip). So
  `ai_generated: true` in the Blotato config (TikTok) and the altered/synthetic flag on YouTube. The section-card AI picture of Dan with a beer
  (1:25) is a labelled still and does not by itself trigger the flag. Keep the one-line AI-image sentence in the description.
- Content for the description: the 7 factors, in order: sleep (7 to 8 hours, bedroom at 63, glycine), alcohol, hormones (low testosterone,
  cortisol), meal timing (stop eating 3 hours before bed), protein (every meal, protein first), exercise (lift weights, cardio gets eaten back),
  daily movement (8 to 10K steps). Script source: `Docs/SCRIPTS_923_SHOOT_LONGFORM_DAN_EDITED_20260921.md`. UTM link and CTA per `/video-setup` Step 3.
- Sources for the description (from `notes-RO11.md`): Nedeltcheva et al., Annals of Internal Medicine 2010 (sleep); Siler et al., Am J Clin
  Nutr 1999 (alcohol); Vujovic et al., Cell Metabolism 2022 (late eating); Cienfuegos et al., Cell Metabolism 2020 (4 and 6 hour eating
  windows); Lin et al., Annals of Internal Medicine 2023 (12 months of fasting); Longland et al., Am J Clin Nutr 2016 (protein, McMaster);
  Martin et al., E-MECHANIC, Am J Clin Nutr 2019 (cardio); Levine et al., Science 1999 (daily movement, Mayo Clinic).
- Description links to other videos go in only once that video is public: the alcohol video (RO-13, Nov 15), the first calories video (RO-10,
  Nov 29). The glycine video (RO-15) is not edited yet: leave it out.
- **The delivery gate stamp reads FAIL (gate 2.5.0), 35 of 39 rows pass.** The four failing rows are the same four every organic long-form
  shows and RO-11 round 2 showed: `captions:burned`, `captions:card_collision` (the Soft Blue lower thirds read as captions; nothing is burned
  in), `cut:splice_visibility` (5 of 91 deliberate framing cuts just over the ceiling) and `framing:push_coverage` (a measuring gap). The
  independent review said SHIP. Do not rebuild or re-gate; if a setup script refuses the stamp, tell Dan what it refused and stop.
- The master is over Blotato's 400 MB cap: encode a platform copy (`nice -n 20`, VideoToolbox, audio copied).

## 3. Thumbnails first

Read `.claude/skills/_shared/VIDEO-RULES.md` (the thumbnail section, the 10-04 belly rule: no belly close-ups or fat pinching, and thumbnails
never put text over his face or hair; the Speedo crop rule; no frowning photos), `.claude/skills/_shared/IMAGE-GENERATION.md`, then `/youtube-packaging`.
**Dan's five, exactly (2026-10-09):**

1. **One real pool-shoot photo** (a real photo of Dan, never redrawn; background-removed cutout plus type in code).
2. **One real studio-shoot photo** (same rule). Rotate away from the photos the last few videos used, and from photo-21 and photo-29, which are on
   this film's Sleep and Exercise cards.
3. **One AI image of Dan looking ripped, eating a ton of high-calorie food** (burgers, pizza, donuts, fries, a table piled with it). The
   joke is the contradiction: a lean, shredded man in front of a mountain of food, which is the video's point. Build it from his real likeness
   references, as the 10-05 alcohol thumbnail did: `social media graphics/youtube/thumbnails/Can You Drink Alcohol And Still Have Abs/_build-2026-10-05/assets/ai_dan.png`
   (and its `log_dan.txt`) show the Codex recipe that worked. Per the belly rule he is lean and shown chest up or whole figure, never a belly
   close-up, no hands on his stomach. Thumbnails carry no AI label.
4. **AI image #2 and 5. AI image #3: two other AI-generated images, each a unique design of Codex's choice**, attention-getting and highly
   relevant to the topic (calories are not everything: sleep, alcohol, hormones, meal timing, protein, exercise, daily movement; a calorie
   counter or scale versus a lean physique; a plate of food versus a clock; etc.). They do not have to be Dan. Different image and different
   design from each other and from #3.

Same copy on all five unless Dan asks for alternatives. The video's own line is "In a deficit, you can still keep your belly fat" and its
lower third reads "CALORIES AREN'T EVERYTHING"; keep thumbnail copy short and big (two lines beats three), no claims or numbers-as-results.
`.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high` for every AI image; no outside image model. QC on the RENDERED files:
person-mask clearance of every text block from his face and hair of at least 25 px, and look at the sheet yourself before sending it (every
past defect was visible on the sheet and invisible to the numbers). Save the finals in
`social media graphics/youtube/thumbnails/When Calories Don't Matter For Fat Loss/`. Show all five on one review sheet
(`SendUserFile`, display render), list them in plain words, and **STOP for Dan's pick.** He may pick one, or two for an A/B test (Step 6).
Final file: `<title> - thumbnail FINAL.jpg`, 1280x720 JPEG, under 2 MB.

## 4. Then `/video-setup`

Backups (Extreme, Drive with anyone-with-link), packaging (title, description with the UTM link and the chapters, tags, pinned comment),
Blotato release: **YouTube first on a Sunday at 9 AM America/Chicago, one long-form per week**, then Facebook, Instagram @danrosefit and
TikTok no earlier than the following Monday 9 AM, only after the YouTube video is verified public. Read the live Blotato YouTube queue first. As
of the 10-09 board these Sundays are taken: Oct 11 Stop Deadlifting, Oct 18 RO-05, Oct 25 RO-12, Nov 1 RO-16, Nov 8 Oura, Nov 15 RO-13,
Nov 22 RO-02, Nov 29 RO-10, Dec 6/7 RO-01. So expect **Dec 13**; use `scripts/blotato/longform_queue.py`, which refuses an off-Sunday or occupied
slot. Never upload to YouTube yourself; Blotato creates the public video at release time. Receipt in `Docs/RO11_SETUP_RECEIPT_<date>.md`, board
entry (delete the RO-11 review entry), Edit Queue `uploaded`. The sixpackabs.com article is written now and published once the video is public (Step 6b).

## 5. Clip library, once the release is queued (Dan approved the film)

Register what the approved film used with `python3 .claude/skills/_shared/cliplib/clip_library.py add ... --status used-final --used-in "RO-11"`,
then `clip_library.py sheet`: the AI opener clip (`/Volumes/Extreme/_edit_work/ro11/aiframes/C_motion_v2.mp4`, kind ai, trimmed from 3.29 s, the
heavy man at a kitchen table), the 10 Pexels clips used (`/Volumes/Extreme/_edit_work/ro11/stock/p7556225, p6944072, p10317805, p5847850,
p6290471, p6036689, p9902350, p38757135, p5116397, p4259069, p8550877`; descriptions in `recipe/plan.py`, items C01 to C12; C09 and C10 are
already library clips B0287 and B0098, skip them) and the four section-card Pexels stills (`assets/titles/src/pexels-4040557, 10755460, 5463890,
17944685.jpg`). Check `clip_library.py find` first so nothing is added twice.

## 6. Open items (board, not blocking)

- Dan's known small notes, accepted by his approval: the Alcohol card's AI image hair is about 13 px from the top edge at the end of the slow push
  (not cut), the Daily Movement stock walker's head touches the top edge, and the 0.7 s added ending is room tone at -77 dB. Not part of this task.
- Run `scripts/git/drift-check.sh` first; push with `scripts/git/safe-push.sh` only.
- Delete the RO-11 board entry once this task has queued the release.

## Starter prompt (Claude Sonnet 5.5, effort medium)

Read `Handoffs/handoff-20261009-ro11-thumbnails-and-video-setup.md`. Name this session "Calories Don't Matter LFC Setup". This is a CONTENT
long-form and I approved the round 4 film. Use the Codex subscription to generate the images. Make my five thumbnail choices (1 pool photo,
1 studio photo, 1 AI image of me looking ripped eating a ton of high-calorie food, and 2 other unique AI designs of Codex's choice that are
attention-getting and relevant), show me the sheet and stop for my pick, then run /video-setup.
