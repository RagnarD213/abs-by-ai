# RO-09: "Pushup Masterclass: 6 Levels From Beginner To Advanced", first cut from raw footage

**List 1 · organic long-form (raw only) · READY.** Read `00-RULES.md` first. Added 2026-09-19 at Dan's request: he confirmed
the masterclass was filmed on 8/28, near the end of the shoot. The earlier "not yet filmed" lists were out of date.

## Source (8/28 shoot, main camera, 4K 29.97 S-Log3)
Folder: `/Volumes/Extreme/abs by ai 8:28 shoot | jeff | dan | ads, dedicated shorts, b roll, scripted long form content/main camera/`

| roll | what is on it | use |
|---|---|---|
| **C1680** (4:24) | The main ladder. Dan on the blue mat by the pool, profile angle, far framing. Knee pushups, standard pushups, then pushups on handles, with kneeling rests between sets (he faces the camera at the start and between sets). Silent: mean audio -78 dB. | levels 2, 3, 4 (and probably 5, verify) |
| **C1681** (0:56) | Elevated pushups, feet on a chair, hands on handles. | level 6 (decline) |
| **C1684** (0:40) | Handstand pushups against a pillar, patio, dim light. | optional bonus "beyond level 6" beat |
| **GoPro 1 `GOPR0044`** (8:53, has audio) | Second camera, low floor angle, same mat session. Dan speaks a slate before every clip: knee pushups, regular pushups, mistakes (half reps, butt in the air, sagging back), regular with handles, **close-grip with handles (level 5, confirmed)**, then the chair. Sidecar with transcript: `regular gopro 1/GOPR0044.roll.md`. | second angle for levels 2 to 6, and the mistake clips; the slates are the map |
| **GoPro 2 `GH010276`** (15:44, has audio) | Same session from a third angle, same slates (knee, regular, mistakes, handles, close-grip, decline off the chair). Sidecar: `regular gopro 2/GH010276.roll.md`. | another angle, same use |
| `GH010277` | Very low close angle of handstand pushups. | bonus angle |

Roll sidecars (`<roll>.roll.md`) sit next to each file with timelines. **C1678 is NOT pushups** (it is ab wheel; the old
shoot report mislabelled it). C1671 (about 2:20 to 3:50) holds the talking for the separate short DS-20; do not lift from it
without checking, it is written for the short.

## Script
Outline: Shoot 5 doc `1yZjcG5pkbw0kPsfTvc7OOr2bX6v0bVYMqquUiRENQ4k`, Section 2, "Pushup Masterclass". Same content in
`1ND_BTQKfIIBdfBC_WJGhxc_SZHtQFh32HI3ksD_dIVo`. It is DEMONSTRATION ONLY: there is no workout-only cut.
The six levels: 1 incline (couch/table/wall), 2 knee, 3 standard floor, 4 standard with handles, 5 close-grip on handles,
6 decline (feet up). Rule for moving up: 3 sets of 15 clean reps.

## Known gaps (status 2026-09-19)
* **Level 5 (close-grip): FOUND.** Slated "close grip pushups with handles done right" on GOPR0044 and GH010276; the matching stretch of C1680 is the main-camera version.
* **Level 1 (countertop, outdoor kitchen): NOT ON THE DRIVE (searched exhaustively 2026-09-20).** Dan says it was filmed outdoors
  right before the floor pushup b-roll. All four cards of the 8/28 shoot were searched (Jeff says "four cards to download" on
  GH010278): main camera C1646 to C1685 (every contact sheet and transcript; the outdoor kitchen is the covered patio in C1684
  and C1685, which hold only handstands and battle ropes), GoPro 1 (all four clips, frames and slates), GoPro 2 (all six clips),
  and the 360 clips. Dan slates every clip out loud ("I'm now going to show ..."); no slate anywhere says countertop or
  incline, and GoPro 1 ends its ab wheel clip with "Let's go to our push-ups on the ground". Next: ask Dan or Jeff whether it
  was shot on a phone or a fifth card. If not found, film a 30 second pickup at the outdoor kitchen counter (on the next
  shoot list) or build the video as five levels. Do not fill level 1 with AI.
* **On-camera talking (intro, why pushups, form rules, when to move up, CTA): NOT FOUND YET.** Every talking roll's transcript was
  searched (C1650 to C1672). The only pushup talking is the short DS-20 on C1671 (the five levels, 137 to 230 s). Same open
  question as level 1: Dan says it was filmed outside at the end of the shoot, so it is probably on media not on the drive.
  If it never surfaces, the fallback is a silent demonstration with level cards and text, or Dan records it as a pickup.
* C1680 and C1681 are also named as b-roll for DS-20 ("Five Levels Of Pushups"). Keep both cuts consistent.

## Build
* Codex first cut per the queue routing (`scripts/edit-queue/config.json`), `$abs-edit-organic`. Model the structure on the
  approved organic standard (Zeeshan's ab wheel videos).
* 16:9 master + SRT. Level title cards (LEVEL 1 to 6), on-screen rep counter or set label, the "3 x 15 clean reps" rule as a
  card, AbsByAI.com CTA end card. Labels per `00-RULES.md` section 2.
* Colour: 8/28 S-Log3 conversion, decoded as BT.709 (untagged files). Per-clip trim; C1680 is a stop or so dimmer than the
  pool rolls. Audio: silent b-roll, so music bed only unless real talking is found.

## Starter prompts
**Claude (Opus 5, high):**
> Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/RO-09-pushup-masterclass.md`: first list the gaps (level 1, level 5, any on-camera talking), then cut the Pushup Masterclass from 8/28 rolls C1680, C1681 and the extras to the approved organic standard. Every gate, independent audit, deliver, send me the review copy, update the master list.

**Codex (GPT-6 Astra, high):**
> Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table), then execute `Handoffs/video-editing/RO-09-pushup-masterclass.md` with `$abs-edit-organic`. List the gaps first, deliver, send Dan the review copy, update `00-MASTER.md`.
