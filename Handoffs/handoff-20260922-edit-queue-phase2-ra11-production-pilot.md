# Handoff: Phase 2 production pilot on RA-11 (2026-09-22)

**Status:** ready for preflight, not executed. This replaces the DS-05 pilot handoff because Muhammad owns DS-05. Do not
start RA-11 until its ownership, source, claims, queue eligibility and current product claims pass the checks below.

## Goal

Prove the early asset-approval workflow on one real, small video without disturbing another editor's work. The editor
shows Dan the exact proposed moving app-demo insert early, continues the ad with a timed placeholder, exits, and lets
the queue wait. After Dan approves, the queue resumes the same work, replaces only affected scenes, runs all quality
checks and one independent final review, and sends a review copy. Measure usage, cost, time, revisions and reuse.

**Pilot:** RA-11, “What Would You Look Like With Abs?” Job spec:
`Handoffs/video-editing/RA-11-what-would-you-look-like-with-abs.md`. It is a size-S short ad from the mounted C1667
8/28 roll. At handoff writing, the job record and master list say READY, no owner appears on the coordination board,
and no RA-11 work directory was found. Recheck all three at launch. The script explicitly calls for a product image-
generation screen capture. A real Dan lockscreen insert is optional only if a suitable real source exists.

RA-11 is a better safe candidate than DS-05 because it is unowned and has a genuine existing-B-roll choice. It is a
limited pilot: do not invent AI motion, stock or a lockscreen shot merely to exercise software. If the approved app
insert already has the exact hash, trim, crop, slot and scope recorded, the editor may reuse it without another approval.
If that leaves no new approval item, this is no longer a valid Phase 2 pilot. Stop and select another unowned job.

## Read and verify before a claim

Read `AGENTS.md`, `.claude/skills/_shared/VIDEO-RULES.md`, `.claude/skills/_shared/ASSET-APPROVAL.md`,
`Handoffs/video-editing/00-RULES.md`, the RA-11 job doc, `$abs-edit-ad`, the vertical-short rules it links, and
`scripts/edit-queue/README.md`. Re-read `AI_COORDINATION.md`, live `jobs.json`, the master row, dispatcher status,
claims and process list immediately before launch. Respect the two-build cap. Use a fresh dedicated queue work
directory. Do not touch Muhammad's DS jobs or any active build directory.

The Phase 2 software was committed on 2026-09-18 (`de7631e`). Re-run its queue, page and placeholder-gate tests and
the full QC corpus before the real pilot. Verify the local review page works and the source roll is mounted.

**Queue eligibility needs a narrow fix before this pilot.** The unattended dispatcher currently permits AV/AS/SL
size-S jobs, not RA. A hand-fired `launch-one RA-11` can start stage one, but would not prove automatic finishing
after approval. Do not mark that manual path as a successful auto-resume test. First add and test a single-job pilot
allowlist for RA-11 within the existing dispatcher, or choose a different naturally eligible unowned job with a real
new approval item. The allowlist must preserve the current routing, slots, nightly cap, review limit, claim checks,
budget and group eligibility for every other job. Prove with isolated fake-job tests that only RA-11 gains eligibility
and that its approved finishing run launches once on an ordinary tick. Commit and push only this narrow queue change
before claiming real footage. Do not open the whole RA group to unattended launches.

If RA-11 becomes owned, its source is unavailable, a current claim exists, the software tests fail, or no safe
single-job eligibility path exists, do not launch. Report the exact blocker and leave the job READY.

## Content-specific preflight

The app demonstration must show the same person before and after. The known older recording of a different man may
be used only with that man's own result. A fresh Dan recording must come from the real product and must not consume
user credits on a test path. Reject banned email-capture and side-by-side before/after screens. Verify the current
offer before using the spoken “completely free” claim in an ad; if the claim is no longer accurate, stop and ask Dan
about a truthful cut or rerecord rather than silently shipping it. Keep the filmed CTA intact. Ads are never posted
organically; this pilot performs no upload or publication.

## Early approval package and placeholder cut

After the spoken cut and scene plan, create one compact, timeline-ordered packet on the existing local review page:

1. The exact 0.5-15 second moving preview of the proposed app-demo source, trim, crop and basic treatment, with
   source rights, identity, content hashes, spoken beat and exact slot duration.
2. A real lockscreen moving preview only if that optional source genuinely exists and is needed. Otherwise omit it.
3. One best start/end-frame pair, intended action and estimated generation cost only if the finished scene plan
   legitimately needs new AI motion. Frame approval must precede motion generation. Do not add motion for the test.

Record the item and approval state in schema-1 `placeholders.json`. The packet must be visible before stage one ends.
The editor then continues take selection, colour, audio, music, captions and graphics with an exact-duration,
conspicuously labelled placeholder for each pending insert. Reuse the C1667 roll sidecar, transcript, lav decisions
and unchanged scene assets by hash. Stage one exits with a DRAFT review copy and no delivery PASS or independent
review. Do not keep an AI session alive to wait or poll Dan.

Dan sees one concise batch with the exact clips and intended placements. Store his exact words per item. A rejection
changes only that item; already approved items remain locked. A material change to source, trim, crop, action or
duration goes back for approval.

After all current items are approved, the ordinary dispatcher launches finishing. Recheck packet and source hashes,
insert exactly the approved clips, rebuild only affected scenes and adjacent joins, and remove every placeholder.
Produce the required 9:16 ad and its 16:9 version from the same approved edit. Run all normal full-file gates,
chronological picture and audio review, and exactly one fresh independent complete-candidate review. A rejection
parks the job with one consolidated fix list; it does not start a supervisory loop. Send Dan the review copies, but
do not upload, schedule, queue or publish either version.

## Report and acceptance

Write `PHASE2-PILOT-REPORT.md` in RA-11's work directory. Report stage-one editor, finishing editor and reviewer
model usage separately, with available token totals and splits. Put `null` and the exact reason for unavailable
values. Itemize paid-provider calls, retries and failures, or `usd: null` with a reason. Keep human approval wait,
AI work time, render/queue wait and total elapsed separate. Count final-video revisions, approval submissions,
rejected items, reviewer verdicts, short previews and full renders. Identify reused and rebuilt scenes, audio,
transcript and assets with paths and hashes. Report all quality-gate rows and Dan's final decision. Compare with a
similar prior short only if real baseline data exists; otherwise say `baseline unavailable`.

Success requires packet visibility before stage-one completion, no AI motion before frame approval, no AI polling,
queue-owned automatic pause and resume, a placeholder-free final file with exact approved assets, unchanged work
reused, all gates passing and one independent final review. Never claim a percentage saving from estimated usage.

If Dan finalizes RA-11, add only exact final inserted clips and their immutable hashes to the approved-clip registry,
with source job, item ID, action/beat, duration, crop, format, rights, approval words/date and finalized-video hash.
Frame approval alone does not seed the library.

Call out what remains unproven: AI start/end-frame and generated-motion approval if the edit needs none; stock source
selection if it uses only the app capture; long-form projects with many items; remote Artifact approval if only the
local page was used; and three consecutive unattended nights. The pinned remote Edit Queue Artifact still needs to
consume status schema 2. The local page is the approval authority until that is verified.

## Recommended executor and starter prompt

**Codex GPT-5.6 Sol, High effort.** Use the existing single editor and one independent reviewer. Do not spawn
additional agents for implementation. Dan alone makes the asset approval decision.

> Read `Handoffs/handoff-20260922-edit-queue-phase2-ra11-production-pilot.md` and run its preflight with Codex
> GPT-5.6 Sol at High effort. RA-11 is the candidate, not an unconditional launch: recheck that it is READY,
> unowned, source-mounted and genuinely needs a new approval item. First prove the existing Phase 2 tests and add
> only the narrow RA-11 queue eligibility needed for automatic dispatcher resume, with isolated tests, commit and
> push. Never open the whole RA group or touch Muhammad's DS edits. Then run the pilot through the normal queue:
> show the exact app-demo moving preview early, continue the cut with a labelled placeholder, exit while Dan
> decides, resume once on approval, rebuild only affected scenes, run all gates and one independent final review,
> and send review copies without uploading or publishing. Produce an honest `PHASE2-PILOT-REPORT.md`; seed the clip
> registry only after Dan finalizes the video. If any preflight condition fails, stop safely and report it.
