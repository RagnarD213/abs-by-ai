# Handoff: RO-10 "Calories: The Reason You're Not Losing Weight", thumbnails then upload and setup (2026-10-02)

**One Claude task does both halves** (Dan's rule, 2026-10-01): make the thumbnail options, stop for Dan's pick, then run
`/video-setup`. **Use the Codex subscription to generate the images**, called from the command line, on **Sol 6.1 at
high effort** (Dan, 2026-10-02). No separate Codex handoff.

**Session name:** `Calories Not Losing Weight LFC Setup`.

## 1. The video
- **Approved by Dan 2026-10-02:** *"All right, this video is approved."* Organic long-form, 8:38.25. Ending: "Subscribe,
  and make sure you don't miss that next video" (organic, no button call to action).
- Folder: `claude edited long form content/10 - Calories The Reason You're Not Losing Weight/`
  - Master: `Calories The Reason You're Not Losing Weight | claude round 2 | 16x9 | RO-10.mp4`
    (sha256 `655c71882ea3e6baa1c71d661fdcd8465e94d972183f4969e09d2430787bb76e`, 1920x1080, 2.5 GB).
  - Beside it: `.srt` (156 cues), `.chapters.txt` (11 chapters), `notes-RO10.md` (checks, gate rows, upload notes).
- What it says: the one reason you are not losing weight is calories. The proof (the professor who lost 27 lb on snack
  cakes at 1,800 calories a day; Stanford's low-carb vs low-fat study; people eating 47% more than they thought), then 8
  ways to eat less without being hungry: a GLP-1 medication, know your calorie number, track with AI, fast until 2 PM,
  black coffee, start meals with a salad, protein snacks, no liquid calories.
- Dan wears a black tank top throughout, so **no frame of the film shows his abs**.

## 2. Thumbnails: five options, Dan's mix for THIS video
Dan asked for this mix (it replaces the standing five-choice mix for this video only):

1. **One with Dan from the pool shoot** (real photo).
2. **One with Dan from the studio shoot** (real photo).
3. **Three unique AI-generated images, each with its own unique design that Codex chooses.**

That is five options. ⚠ Dan's dictated wording was "three unique AI-generated images and three unique designs for each of
them". Claude read it as three images with one design each. If Dan says he meant three designs per image, build nine AI
options (eleven in all); ask nothing first, show five, and offer the extra six in the review message.

**How to call Codex (model and effort are Dan's):**
```bash
.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high --prompt-file p.txt --out result.png [--image ref.jpg]
```
(`--model` was added 2026-10-02; `gpt-6.1-sol` was tested on the command line and answers.) State the image count before
the batch; do not generate spares. Rule and traps: `.claude/skills/_shared/IMAGE-GENERATION.md`.

**Options 1 and 2 (real Dan):** Codex never redraws him. Have Codex generate the BACKGROUND only (a bold, topic-specific
scene: junk food, a scale, a calorie number), then layer his real cutout from
`photos/finalized social media photos/_cutouts/` and set the type in code. Abs visible, text never on his face, hair or
abs, never a frowning photo, pool Speedo photos cropped at the waistband. Rotate away from photos the last few long-form
thumbnails used (`social media graphics/youtube/thumbnails/`).

**Options 3, 4, 5 (AI images):** let Codex choose. For each, ask Codex (Sol 6.1, high) for one image concept AND its
layout (where the headline sits, what the accent is), each visibly different from the other two in subject, colour and
composition. Ideas it may use or ignore: the snack-cake diet, a scale, a plate against a calorie number, "low carb vs low
fat". Type that ships is set in code, in the position Codex designed, because generated type touches heads and arms. If
Codex puts Dan in an image, pass a real reference photo and say "lean and shredded, not bulky, same size as the reference".

**Standing rules that still apply:** `.claude/skills/_shared/VIDEO-RULES.md` (read in full first), `/video-setup` Step 2 and
`/youtube-packaging` for the type system, no claims or result numbers as promises, no AbsByAI.com on the thumbnail, short
big copy (two lines beat three), same headline across the five unless a design needs its own. Headline direction (your
call): about calories being the reason, e.g. `IT'S THE CALORIES` or `WHY YOU'RE NOT LOSING WEIGHT`. Do not show a drug
name on a thumbnail.

**Deliver:** build in `social media graphics/youtube/thumbnails/Calories The Reason You're Not Losing Weight/_build-2026-10-02/`.
Check each on the rendered file (person-mask clearance of the text, legible at 320 px wide, nothing clipped). One review
sheet with the five labelled 1 to 5, the Codex token total, then **stop for Dan's pick** (he may pick two for an A/B test).
After the pick export `... - thumbnail FINAL.jpg` (and `FINAL B.jpg`) at 1280x720, JPEG, under 2 MB.

## 3. Upload and setup (`/video-setup`, after the pick, no further stop)
- Read `.claude/skills/video-setup/SKILL.md` and follow it. Organic: **Blotato only**, no upload to YouTube by us, never
  Public by us, no native scheduling. Run `python3 scripts/blotato/ad_guard.py --scan` before and after.
- **AI flags are TRUE for this video:** YouTube altered/synthetic and TikTok AI-generated (three realistic AI clips: the
  opener's two and the 0:31 kitchen clip). Keep the one-line AI-image sentence in the description.
- Description: chapters from `.chapters.txt`; sources (Haub, Kansas State, 2010; Gardner et al., DIETFITS, JAMA 2018;
  Hall and Guo, Gastroenterology 2017; Lichtman et al., NEJM 1992; Jastreboff et al., SURMOUNT-1, NEJM 2022; Rolls et al.,
  J Am Diet Assoc 2004; DiMeglio and Mattes, Int J Obes 2000). Dan says on camera he will link his Zepbound tips video:
  that video (RO-12) is queued for Oct 25. If this one releases first, leave a note in the setup receipt to add the link
  the day RO-12 is public; if it releases after, put the link in.
- The film ends "In the next video, I'm going to show you when calories don't matter", which is RO-11 (in review). Pick a
  release slot that keeps this one before RO-11, and say which slot you chose.
- Blotato's 400 MB cap: the master is 2.5 GB, so make the platform copy as the skill says (hardware encoder, low priority).
- TikTok length cap and cover-first copy: per the skill.
- Edit Queue: `python3 scripts/edit-queue/queue.py set RO-10 uploaded ...` only after the schedule is read back; mirror to
  the queue page. Write `Docs/RO10_SETUP_RECEIPT_<date>.md`.

## 4. Already done (do not redo)
- Film built, gated, independently reviewed (SHIP) and delivered 2026-10-01; Edit Queue shows `finalized` (2026-10-02).
- All 17 clips are in the clip library (A0143 to A0145, B0480 to B0493).
- Known and accepted with the approval: delivery-gate stamp reads FAIL on six rows that are detector readings, and 16
  shots open on one repeated frame (see `notes-RO10.md`). Neither blocks the upload. Do not rebuild the film.

## 5. Finish
Board entry (re-read from disk, edit only yours, `scripts/board-check.sh`), `Handoffs/README.md` row to executed, commit
with `scripts/git/safe-push.sh -m "..." -- <your files>`. No em dashes in anything you write.

## 6. Model and starter prompt
**Claude Opus 5.5, effort medium** (design inside locked standards plus a checklist setup).

> Name this session `Calories Not Losing Weight LFC Setup`. Read and execute `Handoffs/handoff-20261002-ro10-thumbnails-and-video-setup.md`. Use the Codex subscription to generate the images: call Codex from the command line on Sol 6.1 at high effort. Make the five thumbnail options (one pool photo of me, one studio photo of me, three AI-generated images each with its own design that Codex chooses), show me the review sheet and stop for my pick. After I pick, run the upload and setup for RO-10 through Blotato without asking me anything else.
