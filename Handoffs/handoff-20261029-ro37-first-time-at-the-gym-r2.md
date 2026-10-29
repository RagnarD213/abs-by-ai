CONTENT (LFC). Task name: `First Time At The Gym LFC R2`. Model: Claude Opus 5.5, high effort (the video started on Claude).

# RO-37 "I'm 41. Here's What I'd Do If I Walked Into A Gym For The First Time": round 2

**Fire only after Dan replies to the round 1 page** (http://127.0.0.1:9537/). Round 1 delivered 2026-10-29; nothing here is approved yet.

## Read first
`Handoffs/video-editing/00-RULES.md`, `.claude/skills/_shared/VIDEO-RULES.md`, `.claude/skills/_shared/PRE-RENDER-APPROVAL.md`,
`.claude/skills/longform-edit/reference/ro37/README.md` (portrait presentation and the traps round 1 paid for). Work folder:
`/Volumes/Expansion/_edit_work/RO-37/round1/` (recipe/ holds the live scripts). Build round 2 in a new `round2/` folder; never overwrite round1 media.

## State at the end of round 1
- EDL: 35 pieces from C1894, C1895, C1897 (C1893 hook take not used), film 7:55.5. Take choices and cut ad-libs: `recipe/edl.py` (each row says why).
  Every join re-transcribed (`recipe/asr_check.py`, `logs/asr2.log`): clean.
- Presentation built as (a): W = upright panel on the moving Soft Blue field, T = full-frame close-up, T2 = tighter close-up at take joins under
  lower thirds. Lower thirds always on close-ups (`build.lt_framing`); side lists push the panel right with an eased slide.
- Colour F Deep And Vivid, voice A Natural Warmth (both the pool set's prior picks) used in the draft. Options shown: presentation a/b/c, colour F/E/B,
  voice A/B/C/D. 10 blind listens preferred C (untreated) 6.5 vs A 3.9, noisy.
- 24 HyperFrames graphics (`hf/manifest.json`), 13 gym B-roll clips with name chips (`broll/grade.json` lifts), all in context on the page.
- AI frame pairs passing gate + fresh reviewer: A1 Frozen at the gym door, A2 Done at hour two, A3 Too sore for the stairs, A4 The gym bag under the desk,
  A6 Two weeks of cobwebs, A7 Nobody is watching you (`ai/frames_report_page.json`). A5 "300 pounds on day one" failed 5 tries: off the page.
- First minute hair check PASS (closest 36 px). Not run yet: delivery gate, audio gate stamp, full jump-cut/junk pass, ra-reviewer.
- Spend: $0. Release Fri Jan 1, 2027; finished and set up by Dec 18.

## Hashes (sha256)
- first minute draft `review/first-minute/DRAFT - First Time At The Gym R1 - first minute.mp4`: 6c913a4bcec10f83fcdbbb0bcacf4a04d4ac325df469671d0651fa7fc2b4f6d9
- edl.json 7f736942b78072bc97aac0a4688a787ccb70a67047bdfeeee376a0fd05237b4c · shots.json 30000c89e6a153280e053fb8a52c84674d986bf70a2599e42fbeb5eb76863191
- plan_resolved.json 7b26436637c5044255dd17f4be7300cf2c089ca5b0383daa389ca58d704c30e0 · hf/manifest.json 5d7973342b3a554707c83d2c8139a50636f4fede1ca9c33a378ebf57cda96b72
- AI frames report 709af3fb5468d57733eef90551f3c674ea08f5bd2186bd035e0f7dee929825b9

## Next action
1. `python3 .claude/skills/_shared/editcap/editcap.py acquire RO-37 --title "I'm 41. Here's What I'd Do If I Walked Into A Gym For The First Time" --type LFC`.
2. Save Dan's exact words in `round2-plan/decisions.json` (per item: verdict, his words, scope), re-hash the files above.
3. Apply his picks (presentation, colour, voice; `RO37_GRADE`/`RO37_VOICE` env or edit defaults), generate motion for the approved AI pairs on Google
   Flow via the background `flow-veo` agent (subscription; never paid without his yes), motion gate + fresh frame-reviewer on every take.
4. When nothing is pending: full film, exact-file gates (`deliver/gate.py --format longform`, audio gate), CUT-CONTINUITY-QC, independent `ra-reviewer`,
   then the R2 page with revision timestamps, `Videos to Review/` copy, queue `delivered`, `editcap release --review`.

## Starter prompt
> Read Handoffs/handoff-20261029-ro37-first-time-at-the-gym-r2.md and continue "I'm 41. Here's What I'd Do If I Walked Into A Gym For The First Time" (First Time At The Gym LFC R2) with Dan's round 1 reply: <paste Dan's reply>. Name the chat "First Time At The Gym LFC R2".
