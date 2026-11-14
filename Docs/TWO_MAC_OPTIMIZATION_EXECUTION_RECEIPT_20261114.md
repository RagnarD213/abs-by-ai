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
| Route/priority/resume unit fixtures | 67 passing after the whole-edit waiter guard | Final recheck recorded below |
| Render-queue process fixtures | 57/57; four real CPU/RSS stress assertions deliberately not run in the final safe mode | 57/57, same explicit stress omissions |
| Edit-slot fixtures | 27/27 | 27/27 |
| Archive fixtures | 16/16 | Final recheck recorded below |
| Contact-sheet child lifetime | PASS; slot still held after actual sleeping child exit | PASS |
| Launcher fixtures | 59 policy, 11 fake end-to-end, 5 repair, 2 review-page, 7 asset tests passed | Same suites passed before the final archive/waiter-only guard update |

The original three M6 editcap CLI failures were test isolation defects: fake jobs were accidentally looking up real ownership. The ownership guard remains; the fixtures now use explicit private host data. Three older launcher expectations still assumed September's executor routing. Tests now reflect the approved routing, and generic cross-executor tests set their intended routing explicitly. Fake launcher tests use a fixture router, not real production job IDs. Launcher suites run as separate processes because their old module globals collide under one discovery process.

The private client harness uses five isolated state directories and two occupied slots. Its “checked preview” is a fixture marker, not film QA. Fresh clients explicitly reported this distinction. No real waiter was awakened as a test and no real queue claim or film status was created by a fixture.

## Measured effects and limits

A six-core competition fixture used real sleeping commands with fixed short durations. On M6, the selected light check started at **3.039 s with borrowing off**, **0.292 s with borrowing on**; the heavy follower started at **2.061 s versus 2.109 s**. The next quick task waited until that heavy opening, proving the shared one-loan bound. This is simulated scheduling evidence, **not a film speedup**. The same fixture passed on physical M2; its exact timings are in the private receipt.

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
