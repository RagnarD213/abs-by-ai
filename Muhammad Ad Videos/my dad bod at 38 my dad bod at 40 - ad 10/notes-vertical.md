# Ad 10: 9:16 vertical and 57-second cutdown

Built from Muhammad's finalized 16:9 Ad 10 with the locked 9:16 production kit. The picture was decoded as BT.709 from the start. Muhammad's approved audio remains untouched in the full version. The cutdown uses only clean sections of his mix, joined at the selected edit seams with no gain, limiting, compression, EQ, or other processing.

## Delivered files

| Version | Duration | Frames | SHA-256 |
|---|---:|---:|---|
| Full 9:16 master | 181.615 seconds | 5,443 | `b25b6e50e106cc4c6407fc949ff6edda25ceab8b1c75a559eff6427b0fc32cc6` |
| 9:16 cutdown | 57.124 seconds | 1,712 | `36ae2f6d528ebf34692e81040343c88d17046eff27a25bc1c266f2fd816dd00f` |

Both masters are 1080 by 1920, H.264, 30000/1001 fps, with 48 kHz stereo AAC audio. The 540p review copies retain the masters' audio streams and were separately checked against Muhammad's source mix.

## Cutdown structure

The 57.124-second version uses three complete sections from the full vertical:

1. 0:00.000 to 0:30.063: hook, real proof pictures, and the AI mechanism.
2. 1:30.223 to 1:48.175: goal image, lock screen, identity shift, and real payoff.
3. 2:52.506 to 3:01.615: final app invitation and button CTA.

Every cut is at a picture boundary and a clean audio seam. The same person is used before and after in each app demonstration. No banned email or mismatched-person result screen appears.

## Labels

Every real picture of Dan has the real-picture label. AI pictures have the AI-generated label. A fresh independent exact-frame review checked the two cutdown appearances and their transition frames. Both labels are fully readable, above Dan's head, and clear of his face and abs. The full version passed the same label gate.

## Final verification

Both exact master files passed the current 39-row delivery gate with 39 of 39 rows and no failures.

| Review | Full version | Cutdown |
|---|---:|---:|
| Fresh assigned visual judgments | 241 | 82 |
| Reviewed transitions | 116 of 116 | 39 of 39 |
| Open defects | 0 | 0 |
| Negative-event findings | 0 of 30 | 0 of 30 |
| Delivery gate | PASS 39 of 39 | PASS 39 of 39 |
| Audio gate | PASS | PASS |

The full visual review used three fresh GPT-5.6 judge sessions. The cutdown used three separate fresh GPT-5.6 judge sessions plus a fresh exact-frame label-clearance judge. The build session did not grade its own evidence.

Audio proof on the exact masters:

- Full: source correlation 1.0000, level difference 0.00 dB median, -13.50 LUFS, true peak -1.00 dBTP.
- Cutdown: source correlation 1.0000, level difference effectively 0.00 dB median, -13.60 LUFS, true peak -1.00 dBTP.

The `recipe-vertical` folder contains the build scripts, plans, gate reports, audio stamps, and independent judgment records needed to reproduce or audit the work.

The complete 96-entry shared quality corpus was also run after the tooling fixes. All 95 entries relevant to the changed delivery checks behaved as expected. The runner still reports one pre-existing mismatch on approved DS-17 outdoor audio: its corpus entry intentionally requires the indoor audio-artifact row to pass while its own note records that the exact file fails that row. AV-07 changed no audio-gate code, and neither AV-07 file has that failure.

## Approval state

These files are delivered for Dan's review. AV-07 remains delivered, not finalized, until Dan gives his verdict. AS-06 remains blocked until that approval. Dan's exact verdict will be recorded in the shared quality corpus after he reviews the copies.
