from pathlib import Path
import sys,json,hashlib,cv2,numpy as np,subprocess,time
W=Path(__file__).parent;R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI')
sys.path.insert(0,str(R/'.claude/skills/_shared'));import buildcap
while not (W/'watch/watch_pass.json').exists():time.sleep(3)
buildcap.wait('Bill Maher R4 parent native scene and freeze evidence')
sys.path.insert(0,str(R/'.claude/skills/_shared/audio'));import common as C
A=json.loads((W/'assembly.json').read_text());P=json.loads((W/'plan.json').read_text());v=A['master'];fps=A['fps'];d={'sha256':C.sha256(v),'checks':{},'freeze_dispositions':[]};assert d['sha256']==A['sha256']
refs=[('R3 key',W.parent/'round3/review/media/sample.mp4','1c07c3d3c585fe05a7a2f1274d4a62bec46de1e6be7bdbfb4214f44af2b7ace1'),('Balanced voice',W.parent/'round2/voice-balanced.wav','089264175840f8aa4956d98a7e8bd82d93bd8c1dcee73493d4733ae224df2a6f'),('warm grade',W/'grade.py','d6d2c4cd854088f4383649f4b9929631a7f2c3d409c8dd08d1db41a916f600ce')]
for name,p,h in refs:got=C.sha256(str(p));assert got==h;d['checks'][name]={'sha256':got,'reference_unchanged':True}
x=C.pcm(str(W.parent/'round2/voice-balanced.wav'));y=C.pcm(str(W/'review/media/r4-voice-check.wav'));n=min(len(x),len(y));r=float(np.corrcoef(x[:n],y[:n])[0,1]);gain=20*np.log10(np.sqrt(np.mean(y[:n]**2))/np.sqrt(np.mean(x[:n]**2)));d['checks']['same_passage_voice']={'correlation':r,'rms_gain_db':float(gain),'seconds':n/48000}
w=json.loads((W/'watch/watch_pass.json').read_text());cap=cv2.VideoCapture(v);events=w['scan']['frozen'];bmi=np.asarray(__import__('PIL.Image',fromlist=['Image']).open(W/'bmi-table.png').convert('RGB'))[:,:,::-1]
for e in events:
 a=round(e['t']*fps);b=min(A['frames'],a+round(e['seconds']*fps));cap.set(cv2.CAP_PROP_POS_FRAMES,max(0,a-2));prev=None;diff=[];same=0
 for k in range(max(0,a-2),min(A['frames'],b+3)):
  ok,fr=cap.read();assert ok
  field=fr[100:1370,:].copy();field[140:1260,36:1044]=0
  if prev is not None:
   delta=np.abs(field.astype(np.int16)-prev.astype(np.int16));diff.append(float(delta.mean()));same+=int(not delta.any())
  prev=field
 d['freeze_dispositions'].append(dict(e,actual_pixels='Height/weight BMI table, continuous shared Soft Blue Light field and accent. No presenter hold.',native_field_mean_abs_diff_min=min(diff),native_field_mean_abs_diff_max=max(diff),identical_adjacent_native_field_frames=same,inspected_native_pairs=len(diff)))
cap.set(cv2.CAP_PROP_POS_FRAMES,1500);ok,fr=cap.read();assert ok;d['checks']['BMI_table_actual_pixels']={'mean_absolute_rgb_difference_from_independent_table':float(np.abs(fr[240:1360,36:1044].astype(float)-bmi).mean()),'independent_table_sha256':C.sha256(str(W/'bmi-table.png')),'cells':81}
cap.release()
for t in [19.6196,32.399,42.5094,55.7474,60.6606]:
 assert t<A['duration']
d['required_scenes']=['Bill Maher original excerpt first','Dan actual silent watching','complete scripted response','G02 belly fat emergency','G03 numeric height/weight BMI table through all three lines','return to Dan with G04 subscribe']
d['limits']=['Parent continuous sampled AV and complete audio review were on internal candidate C; final D differs only in one caption frame. Final native watch, direct AAC CTC and independent review bind final D.','This report does not claim full native human playback or a numerical temporal hair pass.','Caption timing gate measures chunk onsets, not individual word highlights.']
(W/'parent-self-qa.json').write_text(json.dumps(d,indent=2));print(json.dumps(d,indent=2))
