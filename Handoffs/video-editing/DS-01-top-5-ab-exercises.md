**Current next action (2026-10-26):** R4 delivered for Dan's review: Dan's own cable crunch (B0574) swapped into Muhammad's HQ V4 at 18.785-25.993, everything else unchanged. Review http://127.0.0.1:9101/; notes `/Volumes/Extreme/_edit_work/DS-01/round4/NOTES-R4.md`. After approval: finalize, file `Short-form video content/ds-01_top-5-ab-exercises.mp4`, then `/video-setup`. The original first-cut instructions below are historical.

# DS-01 — "Top 5 Ab Exercises": dedicated talking short, first cut from raw footage

**List 1 · organic dedicated short (raw only) · READY.** Read `00-RULES.md` first. Filmed on 8/28 **as a short**, not
cut from a long-form. It's a vertical original, so there's no parent video to wait for.

## Source
* **Roll:** `/Volumes/Extreme/abs by ai 8:28 shoot | jeff | dan | ads, dedicated shorts, b roll, scripted long form content/main camera/` **C1654 ≈0:00–2:40**. Times are approximate, from a Whisper pass. Full transcript: `/Volumes/Extreme/_edit_work/_transcripts-828-full/`. The range holds the slate
  (*"the video I'm about to film is…"*), every take and crew chatter.
* **Script:** Shoot 5 scripts doc, Drive `1yZjcG5pkbw0kPsfTvc7OOr2bX6v0bVYMqquUiRENQ4k` (local plain-text copy: `Media/codex-video-trial/05-recipes/candidates/shoot5-notes.txt`), lines **619–634** (section 6, short-form talking scripts ("Dedicated shorts content. Vertical 9:16.")).
* 4K 29.97 S-Log3, four mono tracks: `pick_lav.py` per file. Framed horizontal and centre-safe; verify Dan stays inside the vertical crop on every take you use.

## Deliverable
**One 1080×1920 short, 45–66 s** (Dan's measured target; memory `shorts-organic-research`; `/shorts-scripting` sets a hard 66 s ceiling). Cold open, no greeting.
Word-timed captions in the J2 tactical style, AbsByAI.com mark where the script cues it, and a comment-prompt CTA as filmed. No cover image: covers are a separate Codex task (Dan, 2026-09-25).
REVIEW copy, audio A/B, stamps, `notes.md` (take map + choices), `recipe/`.

## Build
* **Take selection:** best take of every line (Claude: `/ad-edit` Steps 1-4 method; Codex: `$long-form-content-edit`). Airtight, zoom cuts on word onsets, no naked jump cuts.
* **Vertical finishing:** `/shorts` rules for captions, graphics, safe areas and steady framing (`_shared/framing-motion.md`).
* **Colour:** the 8/28 S-Log3 conversion (memory `shoot-828-slog3-format`), decoded as BT.709. Build all dedicated shorts to one look.
* **Audio:** `pick_lav.py` → `voice_chain.py` → `audio_gate.py` on the delivered file.
* **B-roll / pictures:** every cue in the script gets filled. Label real pictures of Dan and every AI image (`00-RULES.md` §2). List the holes before building. Pexels for stock.

## This short's specifics
* B-roll: ab wheel rollout (the $17 Ab Wheel long-form or 8/28 b-roll C1679), spiderman plank (`short4_spiderman-planks`), V-sit twist (`short3_v-sit-twists`), toe touch (`short2_toe-touches`), plus 8/28 b-roll C1682/C1683.
* **Hole:** cable crunch, which doesn't exist. Use a Pexels clip.

## Deliver
`Short-form video content/ds-01_top-5-ab-exercises.mp4` + stamps (no covers: separate Codex task). **Don't upload or queue.** Organic shorts go out through Blotato, uploaded Private (`/video-setup` step, separate). Send Dan the review copy. Update `00-MASTER.md`.

## Starter prompts
**Claude (Fable 5.1, high; Opus 5 high is enough when every b-roll cue already exists):**
> Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/DS-01-top-5-ab-exercises.md`: cut the dedicated short "Top 5 Ab Exercises" from its 8/28 raw takes. Best take of every line, 1080×1920, 45–66 s, J2 captions, every b-roll cue filled and labelled, the 8/28 S-Log3 conversion, lav picked per file, cover image. Every gate, independent audit, deliver, send me the review copy, update the master list.

**Codex (GPT-6 Astra, high):**
> Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table), then execute `Handoffs/video-editing/DS-01-top-5-ab-exercises.md` with `$long-form-content-edit` for take selection/audio/colour and `.claude/skills/shorts/SKILL.md` for vertical finishing. Deliver, send Dan the review copy, update `00-MASTER.md`.


## October 23 library dependency resolved (2026-10-25)

Dan finalized the exercise identities and Color C. The checked full-quality cable-crunch assets below are registered in the shared library and have verified copies on Extreme, Expansion and Drive. Use the final Color C editing masters, then fit them to the approved film as already required. The source range map and checked clip hashes are in `Media/footage-index/shoot-20261023/permanent-library-map.json`. Original recordings remain on Expansion.

- **B0574**: checked native editing master. Resolve its path/link and exact source range through the private shared catalog.
- **B0582**: checked native editing master. Resolve its path/link and exact source range through the private shared catalog.
- **B0583**: checked native editing master. Resolve its path/link and exact source range through the private shared catalog.

The longer side-angle second take is the first candidate for the 7.2-second replacement. Inspect its complete motion and keep the rope near the head, ribs curling toward the pelvis and hips steady. The short frontal close-ups provide alternatives. Teaching intent remains unknown where the source did not establish it; these are identified cable-crunch assets, not a blanket endorsement of every rep. The stock-footage dependency is resolved. The existing film revision has not been executed by this footage-preparation task. No editing chat was started.
