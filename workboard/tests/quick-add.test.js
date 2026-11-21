'use strict';
const test=require('node:test'),assert=require('node:assert/strict');
const {mutate}=require('../model'),{makeInitial}=require('../personal'),{createAssistant}=require('../assistant');
test('personal quick add takes priority and position; priority editable',()=>{
 let b=makeInitial();const l=b.lists[0].id,d='2026-11-19';
 for(const t of ['A','B'])b=mutate(b,'card.create',{listId:l,title:t,plannedFor:d}).board;
 b=mutate(b,'card.create',{listId:l,title:'Top',plannedFor:d,priority:'key',index:0}).board;
 assert.deepEqual(b.cards.filter(c=>c.listId===l).map(c=>c.title),['Top','A','B']);
 assert.equal(b.cards.find(c=>c.title==='Top').priority,'key');assert.equal(b.cards.find(c=>c.title==='A').priority,'unassigned');
 b=mutate(b,'card.create',{listId:l,title:'Mid',plannedFor:d,index:2}).board;
 assert.deepEqual(b.cards.filter(c=>c.listId===l).map(c=>c.title),['Top','A','Mid','B']);
 assert.throws(()=>mutate(b,'card.create',{listId:l,title:'X',plannedFor:d,priority:'urgent'}));
 const c=b.cards.find(c=>c.title==='A');b=mutate(b,'card.update',{id:c.id,title:'A',description:'notes',labels:[],dueDate:'',priority:'high'}).board;
 assert.equal(b.cards.find(c=>c.title==='A').priority,'high');assert.equal(b.cards.find(c=>c.title==='A').description,'notes');
});
test('assistant quick add takes position and description can be set',async()=>{
 const files={'todos.json':{assistant:[{text:'One',priority:'low'},{text:'Two',priority:'low'}]},'task-checks.json':{},'timesheet.json':{active:null,entries:[],payments:[]}};let sha=1;
 const a=createAssistant({read:async n=>({data:structuredClone(files[n]),sha:String(sha)}),write:async(n,d)=>{files[n]=structuredClone(d);sha++;},lock:fn=>fn()});
 let s=await a.state();s=await a.change({revision:s.revision,action:'add',text:'New',priority:'high',index:1});
 assert.deepEqual(s.tasks.map(t=>t.text),['One','New','Two']);assert.equal(s.tasks[1].priority,'high');
 s=await a.change({revision:s.revision,action:'describe',text:'New',why:'  Details here '});assert.equal(s.tasks[1].why,'Details here');
 s=await a.change({revision:s.revision,action:'describe',text:'New',why:''});assert.equal(s.tasks[1].why,undefined);
});
