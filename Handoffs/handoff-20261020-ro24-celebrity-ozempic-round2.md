**LFC.** Task name: `Celebrity Ozempic LFC R2`.

# RO-24 "Reacting To Celebrity Ozempic Transformations": round 2 handoff (written 2026-10-20 at the end of round 1)

**Waits for Dan's reply to the round 1 page.** Do not start until his answers exist; then follow them exactly.

## Read first
`Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md`, `.claude/skills/_shared/chroma-key/README.md`,
`.claude/skills/_shared/PRE-RENDER-APPROVAL.md`, the job doc `Handoffs/video-editing/RO-24-reacting-to-celebrity-ozempic-transformations.md`.
Recipe of round 1 (copied into the repo): `.claude/skills/longform-edit/reference/ro24/` (README there).

## Where things are
- Work dir: `/Volumes/Expansion/_edit_work/RO-24/round1/` (Extreme is 99 % full; everything lives on Expansion). Build round 2 in `round2/`.
- Review page: http://127.0.0.1:9124/ (`review/index.html`), served by `_shared/review_server.py 9124 .../round1/review`.
- First minute: `review/first-minute/DRAFT - RO-24 round 1 - first minute.mp4` (+ `.build.json`); VLC copy in `Videos to Review/`.
- Source roll (read only): `/Volumes/Extreme/10:15 .../C1726.MP4`, lav = left channel only, the Ozempic video is 7:25 to the end.
- Transcript (medium.en, source seconds): `audio/words_src.json`; sentences: `script/tx_medium.txt`; script with cues: `script/shootdoc.txt` from line 2730.
- Whole-film take list (best take of every line, edges on the measured envelope, pauses not yet capped): `edl_full_takes.json` (16 pieces, about 6:58).

## Round 1 choices waiting for Dan (recommended first)
1. Key: refined edges (`key16.py --variant refined`) vs the approved Bill Maher key exactly (`--variant approved`).
2. Colour: warm (DS-40 grade) / rich / natural (`comp16.grade`).
3. Background: depth / light / navy (`comp16.background`).
4. Voice: Balanced + 3 dB at 120 Hz / Balanced / Open (EQ strings in `recipe/audio_options24.py`; no expander; -14.1 LUFS, -1.5 dBTP, oversample 4).
5. First 5 s: celebrity photo montage / AI clip (two men, same shot, ripped vs gaunt) / camera open.
6. Permission to download ~20 news photos of Sharon Osbourne, Fat Joe, Amy Schumer, Meghan Trainor, Oprah, Tracy Morgan (<30 MB). No download before his yes.

## Round 2 work (after his answers)
1. Key every piece of `edl_full_takes.json` with `recipe/key16.py` (one queued job per piece, ~2.5 s/frame when the Mac is busy; plate screen).
   Temporal neighbours never cross a piece boundary (the script reads 2 handle frames inside the same continuous take).
2. Cap pauses inside pieces (stretched words: `out` 684.2-686.7, `and` 786.4-789.1), then re-read every join.
3. Photos (if yes): shown as each person is named; real news photos are not Dan, so no "real photo of me" label; credit the outlet in small type.
4. Graphics from the script cues (Soft Blue Light HyperFrames, title case, no drug names on screen): Fat Joe numbers, no bread/pasta/rice,
   Amy Schumer, the head-to-head study full-screen card (about 50 vs 33 lb, 72 weeks, NEJM 2025; quit over stomach side effects 2.7 % vs 5.6 %),
   the protein rule (lift every day, 0.8 g per lb of lean mass), Oprah (stopped a year, 20 lb back), trial (14 % regained within a year),
   step-down schedule (5 to 4 to 3 to 2, 1 mg a week), recap (4 points). The Elon Musk section was not filmed.
5. B-roll: training and meal prep / salmon were not filmed; clip library first (`clip_library.py find`), grade every clip to the presenter.
6. AI clip ideas (6 to 9 frame pairs, funny where the line is hard to picture) through `_shared/framecheck` before Dan sees them.
7. Then the full film: delivery gate, watch pass, edit sheet, independent review, SRT (Whisper fixes: "Osempic/Ozenpik" = Ozempic,
   "Zebbound/zetbound" = Zepbound, "Monjaro" = Mounjaro, "six pack abs .com" = sixpackabs.com, "old zempic" = Ozempic).

## Watch for
- A Claude session (DS-40 R2, `/Volumes/Extreme/_edit_work/ds40/r2/`) is polishing the same key on Bill Maher (hair flicker, dark rim, watch glass). Before keying the full film, check whether Dan approved a newer key there and fold it in.
- On the light background the Soft Blue Light lower third's glass strip reads lighter (slate) than on studio films. If Dan or the reviewer flags it, make the strip's fill more opaque over light backgrounds rather than changing the template's look elsewhere.

## Costs so far
About $0.40 of Gemini listening (16 calls). No generation. Long-form AI budget: $15.

## Model
Claude: Opus 5.5, high effort.

## Starter prompt
> Celebrity Ozempic LFC R2. Read `Handoffs/handoff-20261020-ro24-celebrity-ozempic-round2.md`, then Dan's round 1 reply, and execute round 2 of "Reacting To Celebrity Ozempic Transformations" (RO-24) with /longform-edit.
