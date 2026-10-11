**EXECUTED 2026-10-11. Do not fire. Next round: `handoff-20261011-ro20-round3-pickups-and-first-minutes.md`.**

# RO-20 "Why You Should Invest More In Your Health": round 2, now THREE videos, one task

**CONTENT (LFC), organic long-form, 16:9, three videos cut from one roll. Sidebar name: `Invest In Your Health LFC R2`.**
Written 2026-10-11 by the round 1 session (Claude Opus 5.5) after Dan reviewed round 1. This replaces the earlier version of
this file. One task edits all three videos (Dan: "edit all three videos together in one single task").

## Goal

Dan reviewed the round 1 page and decided to split the 53 minute cut into three videos, tied together with AUDIO PICKUPS he
will record. This task (1) writes those pickup scripts and plans what is on screen under each, (2) applies his round 1
revisions, (3) builds and delivers the three videos on the round method. Nothing is fully rendered yet.

## Read first

1. `Handoffs/video-editing/00-RULES.md`, then `.claude/skills/_shared/VIDEO-RULES.md` (two new sections dated 2026-10-11 at
   the top: all B-roll colour corrected; never clip B0437, no "person looking at a phone" cutaways) and `PRE-RENDER-APPROVAL.md`.
2. `.claude/skills/longform-edit/reference/ro20/README.md` (recipe, order, traps). Working recipe: `/Volumes/Extreme/_edit_work/ro20/recipe/`.
3. `/Volumes/Extreme/_edit_work/ro20/round2-plan/decisions.json`: Dan's answers word for word, hashes, what is locked.
   Re-hash against `round1/round1-hashes.sha256` before touching anything.
4. `cut_transcript.md`, `take_map_notes.md` in the work dir. Round 1 page: http://127.0.0.1:8862/ (`round1/`, do not overwrite;
   build in `round2/` on a new port).

## The three videos (film times are on the round 1 cut; shot joins at 894.29, 904.74 and 1420.79 s)

| | working title | from the round 1 cut | est. length |
|---|---|---|---|
| 1 | Why You Should Invest More In Your Health | 0:00 to 15:00.2 (through "You need to be spending more money on your health."), then pickup P1, then the OTHER closing take | about 16 min |
| 2 | What To Cut To Afford Getting In Shape | pickup P2, then 15:04.8 ("But I know at this point in the video...") to 23:40.7 ("...once you're there in a couple months."), then pickup P3 | about 10 min |
| 3 | What To Buy For Your Health At Every Income Level | pickup P4, then 23:40.8 ("All right. So let me walk you through it...") to the end (summary and the closing take already in the cut) | about 30 min |

- Dropped from all three: "So, I'll be telling you exactly what you should be spending that money on in a minute." (15:00.2 to
  15:04.4). It is false in a three-way split.
- Video 1's sign-off is the roll's other complete closing take (C1511 about 3974 to 4046 s, "Alright guys, that's today's
  video. If you wanna take the first step to getting in shape, go to absbyai.com ... I'll see you next time."; it has two
  internal restarts near 3991 and 4023 s to cut by the take rule). Video 3 keeps the take already in the cut. Video 2 has no
  on-camera sign-off: P3 carries a short spoken close over the approved app demo.
- The second half never refers back to the four reasons (checked). Video 3's summary recaps the cuts and the buys, which is fine.
- Titles are working titles for file names; the real titles come at `/video-setup`. Re-cut the chapter list per video.
- Edit queue: keep `RO-20` for video 1 and add `RO-20B`, `RO-20C` (`queue.py add`, see `_shared/edit-queue/README.md`). Each
  video is its own Sunday release and has its own $5 AI budget.

## Audio pickups: write them first, they block the three openings and endings

Dan: "write scripts for audio pickups that I will do where it's necessary for the video to make sense. For example: at the end
of video 1, I could do a pickup and say, 'In the next video, I'm going to tell you what you should cut.' I could do a pickup
at the beginning and end the video too. At the beginning of video 3..." and "Plan for the graphics that would be on screen:
graphics, stock, or AI-generated clips, or what's going to be on screen when I do that pickup."

Minimum set (add one only where a video would not make sense without it; keep each short):

| id | where | job of the lines | lead-in / lead-out in the footage |
|---|---|---|---|
| P1 | end of video 1, before the sign-off | tease video 2 (what to cut to find the money, even if you are broke) and video 3 (what to buy at every income level) | after "...You need to be spending more money on your health."; before "Alright guys, that's today's video." |
| P2 | start of video 2 | the premise in about 20 s for someone who never saw video 1 (you are being too cheap with your health; part 1 explains why), then what this video covers | must flow into "But I know at this point in the video a lot of y'all guys are thinking, oh well damn that's easy for you to say, you have money. But I am a brokie..." |
| P3 | end of video 2 | wrap, tease video 3, and a short call to action (go to AbsByAI.com, see yourself with abs, free) | after "...you'll be so glad you did once you're there in a couple months." |
| P4 | start of video 3 | the premise in about 15 s, a one-line nod to video 2 (where the money comes from), what this video covers: every level, dead broke to baller | must flow into "All right. So let me walk you through it. I'll walk you through every level..." |

- **Voice:** these go out in Dan's voice. Write a content plan per pickup, then draft with the `dan-voice-writer` agent
  (`/dan-voice`). Blunt, plain words, his phrases ("y'all guys", "brokies", "ballers"); read each against the real sentences
  either side of it. No em dashes. For the hook lines, his own summary is the model ("You are being too cheap with your
  health, and your cheapness and wasting money on bullshit is literally killing you").
- **Deliver the scripts to Dan before anything else:** a Google Doc he can read from (one heading per pickup, the lines, the
  footage sentence before and after for his ear) plus the same text in chat. Recording note, in plain steps: the same lav he
  wore on the shoot if he has it, otherwise his phone close to his mouth in a quiet soft room; one file per pickup named
  `P1` to `P4`, two takes each, dropped in `Media/longform-raw/ro20-pickups/`. Then keep working on everything that does not
  need the audio.
- **On-screen plan, shown with the scripts:** a pickup is audio only, so NOTHING on camera can sit under it. For every
  pickup, list second by second what is on screen: clips from that video's own best cutaways moved forward (allowed opener
  option), a Soft Blue Light title card naming the three parts with the current one marked, library clips, new stock, or a
  new AI clip (frames first). P3's call to action sits under the approved self-generation demo
  (`/Volumes/Extreme/_edit_work/ro06/round5/phone/P01-softblue.mp4`). Videos 2 and 3 therefore open on pictures, not on
  camera: plan their first 5 seconds as their own piece (VIDEO-RULES, 2026-10-08). No source used twice inside one video.
- **When the audio arrives:** pick the take, match its level and tone to the film voice (`build.VOICE4` is the film's
  voice; a pickup from another room needs its own gentle EQ match, checked by ear and by the audio gate rows), set the
  joins on the envelope, and re-check the picture plan against the real lengths.

## Dan's round 1 revisions (all in `decisions.json`)

- **Locked:** colour D for both sizes; voice 4 (warm, less room echo); frames A1 (lip synced), A2, A3; the chapters.
- **Opening of video 1:** no AI opener ("Just use a camera scene for the intro"). Remove O1; open on camera.
- **Remove A4** (the lawyer). He stays on camera there.
- **Ca02 (with lower third Ga04) and Ca03:** replace BOTH with two new AI clips: "a guy in great shape getting a job while
  the fat guy looks on in envy... Not the same scene, maybe in a boardroom." Frames to Dan first. Ca02's slot is 9.2 s: trim
  it to 8 s or less. (Editor's reading of "CA03 instead of CA02 and GA04": the lower third stays, the pictures change. Say so
  on the page so he can correct it.)
- **Cb11 + Gb08:** never B0437 again (marked rejected in the library). Use the earlier AI dating-app clip `A0089` (9:16
  phone-screen mock: no matches, then lots of matches) in the approved phone shell on the Soft Blue field, labelled AI-GENERATED.
- **Cb12 + Gb09:** remove the stock clip. Build a full-screen Soft Blue Light graphic around Dan's diagram
  (`round1/dan-dating-diagram.png`: ten women, ten men, every arrow pointing at the top few men) "with text next to it to fill
  out the graphic" (the line is "winner take all... the bottom 80% are getting nothing"). Show him the still.
- **Colour correct ALL B-roll** (new standing rule). He flagged B0455 (Cb24), B0456 (Cc22) and B0434 (Cf16) as "excessively
  dark"; grade all 30 clips of his own footage against the presenter frames and look at each still beside one. Swap to an
  already bright clip where a grade cannot rescue one.
- **Not answered, stay as built unless he says:** 38:18 "you can't afford it" twice; Bryan Johnson name-only lower third;
  the app phone card (not built); photos of his own things.

## Order of work

1. Pickup scripts + on-screen plans to Dan (above). Re-run the cut as three EDLs (three work sub-folders or three plan
   filters; the cut itself is applied, do not re-tighten pauses).
2. Plan edits for the revisions; `resolve_part.py`, `resolve.py`, **`preflight20.py`** after every resolve; re-render only
   changed lower thirds (`from_plan.py --render --only`).
3. AI: motion for A1, A2, A3 (`gen_motion.py`, Veo 3.1 Fast $0.10/s; A1 8 s plus the RO-06 lip sync, A2 and A3 6 s);
   frames for the two new job clips, then stop for his approval before their motion.
4. Round 2 page (new port): only what changed or is new, each as a still with its context clip: the pickup plans, the two
   new frame pairs, the diagram graphic, the dating-app phone card, before/after stills of the regraded B-roll, the
   finished AI motion in context.
5. With pickups and approvals in: the first minute of EACH video (copies to `Videos to Review/`), then, when nothing is
   pending, the three full films: quiet music bed (the RO-06 / RO-07 bed, level on the audio gate's floor row), SRT, chapters,
   edit sheet, delivery gate, watch pass, one independent `ra-reviewer` per film. `roll_sidecar.py mark-used`. Later rounds
   list each change with timestamps.

## Status of checks, stated honestly

- Audio gate on the round 1 first minute: 12 of 13 rows; the tone row fails by design with voice 4 (as on RO-07). Not tuned.
- Delivery gate, watch pass, independent review: not run (no finished film).
- Hair: the camera clipped the top of his hair for most of the roll; both sizes keep the camera's top row. Dan was told.
- `preflight20.py` is clean except three clips with 0.13 s spare (Cb23, Ce23, Cf11 second shot).

## Cost ledger

Spent: $0.00 generation (12 Codex pictures on the subscription), under $0.50 Gemini listening. Cap: $5.00 per video, three
videos. Planned: video 1 A1 $1.45 + two job clips about $1.20; video 2 A2 $0.60; video 3 A3 $0.60; plus whatever the
pickup pictures need. Ask before any video passes $5.00.

## Recommended model and effort

Claude Opus 5.5, high: scripts in his voice, editorial planning for three openings, and a long build.

## Starter prompt

```
Read `Handoffs/video-editing/00-RULES.md`, then execute `Handoffs/handoff-20261011-ro20-round2-after-dan-review.md`: round 2 of "Why You Should Invest More In Your Health" (LFC, content), now split into three videos edited together in this one task. First write the audio pickup scripts I will record (in my voice) and plan what is on screen under each pickup, and give me those. Then apply my round 1 revisions, generate the AI motion I approved, and show me only what changed or is new. Build each video's first minute, then the full films, only when nothing is pending. Name this session "Invest In Your Health LFC R2".
```
