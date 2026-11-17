# Great Again T: Google Ads compliance pages (2026-11-17, Claude)

Dan asked for four pages written only for the Google Ads policy team: Frequently Asked Questions, How It Works, Contact Us, Privacy Policy. Informational, not sales copy.

**Source Doc (Dan edits it there):** Great Again T Compliance Pages - Draft v1, id `1lu2BkYz5bDkwe3hLij6lZb2qfP60J_AY8isJxim84W8`. Black text is page copy, gold bracketed text is notes, a gold bracket inside a sentence is a fact to confirm. Part B maps each page to the Google rule it answers, Part C is what Dan must confirm, Part D is the extra pages recommended. Not built into the design yet.

Local builder (gitignored, M6): `Media/research/gat-sales-page-contest-20261117/compliance/build_pages.py` (runs the sales page word check; `pages-v1-copy.txt` is the copy as delivered).

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
4. Contact: no business phone number is published; the 7-day reminder email before the first refill charge is not set up.

## Extra pages recommended

Terms and Conditions (with the monthly delivery terms), Shipping and Returns (rewritten for the free month offer), About Us, Ingredients and Label, Disclaimer.
