// Veo 3.1 Fast via the Gemini API -- the working path (Replicate credit has drained twice).
// No audio-directive words in the prompt: they trip the RAI safety filter.
const fs=require('fs'),path=require('path');
const PROJ='/Users/danielrose/Documents/Claude/Projects/Abs By AI';
for(const l of fs.readFileSync(path.join(PROJ,'bakeoff/.env'),'utf8').split('\n')){const m=l.match(/^([A-Z_]+)=(.*)$/);if(m)process.env[m[1]]=m[2];}
const KEY=process.env.GEMINI_API_KEY;
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
const BASE='https://generativelanguage.googleapis.com/v1beta';
const START=process.argv[2]||'frame_mirror.jpg';
const OUT=process.argv[3]||'clip_amazing.mp4';
const PROMPT='Cinematic photorealistic shot, static locked-off camera. A lean athletic man in a warm sunlit bathroom looks at his own reflection in the mirror. He turns his torso very slightly, glances down at his flat defined midsection, then lifts his eyes back to the mirror and gives a small satisfied nod with a quiet half-smile. Slow natural movement, soft morning light, shallow depth of field. Calm, dignified, aspirational. One person only. No text and no graphics on screen.';
(async()=>{
  const body={instances:[{prompt:PROMPT,image:{bytesBase64Encoded:fs.readFileSync(START).toString('base64'),mimeType:'image/jpeg'}}],
    parameters:{aspectRatio:'16:9',durationSeconds:8,resolution:'1080p'}};
  let r=await fetch(`${BASE}/models/veo-3.1-fast-generate-preview:predictLongRunning?key=${KEY}`,
    {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
  let p=await r.json();
  if(r.status>=400){console.log('SUBMIT-FAIL',JSON.stringify(p).slice(0,400));process.exit(1);}
  console.log('submitted',p.name);
  let op=p;
  while(!op.done){await sleep(12000);op=await (await fetch(`${BASE}/${p.name}?key=${KEY}`)).json();}
  const gv=(op.response||{}).generateVideoResponse||{};
  if(gv.raiMediaFilteredCount>0){console.log('FILTERED',JSON.stringify(gv.raiMediaFilteredReasons||'').slice(0,300));process.exit(2);}
  const s=(gv.generatedSamples&&gv.generatedSamples[0])||(gv.generatedVideos&&gv.generatedVideos[0]);
  if(!s){console.log('NO-SAMPLE',JSON.stringify(op).slice(0,400));process.exit(3);}
  const uri=(s.video&&(s.video.uri||s.video.videoUri))||s.uri;
  const vr=await fetch(uri.includes('key=')?uri:`${uri}${uri.includes('?')?'&':'?'}key=${KEY}`);
  fs.writeFileSync(OUT,Buffer.from(await vr.arrayBuffer()));
  console.log('DONE',OUT,(fs.statSync(OUT).size/1048576).toFixed(1),'MB');
})();
