# DS-109 R1 first-review production receipt

[First-review page](http://127.0.0.1:9810/)

Status: first-review packet rendered, checked and delivered November15, awaiting Dan’s choices. The full film has not been rendered or approved. No upload or scheduling.

Original chat: `01a1dc87-ce93-75c1-b1c7-9aac9dc8317a`, Hormozi Not Hungry Bored SFC R1. Resumed November 15 under direct supervision through first-review delivery. Actual remote production worker PID58358 on M2; `/Volumes/Extreme/_edit_work/DS-109`. Root handles local queue and user delivery.

The November 14 attempt queued capacity but failed to launch production after capacity became available. The November 15 resumed run produced real source, key, audio and picture outputs. Its first opening was rejected internally, not sent as ready: source face cropping, an exposed source-camera warning, a forearm cut by a garbage rectangle, and an irrelevant control-room background shot.

The source arm was recovered from the original native frames. The erroneous rectangles were removed; unaffected RGBA and protected head pixels were checked against archived caches. The first key cleanup then failed temporal checks. Independent testing distinguished a newer actual-alpha diagnostic from the required original house pale-composite proxy and retained both results. Moving all continuous body cleanup before the unchanged house temporal stage, restoring original protected head pixels afterward, passes the original house test. The production adapter reproduces all 81 prepared and final speech-calibration frames exactly and verifies the house temporal mathematics by AST comparison.

| Native calibration | House motion ratio | Hair ratio | Key skin rim | Source skin rim |
|---|---:|---:|---:|---:|
| Speech | 0.944 | 0.683 | 3.490% | 4.100% |
| Watching | 0.832 | 0.529 | 3.367% | 3.685% |
| Repaired arm | 0.952 | 0.680 | 2.428% | 3.117% |

Each uses 75 native frames with three neighbor handles each side. All three preserve protected head RGBA, clear zero opaque source-skin pixels and contain zero measured lossless pale-background specks. These are calibration results, not final-export approval. Raw failures remain available; no gate thresholds were loosened. Independent root report: M2 `r1/review-independent/continuous-body-order-before-stage15/INDEPENDENT_REVIEW.md`. Other matching receipts: `continuous-order-watch/evaluation.json`, `continuous-order-arm/evaluation.json`.

Opening plan: 28.06 seconds, 841 frames at 30000/1001. Portrait interview with 0.40 lower-left reaction; titled horizontal speaking panel at 4.004; one handover at 15.115; clean later interview-wide footage silently behind Dan from 16.383; moving Soft Blue Light after “Boredom wants chips,” at 21.121. The first corrected candidate `6d30132db36c23451d2768e40a3511b4e2561830588a92fb08dba4b6f1f3fa0b` cleared the original source/key/control-room defects, but its first-second caption touched the source host’s lower face. Caption-only repair is rendering: y1150 for frames0–27, all later caption positions unchanged. Independent all28-frame bounds give56.49px below the source face and70px above corner Dan’s hair. No full-film approval is implied.

Source: original C1909 from the 11/13 green-screen shoot, decoded portrait2160×3840, no added transpose, S-Cinetone/Rec709. Measured live lav is channel0. Scripted version chosen; whole source inspected, off-the-cuff comparison not judged stronger. Interview: The Iced Coffee Hour Clips, YouTube `A9TMIcajf8A`, quote starting782.70; later clean silent wide from source851. Real R5 laptop-lid layer is disclosed because no laptop was visible in C1909. Protein card uses real egg photo B0046 and Dan’s real labelled sardine tin from C1908 native frame375; no fake prop performance. Crossed-out carb photos are existing real library assets. No new AI image/video generation.

Four speech-first level-matched voice options use the same30 seconds. Five randomized file-model trials did not reliably distinguish untreated/bass-default/fitted finalists; bass default follows the standing preference. Three grades compare matching wide/tight frames and matching moving samples. No human audible listening pass is claimed. Actual file-model billing is unavailable; token usage is recorded in production logs.

All1,057 final body-cache frames are complete and bound through `ACTIVE_KEYS.json`. Color samples, four voice auditions, narrated food context and current key proofs are rendered. The managed review page is published internally on both Macs at port9810. A task-local peer config uses a verified LAN connection; shared SSH/routing configuration and core/slot limits were preserved.

M6 checks on the6d30 packet:29 linked assets returned HTTP200; all media ranges returned206; served opening bytes matched the producer hash. Headless Chrome played and sought all11 unique previews/auditions while actually muted. It finished paused, unmuted, volume1, ownerReady with no recovery/failure. Phone and desktop were visually inspected; no horizontal overflow. No audible human listening is claimed. Browser and HTTP receipts were copied into M2 `r1/root-qa/`.

Actual G00 hash `828bc49b54a4b6e7df916297c1fcdbbceedeff276a1187bdaf58e910d5cdd02a` passed all120 source-overlay frames independently: first-shot264px band, second-shot224px band; source warning covered; conservative clearance23.33/24.22px. Proposed geometry was not substituted for the delivered graphic during this test.

Final opening SHA256: `0687c6c688ea00eaeb63ba71f801c6378398dbf5dc7df9d9bb19cea8e8504913`. Size28,104,603bytes;841frames;28.061367seconds. Independent verdict: READY FOR FIRST REVIEW OPENING ONLY. Actual first28 caption frames and frame28 return were inspected; previous critical cuts showed no regression. Full native decode found no black frames or exact adjacent duplicates. AAC bytes exactly match the6d30 export, ADTS SHA256 `f83067a4bc162b5130ec3d2bdf1e3a43461a78dd9e21b1b597e1a2bf099c8727`. Canonical M2 report: `r1/independent-qa-final-opening/report.md`; evidence `caption-repair-0687c6c688ea/`.

Both managed caches were refreshed. M6 HTTP returned the exact final0687 bytes with correct206 byte ranges. A fresh M6 Chrome check played and sought the repaired opening while muted, returned it to time0 paused, verified preservation of an explicitly chosen zero volume, then handed off paused/unmuted at volume1 with ownerReady and no recovery/failure. Owner-mode desktop rendering was inspected. Earlier all11-source playback/seeking and29-link checks remain valid for unchanged assets. Actual final receipts are in M2 `r1/root-qa/m6-final-http.json` and `m6-final-browser.json`.

The Codex browser-open request was queued by the desktop app, so this receipt does not claim the panel visibly opened. The working local review link is delivered directly in chat. No review file reaches45seconds, so an extra Videos to Review copy was not required.

Dan’s remaining actions: review opening/key; choose color and voice; approve or revise food cards using the one reply box. Only then build the full film. Articles are handled after release by sixpackabs-article-gap-daily. No covers, upload or scheduling were performed.

Queue/master: delivered revision5, with explicit first-review-only scope. Drive status upload verified. The follow-up review handoff synchronized through a task-local LAN peer config; the producer had already released its edit slot, so no current slot remained to release. No duplicate queue revision was created.
