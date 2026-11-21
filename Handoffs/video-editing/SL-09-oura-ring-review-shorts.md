# SL-09: Shorts from "My Honest Oura Ring Review After 1.5 Years" (Zeeshan Video 4)

**List 2 · shorts from a finished long-form · READY.** Read `00-RULES.md` first. Added 2026-10-02 when Video 4 was set up for release.

## Source
`Zeeshan Content Videos/my honest oura ring review - video 4/my honest oura ring review | zeeshan | 16x9 | video 4.mp4` (Zeeshan's Rev 3, Dan finalized as is, 19:47.5, 1920x1080, MD5 `5264285762af41f2a6644366e0bae7eb`). Also on the Extreme drive
(`/Volumes/Extreme/Zeeshan Content Videos/my honest oura ring review - video 4/`) and Google Drive (`Zeeshan Content Videos/my honest oura ring review - video 4`).
The 1,181 s `.srt` is beside it. An editor's finished mix: his audio goes into every short untouched (`--verbatim`).

## How to cut them
* Use `/shorts` (Claude), or its `SKILL.md` as the method (Codex). **Pick segments first and show Dan the list** (title, in/out,
  why it stands alone) before rendering. Dan picks.
* **Graphics: Soft Blue Light built from the HyperFrames templates, not J2** (Dan, 2026-10-01, `_shared/VIDEO-RULES.md`). If this is
  the first vertical batch in that set, Dan gets the full pre-approval round of every asset before anything is built.
* **Every short gives the viewer a tactic** and stands alone (memory `shorts-reason-to-watch`). Benefit-first titles, 45-60 s,
  full-frame 9:16, word-timed captions, steady framing, cuts snapped to silence.
* No covers in this job: covers are made in the setup task.
* **Don't upload or queue.** A short never posts before its parent is public (Wed Oct 14 2026, 9 AM CT, `BLOTATO_QUEUE_PROGRESS.md`).

## This video's specifics
* Natural shorts by chapter: finger vs wrist for sleep (3:56 - 5:22), which finger to wear it on (5:22 - 6:24), the $400 price and the used-ring tip (7:34 - 9:26), the "take it easy" advice you should ignore (11:18 - 12:22), what it showed me about alcohol and late-night driving (15:13 - 16:22), Oura vs WHOOP verdict (17:46 - 18:34). Expect **4-5 shorts**.
* Zeeshan's finished cut has his blue Soft Blue lower thirds burned in; handle them (never crop a card shorter, `VIDEO-RULES.md`).
* The Tesla AI clip (15:46 - 15:53.5) shows a speedometer reading up to 190 while Dan says 120. Dan shipped the long-form as is, but do not carry that flaw into a short: trim it or skip it. The AI label also hangs about 5 frames past the sleep and jiu-jitsu clips; cut on clean frames.
* Realistic AI clips (4:33.5, 6:39, 14:11.5, 15:46) keep their AI-GENERATED labels; `ai_generated: true` at setup for any short that uses one.
* Shorts stand alone: when a short tells the viewer to wear it on a certain finger or buy a used ring, show the thing briefly.
* The ending sells the app and the AI sleep coach; a short ends on its own tactic, not that pitch.

## Deliver
`Short-form video content/oura-short<N>_<title>.mp4` (1080x1920) + stamps, and an `oura-SHORTS.md` listing each
short's in/out, title and parent. Send Dan the REVIEW copies. Update `00-MASTER.md`.

## Starter prompts
**Claude (Opus 5.5, high):**
> Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/SL-09-oura-ring-review-shorts.md`: propose the shorts segments from Zeeshan's Oura Ring review (Video 4) and wait for my picks, then cut them with /shorts in Soft Blue Light, with gates and an independent audit (no covers). Deliver, send me the review copies, update the master list. Name this session "Oura Ring Review SFC R1".

**Codex (GPT-6 Sol, high):**
> Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table), then execute `Handoffs/video-editing/SL-09-oura-ring-review-shorts.md` using `.claude/skills/shorts/SKILL.md` as the method: propose segments from the Video 4 master, wait for Dan's picks, cut, gate, deliver, update `00-MASTER.md`. Name this task "Oura Ring Review SFC R1".
