# 10/15 shoot: raw footage report

Audited 2026-10-15 by Claude from the files on the drive. Every roll was indexed with `roll_sidecar.py` (lav pick,
full Whisper transcript, contact sheet), picture measured on three full-resolution frames per roll, audio measured
with `_shared/audio/common.py`, and every transcript matched line by line against the four teleprompter documents.
This is the shoot the planning docs call **the 10/17 shoot** (`Docs/SHOOT_1017_DOCS.md`); it was filmed on 10/15.

Folder: `/Volumes/Extreme/10:15 dan rose fitness shoot - green screen, outdoor shorts, outdoor b roll, studio backdrop/`

## Format

- 63 rolls, **C1721 to C1783**, 223 GB, 216.8 minutes. Copy verified against the card (sizes plus middle and tail
  checksums on every file). Sidecars (`C####.roll.md`, `.roll.json`, `.roll/`) sit beside each clip.
- Sony FX30, 3840x2160, 29.97p, XAVC 4:2:2 10-bit, **S-Cinetone** (grade as Rec.709, same as 9/23).
- **Portrait rolls** (rotation -90, decode 2160x3840, do not add a transpose): C1728 to C1730 (green screen) and
  C1755 to C1766 (pool shorts). Everything else is 16:9.
- **Audio is different from 9/23:** one stereo stream, **lav on the left channel only, right channel empty** (-90 dB).
  `pick_lav.py` verdict on every talking roll: `single-live`, `-map 0:a:0 -af pan=mono|c0=c0`. There is no backup
  mic. The B-roll rolls (C1732 to C1754) carry only the camera's own mic.
- **The lav clips.** Every talking roll tops out at exactly -0.49 dBFS with flat runs at that ceiling: about 1,800
  samples in C1756, 1,200 in C1758, 620 in C1767, 160 in C1726 (per 10 minutes). Loud, emphatic words are clipped
  for a few milliseconds each. Listen to those lines before using them; the cure is at the shoot (below).
- Camera clock is about 12 hours off again (metadata starts 2026-10-14 23:20 -06:00).
- C1731 is a 1-second accidental clip.

## Roll map

### Green screen, 16:9 (talking, waist up, black tank)

| roll | content |
|---|---|
| C1721 | Pickup test, Invest In Your Health |
| C1722 | **All 12 pickups from Teleprompter 0**: Invest In Your Health (RO-20/B/C), Top 5 Zepbound Tips (SL-06), Belly Fat 90 Days (SL-07), Why You're Not Losing Weight. Every line checked against the document. |
| C1723 | Body Fat % hook, false starts (toilet flush and a plane stop the takes) |
| C1724 | What Every Body Fat Percentage Looks Like (On Me), full |
| C1725 | How Losing Fat Changed My Face, full |
| C1726 | I Ranked Every Ab Exercise (0:00 to about 7:20), then Reacting To Celebrity Ozempic Transformations (7:25 to end) |
| C1727 | Cristiano Ronaldo ab belt, horizontal. **Superseded:** Dan says on C1729 to use the vertical take. |

### Green screen, portrait (reaction shorts; a laptop sits at the bottom edge of the frame)

| roll | content |
|---|---|
| C1728 | Ronaldo false start |
| C1729 | **Ronaldo (use this one)**, Surgeons Carve Fake Abs (1:48), Dad Bod intro (3:16) |
| C1730 (43 min) | All the reactions. Face video's Clavicular reaction pieces (0:07), Ronaldo reaction, Surgeons reaction (3:13), Dad Bod scripted (6:38) and off the cuff (7:28), Fat Shaming scripted (9:26) and off the cuff (10:33), Dr. Mike (12:03, scripted 13:05, off the cuff 13:56), Blended Oats (15:19, scripted 16:08, off the cuff 17:20), ChatGPT Coach (scripted 19:24, off the cuff 20:38), Fat 90-Year-Old (scripted 23:12, spontaneous 24:13), Kevin James (26:16, scripted 27:44, off the cuff 28:46), Post Malone (scripted 30:44, off the cuff 31:57), Terry Crews (about 33:45, off the cuff 34:48), Hormozi (scripted 37:31, off the cuff 38:38), Mr. Olympia vacuum (scripted 40:25, off the cuff 41:27) |

Most reactions have two versions: the teleprompter script and an off-the-cuff take. Dan said on the roll that the
Celebrity Ozempic video uses still images, so no reactions were recorded for it.

### Outdoor B-roll, 16:9, by the pool (no talking, shirtless, knee sleeve on the right knee)

| roll | content | B-roll list item |
|---|---|---|
| C1732 | Countertop push-ups at the outdoor kitchen | **critical**: Five Levels Of Pushups (DS-20), Pushup Masterclass |
| C1733, C1734 | All home equipment laid out on the mat (plus a medicine ball) | **critical**: Home Workouts (DS-27) |
| C1735 | Handheld close-ups of each piece (rope, dumbbells, and so on) | same |
| C1736 | M100 moves: squat thrusts, mountain climbers, squat jumps | **critical**: How To Do M100s (DS-25) |
| C1737 | Bodyweight squats | |
| C1738 | Floor push-ups, then on the knees | |
| C1739, C1742 | Jump rope | |
| C1740 | Reverse lunges | |
| C1741 | Toe touches | |
| C1743 | Kettlebell deadlifts | |
| C1744 | Push-ups on handles, then on the knees | |
| C1745 | Side laterals, including the swinging wrong rep | |
| C1746 | Dumbbell curls | |
| C1747 | Reverse crunches | |
| C1748 | V-sit twists (medicine ball), plus the heels-down version | |
| C1749 | Spiderman planks, then ab wheel rollouts from the knees | |
| C1750 | Kettlebell deadlift into goblet squats | |
| C1751 | Crunches and sit-ups | |
| C1752 | Plank | |
| C1753 | Vacuum, standing, one angle (front) | |
| C1754 | Overhead tricep extensions, seated on the pool edge | |

### Outdoor shorts, portrait, by the pool (shirtless, lav on a cord around the neck)

| roll | content |
|---|---|
| C1755 | Lower Abs, false start |
| C1756 | The Only 2 Exercises For Lower Abs, then V-Taper (2:10) |
| C1757 | 5-second false start (he grabs the jump rope) |
| C1758 | Why Jump Rope Beats The Treadmill (holding the rope), then first Coconut Water attempt (2:32) |
| C1759 | Why I Stopped Drinking Coconut Water, Why I Sleep At 63 Degrees (1:42), 3 Ways To Lose Fat Without Losing Muscle (3:26) |
| C1760 | Why Zepbound Is Actually Free |
| C1761 | End of Zepbound Free, Bigger Arms (0:59), Kettlebell first take (3:30) |
| C1762 to C1765 | Kettlebell deadlift and goblet squat retakes (C1763 is 3 s), then The 3 Exercises I'd Do If I Only Had 5 Minutes (C1765 1:23) |
| C1766 | The Only Ab Exercise That Hits All 4 Ab Muscles |

All 11 outdoor shorts are filmed.

### Studio, dark green backdrop with two cyan tubes and the desk, 16:9

| roll | content |
|---|---|
| C1767 | I'm 41. I Wasted My Life. |
| C1768 | I'm 41. My Life Is Top 1%. |
| C1769 | It's Boring, But It Got Me Abs At 40, first attempt (about 3 min) |
| C1770 | It's Boring, But It Got Me Abs At 40, full |
| C1771 | Why Zepbound Improves Your Health Even If You're Ripped |
| C1772 | Cortisol Belly Is Real, But TikTok Has It Wrong |
| C1773 | Cortisol recap retake |
| C1774 | The Fastest Way To Lose Stubborn Love Handles |
| C1775 | How To Get Rid Of Man Boobs |
| C1776 | I'm 41. Here Are The 10 Exercises I Do Every Week |

All 8 long-forms are filmed.

### Studio, same set, 16:9: shorts from the outdoor teleprompter document, filmed last

| roll | content |
|---|---|
| C1777 | Why I Train With A Timer Instead Of Counting Reps, then Commercial Break first take (1:37) |
| C1778 | 3 Exercises You Can Do In One Commercial Break, then How To Do Towel Rows (1:16) |
| C1779 | How To Do Reverse Lunges |
| C1780 | How To Do Bodyweight Squats |
| C1781 | How To Do Goblet Squats |
| C1782 | How To Do Overhead Tricep Extensions |
| C1783 | 3 Rules For Every Rep |

## Not filmed

All of it is on "Next Shoot - Filming Document (Not Filmed On 10-15)" (`1fNCxSNNDGmAn_nkNgzRJbWIUDuvmxum2LBNCpyKveVg`), and every filmed and unfilmed video has an Edit Queue job: RO-21 to RO-36, DS-33 to DS-75 (`Handoffs/video-editing/00-MASTER.md`, section 1C3).

- **Green screen reactions (6):** There's Now A Card That Tells Your Doctor Not To Weigh You and Bert Kreischer
  (Dan skipped both on the roll at 26:15), and all four Clavicular shorts (Looks Matter, 70% Of Softmaxxing,
  Retatrutide, Hair Is Life). The session moved outside after Mr. Olympia.
- **Short-form content shorts (5):** Why I Only Do 3 Sets, Why Cables Beat Dumbbells (also still needs gym cable
  B-roll), Why I Do A Total Body Workout Every Day, Why I Work Out First Thing In The Morning, Why You Must Train
  Your Abs Every Day.
- **All 4 follow-along workouts** (5, 10, 15 and 20 minutes): the demo clips exist, but none of the spoken cue tracks.
- **B-roll:** robot mower (DS-29 still blocked); towel rows (so the Towel Rows short has no demo); dumbbell side
  bends; swapping light dumbbells for heavy; the side close-up of chest depth on handle push-ups; the vacuum from the
  side; the close-ups (towel on the post, hips curling, elbows up); beginner chair squat and wall lunge; one equipment
  layout per workout. Props were not in hand during the talking takes: coconut water and electrolyte powder, the
  vial, the Gymboss. (The jump rope was.) Gym and home B-roll are not on this card.

## Measurements

| | green screen 16:9 | green screen portrait | pool shorts | pool B-roll | studio |
|---|---|---|---|---|---|
| median luma (face) | 0.43 (0.50) | 0.42 (0.47) | 0.27 (0.40 to 0.50) | 0.16 to 0.35 | 0.24 (0.30) |
| backdrop luma | 0.43 left to 0.55 right | 0.45 to 0.50 | 0.18 (hedge) | | 0.24 |
| clipped pixels | 0 | 0 | 0 on the face | 0 | 0.7% (the tubes) |
| Dan's width in frame | 31 to 34% | 71 to 86% | 75 to 87% | 13 to 33% | 28 to 32% |
| headroom above hair | 7 to 9% | 19 to 25% | 9 to 10% | | 5 to 7% |
| loudness | -23 to -25 LUFS | -24 to -26 | -19 to -26 | (camera mic) | -22 to -27 |
| voice over floor | 33 to 36 dB | 35 to 37 | 31 to 42 | | 34 to 49 |
| room echo (EDT) | 53 to 72 ms | 56 to 57 | **32 to 45 ms** | | 56 to 79 ms |

Against 9/23: the studio is 50% brighter (0.24 against 0.16) and the face now stands out from the backdrop (0.30
against 0.24; 9/23 measured no separation). Recording level is 4 to 6 dB hotter (-24 against -28 to -30 LUFS).
The pool audio is the driest Dan has recorded (Muhammad's reference is 40 ms).

Speaking pace with pauses included: green screen 170 to 178 words a minute, studio 165 to 206 (C1767 195, C1768
206). Recorded words against script words: 1.17x (Cortisol) to 1.53x (Zepbound Health), about 1.33x overall.

## Editor warnings

- **Use C1729 for Ronaldo, not C1727** (Dan, on the roll).
- **Pickups were recorded on the green screen**, not on the studio set the 10-13 pickup rule names. Same lav, so the
  sound should sit much closer to the films than the rejected desk mic did; cover the picture as before, or key it.
- **Studio shorts were shot 16:9.** The approved crop default for this set (`Docs/STUDIO_BLUE_LIGHT_CROP_DEFAULT.md`)
  has a wide view that shows both tube lights. A 9:16 crop of a 16:9 frame is 1215 px wide and the tubes are about
  2,900 px apart, so C1777 to C1783 can only get a medium crop on Dan, never that wide view. Same for any Shorts cut
  from the studio long-forms.
- **Portrait green screen:** the laptop edge is in the bottom of the frame on C1730; crop above it. Dan reads the
  clips off the laptop, so his eyes drop below the lens during the watching parts.
- **The 16:9 green screen falls off left to right** (0.43 to 0.55) with creases low in the frame; key with a garbage
  matte, check the left edge.
- **Lav on a cord on Dan's bare chest** in every pool short (C1755 to C1766), dead centre of the frame.
- **Studio glasses:** both lenses carry a blue-white reflection on every studio roll.
- **Pool B-roll is dark and dappled** (tree shadows across the mat, harsh sun on the concrete). C1742 and C1743
  measure 0.16 to 0.18. Grade every clip before it goes in (B-roll colour rule, 10-11).
- Noise stopped takes: toilet flush and a plane (C1723), an aircraft on the pool rolls (C1764, C1765), something
  audible in the studio at C1777 2:00. Check the end of each kept take.
