---
name: ios-appstore-prep
description: "iOS App Store submission history through rejection 5 (5.1.1(v), argued 2026-08-26) + ASC API/Resolution Center mechanics and simulator gotchas"
metadata: 
  node_type: memory
  type: project
  originSessionId: 8b09ccf3-a078-4285-893b-01b39f332040
  modified: 2026-08-06T14:56:00.954Z
---

App Store submission prep executed July 22 2026 (`handoff-20260722-ios-appstore-submission-prep.md`). Walkthrough of all features in the [[ios-capacitor-app]] shell passed; screenshots (6 shots, 6.9" 1320×2868 native + 6.5" 1242×2688 scaled) and full listing copy live in `app-store-assets/` (LISTING_COPY.md holds the reviewer demo credentials: danroseconsulting+applereview@gmail.com).

Demo account is comp-granted and pre-populated (real transformation + real Trainer program, no paywall). Listing copy finalized with Dan's own subtitle/promo/description intro; app markets to men (female-audience line explicitly declined).

**SUBMITTED to Apple 2026-07-25 (~4:50 PM CT).** Free, build 1.0 (1). **REJECTED 2026-08-05** under 1.4.1 (uncited medical claims) and 3.1.1 (external purchases with no IAP — the "hide the buy buttons" reader-app strategy was a misreading; fitness apps don't qualify). Fixes shipped same day (citations/sources page + US-storefront external purchase links, commits `5f45501` + `bcf8142`), availability narrowed to US-only. **Dan RESUBMITTED 2026-08-05 at 10:12 AM — back to `Waiting for Review` (verified in App Store Connect 2026-08-06). Do not prompt Dan to resubmit again; the only iOS action is waiting for Apple's verdict.** Details in `AI_COORDINATION.md`.

App Store Connect gotchas learned at submission (each one blocked "Add for Review"):
- **A universal build requires 13-inch iPad screenshots** (2064×2752) even if you only care about iPhone. The iPad Pro 13-inch sim captures at exactly that size. Abs by AI renders fine on iPad (centred column), so keeping iPad support beat going iPhone-only, which would have needed a rebuild + re-upload.
- **Price and App Availability are not set by default** and are easy to miss — the version page looks complete without them.
- Screenshots land in **upload-completion order, not filename order** — drag one at a time and verify after. A prior session's set uploaded scrambled.
- App Store Connect **silently rejects PNGs with an alpha channel** — always flatten to RGB.
- The 6.5" iPhone slot auto-mirrors the 6.9" slot ("Using 6.9" Display"), so only 6.9" needs uploading.
- **EU DSA trader status:** declaring trader publishes the address/phone/email **publicly** on EU App Store pages, and Apple documents no self-serve way to edit it afterwards (status *can* be changed later; contact info reportedly cannot). Dan's account is an Individual enrolment, so the default address is his home. Chose non-trader/no-EU for now — the non-trader → trader direction is the documented one. PO boxes are accepted but need a receipt/bill proving association.

Simulator gotchas worth remembering:
- Fresh Debug `xcodebuild` builds of the wrapper fail to launch on a second simulator (RunningBoard POSIX 163 / SBMainWorkspace denial); install the known-good App.app from a working device's Bundle container instead.
- To move a logged-in session between simulators: copy the `absbyai_*` keys between the apps' WKWebView `localstorage.sqlite3` (values are UTF-16LE blobs; use python sqlite3, not the sqlite3 CLI).
- iOS WebKit `input[type=time]` ignores container width unless `-webkit-appearance:none` (fixed in commit `d76c590`).
- On cold boot, some of the parallel account syncs (program/counsel) can silently fail while others succeed — relaunch fixes; suspect the sitewide rate-limit bucket (N2).

**Rejection 4 — 3.1.2, fixed 2026-08-24.** Automated rejection: auto-renewable subscriptions but no
Terms of Use (EULA) link in the App Description. No custom EULA is set on the app, so Apple's check
wants `https://www.apple.com/legal/internet-services/itunes/dev/stdeula/` in the description itself.
Fixed by appending a SUBSCRIPTION block (both prices + auto-renew disclosure + privacy + stdeula) —
never delete it. The 1.1 body-morph objection did NOT recur, so that argument held.

ASC API mechanics for a resubmission (cost real time to work out):
- A rejected submission's items **cannot** be freed with `DELETE /v1/reviewSubmissionItems/{id}` (409
  "already submitted"). Use `PATCH /v1/reviewSubmissions/{id}` `{"canceled": true}`; it clears in
  ~10–20 s, then items are re-addable.
- `POST /v1/reviewSubmissionItems` accepts **only** an `appStoreVersion` relationship. The
  subscription group and each subscription must be added in the ASC UI (**Add for Review → the
  existing Draft iOS Submission**) — three separate items; adding the group does not add its subs.
- Submit with `PATCH /v1/reviewSubmissions/{id}` `{"submitted": true}`.

**Rejection 5 — 5.1.1(v), argued 2026-08-26.** Apple, reviewing 1.0 (3) on an iPad Air 11-inch:
"requires users to register with personal information to purchase In-App Purchase products that are
not account based." Only the app-version item was rejected — the subscriptions stayed
READY_FOR_REVIEW, and 1.1 did not recur for a second round. **We argued rather than rebuilt**, because
the membership genuinely is account-based: every member endpoint is `requireAuth` +
`isActiveMembership`, and `/api/program/checkin` (server.js) promotes or holds a 7-stage ladder stored
in `programs.user_id` from that user's own logged workouts. Sign-up takes email + password only.
Also shipped the explanation Apple's own message suggested (paywall + the auth screen reached from
Subscribe). Resubmitted as `ccc7a7ae-103b-4f1d-a142-4552e48a456a`.

⚠ **The iOS app loads absbyai.com live, so the purchase screen and every other UI surface is
WEB-SERVED — a metadata/UX rejection can usually be fixed with a deploy against the already-reviewed
binary, with no new build and no TestFlight cycle.** This is the single most useful fact for the next
rejection.

**Resolution Center is readable and writable from code**, via the ASC web UI's internal *iris* API
using the browser's logged-in session (the public ASC API carries no rejection text):
`GET /iris/v1/apps/{app}/resolutionCenterThreads`, then
`/iris/v1/resolutionCenterThreads/{id}/resolutionCenterMessages`. Replying is two steps —
`POST /iris/v1/resolutionCenterDraftMessages` (messageBody + `resolutionCenterThread`), then
`POST /iris/v1/resolutionCenterMessages` with a **`createFromDraftMessage`** relationship. A malformed
POST 409s naming the required relationship, so the schema can be probed without creating anything.

⚠ **Post any Resolution Center reply BEFORE cancelling the submission.** Doing it in that order on
2026-08-26 left the thread open (`canDeveloperAddNote: true`); doing it the other way round on
2026-08-22 destroyed the reply channel. Also: a rejected version cannot be resubmitted in place
(`PATCH {submitted:true}` → 409 "not ready to be submitted"), and cancelling detaches the subscription
group and subs back to Developer Rejected, so all three must be re-added in the UI every time.

**Status checks + expedite (2026-09-10).** Once a submission is IN_REVIEW, the prior rejection's
Resolution Center thread is CLOSED to new notes (draft POST → 409 "Cannot add draft message to closed
thread") even though `canDeveloperAddNote` still reads true — there is no written status-question channel.
Apple's expedite form (developer.apple.com/contact/app-store/?topic=expedite) has **no message field**: App
Name is a type-ahead (must click the suggestion, which fills the hidden Apple ID), Platform, then Send — and
it was **granted instantly** ("We'll expedite review for Abs by AI"; a rejection-resubmit stays in the
expedited queue). Used once for `ccc7a7ae` after 15 days; Apple warns excessive requests get refused.
