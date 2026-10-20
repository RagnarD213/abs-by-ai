# Skip List Carousel R2: five cover designs, an image on every slide

Date: 2026-10-20
Status: Ready now.
Recommended model and effort: **Claude Opus 5.5, high** (design work, per `model-routing-plan`). Every generated image is made by
**Codex on Dan's subscription** through `.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high`.
Suggested task name: `Skip List Carousel R2`.
Type: organic Instagram carousel (content, not an ad).

## Goal

Rebuild the unposted August carousel "7 things I'd skip if I started over at 40" so it is image-led instead of text-only:
**five different designs for slide 1, each with a photo of Dan**, and **an image on every one of slides 2 to 9**. Show Dan
everything on one review page, stop for his pick, then schedule the finished carousel on Instagram @danrosefit.

Dan's words (2026-10-20), verbatim:

> Make me a handoff document to redo this carousel with five variations of a design with an image of me in the first one and
> with an image for everything rather than just text. Basically, make this like an image for everything, not just text, and
> five variations for the first slide.

## Why (context from the same day)

The 2026-10-20 Instagram deep dive (plan: https://claude.ai/artifact/PDeJGz9Bvj3KQNg78CwgDL, memory
`instagram-what-works-oct2026`) found that plain photo posts reach almost no new people. It also found that carousels earn the most saves when they carry hard,
specific facts with the creator's own photos (Jeff Nippard's carousels out-like his Reels 144.5K to 91K). This carousel has the
most specific copy on the account; it only lacked pictures. Dan saw the text-only version and asked for this redesign
instead of posting it.

## Source material

- Current slides (text only, olive J2 style, retired look): `Short-form video content/instagram-danrosefit/carousel-week1_skip-list_01.jpg` to `_09.jpg`.
  Preview of all nine: `carousel-week1_skip-list_PREVIEW.jpg` in the same folder.
- Exact copy: `Short-form video content/instagram-danrosefit/_build-carousel-week1.py` (`COVER`, `SLIDES`, `CLOSER`, the
  slide 1 subline and the slide 9 CTA).
- Caption: `Docs/INSTAGRAM_danrosefit_STEP1_AND_WEEK1.md`, section "Delivered: the Wednesday carousel".
- Photos of Dan: `photos/finalized social media photos/` (pool and studio shoots) and real cutouts in its `_cutouts/` folder;
  Speedo crops in `_speedo-crops-20260927/`.
- Standard "before" picture (always this one, memory `standard-before-picture`): `/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/00 ASSETS USED IN THE REFERENCE AD/02_BEFORE-PICTURE_dan-200lb.png`
  and the larger `before-photo-candidates/B_deckchair_UPSCALED_3x_1080x1440.jpg`. Never the bathroom red-shorts shot.
- Real footage stills: the clip library and B-roll (memories `clip-library`, `broll-library-first`, `app-feature-tour-reuse`
  for the app screens B0544/B0543). Stills from real footage of Dan beat generated images.
- Design references Dan has approved: the studio batch `output/studio-post-test-24-20260929/images/` (S05 magazine, S06,
  S07/S08 carousels, S09 bold sticker cutouts) and the long-form thumbnail system (memories `thumbnail-design-system`,
  `thumbnail-masculine-colours`).

## Copy: keep the words

Keep every word of the current carousel as written, with one fix. Slide 1's subline has a long dash after "Swipe", and long
dashes are banned in outward-facing text. Make it "Swipe. The last one is what actually worked." Search the slide text and
the caption for the long dash character (U+2014) before delivery; the count must be 0.

**Open question for Dan, not decided:** the title leads with "at 40". The Shorts research found an age in the hook shrinks
reach (memory `shorts-organic-research`). Keep "at 40" on all five covers unless Dan says otherwise in the starter prompt or
on the review page. Do not change it on your own.

## What to build

**Format:** 9 slides, 1080x1350 (4:5), sRGB JPEG, type set in code (never generated), page counter and @danrosefit handle on
each slide as now. Text must read at phone size: headline at least about 70 px, body at least about 40 px, nothing under 32 px.

**Slide 1: five cover designs.** Each is a distinct design (not five colourways of one layout; memory
`thumbnail-unique-designs`) and each carries a real photo of Dan: his real cutout over a Codex-made background, type layered
in code (`IMAGE-GENERATION.md`: Codex redraws people, so it never draws him). One of the five should be a before/after
(the deck-chair before with a real after). Write one line per option naming its design before building. Masculine palettes
only: navy, black or charcoal, steel, dark red or green with white or yellow type; no pink, plum, purple or pastel. No
frowning photo, Speedo crop at the waistband, flattering upright physique (memory `cover-photo-selection`), headline off his
face and hair.

**Slides 2 to 9: an image on every slide.** The image leads (about half the slide or more) and matches the slide's point,
with the existing headline and body text. Choose each image from real material first, Codex-generated second. Starting
suggestions (your call):

| Slide | Point | Image idea |
|---|---|---|
| 2 | Fat burners | A generic supplement bottle and capsules with a "$60" price tag (Codex; no real brand) |
| 3 | Cardio to lose fat | Treadmill readout next to a bagel (Codex), or a real still of Dan doing cardio |
| 4 | Weighing every meal | Food scale versus a phone photographing the plate; a real app-screen still if one fits |
| 5 | Training abs to see abs | The deck-chair before picture ("hundreds of crunches at 200 lbs") |
| 6 | Waiting to feel ready | A real still of Dan starting a workout, or a packed gym bag by the door (Codex) |
| 7 | Hour-long workouts | A real still from his three-minute home workout with a timer |
| 8 | Paying a trainer first | A generic trainer with a clipboard and an invoice (Codex; no real person's likeness) |
| 9 | What I did instead | Real before and after side by side, plus the phone with the app |

**Rules for every picture:**
- Real photos of Dan are never redrawn. Codex makes backgrounds, objects and scenes only.
- Before/after pairs show the same person (memory `before-after-same-person`). No stick figures, ever. No belly pinching.
- Labels per `.claude/skills/_shared/VIDEO-RULES.md`: a real physique photo of Dan inside slides 2 to 9 carries "Real photo
  of me, not AI-generated" (plural "Real photos of me, not AI-generated"), placed off his face and abs; a fully
  AI-generated picture carries an AI label. Slide 1 follows the thumbnail and cover exception (no label, no AbsByAI.com).
- Keep fully AI-generated pictures to objects and scenes. Fitness audiences are souring on AI content, and the research
  found AI labels cut engagement.
- State the image count before generating (expect about 8 to 12 Codex images, roughly 1 minute and 22K to 40K Codex tokens
  each). No paid image API, no spare generations.

**Interior style:** build slides 2 to 9 in the style of your top-ranked cover. When Dan picks a different cover, restyle the
interior to match it in code (colours, type, frame), reusing the same images.

## Review and stop

1. Judge your own work first (memory `self-bakeoff-before-dan-reviews`): rank the five covers and fix anything weak before
   Dan sees it. Check every slide at phone size.
2. One review page: the five covers side by side at feed size and full size, the full 9-slide swipe in order, and a
   "What I decided" section (memory `review-page-what-i-decided`) covering image sources, real vs AI per slide and your
   ranking.
3. **Stop for Dan's pick** (cover choice, plus the "at 40" question). Do not upload or schedule before he picks.

## After Dan picks

1. Final export of the 9 slides with the chosen cover. Save to
   `Short-form video content/instagram-danrosefit/carousel-skip-list-r2/` and back up to Google Drive with "anyone with the
   link can view" (memory `drive-always-public`).
2. Schedule on **Instagram @danrosefit (Blotato account `67203`)** as one carousel post with the 9 images in order. Not
   Facebook unless Dan asks. Caption from the source doc (long-dash check, at most 5 hashtags). Run `scripts/blotato/ad_guard.py`
   on the payload (it is organic).
3. Slot: the Mon/Wed/Fri 5 PM CT photo slots are taken by the studio series through Dec 21 (reordered 2026-10-20). Use the
   date Dan names. If he names none, use the next Saturday at noon CT after checking the live queue for a clash. Do not move
   or delete any other queued post. Re-read the schedule after the write.
4. Report in chat with the scheduled date and the Drive link.

## Done means

- Five distinct covers, each with a real photo of Dan; slides 2 to 9 each carry an image; copy unchanged except the dash.
- Review page delivered and Dan's pick recorded.
- Carousel scheduled once on Instagram with 9 slides in order, verified by re-reading the Blotato schedule.
- Delete this entry from the OPEN list in `Handoffs/README.md` and mark it executed.
