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
- **Staccato fragments (Dan, 2026-11-12: "an AI tell ... it sounds like slop").** No runs of clipped one to three
  word sentences: "Clean. Lean. No fat.", "Same workouts. 12 weeks.", "More strength. Less body fat.", "Option one.
  Keep eating...". Join them into full sentences ("They're marketed as the clean, lean choice with no fat"). This
  cuts hardest against the V Shred style, which leans on fragments; keep V Shred's structure, not its chop. A single
  short line he writes himself ("That's right. A potato.", "Same amount of protein.") is fine.

## Upsell scripts: act as the winner (Dan, 2026-11-10 and 11-11)

Post-purchase upsell videos use a different method from the VSL method above. Dan approved it after the Great Again T
upsells: "This is the way. Act as successful direct response marketers, not yourself." Model the winner's upsell
video, not Dan's VSL and not Claude's own idea of a pitch.

1. **Get the winner's video in the same funnel slot and transcribe it.** TestoGreens and V Shred post-purchase
   transcripts (12 videos): `Docs/testosterone-upsells-20261110/transcripts/` (local only, git-ignored).
2. **Outline first.** Their beats in their order, their timestamp on every section, their lines with our product
   swapped in, and a NOTE on each forced difference. Dan approves the outlines before any script.
3. **Two scripts per upsell, one per winner, shown blind** as Script 1 and Script 2 (order drawn at random, key in a
   local file). After his picks: one WINNERS doc and one REJECTED doc (he stitches parts across), then `/copy-edit`.
4. **Sell at the winners' strength.** Dan wants to be deleting lines for going too far. Calibration from the blind
   test: the hardest script was "the first time you sold aggressively enough", and he still picked the subtler one.
   Go hard on benefits, price and urgency. Do not go hard on fear.
5. **Never invent customer facts** (sales counts, refund rates, past stock-outs, testimonials). Ask Dan for real ones.

Rules from his picks on 2026-11-11 (V Shred style won the prepaid packs and creatine; TestoGreens style won Eternal
Burn and Abs By AI):

- **One warning per funnel, at most.** "I need to warn you about something" on upsell after upsell stops being
  believed. Later upsells open by congratulating him on the decision he just made.
- **Always assure him the product he bought works on its own.** The upsell gets him MORE ("you'll get even more out
  of Great Again T when you pair it with..."). Never say or imply it will not work without the upsell: Dan expects
  that to cause refunds. A different product can be sold as needed a little harder than more of the same product.
- **No obvious scare tactics.** Stock-outs and missed doses are points inside the consistency argument, made the
  subtle V Shred way, never a threat scene ("fake stockouts" was his phrase for the version he rejected).
- **More of the same product: lead with the discount.** He already bought it. The size of the saving is the pitch.
- **Assume the prospect is doing nothing.** No workout program, no diet. Never write as if he is trying and only
  lacks knowledge ("you don't know which workouts to do"), and never tell him that adding a workout and a diet will
  be "easier". Say only what he will believe.
- **Assume he knows nothing about the ingredient.** Explain what it is and what it does, sell the benefit, give the
  proof in a sentence or two, THEN reveal the product. A reveal before the benefits makes the studies read as
  pitching, and they drag.
- **Tie a complementary product back to what he bought,** point by point (the right workouts raise testosterone, the
  right food raises testosterone, sleep is when the body makes it).
- **Analogies must be ones he feels.** The water analogy landed. "The fastest route is a straight line" did not.
- Docs: outlines `1zzhHGA1qswxqzBR00OtNFzjzwiSNsXvAK7JI0T4XJto`, winners
  `1lOl-CdLLIkvMQmECAmHz2WmrHfbpDOzxMuKlTMtXRcc`, rejected `1S-3DLXHgTXrzpRyQwgcgvG0fhuZ5ZTwi6cXfR_w1XhA`. When Dan
  finishes editing the winners, diff his edits against them and add what he changed here.
- **What Dan changed by hand in the four winners (2026-11-11, 13 edits).** Write these in from the start:
  - Winner slang comes out: "cramp city" became "dehydrated and cramping", "NUCLEAR BOMB" became "an incredibly
    powerful strategy for taking your results with Great Again T to the next level", "And I'm serious" became "And I
    know this supplement is going to change your life". Keep the winners' structure, not their catchphrases.
  - Outcomes he can picture beat adjectives: "look how lean and powerful I've become" became "I look like I did in
    my twenties".
  - He adds the assurance himself wherever a line implies the product fails alone: "Other men get good results"
    gained "Still significant, but much less than the top guys"; "flush it down the drain" became "flush most of it".
  - Stock-outs get a believable, modest fact from him ("We try our best to never stock out, but we have run out of
    inventory a few times in the past") and "unfortunately, Great Again T isn't easy to make", not drama.
  - A reason that makes no sense for the product gets a real one: "if I could have fit it in one tablet" became why
    day and night need different ingredients; "your order hasn't shipped yet" (wrong for an app) became a reason
    tied to his testosterone results.
  - The guarantee is justified by results and word of mouth ("the men who stack get elite results ... you'll tell
    all your friends"), not by "they ask for MORE".
  - "The one I'd grab" became "the one most guys choose"; melatonin is listed last, as "a microdose of melatonin".
- Trap: a write hook blocks Google Doc and file writes that contain phrases Dan cuts (`HARD_PHRASES` in
  `scripts/voice/voice_check.py`). Check a long script against that list before sending it.

## Ad scripts: three styles, shown blind (Dan, 2026-11-12)

Dan after the first run: "this validates our approach of modeling three different styles of copywriting and then
choosing the winner from a blind test. This is our new way to write ads now."

1. **Dan sets up each ad in the outlines Doc** (`1i_8S6ZkMDMdh17jSYe7K4JJmPNaXwnR-tGXhXhkZYU0`). Under the ad's
   heading: his scripted opening lines in **bold italics**, normal capitalization; his outline changes in **bold
   italic ALL CAPS** below them; outline sections he does not want are struck through. Read the Doc with formatting
   (bold, italic, strikethrough) every time; he edits while you work, so write to it without a revision lock and
   only inside the ad's own section. "Write it as is" means no new intro: open on the outline's own hook lines.
2. **Three scripts per ad, one per style, each on his exact intro and only the sections he kept:**
   - **TestoGreens:** "surprising new research shows", "And the worst part of all is", "Yes, you heard that right",
     "sucking your T levels dry", "How is that possible? Because...", "But now, here's the good news", "Best of
     all", three "Imagine" lines, and the close "the man you swore you'd never become ... There is option two."
   - **V Shred:** "Here's why.", "That's why your gut keeps growing...", "This isn't about discipline", "But here's
     what's fascinating", "if there's one thing I've learned from working with that many guys", option one / option
     two, "the guy who decided this was the day things changed."
   - **Healthy Back (his own top 10 HBI ads):** credential right after the hook, "Yes, I said protein. I know.",
     "the so-called health experts", "But the FACTS are", "See, ...", "That's right - X", "most guys never connect it
     back to...", "It can really be that simple", "just one of the ... There are more like this, which most guys
     don't know about", "That's why I'd like you to watch my full video", "in simple terms anyone can understand",
     "click 'Watch Now' below", "I know that once you ..., it will change your life", "I guarantee you're going to
     be surprised", "I urge you to watch it right now ... don't procrastinate!", "I'll see you there!" Scripts and
     spend: memory `hbi-top-ad-creatives-sheet`; local copies in `Docs/hbi-top-ads-20261112/` (git-ignored).
3. **Show them blind** as Script 1, 2 and 3 on one artifact page, order drawn at random per ad, key in
   `tmp/*-blind-key.json` (git-ignored). Adding an ad to a page must not reshuffle ads he has already read. After his
   pick, reveal the styles, put the winner into the Doc under the ad's heading (model line, AD SETUP line, script),
   and log the result below.
4. **He films on green screen.** Every script carries bracketed directions for what is on screen, what he holds and
   where he points, at each important line. Before and after photos go full screen one at a time.
5. **Curiosity ads never name the replacement food unless his outline keeps that section.** L02: the script that
   named the baked potato "reduced the intrigue and desire to watch the VSL." Reveal one bad food, keep the others
   covered, and make the click the only way to learn the rest.
6. **Results so far:** L02 "3 Healthy Foods": the Healthy Back model (his "Five Foods" ad, beat for beat) was "the
   definite winner"; of the first pair he preferred TestoGreens over V Shred. L03 "1 Diet Food": TestoGreens style won over V Shred and Healthy Back. L04 "The Yolk" (30-second timer): Healthy Back style won; what he liked most was the credential moved up into the countdown with a briefer study, so a timed reveal fills its seconds with who he is plus the setup, never a long study. L05 "Healthy Breakfast" (no scripted intro): TestoGreens style won; it "transitioned from my scripted content to the outline better", and he did NOT want the credential moved up here: "save that for later, given the concept and the focus on the breakfast." So the early credential is right when the hook leaves a gap to fill (a countdown, a covered food), and wrong when the hook is a demonstration that should run straight into its proof. Tally after four ads: Healthy Back 2 (L02, L04), TestoGreens 2 (L03, L05), V Shred 0; he keeps marking the V Shred scripts down for staccato. L07 "Low-Fat Diet" (quiz CTA): TestoGreens style won again (3 of 5), for the hand-off from his lines and for opening the proof on "surprising new research shows". He rejected V Shred's "And if that sounds extreme, wait until you hear this": "I don't think it sounds really that extreme." Do not use that line unless the claim before it really is extreme; lead into proof with the research instead.

## Model

Fable 5.2 (it ranked first in the 2026-11-09 blind test and did the edits Dan rated excellent); Opus 5.5 when his
allowance is tight. Codex does not write sales copy.

## Blind testing and more training

Not done yet. The plan to grow the training set and run blind tests is
`Handoffs/handoff-20261110-dan-copywriting-training-and-blind-test.md`.
