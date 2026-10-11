'use strict';
// Isolated disposable schema in the existing authorized database. No production
// table or card is selected or changed. Actual Postgres proves row-lock behavior.
const assert=require('node:assert/strict'),fs=require('node:fs'),{Pool}=require('pg'),{randomUUID}=require('node:crypto'),{createStore}=require('../store');
async function main(){
 const source=fs.readFileSync(process.argv[2],'utf8'),line=source.split(/\r?\n/).find(x=>x.startsWith('DATABASE_PUBLIC_URL='));if(!line)throw new Error('Existing public database URL unavailable.');
 let connectionString=line.slice('DATABASE_PUBLIC_URL='.length).trim();if(/^(["']).*\1$/.test(connectionString))connectionString=connectionString.slice(1,-1);
 const schema='workboard_test_'+randomUUID().replaceAll('-',''),admin=new Pool({connectionString,connectionTimeoutMillis:15000});let pool;
 try{
   await admin.query('CREATE SCHEMA '+schema);pool=new Pool({connectionString,options:'-c search_path='+schema,max:10});const store=createStore(pool);let s=await store.read();
   const workerId=randomUUID();s=(await store.execution('enable',{workerId})).state;
   s=await store.change(s.version,'card.create',{listId:s.lists[0].id,title:'TEST ONLY real Postgres locking'});const id=s.target,q=s.lists.find(l=>l.tone==='codex'&&l.name.includes('queue'));
   s=await store.change(s.version,'card.move',{id,listId:q.id,index:0});
   const claims=await Promise.all(Array.from({length:8},()=>store.execution('claim',{workerId,agent:'codex'})));
   assert.equal(claims.filter(x=>x.claim).length,1);const claim=claims.find(x=>x.claim).claim;
   await store.execution('update',{workerId,runId:claim.run.id,status:'completed',summary:'Synthetic locking test passed.'});
   const persisted=await createStore(pool).read();assert.equal(persisted.cards.find(c=>c.id===id).run.status,'completed');
   console.log('PASS: real Postgres, eight simultaneous claim requests yield exactly one claim; result persists across store restart. Disposable schema only.');
 }finally{if(pool)await pool.end();await admin.query('DROP SCHEMA IF EXISTS '+schema+' CASCADE');await admin.end();}
}
main().catch(()=>{console.error('Disposable Postgres test failed; no credential details printed.');process.exitCode=1;});
