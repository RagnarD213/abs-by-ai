'use strict';
// Explicit local QA only. Synthetic owner and in-memory data never reach production.
const express=require('express'),{fixture,env,token}=require('./api.test'),{createRouter}=require('../router');
(async()=>{const f=await fixture(),app=express();app.use((req,res,next)=>{req.headers.cookie='__Host-absbyai_brief='+token;next();});app.use(createRouter({...f,env,origin:'http://127.0.0.1:8842'}));app.listen(8842,'127.0.0.1',()=>console.log('Local QA fixture only: http://127.0.0.1:8842/dash'));})().catch(e=>{console.error(e);process.exitCode=1;});
