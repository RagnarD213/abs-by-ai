"""Package reviewed R4 films and preserve the repaired managed review player."""
import json,shutil,html,subprocess
from pathlib import Path
R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');W=Path('/Volumes/Extreme/_edit_work/ra16');O=Path('/Volumes/Expansion/Abs By AI Edit Work/ra16/round4');PAGE=W/'round2';DEST=R/'Codex Ad Videos/ai took my job - RA-16';VLC=R/'Videos to Review'
assert (O/'final-review-status.json').exists(),'Final review disposition required'
q=json.load(open(O/'final-review-status.json'));assert q['ready_for_dan_review'],q
local=PAGE/'r4';local.mkdir(exist_ok=True);VLC.mkdir(exist_ok=True)
media=[]
for aspect in ['9x16','16x9']:
 master=O/'masters'/f'AI Took Job AD R4 - {aspect}.mp4';rev=O/'review'/f'AI Took Job AD R4 - {aspect} - REVIEW.mp4'
 for src,dst in [(master,DEST/master.name),(master,VLC/master.name),(master,local/master.name),(rev,local/rev.name)]:shutil.copy2(src,dst)
 poster=local/f'R4-{aspect}.jpg';subprocess.run([str(R/'Media/video_edit/bin/ffmpeg'),'-v','error','-y','-ss','2','-i',str(master),'-frames:v','1',str(poster)],check=True)
 media.append(dict(src='r4/'+rev.name,poster='r4/'+poster.name,label='Full R4 '+aspect,master='r4/'+master.name))
for p in (O/'audio').glob('Audio AB*.mp4'):shutil.copy2(p,local/p.name)
shutil.copy2(O/'final-review-status.json',local/'final-review-status.json')
s='''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AI Took Job AD R4</title><style>*{box-sizing:border-box}body{margin:0;background:#091524;color:#eef4fa;font:16px/1.6 system-ui}main{max-width:1100px;margin:auto;padding:30px}h1{font-size:38px}h2{color:#78d7f7}.card,#dock{padding:18px;background:#13263b;border:1px solid #31465b;border-radius:12px;margin:16px 0}button{background:#15536d;color:white;border:1px solid #6bb3d0;padding:10px 14px;border-radius:8px;margin:5px;cursor:pointer}a{color:#8bdef9}video{display:block;width:100%;height:59vh;max-height:680px;object-fit:contain;background:#020810}#dock{scroll-margin-top:16px}.muted{color:#a2b4c7}#player-status:empty{display:none}@media(min-width:1300px){main{margin-left:2vw;margin-right:490px;max-width:1150px}#dock{position:fixed;top:16px;right:16px;width:450px;z-index:5}}@media(max-width:760px){main{padding:16px}h1{font-size:30px}}</style></head><body><main><p class="muted">AD / Round 4 / Complete Films</p><h1>AI Took Job</h1><p>Both complete films are 58.89 seconds. Your approved color B, crop pair 1, full intro, warm bass voice and four assets are preserved.</p>'''
def js(s):return html.escape(json.dumps(s),quote=True)
s+='<div id="dock"><b id="now">Full R4 9x16</b><video id="player" controls preload="auto" playsinline src="'+html.escape(media[0]['src'])+'" poster="'+html.escape(media[0]['poster'])+'"></video><div><label><input type="checkbox" id="mute" onchange="mutePlayback(this.checked)"> Mute</label><button onclick="togglePlayback()">Play / Pause</button><button onclick="seekBy(-3)">Back 3 Seconds</button><button onclick="seekBy(3)">Forward 3 Seconds</button><button onclick="reloadClip()">Reload Film</button><a id="open-clip" target="_blank" href="'+html.escape(media[0]['src'])+'">Open Film Separately</a></div><p id="player-status" role="status"></p></div>'
s+='<section class="card"><h2>Watch The Complete Films</h2>'
for m in media:s+=f'<p><button onclick="play({js(m["src"])},{js(m["label"])})">{html.escape(m["label"])}</button> <a href="{html.escape(m["master"])}">Native Master</a></p>'
s+='</section><section class="card"><h2>What Changed In R4</h2><p>The full ad is now assembled in both formats. The phone demonstration plays at 0:19.39-0:24.19, analysis at 0:25.26-0:32.80, the plan lower third at 0:32.80-0:38.10, and the life-changes point at 0:42.68-0:47.41. Vertical framing lands on you at each actual cut and return. Captions are applied once. The phrase &ldquo;And finally, AI adjusts&rdquo; now starts at 0:43.14 after the breath; watch 0:42-0:45 to check that repair.</p><p>For the transitions, watch 0:17-0:27, 0:30-0:40 and 0:41-0:49. This is the first complete-film review, so also watch the opening and final call to action.</p></section><section class="card"><h2>Checks And Review</h2><p>'+html.escape(q['summary'])+'</p><p><a href="r4/final-review-status.json">Full Check And Review Record</a></p>'
for p in local.glob('Audio AB*.mp4'):s+=f'<p><a href="r4/{html.escape(p.name)}">Reference / Current Voice A/B ({html.escape(p.stem)})</a></p>'
s+='</section><section class="card"><h2>Your Review</h2><p>Approve both full films, or send timestamps and the changes you want. The R3 asset choices remain approved. Nothing has been published.</p><p>The full-quality files are also in Videos to Review for VLC.</p></section></main><script>const media='+json.dumps(media)+';function mutePlayback(flag){document.getElementById("player").muted=flag;}'+(W/'recipe/round3_player.js').read_text().replace("v.id='player'; v.controls=true;","v.id='player'; v.muted=document.getElementById('mute').checked; v.controls=true;")+'</script></body></html>'
assert '\u2014' not in s and '\u2013' not in s
backup=PAGE/'index-R3-approved-assets.html'
if not backup.exists():backup.write_text((PAGE/'index.html').read_text())
(PAGE/'index.html').write_text(s);(O/'index.html').write_text(s)
print('R4 review page and VLC copies ready')
