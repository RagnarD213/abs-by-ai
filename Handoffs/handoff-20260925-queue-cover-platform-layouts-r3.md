# Queue covers, round 3: separate Instagram and YouTube layouts

Prepared September 25, 2026. Dan reviewed the round 2 gallery and asked for a separate Instagram and YouTube version of each new cover in the next task. This is a layout and review pass. Do not change any publishing queue, installed cover, thumbnail, or schedule.

Recommended model: GPT-6 Astra, high effort. This work needs careful visual checks across two crops for every design.

## Read first

- Read `AGENTS.md`, `.claude/skills/_shared/VIDEO-RULES.md` in full, and `.claude/skills/coverimage/SKILL.md` in full before cover work.
- Read `Handoffs/handoff-20260925-queue-cover-revisions-r2.md` for the exact row copy, sources, and visual quality requirements.
- Round 2 review package: `/Users/danielrose/Documents/Claude/Projects/Abs By AI/Short-form video content/covers/review/queue-bakeoff-20260924/round2-20260925/`.
- Round 2 gallery: `index.html`; editable builder: `build_round2.py`; candidate inventory: `manifest.json`; source and retouch notes: `retouch-provenance.json` and `sources/`.
- Frozen current covers: sibling `baselines/` folder. The round 2 folder and its source files are Git ignored and shared from the original checkout. Use those absolute paths from a worktree.
- The crop failure is visible in `round2-20260925/instagram-grid-crop-check-04-05.jpg`. The new 04-A and 05-A headlines are cut off in Instagram's grid crop. Do not treat those as Instagram-ready files.
- Dan's row 11 black-gap screenshot is preserved at `revision-feedback-20260925/row11-youtube-black-gap-20260925.png` under the same review parent. Inspect it before building the YouTube layouts.

## Why two layouts

The established project rule is that Instagram's profile grid shows a centered 3:4 crop of a 1080 x 1920 Reel cover. It removes approximately the top 240 pixels and bottom 240 pixels. Keep all important text and face/body details inside the visible crop, with breathing room. The existing Instagram builder starts the type around y=240 and checks text placement. Its top reserved area need not be flat black; a photo or designed background may extend upward. Never put essential words in that top area.

YouTube Shorts uses the full vertical cover in the project's Shorts grid. Its existing builder starts type around y=96, fills the upper frame, and avoids a large empty black cap. Use the YouTube layout only for YouTube. The relevant project builders are `Short-form video content/covers/posted covers/_build-covers-batch2-final.py` and `_build-covers-youtube.py`. Do not copy the same crop blindly: a taller photo panel can make the photo crop narrower and cut off a head or arm.

Dan's new visual rule for the YouTube versions: fill the cover with the real subject image as much as the source permits. Remove unnecessary black space above, below, and especially between the headline and the photo. Move the photo panel up until it sits close beneath the last text line, then use a more vertical crop so Dan and the exercise occupy more of the 9:16 frame. Keep the full head, relevant equipment, abs, and enough body to understand the movement. Do not solve empty space by stretching a photo, inventing anatomy, putting words over Dan, or making a tiny image float in a black field. The Instagram version still needs its grid-safe text placement, but it may use photo or designed background in the reserved top band.

## Scope and Dan's latest feedback

- Give every round 2 candidate a distinct Instagram layout and YouTube layout. There are 25 round 2 candidates across rows 04-19, so the target is 50 vertical review exports. Keep the round 2 originals intact. Rows 01-03 still keep their existing covers and need no new design.
- Row 04: Dan prefers new A to the current original. Keep its real deadlift photo and wording. Put `LOOK AT THE CEILING` directly beneath `THE DEADLIFT TRICK THAT SAVES YOUR BACK`, following Claude's text grouping. Make a grid-safe Instagram version and a fuller YouTube version. Keep Dan, the kettlebell, his head, and his full action legible. A modest tighter crop is acceptable if it improves the frame without cutting those elements.
- Row 05: Dan paused before giving design revisions. Preserve its current round 2 source, copy, and overall direction while making the two platform layouts. Do not infer approval of 05-A or invent new copy.
- Row 11: Dan supplied a screenshot of `11-A` showing the large black gap under `WHY I LOVE THE AB WHEEL`. Treat that gap as a failure in the YouTube version. Keep the approved real standing ab wheel image and exact copy, bring the photo up directly under the headline with modest breathing room, and crop it more vertically so Dan, the wheel, and his abs fill more of the cover. Inspect the face, hair, wheel, and lower body after cropping. Apply the same no-dead-gap standard to `11-B` and the other YouTube designs.
- Rows 06-15 and 17-19: adapt the existing A or A/B candidate designs to each platform. Preserve exact copy and source choice from round 2 unless Dan supplies new feedback in the new task. The side/back rollout footage for rows 12-14 still cannot honestly show front-facing abs. State that limitation in the gallery and do not fabricate anatomy.
- Row 16 is currently a 1280 x 720 long-form YouTube thumbnail. Keep that wide file intact as the existing comparison. Dan asked for two platform versions of each candidate, so build portrait Instagram and YouTube review companions from its real pool scene and exact `2-minute home arm workout` wording. Do not stretch the wide image, invent extra body parts, or leave a tiny horizontal image in black space. Flag these portrait companions as review concepts rather than replacements for the wide long-form thumbnail.
- Do not publish, queue, install, or upload any of these covers until Dan chooses them.

## Build and review package

Save the new work in a sibling folder named `round3-platform-layouts-20260925/` under the same ignored review parent. Preserve scripts, inputs, and a manifest linking each row, design variant, platform, source, and output. Name files plainly, such as `04-A-instagram.jpg` and `04-A-youtube.jpg`.

Build a new browser gallery organized by row and candidate. Show the Instagram full cover, its actual centered 3:4 grid crop, and the YouTube full cover side by side at phone size. Include full-size links and the unchanged current cover for context. For row 16, show the unchanged wide thumbnail too. Make the platform difference immediately clear; do not combine the platform exports into a single image file.

Inspect every output at full size and phone size. Check exact copy, text safe area, face and hair, visible abs and exercise, complete equipment, natural retouch, and no text over Dan. Assert 1080 x 1920 RGB on the 50 portrait exports, verify all gallery links, and visually inspect each Instagram grid crop. Make an honest recommendation where the current original is still stronger. Keep all queues unchanged.

## Starter prompt for the new task

Read `Handoffs/handoff-20260925-queue-cover-platform-layouts-r3.md` and the required video and cover rules. Build separate Instagram and YouTube layouts for all 25 round 2 cover candidates, including row 04's requested text grouping and a clear Instagram grid crop preview. In YouTube layouts, move the photo close under the headline, crop more vertically where needed, and remove unused black gaps, especially on row 11. Preserve the existing covers and queues. Deliver the new side-by-side gallery for Dan to review, with full-size links and a frank note about rows 12-14 and the wide row 16 thumbnail.
