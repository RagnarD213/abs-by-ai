const fs=require('fs'),path=require('path');
const ROOT='/Users/danielrose/Documents/Claude/Projects/Abs By AI';
const tok=fs.readFileSync(path.join(ROOT,'bakeoff/.env'),'utf8').match(/REPLICATE_API_TOKEN=(\S+)/)[1].replace(/"/g,'');
const H={Authorization:`Bearer ${tok}`,'Content-Type':'application/json'};
(async()=>{
 const [inp,out]=process.argv.slice(2);
 const m=await(await fetch('https://api.replicate.com/v1/models/vaibhavs10/incredibly-fast-whisper',{headers:H})).json();
 const audio='data:audio/mpeg;base64,'+fs.readFileSync(inp).toString('base64');
 let p=await(await fetch('https://api.replicate.com/v1/predictions',{method:'POST',headers:H,body:JSON.stringify({version:m.latest_version.id,input:{audio,timestamp:'word',language:'english',task:'transcribe',batch_size:8}})})).json();
 while(!['succeeded','failed','canceled'].includes(p.status)){await new Promise(r=>setTimeout(r,3000));p=await(await fetch(p.urls.get,{headers:H})).json();}
 if(p.status!=='succeeded'){console.error(p.status,p.error);process.exit(1);}
 fs.writeFileSync(out,JSON.stringify(p.output));console.log('ok',p.output.chunks.length,'words',p.metrics&&p.metrics.predict_time);
})();
