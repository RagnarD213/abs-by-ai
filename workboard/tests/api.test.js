'use strict';
const assert=require('node:assert/strict'),express=require('express'),{newDb}=require('pg-mem');
const {createStore}=require('../store'),{createRouter,attachment,MAX}=require('../router'),{initial,mutate}=require('../model');
const {createStore:createOwnerStore}=require('../../scripts/brief/web/store');
const env={BRIEF_OWNER_EMAIL:'owner@example.gmail.com',BRIEF_GOOGLE_CLIENT_ID:'fixture.apps.googleusercontent.com'},token='a'.repeat(64);
async function fixture(){const Pool=newDb({noAstCoverageCheck:true}).adapters.createPg().Pool,pool=new Pool(),store=createStore(pool),ownerStore=createOwnerStore(pool);await ownerStore.pinOwner(env.BRIEF_OWNER_EMAIL,'owner-sub');await ownerStore.addSession(token,'owner-sub',Date.now()+86400000);return {pool,store,ownerStore};}
async function main(){
 const {pool,store,ownerStore}=await fixture(),app=express();app.use(createRouter({store,ownerStore,env}));app.use((req,res)=>res.status(418).send('Existing app unchanged'));
 const server=app.listen(0,'127.0.0.1');await new Promise(r=>server.once('listening',r));const base='http://127.0.0.1:'+server.address().port;
 const headers={cookie:'__Host-absbyai_brief='+token,Origin:'https://absbyai.com','X-Workboard-Action':'change','Content-Type':'application/json'};
 const req=(p,o={})=>fetch(base+p,{redirect:'manual',...o}),get=()=>req('/api/workboard/state',{headers});let s;
 const change=async(action,payload,version=s.version)=>{const r=await req('/api/workboard/change',{method:'POST',headers,body:JSON.stringify({version,action,payload})});const data=await r.json();if(r.ok)s=data;return {status:r.status,data};};
 try{
  for(const path of ['/api/workboard/state','/API/WORKBOARD/STATE/','/api/workboard/page.js','/api/workboard/files/unknown'])assert.equal((await req(path)).status,401);
  assert.equal((await req('/workboard')).status,303);assert.equal((await req('/morningbrief')).status,418);assert.equal((await req('/dashboard')).status,418);
  s=await(await get()).json();assert.equal(s.cards.length,0);assert.equal(s.lists.length,10);assert.equal(s.version,0);
  const read=await get();assert.match(read.headers.get('cache-control'),/no-store/);assert.match(read.headers.get('content-security-policy'),/frame-ancestors 'none'/);assert(!read.headers.has('access-control-allow-origin'));
  for(const h of [{...headers,Origin:'https://evil.example'},{...headers,'X-Workboard-Action':''}])assert.equal((await req('/api/workboard/change',{method:'POST',headers:h,body:JSON.stringify({version:0,action:'list.create',payload:{name:'Bad'}})})).status,403);
  assert.equal((await change('card.create',{title:'QA card',listId:s.lists[0].id})).status,200);const id=s.target;
  assert.equal((await change('card.update',{id,title:'Edited QA card',description:'Line one\n<script>alert(1)</script>',labels:[{name:'Priority',color:'amber'}],dueDate:'2026-10-20'})).status,200);
  assert.equal((await change('check.add',{id,text:'Verify preview'})).status,200);const item=s.cards[0].checklist[0];await change('check.update',{id,itemId:item.id,text:'Verify preview and sound',done:true});assert(s.cards[0].checklist[0].done);
  await change('comment.add',{id,text:'Decision recorded'});assert.equal(s.cards[0].comments.length,1);
  const target=s.lists[3].id;await change('card.move',{id,listId:target,index:0});assert.equal(s.cards[0].listId,target);
  await change('card.create',{title:'Second card',listId:target});const second=s.target;await change('card.move',{id:second,listId:target,index:0});assert.equal(s.cards.filter(c=>c.listId===target)[0].id,second);
  await change('list.move',{id:target,index:0});assert.equal(s.lists[0].id,target);await change('list.update',{id:target,name:'Video queue'});
  const prev=s.version;await change('comment.add',{id,text:'New tab change'});const conflict=await change('comment.add',{id,text:'Stale tab change'},prev);assert.equal(conflict.status,409);assert(!s.cards.find(c=>c.id===id).comments.some(c=>c.text==='Stale tab change'));
  const bytes=Buffer.from('Private fixture attachment\n');const upload=await req('/api/workboard/cards/'+id+'/attachments',{method:'POST',headers:{...headers,'Content-Type':'text/plain','X-File-Name':encodeURIComponent('QA notes.txt'),'X-Board-Version':String(s.version)},body:bytes});assert.equal(upload.status,200);s=await upload.json();const a=s.cards.find(c=>c.id===id).attachments[0];
  assert.equal((await req('/api/workboard/files/'+a.id)).status,401);const download=await req('/api/workboard/files/'+a.id,{headers});assert.equal(download.status,200);assert.match(download.headers.get('content-disposition'),/^attachment;/);assert.equal(await download.text(),bytes.toString());
  assert.throws(()=>attachment(Buffer.from('<html>bad</html>'),'text/html','evil.html'));assert.throws(()=>attachment(Buffer.from('not png'),'image/png','x.png'));assert.throws(()=>attachment(Buffer.alloc(MAX+1),'text/plain','large.txt'));assert.throws(()=>attachment(bytes,'text/plain','../x.txt'));
  const invalid=await req('/api/workboard/cards/'+id+'/attachments',{method:'POST',headers:{...headers,'Content-Type':'application/pdf','X-File-Name':'bad.pdf','X-Board-Version':String(s.version)},body:bytes});assert.equal(invalid.status,400);
  await change('card.archive',{id});assert(s.cards.find(c=>c.id===id).archived);await change('card.restore',{id});assert(!s.cards.find(c=>c.id===id).archived);
  await change('list.archive',{id:target});assert.equal((await change('card.move',{id,listId:s.lists[1].id,index:0})).status,400);await change('list.restore',{id:target});
  const persisted=await createStore(pool).read();assert.equal(persisted.version,s.version);assert.equal(persisted.lists[0].name,'Video queue');assert.equal(persisted.cards.find(c=>c.id===id).attachments[0].id,a.id);
  await change('attachment.remove',{id,attachmentId:a.id});assert.equal((await req('/api/workboard/files/'+a.id,{headers})).status,404);
  assert.equal((await change('card.update',{id,title:'',description:'',labels:[],dueDate:''})).status,400);assert.equal((await change('card.update',{id,title:'Bad date',description:'',labels:[],dueDate:'2026-02-31'})).status,400);
  assert.equal((await change('list.move',{id:target,index:-1})).status,400);assert.equal((await change('run.start',{})).status,400);
  await ownerStore.addSession('b'.repeat(64),'other-sub',Date.now()+86400000);assert.equal((await req('/api/workboard/state',{headers:{cookie:'__Host-absbyai_brief='+'b'.repeat(64)}})).status,401);
  await ownerStore.renew(token,Date.now()-1);assert.equal((await get()).status,401);
  console.log('PASS: empty ten-list board, auth denial, owner pin, CSRF, private assets, CRUD, card/list ordering, checklist, comments, archive/restore, attachment privacy and validation, stale-tab 409, persisted reload, route isolation, no worker actions.');
 }finally{await new Promise(r=>server.close(r));await pool.end();}
}
if(require.main===module)main().catch(e=>{console.error(e);process.exitCode=1;});
module.exports={fixture,env,token};
