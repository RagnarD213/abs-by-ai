# Great Again T sales page: blind six-design contest

Written 2026-11-17 by Claude (Fable 5.2) after the research round. Website design, not a video: no edit slot, no render queue.

**Recommended: Claude Opus 5.5, high effort, on the M6** (the reference files are local to this Mac). The session coordinates; it does not design.

## Goal

Dan picks one winning phone design for the Great Again T sales page out of six, without knowing who made which. Then we refine the winner.

Dan asked for exactly this line-up: **2 designs from Fable, high effort; 2 from Opus, high effort; 2 from Astra, high effort.** Blind. Tell him the model and effort level only when he picks.

## What is already done

- Research page Dan reviewed: https://claude.ai/artifact/Mqrk2zasokk3pxzKuz5fYg
- Dan's element picks and direction (2026-11-17), all folded into [BRIEF.md](BRIEF.md). His words:
  - "I like the way the Healthy Back Institute player appears. I definitely want the player to appear like that. I like the way their continuity is presented. I want to model it on the Healthy Back funnel more than anything."
  - Two-line headline, yes. No red word: "I feel like that makes it seem non-scientific." (He dictated "read"; he means red.)
  - Studies: "I want a long list of studies below the video in small text that is just there on the page, not expandable ... nothing clickable, so it looks very scientific."
- Files in `Media/research/gat-sales-page-research-20261116/` (gitignored, M6 only):
  - `img/`: 31 reference crops named in the brief. `shots/*-stitched.jpg`: full-length captures.
  - `reference/Great Again T VSL Script - DAN.txt`: Dan's final script, exported 2026-11-17 from Doc `1CmK7ZG45x-p7mXATjvlWzuUpvlr7AQMHUbiQcdMYCFI`.
  - `reference/shot.mjs`: headless Chrome capture at 390 x 844, 2x (`node shot.mjs outPrefix url maxHeight`). Works on `file://` pages. `build_page.py` and `template.html` built the research artifact: reuse them for the gallery.

## Decisions I made that Dan has not confirmed

1. **The offer stays hidden until the video reaches it.** Dan did not tick "buy section hidden until your first invitation to buy", but he ticked the arrows and the pinned bar "after the reveal", and Healthy Back hides its panel. Entrants deliver both a before and an after page, so either answer works.
2. **Shipping shows as $9.99.** The script says "just cover the shipping costs" with no figure; $9.99 is the funnel plan's proposal.
3. **Review cards use neutral placeholder wording.** No real reviews exist yet; nobody writes invented ones.
4. **Phone only this round.** Dan asked for "almost mobile-only". Desktop comes in the refinement round as the centered phone column.
5. **Mismatch to raise with Dan at delivery, one line:** the script says "I've put links to every one of those studies right below this video." He now wants the list not clickable.

## Dan's decisions during the contest (2026-11-17)

- Quiz: stacked buttons as V Shred, "Not Sure" on questions 2 to 4, V Shred-style progress bar. Wording pending Dan's pick between his set and Claude's tightened set.
- Headline: "Eat More Of These Foods And Less Of Those Foods To Naturally Boost Your T". Text under video: "This is a science-based presentation backed by real research. To see the research supporting the food swaps in this video, see the studies below." Studies directly under it as a large journal-style block (31 real citations with DOI and PMID) pushing the rest far below the fold.
- Sans-serif throughout (serif allowed only for his note and the study list); dark only behind headline and player; logo strip with hamburger menu (Questions, Contact, Shipping and Returns, Privacy Policy, Terms and Conditions) on every page; full company footer.
- **Desktop:** start with V Shred's desktop layout (white centered card over a full-width background photo, two-line headline, video in a 16:9 player box; measured 2026-11-17 at 1440 x 900: card about 1,050 px, player 1000 x 562, vertical video pillarboxed inside it). Later, make a separate 16:9 edit of the VSL for desktop, as Healthy Back does (its desktop page plays a horizontal edit at 890 x 501), which then fills the same box. Build the desktop version in the refinement round on the winner.

## Result and refinement (2026-11-17)

- Dan picked **D** (Codex GPT-6 Astra high, concept 1): dark green quiz and hero read trustworthy. Full mapping in `blind-key.json`; recorded in `Docs/DESIGN_CONTEST_WORKFLOW.md`.
- Round 3 (Claude Opus 5.5): generator `Media/research/gat-sales-page-contest-20261117/refine/gen.py` + `page.css` (responsive 390 / 768 / 1440), `python3 gen.py check` proves all 180 VSL script lines are on the page in order (10 tracked spoken-to-written edits in `EDITS`). Pages: 2-before-offer, 3-after-offer (offer bar inside the dark header), 3b (bottom dock alternative), 4-checkout (modelled on the HBI order page). Review: https://claude.ai/artifact/V5jWex1Nzp7DsPU4TjZ2gm (`build_review.py`).
- Citation fix: entries 15 to 30 carried a neighbour's DOI and PMID in rounds 1 and 2; corrected against PubMed in `package/CONTENT.md` and `citations-final.txt`.

## Steps

### 1. Build the shared package (once, identical for all three)

Work folder: `Media/research/gat-sales-page-contest-20261117/`.

```
package/BRIEF.md            copy of Handoffs/gat-sales-page-contest-20261117/BRIEF.md
package/CONTENT.md          you write this, see below
package/reference/          the crops the brief names, copied from the research img/ folder
package/assets/             logo/, bottle-front.png, bottle-transparent.png, poster.jpg, founder and story photos
```

**CONTENT.md.** One copy deck every entrant uses word for word. Take the words from Dan's script, verbatim, section by section: headline (two lines, from his opening promise about food swaps), the sound line, founder card (two sentences from his self-introduction), five benefits, the free bottle note (script lines around "If you try Great Again T today, I'll send you your first month's supply for FREE" through "$67 a month"), the trial terms box (plain facts from the brief's offer section), guarantee, his story beats with the photo each needs, ingredient names and doses, the questions and answers from his post-offer section, button wording. Follow AGENTS.md "VSL scripts: from Dan's outline": do not write sales copy. Where the script has no line, write the shortest neutral placeholder and collect all of them under a `PLACEHOLDER WORDS` heading at the end for Dan.

- **Four quiz questions:** look for Dan's own four in `Handoffs/great-again-t-20261105/vsl-outlines-AB-20261108.md` and the ad scripts work (board: GAT-ad-scripts). If he has not written them, use four plain yes/no questions that preview the food swaps and list them as placeholders.
- **Ingredients and doses:** from the live product page https://shop.sixpackabs.com/products/great-again-t and the locked label. Known: tongkat ali 400 mg, zinc 50 mg, plus maca, eleuthero, nettle, boron, tribulus. Verify before writing.
- **Studies:** real citations only, as plain text (authors, title, journal, year). Sources: the studies the script cites, `Handoffs/great-again-t-20261105/research-evidence.md`, and the three linked in `Docs/GREAT_AGAIN_T_FUNNEL_PLAN_20261110.md` section 8. Aim for a long list; never pad it with invented entries. If fewer than about 15 are verified, say so at delivery.

**Assets.**
- Logo: `sixpackabs/brand/logo/` (memory `sixpackabs-logo-kit`; gold on dark only).
- Bottle: `Contest/claude/labels-final-round1/mockups-web/02-great-again-t-front.png` and `02-great-again-t-transparent.png`. Web-safe mockups only, never `mockups/` or print files.
- Poster: one 9:16 still of Dan from the VSL (WV-03, medium wood kitchen, on the M2 under `~/_edit_work/wv-03/`; `ssh m2`). If unreachable, a neutral 9:16 grey poster labelled "VSL poster".
- Founder and story photos: use `/findassets`. Rules: memories `standard-before-picture`, `speedo-crop-rule`, `before-after-same-person`, `no-before-after-same-screen`. A slot with no approved photo ships as a labelled grey block.

Put no entrant, model or tool names anywhere in `package/`.

### 2. Run the three entrants (in parallel, same package, same prompt)

Each entrant gets its own copy of `package/` in `entries/<id>/` where `<id>` is a random 6-character code, and this prompt and nothing else:

> Read BRIEF.md in this folder completely, then CONTENT.md, then look at every image in reference/. Design and build the two concepts the brief asks for, in this folder. Check your own pages at 390 x 844 before finishing. Do not ask questions.

- **Fable 5.2, high:** Agent tool, `model: "fable"`, `effort: "high"`.
- **Opus 5.5, high:** Agent tool, `model: "opus"`, `effort: "high"`.
- **Codex Astra, high:** `/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex exec -C "<entry folder>" -m <Astra id> -c model_reasoning_effort=high --dangerously-bypass-approvals-and-sandbox "<the prompt>"`, in the background. Resolve the Astra id from the Codex model catalog (the CLI default on this Mac is `gpt-6.1-sol`; Dan named Astra for this contest, which overrides the newest-GPT default). If Astra is not available, stop and tell Dan; never substitute Sol silently.

Give the subagents no hint about the other entrants or which model they are competing against. Record in `blind-key.json` (work folder root, never published): entry id, model, effort, start and end time, any fix round.

### 3. Check each entry, one fix round at most

Render all 18 files with `shot.mjs` (same script for every entry). Check against the brief:

- headline and whole player on the first screen, player at least 540 px tall
- headline one colour; no highlighted word
- citation list always visible, small, not expandable, nothing clickable
- every chosen element present; none of the left-out ones
- one offer, the terms box by the button, one orange button style
- light page; no sideways scroll; no dashes in page text
- `grep -r -i -E "claude|opus|fable|sonnet|anthropic|codex|openai|gpt|astra|gemini"` over the entry returns nothing

Misses go back to the same entrant, same model and effort, once, as a plain list. Do not fix or polish an entry yourself; equal treatment matters more than a tidy gallery. A concept still broken after the fix round is shown as it is, with the fault stated.

### 4. Build the blind gallery

- Shuffle the six concepts into letters A to F (store the seed and mapping in `blind-key.json`).
- Publish one private Artifact, "Great Again T Page Contest", phone first:
  1. Six first screens of the video page side by side at one size.
  2. For each letter: quiz, before offer, after offer, full length, tap to enlarge. Same order and size for every letter.
  3. A Select control per letter (Dan clicks what he wants; untouched means out), a notes box per letter, and a "Copy my choices" button, as on the research page.
- Nothing in the page, file names, alt text or image metadata may reveal a source. No entrant NOTES on the page.
- If links to an artifact's own published HTML files work, also link each letter's three live pages so Dan can scroll the real thing on his phone. If not, screenshots only.
- Do not rank the designs or recommend one before he picks. Afterwards you may.

### 5. Stop for Dan's pick, then

1. Reveal the full table: letter, model, effort level.
2. Record the result with his exact comments in `Docs/DESIGN_CONTEST_WORKFLOW.md` (evidence section) and `Docs/DESIGN_QUALITY_LESSONS.md`; update memory `model-routing-plan` only if he changes routing.
3. Refine the winner in the same session if context allows (under about 40%), otherwise hand off. Use the `/design-sales-page` process for refinement: a generator, Dan's copy verbatim and proven by script, a Design canvas, phone first, then the desktop column. That skill's locked Abs By AI layout does not apply to this page; its process does.

## Limits

- Mockups only. No changes to the live shop, sixpackabs.com, ads or tracking. No deploy.
- Expected spend $0 (subscription allowance only). No paid image generation; seals, bursts and arrows are CSS or inline SVG.
- Rules that apply: AGENTS.md "Website design: phone first", "Marketing advice: proven direct response only", "No compliance commentary", `Docs/DESIGN_CONTEST_WORKFLOW.md`.

## Done looks like

Dan has one private link showing six unlabelled phone designs at matching sizes, each complete in three states, and can choose in one sitting. `blind-key.json` exists locally. The board entry "GAT-sales-page" says the gallery is waiting on his pick.
