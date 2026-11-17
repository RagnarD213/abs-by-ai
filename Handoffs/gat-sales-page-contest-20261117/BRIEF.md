# Great Again T sales page: design brief for every entrant

Identical for all entrants. Read it fully, then deliver two concepts. Do not ask questions; where the brief is silent, decide and note it.

## The job

Design the phone sales page for Great Again T, a testosterone support supplement sold by SixPackAbs.com. Dan Rose (the founder, 41, fit, on camera) sells it with a vertical 9:16 sales video about 30 minutes long. More than 80% of visitors are on phones. Design at **390 x 844** and nothing else. Desktop is out of scope for this round (it will be the phone column, centered).

Deliver **two concepts that differ in structure**, not in colours. Examples of a structural difference: how the first screen is composed around the player, how the offer panel and its terms are built, how the proof sections below are ordered and shaped.

## Model: Healthy Back Institute first

Dan ran ads for Healthy Back Institute and trusts this funnel from first-hand results. Model the page on it more than on anything else:

- **The player.** A vertical video that fills the phone. On their page the video is 350 x 622 px on a 390 x 844 screen and starts 47 px from the top. Dan: "I definitely want the player to appear like that."
- **How the continuity offer is presented.** A free bottle, the visitor pays shipping, refills bill monthly until cancelled. Their page shows a free bottle panel under the video; their order form shows a titled "How this FREE Trial Offer Works" box with the terms in plain sentences directly above the button.

V Shred's Test Boost Max page is the second model: a few yes/no questions first, then a page with almost nothing on it but a headline and the video until the video reaches the offer.

Reference captures (phone size, taken Nov 16 and 17, 2026) are in `reference/`:

| File | What it shows |
|---|---|
| `hbi-fold.jpg`, `hbi-offer.jpg`, `hbi-featured.jpg` | Healthy Back sales page: player, arrows down to the free bottle panel, credibility card |
| `hbi-order-top.jpg`, `hbi-order-terms.jpg` | Healthy Back order form: offer choice, "How this FREE Trial Offer Works" box, agreement box, button |
| `vs-q1.jpg` to `vs-q4.jpg`, `vs-fold.jpg` | V Shred: the four questions and the bare video page |
| `vs-buy-top.jpg`, `vs-seal-faq.jpg` | V Shred: five checkmarks, bottle with seal, numbered questions |
| `mm-ingredients.jpg`, `mm-guarantee.jpg` | Mars Men: ingredient cards with a dose chip, guarantee block |
| `la-story.jpg`, `la-reviews.jpg`, `tg-reviews.jpg` | Live Anabolic and TestoGreens: story with dated photos, review cards |
| `tp-fold.jpg`, `vfl-countdown.jpg` | Pinned top bar with a button |
| `gr-fold.jpg`, `ry-top.jpg` | Small notes under a button |

## Screens to deliver, per concept

1. `1-quiz.html`: the four yes/no questions, one per screen, with a progress bar. Show all four states (a simple click-through is fine). Any answer leads to the video page.
2. `2-before-offer.html`: the video page as it loads, before the video reaches the offer.
3. `3-after-offer.html`: the same page after the offer is revealed, complete to the footer.

## What the page contains (Dan's picks, numbered as he chose them)

Before the offer:

- **1. Four yes/no questions with a progress bar.** Big tap targets.
- **2. A two-line headline, nothing above it** except a slim logo line if you need one. **One colour only. No red or highlighted word.** Dan: a coloured word "makes it seem non-scientific."
- **3. The vertical player at nearly full phone height**, as on Healthy Back. Hard floor: the headline and the whole player fit on the first 844 px screen, and the player is at least 540 px tall.
- **4. A "Your video is playing, tap for sound" box** on the video.
- **5. One line under the video:** sound on, and a reason to watch to the end.
- **6. A founder card under the video:** Dan's photo, name, two sentences.
- **7. The studies, as a long plain list.** Small text, one citation after another, always visible, **not expandable, nothing clickable.** Dan: "a long list of citations ... so it looks very scientific." It should read like the reference list at the end of a journal article. It sits below the video on both the before and after pages.
- **8. A link to a read-it version** for people who will not watch.

At the offer (appears when the video reaches Dan's first invitation to buy; show it in `3-after-offer.html`):

- **10. Arrows pointing from the video down to the offer.**
- **17. The free bottle panel:** the bottle, a FREE BOTTLE burst, a short note in Dan's voice, one button.
- **The trial terms, Healthy Back style.** A titled box in plain sentences directly above or below the button: what ships today and what it costs, when the first refill bills, the monthly amount, how to cancel. This is the "continuity presentation" Dan wants modelled. Whether to include Healthy Back's agreement tick box is your call.
- **11. A product line with five checkmark benefits.**
- **12. The bottle shot with the guarantee seal overlapping it.**
- **19. One orange button with benefit wording.** The same button style everywhere. No second button colour.
- **20. Two or three small notes under the button:** guarantee, shipping, terms.
- **21. The guarantee as its own block:** seal, headline, two sentences.
- **22. A slim bar pinned to the top with the button,** shown only after the offer is revealed.

Below the offer:

- **24. Ingredient cards with the dose on a chip.**
- **25. Dan's story with dated photos.**
- **27. Buyer review cards with a bold title line.** There are no real reviews yet. Build the card design with neutral placeholder wording ("Review title", "Real buyer review goes here"). Never write an invented review.
- **23. Numbered questions answered in Dan's voice.**
- A final button and a footer.

Not chosen, so leave them out: a pack picker or multi-bottle cards, a one-time versus subscribe choice, a countdown clock, a day 7/30/90 timeline, a bonus stack image, number chips, a "Featured in" logo row, a star rating row.

## The offer (from Dan's final VSL script)

- First month's supply free. The visitor covers shipping only. Show shipping as **$9.99** (proposed, not yet confirmed by Dan).
- If he keeps it: **$67 a month** for monthly shipments, until he cancels.
- If he does not like it: he keeps the free bottle and is not billed again.
- Regular price of one bottle: **$97**.
- Guarantee: return any unopened bottles for a 100% refund, good for a full year after he receives his shipment.

One offer on the page. No other packs or prices.

## Words

Use `CONTENT.md` exactly. Every entrant gets the same words so the designs can be compared. Do not rewrite, add claims, add sections or invent proof. You may break lines and choose which supplied line is a heading. If a section needs words that are not in `CONTENT.md`, use the shortest neutral placeholder and list it in your notes.

## Look

- **Scientific and credible.** That is the reason for the plain headline and the citation list. No hype styling: no starbursts except the one FREE BOTTLE burst, no flashing, no fake urgency.
- **Light page.** Dan dislikes predominantly black sites. A dark band behind the player is allowed if your concept wants the Healthy Back theatre look; the rest of the page stays light.
- **Brand.** SixPackAbs.com. The logo is gold `#C9A766` and appears on dark only (`assets/logo/`). Brand font is Archivo; you may pair another face. The bottle is `assets/bottle-front.png` and `assets/bottle-transparent.png`: use these files as they are, never redraw the label.
- **Photos.** Only the files in `assets/`. Empty slots get a neutral grey block labelled with what goes there.
- Buttons at least 54 px tall. Body text at least 16 px, except the citation list and legal lines.
- No em dashes or en dashes in any page text.

## Technical

- Each screen is one self-contained HTML file: inline CSS and JS, Google Fonts allowed, images by relative path into `../assets/`. No frameworks, no build step, no external scripts.
- The video is a still poster (`assets/poster.jpg`) with the sound box drawn over it. No real video.
- It must render correctly in Chrome at 390 px wide with no sideways scroll.
- **Blind test.** Put nothing in any file that says who or what made it: no model, tool or company names in comments, class names, meta tags, file names or notes.

## Before you hand in

Open your own pages at 390 x 844 and compare them with `hbi-fold.jpg` and `hbi-offer.jpg` side by side. For each concept, name one visible weakness in the first screen and one in the offer panel, fix both, then deliver. A finished checklist is not the bar; the page has to look like something a serious supplement company would run.

## Deliver

In the folder you were given:

```
concept-1/1-quiz.html  2-before-offer.html  3-after-offer.html  NOTES.md
concept-2/1-quiz.html  2-before-offer.html  3-after-offer.html  NOTES.md
```

`NOTES.md`, at most 120 words: the structural idea in two sentences, any placeholder words you added, anything you could not do.
