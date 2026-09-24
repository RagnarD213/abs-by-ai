# Handoff: Phase 2 production pilot on RO-17 (2026-09-24)

**Status:** ready for preflight, not executed. This replaces the RA-11 pilot. RA-11's free-generation entry hook no
longer fits Dan's marketing direction. The overnight edit queue is paused by Dan's decision, and this handoff does
not authorize unpausing it.

## Purpose and choice

Prove the early asset-approval and placeholder workflow on one real video, while measuring its effect on editing
time, model use, provider cost and revisions. Use **RO-17, “3 Healthy Foods That Made Me Fat”**, an organic long-form
video from 9/23 source roll C1713. Its job spec is
`Handoffs/video-editing/RO-17-3-healthy-foods-that-made-me-fat.md`.

RO-17 was READY and unowned when this handoff was written. C1713 is mounted and is about 11 minutes long. C1711 and
C1712 are prompter false starts, not alternate completed takes. The planned cold open and food B-roll were not
filmed, so this edit has genuine source choices that need Dan's early approval. A single source roll keeps the pilot
more contained than the other ready long-form jobs. It is organic instruction, not an ad based on the retired free-
generation entry hook. Recheck ownership, readiness and source availability before claiming it.

This pilot must not add AI motion or stock just to exercise software. Use the best fitting owned footage or Pexels
clips with known rights. If the scene plan genuinely needs AI motion, follow the start/end-frame approval and $5
per-video cap. If every needed B-roll clip is already approved for the exact hash, trim, crop, duration and scope,
there is no new approval item and RO-17 is not a useful Phase 2 pilot. Stop and report that fact.

## Read first and protect active work

Read `AGENTS.md`, `.claude/skills/_shared/VIDEO-RULES.md`, `.claude/skills/_shared/ASSET-APPROVAL.md`,
`Handoffs/video-editing/00-RULES.md`, the RO-17 job doc, `$abs-edit-organic`,
`Docs/SHOOT_923_FOOTAGE_REPORT.md`, `scripts/edit-queue/README.md` and the current queue tests. Read the teleprompter
and scripts plus B-roll documents named in the job doc. Use the Dan-edited long-form script as a cross-check, but
verify what was actually spoken in C1713. Do not invent lines or portray stock footage as Dan.

Immediately before launch, re-read `AI_COORDINATION.md`, live `jobs.json`, the master-list row, dispatcher status,
claim and process checks. Do not touch RO-05, SL-04 or another active build. Use a dedicated RO-17 queue work
directory. Respect the two-build cap and current work budget. Preserve the global pause file, routing, group and
size limits, slots and nightly cap. Do not modify an active queue job to make the pilot fit.

The Phase 2 software was committed on 2026-09-18 (`de7631e`). Run its queue, approval-page and placeholder-gate
tests plus the full QC corpus before the real pilot. If they fail, repair only the isolated software defect before
claiming footage. Confirm the local approval page and C1713 source work. Build or reuse the roll sidecar once, then
reuse its transcript and lav evidence throughout both stages. `VIDEO-RULES.md` still contains an older sentence saying
Phase 2 is not built. Verify the current implementation and tests rather than treating that stale status sentence as
permission to skip the packet, queue state or placeholder gate.

## Keep Dan's queue pause intact

The dispatcher currently reports `PAUSE file present (Dan's off switch)`. Do not call `dispatcher.py resume` or
open all RO jobs for unattended launches. For this one requested pilot, use
`python3 scripts/edit-queue/dispatcher.py launch-one RO-17 --ignore-pilot-limits` for stage one. It applies the normal claim, slot, source and budget checks without
changing saved routing or unattended configuration. After Dan's asset decision, a fresh task or explicit continuation
may make one second `launch-one RO-17 --ignore-pilot-limits` call only when the job is `frames_approved`. Never use
`--no-budget`. The queue remains paused throughout.

The two deliberate launches test durable pause, approval state, finishing and reuse, but **do not prove automatic
unattended resume**. Report that limitation honestly. No AI session stays open to poll approval or rendering; the
queue keeps the state and its normal rendering/heartbeat process owns work once launched. Do not repeatedly ask for
status while waiting for Dan.

## Stage one: source choices early, editing continues

First map the spoken cut and the three food beats. Locate the unfilmed cold-open and B-roll cues from the actual
script. For each proposed new stock or existing B-roll slot, choose one best source and show Dan a 0.5-15 second
moving preview of the exact trim and crop, its spoken line, timeline slot, duration, rights and hashes. Use distinct
visible sources for distinct placements; different trims of the same stock clip do not count as variety. Verify
risky source choices with short moving previews before any full render. If AI motion is genuinely required, provide
one best start/end-frame pair, intended action and estimated cost before generating it.

Publish one compact, timeline-ordered approval batch on the existing local review page immediately after the scene
plan. Save schema-1 `placeholders.json`. The packet must be visible before stage one ends. While Dan decides, the
same editor continues take selection, voice, grade, graphics, captions and music with conspicuous exact-duration
placeholders. Do not generate unapproved AI motion. End with a DRAFT review copy and `DRAFT-DELIVERY.json`, never a
delivery PASS or independent final review.

RO-05's September 23 rejection sets a quality preflight for this edit. Match Muhammad's approved colour, actual
graphics and silent transitions on still comparisons and a 60-90 second finished sample before the full render. No
swipe or whoosh sound. Do not crop Dan's hair that the camera captured. Keep the sample within the normal render
budget, or stop rather than bypassing it. These are quality requirements, not extra supervisory review loops.

## Dan's decision and finishing

Send Dan one concise message linking the batch. Save his exact approval or rejection words per item. A rejected
item is replaced only after Dan responds; every approved item remains locked. Any material source, trim, crop,
action or slot-duration change needs a fresh decision for that item alone.

When all current items are approved and stage one has exited, confirm `frames_approved` and make the one manual
queue finishing launch. Recheck hashes and the video's remaining generation budget. Insert only the approved
clips, rebuild affected scenes and adjacent joins, and preserve unchanged scene renders, audio, transcript and
assets by fingerprint. Inspect any generated motion, especially its first and last second. Remove every
placeholder. Render the 16:9 master and SRT, run every normal gate, chronological picture/audio watch and one
fresh independent complete-candidate review. A rejection parks RO-17 with one consolidated fix list; it does not
start an automatic editor/reviewer loop. Send Dan the review copy. Do not upload or publish RO-17 in this pilot.

## Measurements and what counts as success

Write `PHASE2-PILOT-REPORT.md` in RO-17's work directory. Report stage-one editor, finishing editor and independent
reviewer model usage separately. Use available token totals and splits; write `null` and the exact reason for
missing measurements. Itemize provider charges, including retries and paid failures, or `usd: null` with a reason.
Separate AI work, human approval wait, render/queue wait and total elapsed. Count final-video revisions, approval
submissions and rejections, reviewer verdicts, moving previews and full renders. Identify reused versus rebuilt
scenes, audio, transcript and assets with paths and hashes. Report every gate row, placeholder result, full watch
result and Dan's final decision. Compare with another video only where real baseline data exists; otherwise say
`baseline unavailable`. Do not claim a percentage saving from estimates.

Success means the packet was visible before stage one ended, editing continued while approval was pending, no AI
session waited, no unapproved clip was generated or inserted, the final file contains only exact approved assets,
unchanged work was reused, all quality checks passed and one independent reviewer saw the complete final candidate.
Record the two manual launches and the still-paused dispatcher as a deliberate operating limit, not as automatic
resume success.

Seed the approved-clip registry only if Dan later finalizes RO-17. Frame or source approval alone is not enough.
Record exact final clip hashes, rights, source job, item ID, action/beat, trim/crop/duration, Dan's approval words
and finalized-video hash. Never put production media in Git.

Report remaining gaps: AI start/end-frame and motion approval if none was needed; automatic unattended resume
while Dan's pause remains; long-form edits with many more approval items; remote Artifact approval if only the
local page was used; and three consecutive clean unattended nights.

## Recommended model and ready-to-paste prompt

**Codex GPT-6 Astra, High effort** for the handoff executor because this is a quality-sensitive first cut of a
long-form video. Keep the queue's configured editor and the single independent reviewer unless Dan separately
changes routing. Do not spawn additional implementation agents.

> Read `Handoffs/handoff-20260924-edit-queue-phase2-ro17-production-pilot.md` and execute its preflight with Codex
> GPT-6 Astra at High effort. RO-17 is the candidate, not an unconditional claim. Recheck READY status, ownership,
> C1713, the real unfilmed B-roll needs, the two-build cap and all Phase 2 tests. Keep Dan's global queue pause in
> place. Use one normal `launch-one RO-17 --ignore-pilot-limits` for stage one, show Dan exact moving source previews
> early, then continue the edit with labelled placeholders and exit. Do not poll or generate unapproved motion.
> After Dan approves the exact items, make one manual queue finishing launch, rebuild only affected scenes and
> joins, run every quality gate and one independent final review, then send a review copy without uploading or
> publishing. Measure model use, costs, time, revisions, renders and reuse honestly. State that automatic
> unattended resume remains unproven while the queue is paused. Seed approved clips only if Dan finalizes RO-17.
