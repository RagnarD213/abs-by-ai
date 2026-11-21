# Filmed ad workflow

The spoken script defines the sales story and order. Align each sentence to original takes; prefer complete, fluent delivery with energy and a clean transition into the next line. Remove slates, repeats, abandoned takes, director chatter and dead setup while keeping complete word tails. When Dan changes wording live, keep his version unless it changes the substantive claim or a required qualifier; flag that discrepancy.

Build a source/output cut map and the scene-to-speech plan before graphics. The opening must establish the hook's actual object. Carry the story through problem, mechanism/proof, product use and CTA as the script calls for them. Product screens must demonstrate the feature being described, including same-person generation and real playing exercise sheets. Every visual must earn its place by supporting that beat.

As soon as the scene plan identifies new AI-motion, stock or existing-B-roll slots, prepare the single asset-approval batch required by the shared standards. Send it before the draft is finished, then keep building all non-blocked work with exact-duration labelled placeholders. The approval batch is not a second editor or an early independent review. Existing hash-matching approved choices remain fixed and are not resubmitted.

For a revision, begin from `WORK_PACKET.json`: the short requested-change list is exhaustive and the approved-element list is protected. Verify old-channel proof, exercise/app demonstrations, generated motion, identity pairs and disclosure placement in short moving previews before starting the full render. Preserve hash-matching scenes, accepted audio packets/mix, transcripts and assets; rebuild only the affected scenes, caption layers, joins and final assembly.

Use the current Soft Blue Light family and Motivation lower thirds from the shared graphics standard, with readable Poppins, deliberate reveal motion and strong graphic scale. Historical Ad 1 graphic palettes are reference history, not the current default. Preserve approved fixed talking compositions and the separately specified transitions hiding joins. Ads use burned captions. Keep captions clear of graphic labels and physique; inspect exact render timing and complete sentence text. Do not copy the rejected first ad's redesign or the four deferred picture errors from the accepted sound/color benchmark.

## Existing working path

Read the relevant files in `Media/codex-video-trial/04-ad1/rebuild-muhammad/full-ad-approved/`: `full-edit.json`, `SOURCE_MAP.md`, `render_full.py`, `finish_full.py`, `final-recipe.json`, `dependencies.json`, `make_gate_plan.py`. `render_full.py` uses original shared components from its parent's `render_proof.py` and `patch_transitions.py`. The original files are reference implementations with fixed paths/timelines, not safe new-video commands. `RECIPE.md` describes the historical build but its old “Stage 05 waits” statement is superseded by current feedback and the registry.

For a new ad, copy/adapt these implementations into the new isolated video directory, explicitly replace old source/take/asset paths and timing, and preserve the reusable component imports. Replace the source-specific calibration only where the recording differs. Do not call the old `prepare_full.py`/`render_full.py` in their own historical directory. No general raw-ad renderer is promised by Phase 5: a new editorial adapter is required, and the runner's raw route stops with that fact before expensive work.

The source production skill is `.claude/skills/ad-edit/SKILL.md`: consult its take selection, demo and caption sections when needed. Its unconditional second aspect ratio, first-minute take-reel stop, early graphics defaults and generic audio prose do not override the current trial scope or accepted source-specific recipe.

Caption-only revision caveat: historical `AD1_FULL_PICTURE.mp4` already includes `full.ass`. Reuse accepted AAC, but verify that any picture cache is genuinely uncaptioned before burning new captions. If no clean cache exists, rebuild the necessary picture from original components in scratch. Phase 5's independent caption cache is proven for its replay; it is not retroactively present in that historical full-film renderer.

Finish editor self-QA with `ad16x9` exact-file checks, complete chronological picture and full audio review through a supported route, immutable first-cut hash and honest costs. Then use one independent reviewer at the complete-candidate checkpoint. A rejected candidate parks with one consolidated correction list; do not automatically run a second editor/reviewer loop. Future new-video tests must freeze first cuts before opening their matching human exports or critiques.

The independent reviewer starts only after every approved clip is inserted and `placeholders.json` has no open item. A draft with placeholders may be shown to Dan for the combined cut/source decision, but it remains internal DRAFT media and cannot receive a delivery PASS.

For a near-final picture-only revision with protected audio and approved scenes, follow the verified [Ad14 R4 revision method](ad14-r4-methods.md). It demonstrates two-job replacement, exact app/audio preservation, source-identity proof and honest handling of inherited gate findings; its source timestamps remain specific to Ad14.

## Approval before full assembly, 2026-09-26

The [shared pre-render workflow](shared/standards.md#approval-before-a-full-render) supersedes older instructions here to build a full draft with placeholders. Approve the first 30 seconds or preserve an explicit prior approval/waiver, every graphic with before/during/after speech, all selected clips and AI frame pairs followed by motion. Continue independent preparation and isolated/contextual previews only until those choices are locked. Keep the source-specific accepted audio/color and unchanged caches.

## Graphics in new build adapters (2026-10-03)

Replace historical panel rendering with `scripts/video/hyperframes_graphics.py`: phrase-anchored plan data, shared `from_plan.py --render`, `Compositor.apply(frame, film_frame)` in the RGB frame loop, and shared `checks.py` on the composite. See `.claude/skills/_shared/hyperframes/README.md` and the RO-10 reference build. Record template/config/text/driven_by in the edit sheet and validate it. The version stays 0.8.97. Copy editorial source/cut/audio mechanics only, never templates or old graphics defaults.
