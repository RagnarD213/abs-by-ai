// Own-voice auditions explicitly requested by Dan. Receipts are resumable, inputs redacted.
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const ROOT='/Users/danielrose/Projects/Claude/Projects/Abs By AI',D='/Volumes/Extreme/_edit_work/SL-12/round2/audio';
for(const l of fs.readFileSync(ROOT+'/bakeoff/.env','utf8').split('\n')){const m=l.match(/^([A-Z_]+)=(.*)$/);if(m)process.env[m[1]]=m[2]}
const token=process.env.REPLICATE_API_TOKEN;
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const text="Here's why lifting weights is mandatory if you're taking weight loss medication.";
async function predict(model,input,tag){
 const receipt=D+'/'+tag+'-prediction.json';let p;
 function save(){let q={...p,input:{...p.input}};for(const k of ['voice_file','reference_audio'])if(q.input[k])q.input[k]='[reference data URI omitted; reference hashes in manifest]';fs.writeFileSync(receipt,JSON.stringify(q,null,2))}
 if(fs.existsSync(receipt))p=JSON.parse(fs.readFileSync(receipt));else{
  const r=await fetch('https://api.replicate.com/v1/models/'+model+'/predictions',{method:'POST',headers:{Authorization:'Bearer '+token,'Content-Type':'application/json',Prefer:'wait=60'},body:JSON.stringify({input})});p=await r.json();if(!r.ok)throw Error('HTTP '+r.status+': '+JSON.stringify(p).slice(0,250));save();
 }
 while(['starting','processing'].includes(p.status)){await new Promise(r=>setTimeout(r,4000));const r=await fetch('https://api.replicate.com/v1/predictions/'+p.id,{headers:{Authorization:'Bearer '+token}});if(!r.ok)throw Error('Poll HTTP '+r.status);p=await r.json();save()}
 if(p.status!=='succeeded')throw Error(tag+': '+p.status+': '+JSON.stringify(p.error));return p.output;
}
async function speak(tag,model,input){
 const file=D+'/'+tag+'.wav';if(!fs.existsSync(file)){const o=await predict(model,input,tag);const url=typeof o==='string'?o:o.audio||o.url||o[0];if(!url)throw Error('No audio for '+tag);const r=await fetch(url);if(!r.ok)throw Error('Audio download '+r.status);fs.writeFileSync(file,Buffer.from(await r.arrayBuffer()))}console.log('VOICE_READY',tag,fs.statSync(file).size);return {tag,model,file,sha256:sha(file)};
}
(async()=>{
 let id;const idfile=D+'/parent-voice-id.txt';if(fs.existsSync(idfile))id=fs.readFileSync(idfile,'utf8').trim();else{const o=await predict('minimax/voice-cloning',{voice_file:'data:audio/mpeg;base64,'+fs.readFileSync(D+'/clone-reference.mp3').toString('base64'),model:'speech-02-hd',accuracy:.9,need_noise_reduction:false,need_volume_normalization:false},'parent-clone-mp3');id=typeof o==='string'?o:o.voice_id||o.voiceId;if(!id)throw Error('Missing clone id');fs.writeFileSync(idfile,id)}
 const old=fs.readFileSync('/Volumes/Extreme/_edit_work/SL-11/round1/audio/ai-voice/same-shoot-voice-id.txt','utf8').trim();
 const base={text,audio_format:'wav',sample_rate:44100,channel:'mono',english_normalization:true,language_boost:'English',pitch:0,speed:1};
 const jobs=[['parent-natural-retake','minimax/speech-02-hd',{...base,voice_id:id,emotion:'auto'}],['parent-conversational','minimax/speech-02-hd',{...base,voice_id:id,emotion:'auto',speed:1.06}],['parent-natural','minimax/speech-02-hd',{...base,voice_id:id,emotion:'auto'}],['parent-direct','minimax/speech-02-hd',{...base,voice_id:id,emotion:'neutral',speed:1.04}],['prior-natural','minimax/speech-02-hd',{...base,voice_id:old,emotion:'auto'}],['qwen-parent','qwen/qwen3-tts',{mode:'voice_clone',text,language:'English',reference_audio:'data:audio/wav;base64,'+fs.readFileSync(D+'/qwen-reference.wav').toString('base64'),reference_text:fs.readFileSync(D+'/qwen-reference.txt','utf8'),style_instruction:'Match the reference speaker identity, accent, pitch and ordinary quick conversational teaching delivery. Natural firm emphasis on mandatory. No theatrical announcement.'}]];
 // Independent remote generation calls; no project credits or deployment paths.
 const outcomes=await Promise.allSettled(jobs.map(x=>speak(...x)));const rows=outcomes.map((r,i)=>r.status==='fulfilled'?r.value:{tag:jobs[i][0],error:r.reason.message});
 fs.writeFileSync(D+'/generation-manifest.json',JSON.stringify({text,authorization:'Dan own-voice AI opening, confirmed for A on Nov2',estimate_upper_usd:5,actual_clone_upload:{file:D+'/clone-reference.mp3',sha256:sha(D+'/clone-reference.mp3')},reference:[['clone-reference',455.064,488.764],['qwen-reference',347.8,366.5]].map(([n,a,b])=>({file:D+'/'+n+'.wav',sha256:sha(D+'/'+n+'.wav'),parent_range:[a,b]})),candidates:rows},null,2));
 if(rows.some(x=>x.error))console.log('Some candidates failed; inspect manifest.');
})().catch(e=>{console.error('FAIL',e.message);process.exit(1)});
