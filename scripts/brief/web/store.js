'use strict';
// Separate private tables, never product accounts or public Git-backed stores.
const crypto = require('crypto');
const hash = token => crypto.createHash('sha256').update(token).digest('hex');
function createStore(pool, ready = Promise.resolve()) {
  let initialized;
  async function init() {
    if (!pool) throw new Error('Private database unavailable');
    if (!initialized) initialized = Promise.resolve(ready).then(() => pool.query(`
      CREATE TABLE IF NOT EXISTS brief_owner (id INTEGER PRIMARY KEY CHECK (id = 1), email TEXT NOT NULL, google_sub TEXT NOT NULL);
      CREATE TABLE IF NOT EXISTS brief_sessions (token_hash TEXT PRIMARY KEY, google_sub TEXT NOT NULL, expires_at TIMESTAMPTZ NOT NULL);
      CREATE TABLE IF NOT EXISTS brief_document (id INTEGER PRIMARY KEY CHECK (id = 1), document JSONB NOT NULL);
      CREATE TABLE IF NOT EXISTS brief_image (id INTEGER PRIMARY KEY CHECK (id = 1), mime TEXT NOT NULL, bytes BYTEA NOT NULL);
      CREATE TABLE IF NOT EXISTS brief_publish_nonces (nonce_key TEXT PRIMARY KEY, expires_at TIMESTAMPTZ NOT NULL);
      CREATE TABLE IF NOT EXISTS brief_social_master (id TEXT PRIMARY KEY, record JSONB NOT NULL);
    `)).catch(e => { initialized = null; throw e; });
    await initialized;
  }
  return {
    async claimPublicationNonce(id, nonce, expires, now) {
      await init();
      await pool.query('DELETE FROM brief_publish_nonces WHERE expires_at <= $1', [new Date(now)]);
      try {
        await pool.query('INSERT INTO brief_publish_nonces (nonce_key, expires_at) VALUES ($1, $2)', [id+':'+nonce,new Date(expires)]);
        return true;
      } catch (error) {
        if (error.code === '23505') return false;
        throw error;
      }
    },
    async pinOwner(email, sub) {
      await init();
      await pool.query('INSERT INTO brief_owner (id, email, google_sub) VALUES (1, $1, $2) ON CONFLICT (id) DO NOTHING', [email, sub]);
      const result = await pool.query('SELECT email, google_sub FROM brief_owner WHERE id = 1');
      return result.rows[0];
    },
    async owner() { await init(); return (await pool.query('SELECT email, google_sub FROM brief_owner WHERE id = 1')).rows[0]; },
    async addSession(token, sub, expires) { await init(); await pool.query('INSERT INTO brief_sessions (token_hash, google_sub, expires_at) VALUES ($1, $2, $3)', [hash(token), sub, new Date(expires)]); },
    async session(token) { await init(); return (await pool.query('SELECT google_sub, expires_at FROM brief_sessions WHERE token_hash = $1', [hash(token)])).rows[0]; },
    async renew(token, expires) { await init(); await pool.query('UPDATE brief_sessions SET expires_at = $2 WHERE token_hash = $1', [hash(token), new Date(expires)]); },
    async logout(token) { await init(); await pool.query('DELETE FROM brief_sessions WHERE token_hash = $1', [hash(token)]); },
    async readDocument() { await init(); return (await pool.query('SELECT document FROM brief_document WHERE id = 1')).rows[0]?.document || null; },
    async writeDocument(document) { await init(); await pool.query('INSERT INTO brief_document (id, document) VALUES (1, $1) ON CONFLICT (id) DO UPDATE SET document = EXCLUDED.document', [JSON.stringify(document)]); },
    async importMaster(records) {
      await init();
      // Each record is an atomic idempotent upsert. Failed batches can be replayed
      // with a fresh signature; nothing is deleted or truncated.
      for (const r of records) await pool.query('INSERT INTO brief_social_master (id, record) VALUES ($1,$2) ON CONFLICT(id) DO UPDATE SET record=EXCLUDED.record', [r.id,JSON.stringify(r)]);
    },
    async readMaster(after = '') {
      await init();
      const rows = (await pool.query('SELECT record FROM brief_social_master WHERE id > $1 ORDER BY id LIMIT 51',[after])).rows.map(r=>r.record);
      return {rows:rows.slice(0,50),next:rows.length > 50 ? rows[49].id : null};
    },
    async masterRecord(id) { await init(); return (await pool.query('SELECT record FROM brief_social_master WHERE id=$1',[id])).rows[0]?.record || null; },
    async readImage() { await init(); return (await pool.query('SELECT mime, bytes FROM brief_image WHERE id = 1')).rows[0] || null; },
    async writeImage(mime, bytes) { await init(); await pool.query('INSERT INTO brief_image (id, mime, bytes) VALUES (1, $1, $2) ON CONFLICT (id) DO UPDATE SET mime = EXCLUDED.mime, bytes = EXCLUDED.bytes', [mime, bytes]); },
  };
}
module.exports = {createStore, hash};
