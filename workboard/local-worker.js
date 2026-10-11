'use strict';
const http=require('node:http'),fs=require('node:fs'),path=require('node:path'),{spawn}=require('node:child_process'),{randomUUID}=require('node:crypto');
const {agents}=require('./runs');
const origin='https://absbyai.com',port=8843;
function createWorker({root,binaries,now=Date.now,launch=spawn}){
  fs.mkdirSync(root,{recursive:true,mode:0o700});
  root=fs.realpathSync(root);const repository=fs.realpathSync(path.join(__dirname,'..'));
  if(root===repository||root.startsWith(repository+path.sep))throw new Error('Runner state must be outside the web repository, which is served publicly.');
  fs.chmodSync(root,0o700);
  const identity=path.join(root,'worker-id');if(!fs.existsSync(identity))fs.writeFileSync(identity,randomUUID(),{mode:0o600});
  const workerId=fs.readFileSync(identity,'utf8').trim();let lastPoll=0;
  function entries(){return fs.readdirSync(root).filter(x=>/^[a-f0-9-]{36}$/.test(x)&&fs.existsSync(path.join(root,x,'claim.json')));}
  function snapshot(){return {workerId,agents,connected:now()-lastPoll<35000,runs:entries().map(id=>{
    const dir=path.join(root,id),claim=JSON.parse(fs.readFileSync(path.join(dir,'claim.json')));
    let result=null,progress=null;try{result=JSON.parse(fs.readFileSync(path.join(dir,'result.json')));}catch{}try{progress=JSON.parse(fs.readFileSync(path.join(dir,'progress.json')));}catch{}
    return {runId:id,agent:claim.card.run.agent,...progress,...result,status:result?.status||'running',summary:result?.summary||progress?.summary||'Agent starting.',logPath:path.join(dir,'events.jsonl')};
  })};}
  function start(card){
    if(!card?.run||!agents.includes(card.run.agent)||!/^[-a-f0-9]{36}$/.test(card.run.id)||card.run.status!=='claimed'||card.run.workerId!==workerId)throw new Error('Invalid claim.');
    const dir=path.join(root,card.run.id);
    if(fs.existsSync(dir))return snapshot(); // Never spawn an existing claim twice.
    if(snapshot().runs.some(r=>r.agent===card.run.agent&&!['completed','failed','blocked','stopped'].includes(r.status)))throw new Error('Agent is already active.');
    let workspace=null;
    if(card.run.previous){
      const prior=snapshot().runs.find(r=>r.runId===card.run.previous.id);
      if(!prior||!['completed','failed','blocked','stopped'].includes(prior.status))throw new Error('Inspect and stop the previous local session before continuing.');
      // Workspace paths from the website are never authority for local access.
      workspace=prior.workspace||null;
    }
    fs.mkdirSync(dir,{mode:0o700});
    fs.writeFileSync(path.join(dir,'claim.json'),JSON.stringify({card,binaries,workspace,startedAt:now()}),{mode:0o600});
    fs.writeFileSync(path.join(dir,'heartbeat'),'');
    // Durable intent is written before spawn. A crash in this gap blocks the
    // claim instead of repeating execution on restart.
    const child=launch(process.execPath,[path.join(__dirname,'local-agent.js'),dir],{detached:true,stdio:'ignore'});child.unref();
    child.on('error',()=>fs.writeFileSync(path.join(dir,'result.json'),JSON.stringify({status:'failed',summary:'Supervisor launch failed. No automatic retry.'})));
    return snapshot();
  }
  function poll(stop=[]){lastPoll=now();for(const id of entries()){
    const dir=path.join(root,id);
    if(stop.includes(id))fs.writeFileSync(path.join(dir,'stop'),'');
    if(!fs.existsSync(path.join(dir,'result.json'))){
      const claim=JSON.parse(fs.readFileSync(path.join(dir,'claim.json')));
      let processAlive=true;
      if(fs.existsSync(path.join(dir,'process.json'))){try{const processInfo=JSON.parse(fs.readFileSync(path.join(dir,'process.json')));process.kill(processInfo.supervisor,0);}catch{processAlive=false;}}
      if(!processAlive||(!fs.existsSync(path.join(dir,'process.json'))&&now()-claim.startedAt>15000))fs.writeFileSync(path.join(dir,'result.json'),JSON.stringify({status:'blocked',summary:'Start or supervisor was interrupted. This claim will never be spawned again automatically.'}));
      else fs.utimesSync(path.join(dir,'heartbeat'),new Date(),new Date());
    }
  }return snapshot();}
  function handler(req,res){
    res.setHeader('Cache-Control','no-store');res.setHeader('Content-Type','application/json');
    if(req.headers.host!==`127.0.0.1:${port}`||req.headers.origin!==origin){res.writeHead(403);res.end('{"error":"Only the private workboard may connect."}');return;}
    res.setHeader('Access-Control-Allow-Origin',origin);res.setHeader('Vary','Origin');res.setHeader('Access-Control-Allow-Private-Network','true');
    if(req.method==='OPTIONS'){res.setHeader('Access-Control-Allow-Methods','POST');res.setHeader('Access-Control-Allow-Headers','Content-Type,X-Workboard-Local');res.writeHead(204);res.end();return;}
    if(req.method!=='POST'||req.headers['x-workboard-local']!=='owner-tab'){res.writeHead(403);res.end('{"error":"Invalid local request."}');return;}
    let body='';req.on('data',chunk=>{body+=chunk;if(body.length>131072)req.destroy();});req.on('end',()=>{try{
      const p=JSON.parse(body||'{}');let result;
      if(req.url==='/poll')result=poll(p.stop);
      else if(req.url==='/start')result=start(p.card);
      else if(req.url==='/open'){
        const run=snapshot().runs.find(r=>r.runId===p.runId);if(!run||!run.workspace)throw new Error('Session unavailable.');
        // Only a documented workspace launch is supported. No guessed deep link.
        if(run.agent!=='codex')throw new Error('Claude CLI does not expose a verified Desktop session-open API. Use claude --resume with the session ID.');
        const child=launch(binaries.codex,['app',run.workspace],{stdio:'ignore'});child.on('error',()=>{});result={openedWorkspace:true};
      }else throw new Error('Unknown local action.');
      res.end(JSON.stringify(result));
    }catch(e){res.writeHead(409);res.end(JSON.stringify({error:e.message}));}});
  }
  return {workerId,start,poll,snapshot,handler};
}
if(require.main===module){
  const root=process.argv[2];if(!root||!path.isAbsolute(root)){console.error('Usage: node workboard/local-worker.js /absolute/private/runner-state');process.exit(1);}
  const binaries={claude:process.env.WORKBOARD_CLAUDE||path.join(process.env.HOME,'.local/bin/claude'),codex:process.env.WORKBOARD_CODEX||'/Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex'};
  for(const binary of Object.values(binaries))if(!fs.existsSync(binary)){console.error('An installed agent CLI is missing. Configure WORKBOARD_CLAUDE or WORKBOARD_CODEX.');process.exit(1);}
  const worker=createWorker({root,binaries});http.createServer(worker.handler).listen(port,'127.0.0.1',()=>console.log('Local workboard worker listening at 127.0.0.1:8843. Open the private board and Connect. No task starts until Enable and a new assignment.'));
}
module.exports={createWorker,origin,port};
