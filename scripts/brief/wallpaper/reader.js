#!/usr/bin/env node
'use strict';
// Invoked every minute by a user LaunchAgent. Outbound HTTPS only, no listener.
const fs=require('fs'),path=require('path'),crypto=require('crypto'),{execFileSync}=require('child_process');
const {choose}=require('./rotation');
const HOME=process.env.HOME,root=path.join(HOME,'Library/Application Support/AbsByAIWallpaper');
const origin='https://absbyai.com',prefix='/api/brief/wallpaper',helper=path.join(__dirname,'mac-helper');
const hash=bytes=>crypto.createHash('sha256').update(bytes).digest('hex');
function native(action,input=''){return JSON.parse(execFileSync(helper,[action],{input,encoding:'utf8',timeout:20000,maxBuffer:32768}));}
function read(file,fallback){try{return JSON.parse(fs.readFileSync(file,'utf8'));}catch(e){if(e.code==='ENOENT')return fallback;throw e;}}
function write(file,value){const temp=file+'.tmp';fs.writeFileSync(temp,JSON.stringify(value),{mode:0o600});fs.renameSync(temp,file);}
async function request(route,method='GET',body=Buffer.alloc(0)) {
 const timestamp=String(Math.floor(Date.now()/1000)),nonce=crypto.randomBytes(16).toString('hex');
 const {publicKey}=native('--public'),id=hash(Buffer.from(publicKey,'base64'));
 const text=['absbyai-wallpaper-v1',method,route,hash(body),timestamp,nonce,id,''].join('\n');
 const signed=native('--sign',text);
 if(signed.keyId!==id)throw Error('Reader key changed');
 const response=await fetch(origin+route,{method,body:method==='POST'?body:undefined,redirect:'error',signal:AbortSignal.timeout(20000),headers:{'X-Wallpaper-Key-Id':id,'X-Wallpaper-Timestamp':timestamp,'X-Wallpaper-Nonce':nonce,'X-Wallpaper-Signature':signed.signature,...(method==='POST'?{'Content-Type':'application/json'}:{})}});
 if(!response.ok)throw Error('Private sync HTTP '+response.status);
 return response;
}
async function main() {
 if(fs.existsSync(path.join(root,'disabled')))return;
 fs.mkdirSync(root,{recursive:true,mode:0o700});fs.chmodSync(root,0o700);
 const lock=path.join(root,'run.lock');let fd;
 try {fd=fs.openSync(lock,'wx',0o600);}catch(e){
  if(e.code!=='EEXIST')throw e;
  const pid=Number(fs.readFileSync(lock,'utf8'));
  if(Number.isSafeInteger(pid)&&pid>0){try{process.kill(pid,0);return;}catch(error){if(error.code!=='ESRCH')return;}}else return;
  fs.unlinkSync(lock);fd=fs.openSync(lock,'wx',0o600);
 }
 fs.writeFileSync(fd,String(process.pid));
 try {
  const cache=path.join(root,'originals');fs.mkdirSync(cache,{mode:0o700,recursive:true});
  const stateFile=path.join(root,'state.json'),manifestFile=path.join(root,'manifest.json');
  const state=read(stateFile,{displays:{}});let manifest=read(manifestFile,null),online=false;
  try {
   const candidate=await (await request(prefix+'/manifest')).json();
   if(!/^[a-f0-9]{64}$/.test(candidate.version)||candidate.rotationIntervalSeconds!==1800||!Array.isArray(candidate.rows))throw Error('Invalid manifest');
   for(const row of candidate.rows) {
    if(!/^[a-f0-9]{64}$/.test(row.sha256)||!['image/png','image/jpeg'].includes(row.mime)||!Number.isInteger(row.sizeBytes)||row.sizeBytes<1||row.sizeBytes>8*1024*1024)throw Error('Invalid original metadata');
    const file=path.join(cache,row.sha256+(row.mime==='image/png'?'.png':'.jpg'));
    if(fs.existsSync(file)&&hash(fs.readFileSync(file))===row.sha256)continue;
    const response=await request(prefix+'/'+row.sha256+'/image');
    if(Number(response.headers.get('content-length'))>8*1024*1024)throw Error('Original too large');
    const chunks=[];let length=0;
    for await(const chunk of response.body){length+=chunk.length;if(length>8*1024*1024)throw Error('Original too large');chunks.push(chunk);}
    const bytes=Buffer.concat(chunks);
    if(bytes.length!==row.sizeBytes||hash(bytes)!==row.sha256)throw Error('Original digest mismatch');
    fs.writeFileSync(file+'.tmp',bytes,{mode:0o600});fs.renameSync(file+'.tmp',file);
   }
   manifest=candidate;write(manifestFile,manifest);online=true;
  }catch(e){console.error(e.message);}
  if(!manifest)return;
  const rows=manifest.rows,files=Object.fromEntries(rows.map(r=>[r.sha256,path.join(cache,r.sha256+(r.mime==='image/png'?'.png':'.jpg'))]));
  const available=rows.filter(r=>fs.existsSync(files[r.sha256])&&hash(fs.readFileSync(files[r.sha256]))===r.sha256).map(r=>r.sha256);
  let observed=native('--inspect');if(observed.length!==3)throw Error('Waiting for all three Mac displays');
  // Manual changes or a reconnected screen get a fresh, verified assignment.
  for(const display of observed)if(display.path!==files[state.displays[display.id]?.sha256])delete state.displays[display.id];
  const plan=choose(available,observed.map(d=>d.id),state.displays,Date.now());
  if(plan.length){observed=native('--apply',JSON.stringify(plan.map(p=>({id:p.id,path:files[p.sha256]}))));for(const entry of plan)state.displays[entry.id]=entry;write(stateFile,state);}
  if(online&&rows.length&&available.length===rows.length) {
   const displays=observed.map(d=>({id:d.id,sha256:state.displays[d.id]?.sha256}));
   if(displays.some(d=>!available.includes(d.sha256)||observed.find(o=>o.id===d.id).path!==files[d.sha256]))throw Error('Mac readback incomplete');
   await request(prefix+'/receipt','POST',Buffer.from(JSON.stringify({version:manifest.version,rotationIntervalSeconds:1800,displays})));
   console.log('Private favorites synced; three Mac wallpapers verified.');
  }
 }finally{fs.closeSync(fd);fs.unlinkSync(lock);}
}
main().catch(e=>{console.error(e.message);process.exitCode=1;});
