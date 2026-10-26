"""Package only exact, checked SL11 masters. No uploads, covers or publication."""
from pathlib import Path
import json,sys,shutil,subprocess,html
from full import ROOT,R,sha,dump,FPS
NAME={'A':'How To Do A Standing Stomach Vacuum','B':'Stop Holding Your Breath During Stomach Vacuums','C':'Start With One 20-Second Vacuum Every Morning'}
def target(S):return ROOT/'Short-form video content'/f"vacuum-short{list(NAME).index(S)+1}_{NAME[S]}.mp4"
def stage(S):
 d=R/'build'/S;v=d/f'Vacuum-{S}-R1.mp4';out=target(S);shutil.copy2(v,out);assert sha(v)==sha(out)
 ast=Path(str(v)+'.audio_gate.json');a=json.loads(ast.read_text());assert a.get('verdict')=='PASS' and a['sha256']==sha(v),a
 shutil.copy2(ast,Path(str(out)+'.audio_gate.json'));print('EXACT MASTER STAGED',S,out,flush=True);return out

def package():
 rows=[];rev=R/'review';films=rev/'films';vlc=ROOT/'Videos to Review';vlc.mkdir(exist_ok=True);recipe=ROOT/'Short-form video content/recipe-vacuum-R1';recipe.mkdir(exist_ok=True)
 for S in NAME:
  d=R/'build'/S;v=target(S);h=sha(v);dg=Path(str(v)+'.deliver_gate.json');ag=Path(str(v)+'.audio_gate.json');dd=json.loads(dg.read_text());aa=json.loads(ag.read_text());watch=json.loads((d/'gate/logs/watch_pass.json').read_text());fr=json.loads((d/'framing.json').read_text());T=json.loads((d/'timeline.json').read_text())
  assert dd['verdict']=='PASS' and dd['sha256']==h,(S,'delivery gate');assert aa['verdict']=='PASS' and aa['sha256']==h,(S,'audio gate');assert watch['sha256']==h and watch['inspected'] and watch['open_defects']==0,(S,'independent watch');assert fr['sha256']==h and fr['min_hair_clearance']>=20
  phone=films/f'Vacuum-{S}-R1-540p.mp4';pa=json.loads(Path(str(phone)+'.audio_gate.json').read_text());assert pa['verdict']=='PASS' and pa['sha256']==sha(phone),(S,'phone audio gate')
  full=films/f'Vacuum-{S}-R1-1080p.mp4';shutil.copy2(v,full);assert sha(full)==h
  shutil.copy2(d/'proof/f0000.jpg',films/f'Vacuum-{S}-poster.jpg')
  for st in [ag,dg]:shutil.copy2(st,Path(str(full)+str(st)[len(str(v)):]))
  vc=vlc/f'The Vacuum SFC R1 - Short {S} - {NAME[S]}.mp4';shutil.copy2(v,vc);assert sha(vc)==h
  for p in [d/'timeline.json',d/'shots.json',d/'words.json',d/'cues.json',d/'graphics.json',d/'framing.json',d/'gate/plan.json',d/'gate/logs/watch_pass.json',d/'gate/logs/findings.json']+([d/'coverage-source-evidence.json'] if S=='C' else []):
   dest=recipe/S/p.relative_to(d);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
  ad=recipe/S/'independent';ad.mkdir(parents=True,exist_ok=True)
  for ap in (d/'independent').glob('*.json'):shutil.copy2(ap,ad/ap.name)
  if S=='C':shutil.copytree(d/'gate/original-palette-fail',recipe/S/'gate/original-palette-fail',dirs_exist_ok=True)
  rows.append(dict(short=S,title=NAME[S],file=str(v),sha256=h,seconds=T['seconds'],review_full=str(full),review_phone=str(films/f'Vacuum-{S}-R1-540p.mp4'),vlc=str(vc),audio_gate=str(ag),delivery_gate=str(dg),independent_watch=str(d/'gate/logs/watch_pass.json')))
 shutil.copytree(R/'parent',recipe/'parent',dirs_exist_ok=True)
 shutil.copytree(R/'audio/ai-voice',recipe/'pickup/ai-voice',dirs_exist_ok=True)
 shutil.copy2(R/'audio/pickup-choice.json',recipe/'pickup-choice.json')
 shutil.copy2(R/'cost-ledger.json',recipe/'cost-ledger.json')
 (recipe/'pickup').mkdir(exist_ok=True)
 for p in [R/'audio/yeti-test/vaccuum pickup.aifc',R/'audio/yeti-test/take3-peak-safe.wav',R/'audio/ai-voice/natural-final.wav']:shutil.copy2(p,recipe/'pickup'/p.name)
 shutil.copy2(Path('/Volumes/Extreme/_edit_work/ro02/words_out.json'),recipe/'parent/words_out.json')
 for p in (R/'recipe').glob('*'):
  if p.is_file():shutil.copy2(p,recipe/p.name)
 for p in [R/'decisions.json',R/'framing-graphics-approval.json',R/'demo-range.json',R/'audio/yeti-test/ingest.json',R/'audio/yeti-test/comparisons.json',R/'audio/yeti-test/independent/pickup-listening-review.json',R/'audio/yeti-test/independent/source-release-review.json']:shutil.copy2(p,recipe/p.name)
 dump(recipe/'delivery-manifest.json',dict(stage='Delivered for Dan review; unapproved; not uploaded or scheduled',films=rows));dump(R/'delivery-manifest.json',dict(stage='Checked films ready for Dan review',films=rows))
 cards=[]
 for row in rows:
  S=row['short'];cards.append(f'''<article><p class="tag">Short {S} · {row['seconds']:.1f} seconds</p><h2>{html.escape(row['title'])}</h2><video controls playsinline preload="metadata" poster="films/Vacuum-{S}-poster.jpg" src="films/Vacuum-{S}-R1-540p.mp4"></video><p><a href="films/Vacuum-{S}-R1-1080p.mp4" download>Download full quality</a> · <a href="films/Vacuum-{S}-R1-540p.mp4" download>Download phone copy</a></p></article>''')
 if not (rev/'opening-auditions.html').exists():shutil.copy2(rev/'index.html',rev/'opening-auditions.html')
 (rev/'index.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>The Vacuum · Three Shorts · R1</title><style>*{box-sizing:border-box}body{margin:0;background:#edf4fa;color:#16324c;font:17px/1.55 system-ui}main{max-width:1400px;margin:auto;padding:32px 26px 70px}h1{font-size:40px;line-height:1.15}h2{font-size:23px;line-height:1.25}.tag{font-size:13px;color:#54748f}.note,article{padding:20px;background:white;border:1px solid #bfd5e6;border-radius:14px}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px;margin-top:24px}video{width:100%;max-height:68vh;background:black}a{color:#135f94}article p:last-child{font-size:14px}@media(max-width:800px){.grid{grid-template-columns:1fr}h1{font-size:32px}video{max-height:75vh}}</style><main><p class="tag">CONTENT · THE VACUUM SFC R1 · A, B AND C</p><h1>Three Complete Shorts</h1><div class="note">Rendered and checked, including an independent review. <b>Awaiting Dan's review.</b><br>A and C use the original film audio. B opens with an AI version of Dan's own voice made from this shoot. Dan approved this exact AI Natural audio; the complete film awaits review. Original colour and Soft Blue Light graphics retained. No covers, uploads or scheduling.<p>Watch all three complete Shorts for the first full-film review. For B, listen especially to the opening transition at about0:04. Full-quality copies are also in the project's <b>Videos to Review</b> folder for VLC.</p></div><section class="grid">'''+''.join(cards)+'''</section><h2>Opening Audio Comparison</h2><p>Compare AI Natural with the recorded Yeti opening:</p><audio controls preload="none" src="audio/AI-natural-final-joined.wav"></audio><audio controls preload="none" src="audio/Yeti-final-joined.wav"></audio><p><a href="opening-auditions.html">All opening auditions</a></p></main></html>''')
 print('PACKAGE READY',json.dumps(rows,indent=1))
if __name__=='__main__':
 if sys.argv[1]=='stage':
  for S in sys.argv[2:] or NAME:stage(S)
 elif sys.argv[1]=='package':package()
