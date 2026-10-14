# SL-16: Shorts from "Intermittent Fasting: The Best Way To Get Abs" (RO-08)

**CONTENT, long-form (LFC): it gets Shorts cut from it and nothing else.**
**List 2 · shorts from a finished long-form · READY.** Read `00-RULES.md` first. Added 2026-10-14 when Dan finalized RO-08.

## Source
`claude edited long form content/15 - Intermittent Fasting The Best Way To Get Abs/Intermittent Fasting The Best Way To Get Abs | claude round 3 | 16x9 | RO-08.mp4`
(Claude round 3, Dan approved 10-14, 14:40.75, 1920x1080, SHA-256 `976b9761bc1e84553727aa599fe50e0befb7aa27e924220b4a14541bbba8867c`).
The `.srt` and `.chapters.txt` are beside it; the recipe is in `recipe-RO-08/` and `.claude/skills/longform-edit/reference/ro08/`, the work
folder is `/Volumes/Extreme/_edit_work/ro08/round3/`. Our own mix: voice 1a with the bass lift (Dan's pick, 10-12).

## How to cut them
* Use `/shorts` (Claude), or its `SKILL.md` as the method (Codex). **Pick segments first and show Dan the list** (title, in/out, why it stands alone) before rendering. Dan picks.
* Graphics: Soft Blue Light built from the HyperFrames templates (`_shared/VIDEO-RULES.md`). Every short gives the viewer a tactic and stands alone (memory `shorts-reason-to-watch`); 45-60 s, full-frame 9:16, word-timed captions, the land-then-hold framing, cuts snapped to silence.
* A short never opens on a list number ("Reason 3", "Mistake 2") or a line that points back at the long-form. Where one does, write the pickup line into the shortlist; pickups are recorded on the studio set at a shoot (VIDEO-RULES, 2026-10-13), so a short that needs one waits for the shoot.
* No covers in this job: covers are made in the setup task. **Don't upload or queue.** A short never posts before its parent is public.

## This video's specifics
* Natural shorts by chapter: what intermittent fasting is and the daily fast he does (0:37 - 2:31), the simplest way to eat less (2:31 - 4:12), it saves your mornings and you get more done (5:02 - 6:59), how to start: just skip breakfast, and the first month (9:04 - 11:08), break your fast with a salad (11:08 - 11:43), the three mistakes (11:43 - 14:04, binge eating at night, eating right before bed, alcohol). Expect 4-5 shorts; most open on a list number, so expect pickups.
* AI clips in the film carry the AI-GENERATED chip (0:00 opener, 3:23 boxing glove, 4:55 cell cartoon, 6:07 donut, 7:24 and 7:45 excuse voices, 12:11 fridge raid, 13:35 beer); `ai_generated: true` at setup for any short that uses one. A short that keeps one keeps it as it is in the film: every one passed the three AI clip questions (VIDEO-RULES top section). Do not extend any of them past their cut in the film (the library notes say why: clip library A0169 to A0175).
* Hair touches the top edge through the roll (camera framing, accepted by Dan). In the vertical crop, take the window that gives the most room above his hair.
* The ending sells the app; a short ends on its own tactic, not that pitch.

## Deliver
`Short-form video content/fasting-short<N>_<title>.mp4` (1080x1920) + stamps, and a `fasting-SHORTS.md` listing each short's in/out, title and parent. Send Dan the REVIEW copies (and copies in `Videos to Review/` for anything 45 s or longer). Update `00-MASTER.md`.

## Starter prompts
**Claude (Opus 5.5, high):**
> Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/SL-16-intermittent-fasting-shorts.md`: propose the shorts segments from the RO-08 Intermittent Fasting master and wait for my picks, then cut them with /shorts in Soft Blue Light, with gates and an independent audit (no covers). Deliver, send me the review copies, update the master list. Name this session "Intermittent Fasting SFC R1".

**Codex (GPT-6 Sol, high):**
> Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table), then execute `Handoffs/video-editing/SL-16-intermittent-fasting-shorts.md` using `.claude/skills/shorts/SKILL.md` as the method: propose segments from the RO-08 master, wait for Dan's picks, cut, gate, deliver, update `00-MASTER.md`. Name this task "Intermittent Fasting SFC R1".
