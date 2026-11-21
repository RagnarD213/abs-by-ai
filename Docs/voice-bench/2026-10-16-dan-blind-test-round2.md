# Dan's own blind test, Round 2 (answers 2026-10-16)

Twenty pairs from the `set5` run (real passages first, no rules), all from the half of the hold-out set Dan had not
seen. Page: https://claude.ai/artifact/QbzMfnMzQzNsrGDxCyRydK . His picks are saved locally in
`voice-corpus/bench/2026-10-10-set5/blind-votes/`.

## The score

**Dan picked his own writing in 17 of 20 pairs (85%).** He was fooled 3 times. The goal is 12 or fewer. Round 1
(the old guide, the other 20 passages) was 13 of 19 (68%).

| type | pairs | right | fooled |
|---|---:|---:|---:|
| Content, long-form (off the cuff) | 7 | 4 | 3 |
| Content, short | 1 | 1 | 0 |
| Ads | 5 | 5 | 0 |
| Sales scripts and letters | 3 | 3 | 0 |
| Products (books) | 4 | 4 | 0 |

The two rounds used different passages, so 68% against 85% is not a comparison of methods. On these same 20
passages the model judges caught the old guide's drafts 38 times of 40 and the `set5` drafts 33 of 40: the new
method did better on them, and they are harder passages for Claude than Round 1's. Dan caught every written piece
(13 of 13). All three times he was fooled it was off-the-cuff speech, the type the bench also says moved most.

## What gave Claude away, in his words

1. **Softened language. He called it one of the biggest Claude tells.** Claude writes the polite word where he
   writes the blunt one: "unattractive" and "severely overweight" for his "ugly" and "grossly obese"; "overstated"
   for his "exaggerated (lied)"; "they're going to love you" for his "worship the ground you walk on". He reads it as
   Claude being afraid to offend: avoiding the manosphere point of view, holding back from calling a woman ugly or
   using "slut" and "whore" where his book does, defaulting to a feminist frame.
2. **Weak direct-response language.** His version has the colourful sales words: "whopping 50% savings", "BLOWN
   AWAY" in capitals, "the pounds melt off", "a single cent", a faster metabolism. Claude
   writes "weight comes off" and "spend any money at all". He wants this corrected, not imitated.
3. **Caring about minor ethical points.** Claude framed his own lie about his income as "overstated"; he would say
   he lied, plainly, and end the line with an exclamation mark. CAPITALS on the key lesson are his.
4. **The exception: compliance on disease claims.** On the arthritis ad he picked the version with careful
   wording ("significant pain relief", "difference in your symptoms") because disease claims are a sensitive
   Google Ads category. For six-pack abs he is not worried about it.
5. **Off-the-cuff is not his script.** On five long-form pairs he repeated that this is extemporaneous speech from
   an outline and not how he wants a script written.

## A finding behind point 1: the bench put the soft words there

Checked after his answers: in every pair he flagged for softened words, the soft word came from the bench's own
content brief, and the writer copied it. The brief is written by Claude "in neutral, plain wording" so the writer
cannot copy the real passage; that rule turned "ugly" into "unattractive", "lied" into "overstated", "a single cent"
into "money". So part of this tell is a fault in the test, and part is real (the brief writer is Claude, softening).
In real use the writer gets his own outline wording, which keeps his words, but any content plan Claude writes in
between can soften them the same way.

What follows:

- **Real use, now:** a content plan must carry his exact words for every claim and label, the strong ones most of
  all. Never neutralize them in the plan. (Added to `DAN-VOICE.md` and the `dan-voice-writer` agent.)
- **Bench, before Phase C:** rewrite the brief rule so it keeps the strength of every claim and the bluntness of
  every label (single charged words allowed, still no 4-word runs), re-brief the 40 passages, and re-score `guide`
  and `set5`. Every later score uses the new briefs.

## Corpus question for Dan

Pair 8, the "Five Levels Of Pushups" short: he thinks Claude wrote that script, so both sides were Claude. Logged in
`Docs/DAN_DECISIONS.md`. If he confirms, it leaves the corpus and the hold-out set the way Battle Ropes did after
Round 1.
