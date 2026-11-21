# HANDOFF — Admin Panel + Free Beta Accounts

**Goal:** an admin panel at `absbyai.com/admin`, gated by Dan's normal site login
(danroseconsulting@gmail.com + his existing password). Its only feature for now:
create/list/revoke **permanent free beta accounts** with full membership access —
no Stripe transaction, no expiry, no feature limits.

**Recommended model:** Sonnet 5 · medium effort. This follows existing,
well-documented server/UI patterns (same rationale as membership work item 2 in
`MEMBERSHIP_PLAN.md`). After implementation, run `/code-review` on the diff —
the admin gate is security-sensitive.

---

## Context (read first, do not rebuild)

- Accounts live in Postgres (`db.js`): `users` has `membership_status`,
  `membership_plan`, `membership_period_end`, `stripe_customer_id`,
  `stripe_subscription_id`. No schema change is needed for this feature.
- Session auth: `requireAuth` (server.js ~line 2050) reads `Authorization:
  Bearer <token>` and attaches `req.user = { id, email, device_id }`.
  Login/signup at `/api/auth/login` / `/api/auth/signup` (~2070–2125).
- **The single membership gate:** `isActiveMembership(userRow)` (server.js
  ~2475). Every premium endpoint calls it — trainer, generations bypass of
  credits (~1815), meal analysis, Counsel, Sleep Coach, etc. Opening this gate
  opens everything; there are no separate per-feature limits for members.
- Stripe webhook sync (`syncSubscriptionState`, ~2653) updates rows **by
  `stripe_subscription_id`**. Beta accounts will have none, so Stripe events
  can never touch them. `trialReminderSweep` (~2668) only targets
  `'trialing'` — beta accounts get no billing emails.
- `/dashboard` is served as a static page (server.js ~121) — `/admin` follows
  the same serving pattern but its API must be auth-gated (see below).

## Design decisions (already made — do not relitigate)

1. **A beta account is a normal user row with `membership_status = 'comp'`,
   `membership_plan = 'beta'`, `membership_period_end = NULL`.** Permanent by
   design: add `if (status === 'comp') return true;` to `isActiveMembership`.
2. **Admin = allowlisted email(s) on the existing session auth.** New env var
   `ADMIN_EMAILS` (comma-separated, lowercase-trimmed). If unset/empty, every
   admin API returns 503 and the feature is inert. Production value:
   `danroseconsulting@gmail.com`. No new password/secret — Dan logs in with
   his normal account credentials.
3. **No expiry, no caps.** Revocation is manual via the panel.
4. Free membership ≠ free physical prints. Print checkout (canvas/poster/
   keychain) is intentionally untouched — beta testers pay for prints like
   anyone else.

## Implementation spec

### 1. server.js — admin gate

```
const ADMIN_EMAILS = (process.env.ADMIN_EMAILS || '')
  .split(',').map(s => s.trim().toLowerCase()).filter(Boolean);

async function requireAdmin(req, res, next) — runs requireAuth, then:
  - if ADMIN_EMAILS is empty → 503 { error: 'Admin not configured' }
  - if !ADMIN_EMAILS.includes(req.user.email) → 403 { error: 'Not authorized' }
```

Apply `authLimiter` + `requireAdmin` to every `/api/admin/*` route. The gate
must be server-side on each route — hiding UI is not access control.

### 2. server.js — membership gate + checkout exemption

- `isActiveMembership` (~2475): add the `'comp'` status branch (one line).
- `/api/stripe/create-membership-checkout` (~2528): the "already have an
  active membership" rejection must NOT fire when `row.membership_status ===
  'comp'` — a beta tester who wants to pay may subscribe; the webhook then
  overwrites comp with a real subscription (acceptable: paying wins).
  Comp rows have no `stripe_subscription_id`, so `isFirstSubscription` stays
  true and they still get the 7-day trial.

### 3. server.js — admin endpoints

- `POST /api/admin/beta-members` — body `{ email, password? }`.
  - Normalize email like signup does (trim/lowercase, `EMAIL_RE`, ≤254).
  - Existing user → `UPDATE users SET membership_status='comp',
    membership_plan='beta', membership_period_end=NULL WHERE email=$1`.
    Respond `{ created: false, email }`. If the row already has status
    `'active'`/`'trialing'` (real paying member), 409 — never overwrite a
    paid subscription with a comp.
  - New user → create like signup: bcrypt hash (cost 10), `device_id =
    'beta-' + crypto.randomBytes(6).toString('hex')`, then set the comp
    fields. If no password supplied, generate one
    (`crypto.randomBytes(9).toString('base64url')`) and return it ONCE in the
    response `{ created: true, email, tempPassword }`. Never log passwords.
    Do NOT push admin-created accounts to MailerLite (testers didn't opt in).
- `GET /api/admin/beta-members` — `SELECT email, created_at FROM users WHERE
  membership_status='comp' ORDER BY created_at DESC`.
- `DELETE /api/admin/beta-members/:email` — `UPDATE ... SET
  membership_status=NULL, membership_plan=NULL, membership_period_end=NULL
  WHERE email=$1 AND membership_status='comp'`. The status guard means this
  can never cancel a real subscription. 404 if no row matched.

### 4. admin.html — new file, served at `/admin`

Serve like `/dashboard` (server.js ~121). Single self-contained page:

- **Login view:** email + password → `POST /api/auth/login`; keep the token in
  `localStorage` under a NEW key (e.g. `absai_admin_token`) so it doesn't
  collide with the app's `AUTH_TOKEN_KEY`. After login, call
  `GET /api/admin/beta-members`; a 403 means logged-in-but-not-admin — show
  "This account doesn't have admin access." and a logout button.
- **Panel view:** form (email, optional password, "Create beta account"
  button) + table of current beta members (email, created date, Revoke
  button with confirm). When a temp password comes back, display it in a
  copy-to-clipboard box with a "shown only once" note.
- Keep it plain — same lightweight inline-CSS approach as `dashboard.html`.
  No framework, no build step.

### 5. index.html — membership screen handles `'comp'`

`/api/membership` will return `{ active: true, status: 'comp', plan: 'beta',
periodEnd: null }`. In `#membershipSection` (~2012) and any hub badge logic:
render a simple "Beta tester — full access" state; hide plan cards, renewal
date, and the Stripe billing-portal/cancel controls (there's no subscription
to manage). Search index.html for where `status`/`periodEnd` from
`/api/membership` drive the UI.

### 6. .env.example

Add `ADMIN_EMAILS=` with a one-line comment.

## Testing (all local, `DATABASE_URL=pgmem://`)

1. Signup dan@test.com; set `ADMIN_EMAILS=dan@test.com`; login on `/admin` →
   panel loads.
2. Signup tester@test.com (normal user) → admin grants → `GET /api/auth/me` +
   `/api/membership` for tester shows `active: true, status: 'comp'`; an
   image generation does NOT decrement `/api/credits` for their device.
3. Create brand-new beta account from panel → temp password shown once →
   login works with it.
4. Revoke → membership inactive again; revoke is a no-op on a row with
   status `'active'` (seed one manually to prove the guard).
5. Grant to an email with status `'active'` → 409.
6. Negative auth: logged out → 401; logged in as non-admin → 403;
   `ADMIN_EMAILS` unset → 503.
7. Comp user can open membership checkout (no "already active" rejection).

## Deploy steps (Dan)

1. Merge + deploy to Railway.
2. Add `ADMIN_EMAILS=danroseconsulting@gmail.com` env var on Railway.
3. Visit `absbyai.com/admin`, log in with the existing account password.

**Security note for Dan:** admin access is now exactly as strong as that
account's password — make sure it's long and unique, since password reset
emails could otherwise become an admin-takeover path.

## Out of scope (separate handoffs)

- Protecting `/dashboard` and `/api/morning-data` → `HANDOFF_dashboard_auth.md`.
- Free/discounted physical prints for testers — not planned.
