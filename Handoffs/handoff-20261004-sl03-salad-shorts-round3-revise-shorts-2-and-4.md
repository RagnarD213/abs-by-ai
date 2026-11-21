# SL-03 Daily Salad shorts: round 3 (revise shorts 2 and 4, then finalize the batch)

**Category: CONTENT. These are Shorts cut from a long-form (`SFC` from the RO-05 `LFC`), which is the format a
long-form gets. Written 2026-10-04 by Claude (Opus 5.5). Task name: `Daily Salad SFC R3`. Recommended: Claude Opus 5.5, high.**

## EXECUTED. Dan finalized all six shorts on 2026-10-08. Next: `handoff-20261008-sl03-daily-salad-shorts-covers-and-setup.md`

## (history) STATUS 2026-10-04: steps 1 to 4 done, waiting for Dan's review of shorts 2 and 4

Both revised shorts are delivered (reviewer SHIP, delivery gate PASS, audio gate PASS). Review page:
`_shared/review_server.py 8831 /Volumes/Extreme/_edit_work/sl03/r3/review` (http://127.0.0.1:8831/). What was built, and
where it differs from the cuts recommended below (short 2 ends on the "lock in" line; short 4 ends on the vinegar
caution line and drops "coated in oil and vinegar and spices"), is in `Short-form video content/daily-salad-SHORTS.md`,
"Round 3". Why: `shorts/reference/softblue-sl03/README.md`, "Round 3". **Next: when Dan answers, do step 5 below** (or
revise the short he names; `plans.py` is current).

## Dan's verdict on round 2 (2026-10-04, his words; hashes in `/Volumes/Extreme/_edit_work/sl03/round3-plan/decisions.json`)

| Short | Verdict | His words |
|---|---|---|
| 1 Break Your Fast With This | **approved** | "The first one looks good. That's approved." |
| 2 The $20 Salad You Can Make For $4 | **changes** | "I want to remove the content at the end talking about the rotisserie chicken. I feel like that was a little bit not related to the main point of the video. I want to add in a little bit at the beginning, basically from the intro clip of the long form, to give context: 'Hey guys, today I'm going to show you my Daily Salad.' I feel like this needs a little bit more context overall to be understood by someone who did not watch the long form... add a little bit of content into the beginning from the beginning of the long form, which gives a viewer context for what this video will be about. Shows a salad" |
| 3 Keep Your Salads Fresh For 7 Days | **approved** | "Looks good. That is approved." |
| 4 Stop Buying Salad Dressing | **changes** | "I also want you to add in a little bit of content at the end talking about the vinegar and spices. If necessary, cut some other content throughout the video, but I feel like this doesn't really make sense without also at least briefly showing the vinegar and spices." |
| 5 Track A Week Of Meals From 1 Photo | **approved** | "looks good. That is approved." |
| 6 The One Line That Makes It Accurate | **approved** | "Short 6 looks good. That's approved." |

He did not answer the page's question about the following close-up crops. Short 5 is approved as delivered and he asked
for nothing on short 4's close-up, so that crop stays. Do not ask again.

**Shorts 1, 3, 5 and 6 are final. Never re-render, re-plan or re-deliver them.** Their files, stamps and `shots.json` stay
exactly as they are. ⚠ `batch.py`'s planner changed after some of them were rendered, so `batch.py plan` on S1, S3, S5 or
S6 would rewrite their `shots.json` and break the match with the delivered file. Run every command with `S2` and/or `S4` named.

## Read first

1. `.claude/skills/_shared/VIDEO-RULES.md` (in full), `Handoffs/video-editing/00-RULES.md`.
2. `.claude/skills/shorts/reference/softblue-sl03/README.md`: the round 2 run order and, above all, "What the independent
   reviews taught" (eight review passes; every rule there was a rejection first).
3. `.claude/skills/shorts/reference/softblue-sl03/plans.py`: shorts 2 and 4 as data (`SEG`, `TRIM`, `COVERS`, `SPLIT`,
   `SHOTS`, `BARS`, `TEXT`). This is the file you edit.
4. `Short-form video content/daily-salad-SHORTS.md` (status, key points, what each gate declaration is).
5. `.claude/skills/_shared/GRAPHICS-STANDARDS.md`, "Soft Blue shorts standard" (the locked look; no look round).

## State

- Delivered files: `Short-form video content/daily-salad-short1..6_*.mp4` (all six: independent review SHIP, delivery gate
  2.4.0 PASS, verbatim audio gate PASS). Review copies and sound checks: `Short-form video content/daily-salad REVIEW/`.
- Build: `/Volumes/Extreme/_edit_work/sl03/r2/<S>/`. Run tools from `/Volumes/Extreme/_edit_work/sl03` with the scripts in
  `.claude/skills/shorts/reference/softblue-sl03/` (`batch.py`, `deliver.py`, `page_r2.py`, `rungate.sh`).
- Source: RO-05 round 4 master times ("film" seconds) in `/Volumes/Extreme/_edit_work/ro05-fable/round4/full/`
  (`timeline.json`, `mapped-words.json`). Audio is cut from `sl03/master_audio.wav` (the approved mix, cut only). Picture
  is the RAW rolls through the long-form's grade; talking shots follow the long-form's audio map.
- Review page: `http://127.0.0.1:8811/` (`review_server.py 8811 /Volumes/Extreme/_edit_work/sl03/r2/review`).
- Queue: SL-03 is `ready` (this handoff). Spend so far $0.
- ⚠ Git: commit `9845e46` (round 2 tooling and standards) is local only. `safe-push.sh` stopped because another session
  has uncommitted edits in `_shared/VIDEO-RULES.md`, `_shared/framing-motion.md` and
  `shortad-from-longform/reference/render.py`. This handoff and the board edits are uncommitted for the same reason
  (the rule is not to commit on top). Run `safe-push.sh` with your files plus this handoff when those three are clean.

## Short 2: the new cut

Now: `[65.76, 97.76]` + `[574.15, 586.10]` (the rotisserie chicken), 43.9 s. Opens on the salad over "Let's talk about why
I make it myself".

Change:
1. **Remove** the chicken piece `[574.15, 586.10]`, its B-roll cover (`C1548 117.30`) and key point G2 ("Buy A ROTISSERIE
   CHICKEN / Better Taste, HALF THE PRICE"). The short then ends on "...so it's much, much cheaper." (film 97.76).
2. **Add the long-form's opening line at the start:** "What's up guys? Today I'm gonna be showing you how I make my daily
   salad." Film `0.00` to about `4.40` (silence 0.00-0.31 before, 4.29-4.59 after). Raw: C1535, raw = 3.30 + film.
3. **Recommended second context line (my call; put it under "What I decided"):** "Now this salad is a tremendous
   breakthrough for me because it only costs a few dollars." Film about `10.70` to `15.30` (silences 10.42-10.98 and
   15.20-15.45; C1535 raw 14.1-18.5). It ties the intro to the $4 title and leads straight into "Let's talk about why I
   make it myself". Round 1 already told Dan this line was the fallback opener. With both lines the short is about 41 s.
4. **Show the salad in the intro** (his "Shows a salad"). Recommended: the finished salad fills the frame under the first
   line (two different moments of C1550, e.g. 118.6 then 111.3, with a cut near the word "showing"), then Dan on camera for
   "Now this salad...". The first frame stays the dish, as on every food short. Proof it before rendering.
5. The join into `65.76` is now internal. It still starts 10 ms after a "But" with no pause (envelope: "But" 65.69-65.75,
   "Let's" from 65.79); splice it after the new intro and transcribe it in context before rendering (README, first lesson).
6. Key point G1 ("Salad Bar: $20 A SALAD / Homemade: About $4") stays. A second bar is optional; if you add one, it must
   distill (for example the drive: the habit broke on weekends and busy days), sit on a full-level hold and land on words.
7. `plans.py`: `SEG["S2"]`, `COVERS["S2"]`, `BARS["S2"]`, `TEXT["S2"]` (add the intro text with a ` | ` at each audio
   join), and **renumber `SHOTS["S2"]`**: its keys are shot indices as `batch.py plan S2` prints them, and the new intro
   shifts every one. The two long takes keep `auto=True` (the steady-hold planner).

## Short 4: the new cut

Now: `[145.31, 172.15]` store dressing vs olive oil, `[485.95, 494.01]` "you don't need to pre-make your dressing... put
your spices right on there", `[522.32, 539.45]` olive oil is 120 calories, the two pours. 50.5 s. It stops before the
vinegar and never shows a spice.

Where the vinegar and spices are in the long-form (film seconds, words from `mapped-words.json`):

| Film | Words | Raw picture |
|---|---|---|
| 494.23-497.15 | "I'm going to add in some black pepper. I pour on a good amount like this." | C1547 237.1-240.3 |
| 497.20-499.95 | "Garlic powder, pour on a generous amount." (pause 497.88-498.77) | C1547 250.4-253.2 |
| 505.57-506.6, 512.21-513.90 | "Now adobo." / "So I'm going to put on a few sprinkles like this," | C1547 259.7, 274.3 |
| 539.34-540.71 | "Now the vinegar." | C1548 39.4-40.7 |
| 553.56-557.15 | "Too much vinegar and you will have diarrhea. Too little and it's going to be dry." | C1548 58.3-60.5, 63.5-65.0 |
| 557.49-560.02 | "So I find about the optimal amount is another two tablespoons." | C1548 65.3-67.9 |
| 567.32-570.92 | "All our vegetables are coated in oil and vinegar and spices." | C1548 101.0-104.6 |

Raw time for a talking shot is the long-form's audio map (`timeline.json` "A": raw = in + film - at); `batch.py plan`
does this for you once the ranges are in `SEG`.

**Recommended cut (about 56 s; my call, list it under "What I decided"):**
1. `[145.31, 164.14]`: "Now let's talk about the dressing... long shelf life. Instead, you want this, olive oil." (18.8 s).
   This drops "In my opinion, the healthiest fat that you can consume and also the best tasting fat." (164.14-168.80) and
   "This olive oil based dressing will taste better than this store-bought dressing." (168.80-172.15) to make room, as
   Dan allowed. Silence at 163.89-164.19 gives the out point.
2. `[485.95, 494.01]` as now (8.1 s).
3. Spices, right after "put your spices right on there": black pepper `[494.23, 497.15]` and garlic powder
   `[497.20, 499.95]` (5.7 s). Add adobo only if the length allows.
4. `[522.32, 539.45]` olive oil and the pours, as now with its two pause trims (15.6 s).
5. Vinegar: `[539.34, 540.71]` + `[557.49, 560.02]` (3.9 s).
6. Close: `[567.32, 570.92]` "All our vegetables are coated in oil and vinegar and spices." (3.6 s). The short then ends
   on vinegar and spices, which is what Dan asked for.

His words were "at the end". The spices sit mid-short in this cut because that is where he does them (right after "put
your spices right on there"), and the ending carries the vinegar and the line that names all three. If you judge the
literal reading safer, move the two spice pieces after the oil instead; check the bowl looks right across that order.
Either way say which you did under "What I decided". Keep it under 0:59; if it runs long, cut the adobo, then the
"too much vinegar" line, never the vinegar amount or the closing line.

Then:
- **Key points:** G1 ("Skip STORE DRESSING / Use OLIVE OIL Instead") lands on a line this cut removes; re-land it on
  "Instead, you want this" or the store-oils sentence, on a full-level hold with his face above y1130 (the opening is an
  extreme close-up: no bar there). G2 and G3 stay. One new bar for the ending is worth it, for example
  `The Whole DRESSING:` / `Olive Oil, VINEGAR, Spices` on the closing line. Two lines, each landing on a word.
- **Picture:** new shots from C1547 (spices) and C1548 (vinegar, toss). Same-camera joins need a real size step
  (about 1.25x on the displayed face) or a steady, faceless cutaway; no B-roll shot twice (already used in this short:
  C1550 114.0, C1533 33.2, C1550 98.0; the C1548 3.7 bottle cover leaves with the part being cut). The pours are kept as teaching pauses (declared `junk:dead_air`).
- **Pauses:** check every new piece for a silence over 1.0 s (`batch.py audio S4` prints the joins; `silence.json`).
- `plans.py`: `SEG["S4"]`, `TRIM["S4"]` (film times, unchanged), `COVERS["S4"]`, `SPLIT["S4"]`, `BARS["S4"]`,
  `TEXT["S4"]`, and renumber `SHOTS["S4"]` from the new `batch.py plan S4` table. The cover at film 165.41-166.26 falls
  inside the part being cut; remove it.
- `gate/declare.json` for S4: re-check each declaration against the new cut (the wide-level hold, push statistic and
  pour pauses were written for the old one). A declaration that no longer applies comes out.

## Work, in order (shorts 2 and 4 only)

1. Re-hash the four approved files against `round3-plan/decisions.json`. Check the two-build cap.
2. Edit `plans.py`. Then per short: `batch.py audio`, `words` (read the low-confidence list and the caption text),
   `plan`, `track`, `gfx`, `proof`. Look at the proof sheets before rendering: face inside the frame, bars off his face,
   every cutaway steady.
3. `batch.py render`, `deliver.py copy` (audio gate, 540p, transcript diff, plan), `watch.py`, a fresh `ra-reviewer`
   subagent as judge and independent auditor (brief pattern: files and the approved look, never your notes), then
   `watch.py --judge` and `rungate.sh`. Expect more than one review pass. Fix, re-render, re-review; a changed file needs
   every stamp again.
4. Rebuild the review page for round 3 (`page_r2.py` with a new `extra.json`, or a round 3 copy): only shorts 2 and 4 are
   questions, the four approved ones appear as a record line, with "What I decided" for every call above. Send Dan the
   page. `queue.py set SL-03 delivered`, mirror to the Edit Queue page, update `daily-salad-SHORTS.md`.
5. **When Dan approves 2 and 4:** `queue.py set SL-03 finalized` with his words, mirror it, delete the board entry,
   register the B-roll inserts in the clip library (list in `daily-salad-SHORTS.md`, plus the new spice and vinegar
   shots), and write the ONE Claude handoff for covers plus setup (five choices per short: one pool photo, one studio
   photo, three AI designs; it must say "Use the Codex subscription to generate the images"), to run after RO-05 is
   public on Oct 18. Post shorts 5 and 6 at least a week apart.
6. No covers, no upload, no queueing in this task.

## Traps (all hit in round 2)

- Other sessions render on this machine. The gate waits for a build slot and can sit for an hour or more. Launch it with
  `rungate.sh S2` only: any shell or watcher whose command line contains `gate.py` counts as a build and deadlocks it.
- `import deliver` finds `_shared/deliver` (the gate), not ours; `page_r2.py` loads ours by path.
- A B-roll cover's `cx` and a talking shot's window must agree at a cut inside one take, or the picture lurches.
- An extreme close-up needs `head=True` (follow his head, ears in). A shot where his face fits gets a steady crop.
- Port 8810 is another session's server. The board is at its 2,500-word limit: keep the SL-03 entry to one line.
- Do not run a watcher on a log file a previous run already wrote (it reads the stale result). Empty the log first.

## Starter prompt

> Name this task `Daily Salad SFC R3`. Read `Handoffs/handoff-20261004-sl03-salad-shorts-round3-revise-shorts-2-and-4.md`
> and the files it lists. Shorts 1, 3, 5 and 6 are approved and final: do not touch them. Revise short 2 (cut the
> rotisserie chicken ending, add the long-form's opening line with the salad shown) and short 4 (add the vinegar and
> spices at the end, cutting other content if needed), re-check both with the watch pass, an independent audit and the
> gates, and send me the two on a review page. No covers, no upload.

Model and effort: Claude Opus 5.5, high.
