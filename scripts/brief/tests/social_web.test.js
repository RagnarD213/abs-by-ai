'use strict';
const assert=require('node:assert/strict'),express=require('express'),crypto=require('node:crypto');
const {Readable}=require('node:stream');
const {newDb}=require('pg-mem');
const {createStore}=require('../web/store'),{createRouter,COOKIE}=require('../web/router');
const {mediaURL,validateMaster}=require('../web/social');
const {signedHeaders}=require('../web/publication');
const now=Date.now();
const sample={schemaVersion:1,forDate:'2026-10-08',timezone:'America/Chicago',generatedAt:new Date(now).toISOString(),editionType:'daily',routineEnabled:false,focus:{status:'missing',task:'Synthetic priority',why:'Synthetic',source:'Synthetic'}};
const row=n=>({id:n.toString(16).padStart(64,'0'),platform:'instagram',account:'synthetic',scheduledAt:'2026-11-01T15:00:00Z',title:'Synthetic post',caption:'Synthetic caption',kind:'photo',cover:'https://database.blotato.io/storage/v1/object/public/public_media/abc-def/123-456.jpg',media:['https://database.blotato.io/storage/v1/object/public/public_media/abc-def/123-456.mp4'],approval:{status:'approved',reference:'Synthetic approval',quote:'Approved synthetic content'},provenance:[{source:'synthetic',sourceId:String(n),checkedAt:new Date(now).toISOString()}]});
(async()=>{
  for(const u of ['https://127.0.0.1/a.mp4','https://database.blotato.io.evil.test/a.mp4','https://database.blotato.io@evil.test/a.mp4','https://database.blotato.io/storage/v1/object/public/public_media/abc/def.mp4?url=http://localhost','file:///private/a','https://i.ytimg.com/../../private'])assert.equal(mediaURL(u),null);
  assert(mediaURL(row(1).cover));assert.throws(()=>validateMaster([{...row(1),approval:{status:'approved',reference:'',quote:''}}]));
  const {Pool}=newDb().adapters.createPg();const pool=new Pool(),store=createStore(pool);
  const keys=crypto.generateKeyPairSync('ed25519');
  const env={BRIEF_OWNER_EMAIL:'fixture@gmail.com',BRIEF_GOOGLE_CLIENT_ID:'123-fixture.apps.googleusercontent.com',BRIEF_PUBLISH_PUBLIC_KEY:keys.publicKey.export({type:'spki',format:'der'}).toString('base64')};
  await store.pinOwner(env.BRIEF_OWNER_EMAIL,'owner');await store.addSession('a'.repeat(64),'owner',now+86400000);
  let upstreamCalls=0,range;
  const app=express();app.use(createRouter({store,env,now:()=>now,mediaFetch:async(url,options)=>{upstreamCalls++;range=options.headers.Range;return {status:range?206:200,headers:new Map([['content-type',url.endsWith('.mp4')?'video/mp4':'image/jpeg'],['content-length','4'],['accept-ranges','bytes'],...(range?[['content-range','bytes 0-3/4']]:[])]),body:Readable.from(Buffer.from('test'))};}}));
  const server=await new Promise(resolve=>{const s=app.listen(0,'127.0.0.1',()=>resolve(s));});
  const base='http://127.0.0.1:'+server.address().port,cookie=COOKIE+'='+'a'.repeat(64);
  try{
    for(const route of ['/api/brief/master','/api/brief/media/'+row(1).id+'/video'])assert.equal((await fetch(base+route)).status,401);
    assert.equal(upstreamCalls,0);
    const rows=Array.from({length:253},(_,i)=>row(i+1));
    for(let offset=0;offset<rows.length;offset+=100){const bytes=Buffer.from(JSON.stringify({...sample,socialMasterImports:rows.slice(offset,offset+100)}));const response=await fetch(base+'/api/brief/publish',{method:'POST',headers:{'Content-Type':'application/json',...signedHeaders(bytes,keys.privateKey,now)},body:bytes});assert.equal(response.status,200);}
    await store.importMaster(validateMaster(rows.slice(0,100)));
    let after='',count=0;
    do{const response=await fetch(base+'/api/brief/master'+(after?'?after='+after:''),{headers:{cookie}});assert.equal(response.status,200);assert.match(response.headers.get('cache-control'),/private, no-store/);const page=await response.json();count+=page.rows.length;after=page.next;}while(after);
    assert.equal(count,253);
    const stored=await store.readDocument();assert(!stored.socialMasterImports);assert.equal(stored.focus.task,sample.focus.task);
    const media=base+'/api/brief/media/'+row(1).id+'/video';
    const full=await fetch(media,{headers:{cookie}});assert.equal(full.status,200);assert.equal(await full.text(),'test');
    const part=await fetch(media,{headers:{cookie,Range:'bytes=0-3'}});assert.equal(part.status,206);assert.equal(range,'bytes=0-3');assert.equal(part.headers.get('content-range'),'bytes 0-3/4');await part.text();
    assert.equal((await fetch(media,{headers:{cookie,Range:'bytes=0-1,3-4'}})).status,416);
    const privatePage=await fetch(base+'/morningbrief',{headers:{cookie}});assert.match(privatePage.headers.get('content-security-policy'),/media-src 'self'/);
    console.log('social_web: 253 persistent records, repeat import, pagination, unchanged text, owner-only media, byte ranges and SSRF rejection passed');
  }finally{await new Promise(resolve=>server.close(resolve));await pool.end();}
})().catch(e=>{console.error(e);process.exitCode=1;});
