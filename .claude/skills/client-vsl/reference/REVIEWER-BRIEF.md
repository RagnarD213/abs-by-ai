# The fresh reviewer

A new agent for every review: `Agent` with `model: "fable"` (Claude Fable 5.2, high effort; never max), run in the
background. If Dan's Fable allowance is low, use `ra-reviewer` on Opus 5.5 high and say so. Joint Vigor ran seven: block
1, A and B (halves), then C, D, E, F on the whole film. Each took 20 minutes to 1 h 45.

**Give it:** the delivered masters (captioned and clean at the locked pace) and the SRT, their sha256 (from `gates.json`),
the master script, `STYLE-LOCK.md`, the "Visual rules" section of the blocks brief, `_shared/VIDEO-RULES.md` (headings
plus the B-roll grading, cutaway, AI disclosure, AI clip fault and scene/freeze sections), and the previous review in
full. For a narrow re-check (only after a clean whole-film review), also the previous master to diff against.

**Never give it:** the editor's receipts, fix lists, STATUS.md, TIME-LOG.md, the editor's own check sheets, or your
opinion of what is fixed.

## Prompt (fill the brackets)
> You are an independent reviewer of a client direct-response VSL, category AD, job [JOB]. You have not seen how it was
> made, and you work from your own evidence only. Review the whole film: [captioned master path] (sha256 [..]),
> [clean master path], [SRT path]. Rules: [STYLE-LOCK.md path], the "Visual rules" section of [BLOCKS-BRIEF path], the
> master script [path], and from [VIDEO-RULES.md path] its headings plus the B-roll grading, cutaway, AI disclosure, AI
> clip fault and scene/freeze sections. The previous review is [path]: verify every item in it against the new file and
> say fixed, not fixed or new problem.
>
> Check at least: container and hashes; the whole picture by full decode with an explicit BT.709 matrix (per-frame luma,
> black, flashes, isolated frames, freezes, every shot of 10 frames or fewer as a strip, first and last frame of every
> changed span, captioned against clean); contact sheets of the whole film, read by eye; one frame of every non-
> spokesperson shot against the casting rule; every AI shot of people for the "Dramatization" chip at native size; every
> story scene for one location, one cast and beats in order; every card for text in the caption band and for spelling
> against the script; the product reveal frame against the spoken word, and no product before it; spokesperson colour
> across the whole film; reuse of any shot within 90 s; captions against the SRT and a Whisper transcript of the opening;
> sound offline only (EBU R128, dropouts, the stem at every edit). Do not play audio aloud.
>
> Write [job]/asm/REVIEW-[letter].md: how you checked, what passed, every earlier item, findings as MUST (breaks a rule
> or would embarrass Dan with the client), SHOULD and NIT, each with the exact time at the locked pace, frame number,
> what is wrong and a concrete fix, then "Not verified" (everything you could not check, including that nobody
> listened), then a defect list, then one line: VERDICT: SHIP or VERDICT: DOES NOT SHIP. SHIP means zero MUST.

## After the review
- Any MUST: fix every MUST and SHOULD (or record why a SHOULD stays, for Dan), run the whole-film sweeps again
  ([GATES.md](GATES.md)), one re-finish, all gates, a NEW reviewer. Do not show Dan a DOES NOT SHIP film unless he asks.
- SHIP: Dan's page with the remaining SHOULDs listed as "For Dan's call", slot released `--review`.
- Log the review in `TIME-LOG.md` with its start, end and verdict.
