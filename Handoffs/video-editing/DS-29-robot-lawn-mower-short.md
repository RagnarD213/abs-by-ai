# DS-29: "Robot Lawn Mower (short)", first cut from raw footage

**Dedicated shorts · 9/23 shoot · BLOCKED.** Added 2026-09-24 at Dan's request. Read `00-RULES.md` first.

## Source (9/23 shoot)
Folder: `/Volumes/Extreme/dan rose fitness 9:23 shoot - vsls, long form content, short form content/`
Read `Docs/SHOOT_923_FOOTAGE_REPORT.md` first. Format: Sony FX30 4K 29.97p **S-Cinetone** (grade as Rec.709, never the 8/28 log LUT); one dual-mono lav, use `pick_lav.py`'s map. Footage is dark and soft; dereverb above 55 ms EDT per the chain. Glasses reflection and visible lav clip are known.
Scripts: teleprompter doc `1qt47J2sWcdLXIQYQ055dooKPad8cOJrFMsYhj0VWrIQ` (what Dan read) and scripts + b-roll doc `1tTPTksuG_YwifjMWohtmXpelrjTFdo8KzjfxyuVvxq4` (cues). Dan-edited long-form text: `Docs/SCRIPTS_923_SHOOT_LONGFORM_DAN_EDITED_20260921.md`.

## This video
Roll: **C1720**. Robot mower b-roll not filmed. Use Dan's final numbers ($100-$200 a visit, about $3,000 a year), not the script's.

Deliverable: 1080x1920, 45-66 s, J2 captions. No cover image (a separate Codex task, Dan 2026-09-25). **Portrait roll**: stored 3840x2160 rotation -90, decodes to 2160x3840; do not add a transpose. No alternate hook takes except Wispr Flow.

## Starter prompts
**Claude (Opus 5.5, high):**
> Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/DS-29-robot-lawn-mower-short.md`: cut "Robot Lawn Mower (short)" from 9/23 roll C1720 with /shorts. Best take of every line, every gate, independent audit, deliver, send me the review copy, update the master list.

**Codex (GPT-6 Astra, high):**
> Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table), then execute `Handoffs/video-editing/DS-29-robot-lawn-mower-short.md` with `$long-form-content-edit`. Deliver, send Dan the review copy, update `00-MASTER.md`.

## UPDATE 2026-11-17 (Dan): the mower B-roll was filmed and used, you are unblocked
Dan's real robot lawn mower footage (his Mammotion mower, shot 2026-10-22 on his iPhone) was used in the long-form "How To Make Time For Exercise & Nutrition: 6 Ways To Get 10+ Hours Back" (RO-18, approved R4 2026-10-27). Filed in the clip library (permanent IDs, never re-file), all under `/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/03 B-Roll - Real Footage/dan-filmed/`:
- **B0726** `B0726_dans-robot-mower-drives-toward-camera_16x9_5s.mp4` (4.8 s; Drive `1DnBak8bwda5TWiXbJ5R5FJovjd-AL-_C`)
- **B0727** `B0727_dans-robot-mower-close-pass-profile_16x9_4s.mp4` (4.0 s; `1FmMTKlKob3XDqINguy8hK6D7fKVdkHx8`)
- **B0728** `B0728_dans-robot-mower-with-deer-behind_16x9_4s.mp4` (4.0 s; `13tiQtk9aFo3mM6AO1KxWiuiBe38VNCHY`)
- **B0729** `B0729_dans-robot-mower-leaves-dock_16x9_5s.mp4` (5.4 s; `1mf9FicLa-TZM0nrNjt_zQLBrLfNkQtw5`; glare after about 10 s in the source)
Those are 16:9 crops. For a 9:16 short use the **portrait originals**, in `/Volumes/Expansion/_edit_work/RO-18/round3-plan/assets/`: `mower-IMG_1006-open-lawn.MOV` (best: 2160x3840, 60 fps, HLG HDR, 34.2 s, close passes 0-6 s and 16-24 s), `mower-IMG_1005-dock-exit.MOV` (29.5 s, leaves its dock 0-9 s, glare after about 10 s) and `mower-IMG_1009-landscape-main.MOV` (landscape 4K HLG, 222.5 s: close passes, mowed stripes, a deer walks past about 148-185 s). Tone-map HLG to SDR first (RO-18 recipe: `zscale=t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=hable:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p`, see `/Volumes/Expansion/_edit_work/RO-18/round3-plan/decisions.json`), then grade to sit with Dan's talking shots and check the rendered result. Real footage of his own mower, no label; the Mammotion badge is his mower, keep it. IMG_1007/1008 are not usable (mower is a speck). Use Dan's final numbers ($100-$200 a visit, about $3,000 a year), not the script's. Task name `Robot Lawn Mower SFC R1`, Claude Opus 5.5 high. State is `ready`. 9/23 batch: this edit, DS-26 and DS-32 are the three that hold the 9/23 shoot on the Extreme drive.
