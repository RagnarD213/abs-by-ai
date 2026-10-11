'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
async function test(){
  const controls={'move-list':{value:'queue'},'move-position':{value:'1',options:[{value:'0'},{value:'1'}]},workers:{},'execution-status':{}};
  let pending,locked=false;
  const context=vm.createContext({console,AbortSignal,setInterval,clearInterval,
    state:{cards:[{id:'test',listId:'unassigned'}]},current:'test',busy:false,conflict:false,
    document:{getElementById:id=>controls[id]},$:id=>controls[id],
    busySet:value=>{locked=value;context.busy=value;},
    getCard:()=>context.state.cards[0],activeLists:()=>[{id:'queue'},{id:'unassigned'},{id:'progress'}],
    render:()=>{},positions:()=>{controls['move-position'].value='0';},
    renderCardParts:()=>{controls['move-list'].value=context.state.cards[0].listId;controls['move-position'].value='0';},
    response:async res=>res,fetch:()=>new Promise(resolve=>{pending=resolve;}),window:{},notice:()=>{}
  });
  vm.runInContext(fs.readFileSync(require.resolve('./execution-page.js'),'utf8'),context);
  const same=vm.runInContext("executionCall('heartbeat')",context);
  assert.equal(locked,true,'owner saves cannot overlap an execution request');
  pending({state:{cards:[{id:'test',listId:'unassigned'}]}});await same;
  assert.equal(controls['move-list'].value,'queue','progress refresh keeps a pending move destination');
  assert.equal(controls['move-position'].value,'1','progress refresh keeps a pending position');
  assert.equal(locked,false);
  const moved=vm.runInContext("executionCall('claim')",context);
  pending({state:{cards:[{id:'test',listId:'progress'}]}});await moved;
  assert.equal(controls['move-list'].value,'progress','a real claimed-card move updates the controls');
  assert.equal(locked,false);
  console.log('Execution UI request locking and pending move preservation passed.');
}
test().catch(e=>{console.error(e);process.exitCode=1;});
