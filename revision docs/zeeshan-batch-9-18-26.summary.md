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
- 8:10–8:16.5 the "rear delt fly" clip is a bent-over ROW — the exact mistake he warns about 8 s later.

---

## For Dan

- **Confirm the round numbers before forwarding.** I read "Video 2 Rev 3" as round 4 of the arms & shoulders video (rounds 1/2/3 were 09-14, 09-15, 09-17) and "Video 3" as round 1 of STOP Deadlifting, his first delivery of it.
- **The "footage of me at the gym" problem is really your call.** There is no footage of you doing T-bar rows, lat pulldowns, leg presses or rear delt flys anywhere on the drives — the 8/3, 8/14 and 8/28 shoots are home and outdoor only. The doc tells him to trim the promise out of the line. The alternatives are to film that footage, or to use the AI-Dan demo clips we already have (`lat-pulldown`, `leg-press`, `seated-cable-row`, `db-row` are in `Media/exercise-demos/` and live at absbyai.com/exercise-demos/) with AI labels — I did not put that in the doc because they are AI and the line says "actually".
- **0:10 – 0:20 is a free old-channel proof beat.** You say "our first video to go viral with six-pack shortcuts was a video of me deadlifting back in the day" over nothing. Your standing rule wants that shown as the old video playing inside the full YouTube page with the channel name, subscriber count and views legible. We do not have that screen capture yet. Say the word and I will make one and add it as an item.
- **The talking-section music in BOTH videos is unidentified.** He only ever sends the gym track. Until he names them I cannot clear either video for Content ID.
- The stock exercise models are all men in their early twenties. I did not itemise it (they are illustrative, not identification shots), but if you want the demos cast at 30–50 like the rest of the brand, say so and I will add one THROUGHOUT line.

---

## Paste-ready Upwork message

Hey Zeeshan, thanks for both of these.

Video 2 is basically done — the black at the end is gone and everything else is exactly where I left it. Two things left and neither one is editing: I need the name of the track that's now under the talking sections (the gym track you sent is the live-round one, and that one's clean, I checked it), and the subtitle file in the folder is the deadlift video's, not this one's. Send me the arms and shoulders .srt with "GymBoss" fixed to "Gymboss" and video 2 is finished.

The deadlift video is a good first cut. The framing is right the whole way through, the colour is even, and the audio is right — no notes on any of that. Round 1 is at the top of the same doc: https://docs.google.com/document/d/13uu4k9y2ttOWD9sp3KU-OLAeCNO74-3pWeIrBjcgVhk/edit

The big ones: there's a four-minute stretch from 0:55 to 5:05 with no picture except me talking, so I need two or three inserts in there. A few of the exercise clips don't show the exercise I'm describing — the leg press one is a still close-up of a weight plate, and the rear delt one is a row, which is the exact thing I tell people not to do. And there's a list of words to fix in the graphics; the one that matters most is "AI Personal Traniner" at 9:14, which is my own product misspelled right where I'm sending people to the site. Send me the name of the music track on this one too, and the .srt with the next export.
