# Two-Mac edit dashboard: Astra review, then build

**Executed November 14, 2026.** [Open the installed dashboard on M6](http://127.0.0.1:8976/). [Verification and measurements](../Docs/two-mac-dashboard/receipt.md). The original authorized brief below is retained for reference.

## Goal and authorization

Build Dan a simple local dashboard showing what is editing on both Macs and whether more work should start or wait. The dashboard itself must consume very little CPU and RAM. Prioritize useful finished edits and a responsive daily Mac over the number of open editing sessions.

Dan's exact instruction: “Let's have Astra review the plan first, incorporate any worthwhile changes, and then go ahead and build it. Make me a handoff for that.”

This file is the handoff, not a completed review or implementation. The next owner must obtain Astra's review, incorporate justified changes, and continue through implementation, installation and verification without returning to Dan for routine approval. No dashboard code has been written or service installed by this handoff task.

Recommended execution owner: **newest available stable Sol, high effort**, verified in this client's local model catalog on November 14 as `gpt-6.1-sol`. **Astra reviewer: `gpt-6-astra`, high effort**, also listed. Recheck supported IDs before use; do not silently substitute the reviewer. Dan explicitly authorizes one bounded Astra subagent review. Use supported collaboration tools with an explicit Astra model and high effort, `fork_turns: "none"`, and a full self-contained brief. Keep Sol as the sole implementation owner. No new user-facing chat or competing implementation is requested. If explicit Astra selection is unavailable, prepare the review brief and report that exact blocker; do not pretend a Sol self-review was Astra's review.

Routine reversible file edits, local service installation, SSH inspection/helper deployment, tests, scoped commits and pushes are authorized. No paid API calls, production video launches, concurrency increases or unattended-dispatcher restart are authorized by this dashboard request.

## First action: establish current owners and evidence

Read current `AGENTS.md`, `AI_COORDINATION.md`, applicable skills and:

- `Docs/TWO_MAC_VIDEO_EDITING_OPTIMIZATION_PLAN_20261114.md`.
- `Handoffs/handoff-20261114-two-mac-video-editing-optimization-execution.md`.
- `.claude/skills/_shared/editroute/{README.md,hosts.json,hostcfg.py,editroute.py}`.
- `.claude/skills/_shared/editcap/{README.md,editcap.py}`.
- `.claude/skills/_shared/renderq/{README.md,renderq.py}`.
- `.claude/skills/_shared/review_hub.py`, `.claude/skills/_shared/review_server.py` and their relevant tests.
- `.claude/skills/_shared/stallwatch/README.md` and `Docs/DESIGN_QUALITY_LESSONS.md`.

**Another chat owns live infrastructure repairs.** At handoff creation the board says “Two-Mac infrastructure: ACTIVE 2026-11-14, Codex optimization execution,” working in an isolated worktree, with router rollout awaiting the DS-107 owner boundary. Do not edit its owned scheduler/router/archive files or deploy over them. Implement dashboard files separately and consume the current supported state. If a shared observation interface is needed, prepare the adapter separately and resolve the owner boundary before touching those files. Do independent frontend/fixture work meanwhile. This handoff does not authorize messaging unrelated chats; inspect the board and local artifacts first, and ask Dan only if an unavoidable ownership decision remains.

The older optimization plan excludes a dashboard from *its* scope. Dan's later explicit request authorizes this separate dashboard; it does not expand that other owner's task.

## Machines and known state

| | M6, Dan's daily Mac | M2, editing Mac |
|---|---|---|
| SSH alias | `m6`, address `10.66.0.1` | `m2`, address `10.66.0.2` |
| User/project | `/Users/danrrose/Projects/Claude/Projects/Abs By AI` | `/Users/danielrose/Projects/Claude/Projects/Abs By AI` |
| Whole-edit limit | 2 | 3 |
| Render core budget | 6 while present, 10 after 30 minutes away | 8 |
| Storage | Internal SSD for editing; external drives visible as network shares | Extreme and Expansion attached locally |

On M6 `/Users/danielrose` aliases `/Users/danrrose`. The Documents project path in older chats resolves to the Projects checkout. Resolve actual paths; do not create another accidental checkout.

Read authoritative config/live state instead of hardcoding the table. The optimization work changes the night rule so recent input or unknown presence keeps M6 at six cores, even at night. Detect deployed behavior; do not label a planned fix installed merely because it is approved.

At approximately 2:23 p.m. Central November 14, the observed production jobs were M6 WV-03 and DS-98; M2 DS-107, DS-41 and REALDEMOS-B03, with EXDEMO-3MORE waiting. M6 memory pressure was warning. Both Macs were reachable. These are historical examples, not the live starting state for this task. DS-98 is a blind comparison: owner-facing dashboard details must not expose arm/model mappings or sealed identities.

**Correction to the original discussion:** status reported legacy holders, but the separate infrastructure investigation found that normal holder publication can omit the version and therefore falsely label current code legacy. Missing version alone does not establish stale loaded code. Never recommend restarting a holder based on that label. The original whole-edit limits are configured limits, not a measured optimum.

## The proposed plan Astra must review

### 1. Small local page

One prominent recommendation, with a short reason: “Start one more on M2,” “Queue additional edits,” or “Status needs checking.” Then show each Mac's production edits, render holders, waiting work, memory health and last successful observation. Separate waiting for capacity, waiting for Dan and observed rendering/checking. If exact stage is unsupported, say “In production, current step unknown.” Use recognizable video titles, with technical details collapsed.

Design at 390px phone width first, then desktop. Text and compact capacity indicators are enough. No animations, video previews, external fonts, CDN assets, chart framework or continuously running AI. Include Refresh and a clear timestamp. Initial page should be readable immediately while live collection occurs.

### 2. Dedicated, genuinely observational snapshots

Do not repeatedly shell out to full `editroute.py status --json`: `local_status()` also probes drives/work folders, checks Git and records diagnostic/cache files. Some low-level queue readers are not observational: `renderq.slot_states()` may finish records/write history, `_tickets()` deletes dead tickets, and `editcap.view()` calls those readers and settles an in-memory registry. Read source before reuse.

Build a bounded observation path reading small state files, current configuration and necessary kernel/process identity data without changing scheduler state. Never acquire/promote/release edit slots, clean tickets, finalize holders, append scheduler events, create work folders, run route picks or claim wakes from a page request. Dashboard-owned caches are allowed. Use fixture tests to verify no scheduler mutation. Account for stale records, PID reuse and cleared `/tmp`; missing/unreadable state is unknown, not zero usage. Preserve recorded versus inferred distinctions.

Relevant state: per-host `/tmp/absbyai-editcap/registry.json`, `/tmp/absbyai-renderq/` slot/ticket files; primary route reservations/waiting state usually under `~/.absbyai-editroute/`, with documented `/tmp/absbyai-editroute` fallback. Use actual configured locations. Read bounded metadata, not entire ever-growing event histories. Existing small job-title/release records can be cached by modification time.

No footage scans, media decoding, recursive workdir inventories, Git/network fetches, directory-size calculations or disk benchmarks. Do not probe sleeping external drives each refresh. If storage is shown, use timestamped existing observations, clearly marked cached; unknown space cannot establish suitability. Report cheap unmanaged-work observations if available; do not imply allowances enforce actual CPU usage. Absolute swap used and macOS load average alone are not reliable overload decisions.

### 3. Sparse, shared collection

Refresh once per 60 seconds while visible; stop automatic collection when hidden/closed, refresh on return if stale. Returning while the cache is fresh should reuse it. Manual Refresh requests a bounded update, not a concurrent scan. Multiple tabs share a server-side cache and one in-flight collection; use a defined minimum interval to prevent repeated-click/process storms.

Prefer a small Python-standard-library backend and plain HTML/CSS/JS. Reuse the existing local service if it supports the endpoint safely without restarting live review pages or changing another owner's files. Otherwise use one small on-demand service with bounded idle lifetime and a stable local address. Choose the simpler verified option after Astra's review and inspection. No persistent M2 polling daemon is needed: a short-lived read-only helper over existing SSH should suffice. Put runtime/cache on internal local storage, outside media folders and network shares. Bind local-only; public hosting and cloud services are unnecessary.

Use existing SSH aliases, batch/noninteractive mode, bounded connect/whole-call timeouts, no repeated retries per refresh, and cleanup of timed-out children. Collect hosts independently so an unreachable M2 cannot prevent fresh M6 display. Cache last success separately from latest error/attempt. A failed refresh must not reset the freshness timestamp. No overlapping children or accumulating threads when a host hangs. SSH keep-alive machinery is optional only if measurements justify it.

### 4. Explainable advice, separate from authority

Use the deployed queue/routing policy as authority. Reuse pure calculations where safe; do not create a second scheduler. Consider active/promoted edits, reservations, local and combined waiters, existing owners, host health, core budgets, memory/settling and relevant priority/reservation state once deployed. Separate “can admit an edit” from “can render immediately”; an unused whole-edit slot is not automatically ready CPU capacity. Existing waiters get their policy-defined turn before a recommendation to add new work. Recommendations should identify suitable work category/host where evidence supports it, never promise any edit can start or infer a named existing job may move.

An unavailable host means unknown capacity, not idle. A healthy host may still have a clearly qualified recommendation if it is independently safe and ownership/reservations can be verified; otherwise say check status/queue only. Show stale/partial/unsupported-version caveats explicitly. Initially treat observations older than two visible refresh intervals as stale; Astra may improve this threshold with reasons. Do not fabricate time-to-completion or claim the system chooses an optimal five.

Keep two M6 and three M2 production edits. Explain warnings in plain language. Suspected stalled jobs need evidence and a “possible stall” label, not automatic intervention. No start, stop, priority or queue-control buttons in v1. Keep the overnight dispatcher paused.

### 5. Resource targets and verification

Initial targets, to measure rather than assert: additional backend memory under **50 MB across both Macs**, and average additional CPU under **0.5% of one core on each Mac** during normal 60-second refresh. Include transient collectors and SSH helpers in accounting; separate steady, peak and idle measurements. Browser-tab incremental RAM/CPU is reported separately, not hidden behind the backend target. The frontend page limit is not a promise about the browser's total process size. Astra should assess whether targets are realistic without weakening the low-overhead objective.

Measure baseline, visible, hidden, closed, multiple-tab and unreachable-M2 cases, with observation windows long enough to include several refreshes. Report CPU seconds / elapsed seconds and MB definitions clearly; count only incremental dashboard work, identify shared-process baseline and measurement limitations. Use bounded lightweight sampling, not an always-on profiler. No production render stress test, artificial edit launch or interference with real work. If targets are missed, optimize, measure again and report any remaining gap honestly.

Functional tests: both hosts healthy/full, one free with/without queued work, active/promoted/reserved overlap without double counting, warning memory, changed presence/core budget, unknown pressure/config/state, reboot-cleared registries, stale/PID-reused holder, unsupported schema, cached sleeping-drive data, M2 failure/recovery, local partial failure, concurrent tabs, manual refresh storms, hidden/visible lifecycle, timeout cleanup and zero scheduler mutation. Fixtures/scratch paths must never claim real waiters. A normal page request must not touch media or wake a sleeping drive. Test no polling while hidden and cache sharing server-side, not just a disabled browser timer. Preserve DS-98 blind identities.

## Astra review sequence, then implementation

1. Save the initial plan/review brief in a dashboard-specific folder. Ask Astra to inspect the relevant source and review this actual plan, without modifying implementation, launching edits or running expensive experiments. Focus on false “start more” advice, observation side effects, cheapest architecture, stale/partial-state handling, existing-owner conflicts and measurable resource targets. Ask for a short prioritized list of changes and reasons; one review round is sufficient unless a blocking contradiction remains.
2. Save Astra's actual returned review. Write a short adopted/rejected/deferred comparison with reasons and produce one revised execution plan. Do not claim agreement or incorporate unverified assertions merely because Astra proposed them. Routine architecture improvements within scope are authorized; continue without asking Dan to approve the same build again.
3. Implement in isolated dashboard-owned files, run meaningful fixture tests, and deploy the small helper to M2 only as needed. Preserve concurrent dirty files, live ports, review services and scheduler owners. Read the available site/browser skills if they apply; a local process/SSH requirement must not be replaced with public hosting. Use supported browser tools to inspect phone and desktop layouts and refresh behavior.
4. Verify live readings against both Macs using a bounded snapshot; reconcile ordinary refresh-time differences. Measure overhead, verify hidden/closed behavior and timeout recovery, and leave a working stable local link on M6. No media playback is necessary for this dashboard. If any media inspection is introduced, first read the full shared video rules and obey silent checks and sound-ready handoff.
5. Deliver the dashboard link first, concise usage instructions, Astra's worthwhile changes, actual resource measurements and remaining limitations. Save a receipt with installation/restart/removal instructions and tests. Commit/push only owned changes using current safe project workflow; never stage unrelated dirty files. Update this handoff's index status accurately and keep the coordination board short. Do not call installation a verified working dashboard until the real page and data path were checked.

## Done means

- Astra actually reviewed the plan and its worthwhile changes were incorporated with a record.
- One usable local dashboard displays both Macs, job titles, justified start/wait advice and per-host freshness.
- Tests establish that page requests cannot control the queues or interfere with existing owners, media or dispatcher state.
- Resource overhead and failure/hidden-tab behavior were measured, with results and limits reported.
- Dan has the working link and can use it without launching a terminal command.

## Starter prompt

Use newest available stable Sol, high effort (`gpt-6.1-sol` verified at handoff creation):

> Read `Handoffs/handoff-20261114-two-mac-edit-dashboard.md` in the Abs By AI project and execute it. Dan authorized a bounded GPT-6 Astra high-effort subagent review first, then incorporation of worthwhile changes and the complete dashboard build, installation and verification without another routine approval. Preserve the other chat's infrastructure ownership and live edits. Minimize CPU/RAM, keep the existing production limits and paused dispatcher, verify that observation cannot mutate scheduler state, measure actual overhead, and deliver a working local dashboard link. This is an execution handoff; the review and build have not started yet.
