# CONTENT: Meal Prep SFC R5 complete color finish

Updated: 2026-10-15. Owner: Codex, Meal Prep SFC R5.

Color A, Clean and balanced, is applied to all 17 original-camera segments of the complete 59.5595-second Short, before approved graphics and captions. Dan selected the grade on 2026-10-14 and instructed that everything else was approved. The exact selected filter is in `Docs/DS28_APPROVED_COLOR_A_20261014.json`.

## Delivered files

Review: http://127.0.0.1:8891/ . Full-quality VLC copy: `Videos to Review/Meal Prep SFC R5 - complete Short.mp4`.

Authoritative master: `/Volumes/Extreme/_edit_work/ds28/round5/review/Meal Prep SFC R5 - complete Short.mp4`.
SHA256: `200afaaab059109b3fc168624136c0bb074d809d521d733ffee5b94ddf4298da`.
1080x1920, Rec.709, 1785 frames at 30000/1001 fps. Rounds 1-4 preserved.

The review folder includes the phone copy, unchanged SRT, unchanged approved audio comparison, three short color-context excerpts, exact-file stamps, editor and independent reviews, integrity evidence, manifest and reproduction ZIP. The maintained shared graphics templates are referenced, never forked. No covers, other formats, new stills/motion, uploads or publishing. Dispatcher stays paused; Victory Dashboard untouched.

## Revision and exact full-film watch ranges

Only original-camera color changed. Camera spans are 0:04.97-0:18.62 and 0:22.49-0:59.56. The opening and meal-reuse AI footage remain approved and unchanged.

- Wide view: 0:04.97-0:10.64, `wide-color-context.mp4`.
- Wide/tight check: 0:28.13-0:33.67, `tight-color-context.mp4`.
- Closing pickup: 0:53.05-0:59.56, `closing-color-context.mp4`.

Pair B tracking and crop map, both AI scenes and placements, seven graphics, every cut, caption text/timing, normal speed, pickup and four repaired graphic edge frames 457, 558, 843, 1349 are preserved. The R3 AAC is stream-copied. Extracted AAC SHA256 remains `72dc18a349f860e85b90a28dac6c33fa446f37b61b2667b9672907178c1de52c`. Reused R3 ASR is explicitly rebound to the R5 hash using this proof; no fresh transcription claimed.

## Review and exact-file status

Native review found no confirmed new color defect or unintended regression in the selected Color A build. The model review alleged an ungraded pickup from 53.05 to 59.56, but exact approved A and delivered frames match in both pickup framings. Existing automatic delivery gates still fail, so this is not a delivery pass.

Editor inspection covered all 17 camera hold interiors, all 3 chronological sheets, all 19 native boundary strips and pairs, the selected A comparison, and a supported complete audio/video review. The native scan read all 1785 frames with no frozen runs, black runs or unexplained jumps. All 531 mapped A-preview frames were compared, with median PSNR 45.81 dB and mean absolute pixel difference 0.782 at 270x480; six comparison pairs were inspected visually. Compression and denoiser history cause small differences. Original motion components were checked separately; copying old pixels alone is not the scene-content verdict.

Current delivery gate 2.6.0: {'PASS': 30, 'FAIL': 6, 'N/A': 3}. Aggregate remains FAIL. Audio gate remains FAIL on approved tone. Thresholds and approved creative choices were not changed. Exact current failed rows:

- `audio:stamp`: no valid audio-gate stamp: AUDIO GATE FAILED on Meal Prep SFC R5 - complete Short.mp4: tone -- fix the audio, do not deliver
- `framing:headroom`: 10 tracked talking holds + 6 intentional fixed-wide; per-hold min hair top [55, 199, 61, 60, 55, 55, 55, 56, 196, 52] (must sit in 30-70 normalized px inside its own window): 2 loose [(10.75, 199), (53.0, 196)], 0 tight []; median over the video 61 (max 75)
- `framing:no_wide_level`: 16 talking holds; head height (hair -> chin) per hold: smallest 18.9% of its window at 41.0s (min 27.0%); 9 wide hold(s) [(5.0, 0.19208), (10.75, 0.19672), (15.25, 0.1974), (22.5, 0.19099), (28.25, 0.19229)]
- `framing:push_coverage`: 9 talking holds on the dominant shot (head 19.2% of its window): per-hold median head height 18.9-19.7% = spread x1.045 (min x1.1); 0% of that talk sits >= 6 % off the dominant level; 7 hold(s) on other shots ignored
- `cut:splice_visibility`: 1/18 joins above the file's own p99 ceiling (36.45): [(56.22, 36.75)]
- `captions:sync`: 14 cues measured: speech starts a median -492 ms after the cue (worst -600 ms, max 120 ms)

This is a complete review candidate with honest automatic failures, not a certified release claim. Native image inspection and supported model audio/video review are recorded separately from automatic checks. No continuous human realtime full playback or native hearing is claimed.

## Costs and next action

R5 generation spend: $0. R5 review estimate from reported tokens: $0.110792; cumulative review estimate: $0.911640. Historical motion spend remains $1.40 of $5. Provider invoices and editor/reviewer session token totals unavailable. Per-call usage is in `review-ledger.json`.

Next: Dan reviews the complete R5 film and the three exact watch ranges. Do not start covers, setup, uploads or other formats from this delivery.
