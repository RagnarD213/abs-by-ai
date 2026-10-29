from pathlib import Path
import json,shutil
W=Path(__file__).resolve().parents[1]
page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Mouthpiece · Audio R3</title>
<style>*{box-sizing:border-box}body{margin:0;background:#edf4fb;color:#102a43;font:17px/1.55 system-ui,sans-serif}main{max-width:1050px;padding:46px 24px 100px;margin:auto}.tag{font-size:12px;letter-spacing:.15em;font-weight:750;color:#38648e}h1{font-size:clamp(30px,5vw,47px);line-height:1.12;max-width:750px;margin:16px 0}h2{font-size:22px;margin:30px 0 12px}p{max-width:780px}.lead{font-size:20px;color:#405d76}.panel,.card{background:#fff;border:1px solid #ccdfef;border-radius:18px;padding:22px;box-shadow:0 9px 30px #153c6610}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}.card{cursor:pointer;text-align:left;color:inherit;font:inherit;transition:.15s}.card:hover{border-color:#3280c8}.card[aria-pressed=true]{outline:3px solid #3e84c6;border-color:transparent}.letter{display:block;font-size:13px;font-weight:800;color:#477092;margin-bottom:6px}.card strong{font-size:21px;display:block}.card small{display:block;line-height:1.4;color:#556e84;margin-top:9px}.controls{display:flex;gap:10px;flex-wrap:wrap;margin:20px 0 10px}button.action{font:600 15px system-ui;border:1px solid #9dbbd5;border-radius:9px;padding:11px 17px;background:white;color:#153c66;cursor:pointer}button.primary{background:#184f82;color:white;border-color:#184f82}audio{width:100%;margin-top:10px}.now{font-weight:700;color:#184f82}.muted{color:#9c3c1d;font-size:14px}a{color:#1b5d99}small,.meta{color:#526f87;font-size:14px}textarea{width:100%;min-height:80px;border:1px solid #b4cada;border-radius:10px;padding:12px;font:16px system-ui}details{margin-top:22px}summary{cursor:pointer;font-size:14px;color:#526f87}.notes{font-size:14px}blockquote{margin:18px 0;padding-left:18px;border-left:3px solid #82aed2;color:#4a6680}@media(max-width:650px){main{padding:28px 16px 80px}.grid{grid-template-columns:1fr}.card{padding:16px}.card strong{font-size:19px}.card small{margin-top:5px}}</style></head><body><main>
<span class="tag">WHY I WEAR A MOUTHPIECE · SFC · AUDIO ROUND 3</span>
<h1>Which version sounds clearest<br>and still sounds like you?</h1>
<p class="lead">The same 12-second passage, played at the same volume. Switch versions during playback to compare the same words.</p>
<section class="panel" aria-label="Audio comparison">
<div class="grid">
<button class="card" id="pickA" aria-pressed="true" onclick="choose('A')"><span class="letter">A</span><strong>Current audio</strong><small>The Natural Warmth voice in your current full edit.</small></button>
<button class="card" id="pickB" aria-pressed="false" onclick="choose('B')"><span class="letter">B</span><strong>Gentle cleanup</strong><small>Light background cleanup and a small clarity adjustment.</small></button>
<button class="card" id="pickC" aria-pressed="false" onclick="choose('C')"><span class="letter">C</span><strong>Stronger cleanup</strong><small>More background reduction with a slightly larger clarity adjustment.</small></button>
</div>
<div class="controls"><button class="action primary" id="toggle" onclick="toggle()">Play</button><button class="action" onclick="restart()">Play from start</button><button class="action" onclick="sequence()">Play A → B → C</button><button class="action" id="mute" onclick="mute()">Mute</button></div>
<div class="now" id="now" role="status" aria-live="polite">A · Current audio</div><div class="muted" id="sound"></div>
<audio id="player" controls preload="metadata" src="media/A.wav"></audio><p class="meta">Passage from 0:13.72–0:25.80 in the full Short. A new selection keeps your current position. “Play from start” repeats the whole passage.</p>
</section>
<h2>Your decision</h2><p>Choose <b>A, B or C</b>. Listen especially to “breathe through my nose” and “a better and more efficient way.” Does the cleanup help while keeping the warmth and texture of your voice?</p>
<p id="recommendation">All three are auditions. Your full R2 edit is still unchanged.</p>
<textarea aria-label="Your audio choice">Audio choice: A / B / C
Notes:</textarea>
<h2>What I decided (overrule anything)</h2><ul><li>Keep the warm voice you selected and use restrained cleanup strengths.</li><li>Use noise reduction and small tone adjustments, with no voice replacement or echo-removal treatment.</li><li>Match the volume, preserve complete phrases, and correct processing delay so switching stays on the same word.</li></ul>
<p><a href="http://127.0.0.1:9275/">Open the unchanged full R2 edit</a> · Download <a href="media/A.wav">A</a> / <a href="media/B.wav">B</a> / <a href="media/C.wav">C</a></p>
<details><summary>Checks and review notes</summary><div class="notes" id="qa">QA_PENDING</div><p class="notes"><a href="notes/quality-review.txt">Audio listening review</a> · <a href="notes/checks.txt">Measured checks</a></p></details>
</main><script>
const p=document.getElementById('player');let key='A',seq=false,switchVersion=0;
const names={A:'Current audio',B:'Gentle cleanup',C:'Stronger cleanup'};
function update(){document.getElementById('toggle').textContent=p.paused?'Play':'Pause';document.getElementById('mute').textContent=p.muted?'Unmute':'Mute';document.getElementById('sound').textContent=p.muted?'Sound is muted. Select Unmute to hear the comparison.':''}
async function choose(k,keepSequence=false,fromStart=false){const t=fromStart?0:(Number.isFinite(p.currentTime)?p.currentTime:0),playing=!p.paused;seq=keepSequence;key=k;const version=++switchVersion;for(const j of ['A','B','C'])document.getElementById('pick'+j).setAttribute('aria-pressed',j===k?'true':'false');document.getElementById('now').textContent=k+' · '+names[k];p.pause();p.src='media/'+k+'.wav';p.load();await new Promise((ok,bad)=>{p.addEventListener('loadedmetadata',ok,{once:true});p.addEventListener('error',bad,{once:true})});if(version!==switchVersion)return;p.currentTime=Math.min(t,Math.max(0,p.duration-.01));if(playing)await p.play();update()}
function toggle(){seq=false;p.paused?p.play():p.pause();update()}
function restart(){seq=false;p.currentTime=0;p.play();update()}
async function sequence(){p.pause();await choose('A',true,true);seq=true;p.currentTime=0;await p.play();update()}
function mute(){p.muted=!p.muted;update()}
p.addEventListener('play',update);p.addEventListener('pause',update);p.addEventListener('volumechange',update);p.addEventListener('ended',async()=>{if(seq&&key!=='C'){await choose(key==='A'?'B':'C',true,true);p.currentTime=0;await p.play()}else{seq=false;update()}});p.addEventListener('error',()=>{document.getElementById('now').textContent='Audio could not load. Reload this page or use the download links.'});
</script></body></html>'''
import html
notes=(W/'review/notes/checks.txt').read_text() if (W/'review/notes/checks.txt').exists() else 'Checks are in progress.'
page=page.replace('QA_PENDING',html.escape(notes).replace('\n','<br>'))
(W/'review/index.html').write_text(page)
print(W/'review/index.html')
