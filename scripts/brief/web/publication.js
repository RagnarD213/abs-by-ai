'use strict';
const crypto = require('crypto');
const PATH = '/api/brief/publish';
const IMAGE_PATH = '/api/brief/image/publish';
const WINDOW = 300;
const digest = body => crypto.createHash('sha256').update(body).digest('hex');
const keyId = key => digest(key.export({type:'spki',format:'der'}));
function canonicalDigest(hash, timestamp, nonce, id, route) {
  if (typeof hash !== 'string' || hash.length !== 64 || !/^[a-f0-9]{64}$/.test(hash)) throw new Error('Invalid body digest');
  return Buffer.from(['absbyai-brief-v1','POST',route,hash,timestamp,nonce,id,''].join('\n'));
}
const canonical = (body, timestamp, nonce, id, route = PATH) => canonicalDigest(digest(body),timestamp,nonce,id,route);
function publicKey(value) {
  if (typeof value !== 'string' || value.length > 128 || !/^[A-Za-z0-9+/]+={0,2}$/.test(value)) throw new Error('Publication key unavailable');
  const der = Buffer.from(value,'base64');
  if (der.toString('base64') !== value) throw new Error('Publication key unavailable');
  const key = crypto.createPublicKey({key:der,type:'spki',format:'der'});
  if (key.asymmetricKeyType !== 'ed25519') throw new Error('Publication key unavailable');
  return key;
}
function signedDigestHeaders(hash, privateKey, now, nonce, route) {
  if (privateKey.asymmetricKeyType !== 'ed25519') throw new Error('Wrong signing key');
  if (![PATH,IMAGE_PATH].includes(route)) throw new Error('Wrong publication route');
  const id = keyId(crypto.createPublicKey(privateKey)), timestamp = String(Math.floor(now / 1000));
  return {'X-Brief-Key-Id':id,'X-Brief-Timestamp':timestamp,'X-Brief-Nonce':nonce,
    'X-Brief-Signature':crypto.sign(null,canonicalDigest(hash,timestamp,nonce,id,route),privateKey).toString('base64')};
}
function signedHeaders(body, privateKey, now = Date.now(), nonce = crypto.randomBytes(16).toString('hex'), route = PATH) {
  return signedDigestHeaders(digest(body),privateKey,now,nonce,route);
}
// Precomputed digests can authorize only the existing image publication route.
function signedImageDigestHeaders(hash, privateKey, now = Date.now(), nonce = crypto.randomBytes(16).toString('hex')) {
  return signedDigestHeaders(hash,privateKey,now,nonce,IMAGE_PATH);
}
function verifyRequest(req, key, now = Date.now()) {
  const type = req.originalUrl === PATH ? /^application\/json(?:\s*;|$)/i : /^image\/(?:png|jpeg)$/;
  if (req.method !== 'POST' || ![PATH,IMAGE_PATH].includes(req.originalUrl) || !Buffer.isBuffer(req.briefRawBody) ||
      !type.test(req.headers['content-type'] || '') ||
      (req.headers['content-encoding'] && req.headers['content-encoding'] !== 'identity')) throw new Error('Invalid publication');
  const h = req.headers, timestamp = h['x-brief-timestamp'], nonce = h['x-brief-nonce'], id = h['x-brief-key-id'], signature = h['x-brief-signature'];
  if (typeof timestamp !== 'string' || !/^\d{10}$/.test(timestamp) || typeof nonce !== 'string' || !/^[a-f0-9]{32}$/.test(nonce) ||
      id !== keyId(key) || typeof signature !== 'string' || !/^[A-Za-z0-9+/]{86}==$/.test(signature)) throw new Error('Invalid publication');
  const age = Math.floor(now / 1000) - Number(timestamp);
  if (age < -30 || age > WINDOW || !crypto.verify(null,canonical(req.briefRawBody,timestamp,nonce,id,req.originalUrl),key,Buffer.from(signature,'base64'))) throw new Error('Invalid publication');
  return {id,nonce,expiresAt:(Number(timestamp)+WINDOW+31)*1000};
}
module.exports = {PATH,IMAGE_PATH,WINDOW,digest,keyId,canonical,publicKey,signedHeaders,signedImageDigestHeaders,verifyRequest};
