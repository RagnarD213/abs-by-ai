# Two-Mac editing optimization execution

November 14, 2026, Central. One Codex infrastructure owner on M6; the existing editors retained their films. Authorized source: `Handoffs/handoff-20261114-two-mac-video-editing-optimization-execution.md` and the approved final plan. No production film was designated urgent, moved, approved or published by this work.

## Current outcome

The repairs are installed on both Macs. Both priority modes passed in fresh Codex and Claude desktop sessions on each physical Mac, using disposable registries. M6's scheduler features are enabled after the old render processes drained. M2's final activation is held until its older whole-edit waiters finish naturally. A one-shot watcher in the executing chat is checking the same activation guard. **The overnight dispatcher remains paused; M6's dispatcher remains disabled.**

The first activation guard covered render holders/tickets but missed long-running whole-edit waiters. On finding live M2 waiters for EXDEMO-3MORE and DS-39, I disabled M2's new features, added explicit waiter-version/PID/start checks to the guard, and tested the refusal path. No production priority reservation had been created, no editor was stopped and no files were lost. The older waiter processes retain their original code until they exit. Their owners still showed Running in Claude at the follow-up.

## Shipped behavior

- Long contact sheets hold one slot through the decoder's exit; long scans use heavy, up to 20 seconds uses quick. Audio extraction plus Whisper holds light through its actual children. Nested calls inherit the existing slot. The decode/filter arguments, global FFmpeg thread-injection default, key mathematics, quality gates, grade and approved media stay unchanged.
- Scheduler version 5 survives holder publication and finish/history records. Missing historical versions are unknown metadata. Scheduling normalizes known job aliases without renaming paths or revealing blind arms.
- Ordinary priority is carried through the host line, whole-edit admission and render tickets. Ready normal projects earn an owed turn after two compatible bypasses. Another ready project precedes a second heavy step for the same project; a lone project can use spare capacity.
- Dedicated M6 reservations let running steps finish, park saved edits and yield a whole-edit slot for a third job. Milestone, owner review, cancellation, expiry and recorded PID/start mismatch clear the reservation; saved owners/places return. M2's own queue is independent. This is integrated into the existing locks and registries, not a new dispatcher.
- One measured short recipe can borrow stranded capacity across the light/quick lanes, at most once before the compatible waiting heavy starts. Unknown/long recipes cannot borrow. A recipe overrun finishes, is recorded and disqualifies future borrowing. No timer kills work.
- Whole-edit caps remain M6 two/M2 three; render budgets remain M6 six with recent input or unknown presence, ten after 30 minutes confirmed idle, M2 eight. Night alone no longer increases M6's allowance. CPU allowances remain cooperative, not OS-enforced thread caps.
- Routing and workdir share incremental storage checks and outstanding commitments: 80 GB internal, 30 GB Extreme, 100 GB Expansion remain. Existing folders must have growth room. Full, stale/asleep, missing and network storage cannot become new working capacity. Missing occupancy and unavailable primary route lock fail closed for automatic placement. Combined promotion rechecks the specific job instead of `gather(None)`.
- Review mirroring validates port/root/job provenance before copying, stages separately, then rechecks under a destination lock before refreshing a cache.
- The paused launcher discovers validated absolute executables, checks model/effort against the installed client, separates login/policy/quota readiness, records claims before spawn and retains a ready job on spawn failure. A missing cross-reviewer parks the completed candidate instead of substituting a model. Pilot scope, three starts/night, backlog stop at four, 150 GB Extreme stop and two-hour backoff remain.

## Archive safety and real restore proof

Both private archive workers are installed and scheduled for 2:15 AM, with the actual Expansion volume UUID pinned. The M2's older checkout copy was reconciled with the newer installed baseline before replacement. No manual production archive run occurred.

Removal requires the actual attached volume identity, a complete destination file-set/hash comparison, source stability, an atomic synced manifest and checked index read-back, a fresh reference check and an independently rehashed second copy. A retry keeps the original full manifest, including after partial source removal. Repeated verification does not duplicate the index. Retained sources are reported separately from moves. Board/editcap reviews have no age expiry; registered durable review roots/media also protect their source folders. Missing rule/library/process/review evidence blocks removal. Repository and installed keep lists both apply. Restore verifies the original manifest and reconstructs links; unresolved links are an incomplete restore.

A disposable M6 folder with a space in its name, nested bytes and a relative link was copied over real SSH to the attached Seagate, re-read, indexed, removed only with a verified second copy, and restored to a new space-containing path. Both original file hashes and the restored link matched. That real test exposed an SSH restore quoting bug which local-only fixtures had missed; it was repaired and the real restore then passed. **Production sources removed: zero.** No existing failed destination was cleaned or reorganized.

## Verification by Mac

| Evidence | M6 | M2 |
|---|---|---|
| Fresh Codex invocation | `$priority-edit`, GPT-6.1 Sol/high, PASS | `$priority-edit` through real SSH, GPT-6.1 Sol/high, PASS |
| Fresh Claude invocation | `/priority-edit`, desktop Opus 5.5/high, PASS | `/priority-edit`, actual m2 SSH environment, Opus 5.5/high, PASS |
| Ordinary priority and dedicated-M6 fixture | PASS | PASS; M6 policy simulated on the physical M2 |
| Running step, third-job parking, restored owners, milestone/cancel/expiry/crash | PASS | PASS |
| Physical M2 progress during M6 fixture reservation | Separate real-SSH disposable command completed while the M6 fixture reservation remained active | PASS |
| Route/priority/resume unit fixtures | 67 passing after the whole-edit waiter guard | 67/67 after the final guard |
| Render-queue process fixtures | 57/57; four real CPU/RSS stress assertions deliberately not run in the final safe mode | 57/57, same explicit stress omissions |
| Edit-slot fixtures | 29/29 | 29/29 |
| Archive fixtures | 16/16 | 16/16 after the final reference guard |
| Contact-sheet child lifetime | PASS; slot still held after actual sleeping child exit | PASS |
| Launcher fixtures | 59 policy, 11 fake end-to-end, 5 repair, 2 review-page, 7 asset tests passed | Same suites passed before the final archive/waiter-only guard update |

The original three M6 editcap CLI failures were test isolation defects: fake jobs were accidentally looking up real ownership. The ownership guard remains; the fixtures now use explicit private host data. Three older launcher expectations still assumed September's executor routing. Tests now reflect the approved routing, and generic cross-executor tests set their intended routing explicitly. Fake launcher tests use a fixture router, not real production job IDs. Launcher suites run as separate processes because their old module globals collide under one discovery process.

The private client harness uses five isolated state directories and two occupied slots. Its “checked preview” is a fixture marker, not film QA. Fresh clients explicitly reported this distinction. No real waiter was awakened as a test and no real queue claim or film status was created by a fixture.

## Measured effects and limits

A six-core competition fixture used real sleeping commands with fixed short durations. On M6, the selected light check started at **3.039 s with borrowing off**, **0.292 s with borrowing on**; the heavy follower started at **2.061 s versus 2.109 s**. The next quick task waited until that heavy opening, proving the shared one-loan bound. This is simulated scheduling evidence, **not a film speedup**. On physical M2, the selected light check started at **2.117 s versus 0.357 s**, and the heavy follower at **2.116 s versus 1.976 s**. The same shared-loan bound passed there.

The mirrored fixture was an unchanged 1920×1080 three-second excerpt copied from an existing real-footage review export. HTML returned 200, media ranges 206, and owner/mirror/final-copy size and SHA-256 matched. Another job/source on the occupied port was refused before refresh; a stale page refresh arrived correctly. Twelve local page requests measured about **0.63 ms median, 11.98 ms worst**. This is a local HTTP proxy, not a before/after measurement of Dan's UI responsiveness.

Chrome checks entered silent mode and verified actual mute before playback, seeking and reload. Final observed state: paused, unmuted, readyState 4, sound ready for the next deliberate Play. No audible listening pass occurred. No Mac volume, microphone, audio routing or export audio setting changed. The shared live review hub was not killed and neither Mac was rebooted to manufacture recovery evidence.

A real-SSH disconnect fixture retained its owner PID/start, saved checkpoint and exit 0 after the original connection was terminated. It started once. A pre-start unreachable-host attempt failed with exit 255 and no automatic retry. This proves the existing original-chat transport plus inspect-before-retry procedure for that fixture, not automatic recovery of every recipe. No unrelated watchdog or automation was enabled.

Both Macs remained busy; macOS memory-pressure warnings and production contention met the approved benchmark stopping conditions. **Zero paired video-tuning benchmark runs were started.** OpenCV/native-thread, per-recipe encode and HyperFrames tuning defaults were retained. No percentage improvement in request-to-checked-preview, checked delivery, approvals or real M6 responsiveness is claimed. The existing historical waits remain the baseline: e.g. 9m09 for one M6 preview step, 19m48 for one M2 graphic and 33m37 for a measurement, not comparable whole-film completion samples.

The first three comparable real edits/revisions, Dan's decisions and the next normal 2:15 AM archive logs remain observation evidence to collect. A scheduled definition is not proof of a future overnight run. The real Metabolism Not The Reason film remains with its original editor; fixture delivery is not Dan's review, approval or that film's final delivery.

## Launcher readiness and rollback

Both hosts find the real embedded Codex binary and supported GPT-6.1 Sol/high; sign-in succeeds and the fresh client probes ran. Both find Claude; desktop Opus probes ran, but the standalone background Claude CLI reports signed out. Background Claude readiness therefore remains blocked, correctly, before any separately approved unattended pilot. No credentials were logged or copied and no upgrade/API fallback spending occurred. Future allowance cannot be guaranteed by a login check.

Known-good source/private-worker copies and deployment hashes are saved privately under each Mac's `Projects/_edit_work/two-mac-infra-20261114/`. `priority.py deactivate` is the scoped feature/reservation off switch; independent fairness/borrowing overrides remain. Its fixture rollback/release and activation refusal tests passed. Any source rollback waits for a compatible boundary and restores only these scoped files. Archive uncertainty retains sources; the former unsafe deletion path is not a rollback target.

The shared main checkout's required safe push was attempted and stopped on live edits owned by other sessions. Those files were not reset, stashed, adopted or overwritten. Task files are being published from a separate clean worktree, as allowed by the repository's worktree rule. Final commit, per-host hashes, M2 activation and service observations are appended below.

Private evidence root on M6: `/Users/danrrose/Projects/_edit_work/two-mac-infra-20261114/`; M2: `/Users/danielrose/Projects/_edit_work/two-mac-infra-20261114/`. Raw process snapshots stay private. Shared skill: `.claude/skills/priority-edit/SKILL.md`.

## Publication and final source verification

Implementation commit `0ea9c7440a70dc98e91594365f4314e677b2c402` was pushed to GitHub main from the clean publishing worktree. The only cherry-pick conflict was the replaced archive function; the exact tested archive worker was retained. All 30 task source/test/skill files match byte for byte on both installed checkouts and the published commit. Both private installed archive workers also match. The private comparison manifest SHA-256 is `b691c246f707175027dcee7858fac3895569347f0fef7f4bacc981192b6e35af`.

The final installed client harness ran again on both Macs after the old-waiter guard was added: all six acceptance results passed on each. M2's final tests passed 67 route/priority/resume assertions and 16 archive tests. Both Codex skill links resolve to that Mac's shared project skill.

Both PAUSE files still match the initial SHA-256 `518e294e67524002e5bac0865e5312db80073cf4337558c6211543c9cf0e83d1`. M6's edit-queue launch agent remains disabled. M2's remains loaded, not running, and paused; its unrelated review worker was preserved. Test review listener 9970 was removed on both Macs; cached evidence is retained. Only this task's exact fixture mirror note was retired. No shared hub was stopped.

The homepage returned HTTP 200 after publication. The three automatic Railway deployments for the implementation commit were building at the initial follow-up. Their final status and M2 activation are recorded in the final operational note below when observed.

Use in either supported client, substituting the actual video title or ID:

- Codex: `$priority-edit Make [video] a priority.` or `$priority-edit Give [video] the M6 until its checked preview is ready.`
- Claude: `/priority-edit Make [video] a priority.` or `/priority-edit Give [video] the M6 until its checked preview is ready.`

These requests keep the original editor and owner Mac. Dedicated-M6 time for an existing M2 film first needs an explicit move instruction after its current stage is inspected.

## Review backlog reconciliation

The actual M2 dispatcher's five delivered rows were checked against the current owner records and dated decision evidence. This is separate from the five historical scoreboard runs, which remain preserved.

| Job / current round | Evidence | Action |
|---|---|---|
| DS-38 R3 | Owner note still awaits Dan's scripted/off-the-cuff choice and whole-film approval | Keep pending. |
| DS-39 R3 | Main owner record says R3 is in progress, replacing the older R2 delivery; actual M2 waiter remains alive | Record the discrepancy; do not alter its live edit or older evidence. |
| DS-41 R2 | Owner board and current render show the requested R2 cuts/speed revision in progress | Preserve the owner's current work; no film approval inferred. |
| SL-21 R2 | Dated handoff quotes Dan's Short 3 approval and subsequent Shorts 1/2 approval, names exact final hashes; independent cover-setup receipt confirms all three films final | Correct only the stale M2/public job record from delivered/rev5 to the owner's existing finalized/rev7 fields. Full before/after private audit saved. Covers still need choices; no upload/schedule claim. |
| WV-03 R3 | Original owner is building the new Great Again T round | Preserve owner and pending approvals; no complete-film approval inferred. |

After the one correction, four delivered rows still meet the dispatcher's existing stop threshold of four. PAUSE and Claude background sign-in also independently block unattended launching. No threshold, claim, schedule or editorial choice was changed. The original historical DS-01, AV-01 and RO-17 scoreboard runs were not relabelled as accepted deliveries.

## Final safety checks during the M2 hold

While waiting for the old M2 waiter, another live session ran `editcap.py wait --help`. The old parser treated this as a job. Help is now recognized at subcommand level and unknown flags are rejected before ownership/registry mutation. Both Macs passed 29 editcap assertions. The help-only process had already exited naturally; only its exact stale invalid record was removed after confirming no process or render remained. No process was killed, and its parent editor and real jobs were preserved. Audit: private `invalid-help-cleanup.json` on M2.

The scoped rollback check now includes a second ordinary urgency lease alongside the dedicated reservation. Deactivation clears all dynamic controls. Existing explicitly prioritized tickets retain their recorded order and drain normally. All 67 route/priority/resume tests passed again on both Macs. No production deactivation was run for this final check.

Additional isolated recovery fixtures passed on both physical Macs: a lost wake acknowledgment did not duplicate work, the original owner reacquired, a simulated clearing of temporary registries preserved the durable checkpoint and owner, and an unreachable owner stayed unresolved. Neither Mac was rebooted. This is simulated recovery evidence, not an enabled background watchdog.

The final comparison after these two corrections found zero differences across all 30 task source/test/skill files on either Mac. Manifest `final-source-hashes-complete.json` SHA-256: d0ae69a429230f7e01e360959d1a8a5ca7230824106487caec7e1fc85ee132eb. The earlier archive-worker comparison remains valid because its bytes did not change. Code corrections are published through `ab7250f`; earlier repair deployments completed successfully, as did all three services for the help-fix rollout. Automatic deployment of the final rollback-only correction is being observed. M2's production feature activation remains held while DS-39's original old waiter is alive.
