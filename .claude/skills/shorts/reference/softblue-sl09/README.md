# `softblue-sl09/`: Soft Blue shorts from an EDITOR'S finished master (SL-09 Oura Ring Review, round 1 as R2, 2026-10-18)

The first Soft Blue Light + HyperFrames shorts batch cut from Zeeshan's finished 16:9 master (Video 4, "My Honest Oura Ring
Review After 1.5 Years"). It joins `softblue-sl07/` (the Soft Blue batch renderer, title band, key-point bars, B-roll covers) to
`zeeshan-master/` (his picture and mix carried untouched, his graphics whole or absent). Work folder:
`/Volumes/Extreme/_edit_work/sl09/round2/` (run from there; these are copies kept in git). Read `softblue-sl07/README.md` and
`zeeshan-master/README.md` first: their lessons still bind.

```
asr.py / xcorr.py / vad.py   Whisper words on the five passages; master wav vs -ss pulls (0.0 ms at 9 points); voice-band VAD
edges.py                     every cut edge: words, VAD gaps, 20 ms voice and 5-12 kHz envelopes (his mix has a soft music bed)
scan_src.py, cutframes.py    his own cuts inside each passage, then frame-exact (ffmpeg -copyts!) -> plans.ZCUTS
gfxspan.py                   when his navy lower thirds and the verdict card are on screen (per-frame colour fraction)
batch.py audio|words|plan|track|gfx|proof|render S..   the renderer (master as its own roll; his cuts split shots)
scenes_hf.py [--render]      our moving scenes at the 1080 x 1610 picture area: I_chart (before-card) and J_compare (compare-card)
render_all.sh S..            plan, gfx, render each short in turn, waiting for a build slot
post.py S..                  deliver.py copy (audio gate --verbatim, REVIEW 540p, delivered ASR, plan) + watch.py, per short
rungate.sh S                 the delivery gate (never from a shell line that says gate.py)
export_stills.py S.., decided.py, page_r1.py (+ notes_r1.py)   the round-1 page: stills, context clips, one floating player
chain_r3.sh S..              R3: render_all + fix_tp + clear stale watch images + post, per short (queue several with a wait-for-done shell)
r3/brief.py S                R3: the independent reviewer's brief for one short (file sha, sources, what changed, standing rules, judge + audit jobs)
page_r4.py + r4/r4_page.json R4: the later-round page (what changed with times and watch ranges, the two shorts, each AI clip alone/in context, decisions)
r4/brief.py, r4/*.spec.json  R4: reviewer brief; the motion-gate specs of the three takes; r4/prompts/ every Veo and Codex prompt, kept and rejected
r4/page_assets.sh            R4: review copies, A/B, each new clip alone and in context, a full-quality still (run as one renderq step)
```

## What is different from SL-07

- **The master is its own roll.** `A_pieces()` is the identity map (film time = master time). A talking shot is one continuous run
  of the master between two of HIS cuts: the shot key carries `sum(nsrc >= z for z in ZCUTS)`, and every talking shot stores its
  per-frame source index `n` (asserted strictly +1 per frame). No sliver folding: a fold would run his next shot under this
  shot's window; a talking shot under 8 frames is refused at render (cover it). Windows come from the 1920 x 1080 master at 1x
  (724 x 1080 -> 1080 x 1610 is 1.49x, Lanczos), from row 0.
- **His own wide/near cuts are the framing changes.** The default window is "full" everywhere; our size step (mid) is only for
  our own joins inside one of his framings (`SHOTS_AT`, keyed by a master time, because shot indices move whenever covers change).
- **His graphics are covered, never sliced.** Every lower third in a passage is covered whole by a clip from 0.35 s before its first
  frame to about 1.2 s after its last (`gfxspan.py`). His verdict card (x 60-626) stays outside the crop: `cx=1014` (x0 652).
  His sleep-score card and verdict list were rebuilt as our own moving scenes (`scenes_hf.py`).
- **Cutframes need `-copyts`.** Without it ffmpeg's `showinfo` pts restart at the seek point and every cut came back as "frame 30".
  Close pairs (a 0.5 s shot between two cuts) need a +-0.25 s window or the larger one swallows the smaller.
- **Covers can take master footage** (`src=MASTER, t=<master s>`): his real Tesla footage, framed on the wheel.
- **`psolo`**: Dan's real Oura app recording from the film (his phone mock at x 91-424, 7:00-7:18), cropped to the screen, in our
  phone shell at 1.0x (520 x 1075 from y 316, outline ends 21 px above the captions), whole screen dark. At 1.2x the phone ran
  into the caption band.
- **Audio encode: `aac_at -aac_at_mode abr` at 320k.** The default mode overshot his -1.0 dBTP to -0.8 on short I (audio gate tp
  row FAIL); ABR at the same bitrate measured -1.1, VBR q0 -1.0, native aac -1.0. `remux.sh` swaps the audio without touching the
  picture.

## What round 1 learned

- **A Pexels "clip" can be a montage.** 6698753 (a man awake in bed) dissolves in until 6.4 s and out from 9.2 s; the sourcing pass
  called 5.95-9.7 clean because it looked for hard cuts. Print the frame-to-frame difference over the whole span and treat a
  sustained rise (3x the median for several frames) as a transition.
- **Check a stock actor against Dan.** B0494 (a stressed office worker) reads as Dan at a glance on a phone. Out.
- **Key points: line 1 must fit on its own (~26 letters).** "If Someone Wrecks Your Sleep," wrapped as "If Someone Wrecks Your /
  Sleep," and then "Sleep, They Have To Go". Print `V.lt_scenes` for line 1 alone.
- **Near shots cannot carry a bar.** His near framing puts Dan's chin at source rows 750-880 (output 1430+); bars go on his medium
  shots (chin under row 550) or over clips.
- **The frame gate on a seated, waist-up person:** the pose rows measure legs hidden under the table (visibility 0.05) and fail
  meaninglessly; declare the man as `may_change`, lock the kitchen with `lockstill.py`, and let the reviewer judge his anatomy.
  Lock with a box over START's head as well: START's fine flyaway hairs escaped the person mask and were copied back as two stray
  strands on the cabinet (frame-reviewer FAIL).

## What round 2's reviews taught (SFL R3, 2026-10-18)

- **An editor's animated zoom is not a cut.** `cutframes.py` reported Zeeshan's zoom starts (930.43, 940.27) as cuts, so the shot
  split there and the window hopped sideways or snapped size in the middle of his zoom, mid-word (reviewer H D2, D3). Before a
  ZCUT splits a shot, check the source is discontinuous there: per-frame scale through a real cut jumps; through his zoom it
  runs smoothly (0.95-0.99 or 1.03-1.05 per frame). Keep one window through a zoom; put the size step on his real hard cut.
- **Night driving in a vertical is mostly black sky.** A 16:9 road clip filled into 1080 x 1610 puts the horizon near y 1150
  and leaves the top two thirds empty; a gamma lift then turns it into a flat grey screen (reviewer H D5). Zoom 1.7 at fy 0.95
  lifts the horizon to about y 660 so road and lights fill the picture, and `curves=all='0/0 0.06/0.04 0.3/0.42 1/1'` lifts
  the mids while black stays black.
- **A stock gag runs to its payoff.** The alarm-clock opener cut away with the hammer raised (reviewer A D2); it now runs to the
  hit and cuts to Dan in the next word gap. Look at the clip's whole action before trimming its end.
- **A call-out on a phone screen must win against the screen.** A thin outline in the app's own blue read as the app's
  selected row while "Sleep Score 90 Optimal" stayed the biggest thing (reviewer K D1). `psolo` `hl` now takes `dim` (the
  rest of the screen to 35 %), a warm `color` and `arrow` (an arrow beside the phone that bobs for its whole screen time).
- **A caption never ends before its last word.** The "cue ends on a cut in its last 10 frames" rule cut three cues mid-word;
  it now applies only when the cut falls after the cue's last word ends.
- **Check a reviewer's word timing on the waveform before moving a caption.** A reviewer's Whisper put a word 0.5 s early;
  the 50 ms level print showed the CTC timing was right.
- **No Oura ring or WHOOP stock exists** (Pexels: wedding bands, branded straps). The film's own ring footage (5:48-5:57) has
  Dan talking behind his hand, so lips would not match the short's audio; the ring and band are AI frame ideas (J1, J2) for Dan.
- **The delivery gate's framing rows on an editor's master.** `framing:headroom` grades only TRACKED holds (fixed crops are
  exempt): a crop that follows Dan must anchor his hair 30-70 normalized px down. Fix it in the window, not with a waiver:
  `wh`/`y0` per shot (a slightly smaller window starting lower), or `y0k` keys that glide the top edge inside the editor's own
  zoom when his zoom moves the hair. `framing:push_coverage` wants two holds at the main framing at least 1.1x apart: a
  punch-in (`SPLIT`) on a WIDE shot at a sentence break, never on a near shot (captions land on his mouth).
- **Every cover you remove may have been hiding one of his lower thirds.** Before dropping a clip, list his graphics in that
  span (`gfxspan.py`); short 3's restless-man clip was also covering "High Adrenaline Driving Can Disrupt Your Sleep".
- **An editor's AI clip with a flaw can come back cropped.** His AI Tesla clip (speed read 190 against a spoken 120) works at
  zoom 1.22, fy 1.0: the zoom drops his burned "*AI Generated" text off the top whole and the window leaves the speed display
  out; our chip goes on.
- **The phone alone (`psolo`):** the recording fills the whole rounded screen (538 x 1200 at radius 65), cropped above the
  recording's own home bar; `rise` px keeps it moving; the AbsByAI.com mark is not drawn under it (two-line captions under
  the phone touched it: gate `captions:graphic_clearance`). Pick recording stretches by a frame-change map so no screen
  switch or bounce sits at either end.
- **A long pause inside one piece trips `junk:dead_air` (max 1.0 s):** `TRIM` takes the middle out (audio cut only).
- **Reviewer word disputes:** score the candidates with forced alignment (WAV2VEC2 path log-probability) before changing a
  caption; "near bedtime" beat "in your bedtime" (-32 / -69), "your behavior" beat "their behavior" (-95 / -116).

## What round 4 taught (SFL R4, 2026-10-20: Dan's three approved AI clips into shorts 4 and 5)

- **A WHOOP reads as a WHOOP only by its pod.** Dan sent J2 back because a plain knit band "is just like a bracelet". Codex
  fixed it in one edit of the approved START (`aiframes/J2w_start.txt`: replace only the band; a slim black knit strap and a
  rectangular matte charcoal pod about 3.6 x 2.5 cm, long side across the wrist, on TOP of the wrist, no screen, no logo).
- **A pod on top of the wrist cannot survive a palm-up turn.** The approved action (turn the hand palm-up) would hide the
  pod in the END frame Dan asked to fix. A partial roll came back with the forearm sliding and a confused thumb; the hand
  closing into a relaxed loose fist kept ring, pod and forearm in place and passed gate and reviewer first time. Say so on
  the page ("What I decided"): it is a change of action forced by the fix.
- **Flow credits are shared by every editing session.** On 2026-10-20 four sessions took the balance from 920 to 10 by
  mid-afternoon; K1 got the last 20 and J1/J2 hit `CREDITS_OUT`. Read `~/.absbyai-veo-ledger.jsonl` (the last `balance`
  rows) before promising same-day motion, and queue the clip that matters most first.
- **Veo frames mode snaps to the END frame in the last second or two.** K1 played cleanly to about 6.6 s, then the hand
  popped back up and the table jumped to match END. Plan the edit on the early part (K1 uses 0-4.3 s) and check the tail
  before using it.
- **A bright AI kitchen sits above Dan's studio picture.** K1 measured median 0.49 / saturation 0.19 against Dan's
  picture area 0.34 / 0.26; `curves=all='0/0 0.5/0.44 1/0.96',eq=saturation=1.25` took it to 0.43 / 0.26.
- **Veo hand clips: START frame only beats START + END.** With both frames Veo improvised in the middle every time: two J1
  takes clenched the hand into a fist, four J2 takes flicked a finger up on the way to the approved fist. From the START frame
  alone, with "fingers stay open, move together with the hand" in the prompt (and a negative prompt on the paid route), J2's
  lift-and-tilt and J1's Flow take came back clean first time. Keep the approved END frame as the intent, say so on the page.
- **A take's spec must not mark most of the picture `may_change`.** J1's pair spec covered the top 81 %; the camera fit then
  had only the bottom strip, a sub-pixel wobble there extrapolated to 10 px at the top corners, and `camera` plus
  `still:sheet_top_left` failed while template matching, Farneback flow and phase correlation all measured that corner under
  1.1 px. Narrowing `may_change` to the hand and forearm (stricter, more background points) passed; the reviewer confirmed the
  narrowing was legitimate. Narrow, never widen.
- **`chipplace.py` cannot place a label on a hand close-up:** Vision's person mask marked the whole bed sheet (J1) or bled into
  the desk (J2). Place by measuring the hand on about ten frames of the used range, with the chip's REAL size from
  `B.disclosure` (at 1.6 it is x 40-365, 64 px tall; the 408 x 81 box the tool prints is larger).
- **When Dan is waiting, run the chain as one prioritized queue step:** `renderq.py run --priority --group sl09 -- zsh
  ./chain_r3.sh S`. Started plainly, its three piped ffmpeg calls queued separately and slid back behind other videos'
  continuations for 40 minutes.
- **Two paid `veo.py api` runs at once lost a take record** (each saved the job file it loaded minutes earlier). Fixed in
  `veo.py` 2026-10-20 (locked update, unique take names); in a session started before that, run paid takes one at a time.
