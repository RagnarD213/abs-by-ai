# DS-20 — "The Five Levels Of Pushups": dedicated workout short, first cut from raw footage

**List 1 · organic dedicated short (raw only) · READY.** Read `00-RULES.md` first. Filmed on 8/28 **as a short**, not
cut from a long-form. It's a vertical original, so there's no parent video to wait for.

## Source
* **Roll:** `/Volumes/Extreme/abs by ai 8:28 shoot | jeff | dan | ads, dedicated shorts, b roll, scripted long form content/main camera/` **C1671 ≈2:20–3:50**. Times are approximate, from a Whisper pass. Full transcript: `/Volumes/Extreme/_edit_work/_transcripts-828-full/`. The range holds the slate
  (*"the video I'm about to film is…"*), every take and crew chatter.
* **Script:** Shoot 5 scripts doc, Drive `1yZjcG5pkbw0kPsfTvc7OOr2bX6v0bVYMqquUiRENQ4k` (local plain-text copy: `Media/codex-video-trial/05-recipes/candidates/shoot5-notes.txt`), lines **878–888** (section 7, short-form workout scripts ("Dedicated shorts workout content. Vertical 9:16."); b-roll list in section 8).
* 4K 29.97 S-Log3, four mono tracks: `pick_lav.py` per file. Framed horizontal and centre-safe; verify Dan stays inside the vertical crop on every take you use.

## Deliverable
**One 1080×1920 short, 45–66 s** (Dan's measured target; memory `shorts-organic-research`; `/shorts-scripting` sets a hard 66 s ceiling). Cold open, no greeting.
Word-timed captions in the J2 tactical style, AbsByAI.com mark where the script cues it, and a comment-prompt CTA as filmed. No cover image: covers are a separate Codex task (Dan, 2026-09-25).
REVIEW copy, audio A/B, stamps, `notes.md` (take map + choices), `recipe/`.

## Build
* **Take selection:** best take of every line (Claude: `/ad-edit` Steps 1–4 method; Codex: `$abs-edit-organic`). Airtight, zoom cuts on word onsets, no naked jump cuts.
* **Vertical finishing:** `/shorts` rules for captions, graphics, safe areas and steady framing (`_shared/framing-motion.md`).
* **Colour:** the 8/28 S-Log3 conversion (memory `shoot-828-slog3-format`), decoded as BT.709. Build all dedicated shorts to one look.
* **Audio:** `pick_lav.py` → `voice_chain.py` → `audio_gate.py` on the delivered file.
* **B-roll / pictures:** every cue in the script gets filled. Label real pictures of Dan and every AI image (`00-RULES.md` §2). List the holes before building. Pexels for stock.

## This short's specifics
* B-roll: 8/28 C1680–C1681 (pushup levels): countertop, knee, regular, handles, decline, handstand. Verify every level exists. Level cards 1–5.

## Deliver
`Short-form video content/ds-20_five-levels-of-pushups.mp4` + stamps (no covers: separate Codex task). **Don't upload or queue.** Organic shorts go out through Blotato, uploaded Private (`/video-setup` step, separate). Send Dan the review copy. Update `00-MASTER.md`.

## Starter prompts
**Claude (Fable 5.1, high; Opus 5 high is enough when every b-roll cue already exists):**
> Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/DS-20-five-levels-of-pushups.md`: cut the dedicated short "The Five Levels Of Pushups" from its 8/28 raw takes. Best take of every line, 1080×1920, 45–66 s, J2 captions, every b-roll cue filled and labelled, the 8/28 S-Log3 conversion, lav picked per file, cover image. Every gate, independent audit, deliver, send me the review copy, update the master list.

**Codex (GPT-6 Astra, high):**
> Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table), then execute `Handoffs/video-editing/DS-20-five-levels-of-pushups.md` with `$abs-edit-organic` for take selection/audio/colour and `.claude/skills/shorts/SKILL.md` for vertical finishing. Deliver, send Dan the review copy, update `00-MASTER.md`.
