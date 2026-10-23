# CONTENT, SFL: Not Losing Weight Shorts (SL-23, from RO-14)

**CONTENT, long-form (LFC): it gets Shorts cut from it and nothing else.** List 2 · shorts from a finished long-form.
Added 2026-10-22 at the RO-14 setup. Read `00-RULES.md` first. Task name: **`Not Losing Weight SFL R1`**.

## Start condition
Dan approved the complete RO-14 round 3 film "Why You're Not Losing Weight" on 2026-10-22 ("Okay, everything looks good. This is approved."). Cut from the exact approved master
`claude edited long form content/22 - Why You're Not Losing Weight/Why You're Not Losing Weight | claude round 3 | 16x9 | RO-14.mp4`,
SHA-256 `14f2a85da15f80b10f2594eec3bb1ecfc29a4d030886e597e0bfb503a8e07e3c`. Do not cut from a review copy or the raw roll.
RO-14 releases on YouTube **Sun Jan 3, 2027, 9 AM Chicago** as "Why You're Not Losing Weight (4 Hidden Calorie Leaks)" (`Docs/LONGFORM_RELEASE_CALENDAR.md`).
Not to be confused with RO-10 "Calories: The Reason You're Not Losing Weight" and its Shorts (SL-08).

## Deadlines (Dan's calendars, 2026-10-17)
Three Shorts, Dan's rule of 3 per new long-form (best three moments):

| Short | Airs | Edited, approved and set up by |
|---|---|---|
| 1 | **Mon Jan 4, 2027, 9 AM Chicago** (the day after RO-14) | **Sun Jan 3**, with at least 10 days of editing time |
| 2 | next free Mon/Tue/Fri/Sat Shorts slot after Short 1 | set at its setup |
| 3 | next free slot after Short 2 | set at its setup |

## First step: propose segments, then wait for Dan's picks
Offer standalone lessons with verbatim speech, exact in/out times from the approved master and a reason to watch
(memory `shorts-reason-to-watch`). Chapters: 0:00 Why The Scale Won't Move, 0:29 The Uncomfortable Truth, 1:03 4 Calorie Leaks, 3:18 The Hidden Reasons, 6:23 My Simple System.
Strong candidates: "a fat girlfriend or a fat wife" (the most controversial moment), invisible calories (a tablespoon of olive oil is 120 calories; 400 invisible calories a day is 40 pounds a year), weekend blowouts erasing the weekday deficit, liquid calories ("if it has calories in it, do not drink it"), fat friends, and the 5-step system.
Recommend the strongest three and which one is Short 1. A Short must open as its own video: never on "leak number two",
"reason number one" or a reference back to the list. Trim to a clean opening, or propose pickup
wording in the shortlist (pickups are recorded on the studio set at a shoot, so a Short that needs one waits).

## How to cut them
* `/shorts` (Claude) or its `SKILL.md` as the method (Codex). Soft Blue Light graphics built from the HyperFrames
  templates, word-timed captions, land-then-hold vertical framing, cuts snapped to silence, 45-60 s, 1080x1920.
* Reuse the film's approved inserts, AI clips and graphics; keep every AI-GENERATED chip and set `ai_generated: true`
  at setup for any Short that keeps realistic AI footage. Keep the film's approved audio.
* No full-film vertical or square. No covers here: covers and Blotato setup are the separate setup step. Do not upload
  or queue. No Short posts before RO-14 is public.

## Deliver
`Short-form video content/notlosingweight-short<N>_<title>.mp4` + stamps and `notlosingweight-SHORTS.md` (in/out, title, parent).
Send Dan the review copies (and copies in `Videos to Review/`), gates and an independent audit. Update `00-MASTER.md`.
Next after approval: the setup task makes the covers with Codex and queues Short 1 for Mon Jan 4, 2027, 9 AM Chicago (or the waiting
list if Blotato is full).

## Starter prompts
**Claude (Opus 5.5, high):**
> CONTENT (SFL). Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/SL-23-not-losing-weight-shorts.md`: confirm the approved RO-14 master, propose the Shorts segments and wait for my picks, then cut three Shorts with /shorts in Soft Blue Light, with gates and an independent audit (no covers, no upload). Short 1 airs Mon Jan 4, 2027. Name this session "Not Losing Weight SFL R1".

**Codex (GPT-6.1 Sol, high):**
> Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table), then execute `Handoffs/video-editing/SL-23-not-losing-weight-shorts.md` using `.claude/skills/shorts/SKILL.md` as the method: confirm the approved RO-14 master, propose segments, wait for Dan's picks, cut three Shorts, gate, deliver, update `00-MASTER.md`. Name this task "Not Losing Weight SFL R1".
