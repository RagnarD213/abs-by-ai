# VSL script contest result and lessons (Great Again T, 2026-11-10)

For every model that writes sales copy for Dan: Claude (Opus, Fable, Sonnet), Codex and any other AI. Read this before writing any VSL, sales video, ad script or sales page copy.

## Result

Blind contest, 2026-11-09: three writers scripted Dan's own Great Again T outline from one shared brief. Dan read all three unlabeled.

| Blind label | Writer | Dan's rank |
|---|---|---|
| Script 3 | Claude Fable 5.2, extra-high effort | 1st |
| Script 2 | Claude Opus 5.5, extra-high effort | 2nd |
| Script 1 | Codex GPT-6 Astra, extra-high effort | 3rd, "by far the worst ... awful" |

**None is acceptable to ship.** Dan: "If I shipped any of this stuff, then I would lose all my money. The business would end in disaster." He plans to write most of the VSL himself and lift a few strong sections from Script 3. The scripts, brief and outline: `Handoffs/great-again-t-20261105/contest2/` (Script 1 = `w2/`, Script 2 = `w1/`, Script 3 = `w3/`).

## Dan's feedback (his words, 2026-11-10)

> Script 1 was by far the worst. This was awful. Even in the parts in the beginning where I essentially wrote the rough draft, it took out language that was good and replaced it with weaker language. The language sounds like AI slop. "I know I experienced some negative changes in my body." That's not really how a human would speak.
>
> I found some more examples here. One thing that deserves your attention is a process called age-related testosterone decline. That's just never a sentence that would appear in a VSL or Testogreens vs. [V Shred]. This is just AI slop language. This is not appropriate for a VSL.
>
> Another example: "My story. Moderate the language." With my first YouTube, we reached over 4.4 million subscribers, rather than "we helped." No reason to moderate like that. The VSL scripts, for script 1 or actually all these, just drag.
>
> The most catastrophic decision was the decision to go against my outline and to do 8 examples. I would say scripts 2 and 3 are better, but the biggest problem with each of them is that you went against my outline. The VSL scripts all drag. It just goes on endlessly with examples of the foods, and people probably don't even make it past foods. They don't even know that we have a product for sale.
>
> The sections also don't really tie well together in VSL 1. They're better in 2 and 3, but the transitions, especially in 2, are clunky. Of the three, I liked Blind Script 3 the best. The language, I thought, sounded the most natural. The transitions between sections were the smoothest.
>
> One thing I liked in VSL 3 was the example of the potato versus the protein shake. I thought that was very counterintuitive and something that the prospect would perceive as valuable. It contrasts with Blind Script 2, which chose to use orange juice versus water. Not counterintuitive, something the prospect already knows. Not valuable. Sends them the impression we're just repeating general knowledge that we found on YouTube rather than delivering good insights. That was one way that VSL 3 was superior to VSL 2.
>
> The strongest parts of VSL 3, I think, are the ingredient and nutrient breakdowns. The transition between those sections, though, needs improvement. It's still not good enough to ship.
>
> My rankings overall: 3 is the best, then 2, and then 1, but none are acceptable to ship.

## Why every model failed

1. **The brief broke Dan's outline first (Claude's error).** It added eight food swaps (his outline asked for the egg example plus one more), a 4,500 to 6,000 word target, a selling checklist and a cautious studies pack. All three writers obeyed, so all three dragged and buried the product. A writing brief carries Dan's outline and the model passage only.
1b. **The research pack promoted nutrients that are not in the formula (Claude's error).** Claude asked the research agent to verify "zinc, vitamin D, magnesium, boron, dietary fat" because testosterone research names them most, not because Great Again T contains them. The brief said to use only pack claims, so all three scripts built a five-nutrient section around two nutrients the product does not have (vitamin D, magnesium) and one a tablet cannot deliver (fat). Dan: the section's purpose was to promote our formula. Every proof section must set up an ingredient that is in the bottle, as the winners do; research is chosen to sell the product, not by strength of evidence alone.
2. **AI explains instead of selling.** Handed a pile of studies, every model turned each section into a lesson, proof after proof. A VSL needs just enough proof to believe, then the offer. Models do not know when to stop.
3. **AI rewrites strong human lines into weak, safe ones.** Training pulls toward polite, balanced, hedged wording ("One thing that deserves your attention is...", "we reached 4.4 million subscribers" instead of "we helped"). Script 1 did it most. A "sell, don't hedge" instruction does not reliably override it, least of all next to a studies pack full of cautions.
4. **AI cannot tell what the prospect already knows.** The studies pack ranked swaps by strength of evidence; sugar has the strongest evidence and is common knowledge, so Script 2 picked orange juice. Fable went outside the list and found the potato. "Counterintuitive and valuable to this man" is a judgment about the prospect's mind; ask for it explicitly as a menu ranked by surprise, and let Dan choose.
5. **AI writes sections as separate blocks.** Given headings, each model filled each heading; transitions became generic bridges ("Now, ..."). Flow needs a writer holding the whole argument.
6. **AI fills whatever space it is given.** A word target becomes padding.
7. **AI judges cannot catch any of this.** AI "operator panels" rated earlier Claude scripts top 10%; Dan called them awful. Only Dan's read and real traffic decide.

## The approach (adopted by Dan, 2026-11-10: "Adopt it")

1. **Dan writes the spine:** hook, story, transitions, offer, close. AI never writes a whole VSL.
2. **AI gets small, fenced section jobs, one at a time:** the section's exact place in Dan's draft, his last line before it and first line after it (so it joins), a word cap, the winner's matching passage, the allowed facts, nothing else. Good jobs: ingredient breakdowns, nutrient breakdowns, price math lines, study-card text, on-screen directions, Q&A answers.
3. **Swipe and swap for body sections Dan wants modeled closely:** take the winner's exact passage and change only what must change (product, ingredient, numbers), keeping their sentence shapes, shown side by side with the original.
4. **AI scouts ideas; Dan decides:** for judgment calls (the surprising food swap, hook angles), AI gives a menu of about 10 options, each with its study and an honest "would a 45-year-old guy already know this?", and Dan picks.
5. **AI line-edits Dan's draft only on request:** tighten, fix one clunky transition, three alternatives for one line. Never rewrite his sentences unasked.
6. **Model for section jobs: Fable 5.2** (won this blind test), Opus 5.5 second. Codex does not write sales copy.
7. **Fact check is a separate pass afterward** that flags only false statements and never softens the copy.
8. **Traffic is the real judge:** test hooks and variants with real spend once a script exists (the winners test many ads into one page).
9. **Learn from Dan's edits:** when Dan finishes his draft, diff it against the AI sections he lifted and record what he kept, cut and changed in the skill.

Rules: `AGENTS.md`, "VSL scripts: from Dan's outline, in the winners' voice". Skill: `.claude/skills/vsl-outline/SKILL.md`. Memory: `vsl-scripts-from-dans-outline`.
