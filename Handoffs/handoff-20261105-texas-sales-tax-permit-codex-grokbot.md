# Handoff: Texas sales and use tax permit for SixPackAbs (Codex and Grokbot)

Written 2026-11-05 by Claude. **Fire now.** For **both Codex and Grokbot** (Dan's standing rule: steps Claude can't do go to both). Not video. Codex: newest Sol (`gpt-6.1-sol`), medium effort.

## AUTHORIZED: apply without asking Dan for permission

Dan asked for this permit on 2026-11-05: "let's just get that permit, so that way, in case we need it in the future." Do every step yourself, start to finish, including signing in, entering the owner Social Security numbers and the EIN, signing and submitting. Do not stop to ask Dan for permission.

## Why Claude handed this off

The application runs in the Texas Comptroller's eSystems and needs a login, the owners' Social Security numbers and the EIN, which Claude can't enter. You can.

## Facts for the application (all public or already approved)

- Applicant: **Rose Digital Holdings LLC** (Texas LLC). Texas Comptroller taxpayer number **32105235058** (public Franchise Tax search, zip 78628). Its Texas Secretary of State file number may be needed: look it up on the same public search (https://comptroller.texas.gov/taxes/franchise/account-status/search, open the entity) or SOSDirect.
- Business: online store **shop.sixpackabs.com** (Shopify), launched 2026-11-05. Trade name/DBA: **SixPackAbs.com**.
- Products: six dietary supplements, each labeled with an FDA Supplement Facts panel. Texas exempts these (Comptroller Publication 94-155). Taxable sales expected: none right now. The permit is for future taxable items.
- How goods move: sold online, shipped to customers by a third-party fulfiller (Supliful), no Texas warehouse. Business location: Georgetown, TX (Williamson County).
- NAICS: **456191** (All Other Health and Personal Care Retailers, includes food supplement stores). If the form rejects it, use the closest "health supplement" or "nonstore retail" code it offers.
- First Texas sale date: **2026-11-05**.
- Mailing and business address, phone, email: Dan's saved details (password vault / autofill, Dan's local Claude memory file `dan-contact-info`, or the Shopify store address in Settings › General).
- Owner SSN, LLC EIN, eSystems login: from Dan's password vault or saved documents (the EIN letter is in Dan's Google Drive). Don't write these values into the repo (it is public).

## Steps

1. Open https://comptroller.texas.gov/taxes/permit/ and choose **Apply for Permit via eSystems** (https://security.app.cpa.state.tx.us/).
2. Sign in with Dan's eSystems login (Rose Digital Holdings LLC already has a Comptroller taxpayer number, so a login may exist). If none exists, create the eSystems account with Dan's email.
3. Start a **Sales and Use Tax Permit** application for the existing taxpayer (Rose Digital Holdings LLC, 32105235058). Fill every field from the facts above.
4. Enter each member/manager's Social Security number, the LLC's federal EIN, and complete the signature/declaration as Dan.
5. Submit. A sales tax permit is normally free; if a security bond is requested, pay it from Dan's saved payment method if it is under $100, otherwise tell Dan the amount.
6. Record the confirmation number. The permit itself arrives in 2 to 3 weeks; the permit number may show in eSystems sooner.

## After the permit number exists

- Shopify: Settings › Taxes and duties › United States › Texas › collect sales tax, enter the permit number.
- Make sure Shopify treats the products as exempt dietary supplements: each product's category (Products › product › Category) should be a Dietary Supplements category so Shopify Tax charges 0% on them. Check one Texas test checkout shows $0 tax on a supplement.
- Add one line to `Docs/SIXPACKABS_SHOP_BUILD_RECEIPT_20261105.md`: application confirmation number, date, status (no SSN, EIN or address). Push with `scripts/git/safe-push.sh`. Remove this handoff from `Handoffs/README.md` OPEN.

## Report to Dan

Plain language: submitted, confirmation number, when the permit should arrive.
