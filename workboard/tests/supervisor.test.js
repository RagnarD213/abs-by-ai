'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),os=require('node:os'),path=require('node:path'),http=require('node:http'),{randomUUID}=require('node:crypto');
const {createWorker,origin}=require('../local-worker');
const delay=ms=>new Promise(r=>setTimeout(r,ms));
async function main(){
 const root=fs.mkdtempSync(path.join(os.tmpdir(),'workboard-supervisor-')),fake=path.join(root,'fake-agent');
 fs.writeFileSync(fake,'#!'+process.execPath+'\nlet s="";process.stdin.on("data",x=>s+=x);process.stdin.on("end",()=>{if(s.includes("TEST HANG")){setInterval(()=>{},1000);return;}console.log(JSON.stringify({type:"result",session_id:"test-session",permission_denials:[{tool_name:"Bash"}],structured_output:{status:"completed",summary:"Must not be accepted."}}));});\n',{mode:0o700});
 const proof=require('../claim-proof'),claimKey='synthetic-existing-secret-123';
 const worker=createWorker({root,claimKey,binaries:{claude:fake,codex:fake}}),server=http.createServer(worker.handler);await new Promise(r=>server.listen(0,'127.0.0.1',r));
 try{
  const url='http://127.0.0.1:'+server.address().port+'/hello';
  const request=headers=>new Promise((resolve,reject)=>{const req=http.request(url,{method:'POST',headers},res=>{res.resume();res.on('end',()=>resolve({status:res.statusCode}));});req.on('error',reject);req.end('{}');});
  for(const headers of [{Host:'127.0.0.1:8843',Origin:'https://evil.example'},{Host:'evil.example:8843',Origin:origin}])assert.equal((await request(headers)).status,403);
  const good={Host:'127.0.0.1:8843',Origin:origin,'X-Workboard-Local':'owner-tab','Content-Type':'application/json'};assert.equal((await request(good)).status,200);
  function signed(c){return proof.sign(claimKey,'start',{workerId:worker.workerId,runId:c.run.id,cardDigest:proof.digest(c)});}
  function poll(){return worker.poll(proof.sign(claimKey,'poll',{workerId:worker.workerId,active:worker.snapshot().runs.filter(r=>r.status==='running').map(r=>r.runId)}));}
  function card(title){return {id:randomUUID(),title,description:'Synthetic supervisor test only.',checklist:[],attachments:[],run:{id:randomUUID(),status:'claimed',agent:'claude',workerId:worker.workerId}};}
  const denied=card('TEST DENIAL');worker.start(denied,signed(denied));worker.start(denied,signed(denied));
  let outcome;for(let i=0;i<50;i++){outcome=poll().runs.find(r=>r.runId===denied.run.id);if(outcome.status!=='running')break;await delay(100);}
  assert.equal(outcome.status,'blocked');assert.match(outcome.summary,/denied/);
  const hanging=card('TEST HANG');worker.start(hanging,signed(hanging));
  const dir=path.join(root,hanging.run.id);for(let i=0;i<50&&!fs.existsSync(path.join(dir,'process.json'));i++)await delay(100);
  const processInfo=JSON.parse(fs.readFileSync(path.join(dir,'process.json')));fs.utimesSync(path.join(dir,'heartbeat'),new Date(Date.now()-60000),new Date(Date.now()-60000));
  for(let i=0;i<70;i++){try{outcome=JSON.parse(fs.readFileSync(path.join(dir,'result.json')));break;}catch{}await delay(100);}
  assert.equal(outcome.status,'blocked');assert.match(outcome.summary,/connection lost/i);assert.throws(()=>process.kill(processInfo.pid,0));
  const restarted=createWorker({root,claimKey,binaries:{claude:fake,codex:fake}});restarted.start(hanging,signed(hanging));assert.equal(restarted.snapshot().runs.find(r=>r.runId===hanging.run.id).status,'blocked');
  console.log('PASS: loopback Host/Origin boundary; observed denial cannot complete; heartbeat loss terminates real child; restart and duplicate requests never relaunch.');
 }finally{await new Promise(r=>server.close(r));}
}
main().catch(e=>{console.error(e);process.exitCode=1;});
