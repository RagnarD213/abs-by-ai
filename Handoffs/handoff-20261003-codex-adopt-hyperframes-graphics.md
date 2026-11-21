# Codex: build graphics with the HyperFrames templates, the way Claude does

**Written:** 2026-10-03 by Claude (Opus 5.5) at Dan's request. **For:** Codex. **Model:** GPT-6 Sol, high (adopting
existing, approved templates and shared code, plus one measured proof; no new design work).
Sidebar name: `HyperFrames Codex Adopt`.

## Why

Dan, 2026-10-03: *"I want to start using hyperframes in Codex like we are in Claude."* Claude's videos have drawn their
graphics with HyperFrames since 2026-09-30. Dan's verdict on the pilot: *"significantly better than the graphics that
we're using."* Codex builds still draw flat panels with `orglib` or `modern_graphics` (RO-17, RO-01), which also
cannot be redrawn for a vertical or square version. This handoff closes that gap.

## What HyperFrames is here (and is not)

- It is the **graphics layer only**. Each graphic is an HTML page animated by one paused GSAP timeline, rendered to a
  transparent ProRes 4444 overlay, then laid over the film by our own compositor.
- The cut, grade, audio chain, captions, gates, edit sheet and delivery do not change. Never point HyperFrames at raw
  footage or use it to assemble a video.
- The look stays **Soft Blue Light**. HyperFrames changes how graphics move and land, not the style lock
  (`.claude/skills/_shared/SOFTBLUE.md`, `.claude/skills/_shared/GRAPHICS-STANDARDS.md`).

## Read first, in this order

1. `.claude/skills/_shared/hyperframes/README.md`: the templates, the one-pass recipe, 9:16 and 1:1 layouts, the easing
   table, and "Rules that bit".
2. `Media/hyperframes/README.md`: pinned version, PATH, CLI commands. (`Media/` is not in git, so read it from the main
   project folder, not a worktree.)
3. `.claude/skills/_shared/edit-sheet/CODEX.md`, point 3: graphics come from the templates so each has a template name
   and a config, and a vertical can redraw it.
4. `.claude/skills/longform-edit/reference/ro10/` (`README.md`, `plan.py`, `build.py`): the first full film built this
   way. Copy its shape.
5. `Docs/HYPERFRAMES_RESEARCH.md` only if the reasons are needed.

## Setup on this Mac (already installed, nothing to buy)

- Version is pinned: **hyperframes 0.8.97**, always called as `npx -y hyperframes@0.8.97 ...`. Do not use the global
  `hyperframes` binary in `~/.npm-global/bin` (it is 0.7.7) and do not upgrade. It releases several times a day.
- Before any command:
  `export PATH="/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin:$PATH" HYPERFRAMES_SKIP_SKILLS=1`
- You should rarely call the CLI by hand. `hfbuild.py` wraps it (scene folder, fonts, `lint`, `check`, `snapshot`,
  `render`) and uses absolute paths to the main project folder, so it also works from a worktree.
- HeyGen's own authoring guides are on disk at `~/.claude/plugins/marketplaces/hyperframes/skills/` (`hyperframes-core`,
  `hyperframes-animation`, `hyperframes-cli`). Read them only when writing a NEW template. Do not install a second copy.

## The method (what Claude does on every video)

1. **Cut first.** Graphics are timed on the finished film timeline, never on raw time.
2. **Word timing drives everything.** Every graphic's in, out and each part's reveal is a PHRASE Dan says, resolved to
   the start of its first word from the mapped words file. No whole-second times picked by hand.
3. **Plan as data.** Graphics live in the video's resolved plan (items with `t0`, `t1`, kind and copy), not in Python
   lambdas inside the render script.
4. **One pass:**
   `python3 .claude/skills/_shared/hyperframes/from_plan.py --plan plan_resolved.json --words words_out.json --shots shots.json --out hf --render`
   writes one config per scene, checks the copy fits, lints, renders, and writes `hf/manifest.json` and `hf/BEATS.md`.
5. **Composite** in the per-frame render loop with `composite.py`:
   `C = Compositor(json.load(open("hf/manifest.json")))`, then `frame = C.apply(frame, g)`.
6. **Verify** with `checks.py`: Dan clear of every side card, his face above every lower third, card fill correct.
7. Vertical and square versions redraw the same configs with `vertical.py` and `square.py`. Nothing is re-authored.

## Templates

| Template | Dan's approval | Use for |
|---|---|---|
| `lower-third/` | approved 09-30 | Motivation lower third, parts land on his words, optional counter bar |
| `before-card/` | approved 09-30 | full-screen photo plus glass fact card, number counts up |
| `side-list/` | approved 09-30 | the 3A left card, items land on their words |
| `cycle/` | approved 09-30 | a four-step loop and its reversal, in the left-third card beside Dan |
| `title-card/`, `media-card/`, `cta/`, `tally/` | **not approved yet** | show on a graphic-lock page before using in a full build |

Anything the templates do not cover stays on `softblue.py` for now. Do not invent a new template inside a video build.
A new one is its own small task: build it, show it on a real frame, get Dan's approval, then add it to the shared folder.

## Traps (each of these cost a render)

- **Colour.** Overlays come out untagged BT.601 limited range; our footage is BT.709. Use the shared `composite.py`,
  which decodes each file by its own matrix in RGB. A plain ffmpeg `overlay` shifts the navy.
- **Glass blur.** A transparent overlay cannot blur what is under it. The lower third renders a second `_mask` pass and
  the compositor blurs the footage inside it. Only the shared compositor does this.
- **One root composition per folder.** One project folder per scene. `hfbuild.make_scene` handles it.
- Fonts need `@font-face` to a file inside the scene folder. `fromTo` for every starting state. Finite `repeat` only.
- `check` reports "0/0 text checks" on a transparent overlay. Judge contrast on composite stills.
- Render speed is about 5 to 6 seconds per second of overlay. Render only scenes whose config or template changed
  (`from_plan.py` already skips the rest).
- Side cards: Dan sits right of the card with his arms clear. Slide the crop left inside the 4K frame where there is
  room; see "Placing Dan beside the card" in the shared README and the RO-10 `all_segments` solver.
- A review page served by launchd cannot read `/Volumes`. Serve from `/Users/Shared`.

## What to change

1. **Codex skills** under `Media/codex-video-trial/skills/` (`long-form-content-edit`, `abs-edit-ad`, `vsl-edit`; the
   `~/.codex/skills/` entries are links to these, and `abs-edit-organic` is a pointer to `long-form-content-edit`):
   wherever graphics are described or generated, state that lower thirds, before cards, 3A lists and cycles are built
   from the shared HyperFrames templates through `from_plan.py`, `composite.py` and `checks.py`. Point to the shared
   README instead of copying it. Mark `orglib` and `modern_graphics` panels as superseded for those four kinds
   (`long-form-content-edit/references/workflow.md` line 21 is one such place).
2. **Codex build scripts:** the next build's plan carries graphics as data in the shape `from_plan.py` reads, and the
   render loop calls the shared compositor. Call the shared code. Do not fork it or copy templates into a Codex folder.
3. **Edit sheet:** each graphic is recorded with its template name, config and `driven_by` words, so
   `validate.py` passes and a vertical can be built from it.
4. Add one line to `.claude/skills/_shared/hyperframes/README.md` saying Codex builds use the same folder, with the date.

## Proof (one, small)

Take ONE existing Codex video that has at least one lower third and one side list or before card (RO-17 at
`/Volumes/Extreme/_edit_work/RO-17/` is the natural choice). On a 30 to 60 second excerpt:

- Rebuild its graphics from the templates with copy unchanged and each part landing on Dan's word.
- Composite with the shared compositor and run `checks.py`. It must pass.
- Make a review page in the standard format (`.claude/skills/_shared/PRE-RENDER-APPROVAL.md`): the old excerpt and the
  new excerpt side by side, then every graphic as a still on its real frame, three per row, and a short "What I decided".
- Send Dan the page link with at most two questions. Stop there.

Do not rebuild, re-export or re-upload any approved, queued or published video. The method applies to new Codex builds
and to videos still in revision.

## Rules that still hold

- Work in a Codex worktree and push with plain git. The main project folder cannot push right now (other sessions'
  uncommitted edits stop `safe-push.sh`), so do not commit there. `Media/` is ignored by git except the Codex skill
  files already tracked; heavy media goes to `/Volumes/Extreme/_edit_work/`.
- No sound effects on graphic entrances. No em dashes in anything written. Plain language for Dan.
- HyperFrames is free and renders locally, so there is no spend. Nothing is uploaded or published.
- When done: remove this handoff's line from `AI_COORDINATION.md` and its row from `Handoffs/README.md`.

## Starter prompt

> Name this task `HyperFrames Codex Adopt`. Read `Handoffs/handoff-20261003-codex-adopt-hyperframes-graphics.md` and
> the files it lists under "Read first". Adopt the shared HyperFrames graphics method in every Codex video skill and
> build script: graphics planned as data, timed on Dan's words, built with `from_plan.py`, composited with the shared
> `composite.py`, verified with `checks.py`, pinned to hyperframes 0.8.97. Use the shared templates in
> `.claude/skills/_shared/hyperframes/`; do not fork them. Prove it on one 30 to 60 second excerpt of an existing Codex
> video (RO-17) with an old-versus-new review page, then stop for Dan. Do not rebuild or re-upload any approved video.
> Explain the result in plain language.

Model and effort: GPT-6 Sol, high.
