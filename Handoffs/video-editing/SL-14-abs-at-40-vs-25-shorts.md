# SL-14: Shorts from "Getting Abs At 40 vs 25: What's Different And What To Do About It" (Zeeshan Video 5)

**List 2 · shorts from a finished long-form · READY.** Read `00-RULES.md` first. Added 2026-10-11 when Video 5 was set up for release.

## Source
`Zeeshan Content Videos/getting abs at 40 vs 25 - video 5/getting abs at 40 vs 25 | zeeshan | 16x9 | video 5.mp4` (Zeeshan's Rev 3, Dan finalized 10-10, 20:15, 1920x1080, MD5 `dfdad6d05e9aba3c4ba34d41495d8f9e`). Also on the Seagate
(`/Volumes/Expansion/Zeeshan Content Videos/getting abs at 40 vs 25 - video 5/`) and Google Drive (`Zeeshan Content Videos/getting abs at 40 vs 25 - video 5`).
The `.srt` is beside it. An editor's finished mix: his audio goes into every short untouched (`--verbatim`).

## How to cut them
* Use `/shorts` (Claude), or its `SKILL.md` as the method (Codex). **Pick segments first and show Dan the list** (title, in/out, why it stands alone) before rendering. Dan picks.
* Graphics: Soft Blue Light built from the HyperFrames templates (`_shared/VIDEO-RULES.md`). Every short gives the viewer a tactic and stands alone (memory `shorts-reason-to-watch`); 45-60 s, full-frame 9:16, word-timed captions, steady framing, cuts snapped to silence.
* No covers in this job: covers are made in the setup task. **Don't upload or queue.** A short never posts before its parent is public (YouTube Sun Jan 3 2027, 9 AM CST).

## This video's specifics
* Natural shorts by chapter: why injuries make guys over 40 quit lifting (0:29 - 1:41), what gets easier at 40 (2:39 - 5:50), drop the high-risk lifts and why (6:05 - 9:00), shorter workouts done every day (9:07 - 11:17), fasting until 2 pm (13:33 - 15:22), the three AI things to do (16:42 - 18:31). Expect 4-5 shorts.
* Zeeshan's cut has Soft Blue lower thirds and list cards burned in; handle them (never crop a card shorter, `VIDEO-RULES.md`).
* Realistic AI clips (4:38, 6:26, 8:22) keep their AI-GENERATED labels; `ai_generated: true` at setup for any short that uses one. The opening 0:04 to 0:09 uses real before and after pictures with the real-picture label; the label is missing for 0.6 s on the first after picture (known and accepted by Dan).
* The ending sells the app; a short ends on its own tactic, not that pitch.

## Deliver
`Short-form video content/abs40-short<N>_<title>.mp4` (1080x1920) + stamps, and an `abs40-SHORTS.md` listing each short's in/out, title and parent. Send Dan the REVIEW copies. Update `00-MASTER.md`.

## Starter prompts
**Claude (Opus 5.5, high):**
> Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/SL-14-abs-at-40-vs-25-shorts.md`: propose the shorts segments from Zeeshan's Video 5 and wait for my picks, then cut them with /shorts in Soft Blue Light, with gates and an independent audit (no covers). Deliver, send me the review copies, update the master list. Name this session "Abs At 40 vs 25 SFC R1".

**Codex (GPT-6 Sol, high):**
> Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table), then execute `Handoffs/video-editing/SL-14-abs-at-40-vs-25-shorts.md` using `.claude/skills/shorts/SKILL.md` as the method: propose segments from the Video 5 master, wait for Dan's picks, cut, gate, deliver, update `00-MASTER.md`. Name this task "Abs At 40 vs 25 SFC R1".
