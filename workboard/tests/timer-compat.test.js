'use strict';
// Execute the production handler bodies against disposable storage, never production.
const assert=require('node:assert/strict'),vm=require('node:vm'),fs=require('node:fs');
const source=fs.readFileSync(require.resolve('../../server'),'utf8');
let data={active:null,entries:[{start:'2026-10-10T10:00:00Z',end:'2026-10-10T11:00:00Z',seconds:3600}],payments:[{paidAt:'2026-10-09T10:00:00Z',seconds:7200,sessions:2,entries:[]}]};
const historical=structuredClone(data.payments),context={GITHUB_TOKEN:'synthetic-only',timesheetCache:null,Date,loadTimesheet:async()=>({...structuredClone(data),sha:'fixture'}),saveTimesheetToGitHub:async next=>{data=structuredClone(next);return {ok:true};}};
vm.createContext(context);
for(const name of ['startTimesheet','stopTimesheet','markTimesheetPaid']){const start=source.indexOf('async function '+name+'('),end=source.indexOf('\napp.post(',start);assert(start>0&&end>start);vm.runInContext(source.slice(start,end),context);}
async function call(name){let status=200,body;const res={status:n=>{status=n;return res;},json:d=>{body=d;return res;}};await context[name]({},res);assert.equal(status,200);return body;}
(async()=>{
 await call('startTimesheet');assert(data.active);assert.equal(data.entries[0].seconds,3600);assert.deepEqual(data.payments,historical);
 const started=data.active.startedAt;await call('startTimesheet');assert.equal(data.active.startedAt,started);
 data.active.startedAt=new Date(Date.now()-600000).toISOString();await call('stopTimesheet');assert.equal(data.active,null);assert.equal(data.entries.length,2);assert(Math.abs(data.entries[1].seconds-600)<=1);assert.deepEqual(data.payments,historical);
 await call('startTimesheet');data.active.startedAt=new Date(Date.now()-300000).toISOString();const payment=await call('markTimesheetPaid');assert(Math.abs(payment.seconds-4500)<=1);assert.equal(data.entries.length,0);assert(data.active);assert.deepEqual(data.payments.slice(0,-1),historical);assert.equal(data.payments.at(-1).sessions,3);assert.equal(data.active.startedAt,payment.paidAt);
 console.log('PASS: actual shared production timer handlers preserve unpaid accumulation and historical payments, start idempotently, close/reopen active sessions at synthetic payment. No production writes.');
})().catch(e=>{console.error(e);process.exitCode=1;});
