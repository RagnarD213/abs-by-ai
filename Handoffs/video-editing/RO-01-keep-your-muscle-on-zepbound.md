# RO-01 — "How To Keep Your Muscle On Zepbound": organic first cut from raw footage

**List 1 · organic long-form · READY.** Read `00-RULES.md` first.

## Source
8/14 shoot (`/Volumes/Extreme/abs by ai 8:14 shoot | teleprompter ads, indoor talking content, outdoor workout content | jeff chagrin | dan rose/`): **C1605 (0:59), C1606 (1:56), C1607 (14:59), C1608 (9:09)**, about 27 min raw. C1605 opens: *"this video is the first talking video in the outlines, how to keep your muscle on Zepbound."*

**Script:** Shoot 4 outlines doc, Drive `1uDAWvxoAjXUaawZctgdSDj_9JPa5mfk5MMM2Sh8L7yE` (talking outline, filmed off the outline, not a teleprompter, so expect looser takes).

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
* ⚠ **No drug brand names in on-screen graphics or chips** (Zepbound, Ozempic, Wegovy, Mounjaro). Captions and the SRT get checked too. Dan's spoken words stay.
* Dan's on-camera medical disclaimers are load-bearing. Never cut them.
* Protein-target and resistance-training segments want simple J2 number cards. Keep claims as Dan said them, never stronger.
* ℹ️ Dan's hold on long-forms 02 (Zepbound Update) and 03 (Supplements) is about uploading those two videos, not the topic. Editing this one is fine; publishing timing is his call.

## Starter prompts
**Claude (Fable 5.1, high):**
> Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/RO-01-keep-your-muscle-on-zepbound.md`: transcribe the rolls, map the takes to the script, and cut "How To Keep Your Muscle On Zepbound" into a finished 16:9 first cut with /longform-edit to the approved organic standard (Zeeshan's ab wheel videos). Fill the B-roll and graphics cues, audio through the shared chain, every gate, independent audit, deliver master + SRT + chapters, send me the review copy, update the master list.

**Codex (GPT-6 Astra, high):**
> Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table), then execute `Handoffs/video-editing/RO-01-keep-your-muscle-on-zepbound.md` with `$abs-edit-organic` and the frozen organic recipe. Deliver master + SRT + chapters, send Dan the review copy, update `00-MASTER.md`.
