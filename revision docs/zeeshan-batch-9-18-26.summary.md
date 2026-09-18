# Zeeshan, 2026-09-18 — two deliveries reviewed

Doc (both sections pasted at the TOP, old text byte-intact, verified by text export 67,097 → 78,111 bytes):
https://docs.google.com/document/d/13uu4k9y2ttOWD9sp3KU-OLAeCNO74-3pWeIrBjcgVhk/edit

Work dir: `/Volumes/Extreme/_edit_work/revisions-20260918/`

---

## 1. Arms & shoulders (his "Video 2 Rev 3") — ROUND 4 — essentially final

File: "Video2 Rev 3.mp4", 858 MB, 11:00.1, 1920x1080 @ 29.97, 10.4 Mbps.
Folder: https://drive.google.com/drive/folders/1W-hYEPL_ATzMFE9tb8c6tRGknlwOIqbH

**Measurements**
- Frame-diff vs Rev 2: the ONLY changed region in the whole file is 11:00.0 – 11:26.5. The 27 s black tail is gone; nothing else in the picture moved.
- Audio: −14.40 LUFS, true peak −1.10 dBTP, one mic (L/R +0.999 at lag 0), EDT 37 ms, 0 clipped samples. Live-round effort 16.2 dB under the talking (OK). Round ≥ 2 → not itemised.
- **Live-round music identified: "Energy Gym Thunder" (knox-gym), Pixabay 538872.** Envelope correlation r = +0.941 at 8:25–9:45, offset consistent to 1.5 s. Its Pixabay page does NOT say "Content ID Registered" → clear. **This closes the open question on the board.**
- Talking bed: the old Content-ID track ("Energetic Action Sport", AlexGrohl) no longer correlates (r ≈ 0.09, baseline) — he DID change it. But it is not the trip-hop track we linked either (r ≈ 0.12–0.16, no consistent offset), and a bed is definitely still present (gap floor −37 to −40 dB vs our raw ≈ −53 dB). Unidentified.
- Framing still reads LOOSE (full-body wides) — unchanged since a cut Dan reviewed, so it is his call, not a new item (skill rule 42).

**Items (2, neither is editing work)**
1. Name the track now under the talking sections (or send the file).
2. The .srt in the folder is the WRONG video's — byte-identical to the deadlift .srt ("Stop doing deadlifts…"). Send the arms & shoulders one with "GymBoss" → "Gymboss" at 8:09 and 8:14.

---

## 2. STOP Deadlifting (his "Video 3") — ROUND 1

File: "Video 3.mp4", 746 MB, 9:30.6, 1920x1080 @ 29.97, 10.5 Mbps. Raw source: 7/8 rolls C1487 + C1488.
Folder: https://drive.google.com/drive/folders/1KSgdrBmiX8REMqJ47tg7naAfTXc25bJn

**Measurements**
- Audio: −13.90 LUFS, −1.10 dBTP, one mic, EDT 77 ms (under the 80 ms bound), 0 clipped. Gate's tone/floor rows graded through the music bed — not quoted. No audio item.
- **Framing: every camera shot OK.** `framing.py`: 0 loose camera shots, small margin above his hair throughout, no full-body wides. The two LOOSE rows are the stock still-man at 5:11 and the full-body goal image at 8:59. Credited, no crop item.
- Luma 85–92 across all talking, 97–99 on B-roll. No grade jumps. No dead air.
- AI-artifact pass on the one labelled AI clip (barbell row, 6:33.5–6:38, 28 consecutive frames + plate and face crops at full res): plate reads "20 KG" in every readable frame, face consistent across the shot. **Clean — no artifact item.** (My first read of a "30 KG" plate was wrong; killed by the two-frame test.)
- Goal image 8:59–9:03 carries "*AI Generated", full duration, clear of face and abs.
- Music bed present the whole video, unidentified (not the knox track — r ≈ 0.06 everywhere).

**Items**
- THROUGHOUT: 4:10 with no picture but him talking (0:55 → 5:05), ask for 2–3 inserts at two named beats · 16 word/spelling fixes in the chips · name the music track · chip size and position inconsistent.
- The 16 text fixes include **"AI Personal Traniner" at 9:14.5** (product name misspelled in the CTA), "Higher Odds Of Quiting", "Exercise#1: T-Bar Row1", "Deadlift Build Thick Physique", "Aesthetic  Problem" (double space), "Bar Bell Row".
- 5:11–5:16.5 the "fitness model physique" shot is a skinny kid with no abs → recast.
- **6:07.5–6:17.8 he says "footage of me doing these exercises at the gym" and every exercise clip is a stranger.** Recommended fix: cut 6:12.9 → 6:17.8 (word timings from Whisper) so the line stops promising it.
- 6:28.5–6:33 "T-Bar Row" chip over a talking head, no T-bar footage at all.
- 6:33.5–6:38 Gymshark logo legible on the AI clip's shirt → regenerate plain.
- 7:23.5 chip "Deadlifts Better To Build Leg Muscles" contradicts the video.
- 7:33.5–7:42.5 the "leg press" clip is 9 s of a static macro of a weight plate — no leg press in it.

---

## For Dan

- **Confirm the round numbers before forwarding.** I read "Video 2 Rev 3" as round 4 of the arms & shoulders video (rounds 1/2/3 were 09-14, 09-15, 09-17) and "Video 3" as round 1 of STOP Deadlifting, his first delivery of it.
- **The "footage of me at the gym" problem is really your call.** There is no footage of you doing T-bar rows, lat pulldowns, leg presses or rear delt flys anywhere on the drives — the 8/3, 8/14 and 8/28 shoots are home and outdoor only. The doc tells him to trim the promise out of the line. The alternatives are to film that footage, or to use the AI-Dan demo clips we already have (`lat-pulldown`, `leg-press`, `seated-cable-row`, `db-row` are in `Media/exercise-demos/` and live at absbyai.com/exercise-demos/) with AI labels — I did not put that in the doc because they are AI and the line says "actually".
- **0:10 – 0:20 is a free old-channel proof beat.** You say "our first video to go viral with six-pack shortcuts was a video of me deadlifting back in the day" over nothing. Your standing rule wants that shown as the old video playing inside the full YouTube page with the channel name, subscriber count and views legible. We do not have that screen capture yet. Say the word and I will make one and add it as an item.
- **The talking-section music in BOTH videos is unidentified.** He only ever sends the gym track. Until he names them I cannot clear either video for Content ID.
- The stock exercise models are all men in their early twenties. I did not itemise it (they are illustrative, not identification shots), but if you want the demos cast at 30–50 like the rest of the brand, say so and I will add one THROUGHOUT line.

---

## Upwork message to Zeeshan (DAN'S OWN FINAL VERSION, sent)

This is the version Dan edited and approved. Copy this shape next time: warm praise, big picture only, no rival
editor named, no em dashes, no nitpicks.

Hey Zeeshan, thanks for both of these.

Video 2 is basically finished. The black at the end is gone and nothing else in the picture moved. Two things left and neither is editing work. The gym track you sent is clean, not Content ID registered, so leave the live round alone. But that isn't the track under the talking sections, there's a second one in there, so send me that name too. And the .srt in the folder is the deadlift video's, so I still need the arms and shoulders one with "GymBoss" fixed to "Gymboss".

The deadlift video is a real good first cut! Pacing is right, no dead air, and the AI barbell row clip holds up. I went through that one frame by frame. Round 1 is at the top of the same doc: https://docs.google.com/document/d/13uu4k9y2ttOWD9sp3KU-OLAeCNO74-3pWeIrBjcgVhk/edit

Three big things.

Colour. I put your export next to the camera file and next to my primary editor's ad. Your blacks sit at 22 out of 255, his sit at 2. That's why it reads milky and why I don't separate from the fridge behind me, which you've also blown out. My skin tone is right, don't touch it. It's the black point and the brightness lift that need to come back down.

The text graphics, and this is the one I care most about going forward. Most of them just repeat the words I'm saying while I'm saying them, and that adds nothing, because the viewer already heard me. I want them to distill the point for the guy who didn't follow the explanation. The format is "KEY POINT:" and then the actual takeaway. I've written every one of them out in the doc. Where two or three chips say the same thing three ways, that becomes one. Use this format on every video from now on.

And there's four minutes from 0:55 to 5:05 with nothing on screen but me talking. I need two or three inserts in there.

The rest is in the doc.

Send the music names and the .srt with the next export. Thanks!

### What Dan changed from the draft, and why

- "a good first cut." became **"a real good first cut!"**, and he added **"Thanks!"** to the sign-off. Be warmer and
  more enthusiastic when the editor has done something well.
- "next to Muhammad's ad" became **"next to my primary editor's ad"**. Zeeshan does not know who Muhammad is. Never
  name one editor to another, in the message or in the doc.
- He deleted the "AI Personal Traniner" callout and the whole paragraph about the archive clip. *"The message is really
  only for the big-picture things that we need to communicate, not the tiny tactical things."* Both are in the doc.

## Final state, 2026-09-18 (after Dan's review)

- **Framing credit was WRONG and is retracted in the doc.** `revisions/reference/framing.py` reads "top 0%" as OK; the
  delivery gate reads hair-top **median 0 px, p95 15, 74 % of frames at 0** against a 20 px floor. The raw reads the same
  (head height 408 px vs the cut's 401) — the camera was framed with no headroom, the editor barely cropped, and there is
  nothing to recover. Skill lessons 57-58.
- **Colour item added with numbers:** black point 22 vs the raw's 15 and Muhammad Ad 1's 2; median 51 → 82; clipping
  0.00 % → 1.30 %; but the face matches Muhammad (81.6 / +37.0 / 36.1 % vs 74.3 / +34.7 / 34.1 %). Regrade proof built
  and sent (still 3-up + 10 s moving). Skill lesson 59.
- **All text graphics rewritten to Dan's KEY POINT format** — 15 key points replacing ~20 echo chips; the typo fixes that
  died with their chips were removed; 7 survive. The rule is now in `_shared/VIDEO-RULES.md` and binds every video.
- **0:10 - 0:20 now carries 6 s of Dan deadlifting in the 2010 SixPackShortcuts video** (`-UJHNZHbhiw`, 4:35.5-4:41.5),
  uploaded to Drive `1t2lXssrgCjv47Ow_1E7bSj32clP5M0uh`. 360p is the ceiling (480p exists, every DASH format 403s).
- **Music item restored, specific:** "Energy Gym Thunder" is confirmed clean and is the live-round bed (r = +0.941 at
  8:25-9:45); a different, unidentified bed runs 0:00-8:19 and 9:55-end in the arms video and under the whole deadlift
  video. Skill lesson 62.
- **The 8:10 rear-delt item was wrong and stays deleted.** Dan: *"This is actually a rear delt fly... just done in the
  unconventional way."* Skill lesson 61.
