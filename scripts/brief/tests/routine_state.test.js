'use strict';
const assert=require('node:assert/strict'),crypto=require('node:crypto'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const express=require('express'),{newDb}=require('pg-mem');
const {validate}=require('../web/document'),{createRouter}=require('../web/router'),{createStore}=require('../web/store'),{signedHeaders}=require('../web/publication');
async function main(){
  const now=Date.now(), routine={kind:'cloud',startTime:'07:00',readyBy:'07:30',startsOn:'2026-10-04',confirmedAt:new Date(now).toISOString(),localCron:false,notifications:false};
  const legacy={schemaVersion:1,generatedAt:new Date(now).toISOString(),forDate:'2026-10-03',editionType:'manual',timezone:'America/Chicago',routineEnabled:false,focus:{status:'missing',task:'Confirm priority',why:'No applicable planning input.',source:'Synthetic fixture'},sources:[{name:'Trials',status:'unverified'},{name:'Watch history',status:'stale'}],imageAvailable:false};
  const enabled={...legacy,routineEnabled:true,routine:{...routine,automationId:'synthetic-must-not-leak'}};
  assert.equal(validate(legacy,now).routineEnabled,false);
  assert.equal(validate(legacy,now).routine,null);
  const checked=validate(enabled,now);assert.equal(checked.routineEnabled,true);assert.deepEqual(checked.routine,routine);
  assert.deepEqual(checked.sources,validate(legacy,now).sources);assert(!JSON.stringify(checked).includes('synthetic-must-not-leak'));
  assert.throws(()=>validate({...enabled,routine:null},now));
  for(const change of [{kind:'local'},{startTime:'7:00'},{readyBy:'06:30'},{localCron:true},{notifications:true},{confirmedAt:new Date(now+600000).toISOString()}]) assert.throws(()=>validate({...enabled,routine:{...routine,...change}},now));
  const scope={document:{getElementById:()=>({addEventListener:()=>{}})},fetch:async()=>({status:401}),location:{replace:()=>{}}};
  vm.runInNewContext(fs.readFileSync(path.resolve(__dirname,'../web/page.js'),'utf8'),scope);
  const rendered=scope.routineStatus(checked);assert.match(rendered,/Daily updates enabled/);assert.match(rendered,/7:00 AM/);assert.match(rendered,/7:30 AM/);assert.match(rendered,/Mac must be online/);assert.match(rendered,/Source availability/);assert.doesNotMatch(rendered,/synthetic-must-not-leak/);
  assert.match(scope.routineStatus(validate(legacy,now)),/No enabled daily schedule/);
  const pg=newDb({noAstCoverageCheck:true}).adapters.createPg(),pool=new pg.Pool(),store=createStore(pool),keys=crypto.generateKeyPairSync('ed25519');
  const app=express();app.use(createRouter({store,env:{BRIEF_PUBLISH_PUBLIC_KEY:keys.publicKey.export({type:'spki',format:'der'}).toString('base64')},now:()=>now}));
  const server=app.listen(0,'127.0.0.1');await new Promise(resolve=>server.once('listening',resolve));
  try{
    const body=Buffer.from(JSON.stringify(enabled)),response=await fetch('http://127.0.0.1:'+server.address().port+'/api/brief/publish',{method:'POST',headers:{'Content-Type':'application/json',...signedHeaders(body,keys.privateKey,now)},body});
    assert.equal(response.status,200);const receipt=await response.json();assert.equal(receipt.routineEnabled,true);assert.equal(receipt.scheduleChanged,false);
    const stored=await store.readDocument();assert.equal(stored.routineEnabled,true);assert.deepEqual(stored.routine,routine);assert.deepEqual(stored.focus,validate(legacy,now).focus);assert.deepEqual(stored.sources,validate(legacy,now).sources);
    assert(!JSON.stringify(stored).includes('synthetic-must-not-leak'));
    console.log('routine_state: legacy compatibility, evidence-required enabled cloud status, missing sources unchanged, ID stripping, page text and signed receipt/storage roundtrip passed');
  }finally{await new Promise(resolve=>server.close(resolve));await pool.end();}
}
main().catch(error=>{console.error(error);process.exitCode=1;});
