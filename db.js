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
  `);
  console.log('Postgres schema ready');
}

module.exports = { pool, initDb };
