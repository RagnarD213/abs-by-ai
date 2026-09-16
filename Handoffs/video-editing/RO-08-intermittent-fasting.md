# RO-08 — "Intermittent Fasting: The Best Way To Get Abs": organic first cut from raw footage

**List 1 · organic long-form · READY.** Read `00-RULES.md` first.

## Source
7/8 shoot (`/Volumes/Extreme/abs by ai 7:8 Jeff Chagrin shoot/main camera/`): **C1486 (23:06)**, which holds several intro takes (*"Today I want to show you why intermittent fasting is the number one most powerful way…"*) and the full body through the outro at ~21:11.

**Script:** Second Shoot outlines doc, Drive `15gg6GP_Huy93ZBfTpbQuUtHGDrgHL-bs6Op-nN2UBr8`.

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
* **Older set (7/8 shoot):** 1920×1080 29.97, BT.709 (not S-Log), **one 2-channel audio stream**. Run `pick_lav.py` anyway; don't assume a channel. Same set and camera as published V3 "My Top 10 Tips" (C1489), so match V3's framing and set colour, finished to the newer Zeeshan-level standard.
* **Filmed off an outline, not a teleprompter.** Dan talks freely, so expect restatements. Keep the first clear statement plus the strongest example, and cut the restatements (the pattern in `Handoffs/HANDOFF_invest_health_cutdowns.md`). Target roughly 10–15 min unless the material earns more; say what you cut in `notes.md`.
* Whisper transcript already made (base.en, for mapping only): `/Volumes/Extreme/_edit_work/_transcripts-828-full/<roll>.txt`. Re-transcribe at word level for the edit.
* Health claims (autophagy/cell energy, productivity): keep Dan's hedges, and put no stronger claim in on-screen text. The *"fast until 2 PM, break with salad"* beats can pull B-roll from the Daily Salad rolls (C1533–C1556).
* ℹ️ V3 already covers fasting as tip 5–6. Chapter titles and the thumbnail angle should not duplicate V3's.

## Starter prompts
**Claude (Fable 5.1, high):**
> Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/RO-08-intermittent-fasting.md`: transcribe the rolls, map the takes to the outline, and cut "Intermittent Fasting: The Best Way To Get Abs" into a finished 16:9 first cut with /longform-edit to the approved organic standard (Zeeshan's ab wheel videos). Fill the B-roll and graphics cues, audio through the shared chain, every gate, independent audit, deliver master + SRT + chapters, send me the review copy, update the master list.

**Codex (GPT-6 Astra, high):**
> Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table), then execute `Handoffs/video-editing/RO-08-intermittent-fasting.md` with `$abs-edit-organic` and the frozen organic recipe. Deliver master + SRT + chapters, send Dan the review copy, update `00-MASTER.md`.
