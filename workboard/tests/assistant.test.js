'use strict';
const assert=require('node:assert/strict'),express=require('express');
const {createAssistant,unpaid,ordered}=require('../assistant'),{createRouter}=require('../router'),{fixture,env,token}=require('./api.test');
async function main(){
 const time={active:{startedAt:'2026-10-11T10:00:00Z'},entries:[{start:'x',end:'y',seconds:2180}],payments:[{paidAt:'2026-10-05T00:00:00Z',seconds:66000,sessions:3,entries:[]}]};
 assert.equal(unpaid(time,Date.parse('2026-10-11T11:00:00Z')).unpaidSeconds,5780);assert.equal(unpaid({...time,active:null}).recordedSeconds,2180);assert.equal(unpaid({active:null,entries:[],payments:[]}).hasUnpaidTime,false);assert.throws(()=>unpaid({...time,entries:[{seconds:'2180'}]}));assert.throws(()=>unpaid({...time,active:{startedAt:'invalid'}}));
 let files={'todos.json':{assistant:[{text:'Low first',priority:'low',why:'keep metadata',recurring:true,days:[0,4]},{text:'Key second',priority:'key'}],business:[{text:'Dan task'}],handoffs:[{text:'Handoff'}],custom:'preserved'},'task-checks.json':{checked:['assistant::Low first'],log:{},checkedAt:{'assistant::Low first':'2026-10-10'}},'timesheet.json':time};
 let sha=1,tail=Promise.resolve(),fail=false,writes=0;
 const adapter={read:async n=>({data:structuredClone(files[n]),sha:String(sha)}),write:async(n,data,s)=>{if(fail||s!==String(sha)){const e=new Error('CAS failed');e.status=409;throw e;}files[n]=structuredClone(data);sha++;writes++;},lock:fn=>{const run=tail.then(fn);tail=run.catch(()=>{});return run;}};
 const assistant=createAssistant(adapter),baseline=structuredClone(files);let s=await assistant.state();assert.equal(s.tasks[0].text,'Key second');
 s=await assistant.change({revision:s.revision,action:'move',text:'Low first',index:0});assert.equal(s.tasks[0].text,'Low first');assert.equal(s.tasks[0].priority,'low');assert.equal(s.tasks[0].why,'keep metadata');assert.deepEqual(s.tasks[0].days,[0,4]);
 const old=s.revision;s=await assistant.change({revision:s.revision,action:'priority',text:'Key second',priority:'high'});assert.equal(s.tasks[0].text,'Low first');assert.equal(s.tasks[1].priority,'high');await assert.rejects(()=>assistant.change({revision:old,action:'move',text:'Key second',index:0}),e=>e.status===409);
 const reloaded=await createAssistant(adapter).state();assert.deepEqual(reloaded.tasks,s.tasks);assert.deepEqual(files['timesheet.json'],baseline['timesheet.json']);assert.deepEqual(files['task-checks.json'],baseline['task-checks.json']);assert.deepEqual(files['todos.json'].business,baseline['todos.json'].business);assert.equal(files['todos.json'].custom,'preserved');
 fail=true;await assert.rejects(()=>assistant.change({revision:s.revision,action:'add',text:'Not saved',priority:'low'}));fail=false;assert(!files['todos.json'].assistant.some(t=>t.text==='Not saved'));
 await assert.rejects(()=>assistant.change({revision:s.revision,action:'priority',text:'Low first',priority:'constructor'}));
 s=await assistant.change({revision:s.revision,action:'add',text:'New shared task',priority:'unassigned'});assert.equal(s.tasks.at(-1).text,'New shared task');assert.equal(ordered([{priority:'low',text:'l'},{priority:'key',text:'k'}])[0].text,'k');
 const before=writes;await assistant.balance();assert.equal(writes,before);
 const f=await fixture(),app=express();let actions=[];app.use(createRouter({...f,env,assistant,timesheetAction:async(a,req,res)=>{actions.push(a);res.json({ok:true});}}));const server=app.listen(0,'127.0.0.1');await new Promise(r=>server.once('listening',r));const base='http://127.0.0.1:'+server.address().port,headers={cookie:'__Host-absbyai_brief='+token,Origin:'https://absbyai.com','X-Workboard-Action':'change','Content-Type':'application/json'};
 try{
  for(const p of ['/api/workboard/assistant','/api/workboard/assistant/unpaid','/api/workboard/assistant-page.js'])assert.equal((await fetch(base+p)).status,401);
  const r=await fetch(base+'/api/workboard/assistant/unpaid',{headers});assert.equal(r.status,200);assert((await r.json()).hasUnpaidTime);assert.match(r.headers.get('cache-control'),/no-store/);
  const post=(path,h=headers)=>fetch(base+path,{method:'POST',headers:h,body:'{}'});
  assert.equal((await post('/api/workboard/assistant/time/mark-paid',{})).status,401);assert.equal((await post('/api/workboard/assistant/time/mark-paid',{...headers,Origin:'https://evil.example'})).status,403);assert.equal(actions.length,0);
  for(const a of ['start','stop','mark-paid'])assert.equal((await post('/api/workboard/assistant/time/'+a)).status,200);assert.deepEqual(actions,['start','stop','mark-paid']);assert.equal((await post('/api/workboard/assistant/time/pay')).status,400);
  assert.equal((await f.store.read()).version,0);assert.equal((await f.store.read()).cards.length,0);
 }finally{await new Promise(r=>server.close(r));await f.pool.end();}
 console.log('PASS: shared assistant records, initial priority order, independent persistent drag rank, metadata preservation, stale writes/CAS failures, time and payment history untouched, strict unpaid summaries, owner-only reads and writes, CSRF, existing timer-handler dispatch, zero board migrations.');
}
main().catch(e=>{console.error(e);process.exitCode=1;});
