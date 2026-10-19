# CONTENT, SFL: 3 Healthy Foods Shorts (SL-19, from RO-17)

**CONTENT, long-form (LFC): it gets Shorts cut from it and nothing else.** List 2 · shorts from a finished long-form.
Added 2026-10-18 at the RO-17 setup. Read `00-RULES.md` first. Task name: **`3 Healthy Foods SFL R1`**.

## Start condition
Dan approved the complete RO-17 round 5 film on 2026-10-18 ("final"). Cut from the exact approved master
`claude edited long form content/17 - 3 Healthy Foods That Made Me Fat/3 Healthy Foods That Made Me Fat | claude round 5 | 16x9 | RO-17.mp4`,
SHA-256 `62187e39d262a9ce36902ebf02d12533ab08f8af651fe84f825a13de98ef3fad`. Do not cut from a review copy or the raw roll.
RO-17 releases on YouTube **Sun Dec 13, 2026, 9 AM Chicago** (it took RO-22's Sunday, per `Docs/LONGFORM_RELEASE_CALENDAR.md`).

## Deadlines (Dan's calendars, 2026-10-17)
Three Shorts, Dan's rule of 3 per new long-form (best three moments):

| Short | Airs | Edited, approved and set up by |
|---|---|---|
| 1 | **Mon Dec 14, 9 AM Chicago** (the day after RO-17; took "Face 1"'s slot) | **Sun Dec 13**, with at least 10 days of editing time |
| 2 | 2027, with the other carried-over second Shorts | set at its setup |
| 3 | 2027 | set at its setup |

## First step: propose segments, then wait for Dan's picks
Offer standalone lessons with verbatim speech, exact in/out times from the approved master and a reason to watch
(memory `shorts-reason-to-watch`). Chapters: 0:00 intro, 0:45 Trail Mix, 2:19 Dried Fruit, 3:33 Coconut Water,
5:16 What I snack on instead, 7:15 recap. Each food is a candidate Short, and so is the snack swap (sardines, eggs,
rotisserie chicken, Chipotle protein cup). Recommend the strongest three and which one is Short 1. A Short must open as
its own video: never on "food number two", "the third one" or a reference back to the film. Trim to a clean opening, or
propose pickup wording in the shortlist (pickups are recorded on the studio set at a shoot, so a Short that needs one waits).

## How to cut them
* `/shorts` (Claude) or its `SKILL.md` as the method (Codex). Soft Blue Light graphics built from the HyperFrames
  templates, word-timed captions, land-then-hold vertical framing, cuts snapped to silence, 45-60 s, 1080x1920.
* Reuse the film's approved inserts, AI clips and graphics; keep every AI-GENERATED chip and set `ai_generated: true`
  at setup for any Short that keeps realistic AI footage (the film has eight). Keep the film's approved audio.
* No full-film vertical or square. No covers here: covers and Blotato setup are the separate setup step. Do not upload
  or queue. No Short posts before RO-17 is public.

## Deliver
`Short-form video content/healthyfoods-short<N>_<title>.mp4` + stamps and `healthyfoods-SHORTS.md` (in/out, title, parent).
Send Dan the review copies (and copies in `Videos to Review/`), gates and an independent audit. Update `00-MASTER.md`.
Next after approval: the setup task makes the covers with Codex and queues Short 1 for Mon Dec 14 9 AM (or the waiting
list if Blotato is full).

## Starter prompts
**Claude (Opus 5.5, high):**
> CONTENT (SFL). Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/SL-19-3-healthy-foods-shorts.md`: confirm the approved RO-17 master, propose the Shorts segments and wait for my picks, then cut three Shorts with /shorts in Soft Blue Light, with gates and an independent audit (no covers, no upload). Short 1 airs Mon Dec 14. Name this session "3 Healthy Foods SFL R1".

**Codex (GPT-6 Sol, high):**
> Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table), then execute `Handoffs/video-editing/SL-19-3-healthy-foods-shorts.md` using `.claude/skills/shorts/SKILL.md` as the method: confirm the approved RO-17 master, propose segments, wait for Dan's picks, cut three Shorts, gate, deliver, update `00-MASTER.md`. Name this task "3 Healthy Foods SFL R1".
