# Overnight edit queue

Keeps up to two video edits running from `Handoffs/video-editing/jobs.json` with nobody at the keyboard, and hands
Dan a short review page. Design and Dan's decisions: `Handoffs/handoff-20260917-overnight-edit-queue.md`.
Built 2026-09-17–18 (Phases 0–2), including the two-stage asset-approval flow.

## For Dan, in plain language

* **What runs on its own:** every 15 minutes a small script (not an AI, costs nothing) looks at the job list. If a
  build slot is free and nothing says stop, it starts the next job with the right tool (the table below), lets a
  *different* AI review the completed candidate once, then either puts the video on your review page or parks it
  with one consolidated correction list. There is no automatic fix/re-review supervision loop.
* **Your review page:** http://127.0.0.1:8830 (on the Mac mini). Watch, then Approve, Send back, or Reject. Your words
  are saved exactly as you say them. While a first edit is still running, the same page can show one early batch of
  AI frame pairs and exact moving B-roll previews. One submission decides every current item.
* **Pause everything:** `python3 scripts/edit-queue/dispatcher.py pause`. Or create an empty file named `PAUSE` in
  `scripts/edit-queue/`. A job that is already running finishes; nothing new starts. Undo with `... dispatcher.py resume`
  (or delete the file).
* **Remove it completely:** `scripts/edit-queue/install.sh uninstall`.
* **See what it would do right now, without doing it:** `python3 scripts/edit-queue/dispatcher.py status`.
* **Per-job work budget:** each job now has a time limit and a cap on full renders. If it runs out, the queue parks
  the job as `needs`, keeps every file in its work folder, and never restarts it on its own. Change the S, M and L
  numbers in `config.json` under `budget`. A specific job can override that row with a `budget` object in `jobs.json`.

It will never launch anything when: the PAUSE file exists · 4 videos are already waiting for your review ·
the Extreme drive is unplugged or under 150 GB free · both build slots are busy (your own sessions count) · it
already started 3 jobs tonight · the tool it needs is signed out or hit its usage limit in the last 2 hours.
While you are using the Mac (keyboard or mouse in the last 10 minutes) it uses one slot, not two.

## Who edits what (`config.json` → `routing`; Dan, 2026-09-17)

**FROZEN 2026-09-18 → 2026-09-24 11:00 CT: every group below routes to Codex for both edit and review** (Dan's
Claude allowance freeze — `Handoffs/handoff-20260918-claude-video-freeze-and-codex-routing.md`). The table's
"normal" tool/reviewer columns are what to restore after the reset; until then `config.json` → `routing` sends
`AV`/`AS`/`SL` to `codex` too, and `review.reviewer_for` maps both `codex` and `claude` to `codex` — so a `codex`
edit is reviewed by a **fresh, separate `codex exec` process** (never the editor's own session; see
`build_command` in `eq_common.py`), not by Claude. No code path can select `claude` as editor or reviewer while
frozen; the only way to run Claude on a job is a human passing `dispatcher.py launch-one <ID> --executor claude`
by hand, which is not something the queue does on its own.

| jobs | tool (normal, resumes 2026-09-24) | reviewer (normal) |
|---|---|---|
| `RA` raw ads, `RO` organic long-form, `DS` dedicated shorts (all raw-footage first cuts) | **Codex · Sol / high** | Claude `ra-reviewer` |
| `AV` ad verticals, `AS` ad squares, `SL` shorts from a long-form (all secondary cuts) | **Claude · Opus / high** | a fresh Codex session |
| `RX` | never queued | |

Models (Dan, 2026-09-17): edits run Opus / high and Sol / high. A review session uses the reviewing tool's same
`model` / `effort` (there are no separate review keys); a Claude review runs as the `ra-reviewer` agent.
Flip a row by editing `config.json`. Nothing re-routes itself; the scoreboard only records.
**Pilot limits (`config.json` → `unattended`):** groups `AV/AS/SL`, size `S`, 3 launches a night. Phase 2 now supports
raw cuts' approval needs; expanding the pilot groups remains an explicit operating decision, not an automatic code change.

## Files

| file | what it is |
|---|---|
| `queue.py` | the only writer of job state. New: `claim`, `heartbeat`, `release`, `stall`, the `stalled` state, a write lock |
| `config.json` | routing table and every number |
| `dispatcher.py` | the 15-minute tick: `tick`, `tick --dry-run`, `status`, `pause`, `resume`, `pause-group`, `resume-group`, `launch-one` |
| `runner.py` | runs one job inside its slot: one editor → one cross-review → `delivered` or parked |
| `asset_approval.py` | validates and atomically updates schema-1 `placeholders.json`; recomputes every relevant hash |
| `pre_render_check.py` | validates risky-source hashes and a real 0.5–15 second moving preview before the full render |
| `preamble.md`, `reviewer-brief.md` | the fixed text put in front of every unattended edit / review |
| `review_page.py` | the review page server (port 8830) and a static snapshot |
| `scoreboard.json` | one row per run: tool, reviewer verdicts, gate, revision number, model usage, provider cost, hours and Dan's verdict |
| `launchd/`, `install.sh` | the two background jobs: `com.absbyai.edit-queue` (tick) and `com.absbyai.edit-queue-review` (page) |
| `approved-clips/` | tracked registry schema/instructions; the live empty registry is under ignored work storage |
| `tests/` | unit and end-to-end tests with temporary files and fake executors; no model allowance or real media |

Logs: `~/Library/Logs/absbyai-edit-queue/`; per job `/Volumes/Extreme/_edit_work/<JOB>/queue-run.log`.

## How a slot is counted

By **claims**, not processes: an editing session spends most of its time thinking, so counting ffmpeg would start a
third build. `claim: {by, pid, started, heartbeat}` sits on the job record; the runner touches the heartbeat every
5 minutes and holds the claim through the review. Builds that belong to nobody's claim (Dan's sessions, hand-fired
jobs) are counted from the `00-RULES.md` §1.3 process pattern, grouped by parent process; over-counting is the safe side.
A claim with no heartbeat for 45 minutes **and** a dead pid becomes `stalled`. A stalled job is **never restarted
automatically**: look at its work directory, then `queue.py release <ID>` and `queue.py set <ID> ready`.

Every launch writes `BUDGET.json` in its work folder. `pre_render_check.py` reserves one full render only after the
source-preview evidence passes, then refuses the next render after the cap. The runner uses the size row's edit clock
and review clock. If either clock expires, the scoreboard outcome is `budget_exceeded`, the job becomes `needs`, the
claim is released, and the work folder stays intact. This is different from `timeout`, which is the unchanged absolute
10-hour safety ceiling, and from `session_failed`, which means the editing program ended unexpectedly. A hand-fired
`dispatcher.py launch-one <ID>` uses the same budget. Add `--no-budget` only for an intentional manual exception; it
is logged and still cannot exceed the 10-hour outer ceiling.

A job is skipped when: its state isn't `ready` or `frames_approved`; it has an open "Your calls" row in `00-MASTER.md`; its ID appears in
`AI_COORDINATION.md` ACTIVE; a work directory with a build in it already exists (`ra01`, `ds-17`, `AV-01` spellings);
a source file named above the doc's `## Deliver` heading is missing; it carries `"unattended": false`; or its group is
paused. `dispatcher.py status` prints the reason per job.

## Two Macs: the router decides where a job starts (2026-11-14)

Dan has two Macs: the M6 (his own, 2 edit slots) and the M2 Pro (headless edit machine, 3 slots, holds the drives
and this queue's `work_root`). The dispatcher runs on one Mac (today the M2; its LaunchAgent is disabled on the M6).
Before every launch it asks the two-Mac router, `.claude/skills/_shared/editroute/editroute.py pick JOB --queue`:

- The router names this Mac: the decision is recorded (it holds the slot for 30 minutes) and the job launches here.
- The router names the other Mac (the job's work folder is there, or this Mac's edit slots are full) or says `wait`
  (both full): nothing launches for that job this tick; the next eligible job is asked instead. The tick log says
  `NOT HERE: JOB -> executor: router sends it to the m6. <reason>`.
- No answer from the router, or a Mac `hosts.json` does not know: nothing launches. An unattended launcher never guesses.

Unattended launches are routed as the class QUEUE, which `editroute/hosts.json` sends to the M2 first. The slot
counting below still applies on top (the queue's own two-job limit and the foreign-build count). `launch-one` asks
the router too; `--ignore-router` starts the job on this Mac anyway, for when Dan names it. The PAUSE file is
checked first: a paused queue never calls the router. Tests: `TwoMacRouting` in `tests/test_edit_queue.py`.

## The contract with a launched session (`preamble.md`)

Work in `/Volumes/Extreme/_edit_work/<JOB>/`. The runner writes `WORK_PACKET.json`: one short change list plus the
approved elements that must survive. The editor records fingerprint-backed reuse in `REUSE_REPORT.json`, and checks
risky source choices with short moving previews in `PRE_RENDER_CHECK.json`, then runs `pre_render_check.py` before a
full render. Finish by writing `DELIVERY.json` there, or `BLOCKED.md` for a real blocker. Do **not** set `delivered`:
the runner does that only after the single independent reviewer writes `QUEUE-REVIEW-1.md` with `VERDICT: SHIP`.
`DOES NOT SHIP` parks the candidate as `needs` with one consolidated review attached; Dan's later revision request
starts a new bounded candidate.

If the scene plan needs new AI motion, stock or existing B-roll, stage one writes `placeholders.json` immediately,
then completes a fully timed `DRAFT - ...` cut with conspicuous exact-duration placeholder chips. It writes
`DRAFT-DELIVERY.json`, never `DELIVERY.json`, never runs the independent reviewer, and releases its claim into
`draft_review`. Approval during a live stage-one claim changes only the packet; after stage one exits, all-current
approval becomes `frames_approved`, which is launchable ahead of new work. A fresh finishing session revalidates the
hashes in the same work directory and same logical scoreboard row, builds only approved clips and affected scenes/
joins, runs the full gates, and only then spends the one independent review. A rejection stays parked—there is no
automatic regenerate/resubmit loop. Jobs with no approval items retain the one-stage path.

The Drive export uses schema 2 and includes the labels `DRAFT — asset choices waiting for Dan` and
`ASSETS APPROVED — finishing queued`, plus `assetApprovalSchema: 1`. A remote Artifact should consume those fields;
it must not invent another packet or decision schema.

The scoreboard records the revision number, available paid-provider charges, and one model-usage row per editor or
reviewer session. Codex's text footer supplies a per-session total when present; its input/output/cache split and any
session whose tool omits usage stay explicitly `null`/unavailable instead of being guessed from account-wide usage.

## Exactly how the sessions are launched (Phase 0 findings, 2026-09-17)

**Codex: headless with no prompt.** codex-cli 0.154.0-alpha.6.2, already signed in.

```
/Applications/ChatGPT.app/Contents/Resources/codex exec -C <repo> -s danger-full-access \
  -c 'approval_policy="never"' -c sandbox_workspace_write.network_access=true \
  --add-dir /Volumes/Extreme/_edit_work/<JOB> --add-dir ~/.config/rclone --add-dir ~/.cache \
  -m gpt-5.6-sol -c 'model_reasoning_effort="high"' -   # prompt on stdin
```
⚠ **`-s workspace-write` does not work for an edit.** It passed a smoke test (work drive, project ffmpeg, `queue.py`,
Drive via rclone once `~/.config/rclone` was writable) but the first real job, DS-01, parked within two minutes:
that sandbox denies `/bin/ps`, and every edit must run `ps` to respect the two-build cap. `danger-full-access` is
what Dan's own `~/.codex/config.toml` already uses, so a queue session has the same rights as a hand-fired one.
That first run also proved the park path end to end: `BLOCKED.md` → `needs` with the reason → claim released →
scoreboard row, nothing built, nothing uploaded.

**Claude: headless launch works; the first run died on the account's usage limit.** Dan signed in on 2026-09-17
(~18:00). The first real launch (AV-01, 2026-09-17 20:14, fired by hand from another session) started a session that
worked with **no prompt** — nine minutes of real cut-scanning in the work dir — and then ended with
`You've hit your monthly spend limit · … your session limit resets 9pm`: Dan's daytime sessions had already spent the
5-hour window the queue shares. Three findings, all fixed 2026-09-18 by the proof session:
1. That wording matched none of `usage_limit_patterns`, so the run was filed `session_failed` → `stalled` instead of
   `usage_limited` → `ready` with the 2-hour back-off. Patterns extended (`spend limit`, `session limit`, `limit resets`,
   `hit your monthly/weekly`) with the real message as a test.
2. Commit `3403c6b` (18:29) had overwritten Dan's model decision in `config.json` (Fable/high + Sol/medium instead of
   **Opus/high + Sol/high**), so the run used Fable, and one test pinned the wrong value. Both restored.
3. A run that dies this way leaves a half-used work dir, which the eligibility check reads as "in flight or
   half-built"; nothing restarts it. Recovery: move the dir to `_edit_work/_queue-failed/<run id>/`, then
   `queue.py set <ID> ready`. The dispatcher **cannot see remaining allowance before launching** — `claude auth status`
   only reports sign-in — so the back-off is the only guard; expect a lost launch on any night Dan's day work drained the
   window before 9 pm.
**Re-run 2026-09-18 03:13 → 04:15 (AV-01, Opus/high): the Claude editor leg is proven.** 1.03 h wall, no prompt,
no third build (the dispatcher's own ticks read 0 other builds throughout), nothing uploaded, $0 generated, masters
held in the work dir, `DELIVERY.json` honest: gate FAIL on two rows that are the approved master's own faults, so the
runner parked it as `needs` **without** spending a review (`DELIVERY gate must be PASS before independent review`).
The review leg was then proven by hand on that candidate with the runner's exact command and brief (fresh Codex
Sol/high, 8 min, 224,913 tokens): a valid `QUEUE-REVIEW-1.md`, `VERDICT: DOES NOT SHIP`, same defects. Still open:
* A Claude `-p --output-format text` session exposes **no token counts** (`model_usage` = unavailable) and writes
  **nothing to the log until it ends** — progress is only visible from files appearing in the work dir. Switching to
  `--output-format json`/`stream-json` would fix both; the log parsing must change with it.
* **By-hand `launch-one` runs count toward the nightly cap** (4 since Thu noon after the proof), so the tick launches
  nothing until the next noon roll-over. Intended, but worth knowing on a proof night.
* **`SL-01`/`SL-02` docs say "show Dan the list and wait for his picks"**; an unattended run cannot honour that, so
  both carry `"unattended": false` (2026-09-18). Flip them once Dan has picked. With that, no job is eligible until a
  new AV/AS/SL size-S job is ready — the queue is live but idle.
* The 20:14 launch was fired by hand from outside the proof session (not the dispatcher, not its waiter; no Claude or
  Codex transcript on this Mac holds the confirmation line). Unattributed.

The flags, proven on that launch and the 2026-09-18 03:13 re-run:

```
<newest claude-code/*/claude.app/Contents/MacOS/claude> -p --permission-mode bypassPermissions \
  --add-dir <work dir> --model fable --effort high --strict-mcp-config \
  --disallowedTools "Bash(node scripts/youtube/*),Bash(python3 scripts/blotato/*),Bash(node scripts/ads/*)"
  [--agent ra-reviewer for a review]                                     # prompt on stdin
```
`bypassPermissions` is what this project's `.claude/settings.local.json` already grants. `--strict-mcp-config` with
no MCP config means no connectors at all (no Blotato, Gmail or Drive tools to post or send with). The versioned
folder changes when the desktop app updates, so the newest one is resolved at launch.

**launchd:** a background job started from `~/Library/LaunchAgents` reads `~/Documents`, `/Volumes/Extreme`, `ps` and
`ioreg` with no macOS privacy prompt (checked on the first tick).

## Open operating ends

* Dan's pinned Edit Queue artifact must consume Drive status schema 2 and present `stalled`, `draft_review` and
  `frames_approved` with the labels above. The local page is the decision authority until that remote UI is updated.
* A verdict on the review page marks the scoreboard row `corpus_entry: owed`. The revision session is told to record
  Dan's words in `qc_corpus` first; an approval's corpus entry still needs a session to write it.
* Acceptance still owed: a full Claude job headless, and three consecutive clean nights.

## Launcher repair, November 14, 2026

The overnight dispatcher remains PAUSED. M2 is the sole native dispatcher owner; M6 stays disabled.
Executable discovery uses validated absolute candidates and both version/build-level desktop paths.
Codex now resolves GPT-6.1 Sol/high, verified in each local client catalog. Readiness reports binary,
model/effort, non-billable login and pause policy separately; quota is not inferred from login.
The standalone Claude CLI currently requires sign-in even though Claude desktop sessions work.
No pilot, subscription upgrade, fallback API spend or resumed dispatcher was authorized.

Claims are durable before spawn. A failed spawn removes its fixture claim and retains the ready job.
A missing cross-reviewer parks the finished candidate and records the reason, without substituting
another model. Existing pilot groups, three starts/night, backlog stop at four, 150 GB Extreme stop
and two-hour allowance backoff remain. Tests run as individual processes because their old module
globals collide under one unittest-discovery process; fixture routers never query real job ownership.

## Explicit overnight batches (2026-11-15)

The named batch is installed **disabled** on both Macs. General backlog discovery remains blocked by `PAUSE`.
Dan's first test night begins only after he says go. A passed launcher canary is readiness evidence, not a video delivery.

- `python3 scripts/edit-queue/batch.py preflight`: compare installed scheduler source with pushed main and with the other Mac; require four real launchd session replies per Mac from the current launcher/configuration.
- `batch.py enqueue NAME /absolute/spec.json`: copy immutable briefs to the M2 ledger. It reports **registered** until `batch.py receipt NAME` confirms both Macs' ticks logged it, then **queued**. Enqueue never enables production.
- `batch.py start NAME`: run preflight again, then enable only the named rounds. Use only with Dan's go.
- `batch.py stop`: one M2 control file stops new starts on both Macs, including backlog discovery. Existing workers finish. An unreachable M6 cannot claim anything new; it keeps its running work and saves outcomes locally until it can sync.
- `batch.py status`: authoritative M2 state. `~/.absbyai-batch/morning-report.md` and `.json` on the M6 are saved every two-minute tick, including unknown/unreachable owners.
- `batch.py takeover JOB`: required before a chat resumes batch-owned work. Claimed work cannot be taken over, including an unreachable owner. A queued or terminal round can be taken over; keep its saved work folder.
- A chat that must wait copies a self-contained brief and uses `batch.py enqueue-chat JOB --round N --brief /absolute/brief.md --title 'Recognizable title' --size S --kind SFC --executor codex --need-gb 10 --target 'first review'`. It does not run `editroute.py wait`. Registration is not a running editor. If new starts are disabled, explicitly report that the work is queued and disabled.

A spec contains `{"jobs":[{"id":"DS-106","round":1,"title":"Protein Snack Can","size":"S","order":1,"kind":"SFC","executor":"claude","need_gb":20,"target":"first review only","chroma":true,"brief":"brief.md"}]}`.
Brief paths are relative to the spec or absolute. Preserve the film's existing editor. Placement is fixed at enqueue:
existing work owner, otherwise M2 for long-form/chroma/drive-bound work, otherwise either Mac. Longest size first,
then Dan's order. Active chat production cannot be transferred by enqueue.

The ledger is `~/.absbyai-batch/NAME/{manifest.json,state.json,briefs/}` on the M2, outside Git, with one flock for
all batches. Each local tick pulls its own claim; no cross-Mac start requests or receipts exist. Workers use the
existing editcap slot and renderq work-folder allocator. They preserve the original folder during recovery and
allowance pauses. No volume-share or old ps-based two-build cap applies to a batch. Named rounds bypass the pilot's
three-start and four-review limits. There is one automatic recovery after an unexplained runner exit, and at most
three total allowance attempts, with shared backoff. An orphaned recorded session is stopped and its exit confirmed
before recovery. Unreachable owners are never reassigned.

Every ordinary exit records delivered, delivered-unreviewed with reason, needs-dan with question/link, or blocked
with reason/next action. Exit zero alone proves nothing. Final candidates need current exact-file delivery gate
stamps, preserved efficiency evidence and an independent cross-review. Reviewer timeout/no verdict gets one fresh
session, then unreviewed; a valid rejection parks the cut and findings without a fix loop. Disclosed uncertainty is
an explicit verdict, never an invented request for a new approval. A missing managed review mirror stays in the
owner's durable outbox until the M6 link opens. The local slot is released meanwhile. No publishing occurs.

Queue wait, active/review hours and allowance pauses are recorded per round. Idle-slot minutes are sampled at ticks,
not an exact continuous measurement. No ten-video throughput promise is supported before the real test nights.
Finalized/uploaded jobs are removed from the editcap review register by `queue.py`, and old completed review entries
are hidden by both the register and desk. Other unmatched reviews stay visible with their wait age.

Tests: run each `scripts/edit-queue/tests/test_*.py` in its own Python process; several legacy tests set import-time
environment overrides and cannot safely share one `unittest discover` interpreter. Batch tests use temporary ledgers.

Independent Fable 5.2 review and repair receipts: `Docs/overnight-batch-review-20261115/` and
`Docs/OVERNIGHT_BATCH_IMPLEMENTATION_20261115.md`. The 31 ledger and 18 worker tests include real process-group
interruption with a fake executor and offline outcome sync; they are not a substitute for the held real test night.
Capacity/storage waits do not exhaust the bounded infrastructure-start budget. Storage waits defer only that job on
that Mac for ten minutes. Executor allowance backoff is shared, doubles from two to four hours, and is not extended
by another job merely waiting for the same allowance. The old `editroute.py wait` remains usable while batches are
disabled; after activation, newly submitted `chat-*` batches inherit current enablement. Existing armed waiters or
render-only live jobs cannot be transferred into a batch.
