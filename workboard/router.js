'use strict';
const express=require('express'),path=require('node:path'),{randomUUID}=require('node:crypto');
const {COOKIE,cookie}=require('../scripts/brief/web/router');
const {BoardError}=require('./model');
const MAX=8*1024*1024;
function attachment(bytes,mime,name){
  if(!Buffer.isBuffer(bytes)||!bytes.length||bytes.length>MAX)throw new BoardError('Files must be between 1 byte and 8 MB.');
  if(typeof name!=='string'||!name.trim()||name.length>180||/[\x00-\x1f/\\]/.test(name))throw new BoardError('Invalid filename.');
  const ext=name.split('.').pop().toLowerCase();
  const valid=(mime==='image/png'&&ext==='png'&&bytes.length>24&&bytes.subarray(0,8).equals(Buffer.from([137,80,78,71,13,10,26,10])))||
    (mime==='image/jpeg'&&['jpg','jpeg'].includes(ext)&&bytes[0]===255&&bytes[1]===216&&bytes[bytes.length-2]===255&&bytes[bytes.length-1]===217)||
    (mime==='application/pdf'&&ext==='pdf'&&bytes.subarray(0,5).toString()==='%PDF-')||
    (mime==='text/plain'&&['txt','md','csv','srt'].includes(ext)&&!bytes.includes(0)&&Buffer.from(bytes.toString('utf8'),'utf8').equals(bytes));
  if(!valid)throw new BoardError('Supported files: PNG, JPG, PDF, TXT, MD, CSV and SRT. The file contents must match its type.');
  return {id:randomUUID(),bytes,mime,name:name.trim(),size:bytes.length};
}
function createRouter({store,ownerStore,env=process.env,origin='https://absbyai.com',now=Date.now}){
  const router=express.Router();
  router.use((req,res,next)=>{
    const p=req.path.toLowerCase().replace(/\/+$/,'');
    if(!['/workboard','/workboard-login'].includes(p)&&!p.startsWith('/api/workboard/'))return next('router');
    req.url=p+(req.url.includes('?')?req.url.slice(req.url.indexOf('?')):'');
    res.removeHeader('Access-Control-Allow-Origin');
    res.set({'Cache-Control':'private, no-store','Pragma':'no-cache','X-Content-Type-Options':'nosniff','Referrer-Policy':'no-referrer','Content-Security-Policy':"default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self' blob:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'"});next();
  });
  router.get('/workboard-login',(req,res)=>res.sendFile(path.join(__dirname,'login.html')));
  router.use(async(req,res,next)=>{
    if(!env.BRIEF_OWNER_EMAIL||!env.BRIEF_GOOGLE_CLIENT_ID)return res.status(503).json({error:'Existing private Google sign-in is not configured.'});
    try{
      const token=cookie(req,COOKIE);
      if(!/^[a-f0-9]{64}$/.test(token))return deny();
      const [session,pin]=await Promise.all([ownerStore.session(token),ownerStore.owner()]);
      const expires=new Date(session?.expires_at).getTime();
      if(!session||!pin||pin.email!==env.BRIEF_OWNER_EMAIL.toLowerCase()||pin.google_sub!==session.google_sub||(env.BRIEF_OWNER_GOOGLE_SUB&&pin.google_sub!==env.BRIEF_OWNER_GOOGLE_SUB)||!Number.isFinite(expires)||expires<=now())return deny();
      next();
    }catch{res.status(503).json({error:'Private session check unavailable. Please retry.'});}
    function deny(){return req.path.startsWith('/api/')?res.status(401).json({error:'Sign in with the existing owner account.'}):res.redirect(303,'/workboard-login');}
  });
  const file=name=>(req,res)=>res.sendFile(path.join(__dirname,name));
  router.get('/workboard',file('page.html'));
  for(const name of ['page.js','baseline.css','style.css'])router.get('/api/workboard/'+name,file(name));
  const run=fn=>async(req,res)=>{try{await fn(req,res);}catch(e){res.status(e.status||503).json({error:e instanceof BoardError?e.message:'Could not save or load the board. Please retry.'});}};
  router.get('/api/workboard/state',run(async(req,res)=>res.json(await store.read())));
  router.get('/api/workboard/files/:id',run(async(req,res)=>{
    const f=await store.file(req.params.id);if(!f)return res.sendStatus(404);
    res.set({'Content-Type':f.mime,'Content-Disposition':`attachment; filename="download.${f.name.split('.').pop().replace(/[^a-zA-Z0-9]/g,'')}"; filename*=UTF-8''${encodeURIComponent(f.name).replace(/'/g,'%27')}`});res.send(f.bytes);
  }));
  router.use((req,res,next)=>{
    if(!['POST','PUT','PATCH','DELETE'].includes(req.method))return next();
    if(req.headers.origin!==origin||req.headers['x-workboard-action']!=='change')return res.status(403).json({error:'This action must come from your workboard.'});next();
  });
  router.post('/api/workboard/change',express.json({limit:'64kb'}),run(async(req,res)=>{
    if(!req.body||typeof req.body!=='object'||Array.isArray(req.body)||!req.body.payload||typeof req.body.payload!=='object'||Array.isArray(req.body.payload))throw new BoardError('Invalid board change.');
    res.json(await store.change(req.body.version,req.body.action,req.body.payload));
  }));
  router.post('/api/workboard/cards/:id/attachments',express.raw({type:()=>true,limit:MAX}),run(async(req,res)=>{
    let name;try{name=decodeURIComponent(req.headers['x-file-name']||'');}catch{throw new BoardError('Invalid filename.');}
    const f=attachment(req.body,(req.headers['content-type']||'').split(';')[0],name);
    const raw=req.headers['x-board-version'];if(!/^\d+$/.test(raw||''))throw new BoardError('Board version is required.');
    res.json(await store.change(Number(raw),'attachment.add',{id:req.params.id},f));
  }));
  router.use((err,req,res,next)=>res.status(err.type==='entity.too.large'?413:400).json({error:err.type==='entity.too.large'?'This request is too large. Files may be up to 8 MB.':'Invalid request body.'}));
  router.use((req,res)=>res.sendStatus(404));
  return router;
}
module.exports={createRouter,attachment,MAX};
