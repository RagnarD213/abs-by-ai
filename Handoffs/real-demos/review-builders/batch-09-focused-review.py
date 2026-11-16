"""Focused Batch9 revision review. Media and existing clearances stay unchanged."""
from pathlib import Path
import json,hashlib,shutil,html
import sys
W=Path(sys.argv[1]) if len(sys.argv)>1 else Path('/Volumes/Extreme/_edit_work/REALDEMOS-B09/round2')
P=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI')
R=W.parent/'review'
clear=json.loads((W/'review_clearance.json').read_text())
items=[
 ('db-lateral-raise','Side Lateral','New demo','New narrated demo from the real footage you accepted.',0),
 ('db-hammer-curl','Hammer Curl','Name and pacing revised','Corrected the exercise name and narration, and removed the unnecessary pauses.',0),
 ('db-shoulder-press','Dumbbell Shoulder Press','Middle narration revised','Check the tighter middle narration. Your accepted picture and ending are preserved.',6.3),
]
manifest=[];sections=[]
for i,name,tag,note,start in items:
 out=W/'out'/i;master=out/(i+'-REAL-1080.mp4');app=out/(i+'.mp4');poster=out/(i+'.jpg')
 for file,key in [(master,'master_sha256'),(app,'app_sha256'),(poster,'poster_sha256')]:
  assert hashlib.sha256(file.read_bytes()).hexdigest()==clear[i][key],(i,key)
 gate=json.loads((out/(i+'.mp4.deliver_gate.json')).read_text())
 assert gate['verdict']=='PASS' and gate['sha256']==clear[i]['app_sha256']
 duration=json.loads((out/'edit.json').read_text())['duration']
 shutil.copyfile(master,R/master.name);shutil.copyfile(poster,R/(i+'-poster.jpg'))
 src=master.name+'?v='+clear[i]['master_sha256'][:12]+('#t='+str(start) if start else '')
 watch=(f'{start:.1f} seconds to the end' if start else f'Full {duration:.1f}-second clip')
 sections.append(f'''<section id="{i}" aria-labelledby="title-{i}">
 <div class="label">{html.escape(tag)}</div><h2 id="title-{i}">{html.escape(name)}</h2>
 <p>{html.escape(note)}</p><p class="watch">Watch: {watch}</p>
 <video id="real-{i}" data-start="{start}" controls playsinline muted preload="auto" poster="{i}-poster.jpg?v={clear[i]['poster_sha256'][:12]}" src="{src}"></video>
 <div class="transport"><button type="button" data-play="{i}">Play this change</button><button type="button" data-pause="{i}">Pause</button><span id="state-{i}" role="status">Paused</span></div>
 </section>''')
 manifest.append({'id':i,**clear[i],'duration':duration,'watch_start':start,'file':master.name})
shutil.copyfile(P/'.claude/skills/_shared/review_player.js',R/'review_player.js')
page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Batch 9: only the changes</title><script src="review_player.js" defer></script><style>
:root{color-scheme:light dark;--bg:#f3f6fa;--card:#fff;--ink:#172332;--muted:#536478;--line:#d8e1eb;--blue:#1d5c9a}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 system-ui,-apple-system,sans-serif}
main{max-width:900px;margin:auto;padding:16px}h1{font-size:clamp(25px,4vw,34px);line-height:1.15;margin:12px 0}
h2{font-size:23px;line-height:1.2;margin:5px 0 10px}p{margin:8px 0 12px}.lede,.prior{color:var(--muted)}
nav{display:flex;gap:8px;flex-wrap:wrap;margin:16px 0}nav a{color:var(--blue);padding:6px 10px;border:1px solid var(--line);border-radius:7px;font-size:14px;text-decoration:none}
section{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;margin:22px 0;scroll-margin-top:12px}
.label{color:var(--blue);font-size:13px;font-weight:650}.watch{font-size:14px;font-weight:650}
video{display:block;width:100%;aspect-ratio:16/9;background:#050a10;border-radius:8px}
.transport{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-top:10px}.transport button{font:inherit;font-size:14px;color:var(--ink);background:var(--card);border:1px solid var(--line);border-radius:7px;padding:8px 12px;cursor:pointer}
.transport span{font-size:13px;color:var(--muted)}.prior{font-size:14px;border-top:1px solid var(--line);padding-top:14px}
@media(min-width:760px){main{padding:24px}}@media(prefers-color-scheme:dark){:root{--bg:#101821;--card:#182430;--ink:#eff5fa;--muted:#afc0d0;--line:#304252;--blue:#8fc3ff}}
</style></head><body><main><h1>Only the changes to review</h1><p class="lede">Batch 9 · Three items, about 36 seconds to check.</p>
<nav aria-label="Changes"><a href="#db-lateral-raise">Side Lateral</a><a href="#db-hammer-curl">Hammer Curl</a><a href="#db-shoulder-press">Shoulder Press</a></nav>
'''+''.join(sections)+'''<p class="prior">Your earlier review is retained. Squat, battle ropes, push-up and knee push-up are off this page. Their requested ending and pacing fixes have been checked.</p>
</main><script>
document.querySelectorAll('[data-play]').forEach(b=>b.addEventListener('click',()=>{
 const v=document.getElementById('real-'+b.dataset.play);document.querySelectorAll('video').forEach(x=>x.pause());
 v.currentTime=Number(v.dataset.start);v.play().catch(()=>{document.getElementById('state-'+b.dataset.play).textContent='Press Play to continue';});
}));
document.querySelectorAll('[data-pause]').forEach(b=>b.addEventListener('click',()=>document.getElementById('real-'+b.dataset.pause).pause()));
document.querySelectorAll('video').forEach(v=>{
 const state=document.getElementById('state-'+v.id.slice(5));
 v.addEventListener('playing',()=>{state.textContent='Playing';});
 v.addEventListener('pause',()=>{state.textContent='Paused';});
 v.addEventListener('ended',()=>{state.textContent='Paused';});
});
</script></body></html>'''
(R/'index.html').write_text(page)
(R/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Focused review:3 unchanged1080p masters. Other demos and all app media untouched.')
