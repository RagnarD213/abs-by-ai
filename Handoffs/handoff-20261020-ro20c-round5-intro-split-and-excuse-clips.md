# CONTENT, long-form: What To Buy For Your Health LFC R5

Written 2026-10-20 by Claude (Opus 5.5) at the end of round 4. Sidebar name: **What To Buy For Your Health LFC R5**.
Video: "What To Buy For Your Health At Every Income Level" (RO-20C), part 3 of the three-video "Invest In Your Health" split.
Videos 1 and 2 (RO-20, RO-20B) were finalized by Dan on 2026-10-20 and are NOT part of this task (their setup is
`handoff-20261020-ro20-ro20b-thumbnails-and-video-setup.md`).

**Recommended model:** Codex `gpt-6.1-sol`, high effort (VIDEO-RULES 2026-10-20: Sol high is the default for every video edit and new round).
**Use the Codex subscription to generate the images** (`.claude/skills/_shared/codex-image.sh --model gpt-6.1-sol --effort high`).
AI motion: Google Flow subscription first (VIDEO-RULES 2026-10-17); paid Replicate Veo only if Dan says rush.

## Why a fresh task

New AI frame pairs, a new full-screen graphic, two lip-synced clips, a rebuild and the full gate/judge chain: a heavy round,
and the R4 task had already been compacted once. The Claude R4 task could not start, pin or unpin a task itself (no
supported start-session tool in that Claude session), so its pin stays until Dan opens this one.

## Dan's exact words (2026-10-20)

> For video 3, for the intro graphic, I want to keep this idea. I want a top title graphic that says, "What to buy for your
> health at the top of this full-screen graphic at every income level." Basically, the same text, but larger, or just however
> you think best, at the top as a title graphic. Three-way AI-generated clip split screen:
> * Dead broke: For all of them, it should be me looking ripped and shirtless in these clips. Dead broke: I am homeless, and I
>   am doing kettlebell deadlifts in front of my cardboard box on Skid Row.
> * Middle class: I'm in a suburban house with a delicious and premium-looking cooked salmon meal on the kitchen island.
> * Over 10,000 a month: I am in a baller luxury home gym with a hot girl who's super fit behind me, in the frame.
>
> Give me starting frames for a new intro clip for video 3, "What to buy for your health," and then mock up that full-screen
> graphic, what it looks like with the clips inside it too.
>
> Okay, at 1:47, I want to start in M frames for a new AI clip of an overweight guy in a middle-class house with a bunch of hot
> dogs, French fries, and junk food in front of him, saying this as I talk. Try to lip-sync him so it matches what I'm saying in
> the clip.
>
> At 4:12, I want another similar AI-generated clip of a different guy in a different house with different junk food in front of
> him, lip-synced to match what I'm saying in the excuse-making voice.
>
> Okay, videos 1 and 2 are finalized. Proceed to the next round of edits for video 3.

("start in M frames" is dictation for "start and end frames".) Everything else in the R4 film is approved as delivered. Dan did
not answer round 4's decision 2 (the 4:18 "go and review that stuff that we went over before" sentence): the recommended
default stands, the sentence stays.

## Base film (never edit it; build R5 as a new master)

- R4 master: `/Volumes/Extreme/_edit_work/ro20/round4/v3/MASTER.mp4`, sha256 starting `843a735f293f` (full hash in
  `round4/v3/MASTER.mp4.deliver_gate.json`), 29:40.9, 53,374 frames, 1920x1080 at 30000/1001. Same bytes as
  `Videos to Review/Invest In Your Health LFC R4 - video 3 full film.mp4` and the delivery folder
  `claude edited long form content/20 - What To Buy For Your Health At Every Income Level/`.
- Its build: `/Volumes/Extreme/_edit_work/ro20/recipe/films_r4.py` (layout `VIDEOS["v3"]`, every in-memory fix numbered in its
  comments), `splice_r4.py` (re-renders only changed keyframe windows of a film part, stream-copies the rest; pass an absolute
  `SPLICE_DIR`), `finish_r4.py` (words, SRT, chapters, plan.json), `chain_r4_picture.sh` / `chain_r4_post.sh`,
  `negscan_r4.py` + `negscan_record.py`, `page_state_r4.py` / `finalize_page_r4.py` / `page6_20.py` (review page),
  `deliver_r4.sh`. Repo copy and the R4 lessons: `.claude/skills/longform-edit/reference/ro20/` and its README "Round 4" section.
- Copy the recipe for round 5 (or add a `v3r5` layout) rather than editing what built the finalized videos 1 and 2.

## The three changes

1. **Intro graphic, 0:00 to about 0:07 (pickup P4).** Today it is the locked three-levels card (`cards20.levels_card`, drawn in
   `pickups20.py` P4): small "WHAT TO BUY FOR YOUR HEALTH / At Every Income Level" title top left and three photo tiles that
   arrive on "dead broke", "middle class", "making over $10,000 a month" (P4 words: `round3/pickups/words_P4.json`, cues
   `P4.mp4.cues.json`; the voice is untouched and locked by `round3b/round3b-hashes.sha256`). New version: a large top title
   ("What To Buy For Your Health" / "At Every Income Level", best layout) over a three-way split of AI clips, each tile arriving
   on its tier word, tier labels kept (Dead Broke, Middle Class, Over $10,000 A Month). New graphics are Soft Blue Light
   HyperFrames with real motion for their whole screen time (AGENTS 2026-10-17). In all three clips Dan is ripped and shirtless:
   - Dead broke: homeless Dan doing kettlebell deadlifts in front of his cardboard box on Skid Row. The film already has an
     approved AI clip of a cardboard-box man swinging a kettlebell (A3, about 0:29; frames and prompts under `round3/` and
     `round3-plan/`): reuse its world, but this one must be Dan, shirtless, deadlifting.
   - Middle class: Dan in a suburban house kitchen with a delicious, premium-looking cooked salmon meal on the island.
   - Over $10,000 a month: Dan in a baller luxury home gym, a very fit attractive woman behind him in frame.
2. **1:47.4 to 1:53.5, excuse voice:** "I can't afford healthy food, Dan. If I only had money like you, I could afford to eat
   healthy, but I can't, so there's nothing I can do." (words 107.4 to 113.5 s on the R4 master). AI clip of an overweight man in
   a middle-class house with hot dogs, French fries and junk food in front of him, lips synced to Dan's own recording. Dan is on
   camera there today; lower third Gd34 ends at 1:47.8, so start the clip after it or end the label on the cut.
3. **4:12.3 to 4:16.0, excuse voice:** "Oh, Dan, I don't have the money for $30 a pound on salmon every week." (252.3 to 256.0 s).
   A different man in a different house with different junk food, lip-synced the same way. Dan is on camera there today (stock
   Ce06, seafood platter, ends at 4:09).

Film-time mapping: video time t in part 3 is film frame `43483 + (t - 47.614) * 29.97` (1:47.4 = film 1510.67 s;
4:12.3 = film 1655.57 s). Read it from `round4/v3/layout.json`, never typed times.

## Method (approved, reuse it)

- Excuse-voice clips: VIDEO-RULES "The excuse voice gets a lip-synced AI clip, frames first" and "A lip sync that fails its check
  once goes in without lip sync". Approved method: `longform-edit/reference/ro06/README.md` round 4; RO-20's own scripts
  `recipe/gen_motion20.py`, `lipsync20.py` (sync/lipsync-2-pro on Replicate, about $0.083 per second, untreated voice slot),
  `lipmeasure20.py`. Motion takes now come from Google Flow via the `flow-veo` agent (Claude) or `_shared/veo/FLOW-RUNBOOK.md`
  (Codex), queued with `_shared/veo/veo.py add`. Round 1's approved "fat guy who has money" lip sync is the quality bar.
- Frames: start and end frame per clip, made by Codex; frame gate `_shared/framecheck/gate.py` plus a fresh frame-reviewer per
  pair before Dan sees them; AI-GENERATED label on every clip; no belly close-ups or fat pinching (VIDEO-RULES 2026-10-04);
  shirtless Dan reads ripped; the woman is in gym wear; nothing that makes no physical sense.
- Dan's likeness: the approved Dan reference frames used for this film's AI clips and RO-06's (see `round3-plan/decisions.json`).

## This round's deliverable, then STOP

A review page (`_shared/review_server.py`; port 8868 is RO-20's, reuse it and keep the R4 page as `index-r4.html`) with:
- the three intro clips' start and end frames (gated and reviewed),
- the full-screen intro graphic mocked up with those frames inside it (a still, plus a short moving HyperFrames preview if cheap),
- the two excuse clips' start and end frames, with the line each one covers and its time,
- "What I decided".
No motion, lip sync or film build until Dan approves the frames and the mockup.

## After approval

Motion (Flow), lip sync, gates per clip, a new P4 picture (the voice stays the locked P4 voice), splice the two excuse clips in
with partial renders, full post chain, delivery gate, a fresh watch judge, negative-events scan record for the new hash, the
later-round revision list with timestamps (VIDEO-RULES 2026-10-10), VLC copy in `Videos to Review/`.

## Known, not to reopen

- Hair top touches the frame edge on most of roll C1511: a source limit flagged since round 1 (gate rows `framing:hair_top`,
  `headroom`). VIDEO-RULES 2026-10-20 (head and hair clearance) says to flag it, which every round did; no crop can restore it.
- Gate rows explained in `round4/v3/notes-RO20C-round4.md` (voice 4 tone row, coverage, burned-captions false positive, card
  collision, splice visibility, heartbeat-on-black stock, the mattress false match, the sign-off repeat). Never raise a bound.
- Two builds at a time across all sessions (`_shared/buildcap.py`). Never play audio aloud from a review panel.
- No upload or setup for RO-20C in this task.

## Feedback from Dan on video 1, for this and every video

A stumbled or half-restarted word inside a kept take (video 1 at about 0:33, "priority") is junk to fix: cut to a clean take or
trim it. Rule: VIDEO-RULES "Stumbles inside a kept take get fixed" (2026-10-20). Check RO-20C's build for the same kind of thing.

## Starter prompt

> CONTENT (LFC). Name this task `What To Buy For Your Health LFC R5`. Read `Handoffs/video-editing/00-RULES.md`, then execute
> `Handoffs/handoff-20261020-ro20c-round5-intro-split-and-excuse-clips.md`: round 5 of "What To Buy For Your Health At Every
> Income Level" (RO-20C). Use the Codex subscription to generate the images. Make the start and end frames for the three intro
> clips, the full-screen intro graphic mockup with them inside it, and the start and end frames for the two lip-synced excuse
> clips at 1:47 and 4:12, then stop for my approval. Recommended: Codex gpt-6.1-sol, high effort.
