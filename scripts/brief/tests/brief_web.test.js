'use strict';
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const express = require('express');
const {newDb} = require('pg-mem');
const {OAuth2Client} = require('google-auth-library');
const {createStore, hash} = require('../web/store');
const {validate} = require('../web/document');
const {createRouter, COOKIE, AGE, googleVerifier} = require('../web/router');
const {signedHeaders} = require('../web/publication');
const publishingKeys = crypto.generateKeyPairSync('ed25519');
const env = {BRIEF_OWNER_EMAIL:'fixture-owner@gmail.com', BRIEF_GOOGLE_CLIENT_ID:'123-fixture.apps.googleusercontent.com', BRIEF_PUBLISH_PUBLIC_KEY:publishingKeys.publicKey.export({type:'spki',format:'der'}).toString('base64')};
const clock = Date.now();
const claims = {aud:env.BRIEF_GOOGLE_CLIENT_ID, iss:'https://accounts.google.com', exp:Math.floor(clock/1000)+1800, iat:Math.floor(clock/1000), email:env.BRIEF_OWNER_EMAIL, email_verified:true, sub:'fixture-owner-sub'};
const sample = {schemaVersion:1, generatedAt:new Date(clock).toISOString(), forDate:'2026-09-30', editionType:'retrospective', timezone:'America/Chicago', routineEnabled:false,
  focus:{status:'missing', task:'Synthetic launch review', why:'Synthetic example only.', source:'Fixture'}, yesterday:[], opportunities:[], sources:[{name:'Trello',status:'missing'}]};
async function main() {
  // pg-mem flags constraints on repeated CREATE IF NOT EXISTS as unconsumed AST.
  // Retain production constraints; this option only disables that emulator check.
  const pg = newDb({noAstCoverageCheck:true}).adapters.createPg(), pool = new pg.Pool(), store = createStore(pool);
  let payload = {...claims};
  const app = express();
  app.use('/unconfigured',createRouter({store,env:{}}));
  app.use(createRouter({store, env, verifyToken:async () => payload, now:() => clock}));
  app.use((req,res) => res.status(418).send('Existing product route'));
  const server = app.listen(0,'127.0.0.1');
  await new Promise(resolve => server.once('listening',resolve));
  const base = 'http://127.0.0.1:' + server.address().port;
  const request = (route, options = {}) => fetch(base + route,{redirect:'manual',...options});
  async function login(csrf = 'fixture-csrf') {
    return request('/api/brief/auth/google',{method:'POST',headers:{cookie:'g_csrf_token=fixture-csrf','Content-Type':'application/x-www-form-urlencoded'},body:new URLSearchParams({g_csrf_token:csrf,credential:'synthetic-token'})});
  }
  try {
    assert.equal((await request('/unconfigured/api/brief/data')).status,503);
    assert.equal((await request('/unconfigured/morningbrief')).status,503);
    for (const route of ['/morningbrief','/MORNINGBRIEF/','/morningbrief.html','/brief-publish']) assert.equal((await request(route)).status,303);
    for (const route of ['/api/brief/data','/API/BRIEF/IMAGE/','/api/brief/page.js','/api/brief/style.css','/api/brief/publish.js']) assert.equal((await request(route)).status,401);
    assert.equal((await request('/product-fixture')).status,418);
    assert.equal((await request('/api/brief/data',{headers:{'X-Dash-Key':'synthetic-legacy-password',cookie:'absbyai_dash=legacy-cookie'}})).status,401);
    assert.equal((await login('wrong-csrf')).status,403);
    for (const change of [{email:'other@gmail.com'}, {email_verified:false}, {aud:'wrong-client'}, {iss:'other'}, {exp:0}, {iat:Math.floor(clock/1000)+600}, {sub:''}]) {
      payload = {...claims,...change}; assert.equal((await login()).status,403);
    }
    assert.equal(await store.owner(),undefined);
    payload = {...claims};
    const response = await login(); assert.equal(response.status,303);
    const rawCookie = response.headers.get('set-cookie');
    assert.match(rawCookie,/HttpOnly; Secure; SameSite=Lax/); assert.match(rawCookie,/Max-Age=7776000/);
    const sessionCookie = rawCookie.split(';')[0], token = sessionCookie.split('=')[1];
    assert.equal(token.length,64);
    const rows = await pool.query('SELECT * FROM brief_sessions'); assert.equal(rows.rows[0].token_hash,hash(token)); assert(!JSON.stringify(rows.rows).includes(token));
    assert.equal((await request('/morningbrief',{headers:{cookie:sessionCookie}})).status,200);
    await store.addSession('c'.repeat(64),'another-account-sub',clock+AGE);
    for (const route of ['/api/brief/data','/api/brief/image','/morningbrief']) {
      assert.equal((await request(route,{headers:{cookie:COOKIE+'='+'c'.repeat(64)}})).status,route === '/morningbrief' ? 303 : 401);
    }
    // Sessions persist across a fresh router/store instance, as after a server restart.
    const freshStore = createStore(pool); assert.equal((await freshStore.session(token)).google_sub,claims.sub);
    assert.equal((await request('/api/brief/data',{headers:{cookie:sessionCookie}})).status,404);
    assert.equal((await request('/api/brief/publish',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(sample)})).status,401);
    const signedBody = JSON.stringify({...sample,rawTranscript:'must be dropped'});
    const published = await request('/api/brief/publish',{method:'POST',headers:{'Content-Type':'application/json',...signedHeaders(Buffer.from(signedBody),publishingKeys.privateKey,clock)},body:signedBody});
    assert.equal(published.status,200);
    const data = await request('/api/brief/data',{headers:{cookie:sessionCookie}});
    assert.match(data.headers.get('cache-control'),/no-store/); assert(!data.headers.has('access-control-allow-origin'));
    const edition = await data.json(); assert.equal(edition.routineEnabled,false); assert(!('rawTranscript' in edition));
    // The owner can perform the first proof without any automation ingest key.
    delete env.BRIEF_PUBLISH_PUBLIC_KEY;
    const browserPublish = headers => request('/api/brief/publish',{method:'POST',headers:{'Content-Type':'application/json','X-Brief-Action':'publish',origin:'https://absbyai.com',...headers},body:JSON.stringify(sample)});
    assert.equal((await browserPublish({})).status,401);
    assert.equal((await browserPublish({cookie:COOKIE+'='+'c'.repeat(64)})).status,401);
    assert.equal((await browserPublish({cookie:sessionCookie,origin:'https://other.example.com'})).status,503);
    assert.equal((await browserPublish({cookie:sessionCookie})).status,200);
    assert.equal((await request('/brief-publish',{headers:{cookie:sessionCookie}})).status,200);
    assert.equal((await request('/api/brief/publish.js',{headers:{cookie:sessionCookie}})).status,200);
    await store.writeImage('image/png',Buffer.from('synthetic-private-image'));
    assert.equal((await request('/api/brief/image')).status,401);
    assert.equal(await (await request('/api/brief/image',{headers:{cookie:sessionCookie}})).text(),'synthetic-private-image');
    payload = {...claims,sub:'different-sub-same-email'}; assert.equal((await login()).status,403);
    const altered = sessionCookie.slice(0,-1)+(token.endsWith('a')?'b':'a'); assert.equal((await request('/api/brief/data',{headers:{cookie:altered}})).status,401);
    assert.equal((await request('/api/brief/data',{headers:{cookie:COOKIE+'=%ZZ'}})).status,401);
    assert.equal((await request('/api/brief/data',{headers:{cookie:sessionCookie+'; '+sessionCookie}})).status,401);
    await store.renew(token,clock+86400000);
    const renewed = await request('/api/brief/data',{headers:{cookie:sessionCookie}}); assert.match(renewed.headers.get('set-cookie'),/Max-Age=7776000/);
    await store.renew(token,clock-1); assert.equal((await request('/api/brief/data',{headers:{cookie:sessionCookie}})).status,401);
    await store.renew(token,clock+AGE);
    assert.equal((await request('/api/brief/logout',{method:'POST',headers:{cookie:sessionCookie}})).status,403);
    assert.equal((await request('/api/brief/logout',{method:'POST',headers:{cookie:sessionCookie,origin:'https://absbyai.com','X-Brief-Action':'logout'}})).status,200);
    assert.equal((await request('/api/brief/data',{headers:{cookie:sessionCookie}})).status,401);
    const pinned = await store.owner(); assert.equal(pinned.google_sub,claims.sub);
    const invalid = [true,null];
    for (const routineEnabled of invalid) assert.throws(() => validate({...sample,routineEnabled},clock));
    assert.throws(() => validate({...sample,focus:{...sample.focus,status:'current',statedAt:new Date(clock-40*3600000).toISOString(),applicableDate:sample.forDate}},clock));
    assert.throws(() => validate({...sample,opportunities:[{title:'Bad link',detail:'Example',source:'Fixture',url:'javascript:alert(1)'}]},clock));
    const queue = {status:'partial',checkedAt:new Date(clock).toISOString(),windowFrom:new Date(clock).toISOString(),windowTo:new Date(clock+7*86400000).toISOString(),sourceCoverage:{blotato:'ok',youtubeStudio:'unverified'},rows:[{id:'fixture',platform:'YouTube',account:'Synthetic',scheduledAt:new Date(clock+86400000).toISOString(),title:'Example release',preflight:{cover:'missing',description:'unverified',links:'verified',duplicates:'not_applicable',assetMatch:'unverified'}}]};
    assert.equal(validate({...sample,socialReleaseQueue:queue},clock).socialReleaseQueue.rows[0].preflight.description,'unverified');
    assert.throws(() => validate({...sample,socialReleaseQueue:{...queue,windowTo:new Date(clock+8*86400000).toISOString()}},clock));
    assert.throws(() => validate({...sample,socialReleaseQueue:{...queue,rows:[{...queue.rows[0],preflight:{...queue.rows[0].preflight,cover:'unknown'}}]}},clock));
    // Exercise the same official verifier used in production, with synthetic keys.
    const keys = crypto.generateKeyPairSync('rsa',{modulusLength:2048});
    const client = new OAuth2Client();
    client.getFederatedSignonCertsAsync = async () => ({certs:{fixture:keys.publicKey.export({type:'spki',format:'pem'})},format:'PEM'});
    const encode = v => Buffer.from(JSON.stringify(v)).toString('base64url');
    const sign = p => { const message = encode({alg:'RS256',kid:'fixture'})+'.'+encode(p); return message+'.'+crypto.sign('RSA-SHA256',Buffer.from(message),keys.privateKey).toString('base64url'); };
    const verify = googleVerifier(client);
    assert.equal((await verify(sign(claims),env.BRIEF_GOOGLE_CLIENT_ID)).sub,claims.sub);
    await assert.rejects(() => verify(sign({...claims,aud:'wrong'}),env.BRIEF_GOOGLE_CLIENT_ID));
    await assert.rejects(() => verify(sign({...claims,iss:'wrong'}),env.BRIEF_GOOGLE_CLIENT_ID));
    await assert.rejects(() => verify(sign({...claims,iat:Math.floor(clock/1000)-4000,exp:Math.floor(clock/1000)-1000}),env.BRIEF_GOOGLE_CLIENT_ID));
    const good = sign(claims), pieces = good.split('.'); pieces[1]=encode({...claims,email:'other@gmail.com'});
    await assert.rejects(() => verify(pieces.join('.'),env.BRIEF_GOOGLE_CLIENT_ID));
    console.log('brief_web: owner pin, official signature/audience/issuer/expiry verification, CSRF, page/data/image denial, persistent hashed sessions, renewal/logout, private publication and queue schema passed');
  } finally { await new Promise(resolve => server.close(resolve)); await pool.end(); }
}
main().catch(error => { console.error(error); process.exitCode=1; });
