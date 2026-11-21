# Great Again T: design and code the nine compliance pages

Written 2026-11-17 by Claude (Fable 5.2). Website design and code, mockups only: no edit slot, no render queue, no live shop changes.

**For the running task "Great Again T sales page design contest"** (it owns the generator `refine/gen.py`, `page.css`, the review link and Dan's approved letter design). Dan, 2026-11-17: make a handoff "for the coding task to design and code these pages up" and "just put it in a similar design as the main sales letter." A fresh task instead: Codex GPT-6.2 Astra at High, on the M6, where the work folder is.

## Goal

Nine plain information pages exist next to the sales page, in the same look as the sales letter, at phone, tablet and desktop width, linked from the menu and footer of every funnel page, on the same review link. Their text is the Doc's black text, word for word.

## Why these pages exist (read this before designing)

Dan: "These pages should be written purely for compliance. Only the Google Ads policy team will look at them." They are there to show Google's reviewers a transparent business: who the company is, what the product contains, what the buyer pays and when, how to cancel, how refunds work, how data is used. So the design job is restraint. Same family as the letter, calmer than the letter: no selling.

Google's rules and what each one asks of the site: `Docs/GAT_COMPLIANCE_PAGES_20261117.md`.

## The source

Google Doc **Great Again T Compliance Pages - Draft v3**, id `1QErPnqlCvhgdwfXYut6JL-h6O_iLspkjw2FFznYQeLs` (Drafts v1 and v2 are superseded; do not build from them). Not yet edited by Dan at handoff. He edits the Doc directly and his edits win: re-export it before every build.

- Black text is page copy. Gold bracketed lines are layout notes and never appear on a page.
- Each page starts at a gold label `PAGE n · NAME` and ends at the next label or at `PART B`.
- The one gold bracket inside black text is the date line on the Privacy Policy and the Terms (`[date this page is published]`). In the mockup show "November 17, 2026".
- Part B: the Google rule each page answers. Part C: the defaults Claude used and what the live shop still has to match (Dan's decisions; nothing for you to change in the shop). Part D: footer link order.

| Page | Menu and footer name | File |
|---|---|---|
| 1 Frequently Asked Questions | Questions | `p-questions.html` |
| 2 How It Works | How It Works | `p-how-it-works.html` |
| 8 Ingredients and Label | Ingredients | `p-ingredients.html` |
| 6 Shipping and Returns | Shipping and Returns | `p-shipping-returns.html` |
| 3 Contact Us | Contact | `p-contact.html` |
| 7 About Us | About Us | `p-about.html` |
| 4 Privacy Policy | Privacy Policy | `p-privacy.html` |
| 5 Terms and Conditions | Terms and Conditions | `p-terms.html` |
| 9 Disclaimer | Disclaimer | `p-disclaimer.html` |

The table is in footer link order (Part D).

## Design: the sales letter's look, minus the selling

Keep from the letter (`.letter` in `page.css`): the paper background, the reading column and its width at each size, the body and heading typefaces, text sizes, link colour, the dark logo strip with the gold logo and menu, and the footer.

Leave out: the video player, offer bar, offer card, buy buttons, guarantee seal, study cards, physique photos, red and green highlight treatments, and anything that moves. No buy button anywhere on these nine pages.

Per element:

- **Page title:** the letter's headline face, one size down from the letter headline. A thin gold rule under it.
- **Section headings and question headings:** the letter's subhead style, smaller. Questions on the FAQ are all open: no accordions, no "read more". Google's crawler and the reviewer must see every answer without clicking.
- **Lists:** plain bullets. The numbered "Step 1." lines stay as paragraphs with the step label bold.
- **Summary of charges (How It Works, section 6) and the monthly delivery list (Terms, section 5):** a simple bordered box on the paper colour, so the billing terms are the easiest thing on the page to find.
- **Ingredients and Label:** the real Supplement Facts panel as an image under the title, readable on a phone (full column width), then the text version. Look for the label image on the live product page (`https://shop.sixpackabs.com/products/great-again-t`) and in the SixPackAbs label files (`Handoffs/sixpackabs-production-20261103/`, `Contest/approved/`). If you cannot find it, ship a labelled grey block and say so.
- **Contact Us:** contact details as real text (not an image), then the form from the gold note: Name, Email, Order number (optional), Topic (five options), Message, button "Send Message", line under it. The form does not need to send in the mockup.
- **About Us:** one clothed founder photo already in `refine/assets/` (`founder.jpg` or `founder-kitchen.jpg`). No shirtless photos.
- **Privacy Policy, Terms, Disclaimer:** text only. Web addresses in the Privacy Policy are real links.
- Words such as "our Contact Us page", "our Privacy Policy", "our Ingredients and Label page", "our Shipping and Returns page" link to that page.

Phone first (390), then tablet (768) and desktop (1440): AGENTS.md "Website design: phone first".

## Menu and footer on every page

- The menu panel and the footer links on all pages (quiz, before offer, after offer, checkout and the nine new pages) list the nine names in the table's order, and each link opens its page. The logo links back to the sales page.
- The footer's support email must match the Doc. The Doc says `support@sixpackabs.com`; that mailbox was created on 2026-11-17 on Dan's OK and forwards to him. `gen.py` currently prints `dan@sixpackabs.com`: change it to match, unless Dan told you to use that one, in which case tell him the two differ.
- The checkout shows links to Terms and Conditions, Privacy Policy and Shipping and Returns next to the pay button.

## Steps

1. Export the Doc with formatting: `rclone backend copyid gdrive: 1QErPnqlCvhgdwfXYut6JL-h6O_iLspkjw2FFznYQeLs ./x/ --drive-export-formats zip`, unzip, `python3 .claude/skills/design-sales-page/scripts/parse_doc.py x/<file>.html blocks.json` (the same route `letterdoc.py` uses for the letter). Split the blocks into pages at the `PAGE n ·` labels; drop gold blocks.
2. Add an `info_page()` builder to `refine/gen.py` that renders one page from its blocks with the shared header and footer, and write the nine files in `build()`. Add the styles to `page.css` under one `.info` class so the letter styles stay untouched.
3. Update the menu and footer links in the existing pages.
4. Extend `gen.py check`: every black paragraph of each Doc page is on its page once, in order, word for word; no gold text and no square brackets on any page; no em or en dashes; no buy button on the nine pages; every menu and footer link resolves; the sales page word check (below) passes on all nine.
5. Capture phone, tablet and desktop for each page with `tools/shotw.mjs`, add a "Compliance pages" section to the review with `build_review.py` (phone first), and publish to the same file path so the link stays https://claude.ai/artifact/V5jWex1Nzp7DsPU4TjZ2gm.
6. Report to Dan: the nine pages, phone first, anything you could not find (label image), and the Part C items that are still his to decide.
7. Update your own board entry (GAT-sales-page) and mark this handoff executed in `Handoffs/README.md`.

Word check (same as the sales page; the Doc already passes): the page text matches none of `testosterone|\bdrugs?\b(?! Administration)|needle|prescription|inject|\bTRT\b|estrogen|aromatase|diabetes|cardiovascular|osteoporosis|\bdie\b|passing away|depress|steroid`. "Food and Drug Administration" stays.

## For the live build later (do not do now)

Real text pages on the same website as the sales page, no password, not blocked from Google's crawler, no PDFs. Quiz answers never go into Google tags or page addresses (the Privacy Policy promises this). The 7-day reminder email before the first monthly charge has to exist before launch.

## Limits

- Mockups only. No deploy, no shop, ad, tracking or email changes. Expected spend $0.
- Do not rewrite, add or cut copy. A line that looks wrong goes to Dan as a question, and the page shows the Doc's words meanwhile.
- No sales elements, no invented reviews, no new claims, no images beyond the label and the one founder photo.
- Rules: AGENTS.md "Website design: phone first", `Docs/DESIGN_QUALITY_LESSONS.md` ("Great Again T sales page"), memory `gat-page-google-ads-words`, `gat-sales-page-direction`.

## Local files

`Media/research/gat-sales-page-contest-20261117/compliance/` (gitignored, M6): `build_pages.py` built the Doc and runs the word check; `pages-v3-copy.txt` is the page copy as delivered, for diffing Dan's edits later.

## Done looks like

The review link shows all nine pages at three widths in the letter's look, every menu and footer link works, the Doc check and the word check pass, and Dan has a short report with the open Part C items.
