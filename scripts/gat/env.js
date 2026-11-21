// Great Again T one-page order form: local proofs only. Loads ~/.absbyai-secrets.env and maps the Stripe TEST keys onto
// the GAT_* names gat-checkout.js reads. Never prints a value. No key lives in this repo.
const fs = require('fs');
const raw = Object.fromEntries(fs.readFileSync(process.env.HOME + '/.absbyai-secrets.env', 'utf8').split('\n').filter(l => /^[A-Z0-9_]+=/.test(l)).map(l => { const i = l.indexOf('='); return [l.slice(0, i), l.slice(i + 1).replace(/^"|"$/g, '')]; }));
const env = {
  GAT_STRIPE_SECRET_KEY: raw.STRIPE_TEST_SECRET_KEY, GAT_STRIPE_PUBLISHABLE_KEY: raw.STRIPE_TEST_PUBLISHABLE_KEY,
  GAT_STRIPE_WEBHOOK_SECRET: raw.GAT_STRIPE_WEBHOOK_SECRET || '', GAT_SHOPIFY_SHOP: raw.GAT_SHOPIFY_SHOP, GAT_SHOPIFY_CLIENT_ID: raw.GAT_SHOPIFY_CLIENT_ID,
  GAT_SHOPIFY_CLIENT_SECRET: raw.GAT_SHOPIFY_CLIENT_SECRET, GAT_TEST_KEY: raw.GAT_TEST_KEY, GAT_LINK_SECRET: raw.GAT_LINK_SECRET,
  RESEND_API_KEY: raw.RESEND_API_KEY, GAT_RESEND_API_KEY: raw.GAT_RESEND_API_KEY || '', GAT_FROM: process.env.GAT_FROM || raw.GAT_FROM || '',
  RESET_FROM: 'Abs by AI <noreply@absbyai.com>', DATABASE_URL: raw.DATABASE_PUBLIC_URL || raw.DATABASE_URL,
  GAT_ALLOWED_ORIGINS: 'https://shop.sixpackabs.com,http://localhost:8787,http://127.0.0.1:8787',
};
for (const k of Object.keys(env)) if (!env[k]) delete env[k];
module.exports = { env, raw };
