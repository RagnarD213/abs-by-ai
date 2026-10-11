'use strict';
const {createHash}=require('node:crypto');
const {BoardError}=require('./model');
const priorities={key:0,high:1,med:2,low:3,unassigned:4};
const revision=tasks=>createHash('sha256').update(JSON.stringify(tasks)).digest('hex');
function ordered(tasks){return tasks.map((t,i)=>({t,i})).sort((a,b)=>{
 const ar=Number.isInteger(a.t.boardRank)?a.t.boardRank:null,br=Number.isInteger(b.t.boardRank)?b.t.boardRank:null;
 return ar!==null||br!==null?(ar??Number.MAX_SAFE_INTEGER)-(br??Number.MAX_SAFE_INTEGER)||a.i-b.i:(priorities[a.t.priority]??3)-(priorities[b.t.priority]??3)||a.i-b.i;
}).map(x=>x.t);}
function unpaid(data,now=Date.now()){
 if(!data||!Array.isArray(data.entries)||!Array.isArray(data.payments)||data.entries.some(e=>!Number.isFinite(e.seconds)||e.seconds<0)||(data.active&&!Number.isFinite(Date.parse(data.active.startedAt))))throw new BoardError('Timesheet data unavailable or invalid. Retry before assessing unpaid time.',503);
 const recordedSeconds=data.entries.reduce((sum,e)=>sum+e.seconds,0),activeSeconds=data.active?Math.max(0,Math.round((now-Date.parse(data.active.startedAt))/1000)):0;
 return {recordedSeconds,activeSeconds,unpaidSeconds:recordedSeconds+activeSeconds,hasUnpaidTime:recordedSeconds+activeSeconds>0,unpaidSessions:data.entries.length,active:data.active||null,lastPaidAt:data.payments.at(-1)?.paidAt||null,asOf:new Date(now).toISOString()};
}
function createAssistant({read,write,lock,onTodos=()=>{}}){
 async function state(savedTodos){const [todos,checks,time]=await Promise.all([savedTodos?Promise.resolve({data:savedTodos}):read('todos.json'),read('task-checks.json'),read('timesheet.json')]);const tasks=todos.data.assistant;if(!Array.isArray(tasks))throw new BoardError('Assistant task data unavailable.',503);return {tasks:ordered(tasks),revision:revision(tasks),...{checked:checks.data.checked||[],log:checks.data.log||{},checkedAt:checks.data.checkedAt||{}},timesheet:{...unpaid(time.data),entries:time.data.entries,payments:time.data.payments}};}
 async function change(p){return lock(async()=>{
  const cur=await read('todos.json'),tasks=cur.data.assistant;if(!Array.isArray(tasks))throw new BoardError('Assistant task data unavailable.',503);
  if(p.revision!==revision(tasks))throw new BoardError('Assistant tasks changed. Refresh before saving.',409);
  let next=structuredClone(tasks);
  if(p.action==='add'){
   if(typeof p.text!=='string'||!p.text.trim()||p.text.length>500)throw new BoardError('Enter a task of up to 500 characters.');
   if(next.some(t=>t.text.toLowerCase()===p.text.trim().toLowerCase()))throw new BoardError('That task is already on the list.',409);
   if(!(Object.hasOwn(priorities,p.priority)))throw new BoardError('Choose an existing priority.');
   next.push({text:p.text.trim(),priority:p.priority,recurring:false,addedAt:new Date().toISOString().slice(0,10)});
   if(tasks.some(t=>Number.isInteger(t.boardRank)))next=ordered(next).map((t,i)=>({...t,boardRank:i}));
  }else{
   const t=next.find(t=>t.text===p.text);if(!t)throw new BoardError('Task not found.',404);
   if(p.action==='priority'){if(!(Object.hasOwn(priorities,p.priority)))throw new BoardError('Choose an existing priority.');t.priority=p.priority;}
   else if(p.action==='move'){const sorted=ordered(next),rest=sorted.filter(x=>x!==t);if(!Number.isInteger(p.index)||p.index<0||p.index>rest.length)throw new BoardError('Invalid position.');rest.splice(p.index,0,t);next=rest.map((t,i)=>({...t,boardRank:i}));}
   else throw new BoardError('Unknown assistant action.');
  }
  await write('todos.json',{...cur.data,assistant:next},cur.sha);onTodos({...cur.data,assistant:next});return state({...cur.data,assistant:next});
 });}
 return {state,change,async balance(){const cur=await read('timesheet.json');return {...unpaid(cur.data),source:'timesheet.json',sourceRevision:cur.sha};}};
}
module.exports={createAssistant,ordered,unpaid,revision};
