# Private morning brief: Google sign-in prerequisites

This is a proposed setup and implementation plan, not a configured login. No credentials, grants, consent settings, sessions, allowlists or live routes were created or changed.

## Existing architecture

At source baseline `e3fb909`, product accounts use email/password and Postgres sessions lasting 90 days. `requireAuth` reads a Bearer token, not a browser cookie. The product frontend mirrors its token in localStorage and a script-readable `absbyai_sess` cookie. The admin API checks `ADMIN_EMAILS` after product authentication.

The `/morningbrief` HTML page instead uses `DASH_SECRET` with an `absbyai_dash` signed HttpOnly cookie lasting one year. Its shared secret and dashboard API header do not identify Daniel. An existing product Bearer token cannot authenticate an ordinary HTML navigation by itself. Google sign-in is not implemented. The product users table requires both a password hash and device ID, so a brief-only identity should not silently create a product account or alter billing/credits.

Recommended implementation: a separate brief-owner session, backed by a pinned Google subject (`sub`), with a persistent HttpOnly, Secure, SameSite=Lax cookie. Use a 90-day device session as the initial default, with renewal while active. Every brief HTML/data/image route must enforce the same owner gate. Store actual brief data and personal images outside public Git and `public/`; the current web gate cannot make a public GitHub file private. Keep product login and dashboard behavior outside this narrow change.

## Exact proposed Google client setup

| Field | Proposed value |
| --- | --- |
| Cloud project | Existing `abs-by-ai`, documented project number `768453214640`. Verify it in Console before creation. |
| Client type/name | New **Web application**, `Abs By AI Private Brief (Web)` |
| Authorized JavaScript origin | `https://absbyai.com` |
| Authorized redirect URI / GIS login URI | `https://absbyai.com/api/brief/auth/google` |
| Entry page after implementation | `https://absbyai.com/brief-login` |
| Successful login destination | `https://absbyai.com/morningbrief` |
| Authorized domain | `absbyai.com` |
| Branding homepage / privacy / terms | `https://absbyai.com/`, `https://absbyai.com/privacy`, `https://absbyai.com/terms` |
| Authentication scopes | Default identity scopes only: `openid`, `email`, `profile` |
| New runtime public configuration | `BRIEF_GOOGLE_CLIENT_ID` |
| Private owner configuration | Confirm Daniel's exact Google account, then pin its verified `sub` as `BRIEF_OWNER_GOOGLE_SUB`. Keep it outside Git. |

The proposed callback route does not exist yet. Use a Google Identity Services button with redirect mode; its credential POST is handled only by the proposed endpoint. Verify Google's CSRF cookie/body token, ID-token signature, exact audience, issuer and expiry with `google-auth-library`, then enforce the pinned owner identity before creating a session. Account linking, if requested later, must prove ownership of the existing product account rather than trusting an email match alone.

A client secret, refresh token, offline access, Gmail scope, Calendar scope and Ads scope are not needed for this ID-token sign-in design. The dot's Gmail/Calendar access remains a separate connection. The existing `GOOGLE_CLIENT_ID` is an Ads client whose documented registered redirect is OAuth Playground; use a dedicated client and do not repurpose it or change its existing grant/consent status.

For later local OAuth testing only, register `http://localhost` and one fixed `http://localhost:<port>` origin plus the exact local callback on that port. The synthetic layout prototype has no OAuth flow and needs no Google client. Do not register production preview URLs or www variants without a deliberate hosting decision.

## Decisions and authorization still needed

1. Confirm which exact Google account should own the private brief. The Ads access account in older project documents is evidence of Ads access, not confirmation of Daniel's preferred sign-in identity.
2. Get explicit authorization for creating the dedicated OAuth web client and any necessary branding/domain configuration. The current request expressly holds credential/grant and live access changes. Daniel handles any passkey/account confirmation or consent prompt.
3. Confirm the client ID and pinned owner subject privately, then authorize the scoped authentication implementation and production rollout separately. No other Google user should obtain a brief session. Do not bootstrap ownership from the first arbitrary Google login.
4. Prove persistent sessions on iPad Safari, phone and desktop, including refresh, restart, logout and a different Google account being denied. Browser storage behavior must be tested, not promised.

## References

- [Current session and admin code](https://github.com/RagnarD213/abs-by-ai/blob/e3fb909daa110cf11df00399e560aa415b456002/server.js#L4755), [current dashboard gate](https://github.com/RagnarD213/abs-by-ai/blob/e3fb909daa110cf11df00399e560aa415b456002/server.js#L242), [product storage](https://github.com/RagnarD213/abs-by-ai/blob/e3fb909daa110cf11df00399e560aa415b456002/public/index.html#L6084), [existing Ads project/client](https://github.com/RagnarD213/abs-by-ai/blob/e3fb909daa110cf11df00399e560aa415b456002/Docs/GOOGLE_ADS_API.md#L88).
- [Google client/origin/redirect setup and identity scopes](https://developers.google.com/identity/gsi/web/guides/get-google-api-clientid).
- [Google server token verification, CSRF and subject identity](https://developers.google.com/identity/gsi/web/guides/verify-google-id-token).
