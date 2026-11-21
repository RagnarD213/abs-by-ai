"""Publish only checked A and the unchanged approved B on the existing owned review."""
from pathlib import Path
import json,shutil,hashlib,html,re,importlib.util,urllib.request,sys
from urllib.parse import quote
ROOT=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');R=Path('/Volumes/Extreme/_edit_work/SL-12/round3');O=R/'review'
A='Keep Your Muscle - A - Weightlifting - R3.mp4';B='Keep Your Muscle - B - Daily Protein - R2.mp4';av=O/A
gate=json.loads((R/'qa/A-final-clean/result.json').read_text());assert gate['verdict']=='PASS';assert all(x.get('ok') is not False for x in gate['rows'])
locked=json.loads((R/'build/A-spec.json').read_text());assert hashlib.sha256(av.read_bytes()).hexdigest()==locked['sha256']
stamp=json.loads(Path(str(av)+'.deliver_gate.json').read_text());assert stamp['verdict']=='PASS' and stamp['sha256']==locked['sha256'] and stamp['gate_version']==gate['gate_version']
sys.path.insert(0,str(ROOT/'.claude/skills/_shared/framecheck'));from clipcheck import require_pass
require_pass(locked['motion'],frames=tuple(locked['motion_frames']))
shutil.copyfile(R.parent/'round2/review'/B,O/B);assert hashlib.sha256((O/B).read_bytes()).hexdigest()=='dc37c605692b7d8c6bb09a3bc16b2fddf5f85dfd815a1eb3580719087f7b2e38'
shutil.copyfile(ROOT/'.claude/skills/_shared/review_player.js',O/'review_player.js')
for src,dest in [(R/'qa/A-final-clean/captions.srt','A-R3.srt'),(R/'qa/A-final-clean/result.json','A-checks.json'),(R/'qa/A-final-clean/independent-review.json','A-independent-review.json'),(R.parent/'round2/review/B-poster.jpg','B-poster.jpg')]:shutil.copyfile(src,O/dest)
import subprocess
subprocess.run([str(ROOT/'Media/video_edit/bin/ffmpeg'),'-v','error','-y','-ss','0.8','-i',str(av),'-frames:v','1',str(O/'A-poster.jpg')],check=True)
old=(R.parent/'round2/review/index.html').read_text();css=re.search(r'<style>(.*?)</style>',old,re.S).group(1)
aq,bq=quote(A),quote(B);s=json.loads((R/'build/A-spec.json').read_text())
page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keep Your Muscle SFC R3</title><style>{css}</style></head><body><main>
<p class="eyebrow">CONTENT · A AND B ONLY · ROUND 3</p><h1>Keep Your Muscle</h1>
<p class="status"><strong>A is ready for your review. B is approved.</strong> A uses your chosen Voice 2 and the checked AI clip made from your approved frames. No uploads or schedules. Publishing stays held until RO01 is confirmed public on or after December 6, 2026.</p>
<aside class="dock"><strong id="now">A · Weightlifting Is Mandatory</strong><video id="player" controls playsinline preload="metadata" poster="A-poster.jpg" src="{aq}"></video><p>Starts paused with sound ready. Use the timeline to seek.</p></aside>
<section class="panel"><h2>A: Weightlifting Is Mandatory</h2><p>The complete {s['seconds']:.1f}-second Short. Your chosen <strong>Voice 2</strong> opens over the new AI focus-pull clip and your real curls, followed by your original narration, the approved training card and complete real push-up repetitions.</p><button data-file="{aq}" data-poster="A-poster.jpg" data-name="A · Complete R3 Review Cut">Watch A</button><p><a href="{aq}" download>Download 1080p A</a> · <a href="A-R3.srt" download>Subtitles</a></p>
<blockquote>Here's why lifting weights is mandatory if you're taking weight loss medication.</blockquote>
<p><strong>Watch:</strong> 0:00–0:09 for the new voice/AI opening and its return to your original recording. The rest keeps the approved training graphic and real push-ups. Complete words and natural pauses are preserved at the ending.</p></section>
<section class="panel"><h2>B: Approved</h2><p>You approved the complete R2 protein Short on November 7. This is that same exact file, with its approved calculation graphic and original voice.</p><button data-file="{bq}" data-poster="B-poster.jpg" data-name="B · Approved R2 Cut">Watch Approved B</button><p><a href="{bq}" download>Download 1080p B</a></p></section>
<section class="panel"><h2>What I Decided, Overrule Anything</h2><ul><li>Use Voice 2 exactly as you selected it, with no new pitch or speed changes.</li><li>Keep the better checked AI focus pull. Reject takes with hands, changing props or unnatural camera movement.</li><li>Keep the approved title/graphic style, real exercise footage and original narration.</li><li>Hold the presenter framing steady within each wide or closer shot, with clear hair room.</li><li>Leave B locked to its approved file.</li></ul></section>
<section class="panel"><h2>Your Review</h2><p>Approve A or give any changes with timestamps. B needs no repeat approval.</p><textarea id="reply">A R3: Approve / Changes:</textarea><button id="copy">Copy Reply</button></section>
<details><summary>Checks And Limits</summary><p>A passed the maintained exact-file checks and a fresh independent review. The used AI excerpt passed the measured motion check and a separate reviewer before use. <a href="A-checks.json">A Check Report</a> · <a href="A-independent-review.json">Independent Review</a> · <a href="A-source-then-short.mp4">Audio Preservation Comparison</a>.</p><p>All automated playback tests stayed silent. Offline decoding, audio/source comparisons and native-frame inspections ran; no audible human listening pass is claimed. The AI voice remains an imitation of your own voice, selected by you.</p><p>Motion was generated and downloaded from Google Flow using your subscription. Rejected takes were preserved. No paid AI video API calls. The earlier four missing legacy audio fixture failures remain recorded; no quality threshold was changed.</p></details>
</main><script src="review_player.js"></script><script>
document.querySelectorAll('button[data-file]').forEach(b=>b.addEventListener('click',()=>{{const v=document.getElementById('player');v.pause();v.src=b.dataset.file;v.poster=b.dataset.poster;document.getElementById('now').textContent=b.dataset.name;v.load();if(window.matchMedia('(max-width:1000px)').matches)v.scrollIntoView({{behavior:'smooth',block:'center'}});v.play().catch(()=>{{}});}}));document.getElementById('copy').addEventListener('click',()=>navigator.clipboard.writeText(document.getElementById('reply').value));
</script></body></html>'''
(O/'index.html').write_text(page)
sp=importlib.util.spec_from_file_location('shared_review',ROOT/'.claude/skills/_shared/review_server.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
health=m.health(9954);parent=R.parent/'round1/asset-review';assert health and Path(health['root'])==parent
m.snapshot(O,parent/'round3');cache=Path(health['served_root']);m.snapshot(O,cache/'round3')
(parent/'index.html').write_text('''<!doctype html><html><head><meta charset="utf-8"><title>Keep Your Muscle Review</title></head><body><p><a href="round3/">Open current Keep Your Muscle review</a></p><script>location.replace('round3/'+location.search+location.hash);</script></body></html>''')
m.snapshot(parent,cache)
with urllib.request.urlopen('http://127.0.0.1:9954/round3/',timeout=5) as q:assert q.status==200
print('SL12_R3_REVIEW_READY http://127.0.0.1:9954/')
