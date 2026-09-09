// Veo 3.1 Fast (Gemini API) image-to-video for the website video's AI inserts (ad-edit lesson 9 / Step 4.5).
//   node veo.js <still.jpg> <prompt.txt> <out.mp4> [durationSeconds=8] [aspect=16:9]
// Reads GEMINI_API_KEY from ~/.absbyai-secrets.env. Exit 2 = RAI-filtered (not charged), 1 = submit failed.
// No audio-directive words in a prompt (they trip the filter); the returned audio is stripped at composite time.
const fs=require('fs'),os=require('os'),path=require('path');
for(const l of fs.readFileSync(path.join(os.homedir(),'.absbyai-secrets.env'),'utf8').split('\n')){const m=l.match(/^([A-Z_]+)=(.*)$/);if(m&&!process.env[m[1]])process.env[m[1]]=m[2].replace(/^"|"$/g,'');}
const KEY=process.env.GEMINI_API_KEY; if(!KEY) throw new Error('no GEMINI_API_KEY');
const [STILL,PROMPT,OUT,DUR='8',ASPECT='16:9']=process.argv.slice(2);
const BASE='https://generativelanguage.googleapis.com/v1beta';
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{
  const prompt=fs.readFileSync(PROMPT,'utf8').trim();
  const inst={prompt}; if(STILL&&STILL!=='-') inst.image={bytesBase64Encoded:fs.readFileSync(STILL).toString('base64'),mimeType:'image/jpeg'};
  const body={instances:[inst],parameters:{aspectRatio:ASPECT,durationSeconds:Number(DUR),resolution:'1080p'}};
  let r=await fetch(`${BASE}/models/veo-3.1-fast-generate-preview:predictLongRunning?key=${KEY}`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
  let p=await r.json();
  if(r.status>=400){console.log('SUBMIT-FAIL',JSON.stringify(p).slice(0,500));process.exit(1);}
  console.log('submitted',p.name,new Date().toISOString());
  let op=p,waited=0;
  while(!op.done&&waited<900){await sleep(10000);waited+=10;op=await (await fetch(`${BASE}/${p.name}?key=${KEY}`)).json();}
  if(!op.done){console.log('TIMEOUT');process.exit(4);}
  const gv=(op.response||{}).generateVideoResponse||{};
  if(gv.raiMediaFilteredCount>0){console.log('FILTERED',JSON.stringify(gv.raiMediaFilteredReasons||'').slice(0,400));process.exit(2);}
  const s=(gv.generatedSamples&&gv.generatedSamples[0])||(gv.generatedVideos&&gv.generatedVideos[0]);
  if(!s){console.log('NO-SAMPLE',JSON.stringify(op).slice(0,600));process.exit(3);}
  const uri=(s.video&&(s.video.uri||s.video.videoUri))||s.uri;
  const vr=await fetch(uri.includes('key=')?uri:`${uri}${uri.includes('?')?'&':'?'}key=${KEY}`);
  fs.writeFileSync(OUT,Buffer.from(await vr.arrayBuffer()));
  console.log('DONE',OUT,(fs.statSync(OUT).size/1048576).toFixed(1),'MB',`${waited}s`);
})();
