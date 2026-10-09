# RO-06 "How To Work Out At Home On A Budget": round 7, apply Dan's reply to the round 6 full film

**LFC (long-form content, 16:9).** Sidebar name: `Work Out At Home LFC R7`.
Written 2026-10-09 by Claude (Opus 5.5) after round 6 was shown to Dan. It replaces `handoff-20261009-ro06-round6-revisions.md` (executed).
Read first: `Handoffs/video-editing/00-RULES.md`, `.claude/skills/longform-edit/SKILL.md`,
`.claude/skills/longform-edit/reference/ro06/README.md` (round 6 and its second pass: the tools and every trap),
`/Volumes/Extreme/_edit_work/ro06/round6/round6-record.json` (hashes, checks, what changed),
`/Volumes/Extreme/_edit_work/ro06/round6/ROUND-6-REVIEW-2.md` (the independent review of the delivered file: SHIP).

## State
Round 6 delivered 2026-10-09: `round6/RO-06 round 6 - full film.mp4` (16:38.2, sha256 `258bf122...ba563b`), page
http://localhost:8851/index.html, VLC copy `Videos to Review/Work Out At Home LFC R6 - full film.mp4`, delivery folder
`claude edited long form content/13 - How To Work Out At Home On A Budget/`. **Not approved: wait for Dan's reply. Record his
words and the reviewed hash in `/Volumes/Extreme/_edit_work/ro06/round7-plan/decisions.json` before building anything.**

## What round 6 built (do not reopen unless he does)
1. 3:51 jump rope: the fast skip, roll C1674 from 101.8 s (`round6/c06/`).
2. 9:24 framing: shots mb2.0r0, r1 and r2 on a taller canvas (`recipe/mb2_fix.py`), one 1600x900 crop with 52 px or more above his hair;
   the toe-touch cutaway C12 starts on "because it's a little bit more ergonomic".
3. 11:23 mic: `lav.round6.wav` (`recipe/audiofix6.py`); the build reads it through `RO06_LAV` (set in `render6.py`).
4. 15:44: P03, Dan moved 290 px right with the phone on the left third (`recipe/phone_side.py`, captures from `recipe/appcap6.py`).
Also: every lower third re-rendered with the word-gap fix; G04, G15, G22, G25 two-part again; the 2026-10-09 capitals rule applied outside the
approved first minute (five punch words kept: G06, G17, G21, G26, G29).

## Questions on the page he may answer
- The mic at 11:23 by ear (fine, still hears it, or cut the sentence).
- The slightly flat top of his hair at 9:28 to 9:32 and 9:40 to 9:47 (accept, or cover with B-roll).
- The cut at 15:34.13 (cav2b.0 to cta.0r0, both the camera frame, his head jumps 84 px): a cutaway over it, or one side at another size.
- Capitals: the five kept words, and "No COMMUTE." at 0:55 inside the approved first minute (left as approved).
- Voice tone A or B, the bed, hair at the top edge elsewhere, P01 and P02, the other cutaways: all as built.

## If he approves as is
Follow "After Dan finalizes the film" below. No render.

## If he asks for changes
- Pin every shot to the round 6 film first: point `_R2` in `recipe/build.py` at `round6/RO-06 round 6 - full film.mp4.build.json` and keep the
  `MB2` shots out of the pin only if their crop changes.
- Small things worth folding into any new render: `GRAIN = 0.8` in `mb2_fix.py` (1.6 reads 3 to 4 times busier than the live picture);
  the first minute's "No COMMUTE." only if he says so.
- A lower-third text change: edit `recipe/plan.py`, `resolve.py`, then `hyperframes/from_plan.py --render` (only changed ones re-render).
- Then: `render6.py` copied to `render7.py` and pointed at `round7/`, `finish_chain6.sh` likewise, `merge6.py split` against round 6 for the watch
  pass (carry verdicts for unchanged strips), one fresh `ra-reviewer` on the final file, edit sheet, delivery gate, page (`page6.py`,
  `page_text6.py`), VLC copy replaced, queue `delivered`.
- Never raise a bound. The audio gate's tone row fails with the chain he approved; the delivery gate reads 29 pass, 10 fail (`round6/logs/gate.log`).

## Budget
$5 per video for AI clips, retries included. **Spent: $2.43.** Past $5: stop and tell Dan first.

## After Dan finalizes the film
Queue to `finalized`; `roll_sidecar.py mark-used` for every piece in `edl.json`; register the four AI clips, the stock clips and the new
jump rope cut (`round6/c06/C06-fastskip-C1674-101.8.mp4`) in the clip library (`--status used-final --used-in "RO-06"`); add the approval to
the QC corpus with his words; delete this video's copies in `Videos to Review/`; stop the page services (`review_server.py PORT --remove`
for 8846 to 8851); delete the board entry; write the `/video-setup` handoff (thumbnails with Codex on the subscription, AI flag TRUE at upload
because the film holds AI video clips, the next free Sunday slot).

## Next action
Wait for Dan's reply to the round 6 page, record it, then act on it. Recommended: **Claude Opus 5.5, high** (medium if he approves as is).

## Starter prompt
> Read `Handoffs/handoff-20261009-ro06-round7-dan-review.md` and execute it with /longform-edit. This is RO-06 "How To Work Out At Home
> On A Budget", long-form content (LFC); name this task `Work Out At Home LFC R7`. My reply to the round 6 film is: [paste the reply box
> from the page here]. Use the Codex subscription for any still image. Run every check and one independent review, show me the film
> again with only what changed, then stop.
