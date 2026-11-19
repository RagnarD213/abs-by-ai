# <Product> VSL R4: shared brief for block agents (<date>, <model> orchestrator)

Category: AD (client VSL for <client>). Job `<JOB>`, <Mac>. The orchestrator holds the edit slot and any reservation;
do not touch editcap, priority or the render queue's other jobs. Nothing goes to the client. Spend: subscriptions only.

## Read first
- Style lock: `<path>/STYLE-LOCK.md` (copy in this folder).
- **The client's own words:** `<job>/client/` (his brief, feedback docs and messages, word for word) and the ledger rows
  for your block in "Client ledger rows" below. Where this brief and his words disagree, his words win: stop and tell
  the orchestrator.
- Dialogue foundation: `dialogue/MAP.md` (your block's range, VO passages needing cover, key-visual times), `map.json`,
  `edl_r4.json`, `words_film_r4.json` (film-time words, 1x), `dialogue_r4.wav`, `cam_ranges.json`, `flags_r4.json`.
- Visual vocabulary to start from: the trial lead's plan (`<plan_r5b.json>`) and renderer (`<assemble>`). It is OUR
  draft, not client approved; the client's notes on it are ledger rows and override it shot by shot. Only write
  "approved by <client>" with the approval item's id, for example `[L12]`. Spokesperson compositor (`<r2_doctor.py --map ...>`), callouts (`<f_callouts.py>`), mechanism animation
  (`<graphics/...>`), music (`<music/>`), pace (`<pace.sh>`).
- Assets on hand: client images (`<client_images/>`: **usable only for <what the client allows, with the ledger id>**;
  every use is listed in SOURCES.md with the reason), cached stock (`<stock/>` + index), approved key visuals
  (`<kv/>`), cards (`cards/INDEX.json`), approved AI clips (`<frames/, veo/, clips/>`).
- Master script text: `<scripts/...txt>`.

## Times
All plan times are film time at 1x. The whole film gets <1.1x> in the finish. MAP.md quotes paced times; 1x = paced x <1.1>.

## Client ledger rows (generated: `client_ledger.py report <job>`; every open id must appear here or the build gate fails)
| Id | His words | Where | What we do | Block |
|---|---|---|---|---|
| L<n> | <exact quote> | <trial time / whole film> | <the fix, concretely> | <b1..b4 / all> |

Whole-film rules (type `rule`) apply to every block and are audited over the whole film before every review.

## Visual rules (ours, plus the client rules cited by ledger id)
- Show what the words say, on the line, a cut roughly every 2 to 5 s in voice-over. Every VO passage fully covered: no
  black, no spokesperson over VO, no still held over 5 s.
- Casting: <the client's rule and its exceptions with the passages they cover>. Featured people only; professionals and
  background extras are listed in SOURCES.md for the orchestrator.
- One location and one cast per story scene (a wedding is one reception, the same woman throughout, beats in order).
- Every AI picture of a person is flagged for the "Dramatization" chip.
- No em or en dashes in on-screen text. Every figure, price, date and study from the master script.
- Recurring characters: consistent illustrative footage; never present a generated person as the real person's photo.
- Stock first (Pexels free licence, Pixabay). AI only where stock cannot show the line: list it as `needs_ai` with a
  prompt and a stock fallback. Block planners never drive Chrome or Flow.
- Sound checks silent only. Heavy steps through
  `python3 "<Abs By AI>/.claude/skills/_shared/renderq/renderq.py" run --group <JOB> --heavy -- CMD`. Keep memory modest.

## Output convention
Each block agent writes only into `blocks/bN/`: `plan_bN.json` (the approved plan schema, film time 1x, exactly its block
range, a cam event for every camera span alternating CLOSE/MEDIUM, `callouts`), `SOURCES.md` (every stock id with page
URL and licence, every client image, every AI need, every person who might break the casting rule), `LEDGER.md` (each
ledger id in your block: the film time where it is handled and what you did, or why you could not), contact sheet
`plan_bN_sheet.jpg` (one thumbnail per cover shot with its time and line), `RECEIPT.md` with start and end times.

## Orchestrator decisions (apply to every block; newest last, each timestamped)
- <HH:MM> <decision>
