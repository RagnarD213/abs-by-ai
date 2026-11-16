# Four-content-video test night, November 15–16, 2026

**Result: partial technical success. All four first-review targets are ready and waiting for Dan. This is not a pass for fully unattended operation or four final films.**

The queue was enabled November 15 at 10:01:09 p.m. Central after the corrected one-time 10 p.m. scheduler wake. The source/launcher preflight passed on both Macs. The prior unpublished `/away` change had been pushed and synchronized before launch. First editing began at 10:03:06 p.m.; all four first reviews were accounted for by 12:52:47 a.m. November 16. No video was approved, uploaded, published or scheduled.

## Reviews

| Video | Editor | First-review outcome recorded | Review on M6 |
|---|---|---|---|
| How To Get Rid Of Man Boobs (RO-31; 3 Shorts; parent Jan 24 9AM Central planned) | claude | Nov 15, 10:34:12 PM CST | [First review](http://127.0.0.1:9806/) |
| The Best Protein Snack Costs $2 And Comes In A Can | claude | Nov 15, 11:51:54 PM CST | [First review](http://127.0.0.1:9807/) |
| Why I Sleep At 63 Degrees | codex | Nov 16, 12:02:51 AM CST | [First review](http://127.0.0.1:9808/) |
| 3 Ways To Lose Fat Without Losing Muscle | claude | Nov 16, 12:52:46 AM CST | [First review](http://127.0.0.1:9809/) |

- **How To Get Rid Of Man Boobs:** three proposed Shorts with full transcripts and horizontal 1080p segment previews. Pick which to build. These are not completed vertical Shorts.
- **The Best Protein Snack Costs $2 And Comes In A Can:** 59.4-second vertical draft plus colour/voice choices and every asset in context. Choose the look and voice and review the capsule cutaway/opener.
- **Why I Sleep At 63 Degrees:** 31.9-second opening and separate graphic/clip excerpts, colour and voice choices. The complete film has not been assembled.
- **3 Ways To Lose Fat Without Losing Muscle:** 62.0-second vertical first-review draft, colour and voice choices and every asset in context.

All four correctly ended `needs-dan`, with no live batch claim and no pilot edit holding an editcap slot. Existing unrelated work was preserved. The three review exports over 45 seconds are in `Videos to Review/` and their SHA-256 values match the exact page exports. That existing folder resolves to the Expansion offload; no global folder move or volume change was made.

## What actually passed

1. The named content-only batch was enabled, acknowledged by both Macs, and all four immutable briefs reached their intended first-review outcomes. The two withdrawn ads stayed cancelled. General backlog discovery stayed paused.
2. One deliberate SIGKILL of the Man Boobs runner during its real editor session was performed at 10:11:57 p.m. The scheduler reconciled the exact old process identities, stopped the orphan editor, and resumed once in the same `/Volumes/Extreme/_edit_work/SL-36` folder at about 10:21:54 p.m. The old runner and old editor were confirmed gone; the new runner was live. It subsequently produced its review page. No second recovery or duplicate producer was recorded.
3. Protein Snack returned a real `needs-dan` page and released its slot. The next eligible job, 3 Ways To Lose Fat Without Losing Muscle, entered its editor on M2 after the existing storage backoff elapsed. This proves release and subsequent start, not immediate throughput.
4. All four managed review pages opened on M6. Fifty linked media URLs returned HTTP 206 byte ranges. Silent browser checks verified main playback and seeking on each page, selected auditions/context switches where available, and Finish checks for owner. Every media element was verified paused before sound was enabled. These are functional checks, not a perceptual listening pass or Dan's approval.

## Why fully unattended operation did not pass

Both internal disks were below the required 80 GB reserve at launch: roughly 39 GB available on M6 and 55 GB on M2. M2's launchd-origin workers also received `Operation not permitted` when creating external work folders, although the same operations through its already-authorized SSH context succeeded. The installed M2 LaunchAgent already uses the intended real Xcode Python; it is not the old `/usr/bin` shim.

The supervising chat therefore ran M2 ticks through SSH to launch/recover workers with working drive access. Existing backoff and capacity rules were preserved. All real editing ran on M2/Extreme; no M6 editor could start. This intervention is material: do not call tonight proof that the background services can run the entire workflow alone. No OS permissions, reserve thresholds, global network settings or other owners' work were changed.

Allocation attempt counts include storage waits: 15 for the muscle-preservation Short and 5 for the sleep Short do not mean 15 or 5 editing sessions. The pilot used five real editor sessions across four jobs, including the one Man Boobs recovery. Recorded active hours omit time lost with the killed runner, so they are not a complete efficiency measurement. No ten-video or final-film throughput forecast is supported.

## Incomplete tests and quality limits

- **Hung final reviewer and retry:** not run. The muscle-preservation Short correctly needs Dan's creative choices before a valid final candidate exists.
- **Clean Codex edit followed by Claude final cross-review:** the Codex first review exists, but final cross-review is not run because the sleep video's choices remain open.
- **One-hour M6-to-M2 interruption during a running M6 edit:** not run because no M6 edit could start with its available disk space. The Mac's network and SSH were not disabled.
- **Submitting-chat closure:** not demonstrated as a separate real-run proof; this supervising chat remained active. The workers consumed the durable copied briefs.
- No finished candidate went through the final delivery/watch/independent-review chain tonight. Draft audio checks retain disclosed failures: Protein Snack has tone, early-decay and processing-damage failures; the sleep excerpts have tone and some dryness/artifact failures; the muscle-preservation draft has tone and source/processing-artifact failures. These were not relabelled PASS. Owner choices and the normal final checks still apply.
- No new AI motion was generated. Protein Snack's existing Gemini voice bake-off reports approximately $0.10, an editor estimate rather than a reconciled provider invoice; the other new clip-generation spend was zero.

## Evidence and next action

Private runtime receipts on M6: `~/.absbyai-batch/pilot-prep/night1/`. Key files are `launch-receipt.json`, `four-first-reviews-snapshot.json`, `supervision-events.jsonl`, `sl36-kill-once.json`, `ds106-slot-release-proof.json`, the four `*-functional-review-check.json` files, `vlc-copy-check.json`, and `slots-after-all-four.json`. M2 preserves the authoritative ledger and killed-runner proof under `~/.absbyai-batch/night1-20261115/`.

Dan's next action is to review the four pages and send his picks. Before a larger unattended batch, the implementation owner must resolve or explicitly account for background drive access and M6 storage, then complete the unproven reviewer and connection-interruption cases on eligible candidates. Dan asked for the morning result at about 8:20 a.m. Central on November 16. All four states were rechecked as needs-dan and all four review pages returned HTTP 200. The one-time start automation was deleted; the remaining next actions are Dan’s creative choices and the infrastructure fixes/unproven tests above.
