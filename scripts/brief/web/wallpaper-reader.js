'use strict';
// A separate, revocable machine key can read only active favorites and acknowledge
// Mac integration. It has no brief, publisher, account, or product-data access.
const crypto=require('crypto'),express=require('express');
const {publicKey,keyId,digest}=require('./publication');
const PREFIX='/api/brief/wallpaper';
const canonical=(method,path,body,timestamp,nonce,id)=>Buffer.from(['absbyai-wallpaper-v1',method,path,digest(body),timestamp,nonce,id,''].join('\n'));
function verify(req,key,now) {
 const h=req.headers,t=h['x-wallpaper-timestamp'],n=h['x-wallpaper-nonce'],id=h['x-wallpaper-key-id'],s=h['x-wallpaper-signature'];
 if(typeof t!=='string'||!/^\d{10}$/.test(t)||typeof n!=='string'||!/^[a-f0-9]{32}$/.test(n)||id!==keyId(key)||typeof s!=='string'||!/^[A-Za-z0-9+/]{86}==$/.test(s))throw Error('Unauthorized');
 const age=Math.floor(now/1000)-Number(t),body=req.wallpaperBody||Buffer.alloc(0);
 if(age < -30 || age > 90 || req.headers['content-encoding'] && req.headers['content-encoding']!=='identity' || !crypto.verify(null,canonical(req.method,req.originalUrl,body,t,n,id),key,Buffer.from(s,'base64')))throw Error('Unauthorized');
 return {id:'wallpaper:'+id,nonce:n,expiresAt:(Number(t)+121)*1000};
}
function installWallpaperReader(router,{store,env,now}) {
 const parse=express.json({limit:'4kb',verify:(req,res,bytes)=>{req.wallpaperBody=bytes;}});
 async function machine(req,res,next) {
  let verified;
  try {verified=verify(req,publicKey(env.BRIEF_WALLPAPER_PUBLIC_KEY),now());}catch{return res.sendStatus(401);}
  try {if(!await store.claimPublicationNonce(verified.id,verified.nonce,verified.expiresAt,now()))return res.sendStatus(401);return next();}catch{return res.sendStatus(503);}
 }
 router.get(PREFIX+'/manifest',machine,async(req,res)=>{
  try {const {version,rows,feedbackPolicy}=await store.favoriteManifest();return res.json({version,rows,feedbackPolicy,rotationIntervalSeconds:1800});}catch{return res.sendStatus(503);}
 });
 router.get(PREFIX+'/:id/image',machine,async(req,res)=>{
  if(!/^[a-f0-9]{64}$/.test(req.params.id))return res.sendStatus(400);
  try {const favorite=await store.favorite(req.params.id);if(!favorite?.active)return res.sendStatus(404);
   const image=await store.favoriteBytes(req.params.id);
   if(!image||!['image/png','image/jpeg'].includes(image.mime)||digest(image.bytes)!==req.params.id)return res.sendStatus(503);
   return res.set('X-Brief-Image-SHA256',req.params.id).type(image.mime).send(image.bytes);
  }catch{return res.sendStatus(503);}
 });
 router.post(PREFIX+'/receipt',parse,machine,async(req,res)=>{
  const r=req.body;
  if(!r || Object.keys(r).sort().join(',')!=='displays,rotationIntervalSeconds,version' || !/^[a-f0-9]{64}$/.test(r.version||'') || r.rotationIntervalSeconds!==1800 || !Array.isArray(r.displays)||r.displays.length!==3 || new Set(r.displays.map(d=>d?.id)).size!==3 || r.displays.some(d=>!d||Object.keys(d).sort().join(',')!=='id,sha256'||!/^\d{1,10}$/.test(d.id)||!/^[a-f0-9]{64}$/.test(d.sha256||'')))return res.sendStatus(400);
  try {const manifest=await store.favoriteManifest();if(r.version!==manifest.version || r.displays.some(d=>!manifest.rows.some(f=>f.sha256===d.sha256)))return res.sendStatus(409);
   await store.writeWallpaperReceipt({...r,displayCount:3,checkedAt:new Date(now()).toISOString()});return res.json({ok:true});
  }catch{return res.sendStatus(503);}
 });
}
module.exports={canonical,verify,installWallpaperReader};
