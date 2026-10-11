'use strict';
const {createHmac,timingSafeEqual,createHash}=require('node:crypto');
const digest=card=>createHash('sha256').update(JSON.stringify(card)).digest('hex');
function sign(key,kind,data,now=Date.now()){
  if(typeof key!=='string'||key.length<16)throw new Error('Existing workboard signing secret unavailable.');
  const grant={kind,...data,expiresAt:now+30000};
  return {grant,signature:createHmac('sha256',key).update('absbyai-local-worker-v1\n'+JSON.stringify(grant)).digest('hex')};
}
function verify(key,proof,kind,workerId,now=Date.now()){
  if(typeof key!=='string'||key.length<16||!proof?.grant||proof.grant.kind!==kind||proof.grant.workerId!==workerId||!Number.isFinite(proof.grant.expiresAt)||proof.grant.expiresAt<now||proof.grant.expiresAt>now+45000||!/^([a-f0-9]{64})$/.test(proof.signature||''))throw new Error('A fresh authenticated board grant is required.');
  const expected=createHmac('sha256',key).update('absbyai-local-worker-v1\n'+JSON.stringify(proof.grant)).digest();
  if(!timingSafeEqual(expected,Buffer.from(proof.signature,'hex')))throw new Error('Invalid authenticated board grant.');
  return proof.grant;
}
module.exports={sign,verify,digest};
