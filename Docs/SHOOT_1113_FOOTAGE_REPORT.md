# 11/13 shoot: raw footage report (cards 1 and 2)

Offloaded and sorted 2026-11-13 by Claude. Green screen, Dan in a white tank. This covers the first card only;
the shoot was still going when it was offloaded.

## Where the files are

- Shoot folder: `/Volumes/Extreme/11:13 dan rose fitness shoot - green screen/` (the nightly backup finds it by name).
- While the Extreme was full, C1904 to C1914 were copied straight from the card to
  `/Volumes/Expansion/Abs By AI Raw Footage/11:13 dan rose fitness shoot - green screen/`, then copied back to
  the Extreme folder; all 14 rolls were on the Extreme by 20:05 on Nov 13. Every file was checked by SHA-256 against the bytes read from the card
  (Seagate copy re-read, Extreme copy re-read). Card left unformatted.
- C1900 (Nov 3, a laptop video call, not this shoot) is filed in `not this shoot - C1900 laptop video call 11-03/`
  on the Seagate copy only.
- Roll sidecars (transcript, mic pick, contact sheet) are building overnight through the render queue. C1903 is built
  from the Extreme copy; the others were queued from their Seagate copies (the sidecar's content key still finds them
  after they move).

## Format

- Sony FX30, 3840x2160, 29.97p, XAVC 4:2:2 (AVC 140), S-Cinetone / Rec.709. Grade as Rec.709, no log LUT.
- Audio: one stereo LPCM stream. Run `pick_lav.py` (or read the sidecar) before cutting.
- **C1901 to C1909 are portrait** (stored 3840x2160 with rotation -90, decode to 2160x3840, add no transpose).
  **C1910 to C1914 are landscape.**
- Camera clock is about 12 hours off, as on 9/23: metadata says Nov 12 22:23 to Nov 13 04:14 at -06:00.
- 14 rolls from this shoot, 227 GB, about 221 minutes.

## Roll map

Times are minutes:seconds into the roll, from an audio pass (Gemini 3.8 Flash on each roll's audio). They are close
but not frame-accurate; use the sidecar's word timings for cuts.

| roll | orient. | length | content |
|---|---|---|---|
| C1901, C1902 | portrait | 0:02, 0:12 | setup and framing |
| C1903 | portrait | 45:18 | **Great Again T VSL**, full read with many retakes and pickups across the whole roll |
| C1904 | portrait | 54:49 | **GAT upsells**: 1 Prepaid Packs 0:00-13:45, 2 Eternal Burn AM/PM 13:45-30:31, 3 Electro-Creatine 31:18-44:43, 4 Abs By AI 44:43-54:50 |
| C1905 | portrait | 13:14 | **L01** 0:00-8:38, **L02** 8:38-13:07, then Dan notices they should have been horizontal (both reshot landscape in C1913) |
| C1906 | portrait | 22:34 | Short ads: **S01** 0:23-3:07, **S02** 3:07-5:25, **S03** 5:25-7:47, **S04** 7:47-10:20, **S05** 10:20-13:48, **S11** 14:29-17:00, **S13** 17:00-19:23, **S21** 20:09-22:22 |
| C1907 | portrait | 0:26 | Short "The Best Protein Snack Costs $2 and Comes in a Can" (B05): first line only, stops to grab sardines |
| C1908 | portrait | 4:19 | Short "Here's Why Sardines Beat Protein Bars" (complete) 0:00-1:21; **B08** "Your Metabolism Is Not The Reason You're Fat" 1:21-4:12 |
| C1909 | portrait | 7:47 | Reactions: watches Mike Michalowicz smaller-plates clip 0:00-0:46; scripted "A Money Expert Says The Fix For Your Weight Is Smaller Plates. He's Right." 0:46-1:56; off-the-cuff reaction 1:56-3:26; watches Alex Hormozi clip 3:26-4:27; scripted **C01** "You're Not Hungry, You're Bored" 4:27-6:06; off-the-cuff reaction 6:06-7:48 |
| C1910 | landscape | 0:28 | **L03** hook only, aborted |
| C1911 | landscape | 29:29 | **L01** 0:06-4:39 (unannounced), **L04** 4:39-9:07, **L05** 9:08-14:47, **L07** 14:48-20:18, **L17** 20:19-23:09, **L20** 23:10-28:47, L22 start 28:48 (setup talk) |
| C1912 | landscape | 12:23 | **L22** 0:12-6:30 (many hook restarts, alternate CTAs), **L23** 7:08-12:17 (complete take about 7:46-11:48) |
| C1913 | landscape | 17:48 | **L30** 0:00-5:03, **L01** 5:03-12:40 (horizontal reshoot Dan called the keeper), **L02** 12:40-17:48 |
| C1914 | landscape | 12:26 | **"I Crashed My Tesla Because I Didn't Trust FSD"** complete, 0:00-7:09; **A15** "I'm 41. If I Were 25 Again..." 7:10-12:28, hook restarts, cut off mid-take |

## By video

- **Ads, Great Again T (AD):** VSL (C1903, portrait); upsells 1 to 4 (C1904, portrait); long ads L01 (C1913 keeper,
  also C1911 and portrait C1905), L02 (C1913, also portrait C1905), L03 (aborted hook only, C1910), L04, L05, L07, L17,
  L20 (C1911), L22, L23 (C1912), L30 (C1913); short ads S01, S02, S03, S04, S05, S11, S13, S21 (C1906, portrait).
- **Not on this card:** L18 (not set up yet), and a complete L03.
- **Content:** Shorts "Here's Why Sardines Beat Protein Bars" and B08 Metabolism (C1908); B05 protein snack started
  only (C1907); reaction Shorts smaller plates and C01 Hormozi with off-the-cuff alternates (C1909); long-forms Tesla
  crash (C1914, complete) and A15 (C1914, partial).

## Orientation check

- The VSL (C1903) and the four upsells (C1904) were filmed portrait, before the "should be horizontal" moment in C1905.
  That matches the approved funnel plan (`Docs/GREAT_AGAIN_T_FUNNEL_PLAN_20261110.md`): the VSL is delivered as a native
  9:16 phone video (V Shred model), and the upsells play inside the same phone funnel. Only the YouTube ads needed
  landscape, which is why L01 and L02 were reshot. No reshoot needed for the VSL or upsells.

## Card 2 (offloaded 2026-11-14)

- One roll, **C1915**, landscape, 34:29, 37.85 GB. Copied in one read to the Extreme shoot folder and the Seagate copy; both match the card's SHA-256 (`85e29a9d8c900de67a88a19d032a8b50a1c2373e854da17a098ec5155c4526c6`). Card left unformatted.
- Content (Gemini 3.8 Flash audio pass, close but not frame-accurate): 0:19-3:55 **A15 pickup** that finishes the "I'm 41. If I Were 25 Again" video started in C1914; 4:37-15:55 **A16** "I Ranked 15 Healthy Foods" (acai pronunciation chat about 7:15-8:12); 16:31-25:05 **A17** "Why Bulking Is a Scam"; 25:26-34:29 **A18** "7 Fitness Rules That Are Completely Made Up".

## Card 1 state on 2026-11-14

When card 1 was put back in the reader, C1904 read as 4,162,322,432 bytes on the card itself (it was 60,130,907,491 when copied). The Extreme and Seagate copies were re-hashed and still match the hash taken from the card on 11/13 (`64c3920a...e8916`). Treat card 1 as damaged: not a backup, do not record on it. Google Drive had 13 of 14 rolls; C1914 was uploading and a full Extreme-vs-Drive check was started.

## Edit Queue (added 2026-11-14)

All filmed videos are on the Abs By AI Edit Queue, master-list section 1C5: Great Again T VSL WV-03 and upsells WV-04 to WV-07; Great Again T ads RA-17 to RA-35 (L03 is blocked: hook only); long-forms RO-39 Tesla, RO-40 A15, RO-41 A16, RO-42 A17, RO-43 A18; Shorts DS-106 (B05, filmed as "Here's Why Sardines Beat Protein Bars", needs Dan's title call), DS-107 B08, DS-108 B06 smaller plates, DS-109 C01 Hormozi.
