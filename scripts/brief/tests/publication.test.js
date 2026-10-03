'use strict';
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const {spawnSync} = require('node:child_process');
const express = require('express');
const {newDb} = require('pg-mem');
const {createStore} = require('../web/store');
const {createRouter} = require('../web/router');
const {PATH,IMAGE_PATH,signedHeaders,canonical,keyId,verifyRequest,digest} = require('../web/publication');
async function main() {
  const keys = crypto.generateKeyPairSync('ed25519'), other = crypto.generateKeyPairSync('ed25519');
  const env = {BRIEF_PUBLISH_PUBLIC_KEY:keys.publicKey.export({type:'spki',format:'der'}).toString('base64')};
  const clock = Date.now(), sample = {schemaVersion:1,generatedAt:new Date(clock).toISOString(),forDate:'2026-10-03',editionType:'manual',timezone:'America/Chicago',routineEnabled:false,
    focus:{status:'missing',task:'Synthetic fixture',why:'Synthetic test.',source:'Fixture'},sources:[]};
  const body = Buffer.from(JSON.stringify(sample,null,2));
  const pg = newDb({noAstCoverageCheck:true}).adapters.createPg(), pool = new pg.Pool(), store = createStore(pool);
  let storedImage;
  const query = pool.query.bind(pool);
  pool.query = (sql,params) => {
    if (typeof sql === 'string' && sql.startsWith('INSERT INTO brief_image')) storedImage=Buffer.from(params[1]);
    return query(sql,params);
  };
  const app = express(), productJson = express.json({limit:'100mb'});
  // Match production parser ordering; never reserialize JSON before verifying.
  app.use((req,res,next) => /^\/api\/brief\/(?:publish|image\/publish)\/?$/i.test(req.path) ? next() : productJson(req,res,next));
  app.use(createRouter({store,env,now:() => clock}));
  const server = app.listen(0,'127.0.0.1');
  await new Promise(resolve => server.once('listening',resolve));
  const base = 'http://127.0.0.1:'+server.address().port;
  const send = (headers=signedHeaders(body,keys.privateKey,clock),data=body,route=PATH) => fetch(base+route,{method:'POST',headers:{'Content-Type':'application/json',...headers},body:data});
  try {
    assert.equal((await send()).status,200);
    const saved = await store.readDocument(); assert.equal(saved.forDate,sample.forDate);
    const replay = signedHeaders(body,keys.privateKey,clock);
    assert.equal((await send(replay)).status,200);
    assert.equal((await send(replay)).status,401);
    const freshStore = createStore(pool);
    assert.equal(await freshStore.claimPublicationNonce(replay['X-Brief-Key-Id'],replay['X-Brief-Nonce'],clock+330000,clock),false);
    const nonce = 'e'.repeat(32), results = await Promise.all(Array.from({length:8},()=>freshStore.claimPublicationNonce(keyId(keys.publicKey),nonce,clock+330000,clock)));
    assert.equal(results.filter(Boolean).length,1);
    assert.equal((await send(signedHeaders(body,other.privateKey,clock))).status,401);
    assert.equal((await send(signedHeaders(body,keys.privateKey,clock-301000))).status,401);
    assert.equal((await send(signedHeaders(body,keys.privateKey,clock+31000))).status,401);
    assert.equal((await send(signedHeaders(body,keys.privateKey,clock),Buffer.from(JSON.stringify({...sample,focus:{...sample.focus,task:'Tampered'}})))).status,401);
    const badSignature = signedHeaders(body,keys.privateKey,clock); badSignature['X-Brief-Signature']=Buffer.alloc(64).toString('base64');
    assert.equal((await send(badSignature)).status,401);
    for (const route of [PATH+'?x=1',PATH+'/',PATH.toUpperCase()]) assert.equal((await send(undefined,body,route)).status,401);
    const signed = signedHeaders(body,keys.privateKey,clock), low = Object.fromEntries(Object.entries(signed).map(([k,v])=>[k.toLowerCase(),v]));
    assert.throws(()=>verifyRequest({method:'GET',originalUrl:PATH,briefRawBody:body,headers:{'content-type':'application/json',...low}},keys.publicKey,clock));
    assert.throws(()=>verifyRequest({method:'POST',originalUrl:'/api/other',briefRawBody:body,headers:{'content-type':'application/json',...low}},keys.publicKey,clock));
    assert.equal((await fetch(base+'/api/brief/data',{headers:signed})).status,503); // Publication key has no read identity.
    assert.deepEqual(await store.readDocument(),saved);
    const huge = Buffer.from(JSON.stringify({...sample,oversize:'a'.repeat(525000)}));
    assert.equal((await send(signedHeaders(huge,keys.privateKey,clock),huge)).status,413);
    const image = Buffer.alloc(45); Buffer.from([137,80,78,71,13,10,26,10]).copy(image); image.write('IHDR',12); image.writeUInt32BE(1,16); image.writeUInt32BE(1,20); image.write('IEND',37);
    const imageHeaders = signedHeaders(image,keys.privateKey,clock,undefined,IMAGE_PATH);
    const sendImage = (headers=imageHeaders,bytes=image,mime='image/png') => fetch(base+IMAGE_PATH,{method:'POST',headers:{'Content-Type':mime,...headers},body:bytes});
    const imageResponse = await sendImage(); assert.equal(imageResponse.status,200); assert.equal((await imageResponse.json()).sha256,digest(image));
    assert.equal((await sendImage()).status,401);
    assert.equal((await sendImage(signedHeaders(image,keys.privateKey,clock))).status,401); // Cross-route signature forbidden.
    const brokenImage = Buffer.from('not an image');
    assert.equal((await sendImage(signedHeaders(brokenImage,keys.privateKey,clock,undefined,IMAGE_PATH),brokenImage)).status,400);
    assert.equal((await sendImage(signedHeaders(image,keys.privateKey,clock,undefined,IMAGE_PATH),image,'image/jpeg')).status,400);
    // pg-mem corrupts non-UTF8 bytea parameters. Check exact bytes at the PG
    // boundary; production owner readback is a separate required proof.
    assert(storedImage.equals(image));
    const failing = express(); failing.use(createRouter({env,store:{claimPublicationNonce:async()=>{throw new Error('Synthetic DB failure');}},now:()=>clock}));
    const failedServer = failing.listen(0,'127.0.0.1'); await new Promise(r=>failedServer.once('listening',r));
    try { assert.equal((await fetch('http://127.0.0.1:'+failedServer.address().port+PATH,{method:'POST',headers:{'Content-Type':'application/json',...signedHeaders(body,keys.privateKey,clock)},body})).status,503); }
    finally { await new Promise(r=>failedServer.close(r)); }
    const dir = fs.mkdtempSync(path.join(fs.realpathSync(os.tmpdir()),'brief-key-test-')); fs.chmodSync(dir,0o700);
    const file = path.join(dir,'key.pem'), signer = path.resolve(__dirname,'../mac_signer.js');
    const run = (action,input) => spawnSync(process.execPath,[signer,action,file],{input,encoding:'utf8'});
    try {
      const created = run('--create-key'); assert.equal(created.status,0);
      const config = JSON.parse(created.stdout); assert.deepEqual(Object.keys(config),['BRIEF_PUBLISH_PUBLIC_KEY']);
      assert(!created.stdout.includes('PRIVATE')); assert.equal(fs.statSync(file).mode&0o777,0o600);
      assert.notEqual(run('--create-key').status,0); // Never overwrite an existing key.
      const result = run('--sign',body); assert.equal(result.status,0); assert(!result.stdout.includes('PRIVATE'));
      const h = JSON.parse(result.stdout), localPub = crypto.createPublicKey({key:Buffer.from(config.BRIEF_PUBLISH_PUBLIC_KEY,'base64'),type:'spki',format:'der'});
      assert(crypto.verify(null,canonical(body,h['X-Brief-Timestamp'],h['X-Brief-Nonce'],h['X-Brief-Key-Id']),localPub,Buffer.from(h['X-Brief-Signature'],'base64')));
      fs.chmodSync(file,0o644); assert.notEqual(run('--sign',body).status,0);
      fs.chmodSync(file,0o600); fs.renameSync(file,file+'.real'); fs.symlinkSync(file+'.real',file); assert.notEqual(run('--sign',body).status,0);
    } finally { fs.rmSync(dir,{recursive:true,force:true}); }
    console.log('publication: exact-byte binding, wrong key/body/path/method, expiry/future, replay across stores, atomic nonce race, DB failure, limits and local key privacy passed');
  } finally { await new Promise(resolve=>server.close(resolve)); await pool.end(); }
}
main().catch(error=>{console.error(error);process.exitCode=1;});
