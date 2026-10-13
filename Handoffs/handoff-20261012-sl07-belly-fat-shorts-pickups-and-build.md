CONTENT | SL-07 | If I Had Belly Fat SFC R1

> **2026-10-13, Dan: pickups are recorded on the studio set at the shoot, not on the desk mic.** After hearing the desk-mic pickups in the RO-20 first minutes: "that audio doesn't work... I'm just going to record these pickups on my studio set instead... get all of the pickups that we need for this task and every other outstanding video edit". This job's pickup lines are on the shoot list (`Docs/PICKUPS_1017_SHOOT.md`, the PICKUPS section of the shoot doc, and the pickups teleprompter document). Do not ask him to read them into the desk mic again; build the pickup shorts when the shoot roll is uploaded. Desk takes are timing placeholders only.


# SL-07: record Dan's two pickups, then build five "If I Had Belly Fat" shorts (round 1)

Written 2026-10-12 by Claude (Opus 5.5) at the end of the segment-selection session. Dan picked five segments from a
shortlist of seven, as shortlisted, with no changes. Nothing is cut yet. This task records his two pickup lines, shows
him the round-1 review page, and builds the batch.

**Recommended: Claude Opus 5.5, high effort.** (Shorts from a long-form are a Claude secondary cut; the build will be watched.)

## Goal

Five vertical Shorts (1080x1920) from the RO-16 long-form "If I Had Belly Fat, Here's How I'd Lose It In 90 Days", each
one point, each opening like a dedicated video. Deliver review copies to Dan. No covers, no upload, no queue. The parent
goes public Sun Nov 1 2026, 9 AM CT; no short posts before it is verified public.

## Read first

1. `Handoffs/video-editing/00-RULES.md` and `.claude/skills/_shared/VIDEO-RULES.md` in full. The ones this batch leans on:
   "A Short opens like a dedicated video: record a pickup" (10-11), "More AI clip ideas, funny ones" (10-11), "All B-roll
   is colour corrected" (10-11), "The first 5 seconds get the most effort" (10-08), "Round 1 always reviews every graphic,
   stock item and clip" (10-08), "Review videos also go in Videos to Review/" (10-08), "No fat pinching or belly close-ups"
   (10-04), "Capital letters in graphics" (10-09), "A person looking at a phone is not a picture" (10-11).
2. `.claude/skills/shorts/SKILL.md`, then `.claude/skills/shorts/reference/softblue-sl03/README.md` (the batch renderer for
   a Soft Blue shorts batch from our own long-form, with every lesson from eight review passes). Start from it in a new
   work folder `/Volumes/Extreme/_edit_work/sl07/`.
3. `Handoffs/handoff-20261011-sl06-zepbound-shorts-pickups-and-build.md` and whatever SL-06 has delivered by then
   (`/Volumes/Extreme/_edit_work/sl06/`, `Short-form video content/zepbound-tips-SHORTS.md`): it is the first batch that
   recorded and joined pickups. Reuse its recording and join method and whatever Dan said about how the pickups sounded.
4. `Short-form video content/belly-fat-90-days-SHORTS.md` (the batch record: pieces, the film's audio joins inside each
   piece, which film graphics and clips sit in each range).

## Source

- Master: `claude edited long form content/09 - If I Had Belly Fat, Here's How I'd Lose It In 90 Days/If I Had Belly Fat, Here's How I'd Lose It In 90 Days | claude round 3 | 16x9 | RO-16.mp4`
  (12:09.33, sha256 `c535ab4cfe881fc95796c9f5a191535c87aa2d2bb61d3588a4f850da02643b09`). The 218-cue `.srt` and
  `.chapters.txt` are beside it, with `notes-RO16.md` and `recipe-RO-16/`.
- Build files: `/Volumes/Extreme/_edit_work/ro16/`. `words_out.json` = every word with film time (`t0`, `t1`) and raw-roll
  time (`src0`, `src1`); `edl.json` + `piece_map.json` = the 38 audio pieces (raw in/out and film in/out); `shots.json` =
  43 shots with framing names (W2 wide, T2 tight; W4 inside cards); `plan_resolved.json` = every graphic and clip with
  film times and sources; `round3/RO16_MASTER.mp4` = the master; `round3/RO16_MASTER.mp4.untreated.wav` and `lav.wav` =
  dry voice for silence snapping; `round3/base.mp4` = picture with graphics baked in (do not cut from it).
- Raw roll: `/Volumes/Extreme/dan rose fitness 9:23 shoot - vsls, long form content, short form content/C1710.MP4`
  (9/23 shoot, FX30 S-Cinetone, one dual-mono lav; read-only). Crop windows and the grade are in the recipe
  (`recipe-RO-16/build.py`, `frames.py`, `softblue.py`) and `look/` in the build folder. Cut from the RAW roll through the
  film's edit map with its grade, as SL-03 did.
- Check whether the film mix carries a music bed before planning the pickup joins (`notes-RO16.md` mentions none; confirm
  by listening to a pause in the master against the untreated wav).
- Do not run anything inside `/Volumes/Extreme/_edit_work/ro16/`. Copy what you need.

## The five shorts (Dan's picks, 2026-10-12: "let's do A, B, D, E, and F")

Film times, measured on `words_out.json`. Snap every cut to measured silence on the dry voice; ear-check each piece
opening in context (SL-03 round 2 lesson). `/` marks a join that needs a size step or a clip.

| | Title (working) | Opens with | Film pieces | Length |
|---|---|---|---|---|
| A | Stop Trying To Lose 1 Pound A Week | film line | 0:40.8 - 1:07.5 / 1:18.4 - 1:43.5 | 52 s |
| B | Weigh Yourself Every Morning | **pickup B** | 9:47.8 - 10:36.4 | 49 s + pickup |
| D | Work Out Every Morning, Not 3 Times A Week | **pickup D** | 4:59.6 - 5:35.6, 5:35.8 - 5:53.2 | 53 s + pickup |
| E | The 3-Pound Rule That Keeps Belly Fat Off | film line | 10:42.8 - 10:55.1 / 10:55.8 - 11:25.2 | 42 s |
| F | Track Your Calories With A Photo | film line | 7:21.1 - 8:08.4 | 47 s |

Not picked: G (take time off work) and H (how Zepbound makes fat loss easier). Left out as duplicates: the meal prep
service (same point as the DS-28 Meal Prep dedicated short) and the protein step (same as SL-06 short F).

Spoken text of each, as sent to Dan:

- **A:** "Most fitness channels tell you to make small, sustainable changes and to lose 1 pound a week. In my opinion,
  that advice is bullshit, and that is the reason why most of the people following it are still fat. Let's say you have
  30 pounds to lose and you are losing 1 pound a week. That is going to take you seven months and in my opinion almost
  nobody can stay motivated for that long. It's far, far easier to go all-in for 90 days and get it over with. / Most
  people are trying to squeeze fat loss into their life. They work all day, they drive home, then they take care of their
  family, and then they try to work out and eat healthy with whatever time and energy is left over. And there usually
  isn't any left over, so it never happens. So if I was 30 pounds overweight, I would do it the opposite way. I would make
  losing fat the number one priority in my life for 90 days, and everything else would have to fit around that."
- **B:** [pickup] "Weigh yourself every morning, right after you use the bathroom and before you eat or drink anything.
  Same scale, same time, every day, even on vacation. No exceptions. You have to do this because it's the only way to
  know if the plan is working. In one study, the people who weighed themselves every day lost about 13 pounds more over
  six months than the people who didn't. Now, your weight is going to bounce around 2 or 3 pounds from day to day, just
  from water and salt. So don't freak out about any one day. What you want to look at is your 7 day moving average for
  the week, compared to your average for the week before. If my weekly average was dropping about 2 pounds or more, I
  wouldn't change anything. But let's say it stalled out for a full week. I would cut 200 calories a day and keep going.
  Most guys never adjust anything. They just keep doing the same thing for months and hope the scale is going to move."
- **D:** [pickup] "Most guys do it the opposite way. They go to the gym two or three times a week for an hour and a half.
  They get really sore, then something comes up at work and they miss a day, and within a month they're not going at all.
  Short daily workouts are far better than occasional long workouts because when you're working out every day, you don't
  have to think about it. You're not waking up and asking yourself, is today a gym day or not? You just get up and you do
  it, even on weekends, even on vacation. And if all you can do at first is 10 or 15 minutes, that's fine. You can
  consistently do a 15 minute workout every day. The hour and a half workouts are the ones that end up getting skipped.
  So why first thing in the morning? Let me tell you why. At 8 in the morning, nobody is calling you, your boss doesn't
  need anything from you yet, and your kids are asleep. By 6 at night you're tired, something came up at work, and that's
  when the workout ends up getting skipped. I work out every morning, 7 days a week, and that's the reason why."
  (The hormones and sleep line that follows in the film is left off for length.)
- **E:** "Maintaining your weight is far, far easier than losing weight. And once you have your abs, you can eat more, you
  can have a drink on the weekend, and you can relax a little bit. You can't do that when you're trying to lose two and a
  half pounds a week. / So how does somebody end up 30 pounds overweight in the first place? It's because they're not
  weighing themselves. If you're not weighing yourself, you're going to gain 5 pounds, gain 10 pounds, gain 20 pounds
  before you even realize it. So here's what I would do. I would keep weighing myself every day. And if I ever got more
  than 3 pounds above my goal weight, I would go right back to cutting calories until it's gone. Losing 3 pounds is not a
  big deal. You could do that in a week or two. Losing 30 pounds is 90 days of sacrifice." (Stops before the Zepbound
  microdose lines on purpose: the SL-06 batch covers them.)
- **F:** "If you never look at your bank account, you're probably going to be poor. Same thing applies to your calories.
  Now, before AI, I was always against tracking calories. The old way where you weigh your food on a scale and look up
  every ingredient, that was way too much work for normal people like me and you. But with AI, everything has changed.
  Now you just take a picture of your food and you get the calories, the protein, the carbs, and the fat in a few
  seconds. It's not perfect, but it's reasonably accurate and it's far, far better than not tracking at all. And if
  you're eating the meal prep meals, you just take a picture of the label. We have a free macro tracker for this at
  AbsByAI.com. Just take a picture of your food and it adds up your day for you. Try ours out or use any other AI calorie
  tracking app you like. Once you start tracking, you'll be shocked at how much faster you start losing fat."

## The pickups

Drafted through `dan-voice-writer` on 10-12 (three clean calls, wording unchanged). Dan was sent all three options for
each and did not choose; he records option 1 unless he prefers an alternate. Each is said in about 3 to 4 seconds.

| | Record this (option 1) | Alternates | The film line that follows |
|---|---|---|---|
| B | **Here's how to know if your fat loss plan is working.** | 2. Stop guessing and judge your diet by your seven day average. 3. If your weight is stuck, this is for you. | "Weigh yourself every morning, right after you use the bathroom and before you eat or drink anything." |
| D | **Here's why you should work out every single morning.** | 2. Do a short workout every morning, seven days a week. 3. If you can't stay consistent, work out at 8 AM every day. | "Most guys do it the opposite way." |

D's film line says "the opposite way", so the pickup must name the thing it is the opposite of: options 1 and 2 do.
A, E and F open on a film line that already reads as a dedicated opening. If one reads as mid-thought once it is cut,
offer Dan a pickup for it on the review page; do not add one unasked.

### Recording them (first thing in the task, while Dan is at the desk)

Follow the method in the SL-06 handoff, "Recording them": Yeti through ffmpeg avfoundation (confirm the device index),
one background take of about 60 seconds with each line read two or three times, B then D, at the film's pace. If macOS
refuses the mic, ask for a Voice Memo dropped in the chat. Transcribe, pick the best take of each, fit the pickup's voice
toward the FILM's voice on this roll, match loudness to the line that follows, 15 ms de-click at the join. The film's
approved mix after the join is cut only (`audio_gate.py --verbatim`); declare the pickup span to the gate the way SL-06
did, and never change a bound. Say on the review page how the pickup was treated. If SL-06 found the Yeti reads as a
different room next to the film, tell Dan before recording and let him choose the lav instead.

## Opening picture (first 5 seconds) and AI clip ideas

Dan asked for more funny AI clip ideas than feel safe, with about a third expected to be turned down. Bring all of
these to round 1 as start and end frames (9:16, made with `.claude/skills/_shared/codex-image.sh`); motion only for the
ones he approves. Each has a no-AI fallback so a "no" never blocks a short. Search the clip library again first.

| | 0:00 to about 0:04 | Fallback | More frame pairs to offer |
|---|---|---|---|
| A | AI gag: a snail crawls across a bathroom scale whose needle barely moves (under "small, sustainable changes and lose 1 pound a week") | Dan on camera, tight window, title up | "Seven months": a wall calendar whose pages fly off while a man on a treadmill barely moves. "Squeeze fat loss into their life": a man tries to cram a kettlebell into an overstuffed briefcase (the film's traffic stock and AI kitchen dad A0063 are the straight option) |
| B | Under the pickup: a man steps onto a bathroom scale first thing in the morning (the film's C20 stock, `stock/p7555158.mp4`; use a different scale shot at 9:47 in the same short, or library B0376 if it is not used in SL-06 E the same week) | same | "Bounce around 2 or 3 pounds": a scale whose needle swings like a metronome while a man stares, deadpan. "Hope the scale is going to move": a man kneels and prays to his scale |
| D | Under the pickup: Dan's real ab wheel rollout (B0030), graded | same | Excuse-voice style gag for "is today a gym day or not?": a man in bed flips a coin, it lands on its edge. "Something comes up at work": a phone buzzes itself off a gym bench |
| E | AI gag: a man pulls a dusty, cobwebbed scale out from under the bed (under "Maintaining your weight is far, far easier") | Dan on camera | "Gain 5, gain 10, gain 20 before you even realize it": a shirt button pops off and knocks over a coffee cup, framed chest up, no stomach in shot. "A drink on the weekend": a lean man at a patio raises one beer, relaxed (straight) |
| F | AI gag: a moth flies out of an empty wallet (under "If you never look at your bank account, you're probably going to be poor") | Dan on camera | "Weigh your food on a scale and look up every ingredient": a man at a kitchen counter buried in measuring cups, a food scale and a thick binder. The app itself is the real phone demo, never AI |

Rules on every one: no belly framing or hands on the body, heavier people shown whole, clothed and doing something; AI
chip off faces and bodies; never a cutaway of someone just looking at a phone; colour correct every B-roll clip to the
film's look; no stock clip twice inside one short; register approved new clips in the clip library.

## Standing decisions for this batch (told to Dan on 10-12; he did not overrule them)

- Look: the Soft Blue shorts standard he approved on SL-03 (title band y 0 to 310 for the whole short, two steady
  windows, two-line HyperFrames key-point bar, captions under it, B-roll filling the picture area). No look round.
- One review page after the pickups: the first short finished, the AI frame pairs, "What I decided", then every title,
  bar, card and clip of all five as stills on real frames, three per row.
- The film's graphics are rebuilt for vertical, never sliced: the seven-months point (A, G04 as a key-point bar); the
  study card (B, G18), the 7-day average scene (B, G19) and the weekly check list as the bottom card (B, G20: "Down 2+ lb:
  change NOTHING", "Stalled a week: CUT 200 cal"); the phone beside Dan for the tracker (F, P01, clip B0038); the 3-pound
  point (E, G21 as a key-point bar). Title case; full caps only where a word truly carries the punch.
- Key points distil, they do not echo: write each bar as `KEY POINT:` plus the point, two lines, landing on its words.
- No covers, no upload, nothing queued. Captions print "abs" lower case, "AI" upper case, and keep his swearing.
- `ai_generated: true` at setup for any short that carries an AI clip (A if A0063 or a new opener is in; any short that
  takes one of the gags above).
- Generation budget: $5 per short including frames and retries.
- F overlaps a passage in the Calories long-form; `SL-08` has been told to skip its "track with AI" candidate.
- Posting order to suggest at setup: F, B, A, D, E. B and E (both about weighing) at least a week apart.

## Order of work

1. Rename the task "If I Had Belly Fat SFC R1". The job is already `in_progress` on the queue; check
   `python3 scripts/edit-queue/queue.py pending` and mirror anything waiting
   (`.claude/skills/_shared/edit-queue/README.md`). The board is at its 2,500-word cap: an ACTIVE entry has to fit in
   the words freed by deleting this handoff's line from the HANDOFFS section.
2. Record the two pickups while Dan is there.
3. Round-1 review page (`_shared/PRE-RENDER-APPROVAL.md` layout, `review_server.py`, a port no other review uses). Finish
   B first: one continuous passage plus a pickup and three rebuilt graphics, so it proves the join and the cards. Copy
   it to `Videos to Review/` as `If I Had Belly Fat SFC R1 - short B - Weigh Yourself Every Morning.mp4`.
4. After his notes: generate motion for the approved frames, build the other four, run
   `_shared/deliver/gate.py --format short` and the watch pass on each delivered file, then a fresh `ra-reviewer` audit
   that is not shown your notes. Expect "does not ship" once.
5. Deliver: `Short-form video content/belly-fat-90-days-short<N>_<title>.mp4` + stamps, REVIEW 540p copies, the audio A/B
   clip, `notes-*.md`, `recipe-*/`, and update `belly-fat-90-days-SHORTS.md`. `queue.py set SL-07 delivered`. List the
   five shorts that need covers (a separate task). Copies of each finished short go in `Videos to Review/`.

## Risks

- **Two shorts end on a film audio join**, where the film mix trims the last word's tail: A ends on "that." (film
  103.54) and F on "fat." (488.44). Listen first. Fallback ends inside a take: A can end on "...the number one priority
  in my life for 90 days" only if that cuts cleanly, else drop the last clause; F can end on "Try ours out or use any
  other AI calorie tracking app you like." (8:04.4).
- A's first piece ends on "with." (67.54), which runs straight into "Number one". Check its tail and cut before "Number".
- Film audio joins inside the pieces (a word there may only run straight on): A 85.22, 89.76; B 601.36, 608.12, 615.72,
  625.36, 630.30; D 335.62, 349.90; E 658.63; F 470.76, 480.72.
- B is one locked-camera passage with five film joins: each needs a real size step (about 1.25x displayed face change)
  or a clip, and two same-size joins in a row need a cutaway. The three rebuilt graphics cover most of it.
- A's first 27 seconds have no cutaway in the film (its `style:static_run` row failed there). In the short, the opener
  gag, the seven-months bar and one size step have to carry it.
- E is 42 s, 3 s under the 45 s floor. Dan saw the length and picked it. Do not pad it.
- The Yeti in the office will not sound like the lav in the studio. If the fitted pickup still reads as a different room
  next to the film line, say so on the review page and let Dan hear it.
- Two builds at most on the machine. Check before every render.

## Starter prompt

> Name this task "If I Had Belly Fat SFC R1". This is CONTENT. Read `Handoffs/handoff-20261012-sl07-belly-fat-shorts-pickups-and-build.md` and execute it: record my two pickup lines into the Yeti first, then show me the round-1 review page with short B finished, the AI frame pairs, and every graphic and clip as stills, then build the five Belly Fat shorts with /shorts in Soft Blue Light, gates and an independent audit. Use the Codex subscription to generate the images. No covers, no upload.
