# My First Spray Tan SFL R2: build Shorts A and C (SL-15)

**CONTENT: Shorts extracted from the long-form "Spray Tanning Guide: How To Looksmax With A Spray Tan" (RO-19). SFL.**
Task name: **`My First Spray Tan SFL R2`**. Model: **Opus 5.5, high**. Written 2026-10-18 by `My First Spray Tan SFL R1`.

## Goal
Cut the two Shorts Dan picked from the RO-19 master, in the locked Soft Blue shorts standard, run every gate and an
independent audit on the delivered files, deliver review copies to Dan. No covers, no upload, no queueing.

## Dan's decision (verbatim, 2026-10-18)
Shortlist of eight (A to H) was sent with full transcripts. Dan: *"Let's do A and C"*.
- He picked **two**, not the job doc's three. Build exactly A and C (rule: execute his picks as given). Say in one line at
  delivery that only two were built because he picked two; do not build a third unless he names one.
- **Short 1 = A** (airs **Fri Oct 30, 9 AM Chicago**, `Docs/SHORTS_RELEASE_CALENDAR.md`). **Short 2 = C** (2027 date at setup).
- Neither needs a pickup line. Both open on film words.

## Source
`claude edited long form content/16 - My First Spray Tan (RO-19 re-edit)/My First Spray Tan | claude round 4 | 16x9 | RO-19.mp4`
(SHA-256 `b4b309991b414674e2469fadad7f9b6fb3352ee61f5b02654d1567bbf5b317d8`, 1920x1080). Recipe beside it in `recipe-RO-19/`:
`words_out.json` (word timestamps on the MASTER timeline, field `t0`/`t1`), `plan_resolved.json` (every graphic and insert with
master times), `shots.json`, `edl.json`. Long-form work folder `/Volumes/Extreme/_edit_work/ro19/round4/` is another job's: read only.
Your work folder: `/Volumes/Extreme/_edit_work/spraytan/` exists (check what is in it first; if it is the old 09-02 batch,
make `/Volumes/Extreme/_edit_work/SL-15/` instead). Our own mix: voice B2 with the bass lift; the shorts carry the master's
mix as cut (it is our mix, already gated; do not reprocess the voice, cut at seams only, then audio-gate the delivered file).

## The two Shorts (master times; measure exact silences before cutting)
**A. "Why You Look Less Ripped In Photos"** 0:26.0 to 1:33.0, about 58 s after two cuts:
- opens "If you guys want to look good in photos..." ends "...you'll look much more defined."
- CUT "Now there were some other reasons for that as well like the lighting and what the photographer did"
- CUT "I wasn't exactly like super pale But I was too pale for a fitness photo shoot" (so it reads "the main reason why is that I was too pale and this is the reason why if you look at all fitness models...")
- Each cut is a join: zoom step or insert, never a naked jump (CUT-CONTINUITY-QC.md).
- Inserts already in the film inside this range: Ca01 Tinder stock 28.44-32.56, P02 real photo 48.64-55.06 (label "Real photo of me, not AI-generated", current wording per VIDEO-RULES 2026-10-17), Ca02 bodybuilding stock 69.2-75.1. Lower thirds Ga03, Ga04, Ga05 become key-point bars.
- ⚠ B-roll share is about 28% (16.4 s of 58): under the gate's 30%. Add a library clip at the plan step (e.g. over "a picture of myself in the photo shoot" or "fitness models and bodybuilders"; `clip_library.py find`; Ca03 photographer stock from 1:34 is a candidate).

**C. "Get A Tan Without Sun Damage"** 9:54.6 to 10:41.8, about 47 s:
- opens on "the most important pro of spray tanning..." (trim only the leading "So"; check the opening sounds clean, capitalise the caption) ends "...you're a lot more likely to get that kind of cancer."
- Inserts in range: Cc12 beach stock 601.83-604.8, Cc13 B0233 628.73-633.72, Cc14 B0208 633.72-636.8. Lower thirds Gc12, Gc13.
- ⚠ B-roll share about 23%. Add the film's approved AI clip **A1** (chalk-white vampire under an umbrella on a beach, sprayed golden; `plan_resolved.json` id A1, film 14:42) over "looks like an ultra pale vampire ... takes an umbrella out with him". It carries AI-GENERATED; set `ai_generated: true` at setup.
- Says "Brian Johnson": caption must read **Bryan Johnson**.

## How (rules on record)
- Method: `/shorts` skill, Soft Blue shorts standard (GRAPHICS-STANDARDS.md): title band y 0-310 whole short, picture 1080x1610,
  land-then-hold framing (`cut/landing.py`), key-point bars at 68,1130-1012,1378 in HyperFrames motion, captions from y 1412,
  B-roll fills the picture. Start from `.claude/skills/shorts/reference/softblue-sl07/` (README incl. B-roll share section) or `softblue-sl06/`.
- Hair touches the top in this roll: take the window with the most room above his hair; hair never leaves the frame.
- Round 1 shows every graphic, clip and photo on the review page; since every clip is already approved in the film and
  the look is locked, deliver **both whole Shorts** this round (short-form whole-video rule, 2026-10-14).
- Gates: `deliver/gate.py --format short` on each delivered file, `watch.py` + judge, audio gate stamp, then a fresh
  `ra-reviewer` independent audit on the exact files (the three AI-clip questions for A1). Machine cap: `buildcap.py` before every render.
- Titles name the topic cold; title case; no em dashes anywhere.

## Deliver
- `Short-form video content/spraytan-short1_why-you-look-less-ripped-in-photos.mp4` and `spraytan-short2_get-a-tan-without-sun-damage.mp4`
  (1080x1920) + stamps, REVIEW 540p copies, `spraytan-SHORTS.md` (in/out, title, parent RO-19). Note: older `tan-short*` files are
  the unposted 09-02 batch from the old master; leave them alone.
- Copies in `Videos to Review/` named `My First Spray Tan SFL R2 - short N - <title>.mp4`; review page via `review_server.py`.
- `queue.py set SL-15 delivered`, mirror to the Edit Queue artifact, update `00-MASTER.md`. Covers are listed for the setup task.

## State at handoff
SL-15 is `in_progress` (Claude) on the queue and the page. Board entry `SL-15:PICKS` (update it). Commit `0793081` (claim) is
local; safe-push stopped on live edits by other sessions; any later safe-push carries it. Nothing rendered yet. $0 spent.
