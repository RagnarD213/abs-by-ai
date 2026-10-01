# SL-06: Shorts from "Top 5 Zepbound Tips" (RO-12)

**List 2 · shorts from a finished long-form · READY.** Read `00-RULES.md` first. Added 2026-10-01 when RO-12 was set up for release.

## Source
`claude edited long form content/09 - Top 5 Zepbound Tips/Top 5 Zepbound Tips | claude | 16x9 | RO-12.mp4` (our own master, 9:11.42, SHA-256
`7f6766c5e1d82881fb2a56b9b7414f6baa0bbe49f027828e507991d9f7cae67b`). Also on the Extreme drive
(`/Volumes/Extreme/Claude Content Videos/Top 5 Zepbound Tips - RO-12/`) and Google Drive (`Claude Content Videos/Top 5 Zepbound Tips - RO-12`).
The 180-cue `.srt` and `chapters.txt` are beside it; the build recipe is `recipe-RO12/` and `/Volumes/Extreme/_edit_work/ro12/`.

## How to cut them
* Use `/shorts` (Claude), or its `SKILL.md` as the method (Codex). **Pick segments first and show Dan the list** (title, in/out,
  why it stands alone) before rendering. Dan picks.
* **Graphics: Soft Blue Light built from the HyperFrames templates, not J2** (Dan, 2026-10-01, `_shared/VIDEO-RULES.md`). If this is
  the first vertical batch in that set, Dan gets the full pre-approval round of every asset before anything is built.
* **Every short gives the viewer a tactic** and stands alone (memory `shorts-reason-to-watch`). Benefit-first titles, 45-60 s,
  full-frame 9:16, word-timed captions, steady framing, cuts snapped to silence.
* No covers in this job: covers are a separate Codex task (Dan, 2026-09-25).
* **Don't upload or queue.** A short never posts before its parent is public (Sun Oct 25 2026, `BLOTATO_QUEUE_PROGRESS.md`).

## This video's specifics
* Five tips, each a natural short: needles and vials not pens (0:37 - 2:42, needs trimming), how to inject (2:42 - 4:12), inject
  Thursday evening (4:12 - 5:28), taper off slowly (5:28 - 6:47), focus on protein (6:47 - 8:33). Expect **4-5 shorts**.
* Organic may name the drug (Dan, 2026-09-30). Keep "Not medical advice. Talk to your doctor." on screen in each short.
* Three labelled AI clips (1:42, 6:54, 7:53): keep their AI-GENERATED labels; `ai_generated: true` at setup for any short that uses one.
* Don't duplicate DS-10 (3 Unexpected Ways Zepbound Helped Me) or RO-01's shorts on the muscle point.

## Deliver
`Short-form video content/zepbound-tips-short<N>_<title>.mp4` (1080x1920) + stamps, and a `zepbound-tips-SHORTS.md` listing each
short's in/out, title and parent. Send Dan the REVIEW copies. Update `00-MASTER.md`.

## Starter prompts
**Claude (Opus 5.5, high):**
> Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/SL-06-top-5-zepbound-tips-shorts.md`: propose the shorts segments from the RO-12 "Top 5 Zepbound Tips" master and wait for my picks, then cut them with /shorts in Soft Blue Light, with gates and an independent audit (no covers; Codex does those). Deliver, send me the review copies, update the master list. Name this session "Top 5 Zepbound Tips SFC R1".

**Codex (GPT-6 Sol, high):**
> Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table), then execute `Handoffs/video-editing/SL-06-top-5-zepbound-tips-shorts.md` using `.claude/skills/shorts/SKILL.md` as the method: propose segments from the RO-12 master, wait for Dan's picks, cut, gate, deliver, update `00-MASTER.md`. Name this task "Top 5 Zepbound Tips SFC R1".
