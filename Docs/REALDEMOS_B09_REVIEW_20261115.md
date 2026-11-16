# Real Exercise Demos Batch 9 R1: owner review

2026-11-15. Awaiting Dan's review. No Batch 9 demo has been installed, approved, deployed, published or registered as used-final.

Review: http://127.0.0.1:9870/ (managed shared review service, mirrored on Dan's M6 and the M2).

Six 1080p real-footage candidates, each one continuous original take at natural speed, complete reps, Batch 3 recipe. The app encodes are 960x540; the owner page serves the full 1920x1080 masters. Each targets approximately15 seconds; all exceed10 seconds. Current live AI files were fetched and hashed for four side-by-side comparisons. Squat and battle ropes have no existing demo. Held side lateral's current AI is also displayed.

| Exercise | Picture duration | Independent clearance | Delivery gate |
|---|---|---|---|
| bw-squat | 16.049 s | REVIEW-R2-squat.md | PASS |
| battle-ropes | 15.449 s | REVIEW-R1-lower.md | PASS |
| pushup | 15.349 s | REVIEW-R2-press-push.md | PASS |
| knee-pushup | 15.182 s | REVIEW-R2-knee.md | PASS |
| db-shoulder-press | 13.981 s | REVIEW-R4-press.md | PASS |
| db-curl | 16.116 s | REVIEW-R1-dumbbells.md | PASS |

Six exact app delivery stamps pass all39 measured checks, with26 declared format exclusions and no failed or unmeasured items. Exact master/app audio stamps pass. Independent reviewers inspected delivered pictures, relevant native cue/loop/edge frames, source/grade reference, narration alignment, posters and app comparison. Each report states its actual coverage and limits. Rejected candidates are archived in the work directory. No shared gate code or thresholds were changed.

## What Dan should check

Review all six new demos for form, directions, voice and pacing. In particular, judge squat stance from the high source angle (source light variation and slight original camera reset), and shoulder press's slightly soft overhead elbows and small bottom/rest pose reset at the loop. Other real take joins may show natural pose/background differences. None is claimed pixel-seamless.

Side lateral is HOLD: B0450 does not demonstrate Dan's pour geometry (elbows lead, hands below elbows/pinky up). Current AI stays installed. Required real reshoot details are in PICKUPS.md; no new AI was generated.

## Verified delivery and honest limits

- Full HTTP download SHA-256 matched every served video: six real masters and five current AI files. All11 support206 byte-range requests. Final page200; no technical-preview banner.
- Phone390px and desktop1150px have no horizontal overflow; new footage appears first and comparisons stack on phone. Intermediate800px layout was also checked during preparation.
- All11 players passed silent last-rep seek and restart checks. Browser actual mute/paused state was verified before each group. Final owner handoff verified all11 paused at0, loaded, unmuted, with no playback; next deliberate Play is sound-ready. No volume settings were changed.
- Audio checks were silent offline decoding, transcription, loudness/true peak/clipping/silence and encode differences. No audible listening/timbre/naturalness approval is claimed. Dan's review remains the sound/form approval.
- Shared camera-audio selftest was attempted: exit1/four failures on M2. Missing legacy Muhammad/approvedAd1 references were reported; summed-mic/stack-pan expected-reason checks also failed and were not diagnosed. Separate synthetic profile tests passed8/8, as did all exact candidate synthetic in-app audio and delivery gates. No camera-audio regression selftest pass is claimed.

## Files and evidence

Work: `/Volumes/Extreme/_edit_work/REALDEMOS-B09` on M2. Each `out/<id>/` contains master, app encode, poster, edit/plan, voice placement, audio stamps, watch findings and delivery stamp. `review_clearance.json` binds independent reports to master/app/poster SHA-256. `review/manifest.json` binds the displayed real masters. `current-ai/manifest.json` records live AI URLs/hashes. `sources.json` maps source library clips and originals. `CUE-TO-PHASE-CURRENT.md` records current narration spans; independent reports record observed phases. `COSTS.md`/voice receipts record narration usage. No footage or images were AI generated.

`final-http-qa.json` and `batch9-browser-qa.json` record functional delivery evidence. Screenshot proof: `batch9-phone.jpg` and `batch9-comparison.jpg` copied beside this receipt in the work directory.

## Next action after Dan's decision

Install only the candidates Dan approves, retain the held side lateral, register the approved exact-file hashes/provenance, run app checks and deploy under existing whole-batch authorization. Do not request deployment permission again. If Dan asks revisions, keep this approval-pending manifest and exact reviewed candidates intact and start the appropriate next round. Do not mark the whole batch installed while side lateral is held.

## Exact candidates

```json
{
  "bw-squat": {
    "verdict": "SHIPS",
    "report": "REVIEW-R2-squat.md",
    "master_sha256": "7ce5b37ad5c1dd161556373b94113eb934289d9245bdad27192b40affbfa870c",
    "app_sha256": "55e30ca84022fc8439613a350490b52a5f5abebb4550ef2c8b350ef7658d9d29",
    "poster_sha256": "889fde3a7ebaeb1239eb409566b01821f0d2b4ec75ffc493e46491b014e6a9f6"
  },
  "battle-ropes": {
    "verdict": "SHIPS",
    "report": "REVIEW-R1-lower.md",
    "master_sha256": "294d3a79a9ed84a0251744998141b754a16db295f2fe535350a3409d46859dc9",
    "app_sha256": "57a60f998cb1caeca0425f71f1f3e043831703289005ad20cd26db3fcc5998f7",
    "poster_sha256": "c2dfcd5cfb25d97df7f9a4ec0888094feb0d2433f88b413360a7868f4b2c7ff8"
  },
  "db-curl": {
    "verdict": "SHIPS",
    "report": "REVIEW-R1-dumbbells.md",
    "master_sha256": "64bcfae931b8ceaebaafd776cc751d2c10f1945bf2dd1465b0baa66c33ebbfce",
    "app_sha256": "d5450a33400831dabf16e3689502b1bfd975f29a9846ba901cc233ed1aa809c8",
    "poster_sha256": "a38b68c690eb309a1d4e1a810c490d773671de3a2fe036b0ea4b927ef6dbc5b4"
  },
  "knee-pushup": {
    "verdict": "SHIPS",
    "report": "REVIEW-R2-knee.md",
    "master_sha256": "3c4570d26fe4a7951c6fb7b0ab326e98e08ee70c339f41b29cd5e5fddf9e1e15",
    "app_sha256": "54fcedd6c86bf6289ae541902ca1aad11fefd5aefa4905b21e865beac162183d",
    "poster_sha256": "ef60225b1156baaa14886915551ee263ce4aca6adab369e6eda3058c084bed13"
  },
  "pushup": {
    "verdict": "SHIPS",
    "report": "REVIEW-R2-press-push.md",
    "master_sha256": "c4e5d320bf67764c7ab028cec5040535be858f7a4fa264e76040d67e5325e608",
    "app_sha256": "0709bd0e81850442beb090b14724c57fd182f430be3ced5baa9aec94aa71b876",
    "poster_sha256": "2bb8e2fbddbb0a03bac67c9a6a21ed9346357006479642dc0fbe7867187e208a"
  },
  "db-shoulder-press": {
    "verdict": "SHIPS",
    "report": "REVIEW-R4-press.md",
    "master_sha256": "4356ceb4f3a356c0eb7b3832555ca45b31a8995a01a9a4aa860ada551e0bcd03",
    "app_sha256": "da33b7e1c49a06daae8db8afe9a197a23567df0a76d9bc224a446fc82139b47c",
    "poster_sha256": "e920dbdfe9480355f71fb34445aadffcb2f10824773523afdf8876bc3ca1f4a3"
  }
}
```

## Coordination bookkeeping

Edit slot released with review status. Only this job's status entry was edited. Board check remains over the shared word budget: M6 2511/2500, M2 2516/2500; excluding this nine-word entry, the existing board is already over budget. Other sessions' entries were preserved. This does not change the six media gate passes.
