# CONTENT, SFL: What To Buy Shorts (SL-22, from RO-20C)

**CONTENT, long-form (LFC): it gets Shorts cut from it and nothing else.** List 2 · shorts from a finished long-form.
Added 2026-10-21 at the RO-20C setup. Read `00-RULES.md` first. Task name: **`What To Buy SFL R1`**.

## Start condition
Dan approved the complete RO-20C round 6 film "What To Buy For Your Health At Every Income Level" on 2026-10-21 ("All changes look good. Let's proceed to set up. This is finalized and approved."). Cut from the exact approved master
`claude edited long form content/20 - What To Buy For Your Health At Every Income Level/What To Buy For Your Health At Every Income Level | claude round 6 | 16x9 | RO-20C.mp4`,
SHA-256 `933e5af24171b53a2abd81a7ed75d7328f65498f4b54301c32e68e0070fd22fd`. Do not cut from a review copy or the raw roll.
RO-20C releases on YouTube **Sun Dec 6, 2026, 9 AM Chicago** (`Docs/LONGFORM_RELEASE_CALENDAR.md`).

## Deadlines (Dan's calendars, 2026-10-17)
Three Shorts, Dan's rule of 3 per new long-form (best three moments):

| Short | Airs | Edited, approved and set up by |
|---|---|---|
| 1 | **Fri Jan 15, 2027, 9 AM Chicago** (moved 2026-10-27: Mon Dec 7 went to an already edited Intermittent Fasting Short; see `Docs/SHORTS_RELEASE_CALENDAR.md`) | **Thu Jan 14, 2027**, with at least 10 days of editing time |
| 2 | next free Mon/Tue/Fri/Sat Shorts slot after Short 1 | set at its setup |
| 3 | next free slot after Short 2 | set at its setup |

## First step: propose segments, then wait for Dan's picks
Offer standalone lessons with verbatim speech, exact in/out times from the approved master and a reason to watch
(memory `shorts-reason-to-watch`). Chapters: 0:00 What To Buy For Your Health At Every Income Level, 0:27 If You're Dead Broke, 2:57 Middle Class: The Best Protein, 5:36 A Better Mattress, 8:54 A Membership At The Best Gym, 10:54 A Sleep Tracker, 12:18 GLP-1 Medication, 15:04 TRT, 16:13 Supplements, 18:38 Over $10,000 A Month: A Home Gym, 21:14 A Meal Prep Service Or A Personal Chef, 22:52 A Maid And A Laundry Service, 23:31 A Personal Trainer And Nutritionist, 25:07 Beyond The List, 26:47 Summary, 28:36 Your First Step.
Strong candidates: the under-$100 home workout setup even if you're homeless, salmon vs a 401k contribution, the gym with the most ripped people (not the best equipment), GLP-1s paying for themselves, the big three supplements, and "rich guys who say they're too busy but do their own laundry".
Recommend the strongest three and which one is Short 1. A Short must open as its own video: never on "number two",
"the next thing", "you middle class guys" or a reference back to the series. Trim to a clean opening, or propose pickup
wording in the shortlist (pickups are recorded on the studio set at a shoot, so a Short that needs one waits).

## How to cut them
* `/shorts` (Claude) or its `SKILL.md` as the method (Codex). Soft Blue Light graphics built from the HyperFrames
  templates, word-timed captions, land-then-hold vertical framing, cuts snapped to silence, 45-60 s, 1080x1920.
* Reuse the film's approved inserts, AI clips and graphics; keep every AI-GENERATED chip and set `ai_generated: true`
  at setup for any Short that keeps realistic AI footage. Keep the film's approved audio.
* No full-film vertical or square. No covers here: covers and Blotato setup are the separate setup step. Do not upload
  or queue. No Short posts before RO-20C is public.

## Deliver
`Short-form video content/whattobuy-short<N>_<title>.mp4` + stamps and `whattobuy-SHORTS.md` (in/out, title, parent).
Send Dan the review copies (and copies in `Videos to Review/`), gates and an independent audit. Update `00-MASTER.md`.
Next after approval: the setup task makes the covers with Codex and queues Short 1 for Fri Jan 15, 2027, 9 AM Chicago (or the waiting
list if Blotato is full).

## Starter prompts
**Claude (Opus 5.5, high):**
> CONTENT (SFL). Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/SL-22-what-to-buy-shorts.md`: confirm the approved RO-20C master, propose the Shorts segments and wait for my picks, then cut three Shorts with /shorts in Soft Blue Light, with gates and an independent audit (no covers, no upload). Short 1 airs Fri Jan 15, 2027. Name this session "What To Buy SFL R1".

**Codex (GPT-6.1 Sol, high):**
> Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table), then execute `Handoffs/video-editing/SL-22-what-to-buy-shorts.md` using `.claude/skills/shorts/SKILL.md` as the method: confirm the approved RO-20C master, propose segments, wait for Dan's picks, cut three Shorts, gate, deliver, update `00-MASTER.md`. Name this task "What To Buy SFL R1".
