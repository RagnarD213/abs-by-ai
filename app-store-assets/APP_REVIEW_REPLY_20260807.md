# App Review reply — submission c4dc7f48 (rejection of 2026-08-07)

Paste the text below into "Reply to App Review" in App Store Connect, and mirror the face-data answers into App Review Information notes. All three guideline sections are complete. The 3.1.1 answer reflects the decision taken 2026-08-07: build the membership as a real auto-renewable In-App Purchase (option a). Send this reply with the 1.0 (2) submission, once both subscriptions are attached to the version.

**Updated 2026-08-12** — the 3.1.1 section was rewritten after the full purchase-path audit (`Handoffs/handoff-20260812-ios-iap-purchase-audit.md`). Three things changed since the first draft and all three are live: the subscription IAP was sandbox-tested end to end on a real device; two membership buttons that still jumped straight to the browser were fixed (commit `1df0d01`); and one-time credit packs were retired on every platform (commit `067bbcd`), removing the last in-app link to a non-IAP digital purchase. Do not send the pre-2026-08-12 wording — it understated the fix and left the credit-pack link-out undisclosed.

---

Hello,

Thank you for the detailed review. We have made app and privacy-policy changes to address Guidelines 5.1.1(i)/5.1.2(i), and we answer the Guideline 2.1 face-data questions in full below.

## Guidelines 5.1.1(i) / 5.1.2(i) — Data sent to third-party AI services

We have updated the app (server-delivered, already live in the build under review, no new binary needed):

1. **In-app disclosure and permission before any data is sent.** Before a user's photo or personal details are first shared with an AI service, the app now shows a consent screen that states exactly what is sent and to whom: the user's photo (which may include their face) is sent to Anthropic (Claude) to check that it is usable and to Google (Gemini) — and for some generations ByteDance Seedream via Replicate — to create the image; fitness details the user enters (body info, goals, meals, sleep, supplements) are sent to Anthropic (Claude) to generate plans and analyses. The user must explicitly agree before anything is transmitted; declining cancels the action and no data leaves the device. To see it: tap "Upload your photo" on the home screen — the consent screen appears before the photo picker result is processed.
2. **Persistent disclosure** under the Generate button naming the AI providers, with a link to the Privacy Policy.
3. **Privacy policy updated** (https://absbyai.com/privacy, "Last updated: August 7, 2026") to identify what data the app collects, how it is collected (the user uploads photos and types in details directly), all uses of that data, the named third-party AI providers it is shared with, and that those providers process it solely to provide the service with equal or greater protection.

## Guideline 2.1 — Face data

**1. What face data does the app collect?**
The app does not use facial recognition and does not collect, compute, or store faceprints, facial geometry, or biometric identifiers or templates of any kind. The only "face data" handled is ordinary photographs the user voluntarily uploads (which may include their face) and the AI-generated fitness visualization images created from them.

**2. All planned use, sharing, retention, deletion, and storage practices.**
- **Use:** solely to check that the uploaded photo is usable and to generate the fitness visualization image the user requested. Never used for advertising, profiling, identification, or training AI models.
- **Sharing:** transmitted over an encrypted connection to service providers acting on our behalf: Anthropic (photo review), Google (image generation), and, for some generations, Replicate running the ByteDance Seedream model (image generation). They process the photo solely to provide this service to us. Never sold, never shared with data brokers or advertisers.
- **Storage:** for account holders, uploaded photos and generated images are stored in our database on servers in the United States (so they appear in the user's Transformations gallery). If a user provides only an email address to receive their result, the before/after image pair is stored with that email. Otherwise photos are held temporarily in server memory only long enough to complete the generation (up to about one hour) and are then discarded.
- **Retention:** until the user deletes the images or deletes their account; email-only images are deleted on request to support@absbyai.com; otherwise nothing is retained.
- **Deletion:** in-app at Member Hub → Account → Delete my account — a permanent, immediate deletion of every stored photo and generated image.

**3. Will the face data be shared with any third parties? Where will this information be stored?**
Shared only with the AI service providers named above, acting as processors on our behalf to create the user's requested image. Stored in our database hosted on servers in the United States (account holders and email submissions only, as described above).

**4. How long will face data be retained?**
Account holders: until they delete the image or their account. Email-only users: until they request deletion. All other users: not retained at all — held in server memory up to about one hour to complete the generation, then discarded.

**5. Where in the privacy policy is this explained?**
https://absbyai.com/privacy — the dedicated section titled **"Face data"** (six bullets covering collection, use, sharing, storage, retention, deletion), plus the sections "Photos you upload" and "Fitness details you enter (AI coaching features)".

**6. Quote the specific text from the privacy policy concerning face data.**
From the "Face data" section:
"What we collect: the only face data we handle is the photographs you choose to upload (your before photo, and any progress photos), which may include your face, and the AI-generated images we create from them. We do not use facial recognition, and we do not extract, compute, or store faceprints, facial geometry, or any other biometric identifiers or templates."
"How we use it: your photo is used for one purpose only — to check that the photo is usable and to generate the fitness visualization image you requested. Face data is never used for advertising, profiling, identification, or training AI models."
"Who it is shared with: to create your image, the photo is transmitted over an encrypted connection to our AI service providers — Anthropic (photo review), Google (image generation), and, for some generations, Replicate running the ByteDance Seedream model (image generation). They process the photo solely to provide this service to us. Face data is never sold and never shared with data brokers or advertisers."
"How long it is retained: stored photos and generated images are retained until you delete them or delete your account, at which point they are permanently deleted. If we hold images only against your email address, you can have them deleted at any time by contacting support@absbyai.com. Without an account or email submission, no photo is retained."

## Guideline 3.1.1 — Payments

Thank you for the clarification. The membership is now available for purchase inside the app using In-App Purchase.

Build **1.0 (2)** includes two auto-renewable subscriptions in a single subscription group, purchasable in the app via StoreKit:

- **Monthly Membership** — `com.absbyai.app.membership.monthly`, $19.99/month, with a 7-day free trial
- **Annual Membership** — `com.absbyai.app.membership.annual`, $69.99/year, with a 7-day free trial

Both are attached to this version for review. The purchase screen displays the title, duration and price of each subscription — read from StoreKit at runtime, so it always matches what Apple charges — together with the auto-renewal disclosure, a **Restore Purchases** control, and tappable **Terms of Use** and **Privacy Policy** links. A completed purchase unlocks the membership immediately; entitlements are verified server-side against the App Store receipt, and the app itself is never trusted to grant access. Subscriptions are managed and cancelled through the user's Apple ID, and the app links there for management. We have completed a full sandbox purchase on a physical device to confirm the flow end to end.

**We also audited every remaining purchase path in the app, and closed two further gaps.** Both fixes are server-delivered and already live in build 1.0 (2), with no new binary required:

1. **Two membership entry points still opened the browser directly.** The "Start 7-day free trial" button in the member-hub preview, and the membership link on the out-of-generations screen, were left over from the previous submission and bypassed the new purchase screen. Both now open the In-App Purchase screen described above.
2. **One-time credit packs have been discontinued entirely, on every platform.** The app previously offered a link out to our website to buy one-off image-generation packs. That content is no longer sold anywhere — to us or to any user, on iOS, Android or the web — and the link has been removed. Users who run out of free generations are now offered only the In-App Purchase subscription, or the option to continue to the rest of the app.

As a result, **there is no digital content or functionality purchasable in the app by any means other than In-App Purchase.** The only external links that remain are ones we understand to be permitted, and we would welcome correction if any is not: a link to manage or cancel an existing subscription in Apple ID Settings; a "prefer to pay on the website" alternative offered *alongside* In-App Purchase on the same screen under the US-storefront allowance; and a fallback link shown only in the event StoreKit is unavailable and no In-App Purchase can be offered. Printed posters and canvases remain a physical-goods purchase handled outside In-App Purchase, as required.

**To reach the purchase screen:** create a free account (or sign in), then open **Member Hub → Membership**. Please note that the demo account provided in App Review Information is a complimentary member account, so it intentionally displays no purchase UI. To see the In-App Purchase flow, please create a new free account in the app or remain signed out.

Thank you — we believe the app now fully addresses the privacy guidelines, and we're happy to provide any further detail.
