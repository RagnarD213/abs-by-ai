# Handoff — Edit Queue Phase 2: early asset approval, placeholders and automatic resume (2026-09-18)

**Status:** ready to execute. **Software and tests only:** do not start, alter or render a real video in this handoff.
This implements the workflow Dan approved on 2026-09-18 inside the existing queue; it does not replace the queue or
create a second editing framework.

## Goal, in plain language

Let the editor show Dan all new AI clips and B-roll choices near the start, while it keeps building the rest of the
video with labelled placeholders. The editor then exits instead of waiting. When Dan approves the choices on the
existing review page, the queue wakes the job, inserts only those approved clips, runs the normal quality checks, and
uses one independent reviewer on the complete video.

This should save time and model usage by preventing expensive motion generation and full renders around a source Dan
does not want, while preserving every existing quality requirement.

## Read first

1. `AGENTS.md` and `.claude/skills/_shared/VIDEO-RULES.md` in full.
2. `.claude/skills/_shared/ASSET-APPROVAL.md` — the authoritative packet and placeholder contract.
3. `.claude/skills/ad-edit/SKILL.md` and `.claude/skills/longform-edit/SKILL.md`.
4. `Handoffs/video-editing/00-RULES.md`.
5. `scripts/edit-queue/README.md`, then `queue.py`, `dispatcher.py`, `runner.py`, `review_page.py`,
   `pre_render_check.py`, `preamble.md`, `reviewer-brief.md` and the existing tests.
6. `Handoffs/handoff-20260917-overnight-edit-queue.md` §5. This handoff updates that early design where the newer
   `ASSET-APPROVAL.md` is more specific: stock and existing B-roll now need exact moving previews, and the default is
   one best AI frame pair rather than several options.

Re-read `AI_COORDINATION.md` immediately before touching queue files. If another session owns the queue or a queue job
is running, do not restart services or edit that job's work directory. Code and isolated tests may proceed only when
they cannot alter the running process; otherwise wait for the claim to clear.

## Decisions already made

- One editor owns the cut. One fresh, independent reviewer sees the complete, placeholder-free candidate once. No
  automatic editor/reviewer/fixer loop is added.
- One compact, timeline-ordered approval package goes to Dan immediately after the scene plan. The editor continues
  the cut with exact-duration labelled placeholders; it never sits alive and polls for approval.
- AI motion cannot be generated before its start/end frames and intended action are approved.
- Every new stock or existing-B-roll choice needs a 0.5–15 second moving preview of the exact source trim, crop and
  basic treatment, with source-rights evidence and hashes. A still contact sheet is not enough.
- Unchanged, hash-matching approved assets are reused without another approval. A material frame, source, trim,
  action or duration change makes only that item pending again.
- `placeholders.json` schema version 1 from `ASSET-APPROVAL.md` is the durable source of truth. Chat text is not state.
- Keep the planned queue state names `draft_review` and `frames_approved`. The page may label the latter “Assets
  approved”; retaining the stored name avoids needless migration of the existing config and design.
- A placeholder draft is always DRAFT. It can never receive or inherit a delivery PASS, reach the independent final
  reviewer, be uploaded or be published.
- Existing $5-per-video generation authorization, cost tracking, gates, corpus rules, format bounds, two-build cap,
  claims, work budgets and publishing rules remain unchanged.

## Build this in the existing system

### 1. Add the two queue stages

Extend the current state machine and display mappings:

- `draft_review`: the placeholder cut and approval packet are waiting for Dan. It is not launchable and counts toward
  the review-queue limit.
- `frames_approved`: all current packet items are approved and the stage-one draft is complete. It is launchable and
  stays ahead of `ready`, as `config.json` already specifies.

Export both states through the existing Drive/status JSON. Update the local review page and its static snapshot. Do
not change the remote Artifact in this software handoff; report the exact state/schema update it will need as an
explicit remaining manual step if no supported code/API path exists.

### 2. Make the packet safe and machine-readable

Add a small queue-owned module rather than duplicating JSON handling across scripts. It must:

- create, read, validate and atomically update `placeholders.json` schema 1;
- accept only files inside the claimed job's work directory or explicitly allowlisted source roots;
- recompute every referenced hash at approval and again before insertion;
- preserve Dan's exact approval/rejection words and timestamp;
- preserve already approved items when another item changes;
- refuse partial, stale, duplicate-ID or path-escaping packets with a clear error;
- report total estimated generation cost and the video's prior paid spend before Dan submits approval;
- never infer approval from a file merely existing.

Keep the packet shape in `ASSET-APPROVAL.md`. Add fields only when the software truly needs them, document them, and
retain backward-readable schema 1.

### 3. Put the early package on the existing review page

As soon as a running editor writes a valid packet, the page should show a separate **Asset choices** card even while
the editor continues the rest of the cut. In timeline order, show:

- slot, spoken beat, intended action and duration;
- AI: one best start frame and one end frame, plus estimated item and per-video cost;
- stock/existing B-roll: the exact 0.5–15 second moving preview, source/path, trim/crop and rights note;
- whether the item is new or an exact previously approved reuse;
- approve/reject controls and one compact note box per rejected item;
- one submission button for the batch.

Approvals are item-specific. A rejected item needs words. Submission atomically saves the decision; it must not
silently approve an omitted item. Serve only packet-listed, hash-checked media through the page's existing local-only
media route.

Dan may approve while stage one is still running. In that case, save the approval but leave the job `in_progress`.
When stage one ends, the runner chooses `frames_approved` if the packet is fully approved or `draft_review` otherwise.
If Dan approves after stage one ended, the submission itself moves `draft_review` → `frames_approved`. The background
dispatcher then handles the next launch; no AI process or agent status loop waits for it.

For a rejection, store the exact rejected IDs and words and park at `draft_review`. Do not automatically generate new
choices or start a repeated approval loop. A later explicitly requested replacement run may change only rejected
items; approved items stay locked.

### 4. Split the runner into stage one and finishing

Keep one runner and one work directory:

- **Stage one (`ready`)**: the editor writes the scene plan and packet early, exposes the package, then continues take
  selection, voice, timing, colour, captions, graphics and music with labelled exact-duration placeholders. It writes
  a hash-bound `DRAFT-DELIVERY.json` (or equivalently documented marker) and exits. It does not write a final
  `DELIVERY.json`, run the independent reviewer, generate AI motion or claim PASS.
- **Finishing (`frames_approved`)**: a fresh editor session resumes from `WORK_PACKET.json`, `placeholders.json`, the
  draft marker and reuse fingerprints. It verifies hashes, generates only approved AI motion within the remaining
  per-video budget, inserts exact approved stock/B-roll, rebuilds only affected scenes and boundary joins, removes
  every placeholder, and writes the normal final `DELIVERY.json`.
- **No approval items**: a job with no new AI/stock/existing-B-roll choice keeps today's one-stage path. Do not force a
  pointless human stop.

At both launches keep the existing short `requested_changes` and `approved_elements` lists. Do not wipe prior audio,
transcripts, assets, scene renders or packets. A finishing launch is a resume, not revision round 1, and should not
inflate the revision count.

Only after a valid placeholder-free `DELIVERY.json` with PASS may the existing independent-review branch run. Its one
verdict remains SHIP or DOES NOT SHIP, with no automatic fix/re-review loop.

### 5. Add a hard placeholder delivery check

Add `compliance:placeholder` to the shared delivery gate, all relevant format contracts and the queue's delivery
validation. It must be tied to the exact delivered-file hash and fail when:

- a referenced `placeholders.json` is missing, unreadable or not `complete` for a video that used this flow;
- any item is pending/rejected, lacks approved selected hashes or lacks a final inserted-clip hash;
- the final render or watch evidence still contains a known `PLACEHOLDER — <id>` chip;
- packet, draft, approved source or final-clip hashes no longer match.

Use the existing plan/log mechanism and the shared watch scan; do not invent a second delivery gate. The process
record is the primary deterministic check, and the final chronological watch pass remains the visual backstop.
Because this changes a gate, bump `GATE_VERSION`, add focused tests/fixtures, register the row in the corpus runner and
run the full regression corpus. Never relax another bound or mark the row not-applicable merely to make the corpus
green. If the corpus cannot prove the new row without corrupting approved entries, stop and report the exact gap.

### 6. Create the approved-clip registry, empty

Create the smallest useful index under the existing ignored media/work storage, with a tracked README/schema if
needed. Do not copy production media into Git. A row needs: content hash, source job/video, packet item ID, exact trim,
dimensions/fps/duration, action/beat tags, rights/provenance, Dan's approval words/date and finalized-video hash.

The queue may search this registry before proposing generation. Nothing enters it merely because its frames were
approved: the clip must appear unchanged in a video Dan later finalizes. The production pilot handoff seeds the first
real entries.

### 7. Preserve and extend efficiency reporting

The scoreboard/review page must keep showing:

- one model-usage row for the stage-one editor, finishing editor and independent reviewer;
- available per-session/per-video tokens, with unsupported splits as `null` plus reason — never estimate from account
  totals;
- itemized paid-provider costs, including failed paid attempts, or `usd: null` plus reason;
- human approval wait separately from AI work time;
- final revision count, asset-approval submissions/rejections and full-render count;
- reused vs rebuilt scenes, audio, transcript and assets.

Stage one and finishing belong to one logical video revision even though they are separate sessions.

## Tests — isolated and free

Extend the existing fake-executor tests. Use a temporary `EDIT_QUEUE_DIR`, temporary config, scoreboard and work root,
`EDIT_QUEUE_NO_DRIVE=1`, and synthetic images/videos only. Never read or write the live `jobs.json`, live scoreboard,
`/Volumes/Extreme/_edit_work/<real job>` or an active build.

Required coverage:

1. Stage one publishes a packet before it finishes its draft, then exits to `draft_review`; no reviewer runs.
2. Approval while stage one is running is stored but does not steal/change its claim; on exit it becomes
   `frames_approved`.
3. Approval after exit atomically moves `draft_review` → `frames_approved`; the next ordinary dispatcher tick launches
   finishing exactly once.
4. Partial approval, rejection without words, stale hashes, changed trim/duration, duplicate IDs and path traversal
   are refused or remain waiting as appropriate.
5. Finishing reuses the same work directory and evidence, runs no unapproved motion, and rebuilds only affected
   synthetic scenes/joins.
6. A complete clean packet reaches final review once. An open packet, remaining chip or DRAFT gate never reaches the
   reviewer and never yields `delivered`.
7. A job with no approval items follows today's single-stage path without regression.
8. Model usage/cost/revision/wait/reuse fields survive both sessions and unavailable measurements remain explicit.
9. The new gate's focused fixture fails a placeholder draft and passes the same synthetic video after replacement;
   all queue tests, delivery-gate tests and the full QC corpus pass.

Also run `dispatcher.py tick --dry-run` and `dispatcher.py status` against isolated fixtures. No provider call, real
motion generation, real render, upload or publication belongs in this handoff.

## Proof required

- A short state-transition trace: `ready → in_progress → draft_review → frames_approved → in_progress → delivered`.
- Timestamps proving the asset package became visible before stage-one completion.
- Test output proving zero reviewer launches before the placeholder-free final candidate and one afterward.
- The synthetic placeholder fail/pass result, gate version bump and green corpus output.
- One sample scoreboard row with stage-one, finishing and reviewer usage/cost fields, including honest nulls.
- `git diff` showing targeted queue/shared-gate/docs/test changes only. No live job record, production video, routing,
  executor model, slot count, budget or quality threshold changed.

Update `scripts/edit-queue/README.md` and the relevant shared editing instructions in plain language. Commit and push
only this implementation. No absbyai.com application code is involved; live verification is the local page, test
suite, dry-run dispatcher and corpus proof. Do not restart launchd under an active claim.

## Out of scope

- Running the real pilot, requesting Dan's asset decisions, spending provider money or seeding real clips.
- Changing which model owns a video, adding supervisors, raising render/token limits, or lowering a quality bar.
- Uploading or publishing any video.
- Rebuilding the remote Edit Queue Artifact by hand if no supported API exists; report that remaining UI compatibility
  step plainly.

## Recommended executor

**Codex GPT-5.6 Sol / High.** This is careful queue, state-machine and gate work with an existing Python test harness.
Do not spawn additional agents; use the existing fake-executor tests and one fresh independent review only where the
production workflow already requires it.

## Ready-to-paste starter prompt

> Read `Handoffs/handoff-20260918-edit-queue-phase2-asset-approval-automation.md` and execute it end to end with Codex
> GPT-5.6 Sol at High effort. Build Phase 2 inside the existing edit queue: early timeline-ordered AI-frame and exact
> moving B-roll approval on the current review page, durable hash-bound `placeholders.json`, stage-one placeholder edit,
> queue-owned exit/wait/resume, finishing that rebuilds only affected scenes, and a hard `compliance:placeholder` final
> gate. Preserve one editor and one independent complete-candidate reviewer, all current quality gates and the $5/video
> cap. Use only temporary queue/config/scoreboard/work directories and fake executors for this handoff; do not touch a
> real job or active build, do not spend provider money, and do not upload. Run every queue/gate test and the full QC
> corpus, update the docs, commit and push only the targeted files, and report any remote Artifact update that remains
> manual.
