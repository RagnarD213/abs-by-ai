# RO-06 "How To Work Out At Home On A Budget": round 6, Dan's reply to the full film

**LFC (long-form content, 16:9).** Sidebar name: `Work Out At Home LFC R6`.
Written 2026-10-08 by Claude (Opus 5.5) at the end of round 5. This is the only RO-06 handoff: it replaces
`handoff-20261008-ro06-round5-full-film.md` (executed).
Read first: `Handoffs/video-editing/00-RULES.md`, `.claude/skills/longform-edit/SKILL.md`,
`.claude/skills/longform-edit/reference/ro06/README.md` (round 5 section: the traps and the tools),
`/Volumes/Extreme/_edit_work/ro06/round5/round5-record.json` (hashes, checks, open items, costs).

## State
- The full film was built and shown to Dan on 2026-10-08. **He has not replied yet. It is not approved.**
- Delivered file: `claude edited long form content/13 - How To Work Out At Home On A Budget/How To Work Out At Home On A Budget |
  claude round 5 | 16x9 | RO-06.mp4` (same file as `/Volumes/Extreme/_edit_work/ro06/round5/RO-06 round 5 - full film.mp4`),
  16:38.2, sha256 in `round5-record.json`. VLC copy: `Videos to Review/Work Out At Home LFC R5 - full film.mp4`.
- Review page: `round5/index.html`, served by `review_server.py` on the port in `round5-record.json`.
- Locked by Dan: the round 4 first minute and the four AI clips; his seven answers (hair as shot, length trim, AI product
  pictures, jump rope price as built, a quiet bed, the demo in the blue phone card, on-camera open).

## What Dan was asked (one reply box)
1. The film as a whole, with times for anything to change.
2. The two app demos P01 and P02 (new to him in this form).
3. The thirteen new cutaways C16 to C21, C23 to C27, C29, C30 (strike any).
4. Voice tone: A (as approved, audio gate fails its tone row) or B (4 dB treble shelf, passes).
5. Music bed: keep, quieter, louder or off.
6. Hair at the top edge in the closing rolls: he said leave as shot; the page tells him it is tighter than he was told.

## How to apply his reply
- **Record first:** `round6-plan/decisions.json` with his exact words, the reviewed file's sha256 and a verdict per item.
  Add the approval or rejection to the QC corpus (`_shared/qc_corpus`) with his words in the same session.
- **Voice tone B:** audio only. Add `,treble=g=-4:f=5000:width_type=q:width=0.7` to the `--eq` string in `build.render_voice`
  (or refit), run `build.py voice 0 <total> <master>`, then the audio gate. The picture file is kept. A new sha256 means a new
  watch pass: use `merge_findings.py`'s carry-over (every frame is unchanged).
- **Bed level or off:** `RO06_BED_DB` in `recipe/render5.py` (now -15), same audio-only path.
- **Strike a cutaway:** delete its line in `recipe/plan.py`, `resolve.py`, pre-flight, `render5.py`. `build.py` pins every shot
  to the reviewed render (`_R2`), so nothing else moves.
- **Picture notes:** follow the round 5 order in the README: plan edit, `resolve.py`, `from_plan.py --render`, compare the
  solve with the last `build.json`, pre-flight every clip, `render5.py`, `finish_chain5.sh`, judge only the changed strips,
  `merge_findings.py`, the gate, `page5.py`.
- **If he approves as is:** set the queue to `finalized`, run `roll_sidecar.py mark-used` for every piece in `edl.json`,
  register the four AI clips and the stock clips used in the clip library (`--status used-final --used-in "RO-06"`), delete
  this video's copies in `Videos to Review/`, stop the page services (`review_server.py PORT --remove` for 8846 to 8849 and
  the round 5 port), delete the board entry, and write the `/video-setup` handoff (thumbnails with Codex, AI flag TRUE at upload,
  Sunday-only release slot).

## Open items a reviewer will raise again (all told to Dan on the page)
- Audio gate: tone row fails (5.5 kHz +6.1 in the 20 to 140 s window) with the chain he approved. Not the bed.
- Watch pass: 9 open findings (hands out of the top at 8:59 and 11:23, lower third over his stomach at 1:19 and 13:34, the
  word gap in two-part lower thirds). Hair findings are accepted in his words.
- Delivery gate: FAIL (rows in the notes file). Coverage reads 34 % against 40 %.
- The lower-third template word gap is a separate task (shared template); when it lands, re-render this film's lower thirds.
- Neither independent review returned SHIP; the second ran on the third render and its four fixes are in the fourth.

## Budget
$5 per video for AI clips. **Spent: $2.43.** Round 5 spent $0.

## Next action
Wait for Dan's reply on the round 5 page, then apply it as above. Recommended: **Claude Opus 5.5, high** (medium if he
approves as is and only the close-out is left).

## Starter prompt
> Read `Handoffs/handoff-20261008-ro06-round6-dan-review.md` and execute it with /longform-edit. This is RO-06 "How To Work Out
> At Home On A Budget", long-form content (LFC); name this task `Work Out At Home LFC R6`. My reply to the round 5 full film:
> [paste the reply box from the review page here]
