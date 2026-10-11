'use strict';
// Credentials stay in the HttpOnly owner cookie. The tab proxies only claims
// and bounded run status between the owner API and the loopback worker.
let localConnection=null,executionArmed=false,executionBusy=false,executionTimer=null,hasActivation=false;
async function localCall(path,payload={}){
  const res=await fetch('http://127.0.0.1:8843/'+path,{method:'POST',headers:{'Content-Type':'application/json','X-Workboard-Local':'owner-tab'},body:JSON.stringify(payload),signal:AbortSignal.timeout(10000)});
  const data=await res.json();if(!res.ok)throw new Error(data.error||'Local worker unavailable.');return data;
}
async function executionCall(action,payload={}){
  const data=await response(await fetch('/api/workboard/execution',{method:'POST',headers:{'Content-Type':'application/json','X-Workboard-Action':'change'},body:JSON.stringify({action,payload}),signal:AbortSignal.timeout(10000)}));
  state=data.state;render();if(current)renderCardParts();return data;
}
async function connectWorker(){
  try{
    localConnection={...await localCall('hello'),runs:[]};executionArmed=false;hasActivation=false;
    if(executionTimer)clearInterval(executionTimer);executionTimer=setInterval(executionTick,5000);
    notice('Local worker connected. Enable to arm new assignments. Existing queue cards need an explicit Run.');renderExecution();
  }catch(e){notice('Could not connect to the local worker: '+e.message);}
}
async function executionTick(){
  if(!localConnection||executionBusy||busy||conflict)return;executionBusy=true;
  try{
    if(state.execution?.workerId!==localConnection.workerId)return;
    const heartbeat=await executionCall('heartbeat',{workerId:localConnection.workerId});
    localConnection=await localCall('poll',{proof:heartbeat.controlProof});
    for(const r of localConnection.runs){
      const c=state.cards.find(c=>c.run?.id===r.runId);
      if(!c||!['claimed','running','stopping'].includes(c.run.status))continue;
      const payload={workerId:localConnection.workerId,runId:r.runId,status:r.status,summary:r.summary};
      if(r.sessionId)payload.sessionId=r.sessionId;if(r.workspace)payload.workspace=r.workspace;
      await executionCall('update',payload);
    }
    if(executionArmed&&state.execution?.enabled&&!state.execution.paused){
      for(const agent of ['claude','codex']){
        const result=await executionCall('claim',{workerId:localConnection.workerId,agent});
        if(result.claim){
          try{await localCall('start',{card:result.claim,proof:result.claimProof});}
          catch(e){await executionCall('update',{workerId:localConnection.workerId,runId:result.claim.run.id,status:'blocked',summary:'Local launch was not confirmed. Inspect local logs before continuing. No automatic retry.'});}
        }
      }
    }
    renderExecution();
  }catch(e){executionArmed=false;localConnection=null;clearInterval(executionTimer);notice('Execution connection interrupted: '+e.message+'. Active agents stop after 35 seconds without a heartbeat. Reconnect explicitly.');renderExecution();}
  finally{executionBusy=false;}
}
function renderExecution(){
  const status=document.getElementById('execution-status');if(status)status.textContent=localConnection?(executionArmed&&!state.execution?.paused?'Local agents enabled':'Local agents paused'):'Local agents disconnected';
}
function executionPanel(){showPanel('Local Claude and Codex',body=>{
  body.append(el('p','','Start the local worker on this Mac, connect, then Enable. Keep this authenticated tab open. Each agent runs one card at a time, in queue order. Existing cards stay idle until Run or a new move into the queue.'));
  body.append(el('p','muted','Local command: node workboard/local-worker.js /absolute/private/runner-state --env-file /path/to/existing/private-env-file'));
  body.append(button('Connect local worker',connectWorker),button('Enable new assignments',async()=>{
    if(!localConnection)return notice('Connect the local worker first.');
    try{await executionCall(hasActivation&&state.execution?.enabled?'resume':'enable',{workerId:localConnection.workerId});hasActivation=true;executionArmed=true;renderExecution();notice('Enabled. Only deliberate assignments or explicit Run actions can start.');await executionTick();}catch(e){notice(e.message);}
  }),button('Pause queue',async()=>{executionArmed=false;try{await executionCall('pause');renderExecution();notice('Queue paused. Active work continues.');}catch(e){notice(e.message);}}),button('Stop all and disable',async()=>{executionArmed=false;try{await executionCall('disable');await executionTick();renderExecution();notice('Stop requested for all active runs. Existing changes are retained.');}catch(e){notice(e.message);}},'btn danger'));
});}
window.renderExecutionCard=function(c){
  const box=document.getElementById('card-execution');if(!box)return;box.replaceChildren();
  const tone=state.lists.find(l=>l.id===c.listId)?.tone;if(!c.run&&!['claude','codex'].includes(tone))return;
  box.append(el('h3','','Agent execution'));
  if(c.run){
    box.append(el('p','',c.run.agent+' · '+c.run.status),el('p','',c.run.summary||''));
    if(c.run.sessionId)box.append(el('p','muted','Session: '+c.run.sessionId));
    if(c.run.workspace)box.append(el('p','muted','Local workspace: '+c.run.workspace));
    if(['claimed','running','stopping','queued'].includes(c.run.status))box.append(button('Stop run',async()=>{try{await executionCall('stop',{id:c.id});await executionTick();}catch(e){notice(e.message);}},'btn danger'));
    else box.append(button('Inspected changes: continue task',async()=>{
      if(!confirm('Continue this task after inspecting previous files and side effects? A new session will inspect prior work. External effects are never automatically retried.'))return;
      try{await executionCall('continue',{id:c.id});await executionTick();}catch(e){notice(e.message);}
    }));
    if(c.run.agent==='codex'&&c.run.workspace)box.append(button('Open workspace in Desktop',async()=>{try{const grant=await executionCall('open',{workerId:localConnection?.workerId,runId:c.run.id});await localCall('open',{runId:c.run.id,proof:grant.openProof});notice('Desktop workspace launch requested. Use the displayed session ID to resume this session.');}catch(e){notice(e.message);}}));
    if(c.run.agent==='claude'&&c.run.sessionId)box.append(el('p','muted','Resume locally: claude --resume '+c.run.sessionId));
    box.append(el('p','muted','Private local logs: runner-state/'+c.run.id+'/events.jsonl'));
  }else box.append(el('p','muted','Idle. This card has never been assigned to a local run.'));
  if(!c.run||c.run.status==='cancelled')box.append(button('Run this queued card',async()=>{try{await executionCall('run',{id:c.id});await executionTick();}catch(e){notice(e.message);}}));
};
document.getElementById('workers').onclick=executionPanel;
renderExecution();
