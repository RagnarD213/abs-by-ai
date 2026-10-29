**LFC.** Task name: `Body Fat % LFC R1`.

# RO-21: "What Every Body Fat Percentage Looks Like (On Me)", first cut from raw footage

**Organic long-form · 10/15 shoot · READY.** Added 2026-10-16 at Dan's request. Read `00-RULES.md` first.

## Source (10/15 shoot, called the 10/17 shoot in the planning docs)
Folder: `/Volumes/Extreme/10:15 dan rose fitness shoot - green screen, outdoor shorts, outdoor b roll, studio backdrop/`
Read `Docs/SHOOT_1015_FOOTAGE_REPORT.md` first (roll map, measurements, editor warnings). Format: Sony FX30 4K 29.97p **S-Cinetone** (grade as Rec.709). The lav is on the **left channel only**; use `pick_lav.py`'s map. **The lav flat-tops at -0.49 dBFS on loud words**: listen to emphatic lines and prefer a clean take. Every roll has a sidecar beside it (`roll_sidecar.py show`): full transcript, takes, contact sheet.
Scripts: the editing copy with every cue is the shoot doc `1gt8Fi_wUaNaksa8sAdMoBvcdlBhZLek82EpBr-leq-0`; what Dan read is Teleprompter 2 - Green Screen `1KvL0_IilRCxlofnY5luTfRvjiseGGpGGXU4sAsjbgzQ`.

## This video
Rolls: **C1724 (hook false starts C1723)**.
Set: Green screen, 16:9. Key it; the screen falls off left to right (0.43 to 0.55) with creases low in the frame, so use a garbage matte.
Deliverable: 16:9 long-form, 1920x1080 or 4K per /longform-edit; round method (graphics, AI frames and first minute approved before the full render). Shorts come later from the approved film (`/shorts`), nothing else.

- B-roll on this shoot: the pool demos and equipment (C1732 to C1754, listed in the report). Clip library first for anything else.
- B-roll not filmed yet: cable crunches and leg raises (gym), 3 or 4 heavy sets (gym), meal prep, salmon, sardines and eggs (kitchen), stepping on the scale.

## Starter prompts
**Claude (Opus 5.5, high):**
> Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/RO-21-what-every-body-fat-percentage-looks-like-on-me.md`: cut "What Every Body Fat Percentage Looks Like (On Me)" from 10/15 roll C1723-C1724 with /longform-edit. Best take of every line, every gate, independent audit, deliver, send me the review copy, update the master list.

**Codex (GPT-6 Sol, high):**
> Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table), then execute `Handoffs/video-editing/RO-21-what-every-body-fat-percentage-looks-like-on-me.md` with `$long-form-content-edit`. Deliver, send Dan the review copy, update `00-MASTER.md`.

## Release plan (Dan approved 2026-10-28)
- **Release:** Wed Dec 30, 2026 (January blitz, Sat Dec 26 to Jan 31), 9 AM America/Chicago on YouTube; dated calendar `Docs/LONGFORM_RELEASE_CALENDAR.md`.
- **Edit deadline:** Name a finish date by Dec 11; finished, approved and set up by Dec 18 (first 14 blitz days).
- **Footage:** Green screen: house chroma key plus the locked long-form green-screen background template. Not kitchen footage. Fallback if it misses: the strongest ready non-kitchen film.
- **Model:** Claude Opus 5.5, high effort, or Codex `gpt-6.1-sol`, high effort (the newest Sol; ignore older "GPT-6 Sol" wording in the prompts above). A video stays with the AI it starts on.
- **Edit cap:** run `python3 .claude/skills/_shared/editcap/editcap.py acquire <JOB>` before the first render; at most 5 edits at once.
