# Independent motion audit: Bill Maher Asks If You've Ever Seen A Fat 90-Year-Old. He's Right. (DS-40), Round 3

**Verdict:** The final Round 3 hair treatment is materially cleaner than Round 2 and is suitable for Dan's review as a 10.01-second calibration. Fine loops and individual strands remain visible. The green and gray speckle inside the hair is reduced, with no clear lost-strand, broad helmet, or ghost-trail regression in the examined native frame runs. It is not flawless: a faint gray halo and small edge-color variations remain when enlarged, most noticeable near the viewer's right side of the hair around 8.5 seconds. Dan has not approved this round or a full Short.

## Exact files

| File | SHA256 |
| --- | --- |
| Round 3 sample, `review/media/sample.mp4` | `1c07c3d3c585fe05a7a2f1274d4a62bec46de1e6be7bdbfb4214f44af2b7ace1` |
| Round 3 light/dark comparison, `review/media/hair.mp4` | `89d1e7eead74f5f0d2cf22956823c5fcef1335f9b39b89716970946c83dd4fc9` |
| Round 3 dark check, `review/media/dark.mp4` | `7feff3e5dd55309250a7ba0b579ee1debd41b28c5b9ae33616654aa430148cf4` |
| Round 3 phone copy, `review/media/phone.mp4` | `1c22d4e9fbda034028be96126d7cb056ae147c77fdc07de454d5225adc14e86b` |
| Round 2 Balanced reference | `622ec8a71b344a13496277ce3e7c3de17a8229d6d7d71bcea1084256273d0100` |

The final comparison shows Round 2 on the left and Round 3 on the right, with a light background above and dark background below. The earlier Round 3 render was superseded by a background color correction. I rechecked the final hashes and final moving comparison, not just the earlier render.

## Motion findings

| Time | Observation |
| --- | --- |
| 1-3 seconds | Six consecutive frames at 1.902-2.069 seconds on each background show less speckle and fewer apparent internal openings in Round 3. Curved fine strands remain. No obvious trailing silhouette appears. |
| 4-6 seconds | Six consecutive frames at 4.905-5.072 seconds retain hair volume and fine texture. The right edge has small color changes frame to frame, but is cleaner than Round 2. |
| 7.9-9.1 seconds | Runs at 7.908-8.075 and 8.509-8.675 seconds keep the hair connected without a hard cap. A slight gray/purple haze and a brief uniform-looking patch near the top-right are still visible enlarged, especially on dark. These are residuals, not a material regression. |

I reviewed the exact final watch sheet, all eight final consecutive-frame strips in `audit/final-native-*.jpg`, four full-size final sample frames in `audit/final-full-*.png`, and exact final sampled video through Gemini at 24 fps. The sampled video review also found reduced holes and edge color, with minor remaining flicker in all three target windows. It did not find lost strands, broad blur or ghost trails. Video-model sampling cannot certify every native 29.97 fps frame, so the consecutive strips and automated 300-frame scan are separate evidence. I could not use the browser player for my own full-speed playback because local file navigation was blocked by its URL policy. The parent session owns the browser playback check.

The full sample frames and sampled video show glasses, arms and hands staying intact. The widest native camera view lets some fast hand gestures approach the side edges; this is inherited source framing and outside the hair-only revision. The 300-frame watch scan reports no frozen or black frames, jump candidates or naked splice candidates. This one-shot test has zero edit boundaries, so that scan does not establish a boundary pass.

## Audio and gates

The AAC identity recorded in `audio-identity.json` is `ac037d52c91550a82c92b8b6af6b0e33537425c13602413d409672d1bfce7a7a` for the approved Balanced track and all four Round 3 MP4s. The exact sample's delivery log checks five audio-to-source checkpoints at -0.021 ms each and reports 300 frames over 10.010 seconds. A separate WAV review heard continuous clear speech with no dropout. It suggested possible small lip delay at coarse timestamps, but that was not corroborated by the exact source alignment check, so I do not record a sync defect.

The exact audio gate still fails comb and tone. Those are the same known Balanced-voice measurements Dan accepted, not an invitation to reopen the audio choice. The watch sheet has one clean finding, zero expected and zero defects. `watch.py --judge` records that image judgment, but the delivery gate's nonzero-boundary watch requirement cannot be met on a continuous sample. Do not claim an all-pass gate.

## Cost and limit

Four Gemini quality-review calls cost **$0.0696 total**, including one final hash-bound sampled-video call costing $0.0200. No generation or render spend occurred in this audit. The model's moving review is useful corroboration, not proof of native full-motion quality. This verdict is for Dan to compare the hair sample and decide whether to move on to the full Short.
