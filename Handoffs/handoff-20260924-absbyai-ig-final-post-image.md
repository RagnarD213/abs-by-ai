# Handoff 1 of 2: Build the image for the @abs.by.ai farewell post

**Date:** 2026-09-24
**Executor:** Codex, GPT-6 Sol / Medium (a small design job; Astra is not needed)
**Next handoff:** `handoff-20260924-absbyai-ig-final-post-and-shutdown.md` (Claude) runs after Dan picks an image.

## Goal

The Instagram account `@abs.by.ai` (66 followers) is being retired as a posting account. Everything now
lives on Dan's personal account `@danrosefit`. It will get one last post, pinned, telling people to follow
`@danrosefit`. This handoff builds **only the image** for that post. Do not publish anything, do not touch
Blotato, do not touch Instagram.

## Decisions already made (do not reopen)

- The `@abs.by.ai` account is **kept, not deleted or deactivated**. It stops posting, gets a "we've moved"
  bio, and this post is pinned. Dan approved this plan on 2026-09-24.
- Real photography of Dan, never a video frame. Abs clearly defined, upright posture, no hunched or soft
  frames (memory `cover-photo-selection`). Never a frowning photo as the default (the `Frowning Photos/`
  subfolder is off limits).
- Brand style (memory `thumbnail-design-system`): white Manrope ExtraBold caps headline, red accent bar
  `rgb(201,48,45)`, dark `rgb(5,7,11)` tones, legibility from a gradient scrim, **never a blur**. The photo
  fills the frame; no big black slab. Text never overlaps the abs. Manrope is at `~/Library/Fonts/Manrope.ttf`;
  the variable font defaults to ExtraLight, so call `set_variation_by_name("ExtraBold")`.
- **No em dash and no en dash anywhere in the image text** (Dan's standing rule).
- No claims (no "lost X lbs", no results promise). This is an announcement, not an ad.

## What to build

**Format:** 1080 x 1350 (Instagram 4:5 portrait), sRGB JPEG, quality 92+. Also check it reads correctly
in the 3:4 profile grid crop (1080 x 1440 centre view): the headline and `@danrosefit` must survive that crop.

**Copy (use this, do not rewrite it):**
- Headline: `WE'VE MOVED`
- Handle, large and the most readable thing after the headline: `@danrosefit`
- Small line: `Follow Dan for the workouts, the food and the AI tools.`
- Optional small Abs By AI logo, white. Logo candidates: `logos/`, `public/img/logo.png`,
  `Media/video_edit/work/logo_white*.png`. The dark logo artwork must be recolored white keeping alpha or it
  vanishes on dark backgrounds.

**Source photos:** `photos/finalized social media photos/`. The `*-IG-4x5.jpg` files are already cropped
to 4:5. Good starting candidates: `Dan-flag-FINAL-IG-4x5.jpg`, `photo-103/106/107/111/113_FINAL_PRIMARY-IG-4x5.jpg`,
`dan-pool-shoot-towel-smile-retouched-final.jpg`. Look at each; pick ones where he is smiling or neutral and
the abs are defined. `photos/` is gitignored because it holds shirtless photos of Dan: **never commit these
images or the outputs to git** (the repo is public).

**Deliver three variants** (A, B, C) so Dan can pick:
- A: headline top, handle bottom, photo full bleed with top and bottom scrims.
- B: a different photo, same layout.
- C: your best alternative layout (for example a solid lower band carrying the text), still on brand.

## Output

Folder: `social media graphics/instagram/abs-by-ai-final-post/` (gitignored, create it).
- `final-post-A.jpg`, `final-post-B.jpg`, `final-post-C.jpg`
- `contact-sheet.jpg`: all three side by side, labeled A / B / C, for Dan to look at on his phone.
- `build.py`: the script that builds them, so a one-word change can be re-rendered.
- `README.md`: which source photo each variant used, and the exact text used.

Upload the three variants plus the contact sheet to a Google Drive folder named
`Abs By AI - IG farewell post`, set to **anyone with the link can view** (Dan's rule, memory `drive-always-public`),
and put the folder link in the README.

## Verification before you finish

1. Open every output and look at it: text crisp, nothing overlaps the abs, no cut-off letters, handle spelled
   `@danrosefit` exactly.
2. `grep -c $'\u2014' README.md` returns 0, and no em or en dash appears in the image text.
3. `git status` shows nothing from `social media graphics/` or `photos/` staged.

## Finish

- Tell Dan in plain language: the three variants, the contact-sheet path, the Drive link, and the one choice
  he needs to make (A, B or C).
- Update `Handoffs/README.md` and the HANDOFFS section of `AI_COORDINATION.md`: mark this one done
  (delete its line) and leave handoff 2 as "ready once Dan picks A/B/C". Commit only those two files plus
  this handoff; push to `main`.


## Completed 2026-09-24

Three 1080 x 1350 sRGB JPEG variants and the labeled contact sheet were built and visually checked, including the 3:4 center crop. A uses the smiling towel/pool portrait; B uses the flag portrait; C groups the announcement below the torso on the flag portrait. Recommendation: A.

Local delivery: `social media graphics/instagram/abs-by-ai-final-post/`. Rebuild recipe and exact source/copy records: `build.py` and `README.md` in that gitignored folder. No photographs or generated outputs were added to Git.

[Public Drive folder](https://drive.google.com/drive/folders/1iE7KxVSUZhHoGhU7DL3HvqXUCBMUqPOv) contains A/B/C and the contact sheet. Anyone with the link can view. Nothing was published or scheduled. Handoff 2 is ready once Dan picks A/B/C.


## Revision 2 delivered 2026-09-24

Dan preferred original A, requested headline `I've moved.` and supporting copy `Follow me there to get my workouts, nutrition tips, and life updates`, and asked for four options. Revised A uses the original smiling pool photo; B uses a different pool portrait; C uses a smiling studio portrait on dark blue; D is an AI-assisted editorial composition with cream/red art direction. The handle remains `@danrosefit`.

Latest files and rebuild recipe: `social media graphics/instagram/abs-by-ai-final-post/revision-2/`. [Public revision-2 Drive folder](https://drive.google.com/drive/folders/1ALQ-KZfEmGc0_7S-9EpBHwH0Z1PrqKqM). All four 1080 x 1350 sRGB JPEGs and the contact sheet delivered. Full images and 3:4 grid crops checked. Nothing published or scheduled. Await Dan's final revision-2 A/B/C/D choice; original A preference is not final approval of a revision.
