# Real Exercise Demos Batch9 R2: owner review

Completed 2026-11-16 00:02 CST. Seven revised1080p demos rendered, checked and independently cleared, awaiting Dan's review. No revised exact file is approved. None of the new exercise assets has been installed in the live app. Documentation and timing-policy changes were pushed separately; no public exercise-demo file was changed.

Review: http://127.0.0.1:9870/ . Managed shared local review service on M2 and Dan's M6; one1080p review master per demo. Separate app encodes are960x540, as required for installation, not smaller review copies. The page includes four current live AI comparisons; squat, ropes and correctly identified Hammer Curl have no installed MP4 at their exercise IDs. The live Hammer Curl URL returns the site's HTML fallback, so it is not shown as an AI video. Distinct supinated Dumbbell Curl remains untouched.

| Exercise | Actual picture length | Exact independent report | Delivery |
|---|---|---|---|
| bw-squat | 13.447s | REVIEW-four.md | PASS |
| battle-ropes | 13.881s | REVIEW-four.md | PASS |
| pushup | 12.946s | REVIEW-four.md | PASS |
| knee-pushup | 13.614s | REVIEW-four.md | PASS |
| db-shoulder-press | 13.981s | REVIEW-press-FINAL.md | PASS |
| db-hammer-curl | 13.947s | REVIEW-hammer.md | PASS |
| db-lateral-raise | 14.114s | REVIEW-side-FINAL.md | PASS |

## Dan's revisions applied

- Squat: trimmed16.049s to13.447s at the final word, with its accepted content, picture and grade preserved as a corresponding prefix (minor re-encoding difference). Five complete squats remain. Review11.5s to end.
- Battle ropes: trimmed15.449s to13.881s; short breathing cue fills the internal gap. Review8.4s to end.
- Push-up: trimmed15.349s to12.946s; breathing cue fills a pause before the final instruction. Review9.8s to end.
- Knee push-up: trimmed15.182s to13.614s; abs/rhythm cues fill the long middle gap. Review8.6s to end.
- Shoulder press: original419-frame accepted picture/ending preserved exactly by identical H264 elementary-stream hash. Middle pauses tightened using back/core/breathing/control cues; last word now finishes with the end of the picture. Review6.3s to end. An initial wrong feet-planted sentence was independently rejected and replaced with 'Keep your core braced'; old candidate/report retained.
- Hammer Curl: corrected name, narration and app identity db-hammer-curl. Neutral grip confirmed by independent native cue review; no real demo is installed into supinated db-curl. Useful grip/rhythm/control cues replace internal pauses. Review all13.947s.
- Side lateral: new real demo from Dan-accepted B0450. His approval of the source overrides prior pour-form hold. Full natural-speed original C1676 frames495–917, crop3360x1890 at240,180,14.114s. Widened after initial uncertain shoe-edge containment; actual source form was not rejected again. Review all14.114s. All original source footage remains intact.

Every demo is above10s and aims approximately15s. Last words finish with the picture; measured placement tails are approximately41–68ms, retaining natural word decay, with no added second of silent reps. Independent exact-file ASR/native frame checks support the complete words and directional cue endpoints. Accepted squat's instructional spacing was preserved in Dan's trim-only scope. Useful narration was added elsewhere to fill long pauses. No artificial speed, reversed reps, repeated fake continuous shots, graphic, caption or music added.

## Gates and independent checks

Both master/app audio stamps bind each current hash and pass synthetic in-app-demo measurement. All seven app delivery stamps PASS,39 pass-status rows each, comprising13 measured checks and26 declared format exclusions, no failing/unmeasured rows. Full master/native critical-edge and app comparison coverage is documented by independent reviewers; do not replace their stated sampling/native coverage with a claim that every pixel was manually watched at1:1. Watch judgments come from actual supplied images inspected. No gate thresholds or shared detector code were altered. The old format's narration-tail exclusion does not waive Dan's new rule; the separate actual endpoint and pacing checks are recorded in these fresh reports.

All automated audio/video inspection was silent. Methods include decoding, independent Whisper transcripts, loudness/true-peak/clipping/encode comparisons, waveform endings and picture/cue inspection. No audible listening, voice realism/timbre or human sound approval is claimed. Dan's review remains the final sound/form/content approval. R1 shared camera-reference selftest limitation is recorded in its receipt; no new camera regression pass is claimed. Rejected R2 draft reports/files remain archived separately; no findings were changed to a pass by the editor.

## Functional delivery

Full served SHA256 and206 byte-range requests verified for all11 videos (seven new1080p masters, four live current AI MP4s). Final HTML200. Phone390px and desktop1150px checked visually and without horizontal overflow. Actual media mute/paused state verified during silent seek/restart checks for every player. Final owner handoff verified all11 paused at0, loaded, unmuted, without playback. Temporary viewport reset. Per-player volumes were not changed. Sound-ready state is readiness, not owner content approval.

Evidence: final-http-qa.json, batch9-r2-browser-qa.json and screenshot proof beside this receipt in round2. review/manifest.json binds final displayed masters, app encodes and posters. R1 exact files rehashed unchanged; original R1 page archived intact as review-r1/. New exact-file manifests and reviewer findings are in round2/out/.

## Scheduling and ownership

The user-requested one-time10p.m. fallback fired on November15 at22:00 Central. M2 was verified idle, no manual R2 production had begun, and original chat01a1e07d-6d4d-7812-8af5-43a6bab12fa0 acquired its existing M2 route. The automation resume-batch-9-at-10-p-m was deleted, so it will not restart again. Other editing jobs arrived later; R2's remaining steps waited in the shared queues without changing other jobs' priority or stopping their work. No new editing chat or recurring monitor was created. Original chat remains sole owner.

## Saved policy

Documentation receipts pushed as ba8f19a. The timing rule, skill override and six owner rejection examples were isolated from other sessions' uncommitted edits and pushed as e998fe0 using a clean sparse worktree. Shared detector thresholds/code were not changed. Automatic Railway deployments and live checks are recorded in the final deployment verification receipt; these commits contain no new exercise-media install.

## Next step

Await Dan's review of these exact R2 files. Install only approved IDs/hashes under existing batch authorization, retain distinct db-curl's existing AI until a suitable separate replacement is approved, register approved real provenance and deploy with app checks/live verification. Do not ask deployment permission again. Do not mark batch installed or executed from this owner-review receipt alone.

## Exact clearance

```json
{
  "bw-squat": {
    "verdict": "SHIPS",
    "report": "REVIEW-four.md",
    "master_sha256": "0da54191405ab3c463bcb0fcabb8b1934cd83f70c13506a141e7d522b628940a",
    "app_sha256": "d17fa76d7022c07696b0747f3f7d989dd7ec330260bc3c3a8b893d731d741a21",
    "poster_sha256": "889fde3a7ebaeb1239eb409566b01821f0d2b4ec75ffc493e46491b014e6a9f6"
  },
  "battle-ropes": {
    "verdict": "SHIPS",
    "report": "REVIEW-four.md",
    "master_sha256": "de45cf128130d84f55a647c312e4f19be5138fdaa05570c72c003c196da634a1",
    "app_sha256": "116608e0d4cd9af077bb57ab7927bb1ad024954c5132b8ba192d745028d61f1d",
    "poster_sha256": "c2dfcd5cfb25d97df7f9a4ec0888094feb0d2433f88b413360a7868f4b2c7ff8"
  },
  "pushup": {
    "verdict": "SHIPS",
    "report": "REVIEW-four.md",
    "master_sha256": "c588c132560b57df9487a30a398549f4632de27f0d85c5fa551a3df86cf13a3d",
    "app_sha256": "4e8c76844eedfbdb7d91e9cc1f5ad9c27fccfb3e6b4a7c3ca4e73f191b4e4c8e",
    "poster_sha256": "2bb8e2fbddbb0a03bac67c9a6a21ed9346357006479642dc0fbe7867187e208a"
  },
  "knee-pushup": {
    "verdict": "SHIPS",
    "report": "REVIEW-four.md",
    "master_sha256": "688734958f9f5fa0ec06796b9487b7c61b9e9d810f167c596bd71c078a77ed55",
    "app_sha256": "82ef612120ddc86d6d51b1e473a6aded0fc68afcc644f55b1c45a12bb33e35f6",
    "poster_sha256": "ef60225b1156baaa14886915551ee263ce4aca6adab369e6eda3058c084bed13"
  },
  "db-hammer-curl": {
    "verdict": "SHIPS",
    "report": "REVIEW-hammer.md",
    "master_sha256": "8ac5c17ffc1559fc547b50c864f172284945ba6e2f7d0cd05221ff92c6814c1f",
    "app_sha256": "8643d3ff6d8aa5c5622eab3ef5aa98ea0db66e613b9a55721961f86c0f1c91ea",
    "poster_sha256": "a4346d083ee572f995341d5bfaf6cada1194f3d7d0831647c4e5936bb28c00a7"
  },
  "db-shoulder-press": {
    "verdict": "SHIPS",
    "report": "REVIEW-press-FINAL.md",
    "master_sha256": "6222eae322b4e9d993c919d359e4d1fed8413b6cc1b8344ec6149a6550e4f92c",
    "app_sha256": "2f9405e6ae55cc420fa2280c6e7a835548dedc47ae64ed38245e2bdaf3573d26",
    "poster_sha256": "e920dbdfe9480355f71fb34445aadffcb2f10824773523afdf8876bc3ca1f4a3"
  },
  "db-lateral-raise": {
    "verdict": "SHIPS",
    "report": "REVIEW-side-FINAL.md",
    "master_sha256": "02f0fb7284e2a4b39c02648352ffa41796ef340aef554a55eaa70eabce70231d",
    "app_sha256": "d5383d224792ce7159209554bbcc840042b82695a1bfd65d23f0233989008673",
    "poster_sha256": "34aef3ebc5a193402ebc891e9172ada70f7779ca2f3e0864ab3cfb85ed7b930f"
  }
}
```
