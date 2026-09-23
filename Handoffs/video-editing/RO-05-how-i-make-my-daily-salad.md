# RO-05 — "How I Make My Daily Salad": organic first cut from raw footage

**List 1 · organic long-form · READY (recut).** Read `00-RULES.md` first.

> ⚠ **2026-09-23: Claude's cut was rejected as unpublishable.** Do not execute this doc's starter prompts. Use the from-scratch recut
> handoffs instead: `Handoffs/handoff-20260923-ro05-recut-fable.md` (Claude, Fable 5.1 high) and
> `Handoffs/handoff-20260923-ro05-recut-astra.md` (Codex, GPT-6 Astra high). They carry Dan's verdict, the mistakes, and every
> verified asset.

## Source
8/3 shoot (`/Volumes/Extreme/abs by ai 8:3 jeff chagrin shoot/main camera/`): **C1533–C1556** (24 clips, 0:18–5:45 each, about 50 min raw, kitchen set). C1556 is the outro. **C1541 (5:45) is the app macro-tracking demo**, already used in `claude edited long form content/05 - Meal Prep Macro Tracking (app demo)/` (3:48). Reuse that edit's split-screen as this video's tracking section instead of recutting it. 8/3 GoPro angles (`gopro 2/`) are unmapped. Check whether any cover the counter.

**Script:** Shoot 3 doc, Drive `1VeNXATtvHBVe_Y5S3fxmSjllZxva0zwgo5NghW-G_bU` (item 7).

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
* 50 minutes raw for what should be a tight 10–15 minute video. Cut hard, keeping every ingredient and the reasoning, one take of each.
* Ingredient name/macro cards (J2). No brand claims.
* Its salad footage is also wanted as B-roll by the dedicated short DS-16 "How To Lose The Last Ten Pounds". Note good ranges in `notes.md`.

## Starter prompts
**Claude (Fable 5.1, high):**
> Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/RO-05-how-i-make-my-daily-salad.md`: transcribe the rolls, map the takes to the script, and cut "How I Make My Daily Salad" into a finished 16:9 first cut with /longform-edit to the approved organic standard (Zeeshan's ab wheel videos). Fill the B-roll and graphics cues, audio through the shared chain, every gate, independent audit, deliver master + SRT + chapters, send me the review copy, update the master list.

**Codex (GPT-6 Astra, high):**
> Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table), then execute `Handoffs/video-editing/RO-05-how-i-make-my-daily-salad.md` with `$abs-edit-organic` and the frozen organic recipe. Deliver master + SRT + chapters, send Dan the review copy, update `00-MASTER.md`.
