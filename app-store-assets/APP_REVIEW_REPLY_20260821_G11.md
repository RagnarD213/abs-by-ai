# App Review reply — Guideline 1.1 (body morphing) + 2.1(b) IAP, rejection of 2026-08-20

Submission `be7d8b49-7cc5-49b2-ba60-72b779437e77`, version reviewed 1.0 (2). Paste into the rejection thread's Reply box (4,000-char limit; this text is within it). Send AFTER the revised metadata, IAP submissions, and new binary (1.0 build 3) are all attached to the version — the reply references them as done.

**Status: APPROVED by Dan 2026-08-21.**

---

## Reply text (paste verbatim)

```
Hello,

Thank you for the review. Guideline 2.1(b) is now fully resolved, and we would respectfully ask you to reconsider the Guideline 1.1 finding — we believe Abs by AI was pattern-matched into a category it does not belong to.

GUIDELINE 1.1 — ABS BY AI IS A FITNESS COACHING APP, NOT A BODY EDITOR

We understand and support Apple's action against apps that let users alter photos of other people's bodies — tools that enable harassment, bullying and body-shaming. Abs by AI is not that kind of app, for four concrete reasons:

1. SELF-ONLY, BY DESIGN. The feature exists for one purpose: a user visualizing their OWN fitness goal from their OWN photo. There is no mechanism to browse, receive or share other people's images inside the app; generated images are private to the account that made them. The pipeline also hard-refuses photos of apparent minors and runs content moderation on inputs and outputs.

2. EXPLICIT INFORMED CONSENT. Before any photo is processed, an in-app consent screen names every AI provider involved, and declining cancels the action. The Face data section of our privacy policy (absbyai.com/privacy) documents this.

3. CLEARLY LABELED AS ILLUSTRATIVE AI. Every generated image is presented as an AI-generated goal image, and the app and store listing state that results are "illustrative goals, not guarantees." It is a motivational target, not a claim about the user's body.

4. THE PRODUCT IS COACHING. The goal image is step one of a fitness program, not the product. The app's substance — and what the subscription sells — is an AI Trainer (personalized 4-week workout program), AI Nutritionist (weekly meal plans), photo-based macro tracking, a sleep coach, a supplement review, progress logging and a daily coaching brief. Self-visualization of a fitness goal within a coaching product is an established, accepted pattern on the App Store.

We have also revised the app's metadata for this submission — description, promotional text and screenshot order — so the fitness-coaching purpose is unmistakable and the goal-visualization feature reads as exactly that.

GUIDELINE 2.1(b) — COMPLETED

Both auto-renewable subscriptions (Monthly, com.absbyai.app.membership.monthly, $19.99/month; Annual, com.absbyai.app.membership.annual, $69.99/year; both with a 7-day free trial) are now submitted for review with this app version, each with an App Review screenshot of the in-app subscription screen. A new binary, 1.0 (3), has been uploaded and attached to the version as instructed.

NOTE FOR REVIEW: the demo account in App Review Information is a complimentary full member and intentionally shows no purchase UI. To see the subscription screen, create a free account, then open Member Hub > Membership.

Thank you for your time — happy to provide anything further.
```

---

## SUBMITTED 2026-08-22

Submission `a5fcdbf2-3eca-412e-8c20-b1f075a32c24` sent to Apple 2026-08-22 19:12 UTC with 4 items
(app version 1.0 build 3, subscription group 22294450, Monthly, Annual) — all WAITING_FOR_REVIEW.
Note: the version had to be removed from the dead rejected submission `be7d8b49` first (red minus in
its ACTION column), then re-added to the draft via the ASC API — `POST /v1/reviewSubmissionItems`
with an `appStoreVersion` relationship. A version can only belong to one submission at a time, and
the UI's "Update Review" button re-attaches it to the OLD rejected submission, which silently splits
the version away from the subscriptions. That split is what caused the 2.1(b) rejection. The
subscription GROUP must also be added as its own submission item, separately from the two products.

## App Review Notes — 1.1 block to PREPEND to the Notes field

The rejection thread `be7d8b49` is now marked "Removed", so a reply there may not reach the next
reviewer. The Notes field is the reliable channel. Prepend this above the existing notes:

```
GUIDELINE 1.1 - THIS IS A FITNESS COACHING APP, NOT A BODY EDITOR. Users can only visualize their OWN fitness goal from their OWN photo. There is no way to browse, receive, or alter images of other people - the harassment vector Apple's policy targets does not exist here. An in-app consent screen names every AI provider before any photo is processed, and declining cancels the action. Every generated image is labeled as an AI-generated illustrative goal, not a guarantee. The pipeline hard-refuses photos of apparent minors and moderates inputs and outputs. The product is coaching: AI Trainer, AI Nutritionist, macro tracking, sleep coaching, supplement review, progress logging - the goal image is step one of a program, not the product. Metadata for this version was revised to make that unmistakable.
```
