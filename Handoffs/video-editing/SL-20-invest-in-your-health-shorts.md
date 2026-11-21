# CONTENT, SFL: Invest In Your Health Shorts (SL-20, from RO-20)

**CONTENT, long-form (LFC): it gets Shorts cut from it and nothing else.** List 2 · shorts from a finished long-form.
Added 2026-10-20 at the RO-20 setup. Read `00-RULES.md` first. Task name: **`Invest In Your Health SFL R1`**.

## Start condition
Dan approved the complete RO-20 round 4 film "Why You Should Invest More In Your Health" on 2026-10-20 ("video one looks good. This is finalized"). Cut from the exact approved master
`claude edited long form content/18 - Why You Should Invest More In Your Health/Why You Should Invest More In Your Health | claude round 4 | 16x9 | RO-20.mp4`,
SHA-256 `41e0949adf44fb111a20825c9f5ea12715212ecde5058698cb3775cdd1705c92`. Do not cut from a review copy or the raw roll.
RO-20 releases on YouTube **Sun Nov 22, 2026, 9 AM Chicago** (`Docs/LONGFORM_RELEASE_CALENDAR.md`).

## Deadlines (Dan's calendars, 2026-10-17)
Three Shorts, Dan's rule of 3 per new long-form (best three moments):

| Short | Airs | Edited, approved and set up by |
|---|---|---|
| 1 | **Mon Nov 23, 9 AM Chicago** (the day after RO-20; took "Body Fat % 1"'s slot) | **Sun Nov 22**, with at least 10 days of editing time |
| 2 | next free Mon/Tue/Fri/Sat Shorts slot after Short 1 | set at its setup |
| 3 | next free slot after Short 2 | set at its setup |

## First step: propose segments, then wait for Dan's picks
Offer standalone lessons with verbatim speech, exact in/out times from the approved master and a reason to watch
(memory `shorts-reason-to-watch`). Chapters: 0:00 Reason 1: The Halo Effect, 1:39 How Your Weight Changes Your Relationship, 3:09 Online Dating, 4:41 Reason 2: You Get More Done, 6:03 Gym Time Or Doctor's Office Time, 7:37 Reason 3: Better Mental Health, 8:59 Reason 4: Bad Health Is Ludicrously Expensive, 11:48 Money Does You No Good If You're Dead, 14:58 What's Next. Strong candidates: the halo effect (people judge your brains and personality by your looks), online dating is winner take all on looks, gym time or doctor's office time, the diabetic millionaire (toe amputation, eye injections, ambulance rides), and "money does you no good if you're dead" (the family that sued each other over the inheritance).
Recommend the strongest three and which one is Short 1. A Short must open as its own video: never on "number two",
"the next thing" or a reference back to the series. Trim to a clean opening, or propose pickup wording in the shortlist
(pickups are recorded on the studio set at a shoot, so a Short that needs one waits).

## How to cut them
* `/shorts` (Claude) or its `SKILL.md` as the method (Codex). Soft Blue Light graphics built from the HyperFrames
  templates, word-timed captions, land-then-hold vertical framing, cuts snapped to silence, 45-60 s, 1080x1920.
* Reuse the film's approved inserts, AI clips and graphics; keep every AI-GENERATED chip and set `ai_generated: true`
  at setup for any Short that keeps realistic AI footage (the film has eleven). Keep the film's approved audio.
* No full-film vertical or square. No covers here: covers and Blotato setup are the separate setup step. Do not upload
  or queue. No Short posts before RO-20 is public.

## Deliver
`Short-form video content/invest-short<N>_<title>.mp4` + stamps and `invest-SHORTS.md` (in/out, title, parent).
Send Dan the review copies (and copies in `Videos to Review/`), gates and an independent audit. Update `00-MASTER.md`.
Next after approval: the setup task makes the covers with Codex and queues Short 1 for Mon Nov 23, 9 AM Chicago (or the waiting
list if Blotato is full).

## Starter prompts
**Claude (Opus 5.5, high):**
> CONTENT (SFL). Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/SL-20-invest-in-your-health-shorts.md`: confirm the approved RO-20 master, propose the Shorts segments and wait for my picks, then cut three Shorts with /shorts in Soft Blue Light, with gates and an independent audit (no covers, no upload). Short 1 airs Mon Nov 23. Name this session "Invest In Your Health SFL R1".

**Codex (GPT-6.1 Sol, high):**
> Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table), then execute `Handoffs/video-editing/SL-20-invest-in-your-health-shorts.md` using `.claude/skills/shorts/SKILL.md` as the method: confirm the approved RO-20 master, propose segments, wait for Dan's picks, cut three Shorts, gate, deliver, update `00-MASTER.md`. Name this task "Invest In Your Health SFL R1".
