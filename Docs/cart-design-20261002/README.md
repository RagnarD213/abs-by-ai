# The approved web cart (locked by Dan, 2026-10-02)

This folder is the versioned spec for the new web cart. Build handoff: `Handoffs/handoff-20261002-cart-build.md`.
Matching sales-page change: `Handoffs/handoff-20261002-start-page-365-guarantee.md`.

- Canvas (private): https://claude.ai/artifact/WUrxcVvv6mZNmnjt3LqrPa, page **APPROVED: final cart**.
- `boards/Final-Cart-Phone.dc.html`: phone, Monthly picked (390 wide).
- `boards/Final-Cart-Phone-Lifetime.dc.html`: phone, Lifetime picked.
- `boards/Final-Cart-Desktop.dc.html`: desktop (1200 wide, 1040 px content, form column plus right column).
- `gen.py`, `measure.sh`, `heights.json`: the generator that wrote the boards (`blue_board(NAVY, D, start, 'yellow')`).
  The boards are plain HTML with inline styles: port the markup and the styles. Canvas-only parts to drop: the `x-dc`
  wrapper and script, the fixed board height, `{{holes}}` and `<sc-if>` (they mark what changes with the plan).

How the design was reached (five rounds, research first): `Docs/cart-research-20261002/`, memory
`cart-follows-start-button`, and the earlier canvas pages.

## What Dan locked

1. **Entry.** The buyer arrives straight from a buy button on `/start` (`/?join=1&from=vsl`). No uploaded photo, no goal
   picture, no body numbers anywhere on the cart. None of Dan's before and after pictures.
2. **Structure** (Healthy Back Institute's free-trial cart): top box with the app picture and callout, new-members
   notice, three numbered steps on one page (Your Email, Order Summary, Payment Information), the terms with a tick box
   directly above the button, contact and statement lines, the guarantee, Dan's photo and quote, footer.
3. **Look.** Deep navy `#12306B` for the top stripe, the 1/2/3 step headers, the pay buttons, the notice outline and
   label, the selected-plan outline, the email link and the footer. **The guarantee seal is gold since 2026-10-03**
   (Dan: the same gold seal as `/start`, on top of the card and centred; the boards still show the navy circle). Selected-plan tint `#EEF1F8`.
   Yellow `#FFD23F` with black text for the "FREE 7 days" callout, and yellow for the underline under "Make It Real."
   Green `#15803D` only on the buy button. Red `#C9302D` only on "FREE!" and the required stars. Paper `#F6F4F0`,
   hairline `#E4E1DB`, ink `#05070B`, Manrope 500/600/700/800. No black sections.
4. **Guarantee:** 365 days.
5. **Plans** (at the top of Order Summary, Monthly pre-selected):
   - Monthly: "7 days free, then $19.99 a month". $0 today.
   - Lifetime (badge "Pay once"): "7 days free, then a one-time charge of $69.99 for lifetime access, no recurring
     billing." $0 today. Not a subscription. Dan calls it the annual plan; it replaces Annual on the web cart.
6. **Picking Lifetime** removes "How This Free Trial Offer Works", its three paragraphs and the tick box, and shows the
   Lifetime sentence in a box above the button. The button reads "Start My Free Trial" for both plans.
7. **Phone vs desktop.** The bullet box ("How Abs By AI gets you to your goal:") is desktop only, in the right column
   above the guarantee. On the phone the guarantee sits under the contact lines.
8. **Removed on purpose:** "Questions?" line at the top (it stays under the button), card-brand chips, member comments,
   the doctor or trainer slot, the founder quote from round 2, the "continue without a trial" link, the cart video slot,
   the goal-image recap, the trial timeline.

## Copy, exactly as approved

Top box: "See Yourself With Abs, Then Get An AI Fitness Plan To Make It Real." / "Claim Your Free 7-Day Trial Today!"
Callout: "FREE 7 days". Notice: "NEW MEMBERS ONLY" / "This special, one time offer is only available to new Abs By AI members."
Step 1: "Your Email"; field "Email"; "Your email becomes your login. No password needed today."
Step 2: "Order Summary"; "Choose your plan"; the two plans above; line item "Abs By AI Membership, Free 7-Day Trial"
($19.99 struck, FREE!) or "Abs By AI Lifetime Access, Free 7-Day Trial" ($69.99 struck, FREE!); Subtotal $0.00;
Sales Tax $0.00; Order Total $0.00.
Step 3: "Payment Information"; Apple Pay; Pay with Link; "or pay by card"; Name on Card, Credit Card Number, Expiration, CVV.
Terms (Monthly only): "How This Free Trial Offer Works"
- "With your order today, you get the full Abs By AI membership free for 7 days. You pay $0 today."
- "You will automatically be enrolled as a monthly member and will have 7 days to try everything. If you love it, do
  nothing and you stay a member at the Members Only price of $19.99 a month. Your card is billed $19.99 on day 7 and
  every month after that until you decide to cancel."
- "You can cancel quickly and easily anytime in two taps (Manage membership, then Cancel) or by emailing
  dan@absbyai.com. Cancel before day 7 and you pay nothing."
- Tick box: "By checking this box, you are agreeing to the terms of the offer stated above."
Lifetime box: "7 days free, then a one-time charge of $69.99 for lifetime access, no recurring billing."
Button: "Start My Free Trial"; under it "SECURE 256-BIT ENCRYPTION".
Contact: "Questions Before You Order?" / dan@absbyai.com / "Your purchase will appear on your statement under the name:
[STATEMENT NAME]" / "Goal pictures are AI visualizations, not real results. Individual results vary."
Guarantee: "365-Day No Risk 100% Money Back Guarantee" / "We guarantee you'll love Abs By AI or we'll refund your
money." / "If you're not happy for any reason, email us within 365 days of your first payment for a full refund. No
questions asked."
Desktop bullet box: "How Abs By AI gets you to your goal:" then six bullets (see the desktop board).
Dan's quote, beside the upper-body photo (`public/img/letter/dan-note.jpg`), signed "Dan Rose / Founder, Abs By AI":
"I know you'll love Abs By AI. It's changed thousands of guys' lives, and it will change yours too. That's why I'm
offering you the chance to try it completely free for seven days. And after that, you can use Abs By AI for a full YEAR
at my risk. So try Abs By AI at my risk - it could be the key to getting the body you've always wanted."
Footer: "Copyright (c) 2026 Abs By AI", Terms of Service, Privacy Policy.

The boards are the authority if this list and a board ever disagree.
