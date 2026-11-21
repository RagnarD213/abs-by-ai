# Queue cover and thumbnail redesign bake-off

Prepared September 24, 2026. This is a design handoff for a new task. No queue image was replaced in this task.

Recommended model: **GPT-6 Astra, high effort.** This is a large visual design and source-selection job with 19 comparisons and 76 new candidates.

## Goal

Try to beat every existing cover and thumbnail that Dan reviewed on September 23, excluding the five Shorts already redesigned. For **each of the 19 existing images below**, create four finished alternatives:

1. **Pool photo shoot:** use Dan's real pool shoot.
2. **Studio plus topic background:** use a real studio cutout of Dan with a topic-specific designed background, following the approved Jelly Beans visual approach.
3. **Screenshot:** choose and refine the strongest real frame from the finished video, with readable cover typography where it helps.
4. **Open creative choice:** use the image most likely to win. Dan explicitly permits a non-Dan person, a licensed stock image, an AI-generated image, a graphic concept, or a combination of approaches for this option. Make a meaningful concept, not a minor variation of the first three.

The target is **19 five-column comparisons**: existing image plus four alternatives, **76 new candidate renders**. Keep every row tied to the actual video's subject and promise. Use different visual ideas across the batch so the result is not one template repeated 76 times. Show all finished comparisons to Dan in one navigable gallery, with phone-size previews and full-size access. Recommend the strongest candidate for each row, including the existing image if it remains better. Dan will choose replacements after review. Do not install or publish candidates as part of this design task.

## Frozen baseline and scope

The September 23 live-queue audit is preserved in:

`Short-form video content/covers/review/queue-bakeoff-20260924/baselines/`

Absolute path in the shared checkout: `/Users/danielrose/Documents/Claude/Projects/Abs By AI/Short-form video content/covers/review/queue-bakeoff-20260924/baselines/`. Use that path if the new task runs in a separate worktree. It contains all 19 baseline JPGs, `inventory.json` with the image source URL, scheduled dates, account names and post or video IDs, and two contact sheets. This directory is Git-ignored because it holds Dan's image assets. The original gallery is at `/Users/danielrose/.codex/visualizations/2026/09/23/01a0cfa3-f5f8-7f02-9795-647d2775cf06/queue-covers/index.html`.

The five excluded YouTube Short IDs are `tqURi3qdrIc`, `_Ep_hVPZYzE`, `o1v3wPkNI2I`, `QuswpGj635A`, and `bi_fpkW-3eE`. Their approved redesigns have their own installation work. Do not include or alter them.

Blotato mirrors appear once per distinct cover. The arm workout appears twice because it has separate Blotato and YouTube records. The deadlift, towel and three-minute videos also have separate YouTube previews. Preserve those separate comparisons because the current YouTube previews differ visibly from the designed Blotato covers.

| # | Queue | Subject | Baseline file | Current pixels | Post or video ID |
|---|---|---|---|---|---|
| 01 | Blotato | Why I skip breakfast every single day | `blotato-01.jpg` | 1080 x 1920 | `3876744` |
| 02 | Blotato | Belly fat affects far more than the mirror | `blotato-02.jpg` | 1280 x 720 | `4578150` |
| 03 | Blotato | Arm workout before every photo shoot | `blotato-03.jpg` | 1280 x 720 | `4722757`, `4722761` |
| 04 | Blotato | Deadlift trick that saves your back | `blotato-04.jpg` | 1080 x 1920 | `4066393`, `4066405` |
| 05 | Blotato | Back move with a towel | `blotato-05.jpg` | 1080 x 1920 | `3793992`, `3794055` |
| 06 | Blotato | You always have three minutes | `blotato-06.jpg` | 1080 x 1920 | `4066416`, `4066422` |
| 07 | Blotato | Train all four ab muscles | `blotato-07.jpg` | 1080 x 1920 | `3793994`, `3794057` |
| 08 | Blotato | Toe touch for lower abs | `blotato-08.jpg` | 1080 x 1920 | `3793995`, `3794058` |
| 09 | Blotato | V-sit twists for obliques | `blotato-09.jpg` | 1080 x 1920 | `3793997`, `3794060` |
| 10 | Blotato | Spiderman planks | `blotato-10.jpg` | 1080 x 1920 | `3793998`, `3794061` |
| 11 | Blotato | Why I love the ab wheel | `blotato-11.jpg` | 1080 x 1920 | `4315883`, `4315885` |
| 12 | Blotato | Biggest ab wheel mistake | `blotato-12.jpg` | 1080 x 1920 | `4315887`, `4315890` |
| 13 | Blotato | How far to roll out | `blotato-13.jpg` | 1080 x 1920 | `4315893`, `4315895` |
| 14 | Blotato | Roll the ab wheel slowly | `blotato-14.jpg` | 1080 x 1920 | `4315898`, `4315901` |
| 15 | Blotato | Why the ab wheel beats crunches | `blotato-15.jpg` | 1080 x 1920 | `4315903`, `4315906` |
| 16 | YouTube | Home arm workout | `youtube-01.jpg` | 1280 x 720 | `QHWOoWbgWcY` |
| 17 | YouTube | Deadlift trick that saves your back | `youtube-02.jpg` | 1280 x 720 preview | `D9v9POAKe_Q` |
| 18 | YouTube | Back move with a towel | `youtube-03.jpg` | 1280 x 720 preview | `qH9YRoH2PpM` |
| 19 | YouTube | You always have three minutes | `youtube-04.jpg` | 1280 x 720 preview | `1k518M3EKps` |

Rows 02, 03 and 16 are horizontal long-form designs. Make their candidates 1280 x 720 or higher at 16:9. All other rows are Shorts/Reels. Make those candidates 1080 x 1920 at 9:16, **including YouTube rows 17 to 19**. The YouTube API returned 16:9 preview frames for those Shorts; that is the current baseline, not the shape to design for.

## Sources and design rules

- Read `AGENTS.md`, `.claude/skills/_shared/VIDEO-RULES.md` in full, and `.claude/skills/coverimage/SKILL.md` before building. Dan's four requested routes override the skill's usual two-variant output. The standing rules on hair and face clearance, truthful imagery, and no em dashes remain in force.
- Pool and studio photographs: search `photos/finalized social media photos/` by contact sheet and inspect the actual full-resolution file. Do not use dating-app photos. Select a real image where Dan's physique, expression and crop work at phone size. Do not AI-repaint Dan or substitute an AI face for a real portrait.
- Jelly Beans reference: `Short-form video content/covers/review/jelly-bean-refresh/B3-approved-upload.jpg` and `build.py` in that folder. Keep its useful principles: a strong real studio cutout, topic-specific background, short high-contrast headline, and a clear upper band. Adapt props and color to each video.
- Screenshot route: locate each video's **finished edited export**, extract several sharp frames that actually illustrate the topic, and pick the best expression/action. Do not pull a raw or ungraded camera frame merely because it is easy. A screenshot candidate should be polished enough to compete, not a token frame grab.
- Open creative route: Dan permits non-Dan subjects, stock, AI imagery and bolder compositions. Use Pexels or assets with known usage rights, or approved AI generation. Record each image's source and whether it is AI-generated. Do not imply that another person's body is Dan's or present a fabricated transformation as a real result.
- Text must be readable at phone size and clear of Dan's face and hair. Do not add `AbsByAI.com` or the small real-photo disclaimer to covers. Avoid frowning Dan photos for upbeat topics. A before/after comparison uses the same person on both sides.
- This is a still-image design task. The video-specific AI motion frame-approval rule does not turn a still cover into a motion task. Estimate metered image-generation cost before any batch, track actual spend, and respect the project's $15 single-batch and $25 session approval boundaries.

## Execution and review

1. Recheck the live queue before work so changed dates or removed posts are recorded. Keep the 19 frozen baselines as the comparison set Dan requested, even if a post has since published. Do not overwrite another session's active cover work; check `AI_COORDINATION.md`.
2. Inspect the finished videos, pool shoot, studio shoot, available cutouts and Jelly Beans reference. Make a concise visual concept for each of the four routes per row, then build the actual images. Use image generation where it genuinely improves the design, and local layout/compositing for accurate text and real Dan photography.
3. Save candidates and provenance under `Short-form video content/covers/review/queue-bakeoff-20260924/`. Name each file by row and route, for example `04-pool.jpg`, `04-studio.jpg`, `04-screenshot.jpg`, `04-creative.jpg`. Preserve the original source files and rendering recipe or script so approved work can later be reproduced.
4. Render a five-column sheet for **every row** in the order Existing, Pool, Studio, Screenshot, Creative. Use identical displayed dimensions within each row, a legible title, route labels, and both 9:16 or 16:9 phone-size previews as appropriate. Provide a navigable HTML gallery plus contact sheets and links to full-size candidates.
5. Review every image at full size and at phone size. Check text spelling, face and hair clearance, physique crop, true subject match, safe area, image quality, aspect ratio and source provenance. Do not present a route as finished if the asset is missing or malformed.
6. Show Dan all comparisons and a short recommendation per row. State where a candidate is genuinely better and where the existing image still wins. Keep all queue images and schedules untouched until Dan selects replacements.

## Exact next action

Start a new task with the prompt below. First inspect the 19 preserved baselines and the current coordination board, then build the four alternatives for each row and deliver the side-by-side gallery.

## Ready-to-paste starter prompt

> Read `Handoffs/handoff-20260924-queue-cover-thumbnail-bakeoff.md` in the Abs By AI project and execute the complete 19-image cover and thumbnail bake-off. For every preserved existing image, make four finished alternatives: pool shoot, real studio cutout with a topic-specific Jelly Beans-style background, a polished screenshot from the finished video, and your strongest unrestricted creative idea. Non-Dan, licensed stock and AI-generated images are allowed for the creative route. Show each existing image beside all four candidates at full and phone size, recommend a winner for each, and preserve source provenance. Exclude the five already redesigned Shorts. Do not replace queue images yet.
