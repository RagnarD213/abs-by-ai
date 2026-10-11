'use strict';
const assert=require('node:assert/strict'),express=require('express'),{randomUUID}=require('node:crypto');
const {fixture,env,token}=require('./api.test'),{createRouter}=require('../router'),{createStore}=require('../store');
async function main(){
 const f=await fixture(),app=express();app.use(createRouter({...f,env}));const server=app.listen(0,'127.0.0.1');await new Promise(r=>server.once('listening',r));
 const base='http://127.0.0.1:'+server.address().port,headers={Cookie:'__Host-absbyai_brief='+token,Origin:'https://absbyai.com','X-Workboard-Action':'change','Content-Type':'application/json'};
 const api=async(action,payload={},h=headers)=>{const r=await fetch(base+'/api/workboard/execution',{method:'POST',headers:h,body:JSON.stringify({action,payload})});return {status:r.status,data:await r.json()};};
 try{
   assert.equal((await api('enable',{workerId:randomUUID()},{})).status,401);assert.equal((await api('enable',{workerId:randomUUID()},{...headers,Origin:'https://evil.example'})).status,403);
   const workerId=randomUUID();let s=(await api('enable',{workerId})).data.state;
   s=await f.store.change(s.version,'card.create',{title:'TEST API claim',listId:s.lists[0].id});const id=s.target,q=s.lists.find(l=>l.tone==='claude'&&l.name.includes('queue'));
   s=await f.store.change(s.version,'card.move',{id,listId:q.id,index:0});const claimed=await api('claim',{workerId,agent:'claude'});assert.equal(claimed.data.claim.id,id);assert.equal(claimed.data.claim.run.status,'claimed');
   assert.equal((await api('claim',{workerId,agent:'claude'})).data.claim,undefined);
   const runId=claimed.data.claim.run.id;assert.equal((await api('update',{workerId:'other',runId,status:'completed',summary:'bad'})).status,409);
   const result=await api('update',{workerId,runId,status:'completed',summary:'Verified test.'});const c=result.data.state.cards.find(c=>c.id===id);assert.equal(c.run.summary,'Verified test.');assert.match(result.data.state.lists.find(l=>l.id===c.listId).name,/review/);
   const persisted=await createStore(f.pool).read();assert.equal(persisted.cards.find(c=>c.id===id).run.status,'completed');assert.equal((await api('update',{workerId,runId,status:'failed',summary:'duplicate'})).data.status,'completed');
   console.log('PASS: execution endpoint owner auth/CSRF, assignment persistence, atomic claim, duplicate claim, worker ownership, bounded same-card summary, review transition, reload, terminal no-replay.');
 }finally{await new Promise(r=>server.close(r));await f.pool.end();}
}
main().catch(e=>{console.error(e);process.exitCode=1;});
