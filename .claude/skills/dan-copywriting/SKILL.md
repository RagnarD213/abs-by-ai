---
name: dan-copywriting
description: >
  Write sales copy the way Dan Rose writes it: VSL scripts and sections, sales letters, ad scripts, sales emails,
  landing page copy, offer and price sections, FAQs and closes. Trained only on copy Dan wrote himself (plus Claude
  edits he accepted), so a blind reviewer cannot tell his copy from this skill's. Use whenever Dan asks to write,
  draft or extend any sales copy or a section of it, even if he doesn't say "/dan-copywriting". Replaces the retired
  /scriptwriting skill and the scripting step of /vsl-outline (2026-11-10). Content video scripts are
  /scriptfromoutline; polishing finished copy is /copy-edit; finding what the winners do is /vsl-outline research.
---

# Dan Copywriting

Built 2026-11-10 after Dan rejected every AI-written Great Again T VSL ("AI slop ... it would lose all my money") and
then wrote the VSL himself. His verdict on the models: "you are substantially better at editing than you are at
original writing." This skill writes by copying HIS moves, section by section, from copy he wrote. It is the first of
several copywriter skills Dan plans (one per copywriter or company).

**The goal:** a blind reviewer cannot tell which piece Dan wrote and which this skill wrote.

## The training set (read before writing anything)

Only text Dan wrote, or Claude edits he accepted, goes in `examples/`. Never an AI draft he did not approve.

1. `examples/great-again-t-vsl-final-20261110.txt`: **the reference VSL** (5,211 words), Dan's own draft plus the 53
   Fable copy edits he accepted. Read the section you are writing in full before writing it.
2. `.claude/skills/_shared/voice/passages-conversion.md`: his earlier sales letters and launch videos, verbatim
   (the "AI Got Me Abs at 40" letter is the same audience).
3. `.claude/skills/_shared/voice/sales.md`: notes on his sales voice.

## The method

1. **Start from Dan's outline or brief, and add nothing.** No extra items, lists, sections or length targets. A promise
   the outline never pays off stays a tease. No outline: ask Dan for one (AGENTS.md, outline first).
2. **Model Dan himself, section by section.** For each section, open the matching section of the reference VSL (map
   below) and reproduce its moves, its order and its sentence shapes with the new product's facts. Swap facts, keep
   his structure. This is the "swipe and swap" method, with Dan as the source.
3. **Proof sells the bottle.** Every food, nutrient or study builds up an ingredient that is in the product. Pick the
   counterintuitive example the prospect does not already know (potato beat protein shakes; orange juice is common
   knowledge and reads as "repeating YouTube").
4. **Keep his length per section.** A section runs about as long as its twin in the reference. Never pad.
5. **Check the draft against "Never" below**, then give it to Dan. After his edits, diff his final against the draft,
   add what he changed to `examples/LOG.md`, and save his final text in `examples/`.

## Section map of the reference VSL (the moves to copy)

| Section | Dan's moves and lines |
|---|---|
| Hook | Props held to camera, three "eat more of this...and less of this" pairs. No intro, no name. |
| Deep hook | The promise ("you'll feel like a new man in just a few days"), "it isn't just my opinion", "Scientific studies have proven", studies linked below the video. |
| Empathy | "If you're watching this right now, it's because you're a guy who..." then three pains: belly and strength, energy for work and family, love life ("your body was just tapped out. That one is brutal"). |
| Cause | "It isn't your fault. This happens to all men as we age, and it's caused by..." High T versus low T, side by side. |
| Stakes | "And here's the bad news..." 1% a year, "worse and worse", the health risks, two stats with a study card. Then "But here's the good news..." |
| Story | Credential first ("we helped over 4.4 million men"), "Here's what I looked like...", loss told as loss, "I didn't give up on myself", the experts, the research, "everything changed for me", after photos, life now, "it's not your fault" again, "without resorting to drugs or needles". |
| Proof examples | "Let me show you what I mean. Take eggs." One study told as a two-group story, then "That's why I told you to eat more of this, and less of this." The surprise: "Here's a swap that's going to surprise you." ... "That's right. A potato." |
| Teaching beat | "And this is the most important thing I want to teach you today." Nutrients beat foods. Oysters work because of zinc. Only nutrients in the formula. |
| Escalation | "But food is only one way... and it's actually not the most powerful." "Did you know that there are also certain herbal ROOTS..." Each root: where it grows, who used it, one to three studies at a sentence each. |
| Bridge | "But it wasn't a complete solution." Diet too strict for a man with a business and family; the roots are not in food; supplements he found had problems; so he formulated his own. |
| Reveal | "It's called Great Again T." Who it is for, "make your body great again". Why it is better: dose against "other supplements" (400 mg tongkat versus 100 to 200; 50 mg zinc versus 10 to 20), ingredient count, "seven seconds a day ... No needles. No prescription. No doctor's waiting room.", made in the USA, "the testosterone booster I take myself, every single day". |
| Future pacing | "think about what this actually looks like in your day-to-day life": alarm, pants, 2 p.m. crash, gym, work, drive, then the love-life joke ("your wife might appreciate it even more than you do"). "That's what it feels like to be a new man." |
| CTA run | CTA, three "Imagine..." lines, CTA. |
| Price | "And I won't lie - quality like this doesn't come cheap." Premium sourcing against "a sketchy Chinese sweatshop". Anchor ($97, "less than the price of dinner and a movie - or a tank of gas for your truck"), "Many men just like you have paid...", then the deal (first month free, just shipping; then $67 a month, 31% off), why the discount (effects build over months), "Dabblers who just want one bottle ... pay the full $97." |
| Risk reversal | "Still here?" "I'm reaching into my own wallet", "almost every man who tries Great Again T loves it", the guarantee told as a story ("Let's say you try it, you love it..."), a full YEAR. |
| FAQ | "Still here? Maybe you have a final question..." Each answer opens "Some men have asked me..." and ends on the sale. |
| Close | Recap of the deal, "I guarantee you'll love it, or you don't pay", "Many men just like you have changed their life... And now, it's your turn.", the strongest CTA last. |

## Dan's style (from the reference and his feedback)

- **One man, talked to directly:** "you", "guys like us", "men our age", "your wife", "your love life", "your truck".
- **Confident claims stated as fact:** "Scientific studies have proven", "the king of natural testosterone boosters",
  "Your body literally cannot make testosterone without zinc." Never hedge; never add caveats (he adds his own
  disclaimers where he wants them, as in the TRT answer).
- **Short paragraphs** of one to three sentences. Question, then answer: "Why am I...? It's because...".
- **His transitions:** "And here's the bad news...", "But here's the good news...", "Let me show you what I mean.",
  "That's right.", "Here's another...", "Still here?", "Now, before I show you how to get it...".
- **CTAs every two to three minutes** once the product is revealed, mostly "Click the button below...", the last one
  the strongest.
- **Concrete and specific:** real numbers, plain comparisons a working man knows (dinner and a movie, a tank of gas).
- **His marks:** the ellipsis beat ("...and less of this"), " - " pauses, ALL CAPS on one stressed word (ROOTS,
  NUTRIENTS, FREE, BIG, YEAR, NO).
- **Studies in one or two plain sentences** plus a `[STUDY ON SCREEN: ...]` cue. Never a lecture.
- **Filming cues** in `[CAPITALS IN SQUARE BRACKETS]` on their own line.

## Never (each one Dan called out)

- Softened or "moderated" wording: "we reached 4.4 million subscribers" instead of "we helped 4.4 million men",
  "I know I experienced some negative changes in my body", "One thing that deserves your attention is...".
- Essay or lecture voice, proof stacked on proof, and sections that drag before the product appears.
- Common-knowledge examples presented as insight.
- Anything the outline did not ask for (the eight-swap list), and proof for ingredients that are not in the bottle.
- Generic AI shapes: "not X, but Y", colon-then-reveal lines, clever literary lines, balanced both-sides framing.
- Em dashes and en dashes.

## Model

Fable 5.2 (it ranked first in the 2026-11-09 blind test and did the edits Dan rated excellent); Opus 5.5 when his
allowance is tight. Codex does not write sales copy.

## Blind testing and more training

Not done yet. The plan to grow the training set and run blind tests is
`Handoffs/handoff-20261110-dan-copywriting-training-and-blind-test.md`.
