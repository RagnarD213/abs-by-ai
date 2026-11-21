from pathlib import Path
import json,shutil,html
O=Path('/Volumes/Extreme/_edit_work/ra13/round2');P=O/'review';P.mkdir(exist_ok=True);f=O/'delivery-status.json';status=json.load(open(f)) if f.exists() else {'summary':'Review candidates complete. Final gate results and independent audit are being recorded.'}
items=[('P1','14.35 - 25.16','Same-person goal demo','Kept the approved real-photo upload and AI pool goal. The brief presenter flash before First is covered.'),('A1','28.36 - 33.77','Photo analysis','Rebuilt with the current shared analysis card. Same goal photo, scan, three bars and plan. No printed numbers.'),('P2','33.77 - 38.97','Workout and food tour','Kept the moving push-up instruction followed by food analysis to match the line.'),('CTA','51.38 - 53.92','Get started','Shared Soft Blue Light CTA moved clear of the abs and captions. Vertical sits over shorts; horizontal sits in the left pool space. No ending URL.')]
cs=''.join(f'''<article><div class="eyebrow">{t}</div><h3>{title}</h3><p><b>What I decided:</b> {note}</p><button onclick="load('{id}-9x16-context.mp4','{title}, vertical')">Watch vertical context</button><button onclick="load('{id}-16x9-context.mp4','{title}, horizontal')">Watch horizontal context</button></article>''' for id,t,title,note in items)
s=html.escape(status['summary'])
doc='''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Most Guys Abs AD R2</title><style>*{box-sizing:border-box}body{margin:0;background:#f1f6fb;color:#142b40;font:16px/1.55 system-ui}main{max-width:1100px;margin:auto;padding:30px 24px 180px}h1{font-size:34px;line-height:1.1}.tag,.eyebrow{color:#1474b1;font-size:13px;font-weight:700}section,article{background:white;border:1px solid #d7e4ed;border-radius:16px;padding:22px;margin:20px 0}button,a.download{border:1px solid #89b5d4;border-radius:8px;padding:10px 14px;background:#e9f5ff;color:#074776;cursor:pointer;font:inherit;margin:4px}a{color:#075489}video{display:block;max-width:100%;max-height:62vh;margin:auto;background:#071a2e;border-radius:10px}.player{position:sticky;top:0;z-index:5;box-shadow:0 8px 30px #1232;padding:14px}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}.grid article{margin:0}h3{margin:6px 0}textarea{width:100%;min-height:140px;padding:14px;font:inherit;border:1px solid #aac7dc;border-radius:8px}.note{font-size:14px;color:#42596a}@media(max-width:750px){.grid{grid-template-columns:1fr}main{padding:20px 12px}.player{position:relative}h1{font-size:28px}}</style></head><body><main><span class="tag">AD / RA-13 / ROUND 2 / 53.92 SECONDS</span><h1>Most Guys Abs</h1><p>Brighter Natural B, approved lighter bass and vertical crop. Horizontal close shots retain their size with about 30% less empty headroom.</p><section class="player"><div id="now" class="eyebrow">Whole ad, vertical</div><video id="film" controls playsinline preload="auto" src="Most Guys Abs AD R2 - 9x16 - REVIEW540p.mp4"></video><div><button onclick="load('Most Guys Abs AD R2 - 9x16 - REVIEW540p.mp4','Whole ad, vertical')">Whole vertical</button><button onclick="load('Most Guys Abs AD R2 - 16x9 - REVIEW540p.mp4','Whole ad, horizontal')">Whole horizontal</button><button onclick="recoverVideo()">Reload video</button><span id="playback-status" class="note" role="status" aria-live="polite"></span><button onclick="film.playbackRate=1">1x</button><button onclick="film.playbackRate=2">2x</button><button onclick="film.playbackRate=3">3x</button><button onclick="film.playbackRate=4">4x</button></div></section><p><a class="download" href="Most Guys Abs AD R2 - 9x16.mp4">Full-quality vertical</a><a class="download" href="Most Guys Abs AD R2 - 16x9.mp4">Full-quality horizontal</a></p><p class="note">Full-quality physical copies are also in Videos to Review for VLC.</p><section><h2>Review status</h2><p>STATUS</p><p>Two rejected inserts were removed: the distorted lockscreen clip and the stick-figure workout clip. Their lines stay on Dan. Nothing has been uploaded or published.</p></section><h2>Changes to check</h2><section><button onclick="load('Most Guys Abs AD R2 - 9x16 - REVIEW540p.mp4','Whole vertical, analysis',28)">Jump to analysis (28s)</button><button onclick="load('Most Guys Abs AD R2 - 9x16 - REVIEW540p.mp4','Whole vertical, ending',51)">Jump to ending (51s)</button><p><b>Horizontal headroom:</b> close shots at 2.27 - 14.35, 25.16 - 28.36 and 42.61 - 46.58. Quick watch ranges: 2 - 6, 24.5 - 29, and 42 - 47.</p><button onclick="load('headroom-16x9-context.mp4','Horizontal headroom, 1 - 7 seconds')">Watch headroom context</button><p><b>Opening:</b> removed 0.60 seconds of empty lead before Why. All spoken lines remain.</p></section><h2>Retained graphics in timeline order</h2><div class="grid">CARDS</div><section><h2>Your notes</h2><textarea id="notes" placeholder="Add timestamps and revisions here"></textarea><button onclick="navigator.clipboard.writeText(document.querySelector('#notes').value)">Copy notes</button><p class="note">Notes stay in this browser. Copy and paste them into the chat.</p></section></main><script>const film=document.querySelector('#film');
const playbackStatus=document.querySelector('#playback-status');
let pendingLoad=null;
function setVideo(src,at=0,resume=false,rate=film.playbackRate){
  if(pendingLoad)pendingLoad.abort();
  pendingLoad=new AbortController();
  film.pause();
  film.addEventListener('loadedmetadata',()=>{
    film.currentTime=Math.min(at,Math.max(0,film.duration-0.05));
    film.playbackRate=rate;
    playbackStatus.textContent='';
    if(resume)film.play().catch(()=>{playbackStatus.textContent='Press play to continue.';});
  },{once:true,signal:pendingLoad.signal});
  film.src=src;
  film.load();
}
function load(src,label,at=0){
  setVideo(src,at,true);
  document.querySelector('#now').textContent=label;
  film.scrollIntoView({behavior:'smooth',block:'center'});
}
function recoverVideo(){
  const src=new URL(film.currentSrc||film.src,location.href);
  src.searchParams.set('reload',Date.now());
  playbackStatus.textContent='Reloading video...';
  setVideo(src.href,film.currentTime,!film.paused);
}
film.addEventListener('error',()=>{playbackStatus.textContent='Video could not load. Use Reload video.';});
let inactiveAt=Date.now();
function restoreAfterInactivity(){
  if(document.visibilityState==='visible'&&Date.now()-inactiveAt>60000)recoverVideo();
  inactiveAt=Date.now();
}
document.addEventListener('visibilitychange',()=>{
  if(document.hidden)inactiveAt=Date.now();else restoreAfterInactivity();
});
window.addEventListener('blur',()=>{inactiveAt=Date.now();});
window.addEventListener('focus',restoreAfterInactivity);
window.addEventListener('pageshow',e=>{if(e.persisted)recoverVideo();});
const n=document.querySelector('#notes');n.value=localStorage.getItem('RA13R2notes')||'';n.oninput=()=>localStorage.setItem('RA13R2notes',n.value);</script></body></html>'''.replace('STATUS',s).replace('CARDS',cs)
assert '\u2014' not in doc and '\u2013' not in doc
(P/'index.html').write_text(doc);print(P/'index.html')
