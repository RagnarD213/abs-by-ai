'use strict';
const {randomUUID}=require('node:crypto');
const {BoardError}=require('./model');
const agents=['claude','codex'], live=['claimed','running','stopping'];
const staleMs=90000;
function config(board){
  if(!board.execution)board.execution={enabled:false,paused:true,activatedAt:null,workerId:null,heartbeatAt:null};
  return board.execution;
}
function lists(board,agent){
  const find=phase=>board.lists.filter(l=>!l.archived&&l.tone===agent&&l.name.toLowerCase().includes(phase));
  const queue=find('queue'),progress=find('in progress'),review=find('in review');
  if(queue.length!==1||progress.length!==1||review.length!==1)throw new BoardError(`Restore one ${agent} queue, in progress and review list before running tasks.`);
  return {queue:queue[0],progress:progress[0],review:review[0]};
}
function assign(board,c,agent,now=Date.now()){
  const e=config(board);if(!e.enabled)return;
  if(c.run&&live.includes(c.run.status))throw new BoardError('Stop the active run before assigning this card again.');
  // Only a deliberate movement into a queue or explicit Run invokes this.
  c.run={id:randomUUID(),agent,status:'queued',assignedAt:new Date(now).toISOString(),summary:'Waiting for the local worker. No execution has started.'};
}
function afterChange(board,previous,action,p,now=Date.now()){
  config(board);
  if(action!=='card.move'&&action!=='card.archive'&&action!=='list.archive')return;
  const prior=previous.cards.find(c=>c.id===p.id),c=board.cards.find(c=>c.id===p.id);
  if(prior?.run&&live.includes(prior.run.status))throw new BoardError('Stop the active run before moving or archiving this card.');
  if(action==='list.archive'&&board.cards.some(c=>c.listId===p.id&&c.run&&live.includes(c.run.status)))throw new BoardError('Stop active runs before archiving their list.');
  if(action==='card.move'&&c&&prior.listId!==c.listId){
    if(c.run?.status==='queued')c.run.status='cancelled';
    const dest=board.lists.find(l=>l.id===c.listId);
    if(agents.includes(dest.tone)&&dest.name.toLowerCase().includes('queue')){
      // Movement is not a retry authorization for a task that already ran.
      // Preserve its prior result until the owner explicitly inspects/continues.
      if(!c.run||c.run.status==='cancelled')assign(board,c,dest.tone,now);
    }
  }
  if(action==='card.archive'&&c?.run?.status==='queued')c.run.status='cancelled';
}
function expire(board,now){
  for(const c of board.cards)if(c.run&&live.includes(c.run.status)&&now-Date.parse(c.run.heartbeatAt)>staleMs){
    c.run.status='blocked';c.run.finishedAt=new Date(now).toISOString();c.run.summary='Worker connection lost. Execution may have made changes. Inspect the local session before explicitly continuing. This run will not restart automatically.';
  }
}
function safe(value,max=4000){
  if(typeof value!=='string'||value.length>max)throw new BoardError('Invalid run summary.');
  return value.replace(/(?:sk-[A-Za-z0-9_-]{12,}|gh[pousr]_[A-Za-z0-9_]{15,}|(?:Bearer|token|password|api[_-]?key|secret)\s*[:=]\s*[^\s]+)/gi,'[redacted]').trim();
}
function transition(board,action,p={},now=Date.now()){
  const e=config(board),at=new Date(now).toISOString();expire(board,now);
  let result={};
  if(action==='enable'){
    if(typeof p.workerId!=='string'||!/^[-a-zA-Z0-9]{1,80}$/.test(p.workerId))throw new BoardError('Connect the local worker first.');
    for(const a of agents)lists(board,a);
    if(board.cards.some(c=>c.run&&live.includes(c.run.status))&&e.workerId!==p.workerId)throw new BoardError('Stop active runs before connecting a different worker.');
    for(const c of board.cards)if(c.run?.status==='queued'){c.run.status='cancelled';c.run.summary='Earlier queued assignment is idle after activation. Use Run to deliberately assign it again.';}
    // Activation never scans or arms existing cards.
    e.enabled=true;e.paused=false;e.activatedAt=at;e.workerId=p.workerId;e.heartbeatAt=at;
  }else if(action==='resume'){
    if(!e.enabled||p.workerId!==e.workerId)throw new BoardError('Reconnect and enable this worker first.');e.paused=false;
  }else if(action==='pause')e.paused=true;
  else if(action==='disable'){e.enabled=false;e.paused=true;for(const c of board.cards)if(c.run){if(live.includes(c.run.status))c.run.status='stopping';else if(c.run.status==='queued')c.run.status='cancelled';}}
  else if(action==='run'||action==='continue'){
    const c=board.cards.find(c=>c.id===p.id);if(!c||c.archived)throw new BoardError('Card unavailable.');
    if(c.run&&live.includes(c.run.status))throw new BoardError('This card already has an active run.');
    if(c.run?.status==='queued')throw new BoardError('This card is already queued.');
    const agent=c.run?.agent||board.lists.find(l=>l.id===c.listId)?.tone;
    if(!agents.includes(agent))throw new BoardError('Move the card to an agent queue first.');
    const previous=c.run?structuredClone(c.run):null;
    if(previous&&previous.status!=='cancelled'&&action!=='continue')throw new BoardError('Use Continue after inspecting earlier changes.');
    if(!e.enabled||e.paused)throw new BoardError('Connect and enable the worker first.');
    c.listId=lists(board,agent).queue.id;
    assign(board,c,agent,now);
    if(previous){c.run.previous={id:previous.id,status:previous.status,summary:previous.summary,sessionId:previous.sessionId||null,workspace:previous.workspace||null};c.run.summary='Explicit continuation queued. Inspecting previous changes before continuing.';}
  }else if(action==='stop'){
    const c=board.cards.find(c=>c.id===p.id);if(!c?.run)throw new BoardError('No run to stop.');
    if(c.run.status==='queued'){c.run.status='cancelled';c.run.summary='Cancelled before execution.';}
    else if(live.includes(c.run.status)){c.run.status='stopping';c.run.summary='Stop requested. Waiting for local process termination.';}
  }else{
    if(p.workerId!==e.workerId)throw new BoardError('A different worker is connected.',409);
    e.heartbeatAt=at;
    if(action==='claim'){
      if(!agents.includes(p.agent))throw new BoardError('Unknown agent.');
      if(e.enabled&&!e.paused&&!board.cards.some(c=>c.run?.agent===p.agent&&live.includes(c.run.status))){
        const route=lists(board,p.agent);
        const c=board.cards.find(c=>!c.archived&&c.listId===route.queue.id&&c.run?.status==='queued'&&c.run.agent===p.agent);
        if(c){c.run.status='claimed';c.run.workerId=p.workerId;c.run.heartbeatAt=at;c.run.startedAt=at;c.run.summary='Claimed by the local worker. Starting agent.';c.listId=route.progress.id;result.claim=structuredClone(c);}
      }
    }else if(action==='update'){
      const c=board.cards.find(c=>c.run?.id===p.runId);if(!c||c.run.workerId!==p.workerId)throw new BoardError('Run claim no longer belongs to this worker.',409);
      const r=c.run;
      if(!live.includes(r.status)){result.status=r.status;return result;}
      r.heartbeatAt=at;
      if(p.sessionId!==undefined){if(typeof p.sessionId!=='string'||!/^[-a-zA-Z0-9]{1,100}$/.test(p.sessionId))throw new BoardError('Invalid session.');r.sessionId=p.sessionId;}
      if(p.workspace!==undefined)r.workspace=safe(p.workspace,1000);
      if(p.summary!==undefined)r.summary=safe(p.summary);
      if(p.status==='running'&&r.status!=='stopping')r.status='running';
      if(['completed','blocked','failed','stopped'].includes(p.status)){
        const stopped=r.status==='stopping';r.status=stopped?'stopped':p.status;r.finishedAt=at;
        if(r.status==='completed')c.listId=lists(board,r.agent).review.id;
        board.activity.unshift({id:randomUUID(),at,text:`${r.agent} run ${r.status}: ${c.title}`,cardId:c.id});board.activity=board.activity.slice(0,500);
      }
      result.status=r.status;
    }else if(action!=='heartbeat')throw new BoardError('Unknown execution action.');
  }
  result.stop=board.cards.filter(c=>c.run&&c.run.workerId===p.workerId&&c.run.status==='stopping').map(c=>c.run.id);
  return result;
}
module.exports={config,afterChange,transition,expire,live,agents,safe};
