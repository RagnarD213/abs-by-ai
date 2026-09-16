# RO-02 — "The Vacuum: The Best Ab Exercise For Belly Fat": organic first cut from raw footage

**List 1 · organic long-form · READY.** Read `00-RULES.md` first.

## Source
8/14 shoot (`/Volumes/Extreme/abs by ai 8:14 shoot | teleprompter ads, indoor talking content, outdoor workout content | jeff chagrin | dan rose/`): **C1614–C1629** (16 clips, 0:19–3:02 each, about 26:30 raw). C1614 opens *"The vacuum, the best ab exercise for people with belly fat, video number one."* C1629 is the outro. **C1625 is the live set**, which is also RO-03's source. C1615 (0:19) and C1627 (0:40) are unchecked, possibly false starts.

**Script:** Shoot 4 outlines doc, Drive `1uDAWvxoAjXUaawZctgdSDj_9JPa5mfk5MMM2Sh8L7yE`.

## Build: an organic first cut (16:9 long-form)
* **The standard is the finished organic videos Dan approved**, not our older Claude long-forms: Zeeshan's
  `Zeeshan Content Videos/the 17 dollar ab wheel beats every crunch - video 1/` and `ab wheel workout - video 1/`, and the
  Codex trial's frozen organic recipe (`Media/codex-video-trial/05-recipes/`, `templates/`). Airtight pacing, best take of
  every line, zoom cuts on word onsets, B-roll/graphics wherever the script calls for them, music bed under the voice, J2 graphics.
* **Read the full raw first.** Transcribe every roll (Whisper, local, $0; one build under the two-build cap). Map the takes
  against the script and pick the best take on delivery, not simply the last or the slated take. Remove slates, resets and
  crew chatter.
* **Audio:** `pick_lav.py` per file, `voice_chain.py`, `audio_gate.py` on the delivered file (`00-RULES.md` §2).
* **Colour:** match the approved organic look for this set (the Codex recipe carries per-set LUTs). Measure it on these rolls; don't copy a preset.
* **Assets:** walk every bracketed cue in the script. Use Pexels or owned footage for stock; AI clips follow the $5/video + frame-approval rule.
  **List every hole before you build**, and ask Dan only about holes you can't fill yourself.
* **Deliver the horizontal master + `.srt` + chapters**, then stop for Dan's review. Uploading, thumbnails and Blotato are
  `/video-setup`, a separate step. When Dan approves, its shorts become a new List 2 job in `00-MASTER.md`.

## This video's specifics
* Extra B-roll: 8/28 shoot C1677 (vacuum demo, 16:9, strong side light) in `/Volumes/Extreme/abs by ai 8:28 shoot | jeff | dan | ads, dedicated shorts, b roll, scripted long form content/main camera/`.
* Anatomy cues (transverse abdominis) want a simple labelled graphic, not an AI body.
* ℹ️ DS-04 (the dedicated short "The Only Ab Exercise That Shrinks Belly Fat") covers the same topic. Keep the grade consistent if both are built.

## Starter prompts
**Claude (Fable 5.1, high):**
> Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/RO-02-the-vacuum-explainer.md`: transcribe the rolls, map the takes to the script, and cut "The Vacuum: The Best Ab Exercise For Belly Fat" into a finished 16:9 first cut with /longform-edit to the approved organic standard (Zeeshan's ab wheel videos). Fill the B-roll and graphics cues, audio through the shared chain, every gate, independent audit, deliver master + SRT + chapters, send me the review copy, update the master list.

**Codex (GPT-6 Astra, high):**
> Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table), then execute `Handoffs/video-editing/RO-02-the-vacuum-explainer.md` with `$abs-edit-organic` and the frozen organic recipe. Deliver master + SRT + chapters, send Dan the review copy, update `00-MASTER.md`.
