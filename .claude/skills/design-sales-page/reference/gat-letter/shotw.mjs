// usage: node shot.mjs outPrefix url [maxHeight] [revealJS]
// writes outPrefix-fold.jpg (390x844) and outPrefix-full-N.jpg segments (4000 css px each), plus outPrefix.txt (page text) and outPrefix.json (meta)
import { spawn } from 'node:child_process';
import { writeFileSync, mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
const [out, url, hStr, reveal] = process.argv.slice(2);
const MAXH = parseInt(hStr || '24000');
const W=parseInt(process.env.W||'390'), VH=parseInt(process.env.VH||'844'), SC=parseFloat(process.env.SC||'2'), MOB=W<700;
const port = 9300 + Math.floor(Math.random() * 500);
const prof = mkdtempSync(join(tmpdir(), 'shotprof-'));
const chrome = spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  ['--headless=new', `--remote-debugging-port=${port}`, `--user-data-dir=${prof}`, '--no-first-run', '--mute-audio',
   '--autoplay-policy=user-gesture-required', `--window-size=${W},${VH}`, 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
let tabs;
for (let i = 0; i < 300; i++) { try { tabs = await (await fetch(`http://127.0.0.1:${port}/json`)).json(); if (tabs.length) break; } catch {} await sleep(200); }
const page = tabs.find(t => t.type === 'page');
const ws = new WebSocket(page.webSocketDebuggerUrl);
await new Promise(r => ws.onopen = r);
let id = 0; const pend = {};
ws.onmessage = e => { const m = JSON.parse(e.data); if (m.id && pend[m.id]) { pend[m.id](m); delete pend[m.id]; } };
const send = (method, params = {}) => new Promise(r => { const i = ++id; pend[i] = r; ws.send(JSON.stringify({ id: i, method, params })); });
const ev = async (expression, awaitPromise = false) => (await send('Runtime.evaluate', { expression, awaitPromise, returnByValue: true })).result?.result?.value;
await send('Emulation.setDeviceMetricsOverride', { width: W, height: VH, deviceScaleFactor: SC, mobile: MOB });
if (MOB) { await send('Emulation.setTouchEmulationEnabled', { enabled: true }); await send('Emulation.setUserAgentOverride', { userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1' }); }
await send('Page.enable');
await send('Page.navigate', { url });
await sleep(parseInt(process.env.WAIT||'4000'));
await ev(`[...document.querySelectorAll('button,a')].filter(b=>/^(ok|accept|i consent|accept all|got it|deny|i do not consent|reject all|decline)$/i.test((b.innerText||'').trim())).slice(0,1).forEach(b=>b.click())`);
await sleep(800);
if (process.env.KILLPOP) {
  await sleep(6000);
  const kill = `(()=>{[...document.querySelectorAll('button,a,span,div')].filter(b=>/^(no,? thank(s| you)?|no, i don.t feel lucky|continue|agree|accept|close|×|x)$/i.test((b.innerText||'').trim())&&b.children.length<2).slice(0,3).forEach(b=>{try{b.click()}catch(e){}});
  document.querySelectorAll('body *').forEach(e=>{const s=getComputedStyle(e);if(s.position==='fixed'){const r=e.getBoundingClientRect();const t=(e.innerText||'').toLowerCase();if((r.height>420&&r.width>250)||/cookie|privacy policy|% off|spin/.test(t.slice(0,400))&&r.height>90){e.remove()}}});
  document.querySelectorAll('[role=dialog],[aria-modal=true],dialog,[id*=onetrust],[id*=cookie],[class*=cookie],[id*=klaviyo],[class*=klaviyo],[class*=popup],[id*=popup],[class*=modal-backdrop]').forEach(e=>e.remove());document.querySelectorAll('body *').forEach(e=>{const s=getComputedStyle(e);const z=parseInt(s.zIndex)||0;if((s.position==='fixed'||s.position==='absolute')&&z>=100){const r=e.getBoundingClientRect();if(r.height>240&&r.width>250)e.remove()}});document.documentElement.style.overflow='auto';document.body.style.overflow='auto';document.body.style.position='static';})()`;
  await ev(kill); await sleep(1500); await ev(kill); await sleep(1200);
}
const shot = async (file, y, h) => { const r = await send('Page.captureScreenshot', { format: 'jpeg', quality: 78, captureBeyondViewport: true, clip: { x: 0, y, width: W, height: h, scale: 1 } }); writeFileSync(file, Buffer.from(r.result.data, 'base64')); };
await shot(`${out}-fold.jpg`, 0, VH);
if (process.env.SCROLL) { for (const [i,sel] of process.env.SCROLL.split('|').entries()) { const y = await ev(`(()=>{const e=document.querySelector(${JSON.stringify(sel)});const y=e.getBoundingClientRect().top+scrollY-140;window.scrollTo(0,y);return scrollY})()`); await sleep(900); const r = await send('Page.captureScreenshot', { format: 'jpeg', quality: 80 }); writeFileSync(`${out}-view${i}.jpg`, Buffer.from(r.result.data, 'base64')); } await ev('window.scrollTo(0,0)'); await sleep(500); }
if (reveal) { await ev(reveal, true); await sleep(2500); }
await ev(`(async()=>{for(let y=0;y<Math.min(document.documentElement.scrollHeight,${MAXH});y+=600){window.scrollTo(0,y);await new Promise(r=>setTimeout(r,180))}window.scrollTo(0,0);document.querySelectorAll('[data-aos],.aos-init,.elementor-invisible').forEach(e=>{e.style.opacity='1';e.style.transform='none';e.style.visibility='visible'});document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager')})()`, true);
await sleep(2500);
const H = Math.min(await ev('Math.max(document.documentElement.scrollHeight, document.body.scrollHeight)'), MAXH);
let n = 0;
for (let y = 0; y < H; y += 4000) { await shot(`${out}-full-${String(n).padStart(2,'0')}.jpg`, y, Math.min(4000, H - y)); n++; }
const text = await ev('document.body.innerText');
writeFileSync(`${out}.txt`, text || '');
const meta = await ev(`JSON.stringify({title:document.title,url:location.href,height:Math.max(document.documentElement.scrollHeight, document.body.scrollHeight),videos:[...document.querySelectorAll('video,iframe')].map(v=>({tag:v.tagName,src:(v.src||v.currentSrc||'').slice(0,200),w:v.getBoundingClientRect().width,h:v.getBoundingClientRect().height,top:v.getBoundingClientRect().top+scrollY})).slice(0,12),fixed:[...document.querySelectorAll('*')].filter(e=>{const s=getComputedStyle(e);return (s.position==='fixed'||s.position==='sticky')&&e.getBoundingClientRect().height>20&&e.getBoundingClientRect().width>200}).map(e=>({tag:e.tagName,cls:(e.className+'').slice(0,80),pos:getComputedStyle(e).position,top:e.getBoundingClientRect().top,h:e.getBoundingClientRect().height,text:(e.innerText||'').slice(0,100)})).slice(0,10)})`);
writeFileSync(`${out}.json`, meta || '{}');
ws.close(); chrome.kill('SIGKILL');
console.log('ok', out, H, n);
