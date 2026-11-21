# Ad 10 "My Dad Bod At 38, My Dad Bod At 40" 1:1 square, full + 57 second cutdown (2026-10-04/05)

Built by Claude (Opus 5.5 high, session "My Dad Bod At 38 S/Sh Ad R2") as a re-layout of the approved vertical (`notes-vertical.md`): the same
timeline, cuts, graphics wording (Soft Blue Light), flashes, caption timing and audio. Each square's audio stream is the matching vertical's AAC
stream copied byte for byte (packet md5 `f552a844696ce1fbb6d111ad42cadafa` full, `ca5d023f23582b7773c95f9d5668bb75` cutdown, asserted at the mux and
re-checked on the delivered files). The cutdown is the vertical cutdown's three sections (0:00 to 0:30.06, 1:30.22 to 1:48.17, 2:52.51 to 3:01.62 of
the full) and its picture equals the full square's picture frame for frame (max difference 0.5 grey levels above the caption band, all 1,712 frames).

| File | Length | Frames | Video bitrate | SHA-256 |
|---|---|---|---|---|
| 1x1 (full) | 3:01.615 | 5,443 | 10.6 Mbps | `f2c98162b8aa3ced8abeeeacf6008fa22bd856e80d17912aa626ac1e18ca22eb` |
| 1x1 59s (cutdown) | 0:57.124 | 1,712 | 9.8 Mbps | `fa7c29462157ef9cda50eb8c45f5065e61a83d3c064aee9777782752109bf480` |

## Dan's one change: the calmer camera

Applied as the standard "land on him, then hold" track (policy `vertical-land-then-hold-20261003`, tolerance 20): crop travel 2,052 px,
the crop moves on 40 % of talking frames, he sits 15 px off centre at the median (gate: worst 3.8 % of the window, bound 6 %).
The shared tracker needed the same correction as on Ad 6 round 2: zoom times are not landing anchors (the first render had 16 one-frame sideways
jumps of 11 to 57 px at the start and end of each zoom; `camcheck.py` now reports none on the full square). The first minute on the 10-03 look page
was rendered with the older, busier track.

## What the full builds found, and what changed (each from judges, reviewers or the gate, not from the builder)

- **The editor's lifts leaked the NEXT shot.** In seven lifts of his master the last frame (and up to 8 frames on the second daughter photo) belonged to the
  next shot: Dan's talking head or a flash inside a card, a one-frame crop pop, the wrong label. Each lift now holds its last clean frame.
- **The 2:52.5 hand-off to the phone screen.** The editor's beach clip ends at 2:52.47 and his phone blur-in follows; the first build ended the beach beat
  10 frames late (frozen picture under "So generate"), and the cutdown opened on that stray tail. The beach card now plays to its last frame and the
  phone card starts at 2:52.506, the vertical's own cut. The 10-frame stray tail of the vertical (olive grid and blur-in at the start of its section 3)
  is not reproduced.
- **4 px black bars** at the top and bottom of all four AI clips lifted from his master: trimmed (8 px each side; a 5 px trim left one grey row).
- **Two visible pause splices** that the 608 px vertical window hides, at 15.9 s and 37.87 s (his mouth and hand jump in one frame): a square-only
  closer zoom step on each (1.4 s, eased out), declared in the gate's plan.
- **Hair at the frame edge.** The AI pool picture of Dan (three uses) and the park photo are anchored at the top. The two daughter selfies, the kitchen
  stock clip and the four AI clips go in cards because the picture's own edge cuts a head or the label has no clear spot (reason per picture in
  `recipe-square/sq_copy.json`). Dan's rule is fill unless there is a reason; the reasons are written down.
- **Labels.** The AI picture cards keep the editor's own small burned AI-GENERATED chip and carry no second pill, as in the approved vertical. The gym
  picture's hand-placed chip sat on the left man's hair (gate: whole chip inside the person mask) and is gone with the card.
- **Slow pushes on stills** stepped every other frame (about half a pixel per frame rounds to whole pixels): now pushed at 2x and scaled down.
- **Captions.** The gate's caption images were still olive (7 states failed to match): recoloured to the cyan. The caption "years younger." ran 5 frames
  over the new phone card: not drawn there, and its cue ends at the cut.
- **Encode** at CRF 12 with the 12M cap (the square rules ask 8 to 12 Mbps; CRF 15 gave 6 to 7).

## Left as built, for Dan to know

- The AI beach runner carries an orange sun-flare spot that drifts over his stomach and chest (in the editor's clip and in the vertical).
- Two label styles for a real photo: the pill under a card, and the kit's chip on full-bleed photos (3 lines; the flex photo's wraps to 2).
- Flashes: the cut lands 2 to 3 frames before the flash peak (the vertical's timing, kept).
- The park photo's hair is 14 px from the top (the photo's own crop; the delivery check measures talking heads only).
- "40" at 0:22.9 is not captioned (inherited from the vertical: the "HOW I DID IT" lower third starts there). Both round 2 reviewers listed it as should fix.
- The man holding the phone (0:33.07 to 0:35.17 of the cutdown, 1:33 in the full): the square crops the bottom 15 % of the editor's portrait clip, which removes his
  burned "AI-generated" tag, and our pill sits under the card instead (one label either way). Round 1 chose this crop; the 2026-10-01 rule says an editor's burned
  label stays whole. Dan's call: keep, or restore the uncropped clip.
- After the punch-in cut at 0:33.03 the picture settles 34 px sideways over 8 frames (the track landing; the calmer camera still moves there).
- The opener is the shirtless deck-chair before photo on a card in the first 3 seconds (the stomach is the point of the before picture; same as the
  approved vertical). Dan's 10-04 belly rule landed after the look lock: his call.
- The approved vertical shows the stray blur-in tail at 2:52.5 to 2:52.84 and the master's flash inside the second daughter card; the square fixes both,
  the vertical was left untouched.

## Checks on the delivered files

- Delivery gate 2.4.0 (ad1x1) PASS 39 of 39 on both; audio gate 2.0.0 PASS on both; every stamp's sha256 matches its file.
- Camera check on the full square: 0 isolated crop steps over 6 px; max pan 6 px per frame.
- Judges: six rounds of fresh Opus 5.5 sessions (three per file per round). Final pass: 256 verdicts over 250 images on the full file and 84 over 83 on
  the cutdown, 0 open defects; an image unchanged from an earlier round was carried only where pixel-identical (same time, same size, and its pair image).
- Independent review (fresh `ra-reviewer`, did not read these notes): round 1 `ROUND-1-REVIEW-*` (both DOES NOT SHIP: a frozen beach picture before the phone card;
  fixed); round 2 `ROUND-2-REVIEW-square-full.md` and `ROUND-2-REVIEW-square-cutdown.md`: **SHIP on both**, no blockers.
- Nothing uploaded. This is an ad: Unlisted via `/ad-setup` only after Dan approves. Spend: $0.
