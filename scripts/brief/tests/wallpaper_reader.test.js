'use strict';
const assert=require('node:assert/strict'),crypto=require('crypto'),express=require('express');
const {newDb}=require('pg-mem'),{createStore}=require('../web/store'),{createRouter}=require('../web/router');
const {canonical}=require('../web/wallpaper-reader'),{keyId}=require('../web/publication');
const {wallpaperStatus}=require('../web/favorites'),{choose,INTERVAL}=require('../wallpaper/rotation');
(async()=>{
 for(let count=1;count<=8;count++){
  const ids=Array.from({length:count},(_,i)=>String(i));let previous={};
  for(let cycle=0;cycle<80;cycle++){
   const now=cycle*INTERVAL,plan=choose(ids,['1','2','3'],previous,now);assert.equal(plan.length,3);
   assert.equal(new Set(plan.map(p=>p.sha256)).size,Math.min(3,count));
   if(count>1)for(const p of plan)assert.notEqual(p.sha256,previous[p.id]?.sha256);
   for(const p of plan)previous[p.id]=p;
   assert.deepEqual(choose(ids,['1','2','3'],previous,now+1),[]);
  }
 }
 const independent={a:{sha256:'0',nextChangeAt:100},b:{sha256:'1',nextChangeAt:200},c:{sha256:'2',nextChangeAt:300}};
 assert.deepEqual(choose(['0','1','2','3'],['a','b','c'],independent,150).map(d=>d.id),['a']);
 assert.deepEqual(choose([],['a','b','c'],independent,999),[]);
 const pg=newDb({noAstCoverageCheck:true}).adapters.createPg(),pool=new pg.Pool(),store=createStore(pool),now=Date.now();
 const pair=crypto.generateKeyPairSync('ed25519'),other=crypto.generateKeyPairSync('ed25519');
 const env={BRIEF_OWNER_EMAIL:'synthetic@gmail.com',BRIEF_GOOGLE_CLIENT_ID:'123456-test.apps.googleusercontent.com',BRIEF_WALLPAPER_PUBLIC_KEY:pair.publicKey.export({type:'spki',format:'der'}).toString('base64')};
 const app=express();app.use(createRouter({store,env,now:()=>now}));const server=app.listen(0,'127.0.0.1');await new Promise(r=>server.once('listening',r));
 const base='http://127.0.0.1:'+server.address().port,prefix='/api/brief/wallpaper';
 function headers(route,method='GET',body=Buffer.alloc(0),key=pair.privateKey,time=now){
  const id=keyId(crypto.createPublicKey(key)),timestamp=String(Math.floor(time/1000)),nonce=crypto.randomBytes(16).toString('hex');
  return {'X-Wallpaper-Key-Id':id,'X-Wallpaper-Timestamp':timestamp,'X-Wallpaper-Nonce':nonce,'X-Wallpaper-Signature':crypto.sign(null,canonical(method,route,body,timestamp,nonce,id),key).toString('base64')};
 }
 const call=(route,opts={})=>fetch(base+route,opts);
 const bytes=Buffer.from('synthetic-original'),sha256=crypto.createHash('sha256').update(bytes).digest('hex');
 try{
  const image={sha256,forDate:'2026-10-21',mime:'image/png',sizeBytes:bytes.length,publishedAt:new Date(now).toISOString()};
  await store.writeImage(image.mime,bytes);await store.writeDocument({imageAvailable:true,image});await store.favoriteImage(sha256,image.forDate,now);
  const manifestRoute=prefix+'/manifest';
  assert.equal((await call(manifestRoute)).status,401);
  assert.equal((await call(manifestRoute,{headers:headers(manifestRoute,'GET',Buffer.alloc(0),other.privateKey)})).status,401);
  assert.equal((await call(manifestRoute,{headers:headers(manifestRoute,'GET',Buffer.alloc(0),pair.privateKey,now-100000)})).status,401);
  const signed=headers(manifestRoute),first=await call(manifestRoute,{headers:signed});assert.equal(first.status,200);assert.match(first.headers.get('cache-control'),/private, no-store/);assert(!first.headers.has('access-control-allow-origin'));
  const manifest=await first.json();assert.equal(manifest.rows.length,1);assert.equal(manifest.rotationIntervalSeconds,1800);
  assert.equal((await call(manifestRoute,{headers:signed})).status,401);
  assert.equal((await call('/api/brief/data',{headers:headers('/api/brief/data')})).status,401);
  assert.equal((await call('/api/brief/favorites/manifest',{headers:headers('/api/brief/favorites/manifest')})).status,401);
  assert.equal((await call(prefix+'/'+sha256+'/image',{headers:headers(manifestRoute)})).status,401);
  const imageRoute=prefix+'/'+sha256+'/image';assert.deepEqual(Buffer.from(await (await call(imageRoute,{headers:headers(imageRoute)})).arrayBuffer()),bytes);
  const route=prefix+'/receipt',receipt={version:manifest.version,rotationIntervalSeconds:1800,displays:['1','2','3'].map(id=>({id,sha256}))};
  const send=async(r,signatureBody)=>{const body=Buffer.from(JSON.stringify(r));return call(route,{method:'POST',headers:{...headers(route,'POST',signatureBody||body),'Content-Type':'application/json'},body});};
  assert.equal((await send({...receipt,rotationIntervalSeconds:60})).status,400);
  assert.equal((await send({...receipt,displays:receipt.displays.slice(1)})).status,400);
  assert.equal((await send({...receipt,displays:[receipt.displays[0],receipt.displays[0],receipt.displays[2]]})).status,400);
  assert.equal((await send({...receipt,version:'f'.repeat(64)})).status,409);
  assert.equal((await send(receipt,Buffer.from('{}'))).status,401);
  assert.equal((await send(receipt)).status,200);
  assert.equal(wallpaperStatus(await store.favoriteManifest(),now).state,'confirmed');
  assert.equal(wallpaperStatus(await store.favoriteManifest(),now-60000).state,'pending');
  await store.setFavorite(sha256,false,now);
  assert.equal((await call(imageRoute,{headers:headers(imageRoute)})).status,404);
  assert.equal((await send(receipt)).status,409);
  assert.equal(wallpaperStatus(await store.favoriteManifest(),now).state,'pending');
  delete env.BRIEF_WALLPAPER_PUBLIC_KEY;assert.equal((await call(manifestRoute,{headers:headers(manifestRoute)})).status,401);
  console.log('wallpaper_reader: separate key scope, fail-closed enrollment, signatures, replay/age/path/body rejection, private originals, receipt validation/revocation; 640 three-screen rotation cycles, distinctness, no repeats and independent deadlines passed');
 }finally{await new Promise(r=>server.close(r));await pool.end();}
})().catch(e=>{console.error(e);process.exitCode=1;});
