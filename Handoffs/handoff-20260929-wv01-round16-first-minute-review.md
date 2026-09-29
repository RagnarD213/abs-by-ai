# WV-01 round16: combined opening and CTA tail review

Created 2026-09-29. Recommended next model: **GPT-6 Sol, High effort**.

## Review now

Review page: http://127.0.0.1:8766/round16/index.html

Dan has two pending decisions on that page: the integrated opening through 1:10 and the repaired closing CTA tail. Export the page JSON or reply with both verdicts. No complete film was rendered. Complete film B remains deferred, `scripts/edit-queue/PAUSE` remains present, and publishing is off.

Production root: `/Volumes/Extreme/_edit_work/wv01-edit/round16/`. The prior plan is `round16-plan/decisions.json` under the WV-01 root. All 49 protected source hashes matched before this round's work.

| Item | Exact review file | SHA-256 | Status |
|---|---|---|---|
| Combined opening | `previews/WV-01 round 16 first minute REVIEW 540p.mp4` | `28335a7926aac2c67f72fcb153281ca33543c6b4d1b69d4e6e45123cb51a9386` | Dan decision pending |
| 1080p opening draft | `previews/DRAFT - WV-01 round 16 - first minute through R02.mp4` | `8e27611390d57c54a4e643dc03c3fd332f6c6bda30c3d7fd9ca05eb8c3d464f9` | Same edit, not a separate decision |
| Closing CTA repair | `previews/WV-01 round 16 closing CTA repair.mp4` | `7db4d1081549aba8ac9f6c80e68f19114757f51e3e13fe2904ce966ca4f26f21` | Dan decision pending |

The 2098-frame opening includes the exact approved R01 source action at frames 240-359 (0:08-0:12), then R02 photo 1 at 1768-1872 and photo 2 at 1873-1977. Presenter footage returns at 1978, and the preview runs through frame 2097 (about 1:10). The approved opening audio was reused without narration edits. The three replacement midpoint pictures match their round13 reviewed counterparts to mean absolute pixel differences below 1/255 after review scaling and encoding. Native boundary stills and source mapping: `round16/review/first-join-sheet.jpg` and `first-minute-build.json`.

The CTA cover starts at baseline frame 22329, 14 frames before the old start, hiding the inherited presenter splice. It uses source frames 125-407 from the exact approved `round6/previews/closing-context.mp4`. Source frames 408-421 are a 14-frame continuation of that CTA's animation recipe at its original speed. They received the same CRF19 source encoding before contextual assembly. The existing closing soundtrack is unchanged and contains the complete last words, ending about baseline 753.52 seconds, followed by the original natural tail. The corrected native seam difference is 0.274/255 versus 0.1-0.17/255 for neighboring frames; all final 14 frames differ from one another. The old exposed presenter jump and a frozen end are absent. Records: `round16/review/CTA-tail-repair.json`, `round16/review/round16-local-QA.json`, and `round16/review/cta-join-sheet.jpg`.

Both exact preview files decoded without error. The local review server returned exact matching bytes and a valid HTTP 206 range response; `round16/review/served-verification.json` records this. The review page uses one lazy player. No new paid generation calls were made. Known cumulative motion generation estimate remains **$29.008017301463925** against Dan's **$50** authorization; 56 historical still-call charges and actual provider invoices remain unavailable.

## Locked decisions and limits

Preserve R03-A's approved 132-frame natural trim, R12-B's approved natural 9-second trim, and R05/R07/R09's exact approved motion. R12-A is removed. R12-B retains the disclosed sleeve continuity QC uncertainty and Gemini FAIL finding, alongside Dan's creative acceptance of that exact option. Do not convert that acceptance into a technical QC PASS or generate a replacement without a request.

Preserve the approved opening look, first-minute color and audio, V sit twist phone, exact3A, mirror, photos, 16 cut repairs, and source-specific edit maps. R04 adds 7 narration frames, R10 removes 39, R11 removes baseline frames 22196-22220 once, for a net 56-frame reduction after round12. Never repeat round12's earlier removals. The inherited round12 full-film website gate was FAIL. This short approval packet is not a complete candidate or a delivery gate pass.

The finished round12 closing words include "So tap the button below." Treat upload routing as an ad if setup is later requested. There is no upload or setup action in this round.

## Next action after Dan's decisions

Record both decisions with exact hashes and Dan's words in `round17-plan/decisions.json`. If either needs changes, make only that scoped correction in a new isolated round. If both are approved and Dan authorizes complete assembly, assemble complete A from the locked pieces and repaired CTA tail, then run fresh exact-file gates, full chronological picture/audio QA, native join and junk-footage checks, subtitle timing, and one independent complete-candidate review. Complete B remains deferred and publishing remains off unless Dan changes those instructions.

## Ready-to-paste starter prompt

Continue WV-01 from `Handoffs/handoff-20260929-wv01-round16-first-minute-review.md` using `$abs-edit-organic`. Apply my two round16 decisions to the exact first-minute and closing CTA repair files. Preserve all earlier approved pieces, selected family R12-B, the known sleeve QC finding, and R12-A removal. If both decisions are approved, assemble complete A only after I explicitly authorize that render. Keep complete B deferred, the dispatcher paused, and publishing off.
