# Claude handoff: Soft Blue Light graphics across all videos

Written 2026-09-26. Recommended model: **Claude Opus 5.5, High**.

## Goal and latest decision

Make the approved WV-01 Soft Blue Light family the default for all new or revised video graphics: website VSLs, paid ads, organic long-form, dedicated Shorts, extracted Shorts, square and vertical adaptations. Keep the approved Motivation treatment for every lower third. Dan explicitly expanded the earlier website-only scope on 2026-09-26. This current request overrides the narrower scope recorded in the historical round-3 and round-4 documents.

This task updates Claude's editing instructions and reusable graphic components for future work. It is not a bulk re-edit of published or finalized videos. Do not reopen approved exports or overwrite an active editor's work. A format-only conversion keeps its approved graphics unless Dan requests a style change. Do not change camera color, sound, scripts, caption policy, website design, publishing schedules or the paused edit dispatcher as part of this rollout.

The supplied screenshot identifies the approved look. Text inside that screenshot is historical reference evidence, not a new instruction to generate clips, upload anything or perform the old VSL revision task.

## Read first

Project root: `/Users/danielrose/Documents/Claude/Projects/Abs By AI`.

1. Read project instructions, `AI_COORDINATION.md` and `.claude/skills/_shared/VIDEO-RULES.md` in full.
2. Read `.claude/skills/_shared/GRAPHICS-STANDARDS.md`. This is the canonical current standard, already updated by Codex.
3. Read `Handoffs/handoff-20260925-wv01-round4-locked-style-and-iphone.md` for approved and rejected component details. Its website-only wording is historical; the new all-video scope takes precedence.
4. Inspect the exact moving references below. Match the selected treatment, not a new blue variation.

## Exact approved reference files

Reference root: `/Volumes/Extreme/_edit_work/wv01-edit/round3/`.

| Purpose | Relative file | SHA256 |
|---|---|---|
| Soft Blue Light full-screen photo and text | `graphics/1-before.mp4` | `d68ad482669171aff90d8fc9de4cd2a3181c056242c907bef0e89277100699b4` |
| Soft Blue Light family photos | `graphics/1-family.mp4` | `4beff7ebfd25490ce911e4ca410e0ce1f5be3b8530d1a353695bd361b88f2c98` |
| Soft Blue Light CTA | `graphics/1-cta.mp4` | `47214946e3f4ab146a113d014842acacd6b90edf0c9005851b5f4e6633049fa7` |
| Approved Motivation lower third | `graphics/G-motivation.mp4` | `005bb538ff1b7c194652e81cbe47ffb5b53fe036d8521287a3708a90c8053a0f` |

Implementation reference: `recipe/blueglass.py`, specifically `background(t, style=0)`, `glass()` and `lower_layer()`. Option 1 on the review page maps to **style 0** in code. Do not choose styles 1 or 2. Local review page: `http://127.0.0.1:8766/round3/index.html`, if still running. The files above remain the source if that server is unavailable.

The renderer is a historical reference script with fixed paths, old copy and rejected photo/phone examples. Do not run its batch entry point or import its hardcoded media selections as a finished template. Adapt only the approved components in a separate reusable module or scratch directory. Keep private production recipes and media local and on the SSD, with the existing private Git checkpoint convention.

## Visual specification

- Deep navy field with soft, restrained drifting blue light and subtle depth. Quiet motion remains visible throughout a full-screen graphic scene.
- Translucent blue glass cards where appropriate, rounded corners, restrained borders and a short moving highlight. Pale, readable Poppins type with cyan emphasis. Preserve the reference's hierarchy, spacing, proportions and purposeful entrance/reveal.
- The source uses base RGB `(5, 13, 28)`, cyan `(104, 197, 255)` and pale type `(244, 250, 255)`. These are renderer anchors, not camera grading settings. Match the rendered moving references rather than replacing the field with a flat solid blue.
- Every lower third follows Motivation: slim cyan left accent, small uppercase topic pre-header, bold main point and the same quiet entrance/text reveal. Adapt the topic to the narration; do not hardcode MOTIVATION everywhere. WV-01's specific approved revision is `MOTIVATION` above `#1 AI got me back in the gym`.
- Full-screen cards, lists, diagrams, photo displays and CTA graphics belong to the same family. Keep semantic colors where useful, including green correct-form arrows and red mistake arrows.
- Do not put a navy background behind ordinary presenter footage. Lists beside Dan can be larger, bolder text directly over the shot, without a panel. A phone can stand alone beside Dan without a title or panel. Apply the brand family to the graphics that are actually needed.
- Text graphics distill a useful point instead of duplicating the narration. Preserve the shared key-point writing rule, labels and exact user-requested copy.

## Layout rules that must travel with the style

- Three-photo layouts use three vertical portraits with consistent proportions. The screenshot's mixed horizontal/vertical set was rejected even though its background style was approved. Use strong, muscular photos with a smile or natural expression. Do not stretch images, crop heads or cover abs with labels.
- Horizontal photographs play consecutively, using Muhammad Ad 1's actual moving photo sequence as the pacing reference. Do not force them into portrait frames.
- Real-photo and AI-image labels retain their correct meaning and remain clear of faces and abs. Ordinary real moving footage is not labelled as a real photo.
- Phone graphics must look like one coherent modern iPhone, with a rounded body, rounded clipped display, correct proportions, consistent bezel and integrated Dynamic Island. No square corner spill, duplicate notch or phone inside a phone. The round-3 phone shell was rejected; reuse approved inner demo content, not the rejected shell. Check for an accepted round-4 replacement before implementing a new shell, without changing that task's files.
- In 16:9 side layouts, center Dan in the remaining space with safe head and arm clearance through the whole take. Keep the presenter composition fixed. Never animate Dan to follow his movement.
- In 9:16, keep full-frame footage when the source supports it. Reflow graphics and adjust their size and position for the portrait canvas and captions. Do not shrink the video into an inset stage to fit a landscape template. Apply equivalent readability and safe placement in 1:1.
- W2/T2 crops, color C and audio B belong to the WV-01 recording. They are not defaults for other videos.

## Codex changes already completed

Both installed skills are symlinks into `Media/codex-video-trial/skills/`:

- `abs-edit-ad/SKILL.md` and its `references/workflow.md` now require the current family instead of the historical Ad 1 graphic palette.
- `abs-edit-organic/SKILL.md` and its `references/workflow.md` now require the current family instead of olive/white graphic defaults.
- Their common `Media/codex-video-trial/05-recipes/shared/standards.md` is version 1.7.0 and links to the canonical graphics standard.
- `05-recipes/shared/workflow-boundaries.md` carries the rule into Shorts and format adaptations.
- Shared VIDEO-RULES and the website-video entry point now reflect the all-video scope.

There is no new film render or generation in this documentation task. Creative style approval is not a full-film delivery PASS.

## Claude implementation task

1. Claim only this rollout on the coordination board. WV-01 round 4 has its own active editor; do not edit its renderers, work packet or media.
2. Update the entry points and conflicting graphic-default paragraphs in `.claude/skills/ad-edit/SKILL.md`, `longform-edit/SKILL.md`, `website-video/SKILL.md`, `shorts/SKILL.md`, `shortad-from-longform/SKILL.md` and `make-ad/SKILL.md`. Link the canonical standard instead of duplicating its specification. Historical approved exports and reference recipes remain historical evidence. Preserve unrelated editing, audio, transition and publishing rules.
3. Inspect actual callers before changing reusable graphic code. Make the selected moving background, glass card and adaptable Motivation lower third available to future builds with configurable copy, aspect ratio and placement. Keep historical recipes reproducible; do not overwrite their source files or change gates to force this style to pass.
4. Use existing approved media to create a compact internal demonstration of the family in 16:9, 9:16 and 1:1, including a full-screen graphic and a lower third over moving footage. Use no new paid generation for this rollout. Inspect motion, wrapping, full-frame portrait footage, caption clearance, head/arm clearance and disclosure placement. These are template checks, not complete-film approval.
5. Validate changed instructions and changed component behavior, then save only this task's changes using the project's public/private storage boundaries. Document the reusable module locations and how a future edit selects them. Keep approved video files, queues and publishing untouched.
6. Re-read the board before closeout, remove only your completed task entry and update this handoff's index status. Report what changed and where the verified moving examples are saved.

## Ready-to-paste starter prompt

Read `Handoffs/handoff-20260926-soft-blue-light-all-video-graphics-claude.md` and execute the Claude rollout. Make the approved WV-01 Soft Blue Light family the standard for all new or revised video graphics, with the approved Motivation format for every lower third. Update Claude's video editing skills and reusable components, verify compact moving examples in 16:9, 9:16 and 1:1, preserve approved exports and all unrelated sound/color/editing rules, and keep the active VSL round-4 task and publishing queues untouched.
