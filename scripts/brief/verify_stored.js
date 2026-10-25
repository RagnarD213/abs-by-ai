#!/usr/bin/env node
'use strict';
// Independently read private persisted state without transferring image bytes.
const fs=require('fs'),path=require('path'),assert=require('assert');
const {Client}=require('pg');
const {validate}=require('./web/document');
const [expectedFile,proofFile]=process.argv.slice(2);
function privateFile(file) {
  const absolute=path.resolve(file);
  for(let p=path.dirname(absolute);;p=path.dirname(p)) {
    if(fs.existsSync(path.join(p,'.git')))throw Error('Private file must be outside Git');
    if(p===path.dirname(p))break;
  }
  return absolute;
}
async function main() {
  if(!expectedFile||!proofFile)throw Error('Usage: verify_stored.js <edition.json or --capture> <private proof.json>');
  const output=privateFile(proofFile),settings={};
  for(const line of fs.readFileSync(path.join(require('os').homedir(),'.absbyai-secrets.env'),'utf8').split('\n')) {
    const m=line.match(/^\s*(DATABASE_PUBLIC_URL|DATABASE_URL)=(.*)$/);
    if(m)settings[m[1]]=m[2].trim().replace(/^(['"])(.*)\1$/,'$2');
  }
  const client=new Client({connectionString:settings.DATABASE_PUBLIC_URL||settings.DATABASE_URL,ssl:{rejectUnauthorized:false},connectionTimeoutMillis:10000});
  try {
    await client.connect();await client.query('BEGIN READ ONLY');await client.query('SET LOCAL statement_timeout=10000');
    const document=(await client.query('SELECT document FROM brief_document WHERE id=1')).rows[0].document;
    const image=(await client.query("SELECT mime,octet_length(bytes) AS size_bytes,encode(sha256(bytes),'hex') AS sha256 FROM brief_image WHERE id=1")).rows[0];
    if(expectedFile!=='--capture') {
      const expected=validate(JSON.parse(fs.readFileSync(privateFile(expectedFile),'utf8')));
      assert.deepStrictEqual(document,expected);
      if(expected.imageAvailable) {
        assert(expected.image);assert(image);
        assert.equal(image.mime,expected.image.mime);assert.equal(image.size_bytes,expected.image.sizeBytes);assert.equal(image.sha256,expected.image.sha256);
      }
    }
    fs.writeFileSync(output,JSON.stringify({checkedAt:new Date().toISOString(),documentMatched:expectedFile!=='--capture',forDate:document.forDate,image,document},null,2)+'\n',{mode:0o600});
    fs.chmodSync(output,0o600);
    console.log(JSON.stringify({forDate:document.forDate,documentMatched:expectedFile!=='--capture',imageDigest:image?.sha256,queueRows:document.socialReleaseQueue?.rows.length,routineKind:document.routine?.kind}));
  } finally {await client.query('ROLLBACK').catch(()=>{});await client.end().catch(()=>{});}
}
main().catch(()=>{console.error('Stored brief verification failed; no match claimed');process.exitCode=1;});
