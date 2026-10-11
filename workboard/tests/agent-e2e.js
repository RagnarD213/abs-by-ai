'use strict';
// Explicit opt-in: harmless real subscription calls, disposable board/workspaces.
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),{randomUUID}=require('node:crypto');
const {initial,mutate}=require('../model'),runs=require('../runs'),{createWorker}=require('../local-worker');
if(process.env.WORKBOARD_AGENT_E2E!=='1')throw new Error('Opt in with WORKBOARD_AGENT_E2E=1.');
const root=path.resolve(process.argv[2]||'/tmp/workboard-agent-e2e-'+Date.now());
const binaries={claude:path.join(process.env.HOME,'.local/bin/claude'),codex:'/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex'};
const worker=createWorker({root,binaries});let board=initial();
runs.transition(board,'enable',{workerId:worker.workerId});
const evidence=[];
for(const agent of ['codex','claude']){
  const source=board.lists[0],dest=board.lists.find(l=>l.tone===agent&&l.name.includes('queue'));
  board=mutate(board,'card.create',{listId:source.id,title:'TEST ONLY '+agent+' harmless worker proof'}).board;
  const id=board.cards.at(-1).id;
  board=mutate(board,'card.update',{id,title:'TEST ONLY '+agent+' harmless worker proof',description:'Create proof.txt in this task workspace containing exactly WORKBOARD_TEST_OK. Read the file back and verify it. Do no other work, do not access external accounts or existing project files. Report the file path and verification.',labels:[],dueDate:''}).board;
  const previous=board;board=mutate(board,'card.move',{id,listId:dest.id,index:0}).board;runs.afterChange(board,previous,'card.move',{id,listId:dest.id});
  const claim=runs.transition(board,'claim',{workerId:worker.workerId,agent}).claim;assert.equal(claim.id,id);
  worker.start(claim);worker.start(claim);
  evidence.push({agent,cardId:id,runId:claim.run.id,claimList:claim.listId});
}
const start=Date.now();
const interval=setInterval(()=>{
  try{
    const local=worker.poll();
    for(const r of local.runs){
      const c=board.cards.find(c=>c.run?.id===r.runId);if(!runs.live.includes(c.run.status))continue;
      runs.transition(board,'update',{workerId:worker.workerId,runId:r.runId,status:r.status,summary:r.summary,...(r.sessionId?{sessionId:r.sessionId}:{}),...(r.workspace?{workspace:r.workspace}:{})});
    }
    if(local.runs.every(r=>!['running','claimed'].includes(r.status))||Date.now()-start>180000){
      clearInterval(interval);
      for(const e of evidence){const c=board.cards.find(c=>c.id===e.cardId);Object.assign(e,{status:c.run.status,summary:c.run.summary,sessionId:c.run.sessionId,workspace:c.run.workspace,reviewList:board.lists.find(l=>l.id===c.listId).name});if(c.run.workspace&&fs.existsSync(path.join(c.run.workspace,'proof.txt')))e.file=fs.readFileSync(path.join(c.run.workspace,'proof.txt'),'utf8');}
      fs.writeFileSync(path.join(root,'evidence.json'),JSON.stringify(evidence,null,2));console.log(JSON.stringify(evidence,null,2));
      for(const e of evidence){assert.equal(e.status,'completed');assert.equal(e.file.trim(),'WORKBOARD_TEST_OK');assert.match(e.reviewList,/review/);assert.ok(e.sessionId);}
      console.log('PASS: both actual subscribed agent starts, harmless local write/read, same-card result, review transition, duplicate start suppression.');
    }
  }catch(e){clearInterval(interval);console.error(e);process.exitCode=1;}
},3000);
