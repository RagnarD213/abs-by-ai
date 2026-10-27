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

def rebuild_bundle(recipe):
 recipe=Path(recipe);recipe.mkdir(parents=True,exist_ok=True)
 shutil.copytree(R/'parent',recipe/'parent',dirs_exist_ok=True)
 shutil.copy2(Path('/Volumes/Extreme/_edit_work/ro02/words_out.json'),recipe/'parent/words_out.json')
 code=recipe/'recipe';code.mkdir(exist_ok=True)
 for p in (R/'recipe').glob('*'):
  if p.is_file():shutil.copy2(p,code/p.name)
 # Preserve original evidence above; provide a separate correctly rooted rebuild tree.
 def rebase(value):
  if isinstance(value,str):return value.replace(str(R),str(recipe))
  if isinstance(value,list):return [rebase(x) for x in value]
  if isinstance(value,dict):return {k:rebase(v) for k,v in value.items()}
  return value
 for S in NAME:
  source=R/'build'/S;bd=recipe/'build'/S;bd.mkdir(parents=True,exist_ok=True)
  for name in ['timeline.json','shots.json','words.json','graphics.json']:
   dump(bd/name,rebase(json.loads((source/name).read_text())))
  shutil.copy2(source/'his_mix.wav',bd/'his_mix.wav')
  shutil.copytree(source/'hf',bd/'hf',dirs_exist_ok=True)
  if S in ['B','C']:
   shutil.copy2(source/'coverage-source-evidence.json',bd/'coverage-source-evidence.json')
   (bd/'independent').mkdir(exist_ok=True)
   shutil.copy2(source/'independent/coverage-adjudication.json',bd/'independent/coverage-adjudication.json')
   if S=='B':shutil.copy2(source/'independent/pause-adjudication.json',bd/'independent/pause-adjudication.json')
 ep=code/'edl.py';text=ep.read_text();text=text.replace('import json, wave, numpy as np','import json, wave, numpy as np\nfrom pathlib import Path');text=text.replace('W = '+repr(str(R/'parent')), 'W = str(Path(__file__).resolve().parents[1]/\'parent\')').replace('W = "'+str(R/'parent')+'"', 'W = str(Path(__file__).resolve().parents[1]/\'parent\')');ep.write_text(text)
 fp=code/'full.py';text=fp.read_text().replace("Path('/Volumes/Extreme/_edit_work/ro02/words_out.json')","(R/'parent/words_out.json')");fp.write_text(text)
 (recipe/'REBUILD.md').write_text('''# Rebuild the checked Shorts\n\nUse the nested recipe/ scripts; their parent is this bundle. build/A, B and C contain the exact approved audio, timeline, words, source shots and cached approved HyperFrames movies. Evidence under A/B/C preserves original paths and hashes. Rebuild metadata under build/ has local paths rebased without changing sound or pictures.\n\nRequires this project, its existing Python/FFmpeg dependencies, the approved RO-02 master and original C1622–C1626 rolls on Expansion. No generation calls or new voice decisions are needed. Preserve the approved B WAV; do not run prepare B.\n\nFrom the project folder, acquire the SL-11 edit slot with the shared editcap controller. Run `python3 <this bundle>/recipe/full.py render A B C`, then `python3 <this bundle>/recipe/coverage_evidence.py B` and `python3 <this bundle>/recipe/coverage_evidence.py C` to refresh source proof, then `python3 <this bundle>/recipe/finish.py checks A B C`. Both scripts enter the render queue. New exports require fresh independent review and delivery gates before delivery; old stamps are not reusable. Rebuilding does not approve or publish anything.\n''')

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
  for p in [d/'his_mix.wav',d/'timeline.json',d/'shots.json',d/'words.json',d/'cues.json',d/'graphics.json',d/'framing.json',d/'gate/plan.json',d/'gate/logs/watch_pass.json',d/'independent/findings.json']+([d/'coverage-source-evidence.json'] if S in ['B','C'] else []):
   dest=recipe/S/p.relative_to(d);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
  ad=recipe/S/'independent';ad.mkdir(parents=True,exist_ok=True)
  for ap in (d/'independent').glob('*.json'):shutil.copy2(ap,ad/ap.name)
  if S in ['B','C']:
   folder='original-instrument-fail' if S=='B' else 'original-palette-fail';shutil.copytree(d/'gate'/folder,recipe/S/'gate'/folder,dirs_exist_ok=True)
  rows.append(dict(short=S,title=NAME[S],file=str(v),sha256=h,seconds=T['seconds'],review_full=str(full),review_phone=str(films/f'Vacuum-{S}-R1-540p.mp4'),vlc=str(vc),audio_gate=str(ag),delivery_gate=str(dg),independent_watch=str(d/'gate/logs/watch_pass.json')))
 shutil.copytree(R/'parent',recipe/'parent',dirs_exist_ok=True)
 shutil.copytree(R/'audio/ai-voice',recipe/'pickup/ai-voice',dirs_exist_ok=True)
 shutil.copy2(R/'audio/pickup-choice.json',recipe/'pickup-choice.json')
 shutil.copy2(R/'audio/user-identified-player/Top-50-second-player-current-AI-Natural.wav',recipe/'pickup/Approved-50-second-AI-Natural-mix.wav')
 for p in [R/'phone-review-checks.json',R/'source-sidecar-used-receipt.json',R/'final-used-source-ranges.json']:shutil.copy2(p,recipe/p.name)
 shutil.copy2(R/'cost-ledger.json',recipe/'cost-ledger.json')
 (recipe/'pickup').mkdir(exist_ok=True)
 for p in [R/'audio/yeti-test/vaccuum pickup.aifc',R/'audio/yeti-test/take3-peak-safe.wav',R/'audio/ai-voice/natural-final.wav']:shutil.copy2(p,recipe/'pickup'/p.name)
 shutil.copy2(Path('/Volumes/Extreme/_edit_work/ro02/words_out.json'),recipe/'parent/words_out.json')
 rebuild_bundle(recipe)
 for p in [R/'decisions.json',R/'framing-graphics-approval.json',R/'demo-range.json',R/'audio/yeti-test/ingest.json',R/'audio/yeti-test/comparisons.json',R/'audio/yeti-test/independent/pickup-listening-review.json',R/'audio/yeti-test/independent/source-release-review.json']:shutil.copy2(p,recipe/p.name)
 dump(recipe/'delivery-manifest.json',dict(stage='Delivered for Dan review; unapproved; not uploaded or scheduled',films=rows));dump(R/'delivery-manifest.json',dict(stage='Checked films ready for Dan review',films=rows))
 cards=[]
 for row in rows:
  S=row['short'];cards.append(f'''<article><p class="tag">Short {S} · {row['seconds']:.1f} seconds</p><h2>{html.escape(row['title'])}</h2><video controls playsinline preload="metadata" poster="films/Vacuum-{S}-poster.jpg" src="films/Vacuum-{S}-R1-540p.mp4"></video><p><a href="films/Vacuum-{S}-R1-1080p.mp4" download>Download full quality</a> · <a href="films/Vacuum-{S}-R1-540p.mp4" download>Download phone copy</a></p></article>''')
 if not (rev/'opening-auditions.html').exists():shutil.copy2(rev/'index.html',rev/'opening-auditions.html')
 ap=rev/'opening-auditions.html';archive=ap.read_text()
 if 'approved-audio-archive-note' not in archive:
  shutil.copy2(ap,rev/'opening-auditions-original.html')
  archive=archive.replace('<main>','<main><div class="note" id="approved-audio-archive-note"><b>Earlier auditions, retained for reference.</b> Dan has since approved the saved 50-second AI Natural mix. That exact audio is in the completed Short B on the <a href="index.html">current review page</a>. Provisional wording below describes the earlier comparison stage.</div>',1);ap.write_text(archive)
 (rev/'index.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>The Vacuum · Three Shorts · R1</title><style>*{box-sizing:border-box}body{margin:0;background:#edf4fa;color:#16324c;font:17px/1.55 system-ui}main{max-width:1400px;margin:auto;padding:32px 26px 70px}h1{font-size:40px;line-height:1.15}h2{font-size:23px;line-height:1.25}.tag{font-size:13px;color:#54748f}.note,article{padding:20px;background:white;border:1px solid #bfd5e6;border-radius:14px}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px;margin-top:24px}video{width:100%;max-height:68vh;background:black}a{color:#135f94}article p:last-child{font-size:14px}@media(max-width:800px){.grid{grid-template-columns:1fr}h1{font-size:32px}video{max-height:75vh}}</style><main><p class="tag">CONTENT · THE VACUUM SFC R1 · A, B AND C</p><h1>Three Complete Shorts</h1><div class="note">Rendered and checked, including an independent review. <b>Awaiting Dan's review.</b><br>A and C use the original film audio. B opens with an AI version of Dan's own voice made from this shoot. Dan approved this exact AI Natural audio; the complete film awaits review. Original colour and Soft Blue Light graphics retained. No covers, uploads or scheduling.<p>Watch all three complete Shorts for the first full-film review. For B, listen especially to the opening transition at about0:04. Full-quality copies are also in the project's <b>Videos to Review</b> folder for VLC.</p></div><section class="grid">'''+''.join(cards)+'''</section><h2>Earlier opening auditions</h2><p>The approved audio is already in Short B above. <a href="opening-auditions.html">Open the audition archive</a>.</p></main></html>''')
 print('PACKAGE READY',json.dumps(rows,indent=1))
if __name__=='__main__':
 if sys.argv[1]=='stage':
  for S in sys.argv[2:] or NAME:stage(S)
 elif sys.argv[1]=='package':package()
