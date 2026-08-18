// Postgres access for accounts, sessions, and cloud-synced meals.
// Requires DATABASE_URL (Railway Postgres). When it's unset (e.g. local dev
// without a DB), pool stays null and the auth/meals endpoints return 503 —
// the rest of the app is unaffected.
const { Pool } = require('pg');

const DATABASE_URL = process.env.DATABASE_URL;

// Dev-only: DATABASE_URL=pgmem:// runs an in-memory Postgres (pg-mem,
// devDependency) so login/signup work in local preview without installing
// Postgres. Data resets on every restart. Never set this on Railway.
function makeMemPool() {
  const { newDb } = require('pg-mem');
  return new (newDb().adapters.createPg().Pool)();
}

const pool = DATABASE_URL
  ? DATABASE_URL.startsWith('pgmem')
  ? makeMemPool()
  : new Pool({
      connectionString: DATABASE_URL,
      // Railway's public proxy uses a self-signed chain; internal URLs don't
      // need SSL at all. Only relax verification for non-local hosts.
      ssl: /localhost|127\.0\.0\.1|railway\.internal/.test(DATABASE_URL)
        ? false
        : { rejectUnauthorized: false },
    })
  : null;

async function initDb() {
  if (!pool) {
    console.log('DATABASE_URL not set — accounts/meal-sync disabled');
    return;
  }
  await pool.query(`
    CREATE TABLE IF NOT EXISTS users (
      id            SERIAL PRIMARY KEY,
      email         TEXT UNIQUE NOT NULL,
      password_hash TEXT NOT NULL,
      device_id     TEXT NOT NULL,
      before_image  TEXT,
      after_image   TEXT,
      created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
    );
    CREATE TABLE IF NOT EXISTS sessions (
      token      TEXT PRIMARY KEY,
      user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
      expires_at TIMESTAMPTZ NOT NULL
    );
    CREATE TABLE IF NOT EXISTS meals (
      id        SERIAL PRIMARY KEY,
      user_id   INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      date      TEXT NOT NULL,
      logged_at TIMESTAMPTZ NOT NULL DEFAULT now(),
      meal_name TEXT,
      totals    JSONB NOT NULL,
      items     JSONB NOT NULL DEFAULT '[]'
    );
    CREATE INDEX IF NOT EXISTS meals_user_date_idx ON meals (user_id, date);
    CREATE TABLE IF NOT EXISTS saved_preps (
      id           SERIAL PRIMARY KEY,
      user_id      INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      name         TEXT NOT NULL,
      servings     INTEGER NOT NULL,
      remaining    INTEGER NOT NULL,
      per_serving  JSONB NOT NULL,
      batch_totals JSONB,
      created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
    );
    CREATE INDEX IF NOT EXISTS saved_preps_user_idx ON saved_preps (user_id, id);
    CREATE TABLE IF NOT EXISTS programs (
      id           SERIAL PRIMARY KEY,
      user_id      INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      block_number INTEGER NOT NULL DEFAULT 1,
      intake       JSONB NOT NULL,
      program      JSONB NOT NULL,
      progress     JSONB NOT NULL DEFAULT '{}',
      created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
    );
    CREATE INDEX IF NOT EXISTS programs_user_idx ON programs (user_id, id);
    CREATE TABLE IF NOT EXISTS meal_plans (
      id          SERIAL PRIMARY KEY,
      user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      plan_number INTEGER NOT NULL DEFAULT 1,
      intake      JSONB NOT NULL,
      plan        JSONB NOT NULL,
      created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
    );
    CREATE INDEX IF NOT EXISTS meal_plans_user_idx ON meal_plans (user_id, id);
    CREATE TABLE IF NOT EXISTS counsel_sessions (
      id            SERIAL PRIMARY KEY,
      user_id       INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      decision_type TEXT NOT NULL,
      intake        JSONB NOT NULL,
      opinions      JSONB NOT NULL,
      verdict       JSONB NOT NULL,
      followups     JSONB NOT NULL DEFAULT '[]',
      created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
    );
    CREATE INDEX IF NOT EXISTS counsel_sessions_user_idx ON counsel_sessions (user_id, id);
    CREATE TABLE IF NOT EXISTS sleep_entries (
      id         SERIAL PRIMARY KEY,
      user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      entry_date DATE NOT NULL,
      source     TEXT NOT NULL,
      data       JSONB NOT NULL,
      briefing   JSONB,
      created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
      UNIQUE (user_id, entry_date)
    );
    CREATE INDEX IF NOT EXISTS sleep_entries_user_idx ON sleep_entries (user_id, entry_date);
    CREATE TABLE IF NOT EXISTS transformations (
      id           SERIAL PRIMARY KEY,
      user_id      INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      before_image TEXT NOT NULL,
      after_image  TEXT NOT NULL,
      settings     JSONB NOT NULL DEFAULT '{}',
      is_hero      BOOLEAN NOT NULL DEFAULT false,
      created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
    );
    CREATE INDEX IF NOT EXISTS transformations_user_idx ON transformations (user_id, id);
    CREATE TABLE IF NOT EXISTS weight_logs (
      id         SERIAL PRIMARY KEY,
      user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      entry_date DATE NOT NULL,
      weight     REAL NOT NULL,
      unit       TEXT NOT NULL DEFAULT 'lb',
      flags      JSONB NOT NULL DEFAULT '[]',
      created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
      UNIQUE (user_id, entry_date)
    );
    CREATE INDEX IF NOT EXISTS weight_logs_user_idx ON weight_logs (user_id, entry_date);
    CREATE TABLE IF NOT EXISTS progress_entries (
      id          SERIAL PRIMARY KEY,
      user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      entry_date  DATE NOT NULL,
      photo_front TEXT NOT NULL,
      thumb_front TEXT,
      photo_side  TEXT,
      photo_back  TEXT,
      waist       REAL,
      waist_unit  TEXT DEFAULT 'in',
      recap       JSONB,
      created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
      UNIQUE (user_id, entry_date)
    );
    CREATE INDEX IF NOT EXISTS progress_entries_user_idx ON progress_entries (user_id, entry_date);
    CREATE TABLE IF NOT EXISTS coach_briefs (
      id          SERIAL PRIMARY KEY,
      user_id     INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      brief_date  DATE NOT NULL,
      fingerprint TEXT NOT NULL,
      brief       JSONB NOT NULL,
      created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
      UNIQUE (user_id, brief_date)
    );
    CREATE TABLE IF NOT EXISTS password_reset_tokens (
      token_hash TEXT PRIMARY KEY,
      user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      expires_at TIMESTAMPTZ NOT NULL,
      created_at TIMESTAMPTZ NOT NULL DEFAULT now()
    );
    CREATE TABLE IF NOT EXISTS audit_jobs (
      id         TEXT PRIMARY KEY,
      user_id    INTEGER,
      status     TEXT NOT NULL DEFAULT 'running',
      result     JSONB,
      error      TEXT,
      created_at TIMESTAMPTZ NOT NULL DEFAULT now()
    );
    -- Before/after images captured at email-signup, keyed by email (accounts and
    -- anonymous signups alike). Used to embed the user's own transformation in
    -- the welcome email. Stored as data-URI strings; served via /api/welcome-image.
    CREATE TABLE IF NOT EXISTS welcome_images (
      email        TEXT PRIMARY KEY,
      before_image TEXT,
      after_image  TEXT,
      created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
    );
  `);
  // Membership columns (added after the users table shipped). ADD COLUMN IF NOT
  // EXISTS keeps this idempotent across deploys; pg-mem supports it too.
  for (const col of [
    'stripe_customer_id TEXT',
    'stripe_subscription_id TEXT',
    'membership_status TEXT',
    'membership_plan TEXT',
    'membership_period_end TIMESTAMPTZ',
    // Which billing system owns this membership: 'stripe' (web checkout) or
    // 'apple' (In-App Purchase, via RevenueCat). NULL on legacy rows, which are
    // all Stripe or comp. Load-bearing: it is what stops the Stripe cancel path
    // (account deletion, billing portal) from ever touching an Apple-billed
    // subscription, and vice versa.
    'membership_source TEXT',
    // Trial-ending reminder: set once the "2 days left" email goes out (idempotent).
    'trial_reminder_sent_at TIMESTAMPTZ',
    // Progress Log settings + reminder bookkeeping
    'photo_day INTEGER',
    'weigh_reminder BOOLEAN DEFAULT false',
    'last_photo_nudge DATE',
    // Shared member profile: one JSONB record per account that every AI feature
    // reads (pre-fill intakes) and writes back to (factual updates only). Filled
    // by the pre-trial "Let's build your plan" quiz + seeded from the generation
    // funnel. A `_meta` sub-object holds per-field-group provenance. Behind auth
    // only — never expose in URLs or logs (holds age/weight/diet).
    "profile JSONB DEFAULT '{}'",
    // Google Ads click id (gclid, or gbraid/wbraid on iOS app campaigns), captured
    // from the landing URL and carried through signup and membership checkout.
    // Without this a paid membership can never be attributed back to the ad click
    // that produced it: the trial converts to paid ~7 days later, server-side, with
    // no browser present, so the only ways to report the sale are gtag's own
    // _gcl_aw cookie (same browser only) or an offline conversion upload keyed on
    // this id. Stored latest-wins, matching Google's last-click attribution.
    'ads_click_id TEXT',
    'ads_click_at TIMESTAMPTZ',
    // Trial → PAID membership, reported to Google Ads as the "Subscribe"
    // conversion. That moment happens server-side (Stripe webhook / RevenueCat
    // webhook) with no browser open, so it cannot be reported when it happens.
    // Instead the transition stamps `pending`, /api/membership hands the flag to
    // the client on the member's next visit, the client fires the conversion,
    // and the ack stamps `fired`. `fired` is the dedupe: it is per SUBSCRIPTION
    // (one row per account), deliberately not the per-browser localStorage
    // dedupe fireAdConversion() uses, so clearing storage or returning on a
    // second device can neither lose nor double-report the sale.
    'paid_conversion_pending_at TIMESTAMPTZ',
    'paid_conversion_fired_at TIMESTAMPTZ',
  ]) {
    try {
      await pool.query(`ALTER TABLE users ADD COLUMN IF NOT EXISTS ${col}`);
    } catch (e) {
      // pg-mem older versions lack IF NOT EXISTS on ADD COLUMN — retry plain.
      try { await pool.query(`ALTER TABLE users ADD COLUMN ${col}`); } catch (_) {}
    }
  }
  console.log('Postgres schema ready');
}

module.exports = { pool, initDb };
