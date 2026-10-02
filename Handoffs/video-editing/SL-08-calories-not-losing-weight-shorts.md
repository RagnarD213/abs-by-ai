# SL-08: Shorts from "Calories: The Reason You're Not Losing Weight" (RO-10)

**List 2 · shorts from a finished long-form · READY.** Read `00-RULES.md` first. Added 2026-10-02 when RO-10 was set up for release.

## Source
`claude edited long form content/10 - Calories The Reason You're Not Losing Weight/Calories The Reason You're Not Losing Weight | claude round 2 | 16x9 | RO-10.mp4` (our own master, 8:38.25, SHA-256
`655c71882ea3e6baa1c71d661fdcd8465e94d972183f4969e09d2430787bb76e`). Also on the Extreme drive
(`/Volumes/Extreme/Claude Content Videos/Calories The Reason You're Not Losing Weight - RO-10/`) and Google Drive (`Claude Content Videos/Calories The Reason You're Not Losing Weight - RO-10`).
The 156-cue `.srt` and `.chapters.txt` are beside it; the build recipe is `recipe-RO-10/` and `/Volumes/Extreme/_edit_work/ro10/`.

## How to cut them
* Use `/shorts` (Claude), or its `SKILL.md` as the method (Codex). **Pick segments first and show Dan the list** (title, in/out,
  why it stands alone) before rendering. Dan picks.
* **Graphics: Soft Blue Light built from the HyperFrames templates, not J2** (Dan, 2026-10-01, `_shared/VIDEO-RULES.md`). If this is
  the first vertical batch in that set, Dan gets the full pre-approval round of every asset before anything is built.
* **Every short gives the viewer a tactic** and stands alone (memory `shorts-reason-to-watch`). Benefit-first titles, 45-60 s,
  full-frame 9:16, word-timed captions, steady framing, cuts snapped to silence.
* No covers in this job: covers are a separate Codex task (Dan, 2026-09-25).
* **Don't upload or queue.** A short never posts before its parent is public (Wed Oct 7 2026, `BLOTATO_QUEUE_PROGRESS.md`).

## This video's specifics
* Natural shorts by chapter: the Twinkie professor and the Stanford study (0:30 - 1:44, trim), people eat 47% more than they think + track with AI (3:18), fast until 2 PM + black coffee (3:54 - 5:31), salad first (5:31 - 6:21), protein snacks (6:21 - 7:01), liquid calories and the Purdue study (7:01 - 7:57). Expect **4-5 shorts**.
* Organic may name the drug (Dan, 2026-09-30). The GLP-1 chapter (1:44) keeps "Not medical advice. Talk to your doctor." on screen.
* Realistic AI clips (opener's two, 0:31 kitchen clip, snack cake): keep their AI-GENERATED labels; `ai_generated: true` at setup for any short that uses one.
* The film's ending teases the next video (RO-11, when calories don't matter); do not carry that line into a short.
* Shorts stand alone: when a short tells the viewer to do something (fast until 2, salad first), show the thing briefly.

## Deliver
`Short-form video content/calories-short<N>_<title>.mp4` (1080x1920) + stamps, and a `calories-SHORTS.md` listing each
short's in/out, title and parent. Send Dan the REVIEW copies. Update `00-MASTER.md`.

## Starter prompts
**Claude (Opus 5.5, high):**
> Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/SL-08-calories-not-losing-weight-shorts.md`: propose the shorts segments from the RO-10 "Calories: The Reason You're Not Losing Weight" master and wait for my picks, then cut them with /shorts in Soft Blue Light, with gates and an independent audit (no covers; Codex does those). Deliver, send me the review copies, update the master list. Name this session "Calories Not Losing Weight SFC R1".

**Codex (GPT-6 Sol, high):**
> Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table), then execute `Handoffs/video-editing/SL-08-calories-not-losing-weight-shorts.md` using `.claude/skills/shorts/SKILL.md` as the method: propose segments from the RO-10 master, wait for Dan's picks, cut, gate, deliver, update `00-MASTER.md`. Name this task "Calories Not Losing Weight SFC R1".
