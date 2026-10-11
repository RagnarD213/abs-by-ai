'use strict';
// Read-only scheduled-chat helper. Never writes records or accepts payment actions.
const fs=require('node:fs'),{unpaid}=require('./assistant');
async function main(){
 let token=process.env.GITHUB_TOKEN;
 if(process.argv[2]==='--env-file'){
  const source=fs.readFileSync(process.argv[3],'utf8');
  const line=source.split(/\r?\n/).find(x=>/^(?:export )?GITHUB_TOKEN=/.test(x));
  if(line){token=line.replace(/^(?:export )?GITHUB_TOKEN=/,'').trim();if(/^(["']).*\1$/.test(token))token=token.slice(1,-1);}
 }
 if(!token)throw new Error('Existing GitHub read credential unavailable');
 const fetch=require('node-fetch');
 const r=await fetch('https://api.github.com/repos/RagnarD213/abs-by-ai/contents/timesheet.json?ref=main',{headers:{Authorization:`Bearer ${token}`,Accept:'application/vnd.github.v3+json','Cache-Control':'no-cache'},timeout:20000});
 if(!r.ok)throw new Error(`Authoritative timesheet read failed (${r.status})`);
 const m=await r.json(),data=JSON.parse(Buffer.from(m.content,'base64').toString('utf8'));
 console.log(JSON.stringify({...unpaid(data),source:'RagnarD213/abs-by-ai:main/timesheet.json',sourceRevision:m.sha},null,2));
}
if(require.main===module)main().catch(()=>{console.error('Unpaid balance unavailable. Retry the read; do not interpret this as paid or zero.');process.exitCode=1;});
module.exports={main};
