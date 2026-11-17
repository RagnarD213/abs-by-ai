# DS-26: "Wispr Flow (short)", first cut from raw footage

**Dedicated shorts · 9/23 shoot · BLOCKED.** Added 2026-09-24 at Dan's request. Read `00-RULES.md` first.

## Source (9/23 shoot)
Folder: `/Volumes/Extreme/dan rose fitness 9:23 shoot - vsls, long form content, short form content/`
Read `Docs/SHOOT_923_FOOTAGE_REPORT.md` first. Format: Sony FX30 4K 29.97p **S-Cinetone** (grade as Rec.709, never the 8/28 log LUT); one dual-mono lav, use `pick_lav.py`'s map. Footage is dark and soft; dereverb above 55 ms EDT per the chain. Glasses reflection and visible lav clip are known.
Scripts: teleprompter doc `1qt47J2sWcdLXIQYQ055dooKPad8cOJrFMsYhj0VWrIQ` (what Dan read) and scripts + b-roll doc `1tTPTksuG_YwifjMWohtmXpelrjTFdo8KzjfxyuVvxq4` (cues). Dan-edited long-form text: `Docs/SCRIPTS_923_SHOOT_LONGFORM_DAN_EDITED_20260921.md`.

## This video
Roll: **C1719**. Alternate hooks on the roll. Needs the Wispr Flow ScreenFlow demo, which Dan still has to upload.

Deliverable: 1080x1920, 45-66 s, J2 captions. No cover image (a separate Codex task, Dan 2026-09-25). **Portrait roll**: stored 3840x2160 rotation -90, decodes to 2160x3840; do not add a transpose. No alternate hook takes except Wispr Flow.

## Starter prompts
**Claude (Opus 5.5, high):**
> Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/DS-26-wispr-flow-short.md`: cut "Wispr Flow (short)" from 9/23 roll C1719 with /shorts. Best take of every line, every gate, independent audit, deliver, send me the review copy, update the master list.

**Codex (GPT-6 Astra, high):**
> Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table), then execute `Handoffs/video-editing/DS-26-wispr-flow-short.md` with `$long-form-content-edit`. Deliver, send Dan the review copy, update `00-MASTER.md`.

## UPDATE 2026-11-17 (Dan): the demo footage already exists, you are unblocked
Dan: the Wispr Flow demo was used in the long-form "How To Make Time For Exercise & Nutrition: 6 Ways To Get 10+ Hours Back" (RO-18, 9/23 shoot, approved R4 2026-10-27). Both pieces are filed in the clip library (permanent IDs, never re-file):
- **B0730**: the Wispr Flow screen recording, iPhone 1320x2868, 60 fps, 44.6 s, no audio: ChatGPT open, the Wispr keyboard, tap the mic, the "Listening" waveform, then "I need you to make me a restaurant reservation at 7 pm." lands in the box. File: `/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/03 B-Roll - Real Footage/screen-recordings/B0730_wispr-flow-dictation-into-chatgpt-iphone_1320x2868_45s.mp4` (Drive id `1gbmpzoClNHL4bkKJZ8zTMlhMiLnZCnh0`, 23,644,718 bytes). Original: `/Volumes/Expansion/_edit_work/RO-18/round3-plan/assets/wispr-flow-screen-recording-20260923.mp4`. **Crop the top 190 px** (iPhone status bar and red recording dot). Real screen recording of Dan's phone, no label.
- **B0731**: Dan dictating to the phone, the C1719 take, 9x16, 14.6 s: `.../03 B-Roll - Real Footage/dan-filmed/B0731_dan-dictates-to-phone-wispr-flow-vertical-set_9x16_15s.mp4` (Drive id `1KBkqyNd5vMWbMJIDzHZwcnXvuj-mw3bG`). The recording is time-synced to the camera roll: **recording time = C1719 time minus 94.8 s**. That mic sounds thinner and brighter than the studio rolls: RO-18 used a corrective EQ (`/Volumes/Expansion/_edit_work/RO-18/round4/fit/c1719_eq.json`) and -4.3 dB; start from it.
- How RO-18 used them (placement, phone card, cut pieces, crop): `/Volumes/Expansion/_edit_work/RO-18/round3-plan/decisions.json` item 2 and `/Volumes/Expansion/_edit_work/RO-18/round4/NOTES-R4.md`. The ScreenFlow demo in the 9/23 report (started at C1719 1:14) is the same one. 
The short itself is still cut from the full C1719 roll (alternate hooks on it), 45-66 s, 1080x1920; put the demo in the frame as the proof beat on the line about installing Wispr Flow and talking instead of typing. Task name `Wispr Flow SFC R1`, Claude Opus 5.5 high. State is `ready`. 9/23 batch: this edit, DS-29 and DS-32 are the three that hold the 9/23 shoot on the Extreme drive.
