# Overnight batch implementation, November 15, 2026

Status: installed on both Macs, disabled. The four-job first night is queued and has not started. Final Fable 5.2 review is still in progress. Dan's go is required to start Night 1; no general backlog resume is authorized.

## Repaired and verified today

- Restored M2 editroute storage/priority/client/mirror files and the rolled-back scheduler/launcher files from M6. Backed up the former M2 scheduler under `~/.absbyai-batch/repair-backups/`. No live video worker was restarted or interrupted.
- M2 installed dashboard collector returned `issues: []`. A dry-run route for the existing Hormozi Not Hungry Bored edit selected M2, honoring its work folder and active slot. A new long-form dry run used M6 because M2's three slots were occupied; no fictitious free slot was claimed.
- Pushed the scheduler source to main through a clean checkout at `/Users/danrrose/Projects/_overnight_scheduler`. The shared main checkout's live unrelated edits prevented its normal safe-push merge. No stale adoption, reset, stash, or unrelated commit was used to bypass those owners. Both Macs fetched the pushed commit and received only its scheduler files. Installed source matches pushed Git objects, rather than depending on a dirty local HEAD.
- Restored Claude sign-in on M2 using its normal browser authorization. No new purchase or subscription change.
- Real launchd canaries passed Claude editor, Claude reviewer, Codex editor and Codex reviewer on each Mac. Final current-launcher receipts: M6 `20261115-095910-644885`; M2 `20261115-095911-040d97`. Each recorded the exact generated reply, exit code and elapsed time. These prove session readiness, not editorial quality or throughput.
- Loaded `com.absbyai.edit-queue` on both Macs with a 120-second interval. General discovery remains paused. No batch worker has started.
- Latest saved source/preflight proof on M6: `~/.absbyai-batch/implementation-preflight.json`. Re-run preflight after any scheduler source change.

## Implemented behavior

One M2 ledger outside Git, immutable copied briefs with read-back hashes, one ledger lock, explicit job and round keys, independent local pulling, fixed placement, longest-size-first ordering and Dan's ordering within size. Each runner acquires/refreshes/releases editcap and asks renderq for its work folder. Named rounds bypass the old launch/review caps while PAUSE continues to block general discovery. A single stop disables future starts and leaves running workers to finish.

Ordinary exits record delivered, delivered-unreviewed, needs-dan or blocked. Exit zero without a fresh outcome is a failure. Unexplained runner loss gets one bounded recovery in the same folder after exact process/session reconciliation. No unreachable claim is reassigned. Allowance pauses preserve the folder/owner with shared backoff and at most three total attempts. A reviewer timeout or absent verdict gets one fresh retry, then unreviewed; a valid rejection retains the cut and findings with no fix loop. Current exact-file shared gate stamps are required for final candidates. Missing review mirroring is saved locally and retried before delivery is recorded.

Chat waits use `batch.py enqueue-chat` with their self-contained brief. A batch-owned round requires `batch.py takeover` before chat production; an active or unconfirmed claim cannot be taken over. The M6 morning report is saved every tick and distinguishes checked, unreviewed, owner choices, blockers, unreachable owners and queued/running work. Review links are verified on M6. Queue wait, active/review time, allowance pauses and sampled idle-slot minutes are retained. No throughput forecast is claimed.

No cross-Mac start-request protocol, execution transfer from a live chat, notifications, new dashboard rows or new Drive sync was added.

## Old Waiting for Dan records

Cleared the six confirmed finalized/uploaded entries on both Macs: Calories Don't Matter Shorts (SL-13), Keep Your Muscle Shorts (SL-12), Sleep Better With Glycine (RO-15), Blended Oats (DS-38), Why Fat Shaming Is Good (DS-36), Surgeon Fake Abs (DS-34). Finalization/upload transitions now call editcap forget; the desk and edit register also hide completed review entries, and show the age of remaining reviews.

Inspected the existing owner records without restarting their tasks. The old Codex Joint Vigor trial was handed to the Claude owner; that owner's record says Version B was approved and sent to Eric. Its two superseded trial review entries were cleared. Exercise demos Codex R3 still needs an acceptable curl/real-footage replacement; Joint Vigor style options still awaits the owner's message approval. Those entries remain. The Flow exercise pilot's latest summary concerns a separate music handoff and does not establish its earlier demo's finalization, so its unmatched review entry remains until the production owner resolves it.

## Verification

- 16 new batch tests: competing-process claims, placement/order, disabled receipt, source-preflight failure, global stop, no implicit restart of stopped batches, live takeover refusal, duplicate-round refusal, killed-runner recovery, reuse of its still-registered slot, three allowance attempts, disconnected owner, stale outcome tokens, mandatory owner question/link, offline outbox and distinct uncertainty/rejection verdicts.
- Existing queue tests run in separate processes because their import-time environment overrides interfere when combined in one unittest discovery run. 60 queue unit tests, 5 launcher tests and 11 end-to-end runner tests passed. Asset approval and review-page tests also passed.
- 72 routing tests passed. The old M2 Extreme-first test now expects Dan's current internal-first drive order.
- 29 editcap checks and 15 dashboard tests passed.
- Renderq's non-stress suite: 57/57 passed. CPU-census stress was omitted on the busy Macs; the earlier full stress invocation hit a test cleanup PermissionError. No production renderq behavior was relaxed.
- `https://absbyai.com` returned HTTP 200. Git-triggered Railway builds are queued; a latest-commit successful website deployment has not been verified. These scheduler services run on the Macs, not Railway.

## Night 1, still disabled

Batch: `night1-20261115`. Both Macs logged the batch before its receipt reported queued. All four listed sources were rechecked on M2 and none were missing; the required Ad 8 parent/adaptation is uploaded.

| Video | Editor | Target | Authorized proof after Dan's go |
|---|---|---|---|
| Man Boobs Shorts (SL-36) | Claude | Three standalone segment transcripts and a review page; stop for picks | Kill runner once during editing; one resume in same folder |
| Ad 8 square (AS-08) | Claude | Full and 59-second square review candidates | Hung reviewer, one retry, then delivered-unreviewed |
| How To Generate Abs With AI (RA-02) | Codex | Vertical/horizontal review candidates | Clean Codex edit, Claude cross-review, honor actual unmet approvals |
| Protein Snack Can (DS-106) | Claude | First-review page only | Needs-dan, working link, released slot, next eligible start |

Before starting, finish the independent Fable 5.2 review and resolve its blockers. Then, only after Dan says go:
`python3 scripts/edit-queue/batch.py start night1-20261115`.
The proof still needs its real killed-runner, hung-reviewer and one-hour M6 connection interruption while the submission chats are closed. Do not imply those have passed. Preserve unrelated live editors when arranging the interruption. Pass requires all four accounted for, no duplicate, no silent stop and no false done. Night 2 needs Dan's ten specific videos and measured results before any throughput promise.

M6 owner report: `/Users/danrrose/.absbyai-batch/morning-report.md`.
M2 authoritative batch: `/Users/danielrose/.absbyai-batch/night1-20261115/`.
Operating instructions: `scripts/edit-queue/README.md`.
