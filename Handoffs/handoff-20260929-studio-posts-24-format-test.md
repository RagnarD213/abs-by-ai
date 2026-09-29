# Studio photo posts: 24-post format test

Date: 2026-09-29
Status: Ready for production in a new task.
Recommended model and effort: GPT-6 Astra / High.

## Objective and settled decisions

Create three complete organic Instagram posts in each of approved visual styles 01-08: 24 posts total. Deliver a review gallery, finished image files, captions, reusable templates and a proposed test rotation. Instagram is the primary layout; keep the assets reusable on other image platforms.

Dan liked all concepts except 09 and 10 and chose to test all of 01-08 before narrowing the selection. Do not reopen that decision or reduce the batch to the assistant's earlier four favorites. Styles 09 and 10 are excluded.

Latest direction, verbatim:

> Create a handoff document to make 3 posts in each style, 24 posts total, in a new task. In the new task just make a note to avoid posting the ones where I'm wearing a shirt and to only post shirtless images. Also, crop speedo images so it looks like I'm wearing regular shorts and not a speedo.

Create the complete batch for review. This request does not instruct immediate scheduling or publication. Once the finished batch is reviewable, any approval needed for publishing is one batch decision, not 24 separate requests. Do not touch the existing queue or create a dashboard row.

## Mandatory photo selection and cropping

- Only use genuinely shirtless source photographs of Dan. No shirts, tank tops, singlets or jackets in any image of Dan, including small insets and carousel slides. Text-only interior slides are fine.
- The original mockups for styles 03 and 07 used `studio-gray-31`, which has a white tank. Preserve their visual concepts, but replace that photo with a suitable shirtless source. Never use those generated mockups as finished posts. Do not digitally remove a shirt; select an existing shirtless photograph.
- Crop Speedo/briefs photographs so the final visible garment reads as regular shorts. For standing images, place the photo's bottom crop at the waistband's lower seam, immediately before the leg openings or brief silhouette begin at either hip. Retain as much waistband as possible. Inspect both hips on the final export.
- Dan's latest batch instruction takes priority over the older seated/lying exception in the shared rules. If a seated or lying Speedo image cannot be cropped cleanly for this batch, select a different shirtless image in real shorts. Do not expose the brief shape, cover it with text, or redraw briefs into shorts.
- Real shorts and jeans do not need this special crop. Keep a little headroom and all captured hair. Keep headlines, labels and design elements away from his face, hair and abs.
- Use warm, confident expressions. Avoid `Frowning Photos/` unless a specific negative story makes the expression appropriate.
- Preserve Dan's real face, age, skin, physique, proportions, pose, hands and clothing. Background changes and graphic layouts must not invent a different body or improve his muscles.

## Sources and approved visual references

Original project root, also usable as a read-only asset source from a worktree:

`/Users/danielrose/Documents/Claude/Projects/Abs By AI`

Reference directory:

`/Users/danielrose/Documents/Claude/Projects/Abs By AI/output/studio-style-gallery-20260929/`

- `index.html`: all ten concepts, rationale, research and reusable-format notes. Use 01-08 only.
- `overview.jpg`: numbered contact sheet.
- `images/01.png` through `images/08.png`: style references, not approved production photo layers.
- `concepts.json` and `prompts.json`: original descriptions, input filenames and generation prompts. Override the shirted inputs in 03 and 07.
- `sources/`: five source photos from the concept phase; one is shirted and is excluded.
- `studio-post-directions.zip`: portable complete reference package.

Cloud reference and backup, verified with anyone-with-link viewer access:

https://drive.google.com/drive/folders/1viqEH1bqYTnV9unmC1ZodGdROoH37wqz

Full finalized photo library:

`/Users/danielrose/Documents/Claude/Projects/Abs By AI/photos/finalized social media photos/`

Inspect the originals before choosing. Useful inspected shirtless candidates include `studio-blue-100_FINAL_PRIMARY.jpg` (glasses, white shorts), `studio-blue-247_FINAL_PRIMARY.jpg` (green shorts), `studio-blue-269_FINAL_PRIMARY.jpg` (Thai boxing shorts) and `studio-white-34_FINAL_PRIMARY.jpg` (jeans, arms raised). Many more poses exist. The concept folder's `sources-1.jpg`, `sources-2.jpg`, and `sources-3.jpg` summarize 96 studio originals. Avoid duplicate filenames ending in ` 2.jpg` when an original exists. Existing cutouts are under `_cutouts/`; verify quality and match them to the chosen originals.

Existing Speedo crops and crop metadata:

`/Users/danielrose/Documents/Claude/Projects/Abs By AI/photos/finalized social media photos/_speedo-crops-20260927/`

The gallery was visually checked, its image viewer and navigation worked, all ten previews loaded, and the Drive backup matched 12 delivered files. It was produced with the built-in image-generation tool. Generated previews can subtly redraw Dan, even concept 01. Use the original real photograph or verified cutout for the final person layer. No content was scheduled or published.

## Exact batch structure

| Style | Direction to preserve | Required posts |
|---|---|---|
| 01 | Original studio background, strong photographic crop, minimal treatment | 3 single-image posts |
| 02 | Warm neutral architectural backdrop, restrained editorial photography | 3 single-image posts |
| 03 | Believable training-space setting, matched perspective and light, shirtless replacement source | 3 single-image posts |
| 04 | Outdoor athletic setting that fits the clothing and pose | 3 single-image posts |
| 05 | Monochrome magazine-style personal feature with bold masthead and headline | 3 single-image posts |
| 06 | Pale blue, navy and cobalt topic cover with a clear short headline | 3 single-image posts |
| 07 | Practical, saveable educational carousel, shirtless replacement source | 3 complete carousels |
| 08 | Misconception and better alternative, followed by useful explanation | 3 complete carousels |

There are 18 single-image posts and six carousel posts. A carousel counts as one post, not one post per slide. Default to five slides per carousel: 48 exported images across 24 posts. Use another sensible slide count only when it materially improves the lesson; the post count remains 24. Every carousel must deliver its promised lesson, not just a cover.

## Production approach

1. Read the current `AGENTS.md`, `AI_COORDINATION.md` and `.claude/skills/_shared/VIDEO-RULES.md` from the original project. Claim only this batch's board entry. Read the applicable image-generation skill before generation. This is still-image production; do not run unrelated video gates or revive paused video work.
2. Inspect references 01-08 and shortlist eligible shirtless originals. Create stable IDs `S01-A` through `S08-C` and map each to source photo, topic and intended purpose. Favor distinct photos and meaningful topic variety while keeping the template stable within each style.
3. Build reusable layouts with separate person, background and editable text layers wherever practical. For photographic 01, retain original pixels. For 02-04, generate or replace the environment without regenerating the person, using the approved image tooling and preserving the original photo layer. Match lighting, scale and believable context. The user has already chosen these eight styles; routine production choices do not need another style-selection round.
4. Write useful, concise copy in Dan's voice, drawn from verified project material and his actual experiences. Do not invent autobiographical events, results, timelines, testimonials or statistics. Old Instagram captions are examples of published content, not a source of verified health claims. Do not reuse the abandoned free AI-preview funnel or its keyword CTA. AI generation remains a member feature.
5. Export sRGB 1080 x 1350 primary images, consistent dimensions within each carousel, plus reusable working files and a caption for every post. Avoid tiny supporting type. If a photograph needs a tighter Speedo crop, recompose the canvas around that crop without restoring the hidden briefs.
6. Inspect every exported image and all carousel sequences at phone size. Check subject fidelity, anatomy, shirtless-only selection, Speedo crops, hair, unobstructed face/abs, readable text, spelling, and a clear payoff for each carousel. Check new copy for both em and en dashes; neither is allowed.
7. Deliver a numbered 24-post gallery with clickable full images and complete carousel previews, captions, source mapping, template files and a downloadable package. Save in a new task-owned output folder such as `output/studio-post-test-24-20260929/`. Do not overwrite the initial gallery. Back up the deliverables to a clearly named subfolder on Drive with anyone-with-link viewer access and verify the uploads.

Use existing standing generation budgets. State estimated metered spend before a batch and track usage. Do not invent a dollar figure for built-in tool spend if it is not exposed. Do not switch generation providers or API routes against the installed image-generation skill.

## Test plan to include with the delivery

Prepare a proposed rotation through existing image-post slots, mixing all eight styles rather than publishing three of one style together. Keep topics reasonably comparable across formats, vary days, and give each style three attempts. Do not schedule it yet. This is a directional creative test, not a controlled causal experiment.

Include a blank results ledger keyed to post IDs, with publication date, platform/post URL, topic, source photo, style, reach, likes, comments, saves, shares, profile visits and follows where available. Compare after the same seven-day observation window. Use saves and shares relative to reach for educational content, and profile visits/follows plus reach for photography. Do not replace missing private metrics with guesses. Link attributable product trials or paying customers only when actual tracking supports it. No monitoring automation is requested.

Research already completed, no need to repeat a broad industry audit:

- Dan's recent grid: https://www.instagram.com/danrosefit/ . Pool photos and dark Reel covers dominate; most advice on stills is in captions. Public examples differed in age and topic, so do not call either a proven format winner.
- V Shred's practical carousel: https://www.instagram.com/vshred/p/DdtNV8DlxGs/
- V Shred's consistency post: https://www.instagram.com/vshred/p/Ddg62KzF78K/
- Noom's small-habit story: https://www.instagram.com/noom/reel/DdZ2vJYy99M/
- Cross-industry save-rate evidence: https://www.socialinsider.io/social-media-benchmarks/instagram-engagement-report . The May 2026 report analyzes 15 million posts; its 0.05% carousel and 0.02% single-image save rates are follower-based broad benchmarks, not a forecast for this account.

## Exact next action and starter prompt

Open the numbered reference gallery and finalized studio contact sheets, select eligible shirtless photos, then produce the 24-post batch and full carousels. The new task owns implementation; the current task only prepared this handoff.

Ready-to-paste starter prompt:

> Execute `/Users/danielrose/Documents/Claude/Projects/Abs By AI/Handoffs/handoff-20260929-studio-posts-24-format-test.md`. Create three complete organic posts in each of approved styles 01-08, 24 posts total, with full carousels for styles 07 and 08, captions, reusable templates and a review gallery. Use only existing shirtless photos of me. Replace the shirted examples in styles 03 and 07. Crop Speedo images at the waistband's lower seam before either leg opening is visible so they read as shorts; choose another source if that crop does not work. Preserve my real face and physique. Exclude styles 09 and 10. Prepare the complete batch for review without publishing or changing the queue.
