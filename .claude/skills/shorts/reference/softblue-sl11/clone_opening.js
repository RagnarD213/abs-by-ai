const fs=require('fs'),path=require('path'),crypto=require('crypto');
const ROOT='/Users/danielrose/Documents/Claude/Projects/Abs By AI',D='/Volumes/Extreme/_edit_work/SL-11/round1/audio/ai-voice';
for(const l of fs.readFileSync(path.join(ROOT,'bakeoff/.env'),'utf8').split('\n')){const m=l.match(/^([A-Z_]+)=(.*)$/);if(m)process.env[m[1]]=m[2]}
const token=process.env.REPLICATE_API_TOKEN;
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
async function predict(model,input,tag){
 const receipt=path.join(D,tag+'-prediction.json');let p;
 if(fs.existsSync(receipt))p=JSON.parse(fs.readFileSync(receipt));
 else{const r=await fetch('https://api.replicate.com/v1/models/'+model+'/predictions',{method:'POST',headers:{Authorization:'Bearer '+token,'Content-Type':'application/json',Prefer:'wait=60'},body:JSON.stringify({input})});p=await r.json();if(!r.ok)throw Error('HTTP'+r.status+':'+JSON.stringify(p).slice(0,300));save()}
 function save(){const q={...p};if(q.input?.voice_file)q.input={...q.input,voice_file:'[same-shoot-reference.mp3 data URI omitted; hash inmanifest]'};fs.writeFileSync(receipt,JSON.stringify(q,null,2))}
 while(['starting','processing'].includes(p.status)){await new Promise(r=>setTimeout(r,4000));const r=await fetch('https://api.replicate.com/v1/predictions/'+p.id,{headers:{Authorization:'Bearer '+token}});p=await r.json();save()}
 if(p.status!=='succeeded')throw Error('prediction'+p.status+':'+JSON.stringify(p.error));return p.output;
}
(async()=>{
 const sample=path.join(D,'same-shoot-reference.mp3');let idfile=path.join(D,'same-shoot-voice-id.txt');let id;
 if(fs.existsSync(idfile))id=fs.readFileSync(idfile,'utf8').trim();else{const o=await predict('minimax/voice-cloning',{voice_file:'data:audio/mpeg;base64,'+fs.readFileSync(sample).toString('base64'),model:'speech-02-hd',need_noise_reduction:false,need_volume_normalization:false},'clone');id=typeof o==='string'?o:o.voice_id||o.voiceId;if(!id)throw Error('Missingvoiceid');fs.writeFileSync(idfile,id)}
 console.log('Same-shoot clone created');const rows=[];
 for(const [tag,speed,emotion] of [['natural',1,'auto'],['brisk',1.07,'neutral']]){
 const dest=path.join(D,tag+'.wav');if(!fs.existsSync(dest)){const o=await predict('minimax/speech-02-hd',{text:"Here's a mistake I see with a lot of beginners when they first start doing stomach vacuums.",voice_id:id,emotion,speed,audio_format:'wav',sample_rate:44100,channel:'mono',english_normalization:true,language_boost:'English'},tag);const url=typeof o==='string'?o:o.audio||o.url;if(!url)throw Error('Noaudiodownload');const r=await fetch(url);if(!r.ok)throw Error('Downloadaudio'+r.status);fs.writeFileSync(dest,Buffer.from(await r.arrayBuffer()))}
 rows.push({tag,speed,emotion,file:dest,sha256:sha(dest)});console.log('Created',tag,fs.statSync(dest).size)
 }
 fs.writeFileSync(path.join(D,'generation-manifest.json'),JSON.stringify({authorization:'Dan explicit ownvoicefallback after Yeti mismatch',source_parent_sha256:'24d71e04f1d952c3809b82e25c10f388fe722c12f7258d9c7cd1cb24d874996d',sample:{range:[487.405,522.505],file:sample,sha256:sha(sample)},estimate_usd:3.25,model:'minimax/speech-02-hd',outputs:rows},null,2));
})().catch(e=>{console.error('FAIL',e.message);process.exit(1)});
