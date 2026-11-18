// Local proof server: the built preview pages plus the real gat-checkout.js routes, in Stripe TEST mode.
// node scripts/gat/local-proof-server.js   then open http://localhost:8787/great-again-t-order.html?onepage=1
const path = require('path');
const ROOT = path.resolve(__dirname, '../..');
const { env } = require('./env.js');
process.env.DATABASE_URL = env.DATABASE_URL;
const { pool: db } = require(ROOT + '/db.js');
const express = require(ROOT + '/node_modules/express'), rateLimit = require(ROOT + '/node_modules/express-rate-limit');
const PORT = Number(process.env.PORT) || 8787;
const app = express();
app.use(require(ROOT + '/node_modules/cors')());
const gat = require(ROOT + '/gat-checkout.js').createGatCheckout({ db, dbReady: Promise.resolve(), express, rateLimit,
  env: Object.assign({}, env, { GAT_ALLOWED_ORIGINS: `https://shop.sixpackabs.com,http://localhost:${Number(process.env.PORT) || 8787},http://127.0.0.1:${Number(process.env.PORT) || 8787}`, GAT_FROM: 'SixPackAbs.com <orders@absbyai.com>' }) });
app.use(gat.router());
app.use(express.static(ROOT + '/Media/research/gat-sales-page-contest-20261117/refine/live-preview', { extensions: ['html'] }));
app.listen(PORT, () => console.log('GAT local proof server on http://localhost:' + PORT + ' (' + gat.mode + ' mode)'));
