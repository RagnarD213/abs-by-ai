# App Review reply — Guideline 5.1.1(v), sent 2026-08-26

Thread `eed31ff7-71da-34c5-8d08-5f75bc549a65` (REJECTION_REVIEW_SUBMISSION),
message `ae1b6217-5cfa-4e29-ae99-5e68c041de87`, sent 2026-08-26 22:48 UTC, 2,430 chars.

**Posted BEFORE cancelling submission 22876374 — and the thread stayed open
(`canDeveloperAddNote: true`) afterwards.** That is the opposite of the 2026-08-22
outcome, where removing the version first killed the reply channel. Rule confirmed:
reply first, then do submission surgery.

## What Apple said (rejection, 2026-08-26 21:18 UTC, iPad Air 11-inch (M4), 1.0 (3))

Guideline 5.1.1(v) — Legal — Data Collection and Storage:

> We noticed that the app requires users to register with personal information to
> purchase In-App Purchase products that are not account based. ... revise the app to
> not require users to register before purchasing In-App Purchase products that are not
> account based. You may explain to the user that registering will enable them to access
> the purchased content from any of their supported devices and provide them a way to
> register at any time ... it is not appropriate to force user registration to meet this
> requirement; such user registration must be optional.

Only the app-version item was rejected. The subscription group and both subscriptions
stayed READY_FOR_REVIEW, so the 3.1.2 EULA fix and the 2.1(b) IAP fix both held, and the
1.1 body-morph objection did not recur.

## The text sent

Hello, and thank you for the detailed note.

We would like to ask you to reconsider the 5.1.1(v) finding, because the membership our In-App Purchase unlocks is account based in the sense the guideline describes. It is not a feature unlock placed behind a registration wall.

What the subscription buys is a coach that stores and rewrites the subscriber's own plan. All of the following is server side and keyed to that individual user's record:

1. AI Trainer: a 7 stage progression stored in a per user program record. At the end of each 28 day block the app promotes or holds the user based on how many workouts THAT user logged, and writes the next block against their own history.
2. AI Nutritionist: a meal plan generated from that user's intake, then adjusted at every check in.
3. Macro Tracker, Progress Log, Sleep Coach and Supplement Audit: each one reads and writes that user's own stored history.

There is nothing in the membership that is not the buyer's own saved plan, and nothing that could be delivered to an anonymous device. A purchase with no account would have nothing to attach to and nothing to show. Guideline 5.1.1 permits required registration where it is tied to account specific functionality, and we believe this is that case.

On the data itself: we ask for an email address and a password, and nothing else. No name, phone number, address, date of birth, contacts, or social sign in. The account can be deleted from inside the app at Member Hub > Account > Delete my account.

We have also made the change your message suggested, and it is live now. The app loads its interface from our server, so this applies to build 1.0 (3) exactly as submitted:

1. The membership screen now explains, above the price and before the buy button, that the plan and progress are stored in the account, and that this is what makes the membership work on every Apple device the user signs in on.
2. The sign up screen reached from Subscribe now carries the same explanation, states that only an email and a password are collected, and notes that the account can be deleted at any time.

If after this you still consider the requirement inappropriate, we will change it rather than argue further. It would help us a great deal if you could tell us which membership feature you judge not to be account based, because from our side each one of them is that user's own stored plan.

Thank you for your time.
Daniel Rose

## The evidence behind the claim (not in the letter, but this is what it rests on)

- `server.js:7114` `/api/program/checkin` — reads `programs WHERE id = $1 AND user_id = $2`,
  computes `completedDays` from that user's logged workout dates, and promotes or holds
  their stage. The ladder cannot exist without an account row.
- Every membership feature is `requireAuth` + `isActiveMembership(userRow)`:
  `/api/program/week`, `/api/program/checkin`, `/api/program/equipment-track`,
  `/api/mealplan/swap`, `/api/mealplan/checkin`, `/api/counsel/followup`,
  `/api/supplement/brand`, `/api/progress/recap`.
- Sign-up form is email + password only (`public/index.html`, `#authEmail` / `#authPassword`).
- `parseAppUserId()` at `server.js:6099` rejects RevenueCat's anonymous
  `$RCAnonymousID:…` form — an anonymous purchase has no account to attach to.

## The fallback if Apple holds

Allow the purchase anonymously, then offer (not require) registration afterwards:
RevenueCat aliases the anonymous app-user id to `users.id` on `logIn()`, so the
entitlement transfers. Costs: `parseAppUserId` and the webhook need a device-scoped
path, and a buyer who skips registration owns a coach they cannot use until they
register. All of it is web-served, so it still would not need a new binary.
