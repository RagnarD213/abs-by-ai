// Great Again T one-page order form: a real browser run against the LOCAL proof server (Stripe TEST mode only).
//   node scripts/gat/local-proof-server.js            (or the "gat-order-form-test" preview)
//   node scripts/gat/browser-proof.mjs <outDir> [baseUrl]
// Drives headless Chrome at phone, tablet and desktop sizes: field checks, a declined test card, a retry on the same
// order with a good test card, the thank-you page, then the account page (skip a month, cancel). Saves screenshots.
// Uses only Stripe's published test card numbers, on localhost. Never point it at the live shop.
import { spawn } from 'node:child_process';
import { writeFileSync, mkdtempSync, mkdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const [outDir, base = 'http://localhost:8787'] = process.argv.slice(2);
if (!outDir) { console.error('usage: browser-proof.mjs <outDir> [baseUrl]'); process.exit(2); }
const mode = process.env.GAT_PROOF || 'orders';
// Orders and account actions are typed only into the local proof server. GAT_PROOF=look just opens pages and takes pictures.
if (mode !== 'look' && !/^http:\/\/(localhost|127\.0\.0\.1):\d+$/.test(base)) { console.error('local proof server only'); process.exit(2); }
mkdirSync(outDir, { recursive: true });
const sleep = ms => new Promise(r => setTimeout(r, ms));
const SIZES = { phone: { w: 390, h: 844, mobile: true, dsf: 2 }, tablet: { w: 768, h: 1024, mobile: true, dsf: 1 }, desktop: { w: 1440, h: 900, mobile: false, dsf: 1 } };
const GOOD = '4242424242424242', DECLINED = '4000000000000002';

async function browser(size) {
  const port = 9300 + Math.floor(Math.random() * 500);
  const chrome = spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', ['--headless=new', `--remote-debugging-port=${port}`,
    `--user-data-dir=${mkdtempSync(join(tmpdir(), 'gatproof-'))}`, '--no-first-run', '--mute-audio', `--window-size=${size.w},${size.h}`, 'about:blank'], { stdio: 'ignore' });
  let tabs; for (let i = 0; i < 300; i++) { try { tabs = await (await fetch(`http://127.0.0.1:${port}/json`)).json(); if (tabs.length) break; } catch {} await sleep(200); }
  const ws = new WebSocket(tabs.find(t => t.type === 'page').webSocketDebuggerUrl);
  await new Promise(r => ws.onopen = r);
  let id = 0; const pend = {};
  ws.onmessage = e => { const m = JSON.parse(e.data); if (m.id && pend[m.id]) { pend[m.id](m); delete pend[m.id]; } };
  const send = (method, params = {}) => new Promise(r => { const i = ++id; pend[i] = r; ws.send(JSON.stringify({ id: i, method, params })); });
  const ev = async expression => { const r = await send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true }); if (r.result?.exceptionDetails) throw new Error(r.result.exceptionDetails.exception?.description || 'eval failed'); return r.result?.result?.value; };
  await send('Emulation.setDeviceMetricsOverride', { width: size.w, height: size.h, deviceScaleFactor: size.dsf, mobile: size.mobile });
  if (size.mobile) await send('Emulation.setUserAgentOverride', { userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1' });
  await send('Page.enable');
  const go = async url => { await send('Page.navigate', { url }); await sleep(900); };
  const waitFor = async (expr, ms = 30000, what = expr) => { const t = Date.now(); for (;;) { if (await ev(expr).catch(() => false)) return; if (Date.now() - t > ms) throw new Error('timed out waiting for ' + what); await sleep(300); } };
  const shot = async (name, full = true) => {
    // a full-length picture is taken with the sticky header and sticky column laid flat, or they print mid-page
    if (full) await ev(`(() => { const s = document.createElement('style'); s.id = 'proof-flat'; s.textContent = '.site-top,.co-left{position:static!important}html{scroll-behavior:auto!important}'; document.head.appendChild(s); scrollTo(0, 0); })()`);
    if (full) await sleep(250);
    const h = full ? await ev('Math.ceil(document.documentElement.scrollHeight)') : size.h;
    const r = await send('Page.captureScreenshot', { format: 'jpeg', quality: 82, captureBeyondViewport: full, clip: { x: 0, y: full ? 0 : await ev('scrollY'), width: size.w, height: Math.min(h, 12000), scale: 1 } });
    writeFileSync(join(outDir, name + '.jpg'), Buffer.from(r.result.data, 'base64'));
    if (full) await ev(`(() => { const s = document.getElementById('proof-flat'); if (s) s.remove(); })()`);
  };
  const click = async sel => {
    await ev(`document.querySelector(${JSON.stringify(sel)}).scrollIntoView({block:'center',behavior:'instant'})`); await sleep(250);
    const r = JSON.parse(await ev(`JSON.stringify(document.querySelector(${JSON.stringify(sel)}).getBoundingClientRect())`));
    const x = r.x + Math.min(r.width / 2, 90), y = r.y + r.height / 2;
    for (const type of ['mousePressed', 'mouseReleased']) await send('Input.dispatchMouseEvent', { type, x, y, button: 'left', clickCount: 1 });
    await sleep(250);
  };
  const type = async text => { for (const ch of text) { await send('Input.dispatchKeyEvent', { type: 'keyDown', text: ch, key: ch }); await send('Input.dispatchKeyEvent', { type: 'keyUp', key: ch }); await sleep(25); } };
  const clear = async () => {
    await send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'a', code: 'KeyA', modifiers: 4, commands: ['selectAll'] });
    await send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'a', code: 'KeyA', modifiers: 4 });
    await send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Backspace', code: 'Backspace', windowsVirtualKeyCode: 8 });
    await send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Backspace', code: 'Backspace', windowsVirtualKeyCode: 8 });
    await sleep(150);
  };
  return { send, ev, go, waitFor, shot, click, type, clear, close: () => { ws.close(); chrome.kill('SIGKILL'); } };
}

const setFields = who => `(() => { const set = (id, v) => { const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event('input', { bubbles: true })); e.dispatchEvent(new Event('change', { bubbles: true })); };
  const w = ${JSON.stringify(who)}; for (const k in w) set(k, w[k]); return true; })()`;
const card = async (b, number, first) => {
  await b.click('#op-card-number'); if (!first) await b.clear(); await b.type(number);
  await b.click('#op-card-exp'); if (!first) await b.clear(); await b.type('1230');
  await b.click('#op-card-cvc'); if (!first) await b.clear(); await b.type('123');
};
const text = (b, sel) => b.ev(`(document.querySelector(${JSON.stringify(sel)}) || {}).textContent || ''`);

async function run(sizeName, option, opts = {}) {
  const b = await browser(SIZES[sizeName]);
  const tag = `${sizeName}-${option}`;
  const out = { size: sizeName, option };
  try {
    await b.go(`${base}/great-again-t-order.html?onepage=1${option === 'single' ? '&option=single' : ''}`);
    await b.waitFor(`document.querySelectorAll('.stripe iframe').length >= 3`, 30000, 'Stripe card fields');
    await sleep(1500);
    out.sideScroll = await b.ev('document.documentElement.scrollWidth > innerWidth');
    await b.shot(`${tag}-1-form`);
    // an empty form is refused, field by field
    await b.click('#op-pay'); await sleep(400);
    out.emptyError = await text(b, '#co-err');
    await b.ev(setFields({ 'op-first': 'Paige', 'op-last': sizeName[0].toUpperCase() + sizeName.slice(1), 'op-email': 'delivered@resend.dev', 'op-phone': '512-555-0102',
      'op-addr1': '300 Browser Way', 'op-addr2': opts.apt || '', 'op-city': 'Round Rock', 'op-state': 'TX', 'op-zip': '78664' }));
    if (opts.billing) {
      await b.click('#op-billdiff + .box');
      await b.ev(setFields({ 'op-b-addr1': '9 Billing Blvd', 'op-b-city': 'Austin', 'op-b-state': 'TX', 'op-b-zip': '78701' }));
    }
    if (opts.decline) {
      await card(b, DECLINED, true);
      if (option === 'trial') {
        await b.click('#op-pay'); await sleep(400);
        out.noTickError = await text(b, '#co-err');          // the free month needs the box ticked
        await b.click('#agree + .box');
      }
      await b.click('#op-pay');
      await b.waitFor(`!document.getElementById('co-err').hidden && !document.getElementById('op-pay').disabled`, 40000, 'decline message');
      out.declineError = await text(b, '#co-err');
      await b.ev(`document.getElementById('co-err').scrollIntoView({block:'center',behavior:'instant'})`); await sleep(200);
      await b.shot(`${tag}-2-declined`, false);
      await card(b, GOOD, false);
    } else {
      await card(b, GOOD, true);
      if (option === 'trial') await b.click('#agree + .box');
    }
    await b.shot(`${tag}-3-filled`);
    await b.click('#op-pay');
    await b.waitFor(`/great-again-t-thank-you/.test(location.pathname)`, 60000, 'the thank-you page');
    out.orderId = await b.ev(`new URLSearchParams(location.search).get('o')`);
    await b.waitFor(`!document.getElementById('ty-done').hidden || !document.getElementById('ty-miss').hidden`, 60000, 'order confirmation');
    await sleep(1200);
    out.title = await text(b, '#ty-title'); out.orderName = await text(b, '#ty-order'); out.firstCharge = await text(b, '#ty-first');
    await b.shot(`${tag}-4-thank-you`);
    // a reload must not report the sale a second time
    out.trackedAgain = await b.ev(`fetch('/api/gat/order/${out.orderId}/tracked', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: '{}' }).then(r => r.json()).then(j => j.first)`);
  } catch (e) { out.error = e.message; await b.shot(`${tag}-ERROR`).catch(() => {}); }
  b.close();
  return out;
}

async function account(sizeName, link, label) {
  const b = await browser(SIZES[sizeName]);
  const out = { size: sizeName, account: label };
  try {
    await b.go(link.replace('https://shop.sixpackabs.com/pages/great-again-t-account', base + '/great-again-t-account.html'));
    await b.waitFor(`document.getElementById('ac-wait').hidden`, 30000, 'account page'); await sleep(500);
    out.shows = await b.ev(`['ac-on','ac-off','ac-single','ac-miss'].filter(i => !document.getElementById(i).hidden).join(',')`);
    out.next = await text(b, '#ac-next');
    await b.shot(`${sizeName}-account-${label}-1`);
    if (out.shows === 'ac-on') {
      await b.click('#ac-skip'); await b.waitFor(`!document.getElementById('ac-ok').hidden`, 30000, 'skip'); out.afterSkip = await text(b, '#ac-ok'); out.nextAfterSkip = await text(b, '#ac-next');
      await b.shot(`${sizeName}-account-${label}-2-skipped`);
      await b.click('#ac-cancel'); await sleep(300); await b.shot(`${sizeName}-account-${label}-3-confirm`);
      await b.click('#ac-yes'); await b.waitFor(`!document.getElementById('ac-off').hidden`, 30000, 'cancel');
      out.afterCancel = await b.ev(`['ac-on','ac-off'].filter(i => !document.getElementById(i).hidden).join(',')`);
      await b.shot(`${sizeName}-account-${label}-4-cancelled`);
    }
  } catch (e) { out.error = e.message; await b.shot(`${sizeName}-account-${label}-ERROR`).catch(() => {}); }
  b.close();
  return out;
}

if (mode === 'look') {
  // GAT_PROOF=look  node browser-proof.mjs <outDir> https://shop.sixpackabs.com/pages   : no typing, no orders
  const results = [];
  for (const sizeName of ['phone', 'tablet', 'desktop']) {
    for (const [label, path, wait] of [['onepage', '/great-again-t-order?onepage=1', `document.querySelectorAll('.stripe iframe').length >= 3`], ['classic', '/great-again-t-order', `document.getElementById('co-go') !== null`]]) {
      const b = await browser(SIZES[sizeName]);
      const out = { size: sizeName, page: label };
      try {
        await b.go(base + path); await b.waitFor(wait, 30000, label); await sleep(1500);
        Object.assign(out, JSON.parse(await b.ev(`JSON.stringify({ op: document.body.classList.contains('op'), testBar: !!document.querySelector('.op-test'), cardFields: document.querySelectorAll('.stripe iframe').length,
          payShown: getComputedStyle(document.getElementById('op-pay')).display !== 'none', classicShown: getComputedStyle(document.getElementById('co-go')).display !== 'none',
          shippingShown: document.getElementById('op-first').offsetParent !== null, error: document.getElementById('co-err').hidden ? '' : document.getElementById('co-err').textContent,
          sideScroll: document.documentElement.scrollWidth > innerWidth, noindex: !!document.querySelector('meta[name=robots][content*=noindex]') })`)));
        await b.shot(`live-${sizeName}-${label}`);
      } catch (e) { out.error = e.message; }
      b.close(); results.push(out);
    }
  }
  console.log(JSON.stringify(results));
} else if (mode === 'orders') {
  const results = [];
  results.push(await run('phone', 'trial', { decline: true }));
  results.push(await run('tablet', 'single', { decline: true, apt: 'Unit 4' }));
  results.push(await run('desktop', 'trial', { billing: true }));
  results.push(await run('phone', 'single'));
  console.log(JSON.stringify(results, null, 1));
} else {
  // GAT_PROOF=account  GAT_LINKS='[["trial","https://...account?o=..&k=.."],["single","..."]]'
  const results = [];
  for (const [label, link] of JSON.parse(process.env.GAT_LINKS || '[]')) results.push(await account(label === 'trial' ? 'phone' : 'desktop', link, label));
  results.push(await account('phone', base + '/great-again-t-account.html?o=000000000000000000000000&k=00000000000000000000000000000000', 'bad-link'));
  console.log(JSON.stringify(results, null, 1));
}
