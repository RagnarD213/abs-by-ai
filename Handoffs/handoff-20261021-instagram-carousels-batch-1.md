# Instagram Carousels Batch 1: install C1 to C3, build 30 more, retire the studio batch

Date: 2026-10-21
Status: EXECUTED 2026-10-21/22 (phases 1-3). Dan's round 1 picks queued, studio batch retired (receipt `Docs/IG_TEMPLATE_QUEUE_RECEIPT_20261021.md`). Round 2 revisions are on https://claude.ai/artifact/7ykj2HXD1bpuFp9RGh7UzY, continuing in task "Instagram Carousels Batch 1 R2".
Type: organic Instagram and Facebook image posts (content, not ads).
Recommended model and effort: **Claude Opus 5.5, high** (design and editorial work, per memory `model-routing-plan`).
Every generated image goes through Codex on Dan's subscription: `.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high`.
Suggested task name: `Instagram Carousels Batch 1`.

## Dan's words (2026-10-21, verbatim)

> Okay, I like C1, C2, and C3. I like these. I want to post these particular ones, and I feel like they're good formats.
> I don't like C4 or C5. C4, I feel like, is a little too boring. C5, I feel like, is a little bit too much about me
> personally. There's not really a lot of reason for the viewer to care about that. For the singles, I don't really like
> any of these. Actually, the only one I like is the protein per 100 calories, but I feel like that just needs a small
> image of me added to it. That would be perfect for the protein per 100 calories. I like the cheat sheet format.
>
> 1. To install C1, C2, and C3 as our next three image posts.
> 2. To make 10 additional carousels in each of these formats.
> 3. Once we've chosen the ones that we have, to move all of our old content with that green format to the back of the
>    queue (basically, all that old stuff to the back, where we never release it unless we totally run out of stuff).
>    Probably, we never release it.

## What was decided (the template)

- Review page Dan approved from (all ten R1 mockups as real images): https://claude.ai/artifact/5GyikkcNzJSnkrpgKruXdb
- Design canvas with the source artboards: https://claude.ai/artifact/VxoxLtBBYkWLuKixTCSk3m . **It showed a black screen in
  Dan's side panel on 10-21** (the canvas reported no artboards in view and no errors; the files were intact). Do not send
  Dan to a Design canvas for review. Use a plain image review page like the one above.
- **Approved formats:** C1 The Fix (mistake, then fix, from real footage), C2 Receipts (a belief, the study, the verdict,
  what works), C3 Steal My Workout (one move per slide, recap card to screenshot), and the cheat-sheet single (P2,
  protein per 100 calories) once a small photo of Dan is added.
- **Rejected:** C4 Swaps (too boring), C5 Timeline (too much about Dan personally, no reason for the viewer to care),
  and the singles P1 Proof, P3 Straight Talk, P4 The Math, P5 Routine. Lesson: every post must give the viewer something
  to use. Dan's own story belongs only where it proves the viewer's takeaway.
- **The look (keep exactly):** ink `#0E1013`, bone `#F2EEE6`, red `#D33A2C` (mistakes, "old", the series square), yellow
  `#FFD23F` (fixes, highlights, last-slide asks). Anton for headlines, Manrope for everything else (Google Fonts).
  1080 × 1350 JPEG. Series tag top left, page count, @danrosefit on every slide. Headlines 70 px and up at 1080 wide,
  body 36 px and up, nothing under 32 px. Keep content out of the outer 34 px each side (the profile grid crops to 3:4).
  Real photos of Dan carry "Real photo of me, not AI-generated" (off face and abs); AI images carry "AI-generated image";
  slide 1 of a carousel is exempt. The last slide asks for one thing: save, send, comment on a specific question, or follow.
  Full sheet: `template.jpg` in the folder below.

## Files

Folder (git-ignored, holds shirtless photos; never commit it): `Short-form video content/instagram-danrosefit/template-r1-mockups/`

- Final JPEGs, ready to post: `C1-the-fix-01..05.jpg`, `C2-receipts-01..05.jpg`, `C3-steal-my-workout-01..05.jpg`,
  `P2-cheat-sheet.jpg`, plus the rejected ones for reference.
- `source/`: every artboard as HTML (`Main.dc.html` is C1, `C2-Receipts.dc.html`, `C3-StealMyWorkout.dc.html`,
  `P2-CheatSheet.dc.html`, ...) with the images beside it and an empty `support.js`. These render in plain Chrome.
- `full-boards/`: whole-board renders at 2x. `review-page.html`: the R1 review page source.
- Render recipe that produced the finals (headless Chrome, separate profile, needs network for Google Fonts):
  `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars
  --user-data-dir=<tmp>/chrome-prof --force-device-scale-factor=2 --window-size=<w>,<h> --virtual-time-budget=8000
  --allow-file-access-from-files --screenshot=<out>.png file://<source>/<file>.dc.html`.
  Carousel boards are `32 px padding, 540 × 675 slides, 24 px gap`; slide i crops at x = (32 + i × 564) × 2, y = 64,
  1080 × 1350.
- Real footage stills used: library clips B0430 (jump rope mistake, MISTAKE DEMO ONLY), B0448 (correct boxer skip),
  B0423, B0467, B0455; deck-chair before photo; studio cutouts `studio-blue-53`, `studio-white-90`.

## Phase 1: install C1, C2, C3 as the next three image posts (no stop)

1. Inspect the live Blotato queue first (Blotato MCP or the scripts). Expected state, verify it: the image slots are
   Mon/Wed/Fri 5 PM America/Chicago on Instagram @danrosefit (account `67203`) and Facebook Page Abs by AI (`47105`),
   filled by the 27 Codex studio posts Oct 21 to Dec 21 in the order in `Docs/STUDIO27_BLOTATO_QUEUE_RECEIPT_20261003.md`
   (2026-10-20 section). Never use the retired @abs.by.ai account `65632`. Save a dated before snapshot.
2. C1, C2, C3 take the next three unreleased image slots, in that order, on both platforms (expected Fri Oct 23, Mon
   Oct 26, Wed Oct 28). Each is one multi-image carousel post with its 5 slides in order. The studio posts that held those
   slots (expected S08-B, S09-A, S06-C) move to the end of the studio run, on the next free Mon/Wed/Fri 5 PM slots after
   Dec 21. Leave the Skip List carousel (Instagram, Sat Oct 24 noon) and every video untouched.
3. C3 timers: the slides say 1:00 per move, which was a placeholder. If Dan's starter prompt gives his real times, edit
   `source/C3-StealMyWorkout.dc.html` (the three `1:00` chips and the recap card), re-render, and queue that. If not,
   queue it as is and ask Dan once in the Phase 1 report; swap the media before its slot if he answers.
4. Captions: write them with the `dan-voice-writer` agent. First line repeats the hook with one fact from the post, the
   ask matches the last slide, at most 5 hashtags, and zero long dashes (run the project's dash scan on the text before
   queueing). The Receipts caption names the study (Vispute et al., Journal of Strength and Conditioning Research, 2011).
5. Run `scripts/blotato/ad_guard.py` (organic) before writing. Model the write on `scripts/blotato/skiplist_r2_queue.py`
   (single carousel) and `studio27_queue.py` (paired IG and FB, rescheduling). Record every upload URL, submission ID and
   schedule ID in a new state file, `scripts/blotato/igtemplate_state.json`, keyed so a retry never duplicates.
6. Re-read the whole queue after the writes: right account, time, caption, slide count and order; the three moved studio
   posts at their new dates; nothing else changed.
7. Receipt: `Docs/IG_TEMPLATE_QUEUE_RECEIPT_20261021.md`. Push scripts and Docs files with `scripts/git/safe-push.sh`
   the moment they change.

## Phase 2: the generator, 30 new carousels and the revised cheat sheet, then stop for Dan's picks

1. **Build the generator first** and make it a skill, `.claude/skills/instagram-posts/`: `SKILL.md` holds the template
   rules above plus Dan's format picks and rejections; `reference/` holds one HTML template per format (start from the R1
   source files, which Dan approved), a JSON content file per carousel, and one render script that writes the
   1080 × 1350 JPEGs and a contact sheet with the Chrome recipe above. The goal is that every future post is content in
   a JSON file plus one command.
2. **P2 cheat sheet:** add a small real photo of Dan (a studio cutout about a quarter to a third of the frame height,
   clear of the bars and numbers), labelled. Re-render. It goes on the review page for a quick yes.
3. **10 carousels per format, 30 in all.** Same structure as the approved one in each format, every slide with an image,
   copy in Dan's voice through `dan-voice-writer`, facts only from Dan (memory `dan-personal-facts-for-scripts`) or from a
   source shown on the slide. Never invent a number.
   - **The Fix (10):** one exercise mistake and its fix per carousel, both shown in real footage of Dan. Start from the
     top 7 mistake-and-fix Reels in the 2026-10-20 deep dive (memory `instagram-what-works-oct2026`; plan
     https://claude.ai/artifact/PDeJGz9Bvj3KQNg78CwgDL) and search the clip library first
     (`.claude/skills/_shared/cliplib/clip_library.py find`). Never fake a mistake: no AI image of Dan, no stick figures,
     no other person standing in for him. Where real mistake footage does not exist, still build the carousel with a
     clearly marked photo placeholder and add the exact shot to a "film at the next shoot" list for Dan.
   - **Receipts (10):** one popular belief per carousel, tested by a real study you have checked (authors, journal,
     year, what was measured, the result stated correctly). Verdict slide, a "what actually works" slide, Dan's real
     photo or fact only where it proves the point.
   - **Steal My Workout (10):** only routines Dan really does: his 10 weekly gym exercises, his 3-exercise ab workout
     (spiderman planks and V-sit twists are in it), his timer home workouts (Gymboss), his gym rep scheme (one warm-up
     set of 12 to 15, then two working sets of 6 to 10). Real footage of each move; gym moves have no footage yet (gym
     B-roll is planned for the next shoot), so use placeholders and add them to the shoot list.
   - Images: real footage and photos first; Codex for objects and food only, labelled. State the Codex image count
     before generating.
4. **Check every slide at phone size** (contact sheet at 270 px wide): sizes, nothing in the outer 34 px, labels
   present, no overflow, no long dashes. Rank the 10 in each format yourself and fix the weak ones before Dan sees them
   (memory `self-bakeoff-before-dan-reviews`).
5. **Review page:** a plain HTML artifact like the R1 page (one swipeable row per carousel, the revised P2, the shoot
   list, a short "What I decided"). Stop for Dan's picks. Do not queue any new carousel before he picks.
6. Phase 2 is large. If context passes about half, write a handoff per remaining format instead of pushing through.

## Phase 3: after Dan picks

1. Queue his picks (and P2 if he says yes) into the Mon/Wed/Fri 5 PM image slots right after C1 to C3, Instagram and
   Facebook, in his order, otherwise best first with the three formats alternating. Same verify and receipt steps as
   Phase 1.
2. **Retire the old studio batch.** "That green format" is read as the 27 Codex studio posts, the only older image posts
   left in the queue (the old pool-photo posts were deleted on 10-20; the Skip List carousel is a new navy design Dan
   approved, so it stays). If anything else in the queue is an old green design, include it and list it in the receipt.
   Take every still-unreleased studio post on both platforms off the schedule and record it in a reserve list,
   `scripts/blotato/photo_reserve.json` (media URLs, captions and hashes from `studio27_state.json`). The reserve is used
   only if the image queue would otherwise run dry. This frees up to 54 of Blotato's 200 slots for videos.
   **Dan authorized this batch in his message above;** do not ask again. Back up the queue first, never delete the
   studio image files or state, and re-read the queue after to confirm nothing else changed.
3. Records: add a section to the studio receipt, update memory `instagram-what-works-oct2026`, mark this handoff
   executed and remove its line from the OPEN list in `Handoffs/README.md`.

## Done means

- C1, C2, C3 live in the next three image slots on Instagram and Facebook, verified by re-reading the queue.
- The `instagram-posts` skill exists and renders a post from a JSON file in one command.
- 30 new carousels plus the revised cheat sheet on one review page; Dan's picks recorded.
- Picks queued after C1 to C3; the studio batch off the schedule and in the reserve list; receipts written and pushed.

## Ready-to-paste starter prompt

> Name this task "Instagram Carousels Batch 1". Execute `Handoffs/handoff-20261021-instagram-carousels-batch-1.md`.
> Phase 1 now: install C1, C2 and C3 as the next three image posts on Instagram and Facebook. C3 timer per move:
> [your real times, or leave as 1:00]. Phase 2: build the instagram-posts generator, make 10 new carousels each of
> The Fix, Receipts and Steal My Workout, add a small photo of me to the protein cheat sheet, and show me everything on
> one review page, then stop for my picks. Phase 3 after my picks: queue them after C1 to C3 and take the old Codex
> studio posts off the schedule into the reserve list. You are authorized for that whole batch.
