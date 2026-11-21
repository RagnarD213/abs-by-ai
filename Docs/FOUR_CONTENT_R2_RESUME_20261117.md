# Four content R2s: November 17 resume check

Checked shortly after 7 a.m. America/Chicago on November 17, 2026. This updates the [November 16 continuation receipt](FOUR_CONTENT_R2_CONTINUATION_20261116.md).

**All four R2s remain queued on M2 with Claude. None started overnight.** Each has zero attempts, no active batch claim and no R2 media. No revised R2 review page exists. The R1 pages are not revised output.

| Video | Batch | Verified state |
|---|---|---|
| Man Boobs Shorts | `chat-SL-36-R2` | Queued, Claude, M2, zero attempts |
| Protein Snack Can | `chat-DS-106-R2` | Queued, Claude, M2, zero attempts |
| Why I Sleep At 63 Degrees | `chat-DS-50-R2` | Queued, Claude, M2, zero attempts |
| Lose Fat Without Losing Muscle | `chat-DS-51-R2` | Queued, Claude, M2, zero attempts |

## Actual blockers

The named-batch scheduler is enabled. Both Macs continue recording ticks; the M2 morning report has no `start_block`, transport error or outcome-sync error. The general backlog PAUSE remains untouched and is not the reason these explicitly enabled batches are waiting.

M2 has no production capacity. Its editcap check counts four groups against its cap of three, including unmanaged render-queue activity. The render queue is using all eight permitted editing cores, with both Extreme heavy slots occupied by Great Again T VSL work. Other work and its claims were not interrupted or modified. These four videos have no priority authorization to take another owner's slot.

Storage independently prevents admission. A read-only call to the current shared `storage.check(..., commit=False)` reported **37.4 GB free on Extreme, 25.0 GB already committed elsewhere, and a 30 GB reserve**. These are the batch allocator's actual requirements, not the legacy general dispatcher's separate 150 GB stop.

| Video | Recorded additional need | Free space required with current commitments/reserve | Shortfall at the check |
|---|---:|---:|---:|
| Man Boobs Shorts | 35 GB | 90 GB | About 53 GB |
| Protein Snack Can | 15 GB | 70 GB | About 33 GB |
| Why I Sleep At 63 Degrees | 20 GB | 75 GB | About 38 GB |
| Lose Fat Without Losing Muscle | 20 GB | 75 GB | About 38 GB |

Free space and commitments change as other jobs run. No reservation was cancelled, no need estimate or reserve was reduced, and no job was moved to another Mac to bypass the cap. The old Protein Snack cache occupies about 123 GB, including about 120 GB of keyed-frame caches. It was inspected only and retained for safe reuse; no reviewed source, cache or original was deleted to make space.

## Protected work and continuation

All four stable R2 journals remain queued and retain their original submission IDs. Each saved decision file still matches the SHA bound into its immutable approval manifest. Owning-Mac checks continue to identify M2. There are no duplicate producers or extra round journals.

The existing batch service will retry admission after a production slot becomes available **and** storage checks pass. Finishing active work and releasing its slots/commitments, together with verified archival of completed storage where needed, are the dependencies. Queueing does not prove a start time. No new editor, monitoring automation, forced scheduler tick, public upload, schedule, generation or paid provider request was started in this resume check.

Full execution remains incomplete: no R2 render, final-file quality result, independent final review or owner playback handoff has occurred. Dan does not need to repeat his choices or start editor cards.
