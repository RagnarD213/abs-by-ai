# Handoff: Texas sales and use tax permit for SixPackAbs (Codex and Grokbot)

Written 2026-11-05 by Claude. **Fire now.** For **both Codex and Grokbot** (Dan's standing rule: steps Claude can't do go to both). Not video. Codex: newest Sol (`gpt-6.1-sol`), medium effort.

## AUTHORIZED: apply without asking Dan for permission

Dan asked for this permit on 2026-11-05: "let's just get that permit, so that way, in case we need it in the future." Do every step yourself. Do not stop to ask Dan whether to proceed. Stop only where Dan himself must type something (below), and say exactly what.

## Why Claude handed this off

The application runs in the Texas Comptroller's eSystems. It needs a login account and owners' Social Security numbers, and Claude can't create accounts or enter government ID numbers.

## Facts for the application (all public or already approved)

- Applicant: **Rose Digital Holdings LLC** (Texas LLC). Texas Comptroller taxpayer number **32105235058** (public Franchise Tax search, zip 78628). Its Texas Secretary of State file number may be needed: look it up on the same public search (https://comptroller.texas.gov/taxes/franchise/account-status/search, open the entity) or SOSDirect.
- Business: online store **shop.sixpackabs.com** (Shopify), launched 2026-11-05. Trade name/DBA: **SixPackAbs.com**.
- Products: six dietary supplements, each labeled with an FDA Supplement Facts panel. Texas exempts these (Comptroller Publication 94-155). Taxable sales expected: none right now. The permit is for future taxable items.
- How goods move: sold online, shipped to customers by a third-party fulfiller (Supliful), no Texas warehouse. Business location: Georgetown, TX (Williamson County).
- NAICS: **456191** (All Other Health and Personal Care Retailers, includes food supplement stores). If the form rejects it, use the closest "health supplement" or "nonstore retail" code it offers.
- First Texas sale date: **2026-11-05**.
- Mailing and business address, phone, email: Dan's saved details. Codex reads them from Dan's local Claude memory file `dan-contact-info` (local only) or the Shopify store address (Settings › General). Never write them into the repo, this handoff or chat.

## Steps

1. Open https://comptroller.texas.gov/taxes/permit/ and choose **Apply for Permit via eSystems** (https://security.app.cpa.state.tx.us/).
2. Sign in. Rose Digital Holdings LLC already has a Comptroller taxpayer number (franchise tax), so Dan may already have an eSystems login. If he does, Dan signs in himself. If not, create the eSystems account for Dan with his email; any password and verification code step is Dan's.
3. Start a **Sales and Use Tax Permit** application for the existing taxpayer (Rose Digital Holdings LLC, 32105235058). Fill every field from the facts above.
4. **Dan types these himself:** each member/manager's Social Security number (and the LLC's federal EIN if asked; Dan keeps the EIN letter in Google Drive), and the final signature/declaration. Leave the form open on those fields and tell Dan which fields are waiting.
5. Submit once Dan has filled his fields and signed. If a security bond or fee is requested, report the amount to Dan before paying (normally none for a sales tax permit).
6. Record the confirmation number. The permit itself arrives in 2 to 3 weeks; the permit number may show in eSystems sooner.

## After the permit number exists

- Shopify: Settings › Taxes and duties › United States › Texas › collect sales tax, enter the permit number.
- Make sure Shopify treats the products as exempt dietary supplements: each product's category (Products › product › Category) should be a Dietary Supplements category so Shopify Tax charges 0% on them. Check one Texas test checkout shows $0 tax on a supplement.
- Add one line to `Docs/SIXPACKABS_SHOP_BUILD_RECEIPT_20261105.md`: application confirmation number, date, status (no SSN, EIN or address). Push with `scripts/git/safe-push.sh`. Remove this handoff from `Handoffs/README.md` OPEN.

## Report to Dan

Plain language: submitted or not, confirmation number, what Dan still has to do (if anything), when the permit should arrive.
