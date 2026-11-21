# Handoff: clear old job folders off the Extreme drive (2026-10-21)

**Type:** ops, not a video. **Recommended:** Codex GPT-6.1 Sol, high (ops belong to Codex; careful file work).
**Urgent:** the Extreme SSD had **13 GB free** at 13:40 on 2026-10-21 (3.6 TB, 100% full). Live edits write there;
at 0 GB they fail. Start with the biggest folders.

## Goal

Free several hundred GB on `/Volumes/Extreme` without losing a single file. Dan: "clear the old job folders and
anything else which you're totally confident is safe to delete from the Extreme drive."

## The decision: move, do not delete

Every eligible folder is **moved to the Expansion drive** (`/Volumes/Expansion`, 24 TB, 20 TB free), verified, and only
then removed from Extreme. That frees exactly the same space on Extreme, nothing is lost, and anything can be moved back.
Nothing is permanently deleted by this task. Moved jobs land in `/Volumes/Expansion/_edit_work/<job>/`, where the render
queue's folder picker (`python3 .claude/skills/_shared/renderq/renderq.py workdir <job>`) finds them automatically if a
video ever gets another round.

## Scope

**In scope:** only top-level job folders inside `/Volumes/Extreme/_edit_work/`.

**Never touch (out of scope, do not open, list, move or delete):**
- Everything at the Extreme root other than `_edit_work`: the raw shoot folders (`10:15 ...`, `dan rose fitness 9:23
  ...`, `abs by ai 8:28 ...`, `8:3`, `8:14`, `7:8`, `welcome-video`), `Personal`, `screen recordings` (personal; do not
  open it or list its contents), `Photo Shoots`, `Abs By AI Photo Shoots`, `Claude Content Videos`, `Codex Content
  Videos`, `Zeeshan Content Videos`, `Short-form video content`, `_asset_library_stage`, `ad-edit-research`, `metadata`,
  the SanDisk installer files, and system folders (`.Spotlight-V100`, `.Trashes`, `.fseventsd`, `System Volume
  Information`). Raw footage removal is Dan's separate open decision (board entry "Nightly footage";
  `Handoffs/handoff-20261005-claude-nightly-footage-offload.md`).
- Inside `_edit_work`: any name starting with `_` (clip library, approved clips, gate baselines, transcripts, timing,
  queue folders), `bin` and any `*/bin` folder (ffmpeg wrappers), and loose files (`DELIVERY.md`, `._*`).

## Eligibility: a folder moves only if ALL of these hold

1. **Untouched for 14 days:** `find "<folder>" -newermt "<today minus 14 days>" -not -name '._*' -print -quit` prints
   nothing.
2. **Not named where live work or a rule points at it.** Search for `/_edit_work/<folder>` (any case) in:
   `AI_COORDINATION.md`; every OPEN handoff listed in `Handoffs/README.md`; `AGENTS.md`; `CLAUDE.md`; every `.md` under
   `.claude/skills/_shared/` (VIDEO-RULES, GRAPHICS-STANDARDS, PRE-RENDER-APPROVAL, chroma-key, video-rounds, ...);
   `.claude/agents/*.md`; memory (`Docs/memory/*.md` and
   `~/.claude/projects/-Users-danielrose-Documents-Claude-Projects-Abs-By-AI/memory/*.md`); all code and config under
   `scripts/` (`*.py`, `*.json`, `*.sh`, `*.js`, e.g. Blotato setups); `Docs/LONGFORM_RELEASE_CALENDAR.md`,
   `Docs/SHORTS_RELEASE_CALENDAR.md`. A hit in any of these protects the whole folder. History mentions in individual
   `SKILL.md` files and old `Docs/*RECEIPT*` files do NOT protect (they record past builds).
3. **Nothing is using it right now:** no open file inside it (`lsof 2>/dev/null | grep -F "/_edit_work/<folder>/"`),
   no render-queue slot or waiting job in it (`python3 .claude/skills/_shared/renderq/renderq.py status --json`: check
   each `cwd`, `label`, `cmd`), no review server serving from it.

Anything that fails a check stays put and goes in the report with the reason.

## Starting picture (scan of 2026-10-21; recompute, do not trust blindly)

- `_edit_work`: 159 job folders, 2,005 GB. **94 untouched for 14+ days, 681 GB.** 65 touched since 2026-10-07, 1,324 GB
  (not in scope).
- Biggest untouched: ro05-fable 62 GB, sl05 59, invest-health-cutdowns 54, ad5-vert 42, ad4-vert 37, ro12 33, ro05 33,
  website-video-828 27, ro01 25, zepbound 22, ad2-vert-v2 21, ad1-8-14 21, ad1-sq 18, spraytan 17, ad3-vert 15,
  grok-ad1-first-cut 15, av05-ad6-vert 15, ads234-8-14 14, supplements 13, abwheel 12, then about 70 smaller ones
  (`revisions-*` download folders, `*-publish` setup folders, old ad verticals and squares).
- Already known to be protected by check 2: `abwheel` and `hyperframes-r2` (approved references named in VIDEO-RULES),
  `AV-01` and `muhammad-shorts-publish` (named in `scripts/`). Check every `*-publish` folder carefully: a video still on
  `scripts/blotato/video_waitlist.json` may need its media.
- `grok-ad1-first-cut` holds the target of the `/Volumes/Extreme/_edit_work/bin` ffmpeg symlinks
  (`grok-ad1-first-cut/bin/`). **Keep `grok-ad1-first-cut`**, whatever its age.

## Method, one folder at a time, biggest first

1. Destination: `/Volumes/Expansion/_edit_work/<folder>`. If a folder of that name (any case) already exists there, use
   `/Volumes/Expansion/_edit_work/<folder>__from-Extreme-20261021` instead. Never merge into an existing folder.
2. Copy at background disk priority so live renders keep the drives:
   `taskpolicy -b rsync -a "/Volumes/Extreme/_edit_work/<folder>/" "<dest>/"`. Do not run copies through the render
   queue (a long copy would hold a render slot) and run only one copy at a time.
3. Verify before removing anything:
   - `rsync -a --dry-run --itemize-changes "<src>/" "<dest>/"` prints nothing;
   - the count of regular files and their total bytes match on both sides (ignore `._*` files);
   - `shasum -a 256` of the largest file and two random files match.
4. Only after all three pass: `rm -rf "/Volumes/Extreme/_edit_work/<folder>"`. If any check fails, leave the Extreme
   copy in place, remove nothing, and report it.
5. Append one line to `/Volumes/Extreme/_edit_work/MOVED_TO_EXPANSION.md` and to the repo receipt
   `Docs/EXTREME_CLEANUP_20261021.md`: folder, GB, new path, date, "verified rsync + count/bytes + sha256".
6. Stop the whole run if Expansion falls below 1 TB free, if `df` shows Extreme writes failing, or if a live session
   starts writing into a folder you are copying (re-run check 3 right before step 4).

## Report to Dan (plain words, in chat)

Extreme free space before and after; how many folders moved and how many GB; the folders that stayed and why (one line
each). Then a short list of what is NOT covered and would free the most if Dan decides to clear it later: the raw
shoot folders (about 830 GB, copies already on Expansion `Abs By AI Raw Footage`, Seagate and Drive, but active edits
read them from Extreme), `kit9x16` (160 GB build caches of the vertical-ad kit), and finished videos' folders that were
touched in the last 14 days (`ro20` 200 GB, `ro19` 69, `ro06` 55, `RO-17` 55, `ro07` 52, `ro11` 37, ...). Do not
move any of those without Dan's go-ahead.

## Wrap-up

Commit `Docs/EXTREME_CLEANUP_20261021.md` and this handoff's line removal from the OPEN section of `Handoffs/README.md`
(Codex: push from a clean checkout with plain git, as for RA-13's records). No board entry unless you are blocked.

## Starter prompt

> Run the handoff at `Handoffs/handoff-20261021-extreme-drive-cleanup.md` (Abs By AI repo). Ops task, not a video. The
> Extreme drive is nearly full. Move old job folders from `/Volumes/Extreme/_edit_work/` to
> `/Volumes/Expansion/_edit_work/`, biggest first, only the ones that pass every eligibility check in the handoff. Verify
> each copy (rsync dry run, file count and bytes, sha256 spot check) before removing the Extreme copy. Never touch
> anything outside `_edit_work` and never delete anything that has no verified copy. Report in plain words what moved,
> what stayed and why, and the free space before and after.
