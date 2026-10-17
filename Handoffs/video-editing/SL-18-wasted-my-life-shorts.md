# CONTENT, SFL: I'm 41 Wasted My Life Shorts (SL-18, from RO-25)

**CONTENT, long-form (LFC): it gets Shorts cut from it and nothing else.** List 2 · shorts from a finished long-form.
Added 2026-10-17 from the approved Shorts calendar (`Docs/SHORTS_RELEASE_CALENDAR.md`). Read `00-RULES.md` first.
Task name: **`I'm 41 Wasted Life SFL R1`**.

## Start condition
Start only after Dan approves the complete RO-25 film (R7 or later; see the latest RO-25 entry in `Handoffs/README.md`).
Cut from that exact approved master and record its path and SHA-256 here when you start. Do not cut from a review
candidate, a round folder preview or the raw roll.

## Deadlines (Dan's calendar, 2026-10-17)
Three Shorts, Dan's rule of 3 per new long-form (best three moments):

| Short | Airs | Edited, approved and set up by |
|---|---|---|
| 1 | **Mon Oct 26, 9 AM Chicago** (day after RO-26; RO-25 releases Sun Oct 18) | **Sat Oct 24.** Deliver review copies by Wed Oct 21 so Dan can review and the setup task can make covers |
| 2 | Sat Dec 12 | Dec 11 |
| 3 | Tue Dec 15 | Dec 14 |

Build all three in this round (one segment pick, one review). Short 1 is the priority if time runs short.

## First step: propose segments, then wait for Dan's picks
Offer standalone lessons with verbatim speech, exact in/out times from the approved master and a reason to watch
(memory `shorts-reason-to-watch`). The film is six regrets; each is a candidate Short:
1. Taking Adderall and other ADHD medication (the productivity graph his mentor drew)
2. Sacrificing health for money (sleep deprivation, stimulants)
3. Not taking sleep seriously
4. Settling for low-quality women in his 20s
5. Not looksmaxing earlier
6. Believing in AI but not acting on it

Recommend which three are strongest and which one should be Short 1. A Short must open as its own video: never on
"number one", "my third regret" or a reference back to the film. Trim to a clean opening, or propose pickup wording
in the shortlist (pickups are recorded on the studio set at a shoot, so a Short that needs one waits). Tone is somber
and serious, as Dan set for the film. Swearing stays (memory `swearing-never-cut-never-ask`).

## How to cut them
* `/shorts` (Claude) or its `SKILL.md` as the method (Codex). Soft Blue Light graphics built from the HyperFrames
  templates, word-timed captions, land-then-hold vertical framing, cuts snapped to silence, 45-60 s, 1080x1920.
* Reuse the film's approved inserts, AI clips and graphics; keep every AI-GENERATED chip and set `ai_generated: true`
  at setup for any Short that keeps realistic AI footage. Real photos keep the real-photo label (current wording in
  `.claude/skills/_shared/VIDEO-RULES.md`). Before and after pairs stay the same person.
* Studio set, 10/15 shoot: the lav clips on loud words; keep the film's approved audio, do not re-process it.
* No full-film vertical or square. No covers here: covers and Blotato setup are the separate setup step. Do not upload
  or queue. No Short posts before RO-25 is public.

## Deliver
`Short-form video content/wastedlife-short<N>_<title>.mp4` + stamps and `wastedlife-SHORTS.md` (in/out, title, parent).
Send Dan the review copies (and copies in `Videos to Review/`), gates and an independent audit. Update `00-MASTER.md`.
Next after approval: the setup task makes the covers with Codex and queues Short 1 for Mon Oct 26 9 AM, Shorts 2 and 3
for Dec 12 and Dec 15 (or the waiting list if Blotato is full).

## Starter prompts
**Claude (Opus 5.5, high):**
> Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/video-editing/SL-18-wasted-my-life-shorts.md`: confirm the RO-25 film is approved and record its master, propose the Shorts segments from the six regrets and wait for my picks, then cut three Shorts with /shorts in Soft Blue Light, with gates and an independent audit (no covers, no upload). Short 1 airs Mon Oct 26. Name this session "I'm 41 Wasted Life SFL R1".

**Codex (GPT-6 Sol, high):**
> Read `Handoffs/video-editing/00-RULES.md` (Codex column + environment table), then execute `Handoffs/video-editing/SL-18-wasted-my-life-shorts.md` using `.claude/skills/shorts/SKILL.md` as the method: confirm the approved RO-25 master, propose segments, wait for Dan's picks, cut three Shorts, gate, deliver, update `00-MASTER.md`. Name this task "I'm 41 Wasted Life SFL R1".
