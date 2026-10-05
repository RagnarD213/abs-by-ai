# SL-11: Shorts from "The Stomach Vacuum: The Best Ab Exercise For Belly Fat" (RO-02)

**List 2 · shorts from a finished long-form · READY.** Read `00-RULES.md` first. Added 2026-10-05 when RO-02 was set up for release.

## Source
`claude edited long form content/12 - The Vacuum The Best Ab Exercise For Belly Fat/The Vacuum The Best Ab Exercise For Belly Fat | claude round 3 | 16x9 | RO-02.mp4`
(our own master, 11:46.6, SHA-256 `24d71e04f1d952c3809b82e25c10f388fe722c12f7258d9c7cd1cb24d874996d`). Also on the Extreme drive
(`/Volumes/Extreme/Claude Content Videos/The Vacuum - RO-02/`) and Google Drive (`Claude Content Videos/The Vacuum - RO-02`).
The 203-cue `.srt` and `chapters.txt` are beside it; the build recipe is `.claude/skills/longform-edit/reference/ro02/` and `/Volumes/Extreme/_edit_work/ro02/`.

## How to cut them
* Use `/shorts` (Claude), or its `SKILL.md` as the method (Codex). **Pick segments first and show Dan the list** (title, in/out,
  why it stands alone) before rendering. Dan picks.
* **Graphics: Soft Blue Light built from the HyperFrames templates** (`_shared/VIDEO-RULES.md`, 2026-10-01). If this is the first
  vertical batch in that set, Dan gets the full pre-approval round of every asset before anything is built.
* **Every short gives the viewer a tactic** and stands alone (memory `shorts-reason-to-watch`). A short that tells the viewer to do
  the vacuum shows the whole movement briefly (the live set at 8:48 or the how-to demo), not a detail (`shorts-show-whole-exercise`).
* Benefit-first titles, 45-60 s, full-frame 9:16, word-timed captions, vertical centering per `_shared/framing-motion.md`.
* No covers in this job: covers are a separate Codex task (Dan, 2026-09-25).
* **Don't upload or queue.** A short never posts before its parent is public (Wed Oct 28 2026, 9 AM CT, `BLOTATO_QUEUE_PROGRESS.md`).

## This video's specifics
* Candidate segments (film times): why ab exercises will not burn belly fat (0:00 - 0:34); the transverse abdominis, the hidden sleeve
  (1:24 - 2:03); the bodybuilder waist history (2:03 - 2:31); the mirror and mindset effect (2:50 - 3:36); standing vs hands and
  knees (4:20 - 5:40); how to do it step by step (6:24 - 8:42); the 20 second timer and breathing trap (7:45 - 8:42); the beginner
  one, two, three sets routine (9:12 - 10:19). Expect **4-5 shorts**.
* **No fat pinching, no belly close-ups** (Dan, 2026-10-04). Frame the vacuum from the chest up or wide; do not centre on the belly.
* The opener has two realistic AI clips (crunches, sit-ups) with AI-GENERATED labels (0:00 - 0:06.5): keep the labels and set
  `ai_generated` true at setup for any short that uses them.
* He says Zepbound once (3:40). Organic may name the drug; keep "Not medical advice. Talk to your doctor." on screen in a short that uses it.
* The live set (8:42 - 9:12) is near silent by design; no bed unless Dan asks.
* Do not duplicate RO-16 (If I Had Belly Fat) or RO-10 (Calories) shorts on the same point.

## Deliver
`Short-form video content/vacuum-short<N>_<title>.mp4` (1080x1920) + stamps, and a `vacuum-SHORTS.md` listing each
short's in/out, title and parent. Send Dan the REVIEW copies. Update `00-MASTER.md`.

## Starter prompts
**Claude (Opus 5.5, high):**
> Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/SL-11-the-vacuum-shorts.md`: propose the shorts segments from the RO-02 "The Vacuum" master and wait for my picks, then cut them with /shorts in Soft Blue Light, with gates and an independent audit (no covers; Codex does those). Deliver, send me the review copies, update the master list. Name this session "The Vacuum SFC R1".

**Codex (GPT-6 Sol, high):**
> Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table), then execute `Handoffs/video-editing/SL-11-the-vacuum-shorts.md` using `.claude/skills/shorts/SKILL.md` as the method: propose segments from the RO-02 master, wait for Dan's picks, cut, gate, deliver, update `00-MASTER.md`. Name this task "The Vacuum SFC R1".
