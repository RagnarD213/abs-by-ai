# RO-15: "Sleep Better With Glycine", first cut from raw footage

**Organic long-form · 9/23 shoot · READY.** Added 2026-09-24 at Dan's request. Read `00-RULES.md` first.

## Source (9/23 shoot)
Folder: `/Volumes/Extreme/dan rose fitness 9:23 shoot - vsls, long form content, short form content/`
Read `Docs/SHOOT_923_FOOTAGE_REPORT.md` first. Format: Sony FX30 4K 29.97p **S-Cinetone** (grade as Rec.709, never the 8/28 log LUT); one dual-mono lav, use `pick_lav.py`'s map. Footage is dark and soft; dereverb above 55 ms EDT per the chain. Glasses reflection and visible lav clip are known.
Scripts: teleprompter doc `1qt47J2sWcdLXIQYQ055dooKPad8cOJrFMsYhj0VWrIQ` (what Dan read) and scripts + b-roll doc `1tTPTksuG_YwifjMWohtmXpelrjTFdo8KzjfxyuVvxq4` (cues). Dan-edited long-form text: `Docs/SCRIPTS_923_SHOOT_LONGFORM_DAN_EDITED_20260921.md`.

## This video
Roll: **C1709**. 

Deliverable: 16:9 master + SRT to the approved organic standard (Zeeshan's ab wheel videos; C1652 R4 bar). `[FILM]` b-roll cues and cold opens were not filmed: fill from archive/stock, never fake Dan.

## Starter prompts
**Claude (Opus 5.5, high):**
> Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/RO-15-sleep-better-with-glycine.md`: cut "Sleep Better With Glycine" from 9/23 roll C1709 with /longform-edit. Best take of every line, every gate, independent audit, deliver, send me the review copy, update the master list.

**Codex (GPT-6 Astra, high):**
> Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table), then execute `Handoffs/video-editing/RO-15-sleep-better-with-glycine.md` with `$long-form-content-edit`. Deliver, send Dan the review copy, update `00-MASTER.md`.

## Release plan (Dan approved 2026-10-28; slot assigned 2026-10-29)
- **Release:** Wed Dec 23, 2026 (phase 2 spare slot; a sleep topic suits the holiday low point); dated calendars `Docs/LONGFORM_RELEASE_CALENDAR.md` and `Docs/SHORTS_RELEASE_CALENDAR.md`.
- **Edit deadline:** Name a finish date by Dec 4; edited and approved by Dec 16, else the slot becomes a two-Short day and the film moves to a phase 4 Sunday.
- **Footage:** Tube-light studio (Sept 23), not kitchen.
- **Model:** Claude Opus 5.5, high effort, or Codex `gpt-6.1-sol`, high effort (the newest Sol; ignore older "GPT-6 Sol" wording in the prompts above). A video stays with the AI it starts on.
- **Edit cap:** run `python3 .claude/skills/_shared/editcap/editcap.py acquire <JOB>` before the first render; at most 5 edits at once.
