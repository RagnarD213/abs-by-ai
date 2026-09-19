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
| GoPro 1 `GOPR0044` / `GP010044` | Long low floor angle covering pushups and core takes. | second angle, verify what is on it |
| GoPro 2 `GH010277` | Very low close angle of handstand pushups. | bonus angle |

Roll sidecars (`<roll>.roll.md`) sit next to each file with timelines. **C1678 is NOT pushups** (it is ab wheel; the old
shoot report mislabelled it). C1671 (about 2:20 to 3:50) holds the talking for the separate short DS-20; do not lift from it
without checking, it is written for the short.

## Script
Outline: Shoot 5 doc `1yZjcG5pkbw0kPsfTvc7OOr2bX6v0bVYMqquUiRENQ4k`, Section 2, "Pushup Masterclass". Same content in
`1ND_BTQKfIIBdfBC_WJGhxc_SZHtQFh32HI3ksD_dIVo`. It is DEMONSTRATION ONLY: there is no workout-only cut.
The six levels: 1 incline (couch/table/wall), 2 knee, 3 standard floor, 4 standard with handles, 5 close-grip on handles,
6 decline (feet up). Rule for moving up: 3 sets of 15 clean reps.

## Known gaps to resolve FIRST (list them before building)
* **Level 1 (incline / countertop):** the shot list put this in the kitchen. Nothing on C1680/C1681 shows it. Search GoPro 1
  and the other 8/28 rolls; if it does not exist, say so and stop for Dan (options: film a pickup, or drop to 5 levels).
* **Level 5 (close-grip):** confirm whether the last part of C1680 (after about 3:00) is close-grip or just handles at
  shoulder width.
* **On-camera talking (intro, "why pushups", form rules, when to move up, CTA):** the sidecars found no speech in C1680 or
  C1681. Search every 8/28 roll (run `pick_lav.py` per file, transcribe the roll sidecars marked `not-run:lav-unresolved`)
  for Dan talking the masterclass. If none exists, the video is a silent demonstration with on-screen text cards plus the
  voice-over question for Dan. Do not invent narration in his voice.
* C1680 and C1681 are also named as b-roll for DS-20 ("Five Levels Of Pushups"). Coordinate so both cuts stay consistent.

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
