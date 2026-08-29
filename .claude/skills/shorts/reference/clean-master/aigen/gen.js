// Generate the AI cover clips with Veo 3.1 Fast via the Gemini API.
// Text-only (no start frame) at 9:16, so they drop into the vertical picture area full-bleed.
// ⚠ No audio-directive words in a prompt - they trip the RAI safety filter (ad-edit lesson).
// Veo returns a clip WITH audio; it is stripped at composite time, these are b-roll under Dan.
const fs=require('fs'),path=require('path');
const PROJ='/Users/danielrose/Documents/Claude/Projects/Abs By AI';
for(const l of fs.readFileSync(path.join(PROJ,'bakeoff/.env'),'utf8').split('\n')){
  const m=l.match(/^([A-Z_]+)=(.*)$/); if(m) process.env[m[1]]=m[2];
}
const KEY=process.env.GEMINI_API_KEY;
if(!KEY) throw new Error('no GEMINI_API_KEY');
const BASE='https://generativelanguage.googleapis.com/v1beta';
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const CLIPS=require('./clips.js');
const OUT=path.join(__dirname,'clips'); fs.mkdirSync(OUT,{recursive:true});

async function one(c){
  const dst=path.join(OUT,`${c.id}.mp4`);
  if(fs.existsSync(dst)){console.log(`  ${c.id}: already generated`);return;}
  const body={instances:[{prompt:c.prompt}],
    parameters:{aspectRatio:'9:16',durationSeconds:8,resolution:'1080p'}};
  let r=await fetch(`${BASE}/models/veo-3.1-fast-generate-preview:predictLongRunning?key=${KEY}`,
    {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
  let p=await r.json();
  if(r.status>=400){console.log(`  ${c.id}: SUBMIT-FAIL ${JSON.stringify(p).slice(0,240)}`);return;}
  let op=p, waited=0;
  while(!op.done && waited<600){await sleep(12000); waited+=12;
    op=await (await fetch(`${BASE}/${p.name}?key=${KEY}`)).json();}
  if(!op.done){console.log(`  ${c.id}: TIMEOUT`);return;}
  const gv=(op.response||{}).generateVideoResponse||{};
  if(gv.raiMediaFilteredCount>0){
    console.log(`  ${c.id}: FILTERED ${JSON.stringify(gv.raiMediaFilteredReasons||'').slice(0,200)}`);return;}
  const s=(gv.generatedSamples&&gv.generatedSamples[0])||(gv.generatedVideos&&gv.generatedVideos[0]);
  if(!s){console.log(`  ${c.id}: NO-SAMPLE`);return;}
  const uri=(s.video&&(s.video.uri||s.video.videoUri))||s.uri;
  const vr=await fetch(uri.includes('key=')?uri:`${uri}${uri.includes('?')?'&':'?'}key=${KEY}`);
  fs.writeFileSync(dst,Buffer.from(await vr.arrayBuffer()));
  console.log(`  ${c.id}: ${(fs.statSync(dst).size/1048576).toFixed(1)} MB  (${c.seg}, after "${c.after}")`);
}
(async()=>{
  const only=process.argv.slice(2);
  const todo=only.length?CLIPS.filter(c=>only.includes(c.id)):CLIPS;
  console.log(`generating ${todo.length} clips, ~$1.20 each = ~$${(todo.length*1.2).toFixed(2)}`);
  // two at a time: Veo is slow but the API is happy to run them concurrently
  for(let i=0;i<todo.length;i+=2) await Promise.all(todo.slice(i,i+2).map(one));
  console.log('GEN DONE');
})();
