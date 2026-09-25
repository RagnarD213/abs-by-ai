Read `_shared/VIDEO-RULES.md` first.

# Video editing handoffs — rules every job shares

**Written 2026-09-16 (Opus 5) with the master list `00-MASTER.md`.** Every job doc in this folder is short on purpose.
The rules that bind *every* job live here once. **Read this file in full before the job doc.** Where a job doc and this
file disagree, the job doc wins for its own specifics (frames, timestamps, assets), and `AGENTS.md` beats both.

Each job doc has **two starter prompts**: one for a Claude Code session and one for a Codex session. The job spec is the
same; only the tools differ (section 3).

---

## 1. Before you start (every job)

1. **Check that the job is still open.** Open `Handoffs/video-editing/00-MASTER.md` and read the job's row. If it says DONE,
   IN PROGRESS (someone else) or BLOCKED, stop and tell Dan. Then read `AI_COORDINATION.md` from disk and look for an
   ACTIVE entry naming the same video.
2. **Claim it:** `python3 scripts/edit-queue/queue.py set <ID> in_progress --by <Claude|Codex>` (see §5) and add ONE short entry to
   `AI_COORDINATION.md` ACTIVE (≤ 3 lines, edit only your own entry, run `scripts/board-check.sh`).
3. **Machine cap: never more than two video builds at once across all sessions** (renders, big ffmpeg encodes, Whisper,
   gate runs). Check first: `ps -Ao pcpu,command | grep -E 'ffmpeg|whisper|render\.py|gate\.py|qc_style' | grep -v -E 'grep|Renderer'`.
   If two are running, wait. Four at once measured a 9× slowdown (`AGENTS.md`).
4. **Never run a script inside another session's build directory.** Copy what you need into your own
   `/Volumes/Extreme/_edit_work/<job-id>/` directory.
5. **Raw footage is read-only.** Never move, rename or re-encode anything in the shoot folders on `/Volumes/Extreme`.
6. **Reuse roll sidecars first.** Before transcribing, picking a lav or building a contact sheet for a source clip, run `.claude/skills/_shared/rolls/roll_sidecar.py show`; if there is no sidecar, run `build` and use its output. When the EDL is final, run `mark-used` for every source range.

## 2. Standing content and quality rules (from `AGENTS.md`; the wording there is authoritative)

* **Audio.** Our own mixes go through `.claude/skills/_shared/audio/`: `pick_lav.py` picks the lav **per file**. The
  8/28 rolls have four mono tracks and the 8/3 + 8/14 rolls differ, so never hard-code a channel. `voice_chain.py` is
  the only voice chain, and `audio_gate.py` stamps the delivered file. **An editor's finished mix is used untouched**
  (`--verbatim`); a cutdown only cuts it at the seams. No loudness change, never mono. Run `selftest.sh` before a batch.
* **Colour.** Editor masters carry no colour tags. **Decode as BT.709** (`scale=in_color_matrix=bt709:in_range=tv`),
  never ffmpeg's BT.601 default, and verify against the reference decoded the same way (memory `untagged-video-bt601-trap`).
* **Framing.** Hair-anchored NEAR/FAR only, never wide (memory `framing-standard-hair-anchored`). For vertical and square crops,
  keep wider shots **steady per shot**; track only when a very tight crop needs it (`.claude/skills/_shared/framing-motion.md`, 09-16).
  Zoom cuts, never naked jump cuts.
* **Labels.** Every AI image or clip carries **AI-GENERATED**. Every *real* picture of Dan shown as a result carries
  **"Real picture of me — not AI-generated"**, as the same solid rounded chip. **Never place a label over his face or his
  abs.** Place it by measuring the rendered frame (a person mask gives the head + torso box), never at a fixed y.
* **Before and after are the same person, always.** The only real app screen recording uploads a man who is **not Dan**
  (memory `app-recording-before-after-pair`). If you show his upload, show his result; if the result doesn't exist,
  generate it through the live product. Never a composite.
* **Banned screens.** No side-by-side before/after app screen, no "Meet the new you" screen, no email-capture screen.
  Gate `compliance:banned_screen` scans every frame.
* **Claims.** No unbelievable claims in on-screen text (memory `ad-copy-no-unbelievable-claims`). No drug brand names in
  on-screen graphics for Zepbound/GLP-1 material. Health disclaimers Dan says on camera stay in.
* **Photos.** Don't pick frowning photos by default (they live in `photos/finalized social media photos/Frowning Photos/`).
* **AI clips.** Check every AI shot frame by frame for breath smoke, fogging mirrors, melting hands and morphing objects
  (memory `ai-clip-artifact-giveaways`). Show Dan the start/end frames and the intended action **before** generating
  motion. The budget is **$5 per video** including retries (`AGENTS.md`). Stock: Pexels or assets we already own, never a paid service.
* **One delivery gate:** `.claude/skills/_shared/deliver/gate.py --format <fmt>` on the file that actually goes out, at the
  current `GATE_VERSION`. A check that didn't run FAILS. **Never raise a threshold to make a file pass.** If a gate or bound
  must change, `python3 .claude/skills/_shared/qc_corpus/run.py` must pass first.
* **Independent audit before Dan sees it.** A fresh reviewer (subagent or second session) watches the delivered file at
  full resolution against the script/reference and reports defects. Expect "does not ship" the first time.
* **YouTube: never Public.** Ads are uploaded **Unlisted**; organic is uploaded **Private** and released by Blotato. Read the
  visibility back. (No job in this folder uploads anything unless its doc says so.)

## 3. Tools per executor

| | Claude Code session | Codex session |
|---|---|---|
| ad first cut from raw | `/ad-edit` | `$abs-edit-ad` |
| organic long-form first cut | `/longform-edit` | `$abs-edit-organic` |
| dedicated short from raw (vertical) | `/shorts` for the vertical finishing rules + `/ad-edit` Steps 1–4 for take selection | `$abs-edit-organic` (take selection, audio, colour), then the vertical rules in `.claude/skills/shorts/SKILL.md` |
| shorts cut from a finished long-form | `/shorts` | read `.claude/skills/shorts/SKILL.md` and follow it with Codex tools |
| ad vertical / square / ≤0:59 | `/shortad-from-longform` | read `.claude/skills/shortad-from-longform/SKILL.md` in full; model: `Handoffs/handoff-20260914-ad3-square-codex.md` (the Ad 3 square Codex built and Dan shipped) |

**Codex specifics.** The environment traps (quoted paths with spaces, the project ffmpeg at `Media/video_edit/bin/`,
Python 3.9 process names, zsh word-splitting, `pgrep` self-matching, delivered names containing ` | `) are listed in
`Handoffs/handoff-20260914-ad3-square-codex.md` §2. Read that table. The Codex trial recipes and preference registry are in
`Media/codex-video-trial/` (`templates/`, `05-recipes/`). **Git:** commit docs/scripts only, never media (the repo is public).
Follow the Codex branch rule in `Handoffs/codex-video-trial/00-start-here.md`.

**Model recommendation (both columns are in every doc):** Claude **Fable 5.1, effort high** for any build; Codex
**GPT-6 Astra, effort high**. A job doc names a cheaper setting where it is safe.

## 4. Delivery conventions

* **Ads:** `<Editor> Ad Videos/<title> - ad N/` for editor-origin ads. For our own first cuts, use a new folder
  `Claude Ad Videos/<title> - <id>/` or `Codex Ad Videos/<title> - <id>/`. File names follow `/editor-deliveries`:
  `<title> | <claude|codex> | <16x9|9x16|9x16 59s|1x1|1x1 59s> | <ad N or job id>.mp4`.
* **Organic long-form:** `claude edited long form content/NN - <Title>/` (Claude) or `Codex Content Videos/<title>/`
  (Codex): the master, `.srt` (uploaded, not burned in), chapters, stamps, notes, recipe.
* **Shorts:** `Short-form video content/<slug>_<title>.mp4` + stamps, 1080×1920. **No cover images in an editing job** (Dan, 2026-09-25): covers are a separate, smaller task that Codex runs, to save tokens. An editing job never runs `/coverimage`.
* Every delivery also includes a `REVIEW 540p` copy for Dan's phone, the audio A/B clip, the `.audio_gate.json` +
  `.deliver_gate.json` stamps, a `notes-*.md` (every deliberate choice and deviation) and a `recipe-*/` folder that can rebuild it.
* **Report to Dan in plain language:** what you made, where the review copy is, what his call is. No jargon.
* **Done means Dan approved it after watching.** Passing every gate is not approval.

## 5. Closing out (every job)

1. Update the job's status with `python3 scripts/edit-queue/queue.py set <ID> <state>`: `in_progress` at start, `delivered` when Dan gets the review copy, `finalized` when **Dan says** it's finalized, `uploaded` after `/ad-setup` or `/video-setup` has uploaded it. The script updates `jobs.json` and the `00-MASTER.md` row. **Claude sessions also push it to Dan's pinned page** with `Artifact write_db`, and **Codex commits the change** for the next Claude session to sync. Procedure: `.claude/skills/_shared/edit-queue/README.md`.
   If the job unblocks another (a square waits on its vertical), change that row to READY.
2. On approval: delete your `AI_COORDINATION.md` entry. Once the job is FINALIZED, the job doc can be deleted or moved to
   `Handoffs/video-editing/done/` (keep its notes in the delivery folder).
3. Put techniques and traps you learned into the relevant skill, not into this folder.
4. **No dashboard rows** unless Dan asks (his 09-08 rule). Commit + push the doc changes to `main`.
5. After an ad variant is approved, it goes into Google Ads through `/ad-setup` step 6 as one more `videos` entry on that
   ad's existing Demand Gen ad groups. **That's a separate step. Don't do it inside the edit job unless Dan asks.**

## Edit Queue page is Dan's working list (Dan, 2026-09-24)
A queue change is not done until it shows on https://claude.ai/artifact/1r1T8Znf96XH24zHZhybHs. After `queue.py add` or `set`: push to Drive, mirror to the artifact db, and check the job's `group` (and a Dedicated-shorts `sub`) is one the page renders (its `LISTS` array; subs "9/23 shoot", "Talking", "Workout"). A new group or sub means republishing the page first.
