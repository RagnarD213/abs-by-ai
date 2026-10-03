#!/usr/bin/env node
'use strict';
// Private keys are created/read locally and are never emitted or uploaded.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const {signedHeaders,IMAGE_PATH} = require('./web/publication');
function privatePath(file) {
  const absolute = path.resolve(file), parent = path.dirname(absolute);
  const realParent = fs.realpathSync(parent);
  if (parent !== realParent) throw new Error('Symlinked key directory');
  for (let dir=parent;;dir=path.dirname(dir)) {
    if (fs.existsSync(path.join(dir,'.git'))) throw new Error('Key must stay outside Git');
    if (dir === path.dirname(dir)) break;
  }
  const stat = fs.statSync(parent);
  if (stat.uid !== process.getuid() || (stat.mode & 0o077)) throw new Error('Key directory must be private');
  return absolute;
}
function main() {
  const [action,file] = process.argv.slice(2);
  if (!['--create-key','--sign','--sign-image'].includes(action) || !file || process.argv.length !== 4) throw new Error('Invalid signer arguments');
  const target = privatePath(file);
  if (action === '--create-key') {
    const pair = crypto.generateKeyPairSync('ed25519');
    const fd = fs.openSync(target,fs.constants.O_CREAT|fs.constants.O_EXCL|fs.constants.O_WRONLY|fs.constants.O_NOFOLLOW,0o600);
    try { fs.writeFileSync(fd,pair.privateKey.export({type:'pkcs8',format:'pem'})); fs.fsyncSync(fd); }
    finally { fs.closeSync(fd); }
    console.log(JSON.stringify({BRIEF_PUBLISH_PUBLIC_KEY:pair.publicKey.export({type:'spki',format:'der'}).toString('base64')}));
  } else {
    const fd = fs.openSync(target,fs.constants.O_RDONLY|fs.constants.O_NOFOLLOW);
    try {
      const stat = fs.fstatSync(fd);
      if (!stat.isFile() || stat.uid !== process.getuid() || (stat.mode & 0o077) || stat.size > 4096) throw new Error('Private key permissions invalid');
      const key = crypto.createPrivateKey(fs.readFileSync(fd));
      const body = fs.readFileSync(0);
      if (body.length > (action === '--sign-image' ? 8*1024*1024 : 512000)) throw new Error('Publication too large');
      console.log(JSON.stringify(signedHeaders(body,key,Date.now(),undefined,action === '--sign-image' ? IMAGE_PATH : undefined)));
    } finally { fs.closeSync(fd); }
  }
}
if (require.main === module) { try { main(); } catch { console.error('Local signing failed; no key material returned'); process.exitCode=1; } }
module.exports = {privatePath};
