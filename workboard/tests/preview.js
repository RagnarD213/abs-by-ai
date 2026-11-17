'use strict';
// Disposable local fixture. No production credentials, calls, tasks or payments.
const express=require('express'),{fixture,env,token}=require('./api.test'),{createRouter}=require('../router'),{createAssistant}=require('../assistant'),{propose}=require('../plan-day'),fs=require('node:fs');
(async()=>{const f=await fixture();
 if(process.env.WORKBOARD_PREVIEW_PLAN)await propose(f.store,JSON.parse(fs.readFileSync(process.env.WORKBOARD_PREVIEW_PLAN,'utf8')));
 let files={'todos.json':{assistant:[{text:'QA: Shared assistant task',priority:'high'}]},'task-checks.json':{checked:[],log:{},checkedAt:{}},'timesheet.json':{active:null,entries:[],payments:[]}},revision=1;
 const assistant=createAssistant({read:async n=>({data:structuredClone(files[n]),sha:String(revision)}),write:async(n,d)=>{files[n]=d;revision++;},lock:fn=>fn()});
 if(process.env.WORKBOARD_PREVIEW_IMAGE)f.ownerStore.favoriteManifest=async()=>({rows:[{sha256:'fixture'}]});
 const app=express();app.get('/api/brief/favorites/fixture/image',(req,res)=>res.sendFile(process.env.WORKBOARD_PREVIEW_IMAGE));app.use((req,res,next)=>{req.headers.cookie='__Host-absbyai_brief='+token;next();});app.use(createRouter({...f,env,assistant,origin:'http://127.0.0.1:8842'}));app.listen(8842,'127.0.0.1',()=>console.log('Local QA fixture only: http://127.0.0.1:8842/dash?date=2026-11-17'));
})().catch(e=>{console.error(e);process.exitCode=1;});
