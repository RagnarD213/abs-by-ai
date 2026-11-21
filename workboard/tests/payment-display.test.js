'use strict';
// Exercise the shipped page script with a disposable DOM and read-only API fixture.
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const {unpaid}=require('../assistant');
const source=fs.readFileSync(require.resolve('../assistant-page.js'),'utf8');
async function page(entries,active=null){
 let now=Date.parse('2026-10-23T12:00:00Z');
 const elements=new Map(),intervals=new Map(),events=new Map(),requests=[];
 class Element{
  constructor(){this.children=[];this.value='';}
  set id(value){this._id=value;elements.set(value,this);}get id(){return this._id;}
  append(...children){this.children.push(...children);}
  remove(){elements.delete(this.id);}
  addEventListener(){}setAttribute(){}
 }
 for(const id of ['board','search','assistant-jump']){const e=new Element();e.id=id;}
 const timesheet={entries:entries.map(seconds=>({seconds})),active,payments:[{paidAt:'2026-10-20T00:00:00Z',seconds:99999}]};
 const before=JSON.stringify(timesheet);
 const context={Intl,Date:class extends Date{static now(){return now;}},document:{createElement:()=>new Element(),getElementById:id=>elements.get(id),querySelector:()=>null,hidden:false},window:{addEventListener:(name,fn)=>events.set(name,fn)},setInterval:(fn,ms)=>intervals.set(ms,fn),notice:()=>{},fetch:async(path,options)=>{requests.push({path,options});return {ok:true,json:async()=>({tasks:[],checked:[],log:{},timesheet:{...timesheet,...unpaid(timesheet,now)}})};}};
 vm.runInNewContext(source,context);
 await new Promise(resolve=>setImmediate(resolve));
 return {text:id=>elements.get(id).textContent,tick:seconds=>{now+=seconds*1000;intervals.get(1000)();},refresh:()=>events.get('focus')(),requests,checkUnchanged:()=>assert.equal(JSON.stringify(timesheet),before)};
}
async function main(){
 let p=await page([]);assert.equal(p.text('assistant-payment'),'Next payment: $0.00 at $30/hour');assert.match(p.text('assistant-time'),/Completed: 0h 0m · Not clocked in/);
 p=await page([15418]);assert.equal(p.text('assistant-payment'),'Next payment: $128.48 at $30/hour');assert.match(p.text('assistant-time'),/Unpaid: 4h 16m · Completed: 4h 16m/);p.checkUnchanged();
 p=await page([3600],{startedAt:'2026-10-23T11:30:00Z'});assert.equal(p.text('assistant-payment'),'Next payment: $45.00 at $30/hour (includes running time)');assert.match(p.text('assistant-time'),/Unpaid: 1h 30m · Completed: 1h 0m · Clocked in: 0h 30m/);
 p.tick(60);assert.equal(p.text('assistant-payment'),'Next payment: $45.50 at $30/hour (includes running time)');assert.match(p.text('assistant-time'),/Completed: 1h 0m · Clocked in: 0h 31m/);await p.refresh();assert.equal(p.requests.length,2);p.checkUnchanged();
 // Round the combined seconds once, including half-cent ties, not rounded hours or subtotals.
 for(const [seconds,amount] of [[1,'0.01'],[2,'0.02'],[3,'0.03'],[4,'0.03'],[59,'0.49'],[60,'0.50'],[123456,'1,028.80']]){p=await page([seconds]);assert.equal(p.text('assistant-payment'),`Next payment: $${amount} at $30/hour`);}
 p=await page([1],{startedAt:'2026-10-23T11:59:57Z'});assert.equal(p.text('assistant-payment'),'Next payment: $0.03 at $30/hour (includes running time)');
 p=await page([],{startedAt:'2026-10-23T12:00:05Z'});assert.equal(p.text('assistant-payment'),'Next payment: $0.00 at $30/hour (includes running time)');
 assert(p.requests.every(r=>r.path==='/api/workboard/assistant'&&!r.options.method&&r.options.cache==='no-store'));p.checkUnchanged();
 console.log('PASS: zero, completed, active, ticking, focus refresh, cents and half-cent rounding, total rounded once, paid history excluded, read-only rendering.');
}
main().catch(e=>{console.error(e);process.exitCode=1;});
