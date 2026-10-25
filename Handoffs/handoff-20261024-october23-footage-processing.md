# October 23 Shoot: Identify, Prepare and Catalog the Footage

CONTENT: reusable real B-roll, dedicated Shorts (SFC), and long-form content (LFC). This is footage preparation and queue registration, not authorization to edit or publish every finished video.

Created: 2026-10-24. Status: execution taken up by Codex on 2026-10-24. Live checkpoint: `Media/footage-index/shoot-20261023/checkpoint.json`; batch `SHOOT-20261023`.
Recommended executor: **Codex, GPT-6.1 Sol, high reasoning effort**. The live Codex host tool catalog on 2026-10-24 lists `gpt-6.1-sol` as its latest workhorse and supports `high`. Recheck the destination catalog at execution and use the newest available GPT model under Dan's standing rule. No model change is needed merely for a mechanical stage.
Suggested chat title: **October 23 Footage Processing**.

## Goal and Dan's decisions

Execute all six steps below: identify every recording, build an identification gallery, establish the B-roll color and trim standard with Dan, prepare every usable B-roll take, register the clips in the shared library, and reconcile all filmed scripted content with the existing Claude Edit Queue.

Dan approved this plan and requested this execution handoff. His decisions:

- **Keep all usable takes and angles; mark the strongest as favorites.** Do not keep only one winner per exercise.
- Future editing is by **Codex and Claude only**. Use one shared machine-readable catalog and a local browser gallery for Dan. A separate hosted website is unnecessary.
- Dan confirms proposed exercise identifications and names uncertain clips through the gallery. His corrections must persist for both AIs.
- First review package: shoot inventory, B-roll identification gallery, and approximately six representative color/trim samples. Bulk finishing follows his identification and look decisions. Do independent transcription and queue work while review is pending.
- He believes two long-forms were filmed. Verify the actual recordings; script counts are not filmed counts.
- Preserve all originals. No SD-card clearing, original deletion, publication, cover generation, or scheduling is part of this task.

## Verified source and current state

**Execution routing update, 2026-10-25:** Dan requested the verified non-B-roll working copies on Extreme for editing. Use `/Volumes/Extreme/10:23 dan rose fitness shoot - pool shorts and long form content` for C1790 and C1882 through C1899 (19 recordings). All 96 other gym recordings remain on Expansion. The Expansion paths below identify preserved originals and import provenance; they are not the active content-editing root for those 19 files. The 32 prepared intake maps and matching Extreme/project roll sidecars follow this split. Copy/routing evidence: `Media/footage-index/shoot-20261023/extreme-copy-20261025/verified-copy-manifest.json` and `source-routing-policy-20261025.json`. Historical receipts and the selected Expansion originals/sidecars stay unchanged. The saved inventory generator resolves this policy and preserves reviewed classifications.

Project: `/Users/danielrose/Documents/Claude/Projects/Abs By AI` (resolves to `/Users/danielrose/Projects/Claude/Projects/Abs By AI`).

Primary footage folder:
`/Volumes/Expansion/Abs By AI Raw Footage/10:23 dan rose fitness shoot - pool shorts and long form content`

The Seagate is mounted as **Expansion**, not as a volume named Seagate.

- 115 MP4 recordings, `C1785.MP4` through `C1899.MP4`, and 115 matching XML camera metadata files.
- Total source bytes: **154049270134**, about 154 GB.
- Receipt in that folder: `IMPORT-VERIFIED-20261023.json`. Records 230 verified files, status `complete`, originals retained, and SHA256 comparison of each source with an independent destination read. Completed 2026-10-23 at 22:42 UTC.
- Planning session independently compared current source/destination filenames and sizes on 2026-10-24: none missing, no size mismatches. It did not repeat the full 154 GB hash pass.
- Original card: `/Volumes/Untitled/PRIVATE/M4ROOT/CLIP`. Work from the verified Expansion copy. Ignore `._*` Apple metadata files as media; do not delete them as part of this task.
- Transfer owner chat: **Find space for raw footage**, ID `01a16ac3-d324-7492-a444-ffebfaf485f7`. Read its latest state if backup coordination is needed. A Google Drive backup of this new raw shoot was **not verified by the planning session**. Do not infer backup completion from a proposed prompt visible in a screenshot or start a duplicate transfer.
- No footage identification, transcription, trim selection, grading, gallery, or queue update has been performed by this planning task. No separate audio has been confirmed. Inspect the inventory first; ask only if a real missing source becomes evident.

## Read first and coordinate

Read the current `AGENTS.md`, `AI_COORDINATION.md`, and all of `.claude/skills/_shared/VIDEO-RULES.md`. Then read:

- `.claude/skills/_shared/rolls/README.md`
- `.claude/skills/_shared/cliplib/README.md`
- `.claude/skills/_shared/edit-queue/README.md` and `scripts/edit-queue/README.md`
- `.claude/skills/_shared/CUT-CONTINUITY-QC.md`
- `.claude/skills/_shared/renderq/README.md` and `.claude/skills/_shared/editcap/README.md`
- `Docs/memory/broll-always-colour-corrected.md`

Use one owner and one resumable batch identity, e.g. `SHOOT-20261023`. Claim only this work on the coordination board. Re-read the board before modifying it; keep the entry short. Do not touch other editors' jobs, pause states, or live directories. The Victory Dashboard remains paused.

Before production, check render/edit-cap status and acquire one batch slot using the supported edit-cap CLI (inspect help; do not invent a content type for a mixed asset batch). Release it while awaiting Dan. Follow the current waiting workflow when the cap is full. All heavy processing uses the shared render queue and its worker allowances. Obtain the work directory through `renderq.py workdir` with an estimate based on the inventory; do not hardcode a new work drive or copy all raw footage onto the internal SSD. Retain review assets and reusable outputs outside disposable scratch.

No subagents are required by this handoff. This handoff does not authorize creating or messaging other chats. Use available tools within the executing chat and follow applicable review instructions.

## 1. Inventory and identify the recordings

1. Check the receipt and current file inventory. Read camera XML and probe duration, resolution, rotation, frame rate, audio streams, and color metadata. Do not infer picture profile solely from flat appearance or copy an older shoot's LUT.
2. Check existing roll sidecars before generating transcripts or contact sheets. Reuse matching evidence; build only missing records. For silent B-roll, skip unnecessary speech processing. For spoken content, select the actual good mic per recording and transcribe with source times.
3. Inspect timestamped frames across each recording and moving excerpts wherever the exercise, variation, boundaries, or teaching intent is uncertain. One thumbnail is insufficient for recognizing a movement or choosing trims.
4. Classify source ranges as B-roll, dedicated Short, long-form, pickup, other useful material, or unusable. One recording may contain several actions or several scripts. Account for every source recording, including unreadable or ambiguous ones.
5. Match speech to the current scripts, checking all takes, alternate hooks, restarts, and incomplete endings. Track complete, partial, and not-found scripts separately. Capture useful demonstrations inside scripted recordings too, with exact source ranges.

Script sources:

- [The 10/23 Shoot Scripts](https://docs.google.com/document/d/11nUmri621xbb7K44Wxan7IAljK2mJeizDFCRgK752AA/edit)
- [Shoot shot list and day plan](https://docs.google.com/document/d/1XBOfCig7uB4vCnq5Gt76Lk-HdOlagF7YXoO3RrBdWeI/edit)
- `Docs/NEXT_SHOOT_LIST.md`
- `Docs/SCRIPTS_1023_POOL_LONGFORM_DAN_EDITED_20261020.md`
- `Docs/COPYEDIT_POOL_LONGFORMS_1023_AS_DELIVERED_20261020.md`
- `Handoffs/video-editing/jobs.json` and `00-MASTER.md`

Local planning documents disagree in age/scope: some mention 27 gym Shorts, some earlier notes mention 29, and several long-form scripts were planned. None proves filming. Read the live scripts through the Google Drive skill/tools, preserve Dan's current wording, and let footage establish the actual counts.

## 2. Build Dan's identification gallery

Build a durable local review page using the project's managed review-server pattern. Reuse existing gallery components where suitable. If website authoring requires a skill, follow the applicable installed skill while preserving the agreed local-only destination; do not publish externally without a need.

Each candidate card includes:

- Playable, scrub-able, lightly corrected review excerpt plus representative stills; no burned labels on the underlying library master.
- Stable candidate ID, original filename, exact source in/out, and duration.
- Proposed exercise and variation, equipment, viewing angle, and confidence expressed as confident/uncertain.
- Intended use: correct demonstration, deliberate mistake, beginner variation, setup/detail, or unknown. Never infer deliberate teaching intent from a poor rep alone.
- Confirm, edit name/tags, mark favorite, flag unusable, and add a note. Group related exercises and show uncertain items first; allow confirmation of a visible group without silently approving unseen items.

Persist edits to durable records outside the browser, with date, changed fields, and Dan's confirmation state. Browser local storage alone is inadequate. A supported save backend or an explicit export/import workflow is acceptable; visibly show whether changes are saved. Synchronize confirmed corrections to the shared source records and catalog; automatic re-analysis must not overwrite them.

Test playback, seeking, and save/reload persistence with a temporary test entry, then remove test data. Use `.claude/skills/_shared/review_server.py`; verify HTTP 200 and video byte-range 206 plus real browser seeking. Follow the full-quality `Videos to Review/` rule for any review video at least 45 seconds long. Keep source identification review distinct from approval of finished clips.

## 3. Establish the color and trim standard on a small sample

Choose about six clips that cover actual lighting/set differences, movement speeds, camera angles, and difficult exposures. Produce a few useful color alternatives on matching moments, recommend one per lighting family, and show the proposed usable range in motion. Identify any raw comparison explicitly as diagnostic only; the default gallery view should be corrected.

Check the camera profile and transform before grading. Match natural skin, readable muscle detail, sensible blacks and saturation; avoid grey flat footage, crushed shadows, and neon colors. Prior approved B-roll is a visual reference, not permission to reuse its numeric exposure or LUT on a different shoot. Show enough motion to reveal exposure changes and flicker.

Deliver the inventory, gallery, and samples together. Ask Dan in one batch to confirm/correct identities, mark uncertain teaching intent, and choose the color/trim treatment. Record his words and the exact reviewed sample versions. Continue independent script matching and queue preparation while those decisions are pending. Do not infer approval from silence.

## 4. Trim and color-correct every usable B-roll take

After the relevant sample decisions, apply the approved treatment by lighting family and tune exceptions shot by shot. Preserve all usable takes/angles, with favorites marked separately.

- Remove waiting, resets, camera handling, accidental wandering, unusable focus, and other junk. Between-takes drinking or looking away is not newly discovered B-roll.
- Preserve complete repetitions, useful teaching detail, and natural movement. Start the ready-to-use action promptly, normally within its first second. Keep a small editable handle where useful and record preferred action in/out separately; do not cut off the start or finish of a rep to meet an arbitrary duration.
- Separate multiple exercises, angles, or teaching intentions into distinct selections. Keep intentional mistake demonstrations explicitly labeled, never mixed into correct-form results.
- Preserve native resolution, frame rate, orientation and movement speed where appropriate. Do not bake a vertical crop into the only master. Preserve useful original audio or its recoverable source link; no music or voice processing is needed for silent B-roll.
- Choose a high-quality library encode suited to the source and existing library, estimate storage first, and record color tags/profile. Use small browsing copies for the gallery. Avoid unnecessary repeated encoding and duplicate full-resolution variants.
- Inspect every exported clip for color, action completeness, focus, head/body clearance, freezes/black frames, and clean beginning/end. Automated measurements support moving-picture inspection. Use applicable shared checks and report unsupported/not-applicable checks honestly; do not force B-roll through irrelevant finished-film requirements or weaken gates.

Retain the trim map, grade recipe, source identity and output checks so a revised clip can be rebuilt independently. Originals are never renamed or overwritten. Unusable selections are excluded from the usable library but remain accounted for in the source inventory.

## 5. Register and verify the shared library

Extend the existing library, not a competing catalog:

- Canonical catalog: `Media/clip-library/catalog.json` (private/gitignored).
- Source index: `Media/footage-index/<shoot>/` and the existing roll sidecars.
- Full-quality real clips: existing `03 B-Roll - Real Footage/dan-filmed/` library, resolved from the current tool/config.
- Drive library folder: `1Hby8O4mB4HZS341qvrVKHSHyCGBgP8mi`.
- Library procedures: `.claude/skills/_shared/cliplib/clip_library.py`.

Allocate permanent `B####` IDs through the maintained tool; check for concurrent additions and existing matching source ranges before allocating. Preserve temporary-to-permanent ID mapping. Store a concrete description, exercise aliases, equipment, angle, people, correct/mistake/beginner/unknown use, favorite status, source filename and times, grade/version, approval state, local path, and verified Drive link. Extend metadata compatibly if current fields are insufficient.

Register approved keepers as `usable-unused`; do not claim `used-final` until used in an approved film. Refresh previews and the existing catalog view. The current human spreadsheet is regenerated from the catalog and can overwrite typed edits, so gallery corrections must update the canonical records first.

Synchronize the prepared library files and metadata to its existing Drive location and verify uploads. Coordinate any raw-shoot backup with its transfer owner; raw backup completion is separate from processed-library backup. Do not change sharing to public as a shortcut.

Prove that both editing workflows can use the same records: exercise/equipment search, retrieval of a favorite, exclusion of mistake demos from correct-form results, working media paths, and source-range reconstruction. Test the commands from the project context; do not claim a separate Claude session was tested unless it actually was. Save a concise usage note for Codex and Claude and update their relevant shared library instructions if necessary.

## 6. Reconcile filmed content with the Claude Edit Queue

Target: [Abs By AI Edit Queue](https://claude.ai/artifact/1r1T8Znf96XH24zHZhybHs).

Read fresh queue state immediately before writing. Match by script/title and footage, not just code. Existing planned rows must be updated rather than duplicated. Allocate new IDs only for confirmed new videos. Every entry needs recognizable title, SFC/LFC category, script link, source files and exact take ranges, best/alternate hook information, completeness, useful linked B-roll, and genuine missing items. A partial recording remains blocked/needs with a concrete reason. Do not invent a new queue state without checking the supported schema.

The planning session found four existing blocked follow-along rows: **The 5-Minute No-Equipment Workout For Guys Who Hate Working Out (RO-33)**, **10-Minute Jump Rope And Kettlebell Fat Burning Workout (RO-34)**, **20-Minute Jump Rope And Dumbbell Full Body Workout (RO-35)**, and **15-Minute Jump Rope And Abs Workout (RO-36)**. These are duplicate checks, not a claim any were filmed on October 23.

Also check whether the new B-roll resolves **Top 5 Ab Exercises (DS-01)**, whose existing handoff requests Dan's cable-crunch footage to replace stock. Link a verified appropriate clip and update the dependency, but do not take over or execute that video revision here.

Use `scripts/edit-queue/queue.py` and the shared README. Add/update job briefs and `00-MASTER.md` consistently with `jobs.json`. The tool uploads the shared status file to Drive, ID `1RX-GqepEKqB1LgJqJFRyRU2lOJMnRFgg`, which the artifact is designed to read. Read back the uploaded records and verify expected IDs/states without reverting another session's changes.

**Capability boundary:** Codex has no native Claude `Artifact write_db` tool in this session. Updating the shared data is supported; the artifact's internal fallback database is mirrored by a Claude session using `queue.py pending` and version-guarded writes. Do not mark that mirror synced without a successful write. Verify the visible artifact if accessible; otherwise report that shared-data verification passed and visual/fallback verification remains unconfirmed. Do not claim the interface itself was modified.

Registration does not launch all edits or resume the paused overnight dispatcher. No release dates, full film renders, extracted Shorts, uploads for publication, or scheduling are authorized by this preparation handoff.

## Checkpoints and definition of done

Keep a resumable checkpoint with source inventory, per-range identity/review state, trim and grade versions, exported file hashes, permanent IDs, upload results, queue changes, unresolved questions and exact next command. On resume, reuse verified outputs instead of repeating analysis or rendering.

Completion requires:

1. All 115 source recordings accounted for, with any extra discovered sources explicitly added.
2. All candidate B-roll identified or explicitly unresolved, and Dan's submitted corrections saved durably.
3. Approved sample treatment applied to every confirmed usable take; all usable takes retained and favorites marked.
4. Prepared clips checked, searchable in the shared library, linked to originals, and backed up with verified results.
5. Actual filmed Shorts/long-forms reconciled against scripts and existing queue, with precise source maps and no duplicate jobs.
6. Shared queue records verified; any native Claude mirror or visible-page limitation reported separately.

At each review stop, show the gallery link first, say exactly what Dan needs to confirm, and release the batch's production slot. On completion, report counts of source recordings, usable B-roll clips, favorites, rejected ranges, Shorts, long-forms and unresolved items, plus library/queue links. Report factual stages only. Re-read the coordination board, update only this task, and run `scripts/board-check.sh` if edited. Keep private footage metadata out of the public repository. Remove this handoff from the OPEN index when execution has been taken up and its live checkpoint/owner recorded.

## Exact first action

Read the required instructions and ownership board, verify the Expansion source folder and receipt, inspect existing sidecars, then produce the full inventory and representative-frame map. Proceed through all six steps, stopping only for the specified identification/color decisions or a genuine unresolved blocker, while continuing independent work.

## Ready-to-paste starter prompt

Execute `Handoffs/handoff-20261024-october23-footage-processing.md` in the Abs By AI project. Process the October 23 shoot through all six steps: inventory and script matching, my B-roll identification gallery, representative color/trim samples, all usable B-roll preparation, the shared Codex/Claude library, and the Claude Edit Queue updates. Keep all usable takes and mark favorites. Start now with the verified Expansion footage. Bring me the identification gallery and color/trim samples for the review described in the handoff, then continue after my choices. Preserve originals and do not launch the individual finished-video edits or publish anything.
