# Handoff: Google Ads compliance pages + AI-image labeling

**Date:** 2026-07-30
**Project:** Abs By AI (absbyai.com)
**Business goal this serves:** Marketing performance — this is a hard prerequisite for opening a Google Ads account without it being suspended on initial review. No ads = no paid acquisition channel.

## Objective

Build the legal/compliance pages absbyai.com is missing, label the AI-generated before/after imagery, and surface the trial→auto-renew billing terms before checkout — so that a new Google Ads account survives initial review and Business Operations Verification. Dan asked specifically what pages are needed; the research is done (this doc), the build is not.

## Current State

**Site architecture (important — this shapes the whole plan):** absbyai.com is a **single-page app**. `public/index.html` is ~509 KB and contains ~33 JS-hidden `<section>` screens (hub, macro tracker, trainer, paywall, membership, etc.). Everything the product does lives at ONE URL. The only real second page is `public/privacy.html`.

**What exists today:**
- `public/privacy.html` — a real standalone page (~3.4 KB). Sections: Photos you upload, Payments, Analytics, Age requirement, Data retention, Your choices, Contact. Functional but thin for a service that collects body photos and ships them to three third-party AI providers.
- `server.js:8456` — explicit `app.get('/privacy')` route so it's linked as `/privacy` without `.html`. Same pattern at `:8462` for `/morningbrief`.
- `server.js` SPA fallback `app.get('*')` serves `index.html` for everything unmatched, so **new pages need explicit routes or they'll be swallowed by the fallback** (static files under `public/` are served first by `express.static`, so `/terms.html` would work — but `/terms` would not).
- Footer, repeated on several screens (e.g. `public/index.html:2048`, `:2234`, `:2348`): `Powered by Claude + Gemini · <a href="/privacy">Privacy</a>`. Privacy is the ONLY legal link on the site.
- **Refund + billing + cancellation copy already written** — but buried in the member hub FAQ at `public/index.html:2114-2118`, behind login. Says: billed same day monthly/yearly, cancel via Manage subscription card or email, **full refund within 7 days, no questions asked**. A Google reviewer will never see it.
- A "not medical advice" disclaimer exists but only inside the Supplement Audit verdict (`public/index.html:8533`, `verdictDisclaimer`).

**What does not exist:** terms of service, refund policy page, contact page, site-level disclaimer, public FAQ, about page, how-it-works page, or any footer linking them.

## Key Decisions Already Made

- **Every new page must be a real separate URL served as its own HTML file** — NOT another hidden SPA screen. Adding SPA screens would add zero compliance value, because the whole problem is that a crawler/reviewer landing cold on absbyai.com sees only a headline and an upload box. Google's *Insufficient original content* policy disallows destinations that are blank or have no content; the site isn't actually thin, it just looks thin to a crawler.
- **Copy the `public/privacy.html` pattern** for all new pages (self-contained HTML, inline `<style>`, Manrope from Google Fonts, `.wrap` max-width 720px, `#f6f5f2` bg, `#1b1a18` text) — visual consistency and zero new build tooling.
- **Reuse the refund/billing copy that already exists** in the member-hub FAQ rather than writing new terms. It's already accurate; it just needs to be public.
- **Dan's own three guesses (privacy, disclaimer, FAQ) were right but incomplete** — the full list is 8 pages, and the highest-risk gap is Terms of Service, because the product is a free-trial-into-auto-renew subscription. Google: *"Failure to clearly and conspicuously disclose the payment model or full expense that a user will bear before and after purchase is not allowed."*
- **The pages are NOT the biggest suspension risk** — the AI before/after imagery is. Do not treat the labeling work (step 3 below) as optional polish.
- **Physical address for Contact = the CAN-SPAM address already in use:** Abs By AI, 3520 Cavu Rd., Georgetown, TX 78628. Don't invent a different one; consistency across the site and the email footer is part of what a reviewer checks.

## Detailed Plan

### Step 1 — Build the tier-1 pages (blocking for ads)

Create in `public/`, each modeled on `privacy.html`:

1. **`terms.html`** — the single biggest gap. Must cover: what the service is; that outputs are AI-generated images; trial length; the exact amount charged when the trial converts; billing frequency; that it auto-renews; how to cancel (self-serve in Manage subscription, or email); acceptable use; limitation of liability; governing law (Texas). Pull real numbers from the live membership screen — do not guess prices.
2. **`refunds.html`** — lift the 7-day no-questions-asked policy verbatim from `public/index.html:2117`. Include how to request one.
3. **`contact.html`** — business name, support email, the Georgetown TX address, and expected response time.
4. **`disclaimer.html`** — two parts, both needed: (a) not medical advice, consult a physician before changing training/nutrition/supplements/medication — reuse the wording at `public/index.html:8533`; (b) **results disclaimer** — images are AI-generated visualizations, not predictions, not typical results, not a guarantee.
5. **Expand `public/privacy.html`** — keep the existing sections, add explicit coverage of: biometric/photo data; that photos are processed by named third-party AI providers (Google Gemini, Replicate/BytePlus Seedream, Anthropic); retention periods; the account-deletion path that already ships (member hub → Account → Delete my account); and PostHog analytics.

### Step 2 — Build the tier-2 pages (fixes the "thin site" perception)

6. **`faq.html`** — public. Source copy already exists in the member-hub FAQ; expand with pre-purchase questions (what do I get, is my photo private, what does it cost, is this real).
7. **`about.html`** — who runs the business and what it does. Google's destination-requirements guidance asks for *"updated contact information and a clear explanation of what your company does."*
8. **`how-it-works.html`** — plain-text upload → AI generation → result walkthrough. Doubles as a compliance asset: it's where the site states in its own words that the output is AI-generated.

### Step 3 — Label the AI imagery (highest-risk item, do not skip)

Every before/after in the proof strip and marketing surfaces needs a visible "AI-generated visualization — not a real result" label **on or immediately adjacent to the image**, not in a footer. Google explicitly prohibits before/after images that misrepresent effectiveness, names *Manipulated media* as its own Misrepresentation sub-policy, and treats weight loss as a restricted health category with stricter rules. The proof strip lives in `#proofStrip` in `public/index.html` (see the 2026-07-19 proof-banner work in `AI_COORDINATION.md` for its structure and the `.proof-slide` grid layout).

### Step 4 — Routes and footer

- In `server.js`, immediately after the existing `/privacy` route (`:8456`), add explicit routes for all new slugs. Prefer a single loop over an array (`['terms','refunds','contact','disclaimer','faq','about','how-it-works']`) rather than eight copy-pasted handlers. Must be registered **before** the `app.get('*')` SPA fallback at `:8467`.
- Replace the footer string (three-plus occurrences: `public/index.html:2048`, `:2234`, `:2348` — grep for `Powered by Claude + Gemini` to catch them all) with a footer linking every legal page. Keep it on the logged-out landing screen at minimum; that's the page the ad clicks land on.

### Step 5 — Billing disclosure at the point of purchase

Put the trial → auto-renew terms in plain sight **on the checkout/membership screen, above the payment field** — not only in Terms. This is the specific behavior Google's policy language demands ("clearly and conspicuously ... before and after purchase"). `#membershipSection` in `public/index.html`.

### Step 6 — Verify `support@absbyai.com` actually delivers

**OPEN — needs Dan.** The in-app FAQ (`public/index.html:2116-2117`) tells users to email `support@absbyai.com`. Known from the 2026-07-22 mailbox work: `dan@absbyai.com` forwards to Gmail via Namecheap Email Forwarding. It is **not confirmed** that a `support@` forwarder exists. A dead support address on a subscription site is a real misrepresentation problem. Fix = add the forwarder in Namecheap (Dan's login), or change the site copy to `dan@absbyai.com`. Cheapest path is probably to just use `dan@`.

### Step 7 — Ship and verify

Per `AGENTS.md`: commit, push to `main`, confirm the Railway deploy, and verify each new URL live on absbyai.com (200, renders, correct content, links work) at 375×812 and desktop. **No native retest needed** — new standalone web pages touch no row in the cross-platform trigger table. (If step 5 changes anything visible on `#membershipSection`, that DOES hit the mandatory "anything showing a price, buy button, or Manage membership" row → run `scripts/native-smoke-test.sh` and report the result.)

### Step 8 — Only then, open the Google Ads account

Expect **Business Operations Verification**, where Google reviews the business model, website, customers, and licenses. Account is paused if not completed by the deadline; review takes up to 5 business days.

## Things to Avoid / Lessons Learned

- **Do not add these as SPA screens.** The entire point is separate crawlable URLs. Hidden screens inside `index.html` solve nothing.
- **Do not register routes after the `app.get('*')` fallback** in `server.js` — they'd be dead.
- **Do not invent prices or trial terms.** Read them off the live membership screen / Stripe config. Wrong billing terms in a Terms page is worse than no Terms page.
- **Do not bury the AI-generated label in a footer.** It has to be on the image.
- **Remarketing constraint for campaign setup (not a website task, but plan for it):** Google prohibits remarketing/personalized audiences on sensitive health categories including weight loss. Whoever builds the campaigns needs to know this up front — it can't be retrofitted.
- **Google publishes no literal "required pages" checklist.** The requirements are behavioral (disclose billing, don't overpromise, be reachable); pages are the evidence. Don't expect to find a Google doc listing these eight pages — it doesn't exist, and re-searching for one is wasted time.
- The `*-data.json` files in the repo root are the production database (GitHub-API persisted). Don't touch them, and don't include them in this task's commit.

## Relevant Files & Locations

| Thing | Where |
|---|---|
| Page template to copy | `public/privacy.html` |
| Route registration point | `server.js:8456` (`/privacy`), before `app.get('*')` at `:8467` |
| Existing refund/billing/cancel copy | `public/index.html:2114-2118` |
| Existing medical disclaimer wording | `public/index.html:8533` (`verdictDisclaimer`) |
| Footer to replace (3+ spots) | `public/index.html:2048`, `:2234`, `:2348` — grep `Powered by Claude + Gemini` |
| Proof strip (AI images to label) | `#proofStrip` in `public/index.html` |
| Membership/checkout screen | `#membershipSection` in `public/index.html` |
| Native smoke test | `scripts/native-smoke-test.sh` |
| Live site | https://absbyai.com |
| Business address (CAN-SPAM, reuse it) | Abs By AI, 3520 Cavu Rd., Georgetown, TX 78628 |

**Google policy sources (already researched — don't re-derive):**
[Misrepresentation](https://support.google.com/adspolicy/answer/6020955) · [Unacceptable business practices](https://support.google.com/adspolicy/answer/15938071) · [Unreliable claims](https://support.google.com/adspolicy/answer/15936857) · [Insufficient original content](https://support.google.com/adspolicy/answer/16427718) · [Destination requirements](https://support.google.com/adspolicy/answer/6368661) · [Advertiser verification](https://support.google.com/adspolicy/answer/9703665) · [Health in personalized advertising](https://support.google.com/adspolicy/answer/16701855) · [Restricted targeting](https://support.google.com/adspolicy/answer/143465)

## Model & Effort Recommendation

| Scenario | Recommendation |
|---|---|
| **If Claude usage is low right now** | Claude Sonnet 5, standard thinking. The build is mechanical (8 static pages from an existing template + a route loop + a footer swap); the hard thinking is done and captured above. |
| **If Claude usage is high / approaching a limit** | Split it: have **Codex (flagship, medium effort)** do steps 1–2 page scaffolding, routes, and footer — well-specified, low-ambiguity file work. Bring **Claude** back for the actual legal/marketing copy and step 3 image labeling. |

**Task-type override:** the *copy* on these pages is brand voice and legal-risk writing — that's an always-Claude task regardless of usage. Codex can build the shells; don't let it write the Terms or the results disclaimer. Sonnet 5 is sufficient — no need for Opus here.

## Starter Prompt for the Next Task

> Read `handoff-20260730-google-ads-compliance-pages.md` in the Abs By AI project root, then execute it.
>
> Context: Dan is opening a Google Ads account and the site is missing the legal/compliance pages a reviewer looks for. The policy research is already done and is in that doc — don't re-research Google's policies, and don't go looking for an official "required pages" checklist (there isn't one).
>
> Start with Step 1: create `public/terms.html`, `public/refunds.html`, `public/contact.html`, and `public/disclaimer.html`, modeled on the existing `public/privacy.html` (same inline-style pattern, Manrope, 720px `.wrap`). Before writing the Terms page, read the live membership/checkout screen and Stripe config to get the real trial length, price, and billing frequency — do not guess them. Reuse the refund copy already at `public/index.html:2117`.
>
> Then work through Steps 2–7 in order. Commit, push to `main`, confirm the Railway deploy, and verify every new URL live on absbyai.com before reporting done. Flag Step 6 (whether `support@absbyai.com` actually delivers) to Dan — that one needs his Namecheap login or a copy change.
