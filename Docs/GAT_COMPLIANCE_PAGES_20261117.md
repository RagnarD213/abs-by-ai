# Great Again T: Google Ads compliance pages (2026-11-17, Claude)

Dan asked for four pages written only for the Google Ads policy team: Frequently Asked Questions, How It Works, Contact Us, Privacy Policy. Informational, not sales copy.

**Source Doc (Dan edits it there):** Great Again T Compliance Pages - Draft v3, id `1QErPnqlCvhgdwfXYut6JL-h6O_iLspkjw2FFznYQeLs` (Drafts v1 and v2 are superseded). Since v3 it holds nine pages: the four above plus Terms and Conditions, Shipping and Returns, About Us, Ingredients and Label, and Disclaimer (Dan asked for them the same day). Black text is page copy, gold bracketed text is notes, the only gold bracket inside a sentence is the Privacy Policy date (the build fills it in). Part B maps each page to the Google rule it answers, Part C is the defaults used and what the shop has to match, Part D is the extra pages recommended. Build handoff: `Handoffs/gat-sales-page-contest-20261117/COMPLIANCE-PAGES.md`.

Local builder (gitignored, M6): `Media/research/gat-sales-page-contest-20261117/compliance/build_pages.py` (runs the sales page word check; `pages-v3-copy.txt` is the copy as delivered).

## What Google's policies ask of the website (read 2026-11-17)

| Policy | What it requires | Link |
|---|---|---|
| Dishonest pricing practices | Payment model, full cost, shipping, subscription price and interval, free trial length, automatic charge at the end, all easy to find on the destination | https://support.google.com/adspolicy/answer/15938375 |
| Misrepresentation | Clear business identity, contact information and physical address where relevant, how, what and when users are charged, no improbable result as the likely outcome | https://support.google.com/adspolicy/answer/6020955 |
| Unreliable claims | A guarantee needs a clear, easy to find refund policy; testimonials with specific results need a visible "not guaranteed, results vary" line | https://support.google.com/adspolicy/answer/15936857 |
| Unapproved substances | No supplement implying it works like a medicine or treats, cures or prevents a disease; no listed ingredient. None of the Great Again T ingredients is on the list (https://support.google.com/adspolicy/answer/2423645) | https://support.google.com/adspolicy/answer/15595718 |
| Personalized advertising, Health | A page judged to be about a sensitive health topic (sexual health and intimate body functions are named) loses website visitor, customer list and lookalike audiences. Supplements are not named either way | https://support.google.com/adspolicy/answer/16701855 |
| Remarketing privacy policy | Say how we advertise online, that vendors including Google use cookies to serve ads based on past visits, how to opt out; disclose sharing customer data with third parties acting for us | https://support.google.com/google-ads/answer/2549063 |
| Data collection and use | Personal and payment data only over a secure connection; no personal data in tags or URLs | https://support.google.com/adspolicy/answer/6020956 |
| Destination requirements | Working, crawlable, navigable pages with their own content | https://support.google.com/adspolicy/answer/6368661 |

## Build rules for whoever installs the pages

- Real text pages on the same website as the sales page, linked from the footer of every funnel page (quiz, sales page, checkout), no password, not blocked from Google's crawler, no PDFs, no accordions.
- No buy buttons or sales images on them. The Supplement Facts label image goes on How It Works and under the ingredients answer.
- The Privacy Policy promises quiz answers are never sent to ad platforms: keep quiz answers out of Google tags and page addresses.
- The sales page wording rule applies (memory `gat-page-google-ads-words`).

## Mismatches found between the sales page offer and the live shop (Dan decides)

1. Monthly refill: the page says $67; the shop gives free shipping only from $70, so it would charge $76.99 today.
2. Regular price $97 on the sales page; the shop sells one bottle for $47.
3. Guarantee: the script says unopened bottles within one year of receiving them; the shop's refund page says any reason, 365 days from the order.
4. Contact: the pages publish email, mailing address, hours and a form, no phone number. `support@sixpackabs.com` was created 2026-11-17 on Dan's OK as a WordPress.com forward to his inbox (active; not yet tested with a real email). The 7-day reminder email before the first refill charge is a launch requirement for the checkout build.

## Label facts

The ingredient list, directions and warnings on the Ingredients page come from the supplier listing for this formula (https://supliful.com/catalog/mens-vitality-tablets): calcium 367 mg, zinc 50 mg, tongkat ali 400 mg, maca 250 mg, L-arginine HCl 250 mg, ginseng and eleuthero 125 mg, and a 745 mg blend of 13 ingredients. Compare with the printed bottle before publishing.
