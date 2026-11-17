# Great Again T sales page: install the sales letter on Design D

Written 2026-11-17 by Claude (Fable 5.2). Website design, mockups only: no edit slot, no render queue, no live shop changes.

**Fire after Dan has read and edited the letter Doc.** Best place: the running task "Great Again T sales page design contest" (it owns the generator and has Dan's Round 4 notes). A fresh task: Codex GPT-6.2 Astra at High (AGENTS.md, "Design work: Astra first"), on the M6, where the work folder is.

## Goal

The Design D page shows Dan's sales letter exactly as written in the Doc, with the layout the Doc's gold notes describe, at phone, tablet and desktop width, on the same review link.

## The source

Google Doc **Great Again T Sales Letter - Draft v2** (Draft v1 is superseded; do not build from it), id `1klwTUdTl5q_17MTA5c1Dtv-Agm_-B3rBpxGQPOj1SCI`.

- Black text is page copy, word for word. Gold bracketed lines are layout and image directions. `[P]` marks placeholder words Dan has not written; they render without the tag.
- Part A: the top of the page (already approved, unchanged). Part B: the letter, sections L1 to L22, each with its own direction note. Part C: directions for the whole page (order, section table, type, study cards, buttons, pictures, desktop, build method). Part D: every change from the VSL script. Part E: open items. Part F: the Google Ads wording changes.
- Dan edits the Doc directly. Always re-export it before a build; never work from a saved copy.

## What changed since Round 4 (why the page needs a rebuild)

Round 4 put the 180 lines of the VSL script on the page in order, with spoken transition lines as headings. The Doc is a letter made from the same lines:

- A letter headline and subheadline (L1), so "Prefer to read?" lands on a start.
- 23 subheads lifted from Dan's own sentences, Title Case, with his "…" lines as bold lead-ins.
- Numbered blocks: Food Swap #1 and #2, T Boosting Nutrient #1 and #2, T Boosting Root #1 to #3.
- Five buttons in the letter, where Round 4 had nine. Four "click the button" or repeated lines cut, one moved.
- The offer card in the price section sits after Dan explains the free month and the $67, not before.
- Real pictures for the potato swap; root photos; a real store listing with its price; a red X list for "every supplement I found had problems"; two always-open question cards with real questions as headings.
- The Round 4 pieces Dan approved are untouched: study list, letter look, dark green reveal, seal, offer card, buttons, checkout.

## Google Ads wording (Dan, 2026-11-17): applies to every page of the funnel

Dan: keep the word "testosterone" off the page (write "T", or "test" where he does), keep "drugs" and "needles" off the page, and any other word likely to trip Google Ads. The Doc already follows this; the design task must carry it through everything the Doc does not hold:

- **Study list:** the same 31 studies in the same order, each WITHOUT its paper title (the titles hold the banned words): authors, journal, year, volume, pages, DOI, PMID. Rebuild `citations-final.txt` entries that way; do not edit a title to hide a word.
- **Study cards:** 12, not 14. Cards 23 and 24 and their paragraph are off the page. Card wording is in the Doc's gold notes, already using "T".
- **Quiz:** question 2 says "increase your testosterone". Change to "increase your T".
- **Checkout, offer bar, alt text, captions, text inside screenshots:** none of the words in the Doc's section C10. Crop the store listing to name, picture and price.
- The footer's FDA sentence stays word for word. The film is not changed.
- Add to the page check: the page text matches none of `testosterone|\bdrugs?\b(?! Administration)|needle|prescription|inject|\bTRT\b|estrogen|aromatase|diabetes|cardiovascular|osteoporosis|\bdie\b|passing away|depress|steroid`.

## Steps

1. Read the Doc with its formatting: `rclone backend copyid gdrive: 1klwTUdTl5q_17MTA5c1Dtv-Agm_-B3rBpxGQPOj1SCI ./x/ --drive-export-formats zip`, unzip, `python3 .claude/skills/design-sales-page/scripts/parse_doc.py x/<file>.html blocks.json`. Page copy is every block that is not gold and not a section label (`PART`, `A1 ·`, `L1 ·` ...).
2. In `Media/research/gat-sales-page-contest-20261117/refine/gen.py`, rebuild `letter()` from the Doc blocks by position, keeping the approved components and `page.css`. Add the new pieces listed above. Keep `EDITS` empty: wording now lives in the Doc.
3. Replace `gen.py check` with the Doc check: every black paragraph of Part B on the page once, in order, word for word; no gold text or `[P]` on the page; no em or en dashes; five buttons in the letter; the Google Ads word check above passes on the letter page, the quiz and the checkout.
4. Collect the pictures in Part C7. A missing picture ships as a labelled grey block.
5. Capture phone (390), tablet (768) and desktop (1440) with `tools/shotw.mjs`, rebuild the review with `build_review.py`, publish to the same file path so the link stays https://claude.ai/artifact/V5jWex1Nzp7DsPU4TjZ2gm.
6. Report to Dan: what changed, phone first, then the open items from Part E that he has not answered.

## Limits

- Mockups only. No deploy, no shop, ad or tracking changes. Expected spend $0.
- Do not rewrite, add or cut copy. A line that looks wrong goes to Dan as a question, and the page shows the Doc's words meanwhile.
- No invented reviews. The review section is built and hidden.
- Rules: AGENTS.md "Website design: phone first", "Design work: Astra first", `Docs/DESIGN_QUALITY_LESSONS.md` ("Great Again T sales page"), memory `gat-sales-page-direction`.

## Local files

`Media/research/gat-sales-page-contest-20261117/letter/` (gitignored, M6): `build_letter.py` builds the draft from the VSL script by line number and proves all 180 lines are accounted for; `letter-v1-copy.txt` is the page copy as first delivered, for diffing Dan's edits later (`/dan-copywriting` step 5).

## Done looks like

The review link shows the letter from the Doc on all three widths, the Doc check passes, and Dan has a short list of what changed plus any Part E items still open.
