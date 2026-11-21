# CONTENT, SFL: What To Cut Shorts (SL-21, from RO-20B)

**CONTENT, long-form (LFC): it gets Shorts cut from it and nothing else.** List 2 · shorts from a finished long-form.
Added 2026-10-20 at the RO-20B setup. Read `00-RULES.md` first. Task name: **`What To Cut SFL R1`**.

## Start condition
Dan approved the complete RO-20B round 4 film "What To Cut To Afford Getting In Shape" on 2026-10-20 ("Two looks good. That is finalized"). Cut from the exact approved master
`claude edited long form content/19 - What To Cut To Afford Getting In Shape/What To Cut To Afford Getting In Shape | claude round 4 | 16x9 | RO-20B.mp4`,
SHA-256 `88a6314f43424b28312dacdc1775b73ae7d17c8bf45212f6ffdc2bfccd86dec1`. Do not cut from a review copy or the raw roll.
RO-20B releases on YouTube **Sun Nov 29, 2026, 9 AM Chicago** (`Docs/LONGFORM_RELEASE_CALENDAR.md`).

## Deadlines (Dan's calendars, 2026-10-17)
Three Shorts, Dan's rule of 3 per new long-form (best three moments):

| Short | Airs | Edited, approved and set up by |
|---|---|---|
| 1 | **Mon Nov 30, 9 AM Chicago** (the day after RO-20B; took "Love Handles 1"'s slot) | **Sun Nov 29**, with at least 10 days of editing time |
| 2 | next free Mon/Tue/Fri/Sat Shorts slot after Short 1 | set at its setup |
| 3 | next free slot after Short 2 | set at its setup |

## First step: propose segments, then wait for Dan's picks
Offer standalone lessons with verbatim speech, exact in/out times from the approved master and a reason to watch
(memory `shorts-reason-to-watch`). Chapters: 0:00 You're Being Too Cheap With Your Health, 0:26 The "I'm Broke" Excuse, 0:58 3 Things You Should Never Cut, 1:58 What To Sacrifice, 2:31 Bars And Clubs, 4:00 Eating At Restaurants, 5:34 Junk Food In The House, 6:10 Vacations, 7:21 Therapy And Psychiatric Medication, 8:37 Subscriptions, Car Payments And Clothes, 9:02 What's Next. Strong candidates: the "I'm broke" excuse (you do have the money), bars and clubs ($100 to $300 a week), restaurants don't care about your fitness goals, "you deserve a break once you're ripped" (vacations), and the controversial therapy and medication take.
Recommend the strongest three and which one is Short 1. A Short must open as its own video: never on "number two",
"the next thing" or a reference back to the series. Trim to a clean opening, or propose pickup wording in the shortlist
(pickups are recorded on the studio set at a shoot, so a Short that needs one waits).

## How to cut them
* `/shorts` (Claude) or its `SKILL.md` as the method (Codex). Soft Blue Light graphics built from the HyperFrames
  templates, word-timed captions, land-then-hold vertical framing, cuts snapped to silence, 45-60 s, 1080x1920.
* Reuse the film's approved inserts, AI clips and graphics; keep every AI-GENERATED chip and set `ai_generated: true`
  at setup for any Short that keeps realistic AI footage (the film has five). Keep the film's approved audio.
* No full-film vertical or square. No covers here: covers and Blotato setup are the separate setup step. Do not upload
  or queue. No Short posts before RO-20B is public.

## Deliver
`Short-form video content/whattocut-short<N>_<title>.mp4` + stamps and `whattocut-SHORTS.md` (in/out, title, parent).
Send Dan the review copies (and copies in `Videos to Review/`), gates and an independent audit. Update `00-MASTER.md`.
Next after approval: the setup task makes the covers with Codex and queues Short 1 for Mon Nov 30, 9 AM Chicago (or the waiting
list if Blotato is full).

## Starter prompts
**Claude (Opus 5.5, high):**
> CONTENT (SFL). Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/SL-21-what-to-cut-shorts.md`: confirm the approved RO-20B master, propose the Shorts segments and wait for my picks, then cut three Shorts with /shorts in Soft Blue Light, with gates and an independent audit (no covers, no upload). Short 1 airs Mon Nov 30. Name this session "What To Cut SFL R1".

**Codex (GPT-6.1 Sol, high):**
> Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table), then execute `Handoffs/video-editing/SL-21-what-to-cut-shorts.md` using `.claude/skills/shorts/SKILL.md` as the method: confirm the approved RO-20B master, propose segments, wait for Dan's picks, cut three Shorts, gate, deliver, update `00-MASTER.md`. Name this task "What To Cut SFL R1".
