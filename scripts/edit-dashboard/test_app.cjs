'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
class Element { constructor(tag){this.tag=tag;this.children=[];this.dataset={};this.textContent=''} append(...xs){this.children.push(...xs)} addEventListener(){} }
const document={createElement:t=>new Element(t),getElementById:()=>new Element('button'),addEventListener(){}};
const context=vm.createContext({document,window:{addEventListener(){}},console,Date,Set});
vm.runInContext(fs.readFileSync(__dirname+'/app.js','utf8'),context);
function nodes(e){return [e,...e.children.flatMap(nodes)]}
function fixture(auxiliary,states=['waiting']){return {id:'DS-109',title:'Hormozi setup',states,held:0,tickets:1,occupies:false,auxiliary,workKind:'setup'}}
context.state={data:{used:3,cap:3,jobs:[fixture(true)],issues:[]}};
let all=nodes(vm.runInContext("card('m2',state,{reserved:{m2:[]}},1)",context));
assert.equal(all.filter(e=>e.tag==='strong'&&e.textContent==='Hormozi setup').length,1);
assert(all.some(e=>e.textContent==='SETUP / HELPER WORK (NOT EDIT SLOTS)'));
assert(!all.some(e=>e.textContent==='WAITING OR RESERVED'));
// A normal waiter stays a waiter, a real active edit stays in production.
context.state.data.jobs=[fixture(false)];
all=nodes(vm.runInContext("card('m2',state,{reserved:{m2:[]}},1)",context));
assert(all.some(e=>e.textContent==='WAITING OR RESERVED'));
assert.equal(all.filter(e=>e.tag==='strong').length,1);
context.state.data.jobs=[{...fixture(false,['active']),occupies:true}];
all=nodes(vm.runInContext("card('m2',state,{reserved:{m2:[]}},1)",context));
assert.equal(all.filter(e=>e.tag==='strong').length,1);
assert(!all.some(e=>e.textContent==='SETUP / HELPER WORK (NOT EDIT SLOTS)'));
console.log('Passed setup/helper deduplication and active/waiting UI checks');

context.state.data.jobs=[{...fixture(true),workKind:'helper',batchStage:'Waiting in production queue'}];
all=nodes(vm.runInContext("card('m2',state,{reserved:{m2:['DS-109']}},1)",context));
assert(all.some(e=>e.textContent==='WAITING OR RESERVED'));
assert(!all.some(e=>e.textContent==='SETUP / HELPER WORK (NOT EDIT SLOTS)'));
assert.equal(all.filter(e=>e.tag==='strong').length,1);
assert(all.some(e=>e.textContent.includes('Slot reserved') && e.textContent.includes('render steps queued')));
