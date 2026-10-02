# SL-07: Shorts from "If I Had Belly Fat, Here's How I'd Lose It In 90 Days" (RO-16)

**List 2 · shorts from a finished long-form · READY.** Read `00-RULES.md` first. Added 2026-10-02 when RO-16 was set up for release.

## Source
`claude edited long form content/09 - If I Had Belly Fat, Here's How I'd Lose It In 90 Days/If I Had Belly Fat, Here's How I'd Lose It In 90 Days | claude round 3 | 16x9 | RO-16.mp4`
(our own master, 12:09.33, SHA-256 `c535ab4cfe881fc95796c9f5a191535c87aa2d2bb61d3588a4f850da02643b09`). Also on the Extreme drive
(`/Volumes/Extreme/Claude Content Videos/If I Had Belly Fat - RO-16/`) and Google Drive (`Claude Content Videos/If I Had Belly Fat - RO-16`).
The 218-cue `.srt` and `chapters.txt` are beside it; the build recipe is `recipe-RO-16/` and `/Volumes/Extreme/_edit_work/ro16/`.

## How to cut them
* Use `/shorts` (Claude), or its `SKILL.md` as the method (Codex). **Pick segments first and show Dan the list** (title, in/out,
  why it stands alone) before rendering. Dan picks.
* **Graphics: Soft Blue Light built from the HyperFrames templates, not J2** (Dan, 2026-10-01, `_shared/VIDEO-RULES.md`). If this is
  the first vertical batch in that set, Dan gets the full pre-approval round of every asset before anything is built.
* **Every short gives the viewer a tactic** and stands alone (memory `shorts-reason-to-watch`). Benefit-first titles, 45-60 s,
  full-frame 9:16, word-timed captions, steady framing, cuts snapped to silence.
* No covers in this job: covers are a separate Codex task (Dan, 2026-09-25).
* **Don't upload or queue.** A short never posts before its parent is public (Sun Nov 1 2026, 9 AM CT, `BLOTATO_QUEUE_PROGRESS.md`).

## This video's specifics
* Eight steps, each a candidate: take time off for 90 days (1:07), Zepbound in week one (2:49), work out every morning (4:52), meal prep
  service (6:00), track calories with AI (7:07), 0.8 g protein per pound (8:08), weigh in every day (9:42), plan to never do it again (10:36).
  Also the hook "1 pound a week is bullshit" (0:50 - 1:07). Expect **4-5 shorts**. Dan's on-camera swearing stays.
* Organic may name the drug (Dan, 2026-09-30). Keep "Not medical advice. Talk to your doctor." on screen in each short that
  touches Zepbound.
* Realistic AI clips (mirror opener 0:00, kitchen dad 1:25, office 1:57, pizza refusal 3:34, gym deadlift 9:12, closing scenes
  11:59): keep their AI-GENERATED labels; `ai_generated: true` at setup for any short that uses one.
* Don't duplicate RO-12 (Top 5 Zepbound Tips), RO-10 (Calories) or RO-01 shorts on the same point.

## Deliver
`Short-form video content/belly-fat-90-days-short<N>_<title>.mp4` (1080x1920) + stamps, and a `belly-fat-90-days-SHORTS.md` listing each
short's in/out, title and parent. Send Dan the REVIEW copies. Update `00-MASTER.md`.

## Starter prompts
**Claude (Opus 5.5, high):**
> Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/SL-07-if-i-had-belly-fat-shorts.md`: propose the shorts segments from the RO-16 "If I Had Belly Fat" master and wait for my picks, then cut them with /shorts in Soft Blue Light, with gates and an independent audit (no covers; Codex does those). Deliver, send me the review copies, update the master list. Name this session "If I Had Belly Fat SFC R1".

**Codex (GPT-6 Sol, high):**
> Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table), then execute `Handoffs/video-editing/SL-07-if-i-had-belly-fat-shorts.md` using `.claude/skills/shorts/SKILL.md` as the method: propose segments from the RO-16 master, wait for Dan's picks, cut, gate, deliver, update `00-MASTER.md`. Name this task "If I Had Belly Fat SFC R1".
