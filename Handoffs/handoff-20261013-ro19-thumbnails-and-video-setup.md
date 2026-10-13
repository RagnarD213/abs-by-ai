# RO-19 "My First Spray Tan": thumbnails, then upload and setup

**CONTENT, long-form (LFC).** It gets Shorts cut from it later and nothing else: no vertical, square or 1-minute version.

**Written 2026-10-13 by Claude (Opus 5.5).** One Claude task does everything: five thumbnail choices (made by Codex in the command line),
stop for Dan's pick, then `/video-setup`. Dan approved the round 4 film on 2026-10-13 ("Okay, everything looks good.").
**Model:** Claude Opus 5.5, effort high (five unique thumbnail designs are design work per `model-routing-plan`; the setup after his pick is
checklist work in the same task).
**Sidebar name:** `My First Spray Tan LFC Setup`. **Use the Codex subscription to generate the images.**

## 1. State

The round 4 full film is delivered, gated, independently reviewed (SHIP, no defects) and approved by Dan. Its review pages (ports 8863,
8865, 8866, 8867) and the copy in `Videos to Review/` were removed on 10-13; the delivery folder is the record.
It is ORGANIC: it ends "So take that first step now, go to absbyai.com and generate an image of yourself with six pack abs. Thank you for
watching guys and I'll see you in the next video." with no tap-the-button call to action. Still run the skill's Step 0 classification, and
`python3 scripts/blotato/ad_guard.py --scan` before and after any Blotato write.
Edit Queue row RO-19 is `finalized` (Drive file and artifact mirror done, version 5). When the release is queued set it `uploaded`, mirror
with `ArtifactData` (artifact `https://claude.ai/artifact/1r1T8Znf96XH24zHZhybHs`, collection `jobs`, pin `if_version`), then
`python3 scripts/edit-queue/queue.py mark-synced RO-19`.

**Check first, before anything is queued:** an older edit of this same video exists (`claude edited long form content/01 - My First Spray
Tan/`, August). Look at the YouTube channel, the live Blotato queue and `BLOTATO_QUEUE_PROGRESS.md` for a "My First Spray Tan" that is
already public or queued. If one is, stop and tell Dan in one line (a replacement upload uses a Sunday slot and he decides what happens to
the old one). If none is, carry on.

## 2. Files (all local)

Folder: `claude edited long form content/16 - My First Spray Tan (RO-19 re-edit)/`
- Master: `My First Spray Tan | claude round 4 | 16x9 | RO-19.mp4`, 1.54 GB, 18:46.46, 1920x1080 29.97, h264 + AAC,
  sha256 `b4b309991b414674e2469fadad7f9b6fb3352ee61f5b02654d1567bbf5b317d8`. Re-hash it first.
- `... RO-19.srt` (342 cues, sidecar, never burned in) and `... RO-19.chapters.txt` (17 chapters, use as-is).
- Also there: `... REVIEW 540p.mp4`, the audio AB file, the edit sheet (approved), stamps (`.audio_gate.json`, `.deliver_gate.json`),
  `ROUND-4-REVIEW.md`, `recipe-RO-19/` (with `dan-approval-20261013-verbatim.md`).
- Work folder (SSD): `/Volumes/Extreme/_edit_work/ro19/round4/`.

Facts for the packaging:
- **Realistic AI footage is in the film:** nine AI clips, all with the AI-GENERATED chip: a man at his monitors (2:32), the spray tan
  appointment (4:16), the eight hour wait (5:49), the stained sheets (6:13), a man and his doctor (10:47), the orange tan (12:24), a man
  with a towel in a home gym (13:22), the pale patch on a back (13:44), the vampire on the beach (14:42). So `ai_generated: true` in the
  Blotato config (TikTok) and the altered/synthetic flag on YouTube. The goal picture in the phone demo near 18:01 is a labelled AI still.
  Keep the one-line AI-image sentence in the description.
- **No links are promised on camera.** He names no product or studio. Prices he says: a premium spray tan with contouring about $80 plus
  $20, about $50 without contouring at a cheaper studio, "$50 to $100" each time. Do not invent a link or name a studio.
- What the video covers, for the description (the chapters file is the outline): why a tan makes you look more defined on camera, how he
  found a studio with AI, cost, tanning at home (wipes and sprays), what the appointment is like, drying time and aftercare (rapid tan:
  wait 8 hours), the first shower, how long it lasts (about 7 days), the downside with water, his before and after photos, the biggest
  pro (no sun damage), very pale skin, the cons, who should and should not get one, and how to get the most out of it for a photo shoot.
- His real before and after photos are in the film at 0:03, 0:48, 3:00, 9:13 and 9:24, each with "Real picture(s) of me. Not
  AI-generated." Nothing to do for setup; it is why the description can say the photos are real.
- UTM link and call to action per `/video-setup` Step 3. Write the pinned question comment into the Blotato config as `"pinned_comment"`
  (`Docs/PINNED_COMMENTS.md`): an easy question about this video, for example whether they have ever had a spray tan.
- **The stamps read FAIL and that is known.** Audio gate: the tone row only, with voice B2, the audition Dan picked. Delivery gate 2.5.1:
  31 rows pass, 8 fail (audio:stamp, audio:click_at_joins, style:coverage 32 %, framing:hair_top, framing:headroom,
  cut:splice_visibility, captions:burned, junk:repeated_take). The independent review of this file said SHIP and Dan approved the film.
  Do not rebuild or re-gate; if a setup script refuses the stamp, tell Dan what it refused and stop.
- The master is over Blotato's 400 MB cap: encode a platform copy (`nice -n 20`, VideoToolbox, audio copied).
- TikTok: 18:46 may be over the length the account allows. Check the account's limit; if it refuses, record it in the receipt and tell Dan
  (RO-01's TikTok limit is still unresolved on the board).

## 3. Thumbnails first: five choices, five unique designs, all made by Codex, then STOP

Rule: `.claude/skills/_shared/VIDEO-RULES.md`, first section (Dan, 2026-10-13, set on this video). Read it, `/youtube-packaging` for the
photo, crop and text-clearance rules, and `_shared/IMAGE-GENERATION.md`. His request for this video, in his words:

> For thumbnails, have Codex make me: one with the pool shoot; one with the studio shoot; one with an AI-enhanced image of me getting a
> spray tan, or an AI-generated image of me getting a spray tan; two other AI-generated images of Codex's choice, which can be me or not,
> depending on its judgment. Unique design for all thumbnails.

1. **Pool shoot:** one real photo of Dan from `photos/pool shoot | 7-31-26 | dan | mindi/` (finalized picks and cutouts:
   `photos/finalized social media photos/`, `_cutouts/`). His real cutout over a Codex background; type set in code. Crop at the waistband (Speedo rule). Not a photo from `Frowning Photos/`.
2. **Studio shoot:** one real photo from `photos/studio shoot | 8-28-26 | dan | mindi/`, built the same way.
3. **An AI-enhanced or AI-generated image of Dan getting a spray tan.** Either enhance a real photo of him (give Codex the photo as the
   reference) or generate him in a pop-up tanning tent with a spray gun and mist. Prompt: "lean and shredded, not bulky, same size as the
   reference"; swim shorts, not briefs (Codex refuses a man in briefs). Look at the face before it goes on the sheet: it has to read as
   him. This is the one option where he may be AI-enhanced or generated.
4. and 5. **Two more AI-generated images of Codex's choice**, Dan or not. Let Codex choose. Ideas from the film, only as a starting point:
   a pale half and a tanned half of one torso; a spray gun and a cloud of bronze mist; "$80" on a price tag over a tanning tent; the brown
   body print on white sheets; a vampire under an umbrella on a beach. Thumbnails carry no AI label, no "Real picture" label and no
   AbsByAI.com.

**Five unique designs.** Before building, write one line per option naming its layout, type treatment, colour and composition, and check
that no two share them. The pool and studio options need their own designs as well: no two of the five on the same layout.

Same copy on all five unless Dan asks for alternatives; short and big (two lines beats three). The video's own lines: "My First Spray
Tan", "Is A Spray Tan Worth It?", "I Got A Spray Tan". No result claims. `.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol
--effort high` for every generated image; no outside image model. QC on the RENDERED files: person-mask clearance of every text block
from his face and hair of at least 25 px, and look at the sheet yourself before sending it. Save the finals in
`social media graphics/youtube/thumbnails/My First Spray Tan/`. Show all five on one review sheet (`SendUserFile`, display render), list
them in plain words with each one's design line, and **STOP for Dan's pick.** He may pick one, or two for an A/B test. Final file:
`<title> - thumbnail FINAL.jpg`, 1280x720 JPEG, under 2 MB.

## 4. Then `/video-setup`

Backups (Extreme, Drive with anyone-with-link), packaging (title, description with the UTM link and the chapters, tags, pinned comment in
the config), then the release: **YouTube first on a Sunday at 9 AM America/Chicago, one long-form per week**, then Facebook, Instagram
@danrosefit and TikTok no earlier than the following Monday 9 AM, only after the YouTube video is verified public. Read the live Blotato
YouTube queue first. As of the 10-13 board these Sundays are taken: Oct 18 RO-05, Oct 25 RO-12, Nov 1 RO-16, Nov 8 Oura, Nov 15 RO-13,
Nov 22 RO-02, Nov 29 RO-10, Dec 6 RO-01, Dec 13 RO-11, Dec 20 RO-03, Dec 27 RO-06, Jan 3 Video 5 (Getting Abs At 40 vs 25). RO-07 is
approved and on HOLD because Blotato is full, so RO-19 goes after it: expect mid January at the earliest.
**If Blotato is at its cap, do not make a scheduled task for this video** (Dan, 2026-10-11): finish everything else (thumbnail, backups,
packaging copy, platform copy, config, receipt draft), put the video on `scripts/blotato/video_waitlist.json`, and the daily
`social-queue-daily-refresh` routine queues it on the next free Sunday. Do not delete queued posts to make room without his word.
Use `scripts/blotato/longform_queue.py`, which refuses an off-Sunday or occupied slot. Never upload to YouTube yourself; Blotato creates
the public video at release time. Receipt in `Docs/RO19_SETUP_RECEIPT_<date>.md`, a board entry for the queued or waiting release, Edit
Queue `uploaded` only once it is queued. The sixpackabs.com article is written now and published once the video is public.

## 5. Already done at finalization (do not repeat)

Clip library: the seven new AI clips are registered as used in RO-19 (A0162 vampire, A0163 orange tan, A0164 sheets, A0165 the
appointment, A0166 the doctor, A0167 the eight hour wait, A0168 the pale patch). **A0166 is now the default clip for every "talk to your
doctor" line** (VIDEO-RULES). The round 3 finding and the round 4 approval are in the QC corpus (`ro19-r3-full-film-false-start-20261013`,
`ro19-r4-final-approved-20261013`). The edit sheet carries his approval. The lessons are in
`.claude/skills/longform-edit/reference/ro19/README.md` (Round 4) and the first section of VIDEO-RULES (the thumbnail standard).

## 6. Open items (not blocking)

- Not done at finalization: the footage ranges of roll C1512 were not marked used in the roll index, and the stock and library clips the
  film uses were not marked "used in RO-19" in the clip library. Do both if the setup task has time; they change nothing in the film.
- One 7 ms left/right encoding blip at 15:29.7, told to Dan on the round 4 page; he approved the film. Do not reopen it.
- Hair touches the top edge through the roll (camera framing). He said to leave it. Do not reopen it.
- `/Volumes/Extreme/_edit_work/ro19/round4/film/review4/` holds 6 GB of the reviewer's stills. Safe to delete.
- The Shorts job cut from this film is separate (`/shorts`), after the release is queued.
- Run `scripts/git/drift-check.sh` first; push with `scripts/git/safe-push.sh` only.

## Starter prompt (Claude Opus 5.5, effort high)

```
Read Handoffs/handoff-20261013-ro19-thumbnails-and-video-setup.md. Name this session "My First Spray Tan LFC Setup". This is a CONTENT long-form and I approved the round 4 film. Use the Codex subscription to generate the images. Have Codex make my five thumbnail choices, five unique designs: 1 pool shoot photo, 1 studio shoot photo, 1 AI-enhanced or AI-generated image of me getting a spray tan, and 2 other AI-generated images of Codex's choice (me or not, its judgment). Show me the sheet and stop for my pick, then run /video-setup.
```
