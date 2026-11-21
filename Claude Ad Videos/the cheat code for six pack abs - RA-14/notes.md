# RA-14 "The Cheat Code For Six Pack Abs": 9:16, round 4 (2026-10-14)

AD (short-form, filmed). Claude Opus 5.5. Built from the round 3 parts Dan approved on 2026-10-14 ("Everything is approved and
looks good. Give me the handoff to build the full video in the next round.").

## The file

`the cheat code for six pack abs | claude | 9x16 | RA-14.mp4`: 1080x1920, 30000/1001, 1482 frames, 49.45 s, H.264 BT.709 +
AAC 256k, sha256 4b520fd149ddb1d0. Review copy: `... | REVIEW 540p 9x16 | RA-14.mp4`. VLC copy: `Videos to Review/Cheat Code Six
Pack AD R4 - full 9x16 ad.mp4`. Build folder: `/Volumes/Extreme/_edit_work/ra14/round4/`. Recipe: `.claude/skills/ad-edit/reference/ra14/round3/`
and `round4/`.

## Take map (roll C1667, 8/28 pool shoot; times in the roll)

| range | lines | roll in-out |
|---|---|---|
| R1 | hook + setup ("Guys..." to "...how it works.") | 340.09 to 351.63 |
| R2 | step one ("Step one..." to "...completely free.") | 357.54 to 366.78 |
| R3 | step two ("Step two..." to "...get you there.") | 366.78 to 379.23 |
| R4 | step three a ("Step three..." to "...the whole way.") | 382.70 to 387.00 |
| R5 | step three b + recap ("Whatever problem..." to "...always there.") | 394.01 to 408.92 |
| R6 | CTA ("Tap the button below now to get started.") | 412.33 to 414.69 |

Nothing scripted was dropped. Fresh transcript of the delivered file: 178 of 178 intended words heard.

## Choices this round

1. **Locked parts used as they are.** All 16 locked files re-hashed against the handoff table (`round4/HASHES.json`): all match. No
   locked part was re-rendered. Picture frames 0 to 1469 are the approved picture's own packets.
2. **Ending moved to the held smile (new this round).** The watch-pass judge and the independent reviewer both found that the last
   0.97 s of the take showed Dan mouthing words with no sound, then stepping right out of frame with the crop following him. Dan had
   only seen the first 30 s finished, so he had never seen this. The film now ends at frame 1481, the last frame of his closed-lip
   smile with steepled hands under the button: 1.08 s after "started.". The button is up for 3.0 s. Frames 1470 to 1481 were
   re-encoded from the same source frames with the same settings (PSNR 48.6 dB), because a plain cut broke the last frame.
3. **Music tail smoothed.** After the last word the bed had two rests (49.25 and 49.65 s) that measured a 15.7 dB swing with the
   fade divided out, the same size as RA-01's step that needed fixing. Corrected on the mix itself, only after the last word, so the
   approved voice is untouched: identical to Dan's approved mix up to 48.42 s (integer null test). Swing now 3.7 dB (RA-01 approved
   at 4.5). The last 0.5 s fades to silence for the new ending.
4. **Audio gate: one known row.** `tone` fails by 0.04 dB on the 80 Hz band (2.54 vs 2.5) because of the bass lift Dan made the
   standard on 2026-10-12. His approved voice (`mix_bass.wav`) read 2.55 on the same row. VIDEO-RULES calls this "the known mismatch,
   not a reason to drop the lift". Every other audio row passes, -14.2 LUFS, true peak -2.2 dBTP. The outdoor `artifacts` row the
   handoff expected to fail passes here (flux 0.094 against the untreated 0.109).
5. **Delivery gate 2.6.0: 38 of 39 rows pass;** the one failure is the audio stamp above. Watch pass: 56 of 56 images and 27 of 27
   boundaries judged by a fresh subagent, 0 open defects.
6. **Edit sheet: not written for the 9:16.** `sheet_from_claude_build.py` reads 16:9 builds only. The sheet gets written with the
   16:9 after Dan approves this.

## For Dan's eye (all inside the approved first 30 s unless marked; not changed)

- 10.54 s: the close shot opens with you a little left of centre and the crop catches up over about a third of a second. Same as the
  approved round 3 cut.
- 14.18 s: for a single frame, a sliver of your real upload photo shows on the phone before the real-picture label appears. Not
  visible at playback speed.
- 15.78 to 17.55 s: the caption runs over the bottom of your AI goal picture (over the shorts), as approved.
- 36.3 to 38.3 s (new part): over "a home workout when you can't make it to the gym" the app's Push-Up demo is filmed in a gym.
  It is the approved app tour; flagged in case you want a home-setting demo there.

## Gate plan geometry

`round4/plan.json` from `s93_gateplan.py`: label chips redrawn by the calls that drew them (`s92_chips.py`); phone rectangles
measured on every card frame (`s94_phonebox.py`: the phone ends at y 1348, the shell image's box at 1386); one full-frame
talking-head window per hold; full-screen cards listed in `punch` as covered. Independent review: `round4/ROUND-4-REVIEW.md` (on the
1512-frame version; its one blocker was the ending, fixed above).

## Next

After Dan approves this 9:16: the 16:9 from the same edit (analysis card 16:9 layout is built; lower thirds and R1 use the 16:9
templates; horizontal framing static per shot), its edit sheet, then `/ad-setup`.
