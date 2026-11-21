# Handoff 2 — repair the shared video checker for future videos

**2026-09-16 · READY, NOT EXECUTED. Recommended: GPT-6 Astra / High.**

Project root: `/Users/danielrose/Documents/Claude/Projects/Abs By AI`.

## Goal and separation from upload

Make the shared checking software understand the caption images, composite layouts and moving/baked labels used by our video pipelines. Future videos should receive real measurements and useful findings instead of false alarms or checks that cannot run.

Dan requested two independent handoffs on 2026-09-16: “1. To just upload the video as is” and “2. To fix the checking software so that future videos going forward can be checked.” The exact Ad 3 release is handled by `handoff-20260916-ad3-square-upload-as-is.md`; **this repair is not a prerequisite for that upload**. Do not upload, edit or replace any approved video, change ads or block the upload task. Its one-file release authorization is not a blanket rule for future videos.

Success means reliable shared checks wired into future production workflows, not simply making Ad 3's total turn green. An actual defect or missing evidence must remain visible and fail the applicable check.

## Starting evidence

Ad 3 full square R2.1 was creatively approved by Dan. Master:

`Muhammad Ad Videos/stop paying human trainers - ad 3/stop paying human trainers | claude | 1x1 R2.1 | ad 3.mp4`

SHA-256 `a46861e9d1e3c5f4f517f0b9018d5f129807b9b6f2408382a38492121788646b`.

Its shared v1.2.0 result is 24 measured PASS, 3 N/A, 2 FAIL, 6 NOT MEASURED. Structural checks passed 20/20 and verbatim audio passed. The current stamp verifier was rerun against the exact hash on 2026-09-16 and correctly refused its recorded FAIL. The earlier full report was not overwritten.

Known gaps to reproduce before fixing:

| Check | Observed behavior | Investigate / implement |
|---|---|---|
| `captions:graphic_clearance` | Requires ASS; this compositor uses PNG captions | Measure real caption-image alpha/ink, positions and timing against actual graphic regions, including animated states |
| `captions:sync` | Finds zero cues after its required silence gap | Support continuous speech and word highlighting with evidence from delivered audio and actual rendered caption timing |
| `framing:hair_top`, `headroom`, `centering`, `push_coverage` | Select zero main-scene frames | Recognize talking-head windows and measure in their own displayed coordinates, not against the entire composite |
| `compliance:labels` | 139 low/missing matches, no wrong labels; supporting inspection sees baked app labels | Diagnose scaling, motion, clipping/occlusion, transitions and source templates; support actual label trajectories while still detecting missing/wrong labels |
| `compliance:negative_events` | Any finding, even explicitly uncertain, becomes a generic FAIL | Report uncertainty distinctly from measured defects; preserve human review and genuine blockers without pretending to determine Google's decision |

These are starting hypotheses, not proof that every failed sample is a false positive. Inspect examples and quantify coverage; retain any real issue found.

## Read first and relevant files

- Current `AGENTS.md`, `AI_COORDINATION.md`; claim checker implementation ownership. Do not overwrite concurrent skill/corpus changes.
- `.claude/skills/_shared/deliver/README.md`, `gate.py`, `formats.py`, `common.py`, `checks/captions.py`, `checks/framing.py`, `checks/compliance.py`, `checks/process.py`.
- `.claude/skills/_shared/qc_corpus/README.md`, `run.py`, `corpus.json`; `.claude/skills/_shared/audio/README.md`.
- `.claude/skills/_shared/framing-motion.md` if present, plus current square/vertical adaptation instructions. Dan approved fixed horizontal positions for wider shots, retaining tight-shot tracking. Do not apply superseded “always track/centre/no wide shot” assumptions to intentionally wider framing.
- `Handoffs/handoff-20260911-video-quality-engine.md` and `handoff-20260912-vqc-phase3-watch-pass.md` for overlap. This is a focused repair of the rows above; do not silently absorb the entire unfinished watch-pass programme.
- `Muhammad Ad Videos/stop paying human trainers - ad 3/notes-square-r2.md` and `recipe-square-r2/verification/independent/r2_1-final-review.md`.
- `recipe-square-r2/verification/independent/r2_1/final-delivery-gate.json` in that same ad folder, its `plan.json`, `captions.py`, `app_label_templates.py`, `sqlabelplace.py`, `centering.py`, `qa_full_r2.py` and supporting reports. Review existing per-build checks as evidence; do not create another permanent fork.
- Native source/evidence: `/Volumes/Extreme/_edit_work/ad3-sq-r2/`. Treat this and the approved R1/vertical build folders as read-only. Work in a new scratch directory; missing SSD/input is an explicit blocker for that measurement.
- `output/ad3-square-setup-20260916/ASSESSMENT.md` explains the investigation so far. Its old upload hold is superseded, not a current instruction.

## Implementation sequence

1. **Reproduce and preserve the baseline.** Fingerprint inputs and snapshot reports before changes. Run relevant baseline rows in a scratch workspace; targeted debug runs are not delivery stamps. Inventory existing approved/rejected corpus entries and their missing inputs. The corpus already has uncommitted work from other sessions: merge only this task's additions and preserve other changes.
2. **Define one shared input contract.** Extend the existing plan schema to express caption PNG schedules, highlighted words, graphic regions/animation, talking-head window bounds and label transforms. Prefer actual renderer-exported data over duplicate handwritten timelines. Bind evidence/cache keys to the delivered hash, relevant plan/assets and gate version. Validate declared geometry against delivered pixels; metadata alone cannot prove the pixels exist.
3. **Implement PNG caption clearance and continuous-speech sync.** Keep the ASS path working. Measure actual visible ink, including outlines and motion, at relevant states. Do not invent an ASS approximation that differs from the delivered PNGs. Align/check against delivered speech and actual highlighting, not only intended script timestamps. Missing alignment, no valid cues or inadequate coverage stays NOT MEASURED. The existing 396/397 word check (one inherited “I” miss at 143.32 s) is supporting evidence; inspect its method rather than importing its PASS.
4. **Implement framing within layouts.** Cover full-screen talk, stacked talk/text and side-by-side phone layouts. Recognize photos/B-roll separately, map window coordinates back to delivered pixels and use actual displayed window edges for clipping/headroom. Preserve the independent hair-edge detector. Separate intentional wider fixed shots from tracking errors; do not force every wide shot to move or retroactively change the approved edit. Keep the existing single-camera path covered.
5. **Implement label matching through actual transforms.** Retain mutually exclusive AI/real labels and checks against face/abs obstruction. Use source references, declared transforms and independent delivered-pixel verification. Do not use a crop from the tested output as its own reference: that would let missing/wrong text pass. Measure transitions and readable dwell honestly, with explicit handling of partial occlusion. Do not shorten the tested intervals merely to omit failures or relax correlation bounds to fit Ad 3.
6. **Clarify human policy findings.** An uncertain bathroom-scene finding is not a confirmed platform violation. Preserve the original finding, file hash, timestamps and reviewer disposition; distinguish measured failure, missing measurement and “needs human review” in the report. Unresolved human review must not become an automatic PASS. Keep release authorization separate from measurement truth; do not generalize Ad 3's one-file instruction into an automatic waiver. If changing row aggregation/schema, update all readers and test their handling of old/new records. Do not promise that local software can certify Google eligibility.
7. **Prove the fixes catch defects as well as accept correct examples.** Add regression coverage described below, run the entire corpus, run the format audit, bump `GATE_VERSION`, and verify stale stamps/caches cannot be accepted. All threshold or calibration changes must be justified from existing approved/rejected evidence, never to make a file green.
8. **Wire future builds into the shared implementation.** Inventory the seven declared formats and actual active renderer/delivery entrypoints. Update relevant plan exporters/callers and their instructions so future builds supply the needed inputs automatically. Preserve organic longforms' no-burned-caption rule and format-specific N/A reasons. State which formats genuinely exercise each new path; do not claim unsupported formats were tested. Avoid deleting a legacy dependency another live build uses.
9. **Deliver tested code and operating instructions.** Commit/push task-owned source, tests and documentation to main; verify deployment outcome/live site per project rules. Keep media, test clips, private reports and credentials out of the public repository. Provide a plain-language report of corrected behavior, evidence, remaining limitations and the exact command future editing tasks should use. Update shared README/plan-keys/help, relevant skills and corpus notes; retire this handoff when the work is complete.

## Required validation

- Before committing any gate/threshold/setting change: `python3 .claude/skills/_shared/qc_corpus/run.py`. Preserve its full output and report coverage, known gaps and pending/unimplemented checks separately. A zero exit with missing media is not proof of the complete corpus. Do not invent gaps or remove expected failures to get a green run.
- `python3 .claude/skills/_shared/deliver/gate.py --audit` must answer every row for every format. Increment the version when behavior changes; old reports remain historical.
- Use Dan's approved/rejected examples as specified by each entry. Check whether R2.1's approval is already recorded before adding it; do not equate creative approval with expected PASS on all unrelated/policy rows.
- Add focused positive/negative fixtures for PNG caption collisions, early/late highlights in continuous speech, clipped hair inside a window, intentional fixed wide shots, missing/wrong/moving labels, invalid or stale geometry, missing inputs and uncertain policy findings. Controlled defect clips belong in scratch space and must be labelled test fixtures, not altered approved masters or fake Dan rejections.
- Prove the existing ASS and full-screen paths still work. Include representative square and vertical composites; test other affected formats where the new path is wired.
- Run the revised measurements on a scratch copy of the exact approved R2.1 export and one representative future-style build from another video. Preserve original media and sidecar reports. Publish honest per-row coverage/findings; if a genuine Ad 3 defect remains, report it without editing the video or interfering with its separately authorized upload.
- Respect the global two-build limit for renders, transcription and QC. Inspect processes before each expensive batch; do not run inside another session's live build directory. Keep editor audio untouched. No paid generation is needed by default; existing review-spend rules apply if review calls are justified.

## Completion standard

The affected future pipelines generate valid checker inputs automatically; the new paths measure the delivered video and catch their known bad examples; the full corpus and format audit are documented; versioned enforcement remains honest; instructions explain technical failures versus review findings in plain language. Missing evidence still cannot masquerade as a pass. A schema change alone or an Ad-3-only workaround does not complete this task.

## Exact first action and starter prompt

First read the files above, claim only checker ownership, and reproduce the six missing measurements plus representative label failures in an isolated workspace. Record the baseline before implementing anything.

Read `/Users/danielrose/Documents/Claude/Projects/Abs By AI/Handoffs/handoff-20260916-video-checker-repair.md` completely and execute it. Repair the shared checker for future videos: PNG captions and word timing, framing inside composite layouts, moving/baked labels, and clear reporting of uncertain policy findings. Preserve approved videos, prove the changes against approved/rejected examples and the full regression corpus, and wire them into future builds. This work must not delay the separately authorized Ad 3 upload.
