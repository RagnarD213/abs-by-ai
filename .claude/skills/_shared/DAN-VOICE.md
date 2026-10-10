# Dan's voice: the method

Read this before anything goes out under Dan's name. Rebuilt 2026-10-10 (Dan Voice P2B) from a blind bench, not
from reading. The first guide (2026-10-06) was a list of rules; its structure sections now live in
`voice/STRUCTURE.md`.

## The finding that drives everything

On the bench, a fresh Claude writes the same content as a held-out real passage of Dan's, and two judges (a fresh
Opus and Gemini) pick which one is the AI. Chance is 50%. The goal is 60% or less.

| what the writer was given | caught | kept? |
|---|---:|---|
| nothing (cold Claude) | 86% | floor |
| the old guide: rules plus examples | 91% | no |
| **5 whole real passages, no rules (`set5`)** | **82%** | **yes: this is the method** |
| the same 5 passages plus voice notes (`voice/CORE.md` and the type notes) | 92% | no: notes made it worse |
| the 5 passages, then a critic and checker revision pass | 82% | no: no change |
| 12 passages instead of 5 | 80% | no: inside the noise, costs more |
| the 5 passages, Fable as the writer | 81% | no: the model does not matter |
| worked pairs (brief, Claude's version, his version) | 86% | no |

Reports and the ledger: `Docs/voice-bench/`. Three things follow.

1. **Rules make Claude tidy, and tidy is what gets caught.** Every time voice rules went into the writer's prompt
   the score went back to 91 or 92%. Real passages with nothing else is the only thing that moved it.
2. **The writer must be clean.** A session that has read this file, a writing skill and the project rules is the
   losing condition. The words are drafted by a separate call that sees only his real text and the content plan.
3. **Prompting has a ceiling.** The hard judge (Opus) still catches 39 of 40. For the pieces that matter most, the
   answer is his own words first (Lane 1), not a better prompt.

## How to write as Dan

| lane | use it for | how |
|---|---|---|
| 1. His words first | website sales videos and letters, personal posts, anything read by people who know him | He records a 3 to 5 minute take; `/dan-voice` ASSEMBLE orders and cuts it; 80% of the sentences stay as said |
| 2. Continue from his text | scripts, descriptions, captions, ad copy, lessons | the steps below |

**Lane 2, every time:**

1. **Settle the content with the skill that owns the piece** (`/scriptwriting`, `/scriptfromoutline`,
   `/shorts-scripting`, `/ad-copy`, `/ad-outlines`, `/copy-edit`, `/youtube-packaging`). Hooks, order, proof, the
   offer and the close come from that skill and `voice/STRUCTURE.md`. The result is a **content plan**: what the
   piece is, who it is for, every point, fact and number in order, the ask, the length. No style words in it.
2. **His take, his story, his number:** from the outline, or `voice/POSITIONS.md`. Not there: one question to Dan
   or a `[DAN: ...]` gap. Never invented.
3. **Hand the plan and his own outline wording to the `dan-voice-writer` agent.** It runs
   `python3 scripts/voice/write.py`, which picks 5 real passages from `voice/bank/` by format and length (never by
   topic), puts them first, then his own wording as the seed, then the plan, and asks a clean Opus for "the next
   piece in this set".
4. **Do not polish what comes back.** Fix a wrong fact, a missing point or a hard-rule hit in that sentence. Do not
   smooth, vary, tighten or tidy: each of those moves the draft toward what judges catch.
5. **Structure checks stay with the owning skill** (length for a Short, cue format, the offer wording, claims
   rules). They are checks on content and format, not a licence to rewrite the sentences.

## Types and formats (what the bank holds)

| type | formats | his material |
|---|---|---|
| content | `video` (off the cuff), `video-business`, `podcast`, `short` (he writes these), `script` (teleprompter; see below) | 33 passages |
| ads | `ad-own` (he reads it), `ad-client` (another presenter: structure, not voice) | 20 |
| conversion | `sales-script` (written), `sales-video` (him reading his script) | 18 |
| products | `book`, `book-business`, `lesson` | 20 |

`python3 scripts/voice/bank.py list` shows it; `bank.py pick` returns passages. Each bank passage has a twin in
`voice/contrast/`: the same content written cold by Claude. Those pairs are where the gap list came from.

**A script is not a transcript (Dan, 2026-10-10).** His off-the-cuff speech is the best record of his words, but he
said several times that it "might not be ideal for a script" and that he does not want a ramble on the
teleprompter. For a long-form script use `--format script`: the writer gets his written shorts and an ad of his own
for the script register, and two video transcripts for his wording. This mix has not been scored: the bench has no
long script wholly written by him to test against. The measure for scripts is his edit rate (words he changes),
starting with the 10/17 shoot scripts.

## Hard rules (checked by a hook and by `voice_check.py --hard`)

- No em dash and no en dash, in anything.
- None of the phrases Dan has cut: "Let's be honest", "Honest answer.", "This is that video", "Here is the
  uncomfortable truth", "quote unquote", "to be fair,", "I know how that sounds".
- His girlfriend is never "my wife". No invented fact, number, opinion or story.
- Swearing: `voice/profanity-and-controversy.md`. Never cut his own; never add one for colour.

## What the notes and tools are for

- **`voice/CORE.md` and `voice/type-*.md`:** the gap list in plain words (what Claude does that he does not, with
  counts and rates). For people, for reviewing a draft, and for understanding a judge's verdict. **Not for the
  writer's prompt:** tested, 92% against 82% without them.
- **`scripts/voice/voice_check.py`:** hard rules, plus a score of how far a draft's numbers sit from his bands
  (fitted on his text against Claude's drafts). A tripwire and a diagnosis. Revising a draft until its numbers sat
  inside his bands was tested: the numbers improved and the judges did not notice.
- **`dan-voice-critic` agent:** marks what gives a draft away. It called 29 of 40 drafts "would pass" that the
  judges then caught, so a pass from it means little. Use its marks as a second read on request (`/dan-voice`
  CHECK), not as a gate.
- **`voice/STRUCTURE.md`:** how he opens, proves, builds a mechanism and closes; what he cuts from Claude drafts.
- **`voice/POSITIONS.md`:** his takes and stock stories with sources.
- **`voice/HELD-OUT.md`:** test passages that must never be quoted anywhere in these files
  (`python3 scripts/voice/heldout_guard.py` after editing any voice file).
- Older example files (`voice/ads.md`, `sales.md`, `content-*.md`, `book.md`, `passages-*.md`, `outlines.md`,
  `dan-edits-2026-10-06.md`, `borrowed-keith-wes.md`) stay as reading for building a content plan. The bank
  replaces them as what a writer is shown.

## Changing this method

Add a setup to `scripts/voice/bench_setups.json`, run `python3 scripts/voice/bench.py run --setup <name>`, compare
with `bench.py compare 2026-10-10-set5 <run>`, and keep the change only if the number moves beyond the noise (about
8 trials in 80). Then a fresh blind page for Dan (`bench.py blind --setup <name> --fresh`). Only his own text goes in
the bank: nothing Claude drafted counts as his voice, even after he edits it.
