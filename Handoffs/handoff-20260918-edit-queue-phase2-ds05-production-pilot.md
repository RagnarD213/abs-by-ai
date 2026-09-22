# Handoff — Phase 2 production pilot: DS-05, measurement and approved-clip seed (2026-09-18)

**Status:** superseded on 2026-09-22. DS-05 is owned by Muhammad under the 22-shorts milestone and must not be edited by
the AI queue. Use `Handoffs/handoff-20260922-edit-queue-phase2-ra11-production-pilot.md` instead. This historical DS-05
plan is not authority to claim or edit his active job.

## Goal, in plain language

Prove the new workflow on one small real video:

1. Send Dan the two planned AI clips near the start.
2. Keep editing the full short with obvious placeholders instead of waiting.
3. Let the queue stop, wait without an AI session, resume after Dan approves, insert the exact approved clips, and
   finish the ordinary quality process.
4. Measure whether it saved work and create the first reusable approved-clip records only after Dan finalizes the
   finished video.

The default pilot is **DS-05 — “Why Having Abs Is Better Than Being A Fat Millionaire.”** It is short, currently READY,
and requires two new AI motion clips with a clear frame-approval decision. Its job doc is
`Handoffs/video-editing/DS-05-abs-beat-being-a-fat-millionaire.md`.

## Preflight — do not disturb active work

Read `AGENTS.md`, `.claude/skills/_shared/VIDEO-RULES.md`, `.claude/skills/_shared/ASSET-APPROVAL.md`,
`Handoffs/video-editing/00-RULES.md`, the DS-05 job doc, `$abs-edit-organic`, the vertical-short instructions it links,
and `scripts/edit-queue/README.md`.

Then re-read `AI_COORDINATION.md`, live `jobs.json`, the dispatcher status and process/claim checks in
`00-RULES.md` §1.3.

Use DS-05 only if all are true at launch:

- it is still `ready`, unclaimed, not listed ACTIVE and has no existing in-flight work directory;
- its source roll is mounted and the queue has a legal free slot;
- the Phase 2 state, page, resume and placeholder-gate tests are already green;
- no one else owns or is editing DS-05.

If any condition is false, do not change or move that build. Choose the next unowned, READY, size-S raw ad/organic job
that has at least one new approval item, or stop and report that no safe representative exists. The pilot gets one
normal dedicated queue work directory; never reuse another video's directory. Do not alter launchd, routing or slot
limits to force it through.

## The exact DS-05 approval package

The spoken cut and scene plan come first. Immediately after that plan, propose one best start/end pair for each:

1. **Ripped Dan in a generic dating profile getting a strong positive match.** Use Dan's approved/look-appropriate
   image, `AI-GENERATED`, no Hinge logo, name or trade dress. Show the intended UI/action and exact slot duration.
2. **An invented overweight wealthy man in a generic dating profile getting rejected.** He must not be a real person
   presented falsely, and the treatment must avoid humiliating/degrading imagery under the existing Google negative-
   events standard. No real dating-app logo or trade dress. Show intended action and exact slot duration.

The before picture and pool-shoot picture are still images already specified by the job; verify their hashes,
identity/label rules and approval/reuse status. Do not add stock merely to exercise the software. If the actual scene
plan legitimately needs a new stock or existing-B-roll insert, include its exact 0.5–15 second moving trim/crop preview
and rights note in the same package; otherwise record that the pilot's stock-preview branch was covered only by the
isolated software tests and remains unproven on real footage.

Show one strong pair per AI clip, not a gallery. Alternatives are allowed only for a genuine unresolved creative
choice. Record item cost estimates and the video's cumulative prior spend before submitting the batch. No motion
generation before approval.

## Run the pilot through the queue

### Stage one

- Launch through the normal queue, using its configured **Codex GPT-5.6 Sol / High** editor and budget. Do not keep
  this task alive to watch it; the queue owns heartbeats, rendering and waiting.
- The asset package must become visible on the existing review page before the stage-one editor finishes. Record the
  packet-created and stage-one-ended timestamps.
- Continue the real voice cut, take selection, colour, captions, graphics, audio and music with exact-duration,
  conspicuously labelled placeholders. Reuse the already available 8/28 transcript/lav evidence and any exact approved
  assets rather than rebuilding them.
- Stage one exits with a DRAFT review copy and valid packet. It does not run AI motion, claim PASS, call the independent
  reviewer, upload or publish.

### Dan's decision

Send Dan one concise message pointing to the two AI frame pairs, intended actions, durations and estimated new/total
cost. His exact words must be saved per item.

This is the only unavoidable human pause. Do not poll, repeatedly check status or keep an AI session open. The local
page and ordinary dispatcher handle it. If Dan rejects an item, preserve every approved item and prepare a replacement
only for the rejected ID after his explicit words are recorded; do not restart the whole edit.

### Finishing

After the page has moved the job to `frames_approved`, let the ordinary dispatcher launch finishing. Verify hashes and
generate only the approved motion within the video's remaining $5 cap. Inspect each generated clip in motion,
including its first and last second. Insert the exact clips, rebuild only their scenes and adjacent joins, remove all
placeholder labels, and preserve the unchanged cut/audio/transcript/assets by fingerprint.

Then run every normal full-file gate, chronological picture/audio watch, and exactly one fresh independent review of
the complete placeholder-free candidate. A reviewer rejection parks the job with one consolidated list; there is no
automatic fix/re-review loop.

Send Dan the finished review copy. Do not upload, schedule, queue or publish DS-05. It remains an organic video and any
future upload must be Private before Blotato; that later setup is a separate task.

## Measurements — report what exists, never guess

Write a small `PHASE2-PILOT-REPORT.md` in the DS-05 work directory and summarize it in chat. Include:

| measurement | required reporting |
|---|---|
| model usage | stage-one editor, finishing editor and independent reviewer separately; available token totals/splits, otherwise `null` + exact reason |
| paid providers | each frame/motion call, retry and paid failure; dollars where available, otherwise `null` + reason; cumulative per-video total |
| time | stage-one AI work, human approval wait, finishing AI work, renderer/queue wait and total elapsed kept separate |
| revisions | final-video revision round, asset-approval submissions, rejected/replaced items and reviewer verdict count |
| renders | short previews and full renders counted separately |
| reuse | scenes, voice/audio, transcript and assets: reused/rebuilt/mixed with paths and hashes |
| waste avoided | unapproved motion calls, discarded full renders and rebuilt unaffected scenes; use measured zero/counts, not hypothetical dollars |
| quality | all gate rows, placeholder check, watch result, independent verdict and Dan's final decision |

Compare with the nearest similar completed size-S raw short only where the scoreboard has real data. If there is no
valid baseline, say `baseline unavailable` and why. Do not claim a percentage token or dollar saving from estimates.

## Seed the approved-clip library only after final approval

Frame approval is not enough. After Dan watches and finalizes DS-05:

- add only the exact final inserted clips and their immutable hashes to the Phase 2 approved-clip registry;
- include the source job, item ID, action/beat tags, duration, format, provider/provenance, rights, Dan's exact approval
  words/date and the finalized DS-05 hash;
- record whether a future reuse requires the same duration/crop/meaning or can be safely trimmed;
- verify a registry lookup returns both DS-05 clips by action/beat without opening the original project.

If Dan does not finalize the video, add nothing. Record the reason and leave the registry unchanged.

## Success criteria

- The approval package timestamp is earlier than stage-one completion; editing continued while Dan had not yet acted.
- No AI motion was generated before frame approval and no AI session waited or polled.
- The queue performed the pause and resume; there was no hand-edited state jump except Dan's approval submission.
- The final file contains the exact approved assets, no placeholder chip, no DRAFT/PASS confusion and no unapproved
  source change.
- Unchanged work was reused; only affected scenes/joins were rebuilt.
- One independent complete-candidate review ran after all placeholders were gone.
- Usage, provider cost and revision metrics are present where available and explicitly unavailable elsewhere.
- Dan receives a normal review copy. Nothing is uploaded or published.
- The library is seeded only if Dan finalizes the result.

If the pilot exposes a software defect, pause DS-05 safely with its work intact. Fix only the narrow defect in an
isolated test first, re-run the queue/gate tests and full corpus if a gate changed, then resume. Do not use the live
video as the debugging sandbox and do not lower quality requirements to complete the pilot.

## What remains unproven unless this pilot exercises it

Call these out plainly in the final report:

- real stock/existing-B-roll moving-preview approval, if DS-05 legitimately needs none;
- long-form projects with many approval items;
- cross-machine/remote Artifact approval if only the Mac mini's local page was used;
- exact token savings when a model or CLI does not expose per-session usage;
- three consecutive unattended nights, which remains the broader queue acceptance test.

## Recommended executor

**Codex GPT-5.6 Sol / High.** Use the queue's configured owner and the existing one-review checkpoint. Do not spawn
additional agents. The human frame decision comes from Dan; the one independent reviewer comes only after the finished
candidate exists.

## Ready-to-paste starter prompt

> Read `Handoffs/handoff-20260918-edit-queue-phase2-ds05-production-pilot.md` and run the Phase 2 production pilot with
> Codex GPT-5.6 Sol at High effort, but only after the Phase 2 automation handoff is committed and all tests/corpus are
> green. Recheck ownership and claims; use DS-05 only if it is still READY, unowned and has no existing build. Launch it
> through the normal queue, publish the two AI start/end-frame choices early, continue the edit with exact labelled
> placeholders, then exit and let the queue wait without AI polling. Save Dan's exact per-item decision, generate only
> approved motion within the cumulative $5 cap, resume through the dispatcher, rebuild only affected scenes/joins, run
> every gate/watch and one independent final review, and send the review copy without uploading or publishing. Produce
> `PHASE2-PILOT-REPORT.md` with honest model usage, provider cost, time, revision, render and reuse measurements, marking
> unavailable values as null with reasons. Seed the approved-clip registry only if Dan finalizes the finished video.
