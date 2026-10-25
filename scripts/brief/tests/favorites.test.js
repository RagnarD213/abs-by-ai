'use strict';
const assert=require('node:assert/strict'),crypto=require('node:crypto'),express=require('express');
const {newDb}=require('pg-mem');
const {createStore}=require('../web/store');
const {createRouter,COOKIE,AGE}=require('../web/router');
const {wallpaperStatus}=require('../web/favorites');
const {signedHeaders}=require('../web/publication');
(async()=>{
 const pg=newDb({noAstCoverageCheck:true}).adapters.createPg(),pool=new pg.Pool(),store=createStore(pool),now=Date.now();
 const keys=crypto.generateKeyPairSync('ed25519');
 const env={BRIEF_OWNER_EMAIL:'synthetic@gmail.com',BRIEF_GOOGLE_CLIENT_ID:'123456-test.apps.googleusercontent.com',BRIEF_PUBLISH_PUBLIC_KEY:keys.publicKey.export({type:'spki',format:'der'}).toString('base64')};
 await store.pinOwner(env.BRIEF_OWNER_EMAIL,'owner');await store.addSession('a'.repeat(64),'owner',now+AGE);await store.addSession('b'.repeat(64),'other',now+AGE);
 const app=express();app.use(createRouter({store,env,now:()=>now}));const server=app.listen(0,'127.0.0.1');await new Promise(r=>server.once('listening',r));
 const base='http://127.0.0.1:'+server.address().port,owner={cookie:COOKIE+'='+'a'.repeat(64)};
 const call=(url,options={})=>fetch(base+url,{...options,headers:{...owner,...options.headers}});
 const mutate=(url,body,options={})=>call(url,{method:'POST',...options,headers:{origin:'https://absbyai.com','X-Brief-Action':'favorite','Content-Type':'application/json',...options.headers},body:JSON.stringify(body)});
 const bytes=Buffer.from('original-private-image-bytes'),sha256=crypto.createHash('sha256').update(bytes).digest('hex');
 const image={forDate:'2026-10-21',sha256,mime:'image/png',sizeBytes:bytes.length,publishedAt:new Date(now-86400000).toISOString()};
 const doc={schemaVersion:1,forDate:'2026-10-25',imageAvailable:true,image};
 await store.writeDocument(doc);await store.writeImage(image.mime,bytes);
 try{
  for(const route of ['/api/brief/favorites','/api/brief/favorites/manifest','/api/brief/favorites.js','/api/brief/favorites/'+sha256+'/image']){
   for(const cookie of ['',COOKIE+'='+'b'.repeat(64),'absbyai_dash=legacy'])assert.equal((await call(route,{headers:{cookie}})).status,401);
  }
  assert.equal((await mutate('/api/brief/favorites',image)).status,400);
  const choice={sha256,forDate:image.forDate};
  assert.equal((await mutate('/api/brief/favorites',choice,{headers:{origin:'https://evil.example'}})).status,403);
  assert.equal((await mutate('/api/brief/favorites',{...choice,forDate:doc.forDate})).status,409);
  assert.equal((await mutate('/api/brief/favorites',{...choice,url:'file:///etc/passwd'})).status,400);
  let result=await mutate('/api/brief/favorites',choice);assert.equal(result.status,200);let saved=await result.json();assert.equal(saved.favorite.forDate,'2026-10-21');assert.equal(saved.wallpaper.state,'pending_setup');
  result=await mutate('/api/brief/favorites',choice);assert.equal(result.status,200);assert.equal((await result.json()).favorite.favoritedAt,saved.favorite.favoritedAt);
  assert.equal((await store.listFavorites()).rows.length,1);
  assert.equal((await mutate('/api/brief/favorites',{...choice,sha256:'f'.repeat(64)})).status,409);
  // Signed publication does not acquire private-read rights.
  assert.equal((await call('/api/brief/favorites/manifest',{headers:{cookie:'',...signedHeaders(Buffer.from(''),keys.privateKey,now)}})).status,401);
  // Replacing the daily hero cannot change or destroy a saved favorite.
  await store.writeImage('image/png',Buffer.from('next image'));await store.writeDocument({...doc,image:null});
  const original=await call('/api/brief/favorites/'+sha256+'/image');assert.equal(original.status,200);assert.deepEqual(Buffer.from(await original.arrayBuffer()),bytes);assert.match(original.headers.get('cache-control'),/private, no-store/);assert(!original.headers.has('access-control-allow-origin'));assert.match(original.headers.get('content-disposition'),/attachment/);
  result=await mutate('/api/brief/favorites/'+sha256,{active:false},{method:'PUT'});assert.equal(result.status,200);assert.equal((await result.json()).favorite.active,false);
  assert.equal((await store.favoriteManifest()).rows.length,0);assert.equal((await store.listFavorites()).rows.length,1);
  assert.equal((await call('/api/brief/favorites/'+sha256+'/image')).status,200);
  result=await mutate('/api/brief/favorites/'+sha256,{active:true},{method:'PUT'});assert.equal((await result.json()).favorite.active,true);
  assert.equal((await store.favoriteManifest()).rows.length,1);
  assert.equal((await mutate('/api/brief/favorites',choice)).status,200); // archived original can be reselected even after replacement
  assert.deepEqual(await store.readDocument(),{...doc,image:null});
  const receipt={rotationIntervalSeconds:1800,displays:[{id:'1'},{id:'2'},{id:'3'}]};
  const manifest=await store.favoriteManifest();assert.match(manifest.feedbackPolicy,/positive.*neutral/);
  assert.equal(wallpaperStatus({...manifest,receipt:{...receipt,version:manifest.version,displayCount:3,checkedAt:new Date(now).toISOString()}},now).state,'confirmed');
  assert.equal(wallpaperStatus({...manifest,receipt:{...receipt,version:manifest.version,displayCount:3,checkedAt:new Date(now-600000).toISOString()}},now).state,'pending');
  assert.equal(wallpaperStatus({...manifest,receipt:{...receipt,version:'old',displayCount:3,checkedAt:new Date(now).toISOString()}},now).state,'pending');
  assert.equal(wallpaperStatus({...manifest,receipt:{...receipt,version:manifest.version,displayCount:2,checkedAt:new Date(now).toISOString()}},now).state,'pending');
  assert.equal((await call('/api/brief/favorites?after=../../etc/passwd')).status,400);
  assert.equal((await mutate('/api/brief/favorites',{sha256,forDate:image.forDate,padding:'x'.repeat(2000)})).status,413);
  console.log('favorites: owner-only reads/writes, CSRF, digest/date binding, duplicate clicks, immutable originals after replacement, reversible removal, neutral feedback, stale/offline/three-display status passed');
 }finally{await new Promise(r=>server.close(r));await pool.end();}
})().catch(e=>{console.error(e);process.exitCode=1;});
