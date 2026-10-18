# Oura Ring Review SFL R2: build Shorts A, H, I, J, K (SL-09)

**CONTENT: Shorts extracted from the long-form "My Honest Oura Ring Review After 1.5 Years" (Zeeshan Video 4). SFL.**
Task name: **`Oura Ring Review SFL R2`**. Model: **Opus 5.5, high**. Written 2026-10-18 by `Oura Ring Review SFL R1`.

## Goal
Cut the five Shorts Dan picked from Zeeshan's finished master, in the Soft Blue shorts standard with HyperFrames motion,
show every graphic, clip and opener on a round-1 review page, run every gate and an independent audit on each delivered
file, deliver review copies to Dan. No covers, no upload, no queueing.

## Dan's decision (verbatim, 2026-10-18)
A shortlist of eleven (A to K) went out on 2026-10-15 with full transcripts (my recommendation was A, B, C, E, I).
Dan: *"Okay, let's do A, H, I, J, and K."*
- Build exactly those five (rule: execute his picks as given). The shorts calendar plans only **Oura 1** in 2026
  (**Fri Nov 13, 9 AM Chicago**, due Nov 12; the long-form now releases **Wed Nov 11**, `Docs/LONGFORM_RELEASE_CALENDAR.md`).
  The other four carry over to 2027 slots at setup. Say that in one line at delivery; do not drop any.
- Recommended order (Shorts-feed data favours training/food rules first): **short1 = A, short2 = I, short3 = H,
  short4 = K, short5 = J.** Dan can reorder at setup.
- **None needs a pickup line.** A, I, J, K open on film words that stand alone; H opens on a line moved up from the end
  of its own passage (below). Nothing waits for a shoot.

## Source
`Zeeshan Content Videos/my honest oura ring review - video 4/my honest oura ring review | zeeshan | 16x9 | video 4.mp4`
(Zeeshan Rev 3, Dan finalized as is; MD5 `5264285762af41f2a6644366e0bae7eb`, verified 2026-10-18; 1920x1080,
**29.97 fps** (30000/1001), AAC 48 kHz stereo 320k, 1187.5 s). Copies on `/Volumes/Extreme/Zeeshan Content Videos/...`
and Drive. The `.srt` beside it is Zeeshan's (errors: "the ordering" = "the Oura Ring"; casing of WHOOP). No recipe or
word file exists: get word timestamps yourself (zeeshan-master: Whisper words, then `ctc_source.py` re-timing).
- **His mix ships untouched** (`--verbatim`, cut at seams only, 15 ms de-click fades, AAC 320k). Check for a music bed
  first; if there is one, snap with voice-band VAD (`scored-source/work/vad.py`), not `silencedetect`.
- **Colour:** decode BT.709. **Colour and voice options (2026-10-16 first-round rule) do not apply:** Zeeshan's grade and
  mix are Dan-finalized and carried verbatim (editor-audio rule). Say so in one line on the page.
- Work folder: `/Volumes/Extreme/_edit_work/sl09/` (only `recon/` exists: 2 s frame grabs, ten 2-minute contact
  sheets `sheet_0..9.jpg`, full-res stills). Build in `sl09/round2/`.

## Zeeshan's burned graphics (measured 2026-10-18 on full-res frames)
- **Lower thirds** (navy, blue edge, "DRAWBACK #4" eyebrow): on a NEAR shot at 11:23.5 the box spans **x 90-1830,
  y 770-1016**, i.e. the whole width, so any full-height window slices it. Handle each one whole or absent (zeeshan-master
  README: a short window above the band, or an inset card; pills fade 0.5-0.8 s longer than a colour scan says). Their
  text becomes our own HyperFrames key-point bar where it distills a point (title case, never echo the speech).
- **Verdict list card** (J, 17:46-18:31): top-left, **x 70-624**, grows downward to about y 770 as items add. A 724 px
  window centred on Dan (~x 1000) clears it by only ~14 px: measure the card's shadow and use a window that leaves it out whole.
- **Sleep-score card** (I, 16:47.5-17:03.5): full-frame designed graphic ("MY OURA SLEEP SCORE / Toxic Relationship",
  Dan's real chart on the left, text on the right). It is a card in the vertical, full source height; consider the
  chart side only as a taller card (crop width, never height).

## The five Shorts (master times; measure exact silences and word ends before cutting)
**A. "Train Harder After A Bad Night's Sleep"** 11:21.6 - 12:18.5 (57 s), one piece.
- Opens "The Oura Ring, when you get a bad night of sleep, it gives you advice like better be careful today..." ends
  "...just make sure you're doing low risk workouts so that way you don't get injured." Swearing stays.
- In range: lower third 11:22-11:27 ("The Oura Ring Tells You To SLACK OFF After Bad Sleep. That's Wrong!"); NEAR
  shot 11:36-11:48. No B-roll at all: **share 0%, add at least 18 s of clips at the plan step.**
- Clip ideas: Dan doing a low-risk lift over "low risk workouts" / "go harder today" (real library B-roll, actively
  doing it, colour matched); a clean/Olympic lift as the high-risk move he says to take easy on (stock, clearly the
  "avoid" beat); a tired man waking up over "bad night of sleep" (the film's AI bed clips at 0:24 and 6:38, or stock at
  2:22 / 7:54, re-checked against today's sense rules). If an Oura app screen in the film (6:58-7:18) shows readiness
  advice, it fits "it gives you advice like"; check before using.

**H. "Cut The Adrenaline Before Bed"** about 57 s, two pieces, reordered:
1. 16:16.6 - 16:25.0 "There might be something that you're doing that's spiking your heart rate and your adrenaline near
   your bedtime that you don't really expect right now could be affecting your sleep." (opener; check its first word is clean)
2. 15:27.6 - 16:16.0 "Driving fast, late at night, near bedtime. Now, I used to have a girlfriend..." to "...my sleep has
   gotten a lot better as a result of cutting out that fast driving."
- The join between 1 and 2 needs a real framing change or a clip over it.
- **Replace Zeeshan's AI Tesla clip 15:45.5-15:53.5** (speedometer reads up to 190 while Dan says 120; job doc rule).
  Library or Pexels night driving first; a new AI clip only through frames approval and the Flow subscription
  (`flow-veo` agent). Keep the real daytime Tesla footage 16:03.5-16:13 over "Full Self-Driving".
- Lower thirds in range: 15:58-16:02 and 16:18-16:22. B-roll share ~30% with the two Tesla pieces: add one more clip.

**I. "Your Sleep Score Shows Who's Toxic In Your Life"** 16:28.8 - 17:16.0 + 17:36.0 - 17:45.5 (about 56 s).
- Opens "Here was the most valuable and the most unexpected benefit of getting the Oura Ring for me" (drop the leading
  "And"). Cut 17:16-17:36 ("Nobody is worth sacrificing your health for ... especially late at night?"). Ends "...either
  need to change their behavior or they need to go."
- Sleep-score card 16:47.5-17:03.5 (above). Lower third 16:38-16:41. B-roll ~29%: add one clip (a couple arguing,
  shown whole and clothed; stock first).

**J. "Oura Ring Or WHOOP? Which One To Buy"** 17:46.4 - 18:33.0 (47 s), one piece.
- Opens "Should you buy the Oura Ring?" (drop "So the overall verdict,"), ends "...there's no subscription and the cost is low."
- Verdict card throughout (above). Rebuild the two advantage lists as our own moving Soft Blue comparison (a real
  list, so a larger layout is justified) and show the things he names (Oura ring on the finger, WHOOP, Apple Watch).
  B-roll ~0%: plan the comparison scene plus clips to reach 30%.

**K. "You're Not Sleeping As Well As You Think"** 3:15.0 - 3:57.5 (42 s), one piece.
- Opens "You watching this video right now are probably where I was a few years ago" (drop "So the bottom line is"),
  ends "...even if it is not the Oura Ring."
- Lower third 3:32-3:37 ("A Tracker Shows You The Problem AND WHAT'S CAUSING IT"); NEAR shots 3:16-3:27, 3:48-3:57.
  B-roll 0%: clips that show what he names: stepping on a scale ("never weighing yourself to weighing yourself every
  day"; library `B0376` is a scale stock), a drink, late-night eating, a stressed man.

## How (rules on record)
- Method: `/shorts` skill. Start from **`.claude/skills/shorts/reference/zeeshan-master/`** (editor's master: audio,
  windows, his graphics, CTC captions) **plus `softblue-sl07/`** (Soft Blue renderer, key-point bars, B-roll share,
  `deliver.py plan` lessons). Soft Blue shorts standard (GRAPHICS-STANDARDS.md): title band y 0-310 whole short,
  picture 1080x1610, land-then-hold framing (`cut/landing.py`), key-point bars at 68,1130-1012,1378, captions from y 1412.
- **Every graphic moves for its whole screen time** in Soft Blue HyperFrames (VIDEO-RULES 2026-10-17). Title case.
- **First 5 seconds** of each short: write down what is on screen, try to beat it (library clip, the strongest picture
  from the same short, or 2-3 new AI opener ideas as START/END frames through `framecheck/gate.py` and a `frame-reviewer`).
- **Round 1 page shows every graphic, clip and photo in context** (3-5 s around it, the shared context player). Deliver
  the **whole shorts** this round where every item is an existing approved or library asset; any new AI clip appears as
  frames for approval with a placeholder, and its motion waits for his OK.
- AI motion only through the Google Flow subscription (`flow-veo` agent, background). Paid Replicate only if Dan says rush.
- Hair never leaves the frame; Zeeshan's wides put the hair near source row 0, so windows start at row 0.
- Real photos (if any) say "Real photo of me, not AI-generated" (2026-10-17 wording). AI clips keep AI-GENERATED; set
  `ai_generated: true` at setup for any short that has one.
- Gates on each delivered file: `audio_gate.py --verbatim`, `watch.py` + fresh judge, `deliver/gate.py --format short`
  (through `rungate.sh`), then a fresh `ra-reviewer` per short (the three AI-clip sense questions for any AI clip).
  `buildcap.py` before every render. Review-panel testing stays muted.

## Deliver
- `Short-form video content/oura-short<N>_<title-slug>.mp4` (1080x1920) + stamps, REVIEW 540p copies, and
  `Short-form video content/oura-SHORTS.md` (each short's in/out, title, parent Video 4, order, airing note).
- Copies in `Videos to Review/` named `Oura Ring Review SFL R2 - short N - <title>.mp4`; review page via
  `python3 .claude/skills/_shared/review_server.py PORT DIR` (pick a free port), byte-range check before sending.
- `python3 scripts/edit-queue/queue.py set SL-09 delivered --by Claude`, mirror to the Edit Queue artifact
  (`ArtifactData set`, pin `if_version`, then `queue.py mark-synced SL-09`), update `00-MASTER.md`. List the five for covers.

## State at handoff
- SL-09 is `in_progress` (Claude) on the queue and the Edit Queue page (doc version 3). Board entry `SL-09` (update it).
- Claim commit `143547f` pushed. Nothing rendered, nothing generated. **$0 spent.** Cost cap for any paid AI take:
  $5 per short (other content video); Flow subscription takes cost nothing.
- Decisions file: `/Volumes/Extreme/_edit_work/sl09/round2-plan/decisions.json`.

## Starter prompt
> Read `Handoffs/handoff-20261018-sl09-oura-shorts-r2-build-a-h-i-j-k.md` and execute it: build the five Shorts I picked
> (A, H, I, J, K) from Zeeshan's "My Honest Oura Ring Review" (Video 4) with /shorts in Soft Blue Light HyperFrames, show
> every graphic and clip on the round-1 review page, run the gates and an independent audit on each delivered file (no
> covers). Deliver, send me the review copies, update the master list. Name this task "Oura Ring Review SFL R2".
