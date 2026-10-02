# Private morning brief: Google sign-in prerequisites

The owner-login and private page code is implemented and tested locally. Live login is not configured. No Google credentials, grants, consent settings or live permissions have been changed. Daniel approved the dedicated client for his chosen account and the scoped push on October 2; that identity stays in private runtime configuration.

## Existing architecture

At source baseline `e3fb909`, product accounts use email/password and Postgres sessions lasting 90 days. `requireAuth` reads a Bearer token, not a browser cookie. The product frontend mirrors its token in localStorage and a script-readable `absbyai_sess` cookie. The admin API checks `ADMIN_EMAILS` after product authentication.

The `/morningbrief` HTML page instead uses `DASH_SECRET` with an `absbyai_dash` signed HttpOnly cookie lasting one year. Its shared secret and dashboard API header do not identify Daniel. An existing product Bearer token cannot authenticate an ordinary HTML navigation by itself. Google sign-in is not implemented. The product users table requires both a password hash and device ID, so a brief-only identity should not silently create a product account or alter billing/credits.

Implemented in `scripts/brief/web`: a separate brief-owner session, backed by a pinned Google subject (`sub`), with a persistent HttpOnly, Secure, SameSite=Lax cookie. Random session tokens are stored only as hashes in separate private Postgres tables, last 90 days, renew after 30 days of use and are revoked on logout. Every brief HTML/data/image route enforces the same owner gate before the shared dashboard gate or public static files. Private structured editions and optional image bytes live in these tables, never public Git. Product login and dashboard behavior remain separate.

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
| Private owner configuration | `BRIEF_OWNER_EMAIL` is Daniel's approved exact Gmail account. The first successful Google-verified token for that exact address atomically pins its `sub` in the private database. Optional `BRIEF_OWNER_GOOGLE_SUB` adds an explicit configuration check. |

The callback code uses a Google Identity Services button in redirect mode. It verifies matching CSRF cookie/body tokens and uses Google's official `google-auth-library` for signature, audience, issuer and expiry. The token must also have the exact configured verified Gmail address; only that owner can initialize the persistent subject pin. Later tokens must match the pin. No arbitrary first-user bootstrap or product account linking exists. The compatible verifier dependency is pinned to version 10.0.0 for this backend's Node 18 runtime; its signature verification is exercised with synthetic keys in the tests.

A client secret, refresh token, offline access, Gmail scope, Calendar scope and Ads scope are not needed for this ID-token sign-in design. The dot's Gmail/Calendar access remains a separate connection. The existing `GOOGLE_CLIENT_ID` is an Ads client whose documented registered redirect is OAuth Playground; use a dedicated client and do not repurpose it or change its existing grant/consent status.

For later local OAuth testing only, register `http://localhost` and one fixed `http://localhost:<port>` origin plus the exact local callback on that port. The synthetic layout prototype has no OAuth flow and needs no Google client. Do not register production preview URLs or www variants without a deliberate hosting decision.

## Decisions and authorization still needed

1. Daniel confirmed his preferred owner account and approved client creation on October 2. Configure it privately as `BRIEF_OWNER_EMAIL`; do not infer it from the Ads grant.
2. Create the dedicated OAuth web client with the exact Console fields above. Browser/computer control is not exposed in this implementation session, and no Google Cloud credential-management connector is available. Console creation therefore needs Daniel's handoff or the parent's authorized browser workflow. Daniel completes credential/passkey, binding agreement or security-sensitive permission steps that require handoff/confirmation.
3. Set the returned client ID and approved owner email on the existing Railway service. Parent completed these two public/identity variables with deployments skipped on October 2. No Google scopes beyond identity are needed. Deploy only the scoped code integrated with fresh main, then prove owner login and wrong-account denial before publishing private content.
4. For the manual proof, the signed-in owner uses `/brief-publish` to upload the reviewed private edition. The server requires the owner session, exact same origin and a custom publication header. No ingestion secret is required. For later machine publication only, Daniel can configure a separate random `BRIEF_INGEST_SECRET` of at least 32 characters directly in the existing service and its private local runner. Do not send secret values through chat or model-visible configuration tools. Parent can instead design a supported opaque-authentication publication route before scheduling.
5. Prove persistent sessions on iPad Safari, phone and desktop, including refresh, restart, logout and a different Google account being denied. Browser storage behavior must be tested, not promised.

## Hosting and current proof boundary

On October 2, `absbyai.com` resolved to `blz3qyjz.up.railway.app`; HTTPS returned `Server: railway-hikari` and Railway edge/request headers. Railway serves production. The old Vercel deployment guide is historical. The separate Vercel integration still attempts feature-branch deployments and currently fails on its missing Anthropic secret. Do not move production, alter that secret or claim a Vercel failure is a Railway deployment failure.

Local HTTP tests prove unauthenticated and other-account denial, tampering/CSRF rejection, restart-persistent database sessions, renewal/logout, private publication validation and page/data/image gates. They use only synthetic identities and an in-memory database. Real Google login, production deployment, actual Safari persistence and visual QA remain unproven. Nothing schedules or enables the routine.

## References

- [Current session and admin code](https://github.com/RagnarD213/abs-by-ai/blob/e3fb909daa110cf11df00399e560aa415b456002/server.js#L4755), [current dashboard gate](https://github.com/RagnarD213/abs-by-ai/blob/e3fb909daa110cf11df00399e560aa415b456002/server.js#L242), [product storage](https://github.com/RagnarD213/abs-by-ai/blob/e3fb909daa110cf11df00399e560aa415b456002/public/index.html#L6084), [existing Ads project/client](https://github.com/RagnarD213/abs-by-ai/blob/e3fb909daa110cf11df00399e560aa415b456002/Docs/GOOGLE_ADS_API.md#L88).
- [Google client/origin/redirect setup and identity scopes](https://developers.google.com/identity/gsi/web/guides/get-google-api-clientid).
- [Google server token verification, CSRF and subject identity](https://developers.google.com/identity/gsi/web/guides/verify-google-id-token).
