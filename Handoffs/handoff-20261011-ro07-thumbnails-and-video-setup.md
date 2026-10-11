# RO-07 "Why You MUST Work Out Every Day": thumbnails, then upload and setup

**CONTENT, long-form (LFC).** It gets Shorts cut from it later and nothing else: no vertical, square or 1-minute version.

**Written 2026-10-11 by Claude.** One Claude task does everything: five thumbnail choices (images made by Codex in the command line),
stop for Dan's pick, then `/video-setup`. Dan approved the round 3 film on 2026-10-11 ("Okay, this is looking good. This is approved.").
**Model:** Claude Opus 5.5, effort high (five unique thumbnail designs are design work per `model-routing-plan`; the setup after his pick is checklist work in the same task).
**Sidebar name:** `Work Out Every Day LFC Setup`. **Use the Codex subscription to generate the images.**

## 1. State

The round 3 full film is delivered, gated, independently reviewed (SHIP) and approved by Dan. The copies in `Videos to Review/` and the
review pages (ports 8857 to 8860) were removed on 10-11; the delivery folder is the record.
It is ORGANIC: it ends "Go to absbyai.com now. Thanks for watching guys and I'll see you in the next video." with no tap-the-button call to
action. Still run the skill's Step 0 classification, and `python3 scripts/blotato/ad_guard.py --scan` before and after the Blotato write.
Edit Queue row RO-07 is `finalized` (artifact mirror done, version 9); when the release is queued set it `uploaded`, mirror with
`ArtifactData` (artifact `https://claude.ai/artifact/1r1T8Znf96XH24zHZhybHs`, collection `jobs`, pin `if_version`), then `queue.py mark-synced RO-07`.

## 2. Files (all local)

Folder: `claude edited long form content/14 - Why You MUST Work Out Every Day/`
- Master: `Why You MUST Work Out Every Day | claude round 3 | 16x9 | RO-07.mp4`, 1.79 GB, 18:06.75, 1920x1080 29.97, h264 + AAC,
  sha256 `cc3456461691c9b073b72b4ba34cefdef3e0c12d5f1286c30b94040aa3126615`. Re-hash it first.
- `... RO-07.srt` (338 cues, sidecar, never burned in) and `... RO-07.chapters.txt` (17 chapters, use as-is).
- Also there: `... REVIEW 540p.mp4`, the audio AB file, the edit sheet (approved), stamps (`.audio_gate.json`, `.deliver_gate.json`),
  `ROUND-3-REVIEW.md`, `ROUND-3-REVIEW-2.md`, `recipe-RO-07/` (with `dan-approval-20261011-verbatim.md`).
- Work folder (SSD): `/Volumes/Extreme/_edit_work/ro07/round3/`.

Facts for the packaging:
- **Realistic AI footage is in the film:** five AI clips, all with the AI-GENERATED chip: a dad and kids in a kitchen (2:01), a lifter
  deadlifting (2:24), a sore man on the stairs (2:27), the door and boxing glove gag (4:57), a family dinner (6:42). So `ai_generated: true`
  in the Blotato config (TikTok) and the altered/synthetic flag on YouTube. The goal picture in the phone demo at 17:37 is a labelled AI
  still. Keep the one-line AI-image sentence in the description.
- **Dan promises links on camera.** At about 11:20: "a kettlebell, a yoga mat, an ab wheel, a jump rope, and push-up handles ... I'll link in the
  description to where you can get that on Amazon, super cheap. You can get all that stuff for 50 bucks." The lower third there reads "The
  Basic Equipment I Use Is Linked Below." The five Associates links are already on record in `Docs/AMAZON_ASSOCIATES.md` (RO-06 table,
  tag `danrosefit-20`): use those five, plus the hand towels link for the towel rows (15:36), and the disclosure line "As an Amazon
  Associate I earn from qualifying purchases." Never invent a link. Do not print a total price in the description (the linked items come to
  more than the $50 he says).
- **Gymboss (13:22):** "The one I personally use is Gymboss ... Go and download it right now. It's free." Link the official Gymboss
  Interval Timer app pages (App Store and Google Play; find them, do not guess the URLs) and give the setting he says: 5 rounds of
  30 seconds, repeated 4 times.
- The workout for the description, in his order: bodyweight squats, push-ups (knees if needed), lunges, towel rows, 30 seconds of rest
  jogging in place; beginners 2 circuits (about 5 minutes), advanced 3 or 4. The month plan: month 1 five minutes at home, month 2 ten
  minutes with the basic equipment, month 3 fifteen, month 4 a home gym or a gym membership, then add 5 minutes at a time.
- The chapters file is the outline for the description. UTM link and call to action per `/video-setup` Step 3.
- **The stamps read FAIL and that is known.** Audio gate: the tone row only, with voice 4, the audition Dan picked. Delivery gate 2.5.1:
  30 rows pass, 9 fail (audio:stamp, style:coverage 27 %, framing:hair_top, framing:headroom, cut:splice_visibility,
  captions:card_collision, captions:burned, watch:pass on hair, junk:repeated_take). The independent review of this file said SHIP and Dan
  approved the film. Do not rebuild or re-gate; if a setup script refuses the stamp, tell Dan what it refused and stop.
- The master is over Blotato's 400 MB cap: encode a platform copy (`nice -n 20`, VideoToolbox, audio copied).
- TikTok: 18:07 is over the length some accounts allow (RO-01's TikTok limit is still unresolved on the board). If TikTok refuses it,
  queue the other three and say so.

## 3. Thumbnails first: Dan's mix for THIS video (his words, 2026-10-11)

"5 Codex thumbnail variations: 1 pool shoot, 1 studio shoot, 1 with a screen capture of me doing exercise from B-roll, or any exercise shot
from a photo shoot, 2 other AI-generated images, 5 unique designs." This replaces the standing mix (pool, studio, three AI) for this
video only, because he named it.

Read `.claude/skills/_shared/VIDEO-RULES.md` (the thumbnail sections, including "every image is its own design" of 2026-10-10, the belly
rule, text never over his face or hair, the Speedo crop rule, no frowning photos, no real-picture label and no AbsByAI.com on thumbnails),
`.claude/skills/_shared/IMAGE-GENERATION.md`, then `/youtube-packaging`. **The five:**

1. **One real pool-shoot photo** (a real photo of Dan, never redrawn: Codex makes the background only, his real cutout and the type are
   layered in code).
2. **One real studio-shoot photo** (same rule). Rotate away from the photos the last few videos used.
3. **One real exercise shot of Dan:** a frame from the B-roll, or an exercise photo from a photo shoot. Never redrawn; it may be enhanced
   for clarity (sharpen, grade) and cut out. Good sources, all 4K, where he looks ripped and well lit:
   - handstand push-ups against the pillar: 8/28 roll C1684, 16 to 30 s (library B0545, B0456);
   - push-ups on the handles, side on in low sun: 8/28 roll C1680, 190 to 250 s (library B0546, B0548);
   - fast jump rope by the pool: 8/28 roll C1674 from about 95 s (library B0448);
   - decline push-ups with feet on the chair (library B0453), seated overhead press, lateral raises, curls (B0449, B0450, B0458).
   8/28 rolls live in `/Volumes/Extreme/abs by ai 8:28 shoot | jeff | dan | ads, dedicated shorts, b roll, scripted long form content/main camera/`
   (S-Log3: grade with `website-video-828/slog3_709_e1.30.cube` or `e1.45`, saturation 0.88, as the library cuts do). Grab the frame from
   the roll at full 4K, not from the film. Pick the frame at the hardest point of the rep with his face visible if the angle allows.
4. and 5. **Two other AI-generated images**, each a different idea that sells the topic. They do not have to be Dan. Ideas from the film:
   a calendar with every day checked off; a phone timer reading 5:00 beside a yoga mat at sunrise; a man doing push-ups on a living room
   floor at dawn; "5 MIN" against "1 HOUR" as a visual contrast; an alarm clock and a kettlebell. Thumbnails carry no AI label.

**Five unique designs.** Before building, write one line per option naming its layout, type treatment, colour and composition, and check
that no two share them (headline left stack, centred, bottom band, split panel, over-the-shoulder; different type colours and subject
scale). This time the pool and studio options also need their own designs: the house layout may be used once at most.

Same copy on all five unless Dan asks for alternatives; short and big (two lines beats three). The video's own lines: "Work Out Every
Day", "5 Minutes Daily Beats 1 Hour Twice A Week", "5 Minutes A Day". A time is a fact about the workout, not a result claim.
`.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high` for every generated image; no outside image model. QC on the
RENDERED files: person-mask clearance of every text block from his face and hair of at least 25 px, and look at the sheet yourself before
sending it. Save the finals in `social media graphics/youtube/thumbnails/Why You MUST Work Out Every Day/`. Show all five on one review
sheet (`SendUserFile`, display render), list them in plain words with each one's design line, and **STOP for Dan's pick.** He may pick
one, or two for an A/B test. Final file: `<title> - thumbnail FINAL.jpg`, 1280x720 JPEG, under 2 MB.

## 4. Then `/video-setup`

Backups (Extreme, Drive with anyone-with-link), packaging (title, description with the equipment links, the Gymboss links, the UTM link
and the chapters, tags, pinned comment), Blotato release: **YouTube first on a Sunday at 9 AM America/Chicago, one long-form per week**,
then Facebook, Instagram @danrosefit and TikTok no earlier than the following Monday 9 AM, only after the YouTube video is verified
public. Read the live Blotato YouTube queue first. As of the 10-11 board these Sundays are taken: Oct 11 Stop Deadlifting, Oct 18 RO-05,
Oct 25 RO-12, Nov 1 RO-16, Nov 8 Oura, Nov 15 RO-13, Nov 22 RO-02, Nov 29 RO-10, Dec 6 RO-01, Dec 13 RO-11, Dec 20 RO-03. **RO-06 is
approved but on HOLD because Blotato is full (board), and Zeeshan's Video 5 setup is also waiting**, so RO-07 goes after them: expect the
first free Sunday in January at the earliest. If Blotato is still at its cap, finish everything else (thumbnail, backups, packaging copy,
receipt draft), put RO-07 on the board as HOLD beside RO-06, and tell Dan; do not delete queued posts to make room without his word.
Use `scripts/blotato/longform_queue.py`, which refuses an off-Sunday or occupied slot. Never upload to YouTube yourself; Blotato creates
the public video at release time. Receipt in `Docs/RO07_SETUP_RECEIPT_<date>.md`, a board entry for the queued release, Edit Queue
`uploaded`. The sixpackabs.com article is written now and published once the video is public.

## 5. Already done at finalization (do not repeat)

Footage ranges marked used on the seven rolls (C1484, C1485, C1490, C1493, C1494, C1680, C1684); clip library: the two AI clips (A0158 the
door and glove gag, A0159 the sore man on the stairs), four cuts of Dan (B0545 handstand reps from the first frame, B0546 to B0548 push-ups
side on), one stock clip (B0549), and 31 library clips marked used in RO-07; the approval is in the QC corpus
(`ro07-r3-final-approved-20261011`); the edit sheet carries his approval; the lessons are in
`.claude/skills/longform-edit/reference/ro07/README.md` and the top section of VIDEO-RULES.

## 6. Open items (not blocking)

- Hair touches the top edge in about 2.5 % of the on-camera frames (camera framing). The delivery message asked "leave as shot or add
  headroom"; he approved the film as delivered and wrote no line on it, so it stays as shot. Do not reopen it.
- The Shorts job cut from this film is separate (`/shorts`), after the release is queued.
- Run `scripts/git/drift-check.sh` first; push with `scripts/git/safe-push.sh` only.

## Starter prompt (Claude Opus 5.5, effort high)

Read `Handoffs/handoff-20261011-ro07-thumbnails-and-video-setup.md`. Name this session "Work Out Every Day LFC Setup". This is a CONTENT
long-form and I approved the round 3 film. Use the Codex subscription to generate the images. Make my five thumbnail choices, five unique
designs: 1 pool shoot photo, 1 studio shoot photo, 1 screen capture of me doing an exercise from the B-roll (or an exercise shot from a
photo shoot), and 2 other AI-generated images. Show me the sheet and stop for my pick, then run /video-setup.
