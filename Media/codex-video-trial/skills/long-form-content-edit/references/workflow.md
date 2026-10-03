# Organic teaching and story workflow

Build the story around a clear promise, useful explanation, visible demonstration and ending. Preserve brief requirements and Dan's actual meaning. Check the rough cut as a performance before adding polish: lookaways, reset chatter, abandoned repeated openings and empty setup can survive an apparently fluent transcript. Check complete clauses and word tails at joins. Keep necessary exercise movement and recovery even when speech pauses.

As soon as the scene plan identifies new AI motion, stock or existing B-roll slots, prepare one compact look-and-assets packet. Keep building non-blocked scenes and isolated previews while approvals are pending. Reuse matching approved choices without resubmitting them. This packet is an owner checkpoint, not a second editor or an early independent review.

Use Dan's own exercise demonstrations under the relevant explanation; the accepted ab-wheel video improved when later exercise action illustrated the teaching. A different visible speaking take under narration produces lip mismatch and is not acceptable. Measure tighter explanatory framing and anticipated widening for extensions. Preserve hands, equipment and the full instructional action.

For a revision, begin from `WORK_PACKET.json`: the short requested-change list is exhaustive and the approved-element list is protected. Verify exercise/app demonstrations, generated motion, cast/scene variety, identity pairs and disclosure placement in short moving previews before starting the full render. Preserve hash-matching scenes, accepted audio packets/mix, transcripts and assets; rebuild only the affected scenes, graphic layers, joins, sidecar and final assembly.

Use the current Soft Blue Light family and Motivation lower thirds from the shared graphics standard, with Poppins, rounded cards where appropriate and deliberate reveals. Historical olive/white bars, grid title plates and `modern_graphics.py` defaults are reference history; adapt the component mechanics to the current family rather than carrying forward their old palette. Keep labels clear of face/body/equipment through transitions and posture changes. Teaching plays at natural speed; repetitive workout sets may accelerate deliberately with a visible speed cue and a stronger music bed. The 3x sets and brief 8x rest are ab-wheel decisions, not universal speed defaults.

No running burned captions or watermark: supply a correctly timed SRT sidecar. Featured real/AI photos still need their applicable labels. Grade original camera footage before graphics. Use the separate approved outdoor color addendum only where source calibration applies; later lighting needs its own check.

## Existing working path

The implementation is `Media/codex-video-trial/03-organic-abwheel/workflow.py`; its `verify`, `prepare`, `configure`, `audio`, `picture`, `subtitles`, `master` and `plan` subcommands call existing modules. Read `edit.json`, `framing.json`, `graphics.json`, `inserts.json`, `audio-plan.json`, `configure.py`, `apply_revision.py`, `modern_graphics.py` and the source-specific dependencies listed in the registry. `configure.py` makes this video's editorial decisions, not generic decisions for any footage.

Copy/adapt this implementation into an isolated new-video directory; replace hardcoded source/timing/asset paths before running it. The historical workflow must not be run in its own directory for a new edit. The correct shared self-test command from project root is `zsh .claude/skills/_shared/audio/selftest.sh`; do not use the broken relative command in the frozen proposed README. The new runner preflights a raw manifest but deliberately stops if a new editorial adapter is still needed.

For new or revised lower thirds, before/fact cards, 3A lists and cycles, `orglib` and `modern_graphics` are superseded. Build from `.claude/skills/_shared/hyperframes/from_plan.py`, composite with the shared `composite.py`, and verify with `checks.py`. Use `scripts/video/hyperframes_graphics.py` and the shared README; never fork the templates. Other approved kinds stay on `softblue.py`. Consult `.claude/skills/longform-edit/SKILL.md` only for needed implementation detail (multi-roll mapping, cut placement, subtitle construction). Earlier J2 styling, unconditional paid-tool bans and historical keep-list stops do not override current accepted trial instructions.

Finish editor self-QA with the `longform` exact-file gate, full chronological picture review and supported full audio review. Then use one independent reviewer at the complete-candidate checkpoint. A rejected candidate parks with one consolidated correction list; do not automatically run a second editor/reviewer loop. Keep the SRT, original untreated comparison, gate A/B, immutable first cut and real costs. Frozen v1.1 source files retain their historical pending wording; the registry records the later component approvals without silently overwriting that history.

The independent reviewer starts only after every approved clip is inserted and `placeholders.json` has no open item. Isolated or opening previews may carry clearly labelled placeholders where the shared rules allow them. A complete draft with placeholders is not a review candidate and cannot receive a delivery PASS.

Validated C1652 revision techniques and their explicit verification limits are recorded in [the R3 method note](c1652-r3-methods.md). They do not imply full-film artistic approval or gate clearance.

Verified R4 revision methods and limits: [C1652 R4 methods](c1652-r4-methods.md).

## Approval before full assembly, 2026-09-26

The [shared pre-render workflow](../../../../../.claude/skills/_shared/PRE-RENDER-APPROVAL.md#decision-budget-for-organic-and-other-non-vsl-videos) supersedes older instructions here to build a full draft with placeholders. For organic videos, group the source-specific look check and material new assets into one early review packet. Internally verify every graphic with surrounding speech and every clip in context; ask Dan only about meaningful new choices. Reuse the locked studio look and graphic components when the actual new roll supports them. Get approval of new AI start and end frames before motion generation. Show the finished first minute, then build the complete candidate only when all assets are locked. Keep accepted audio/color and unchanged caches.

## Graphics in new build adapters (2026-10-03)

Replace historical panel rendering with `scripts/video/hyperframes_graphics.py`: phrase-anchored plan data, shared `from_plan.py --render`, `Compositor.apply(frame, film_frame)` in the RGB frame loop, and shared `checks.py` on the composite. See `.claude/skills/_shared/hyperframes/README.md` and the RO-10 reference build. Record template/config/text/driven_by in the edit sheet and validate it. The version stays 0.8.97. Copy editorial source/cut/audio mechanics only, never templates or old graphics defaults.
