# Dan's voice: the core (what is true of him in every type)

Source: 88 pairs where a fresh Claude wrote the same content as a real passage of Dan's
(`Docs/voice-bench/2026-10-10-contrast.md`), the judges' reasons on the bench, and Dan's own notes on his blind test
(2026-10-10). Each line is a gap that showed up again and again, most frequent first. The real passages you were
given outrank every line here: when a passage and a line disagree, follow the passage.

**Not for a writer's prompt.** Tested 2026-10-10: a writer given real passages plus these notes was caught 92% of
the time, against 82% with the passages alone. Use this to review a draft or to understand a verdict; the draft
itself comes from `dan-voice-writer` (`DAN-VOICE.md`).

Strength: **HARD** = never break. **STRONG** = true of most of his pieces. **LIGHT** = a habit, used sparingly.

## The one idea

Claude gets caught two ways. Writing as itself it is too clean: even sentences, varied wording, neat structure.
Trying to sound casual it puts on a costume: fragments, "right?", "honestly", "you've got", "man". Dan is neither. He
is **plain, direct and a little formal, in full sentences, and he repeats himself.**

## What he does (STRONG)

1. **Full sentences with a subject and a verb.** He does not break a point into fragments for punch ("None." "A lot
   cheaper." "Fine."). The point sits inside one sentence.
2. **He goes straight to the point.** No signpost before it ("Here's the thing", "Here's the deal", "Here's why",
   "The reason is simple", "Now look", "Bottom line"). No tag after it ("right?", "okay?", "you know?").
3. **He states a claim flat.** No sincerity marker or softener in front ("honestly", "basically", "pretty much",
   "I mean", padding "actually") and no stacked intensifier ("every single", "at all", "very first", "right now"
   for "now"). His own intensifier is "very" (Claude underuses it) and, in speech only, "really" about twice per
   1,000 words (Claude uses double that).
4. **He repeats the full name of the thing, and the same verb.** Where Claude writes "it", "them", "this" or finds a
   synonym on the second mention, he says "the book", "the ab wheel", "your Zepbound" again, sentence after
   sentence. One verb does the job all the way through ("I'll show you... I'll show you... I'll also show you").
5. **Plain words, a notch formal, never slang.** "I have" and "you have", not "I've got" (Claude says "got" six
   times as often). "Going to", almost never "gonna" (Claude: ten times his rate). In written copy "I'll",
   "you'll", "will", "you need to", "many". "Reduce", "consume", "excessive", "tremendously", "difficult". Not
   "bucks", "a ton", "crank up", "dude", "stuff". And not the literary neat word either: "a few" or "many", never
   "several"; no "cursory".
6. **A linked thought stays in one sentence**, joined with "because", "since", "so", "and" or "but". Claude cuts
   it into two or three short ones. His sentences are uneven: several long ones, then a short one. The checker
   (`scripts/voice/voice_check.py`) holds the band for his spread; stay inside it.
7. **Blunt, and the instruction comes first.** He tells the viewer what to do and names the problem by its plain
   name. A caveat, if he gives one, comes after and is short. He does not say "maybe you need to".
8. **Loose grammar stays loose.** A number that does not agree, a sentence that restarts, a dangling "with" at the
   end. Do not repair what he would not notice.

## What he does sometimes (LIGHT: once in a piece at most, and never required)

- "Listen" or "Look..." before the one sentence that matters most.
- "Number one... number two" to say a list out loud.
- One word in CAPITALS for stress in written copy. An exclamation mark on an offer or a sign-off.
- "..." for a spoken pause and " -- " for an aside in written copy.
- "Now," or "So" to turn to a new section. Not on every sentence.

## Do not perform him

No habit above is ever required. A piece with none of the LIGHT habits is fine; a piece with one in every paragraph
is a costume, and readers catch a costume faster than they catch clean prose. Never add filler, a stumble or a swear
to make a draft "sound spoken". Where a number is below his band, bring it into the band, never past it.

## HARD rules

- No em dash and no en dash, anywhere.
- No phrase from the hard list in `voice_check.py` ("Let's be honest", "Honest answer.", "This is that video",
  "Here is the uncomfortable truth", "quote unquote", "to be fair,").
- His girlfriend is never "my wife". No fact, number, opinion or story he did not give: use
  `voice/POSITIONS.md`, ask him, or leave a `[DAN: ...]` gap.

## A script is not a transcript (Dan, 2026-10-10)

His off-the-cuff speech is the best record of his words, but he does not want a ramble on the teleprompter. For a
script: his wording, his plain words and his bluntness, in order, with line breaks. Imitate the run-on only when
the job is to write what he would say off the cuff.
