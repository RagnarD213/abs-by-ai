# Dan's own blind test, 2026-10-10

Twenty pairs from the "today's guide" run (`2026-10-08-guide.md`): one side is Dan's real words, the other is Claude
writing the same content with the guide loaded. Dan picked the one he believed was his and said why. His full answers
are saved on the page (https://claude.ai/artifact/P7rivcXAjD9weMTyupvTfm, database `votes/`) and locally in
`voice-corpus/bench/2026-10-08-guide/blind-votes/`.

## The score

**Dan picked his own writing in 13 of 19 pairs (68%).** He was fooled 6 times and skipped one. The goal on record is
12 of 20 or fewer. The model judges, on the same kind of pairs, were right 90% of the time: Dan is a much easier judge
to fool than a fresh Claude, and about as easy as Gemini on its weakest types.

| type | pairs | right | fooled | notes |
|---|---:|---:|---:|---|
| Content, long-form (off the cuff) | 5 | 2 | 3 | fooled on Supplements (2026), the payroll-tax video (2021) and the podcast (2020) |
| Content, shorts | 3 | 2 | 0 | one skipped: he believes Claude wrote the Battle Ropes script (it has left the corpus) |
| Ads | 5 | 3 | 2 | right on all three of his own ads; fooled on both client ads (Spy Briefing 2023, HBI 2019) |
| Sales videos and letters | 3 | 3 | 0 | |
| Products | 4 | 3 | 1 | fooled on his own story in The Sex God Method (2007) |

Nineteen pairs is a small sample: the true rate could be anywhere from about 46% to 85%. Read it as "roughly two in
three", not as a pass or a fail.

He called most pairs close. On 3, 6 and 10 he said outright that he was not sure which one he wrote.

## What gave Claude away, in his words

Where he was right, these are the things he named in Claude's version:

1. **Mild, hedged phrasing where he says it straight.** Claude told the viewer they "need to get them out of" their
   life and that "maybe" they need to end a relationship; his own version says they have "got to go" and puts the
   question to the viewer directly. He called it a very Claude way of phrasing, mild and inoffensive.
2. **Words slightly too formal or too neat for him.** "Several" (twice), "reoxygenated", a "cursory" meal, a tip
   that is "flat", making something "available to more men", picking "a point between aggressive and conservative".
   His own choices are plainer: "totally broke", "share it with other guys".
3. **Word order and joins.** He would put the stronger word first in a pair, and join a reveal with "and this is".
4. **His habits Claude underuses.** "Listen" at the start of a key sentence. "Number 1, number 2" for a list.
5. **A sentence that does not quite mean anything.** One opening line read as profound and said nothing he would say.

## What fooled him

- **Old client ads.** Both misses in ads were scripts he wrote years ago for other presenters. He has less memory of
  them and less of his own voice is in them. This matches the corpus rule: client ads teach structure, not voice.
- **Off-the-cuff speech.** In all three long-form misses he reasoned from "how I talk off the cuff". Twice the version
  he took for his own loose speech was Claude's. Claude with the guide can now imitate his run-on speech well enough
  to pass with him.
- **Old writing.** The 2007 book passage was the pair he was least sure of.

## The bigger point he made (this changes Phase B)

Several times he said the real version was him rambling and **"might not be ideal for a script"**, and that Claude's
version "might be better" as a script (pairs 8, 12, 13). His off-the-cuff transcripts are the best record of how he
talks, but they are not what he wants read off a teleprompter. A script should be his words and his directness, with
order and line breaks.

So there are two different targets, and the bench so far measures only the first:

1. **Sounds like him** (the blind pairs). Baseline: model judges 90%, Dan 68%.
2. **Is a script he would read as written** (his edit rate on real drafts). Not measured yet.

And one standing complaint, repeated here: Claude is "overly cautious, overly disclaiming", afraid to go against the
status quo or be controversial, and puts safety ahead of a compelling message. Say what to do first; a caveat, if one
is needed, comes after.

## Page fix

The "what gave it away" box cut comments at 500 characters, which clipped four of his. It now takes 2,000.
