# 9/23 shoot: raw footage report

Audited 2026-09-23 by Claude from the files on the drive (frames at native 4K, audio measured with
`_shared/audio`, every roll transcribed). Folder:
`/Volumes/Extreme/dan rose fitness 9:23 shoot - vsls, long form content, short form content/`

## Format (different from 8/28)

- Sony FX30, 3840x2160, 29.97p, XAVC 4:2:2 10-bit, **S-Cinetone** (not S-Log3). Grade it as Rec.709, never
  through the 8/28 log LUT.
- Audio: **one stereo stream, dual-mono** (L = R, correlation +1.000). One mic only, so no comb filter
  risk and no backup mic. `pick_lav.py` prescribes `-map 0:a:0 -af "pan=mono|c0=0.5*c0+0.5*c1"`.
- **C1716 to C1720 are portrait rolls**: stored 3840x2160 with rotation -90, decode to 2160x3840. Do not
  add a transpose.
- Camera clock is wrong: metadata says 2026-09-22 22:52 to 2026-09-23 04:54 at -06:00 (about 12 hours off).
- 32 rolls, 208 GB, 188.6 minutes. C1640 (Aug 22) and C1688 (Sep 16) are leftover clips from earlier
  cards, not this shoot.

## Roll map

| rolls | content |
|---|---|
| C1689 | empty set, mic test |
| C1690 | framing test |
| C1691 | tube light hue tests (blue 200, green 90, red 0, purple 297) |
| C1692 | slate, VSL 1 version A, false start |
| C1693 to C1696 | VSL 1 version A, hook restarts (C1696 runs 2.8 min) |
| C1697, C1698 | VSL 1 version A, full run (12.5 + 7.1 min) |
| C1699 | VSL 1 version B "fired them all" intro |
| C1700 | VSL 1 version B pickups |
| C1701 | VSL 2 /start full cut |
| C1702 | VSL 2 /start hook takes |
| C1703 | VSL 2 /start pickup lines P1 to P3 |
| C1704 | Calories: The Reason You're Not Losing Weight |
| C1705 | When Calories Don't Matter For Fat Loss |
| C1706 | Top 5 Zepbound Tips |
| C1707 | Can You Drink Alcohol And Still Have Abs? |
| C1708 | Why You're Not Losing Weight |
| C1709 | Sleep Better With Glycine |
| C1710 | If I Had Belly Fat, Here's How I'd Lose It In 90 Days |
| C1711 to C1713 | 3 Healthy Foods That Made Me Fat (C1711, C1712 are prompter false starts) |
| C1714, C1715 | How To Make Time For Exercise & Nutrition (split across two rolls; camera nudged left at the start of C1715) |
| C1716 to C1718 | vertical set, silent tube colour tests |
| C1719 | Shorts: Wispr Flow (with alternate hooks), Home Workouts |
| C1720 | Shorts: Meal Prep, Robot Lawn Mower, Self-Driving Car, AI Homework, AI Job |

Everything on the shoot checklist that is a talking piece was filmed: both VSLs, all 9 long-forms, all 7
shorts. **Not on this card:** M100 pickups, countertop pushups, robot mower footage, the cold opens and
`[FILM]` b-roll cues, and the short-form alternate hook takes (only Wispr Flow has them; Dan will film hook
takes at the next shoot). The Wispr Flow ScreenFlow demo (started at C1719 1:14) is with Dan, to be uploaded.

## Measurements

| | 16:9 set (C1689 to C1715) | vertical set (C1716 to C1720) |
|---|---|---|
| median luma / 99th pct | 0.16 / 0.65 (dark) | 0.20 / 0.83 |
| clipped / crushed pixels | 0.1% / 0.3% | 0.1% / 0.04% |
| face vs backdrop luma | 0.23 vs 0.24 (no separation) | 0.24 vs 0.23 (no separation) |
| face sharpness vs backdrop | 1.2x (soft) | 0.9x (face no sharper than wall) |
| Dan's width in frame | about 40% | about 62% |
| headroom above hair | about 11% | about 23% |
| recorded loudness / peak | -28 to -30 LUFS / -3 to -6 dBFS, 0 clipped | same |
| noise floor (voice over floor) | 35 to 56 dB (Muhammad 28 to 35) | 53 to 62 dB |
| room echo (EDT) | 59 to 64 ms (Muhammad 40; chain dereverbs above 55) | 64 to 67 ms |

## Editor warnings

- Self-Driving Car short: the Model 3 vs Camry cost lines and the look-away-from-the-road lines are Dan's
  intended ad-libs (he compares against a comparable Camry trim). Use his final takes; not a pickup.
- Robot Lawn Mower short: Dan changed the lawn-service numbers from the script ($55 a visit, $1,500 a
  year) to "$100 to $200 a visit, about $3,000 a year or more". Use his final take.
- Home Workouts short: "you're seeing it on screen right now" needs the equipment b-roll, which is not filmed.
- Glasses reflect the prompter/light (a bright rectangle in the right lens on the vertical set).
- The lav clip is visible at the tank neckline on both sets.
- Bottom-right of the 16:9 frame: a white cable coil behind the bulb. Far left edge: small red indicator lights.
