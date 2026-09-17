# Overnight edit queue — keep two video builds running while Dan is away

**Written 2026-09-17 (Claude, Fable 5.1) from a design discussion with Dan.**
**STATUS 2026-09-17: Phase 1 BUILT and installed PAUSED; Phase 0 HALF proven (Codex yes, Claude blocked on Dan's
one-time sign-in). Phase 2 not started. What was built, the proven launch commands and the open ends:
`scripts/edit-queue/README.md`. Remaining before un-pausing: §8a below.**
This is a BUILD handoff for the automation, not an editing job. It is ops/tooling work, so by Dan's 09-15 split it
goes to **Codex**. One build session for Phases 0–1, a second for Phase 2.

## 1. Goal

The Mac mini sits idle overnight and whenever Dan is away. Build a system that keeps **up to two** video edits
running from the master list (`Handoffs/video-editing/jobs.json`, 76 jobs, ~56 ready) with nobody at the keyboard,
and hands Dan a short review queue when he is back.

**The scarce resource is Dan's review time and the AI usage allowance, not the Mac.** The system is sized to what
Dan can review each morning (3–4 items), not to keeping both slots full at any cost.

## 2. Decisions Dan has already made (do not re-open)

1. **Who edits what (Dan, 2026-09-17).** A fixed routing rule, not an A/B test:

   | job group (IDs) | executor | why |
   |---|---|---|
   | Raw ads, first cut from raw footage (`RA-*`) | **Codex** | Dan: Codex is doing the better job turning raw footage into a finished video |
   | Organic long-form from raw (`RO-*`) | **Codex** | same |
   | Dedicated shorts filmed as shorts (`DS-*`) | **Codex** — Claude does nothing on these | they are raw-footage first cuts |
   | Ad vertical / vertical ≤0:59 (`AV-*`) | **Claude** | secondary cut of a finished video; the two are close, Dan assigned Claude |
   | Ad square / square ≤0:59 (`AS-*`) | **Claude** | same |
   | Shorts cut from a finished long-form (`SL-*`) | **Claude** | same |
   | `RX-01` (footage audit) | not in the queue | not an edit; fire by hand |

   Put this table in **one config file** so Dan can flip a row later. Dan called the raw-footage verdict "pretty sure"
   and the secondary-cut verdict "not conclusive", so the scoreboard (§7) keeps recording results per executor.
   No automatic re-routing: a change is Dan's call.
   ⚠ `RA-01` and `DS-04` are raw cuts already in progress with **Claude**, and `RO-01`/`DS-17` with Codex. Leave
   in-flight jobs with their current owner. Routing applies to new launches only.
2. **Placeholder flow (Dan, 2026-09-17).** AI-clip slots do not block the edit. The draft is built with placeholders,
   and Dan approves the cut and the clip frames in the same sitting (§5).
3. **Standing rules are unchanged:** two builds max on the machine, $5 AI-generation budget per video, start/end frame
   approval before any motion is generated, never upload or publish, every gate on the delivered file,
   independent review before Dan sees anything. Read `AGENTS.md` and `Handoffs/video-editing/00-RULES.md` in full.

## 3. What already exists (reuse, do not rebuild)

* `Handoffs/video-editing/jobs.json` — every job with `id, group, size, state, order`, plus a ready-made `claude`
  prompt and `codex` prompt. States: `ready, needs, blocked, in_progress, delivered, finalized, uploaded`.
* `scripts/edit-queue/queue.py` — the only writer of job state. It updates `jobs.json`, the `00-MASTER.md` row, and
  Dan's pinned page through the Drive status file. Procedure: `.claude/skills/_shared/edit-queue/README.md`.
  **Extend this script. Do not write a second state store.**
* `.claude/agents/ra-editor.md` and `ra-reviewer.md` — the Claude editor and independent reviewer definitions.
* `.claude/skills/_shared/deliver/gate.py` (GATE_VERSION 2.1.0, exact-match stamps) and
  `.claude/skills/_shared/qc_corpus/run.py` (must pass before any gate change).
* Work directories: `/Volumes/Extreme/_edit_work/<job-id>/`, one per job.
* **Headless launch, tested 2026-09-17 with a one-line prompt:**
  * **Codex: WORKS today.** `/Applications/ChatGPT.app/Contents/Resources/codex exec "<prompt>"` (codex-cli 0.154,
    already signed in) answered from a plain shell command. So Claude, or the dispatcher, can start a Codex job now.
  * **Claude: the program runs, but is NOT signed in.** Mac-native binary:
    `~/Library/Application Support/Claude/claude-code/<version>/claude.app/Contents/MacOS/claude` (2.1.270; supports
    `-p`). `claude -p` returned "Not logged in · Please run /login". **Dan must sign in once** (run that binary in
    Terminal, `/login`); no AI can enter credentials. ⚠ The path is versioned and changes when the desktop app
    updates: resolve the newest version folder at launch, or install the standalone Claude Code CLI instead. (The
    other binary, under `claude-code-vm/`, is a Linux build. Ignore it.)
  * Still to prove in Phase 0: a **full job** runs unattended with project permissions pre-granted (Codex sandbox/approval
    flags; Claude `--permission-mode` / allowed-tools settings). If it can't, stop and report. No screen automation.

## 4. The dispatcher

A plain script (`scripts/edit-queue/dispatcher.py`), run every 15 minutes by `launchd`. **It is not an AI and
costs nothing to run.** Each tick:

1. **Count slots by claims, not by processes.** An editing session spends most of its time thinking, so a `ps` check
   for ffmpeg undercounts and would launch a third build. A slot is taken by any job whose claim is live.
   Add to each job record: `claim: {by, pid, started, heartbeat}`. The launched session (or its wrapper) touches the
   heartbeat every few minutes. As a second check, also count the `ps` pattern from `00-RULES.md` §1.3, so Dan's own
   daytime sessions and hand-fired jobs still count toward the two.
2. **Stale claim** (no heartbeat for 45 min and the pid is gone) → mark the job `stalled` with a note. **Never
   auto-restart** a stalled job: a half-built directory needs a look first.
3. **Stop conditions — launch nothing if any is true:**
   * Dan's review queue already holds **4 items** (drafts + frame picks + finals, §6). Make the number a config value.
   * `/Volumes/Extreme` is unmounted or has < 150 GB free.
   * The executor hit its usage limit on its last launch (back off 2 hours, then try once).
   * A `PAUSE` file exists in `scripts/edit-queue/` (Dan's off switch), or the job's group is paused (§7).
   * Dan is at the machine (HID idle time < 10 min): drop to **one** automated slot rather than two.
4. **Pick the next job:** lowest `order` among jobs that are `ready` (or `frames_approved`, which goes first so
   half-finished videos finish before new ones start), whose group isn't paused, and that pass the eligibility
   test (§4a). Executor comes from the routing table. When both executors have eligible work, prefer one of each:
   it spreads the allowance burn, and one build's single-threaded Python overlaps the other's encoding.
5. **Launch headless** with the job's own stored prompt plus a fixed unattended preamble (§4b), in its own work
   directory, under `caffeinate`, logging to `/Volumes/Extreme/_edit_work/<job-id>/queue-run.log`. Claim first,
   launch second, so two ticks can never take the same job.
6. **The review runs inside the same slot** before the slot is freed (a watch pass counts as a build under the
   two-build cap). Cross-review: a Codex edit is reviewed by the Claude `ra-reviewer`; a Claude edit is reviewed by a
   fresh Codex session given the same reviewer brief. A "does not ship" verdict gets **one** automatic revision
   round, then the job parks as `needs` with the review attached.

### 4a. Eligibility for unattended running
Eligible: state `ready`/`frames_approved`, no open "Your calls" row in `00-MASTER.md`, source files present on disk.
Not eligible: anything `needs`/`blocked`; a job whose doc requires a fresh recording by Dan (for example RA-03);
anything that uploads.

### 4b. The unattended preamble (prepended to every launched prompt)
> You are running unattended; Dan is not available. Never ask a question: make the documented default choice and
> record it in `notes.md`. Never upload, publish, send a message or spend beyond this video's remaining $5
> generation budget. Do not generate AI motion clips: follow the placeholder flow in
> `Handoffs/handoff-20260917-overnight-edit-queue.md` §5. If you hit a real blocker, write `BLOCKED.md` in the work
> directory saying exactly what is needed, set the job to `needs` with `queue.py`, and exit. Do not add an
> `AI_COORDINATION.md` entry: the queue page is the record for queue-run jobs.

(The board stays short: the dispatcher keeps **one** ACTIVE line on `AI_COORDINATION.md` for the whole queue, not
one per job.)

## 5. The placeholder flow (two nights, two touches per video)

**Night 1 — the draft.**
* Build the complete edit: takes, audio, colour, captions, graphics, music. The voice track runs under the clip
  slots, so everything except the picture in those slots is final and reviewable.
* Fill every b-roll slot that needs **no approval** outright: Dan's own footage, owned assets, Pexels stock (audit
  for a repeated stock source across the whole timeline), and clips from the approved-clip library (§5c).
* For each remaining **AI slot**, generate **2–3 still options** for the start frame and a matching end frame
  (stills cost cents; they count toward the $5). **No motion is generated on night 1.**
* **The placeholder is the proposed start frame held as a still** for the slot's duration, with a burned-in chip:
  `PLACEHOLDER — clip 3 — <intended action>`. Dan judges the frame in context, against the line he is saying.
* Write `placeholders.json` beside the draft: per slot `id, in, out, action, frame_options[], chosen, status`.
* The file is named `DRAFT - …` and gets a **DRAFT stamp, never a PASS.** Run every gate row that can run and
  report results, but the verdict is DRAFT while any slot is open.
* State → `draft_review` (new state; add it to `queue.py` STATES and the page).

**Morning 1 — one sitting, two decisions.** On the review page (§6) Dan approves or revises the cut **and** picks a
frame option per slot (or rejects all, with a note). Cut approved first matters: slot lengths are locked before
any motion is paid for, so a restructured cut never wastes clips.
* Cut approved + all frames picked → `frames_approved`.
* Cut revised → back to the executor as a revision round; frames wait.
* A slot with every option rejected → new options generated the next night (replacement frames need approval again,
  per `AGENTS.md`).

**Night 2 — the finish.** Generate motion from the approved frames only. Check every AI shot frame by frame for the
known giveaways (memory `ai-clip-artifact-giveaways`: hands, breath smoke, fogging mirrors, morphing objects,
smudges). Paid retries count toward the $5; at the cap, stop and park the slot rather than exceed it. Drop the
clips in, add the `AI-GENERATED` chip, remove the placeholder chips, run the full gate + audio gate + independent
review. State → `delivered`.

**Morning 2.** The review page jumps straight to the clip slots; everything else was already approved.

### 5a. A placeholder can never ship
* Every delivery script already refuses a file without a PASS stamp, and a draft never gets one. That is the first lock.
* Second lock (Phase 2): add a `compliance:placeholder` row to the shared delivery gate that FAILS when an open
  `placeholders.json` sits beside the file or the placeholder chip is detected in any frame.
  ⚠ This is a gate change: `qc_corpus/run.py` must pass, `GATE_VERSION` must be bumped, and an exact-match version
  means **every older stamp then needs a re-gate.** Do it once, deliberately, and add a placeholder draft to the
  corpus as a must-fail entry. Do not block the Phase 1 pilot on it.

### 5b. Jobs with no AI slots
The 23 `AV`/`AS` jobs (and `SL`) inherit the master's clips. They run start to finish in one night: `ready` →
`delivered`. They are the pilot jobs.

### 5c. Approved-clip library
When Dan finalizes a video, its approved AI clips are copied to a shared library folder with a small index
(action, duration, source video, date). Night-1 builds check it before proposing a new AI slot.
⚠ Seed it only from clips Dan has approved in a finalized video. Four clips in his "AI clips for Muhammad" folder
have known artifacts (board, 09-15): do not import that folder wholesale.

## 6. The morning review page

One page Dan opens when he is back (an Artifact page, or a local page in the style of the existing review
galleries; the morning brief links to it). Newest first, three kinds of item:

* **Draft + frames** — the draft video, the reviewer's verdict in two lines, gate results, then each slot: its
  timestamp, intended action, and the 2–3 frame pairs to pick from. Buttons: approve cut / revise (dictated notes) /
  reject.
* **Final** — opens at the first clip slot, with a slot-to-slot jump. Approve / revise.
* **Parked** — jobs that need him, with the one-sentence reason from `BLOCKED.md`.

Writing Dan's verdict back: `queue.py` sets the state; his exact words go in the job note. A rejection or an approval
also becomes a regression-corpus entry in the same session, as `AGENTS.md` already requires. **`finalized` still
means Dan's words**, never a passed gate or a page click on a draft.

## 7. Scoreboard

`scripts/edit-queue/scoreboard.json`, one row per run: job, group, executor, reviewer verdict, first-pass gate result,
revision rounds, Dan's verdict and words, wall-clock hours, generation spend. A small summary on the review page.
**Circuit breaker:** when Dan rejects a cut for a systemic reason (audio, framing, colour, captions), pause that job
**group** for that executor until a session has fixed the cause, so he never wakes to five cuts with the same defect.

## 8. Build phases and acceptance

**Phase 0 — prove unattended runs (one evening, by hand).** Launch one `AV` job with Claude and one small raw job
with Codex headless, with the preamble, through the two binaries. Pass = both finish or park cleanly with no prompt
waiting for a human, state and logs correct, no third build started, nothing uploaded.

**Phase 1 — dispatcher, no-AI-slot jobs only.** `claim`/heartbeat/`stalled` in `queue.py`, the routing config,
`dispatcher.py` + the `launchd` job, stop conditions, the `PAUSE` file, cross-review, the scoreboard, and a first
review page. Cap 2–3 launches per night, size S only. Acceptance: unit tests for slot counting, double-claim,
stale claim, every stop condition and routing; a dry-run mode (`--dry-run` prints what it would launch); three
consecutive clean nights.

### 8a. Where Phases 0–1 stand (2026-09-17)
* **Codex headless: proven** on a permissions smoke test (work drive, project ffmpeg, `queue.py`, Drive via rclone,
  no prompt) with `-s workspace-write`, approvals `never`, network on, and the work dir + `~/.config/rclone` +
  `~/.cache` writable. A full raw job (**DS-01**, no AI slots) is queued to fire through `dispatcher.py launch-one`
  as soon as a build slot is free; its result lands on the review page and in `scoreboard.json`.
* **Claude headless: NOT proven.** `claude auth status` says signed out. Dan runs the binary once and types `/login`.
  Then: `python3 scripts/edit-queue/dispatcher.py launch-one AV-01` (the pilot job), read
  `/Volumes/Extreme/_edit_work/AV-01/queue-run.log`, and fix the flags in `config.json` if anything prompted.
* **Un-pause only after that run is clean:** `python3 scripts/edit-queue/dispatcher.py resume`. Then the three
  clean nights start counting.
* Tests: 41 unit + 3 end-to-end (fake editor) pass. One real bug found by the first real launch and fixed with a
  test: a job's own output path was read as a missing source.

**Phase 2 — placeholder flow.** `draft_review` and `frames_approved` states, `placeholders.json`, still-frame
placeholder rendering in the Codex ad/organic/shorts pipelines, the frame picker on the review page, night-2
finishing, the `compliance:placeholder` gate row with the corpus run and version bump, the clip library. Acceptance:
one `RA` job taken from `ready` to `delivered` across two nights with Dan touching only the review page.

**Phase 3 — widen.** M and L sizes, raise the nightly cap if Dan's review queue stays under its limit.

## 9. Risks

* **Same defect across many cuts** → low nightly cap at first, circuit breaker, cross-review.
* **Allowance burn overnight** → the usage-limit back-off; report tokens/spend per run on the scoreboard.
* **Two sessions in one directory** → one work directory per job, claim before launch, never run a script in
  another session's live build directory (`AGENTS.md`).
* **Mac or drive sleep** → `caffeinate`; the unmounted-drive stop condition.
* **Public repo** → commit scripts, docs and job state only, never media.
* **Dan's daytime work slowing down** → the at-the-keyboard rule drops automation to one slot.

## 10. Next action

Run Phase 0. Read `AGENTS.md`, `Handoffs/video-editing/00-RULES.md`,
`.claude/skills/_shared/edit-queue/README.md` and `scripts/edit-queue/queue.py` first.

## Starter prompt (Codex, GPT-6 Astra, effort high)

> Read `AGENTS.md`, then `Handoffs/handoff-20260917-overnight-edit-queue.md` in full, then
> `Handoffs/video-editing/00-RULES.md` and `.claude/skills/_shared/edit-queue/README.md`. Build the overnight edit
> queue: run Phase 0 first (prove one Claude job and one Codex job finish headless and unattended, and report
> exactly which binaries and permission settings made that work). If Phase 0 passes, build Phase 1: extend
> `scripts/edit-queue/queue.py` with claims, heartbeats and the `stalled` state, add the routing config with Dan's
> 2026-09-17 assignment (Codex = all raw-footage first cuts RA/RO/DS; Claude = all secondary cuts AV/AS/SL), write
> `scripts/edit-queue/dispatcher.py` with every stop condition and a `--dry-run` mode, the launchd job, cross-review,
> the scoreboard and the first review page, with tests. Do not start Phase 2 in the same session. Never upload or
> publish anything. Commit scripts and docs only, push, and tell me in plain language what now runs on its own and
> how I pause it.

**If Dan prefers Claude to build it:** Fable 5.1, effort high, same prompt. Phase 2 starter prompt: same opening
reads, then "Build Phase 2 (§5, §5a, §5c and the frame picker in §6); the gate change needs the corpus run and a
GATE_VERSION bump."
