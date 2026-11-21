# Handoff: add the 365-day guarantee to the sales page (/start) so it matches the cart

Written 2026-10-02 by Claude (Opus 5.5), the Cart Mockups session. Not executed.
Recommended: **Claude Opus 5.5, high effort.** Suggested task name: `Start Page Guarantee`.
Use the `/design-sales-page` skill: it holds the locked layout, the generator and the proof scripts for `/start`.

## 1. Goal

Dan locked a new cart on 2026-10-02 with a **365-Day No Risk 100% Money Back Guarantee**. The sales page at
`absbyai.com/start` sends buyers to that cart and says nothing about a guarantee today, and the site's refund policy
page still says 7 days. Make the sales page and the policy pages say what the cart says.

Two parts, because one of them has to wait for the cart:

- **Part A, ship now:** the guarantee on `/start`, and the refund wording on the policy pages.
- **Part B, ship with the cart or right after it:** the lines that describe the second plan, which changes from
  "$69.99 a year" to a one-time $69.99 for lifetime access. The cart build is
  `Handoffs/handoff-20261002-cart-build.md`. **Update 2026-10-03: that cart is live** (`Docs/WEB_CART.md`), the
  site now sells Monthly and Lifetime, so part B is unblocked and ships with part A.

## 2. Source of truth

| item | where |
|---|---|
| The approved cart: guarantee block, colours, every line of copy | `Docs/cart-design-20261002/README.md` and `boards/` |
| Cart canvas (private) | https://claude.ai/artifact/WUrxcVvv6mZNmnjt3LqrPa, page **APPROVED: final cart** |
| Sales page canvas (private) | https://claude.ai/artifact/GM8Han9hMfSHNf625vqtyu, page **Round 2** |
| Sales page generator and live builder | `.claude/skills/design-sales-page/reference/round2-letter/`: `gen.py`, `build_live.py`, `verify_live.py`, `README.md` |
| The live page | `public/start.html` (built by `build_live.py`, never edited by hand) |
| Dan's letter (copy source) | Google Doc `1zCLn6pIuxGv4H1hkyieCk2T4NoYAQBnaNKMEFMcYV9o` |
| Policy and info pages | `public/refunds.html`, `public/faq.html`, `public/terms.html` |

## 3. Part A: the guarantee

**Wording. Use only these lines, which Dan approved on the cart. Write no new guarantee copy.**

- Title: "365-Day No Risk 100% Money Back Guarantee"
- "We guarantee you'll love Abs By AI or we'll refund your money."
- "If you're not happy for any reason, email us within 365 days of your first payment for a full refund. No
  questions asked."
- Short form for a one-line row under a button: "365-Day Money Back Guarantee"

**Look.** The same block as the cart, so a buyer sees the same badge on both pages: a paper card (`#F6F4F0`, 16 px
corners), a round seal reading "365 DAY" in the cart's navy `#12306B` with a white ring, the title beside it, the two
sentences under it. This adds one colour to the sales page. Everything else on `/start` keeps its locked design
system (see the skill). Mock it before building (step 2 below) so Dan sees it once.

**Where it goes (defaults; section names are the `data-k` keys in `public/start.html`):**

1. `offer1`, the offer card under the video: the one-line row under the terms line.
2. `try`, the "Try Abs By AI Free For 7 Days" section: the full guarantee card under the button and its terms line.
3. `faq`: a new question after "Is there a catch?": "What if I don't like it?" answered with the two approved
   sentences.
4. `final`, the closing block: the one-line row under the last button's terms line. Do not put anything between the
   button, "I'll see you inside. Dan" and his photo: that order is locked.

No guarantee row under the buttons inside the story sections. The pinned top stripe stays as it is.

**Policy and info pages (same deploy as the sales page change):**

- `public/refunds.html`: the callout and the membership paragraph say "within 7 days". Rewrite them to the 365-day
  guarantee, after decision 1 below. Leave the sections on credit packs and prints alone.
- `public/faq.html`: "Charged and changed your mind? Full refund within 7 days, no questions asked" becomes the
  365-day line.
- Then `grep -rn -i "refund\|money back\|within 7 days" public/ server.js` and fix any other sentence that now
  disagrees (welcome emails in `server.js` included). Do not touch the Apple or Google refund handling.
- These pages show `support@absbyai.com` and the cart shows `dan@absbyai.com`. Keep each as it is.

## 4. Part B: the second plan's wording (only once the new cart is live)

Lifetime replaces Annual on the web cart: "7 days free, then a one-time charge of $69.99 for lifetime access, no
recurring billing." These lines then disagree with it. Proposed replacements, for Dan's one approval:

| where | today | proposed |
|---|---|---|
| `/start` FAQ, "How much is it?" | "Nothing for 7 days. After that, $19.99 a month or $69.99 a year. That's it." | "Nothing for 7 days. After that, $19.99 a month, or a one-time charge of $69.99 for lifetime access. That's it." |
| `/start` section `s10`, under the button | "Renews automatically at the plan price until you cancel. Cancel anytime in the app in two taps. Cancel before day 7 and you are never charged." | "Monthly renews automatically at $19.99 until you cancel. Lifetime is a one-time charge of $69.99, no recurring billing. Cancel anytime in the app in two taps. Cancel before day 7 and you are never charged." |
| `public/terms.html`, the price list and the renewal sentence | "Annual: $69.99" and "(monthly or yearly)" | Add Lifetime as a one-time charge with no renewal. Keep Annual, described as the plan existing annual members and the apps are on. |
| `public/refunds.html`, membership paragraph | "(monthly or annual, ...)" | Name Monthly, Lifetime and Annual. |

"Pick a plan. Both start with 7 days free." stays: it is still true. Every "$0 today. Then $19.99/month until you
cancel." line stays: Monthly is still the default.

## 5. Decisions for Dan (ask once, at the start, in one message)

1. **What "a full refund" covers for a Monthly member.** The approved line promises "a full refund" for 365 days from
   the first payment. For a Monthly member that reads as every payment made in those 365 days. Confirm that, or say it
   is the most recent payment only, in which case the line on the cart changes too. The refund policy page cannot be
   rewritten until this is answered. **Recommendation: every payment in the 365 days, because that is what the
   approved sentence says.**
2. The navy seal on the sales page, matching the cart (he will see it in the mockup). **Default: yes.**
3. The four placements in section 3. **Default: yes.**
4. The four wording changes in section 4. **Default: yes, shipped when the cart is live.**
5. Optional: Dan's cart quote ("...you can use Abs By AI for a full YEAR at my risk...") beside the guarantee card in
   the `try` section. **Default: no, the letter already closes in his voice.**

## 6. Steps

1. Read this doc, the skill, `Docs/cart-design-20261002/README.md` and the sales-page generator README.
2. Add the guarantee to `gen.py` as two pieces (the card and the one-line row) and place them. Rebuild only the
   boards that change and publish them to the sales page canvas as a new page, "Round 3: guarantee", phone and desktop.
   Send Dan the link with section 5. One approval covers the look, the placements and the wording.
3. Re-export Dan's doc and confirm the letter has not changed since 2026-09-30 (`rebuild_blocks.py`). The guarantee
   lines are additions that are not in the doc: add them to the allow list the proof script uses, and tell Dan the
   exact lines so he can add them to the doc, or offer to add them as suggestions.
4. Run `build_live.py`, then `verify_live.py` (it must pass), then check `public/start.html` at phone and desktop
   widths in the preview: the video still sits above the fold on a phone, the stripe still pins, every button still
   goes to `/?join=1&from=vsl&v=letter-v1` with the click ids.
5. Rewrite the policy pages (section 3) after decision 1.
6. Commit only this task's files with `scripts/git/safe-push.sh`, confirm the Railway deploy, verify live on
   `https://absbyai.com/start`, `/refunds` and `/faq`. One push: every deploy drops locked image holds.
7. Part B: when the cart task reports the new cart is live (or if it already is), apply section 4 the same way and
   deploy. If the cart is not live yet, leave one board line saying part B is waiting on it.
8. Update the skill (`design-sales-page/SKILL.md`: the guarantee block is now part of the locked layout, with its
   placements) and `Docs/VSL_LANDING.md`. Report to Dan in plain words. Delete this handoff's lines from
   `AI_COORDINATION.md` and `Handoffs/README.md` when both parts are shipped.

## 7. Out of scope

The cart itself and anything about payments (the other handoff), the letter's wording beyond the lines listed here,
the video, the page layout, prices, ad campaigns, the native apps.

## Starter prompt

```
Read Handoffs/handoff-20261002-start-page-365-guarantee.md in full and execute it with the /design-sales-page skill.
Rename this task "Start Page Guarantee". Add the 365-day money back guarantee from my approved cart to absbyai.com/start
and bring the refund policy and FAQ pages into line with it. Show me the mockup and ask the section 5 decisions once,
then build and ship part A. Part B (the Lifetime plan wording) ships only when the new cart is live.
```
