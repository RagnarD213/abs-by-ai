from pathlib import Path
import json,subprocess,sys,os,hashlib,re
import numpy as np
W=Path(__file__).resolve().parents[1];R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');P1=W.parent/'round1'
F=R/'Media/video_edit/bin/ffmpeg';os.environ['PATH']=str(F.parent)+':'+os.environ['PATH']
j=json.load(open(W/'round-controller.json'));assert j['productionOwner']=='01a182b7-eccb-7c82-aa31-9c48d25c0e76' and j['phase']=='complete'
sys.path.insert(0,str(R/'.claude/skills/_shared/hyperframes'));import vertical as V,composite as C;C.FF=str(F)
fps=30000/1001;fr=lambda s:round(s*fps);plan=json.load(open(W/'edit-plan.json'));shots=json.load(open(W/'records/shots.json'));CP=json.load(open(W/'records/context-plan.json'));n=1917;dur=n/fps
# Preserve approved full-film word map, replacing only the previously corrected G03 timing region.
words=json.load(open(W/'mapped-words-corrected.json'));a=1489/fps
words=[x for x in words if x['t0']<a]+[dict(w=x['w'],t0=a+x['t0'],t1=a+x['t1']) for x in json.load(open(W/'records/G03-caption-words.json'))['words']]
(W/'records/full-words.json').write_text(json.dumps(words,indent=2));(W/'transcript.txt').write_text(' '.join(x['w'] for x in words))
chunks=[];cur=[]
for x in words:
 if cur and x['t0']-cur[-1]['t1']>.6:chunks.append(cur);cur=[]
 cur.append(x)
 if len(cur)>=3 or re.search('[.!?]$',x['w']):chunks.append(cur);cur=[]
if cur:chunks.append(cur)
def ts(t):
 c=round(max(0,t)*100);return f'{c//360000}:{c//6000%60:02}:{c//100%60:02}.{c%100:02}'
ass='[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\nStyle: Default,Arial,86,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,7,3,8,65,65,1436,1\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n';cues=[]
for i,c in enumerate(chunks):
 s=c[0]['t0'];e=min(max(c[-1]['t1'],s+.35),chunks[i+1][0]['t0']-.01 if i+1<len(chunks) else dur);txt=re.sub(r'\s+([,.!?])',r'\1',' '.join(x['w'] for x in c))
 if e<=s:continue
 ass+=f'Dialogue: 0,{ts(s)},{ts(e)},Default,,0,0,0,,{{\\an8\\pos(540,1436)}}{txt}\n';cues.append(dict(t0=s,t1=e,text=txt,y=1436))
(W/'records/FULL.ass').write_text(ass);(W/'records/FULL-captions.json').write_text(json.dumps(cues,indent=2))
head=dict(id='T02',dur=(n+30)/fps,canvas=[1080,310],drift=-2,line_px=72,accent=[64,50,68],eyebrow=dict(x=64,y=61,px=30,s='CARDIO & WEIGHTLIFTING'),lines=[dict(x=64,y=108,s='Why I Wear'),dict(x=64,y=194,s='A Mouthpiece')])
V.build([(V.HERE/'title-card/title-card.template.htm',head,())],W/'hf',render=True,snap=2)
def ff(args):subprocess.run([str(F),'-nostdin','-v','error','-y']+list(map(str,args)),check=True)
parts=[]
for i,s in enumerate(shots):
 out=W/f'picture/shot-{i:02d}.mp4';parts.append(out)
 if out.exists():continue
 cw,ch,y=s['crop'];xs=np.round(np.array(s['centre'])-cw/2).astype(int);expr=str(xs[0])+''.join(f'{int(d):+d}*gte(n,{k})' for k,d in enumerate(np.diff(xs),1) if d)
 ff(['-ss',s['source_in'],'-i',plan['pieces'][0]['source'],'-an','-frames:v',s['n'],'-vf',f"setpts=PTS-STARTPTS,crop={cw}:{ch}:x='{expr}':y={y},scale=1080:1610:flags=lanczos:in_color_matrix=bt709:in_range=tv,pad=1080:1920:0:310:black",'-r','30000/1001','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',out]);print('SHOT_READY',i,flush=True)
cat=W/'picture/concat.txt';cat.write_text(''.join(f"file '{p}'\n" for p in parts));base=W/'picture/FULL-base.mp4';ff(['-f','concat','-safe',0,'-i',cat,'-c','copy',base]);graded=W/'picture/FULL-graded.mp4'
ff(['-i',base,'-an','-vf',json.load(open(W/'look-options.json'))['colours']['B']['vf'],'-c:v','libx264','-preset','fast','-crf','18','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',graded])
meta={x['id']:x for x in json.load(open(W/'hf/graphics-meta.json'))};gg=[dict(id=g['id'],a=g['a'],b=g['b'],kind='glass',band=meta[g['id']]['band'],mov=str(W/f'hf/renders/{g["id"]}.mov'),mask=str(W/f'hf/renders/{g["id"]}_mask.mov')) for g in CP['graphics']]
comp=C.Compositor(gg,wh=(1080,1920));headtrack=C._Track(str(W/'hf/renders/T02.mov'),0,n+30,False,(1080,310));out=W/'review/media/Why I Wear A Mouthpiece For SFC R2 - full 1080p.mp4'
enc=subprocess.Popen([str(F),'-nostdin','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-framerate','30000/1001','-i','-','-i',str(W/'audio/voice-selected.wav'),'-map','0:v','-map','1:a','-frames:v',str(n),'-vf',f'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,ass={W}/records/FULL.ass','-c:v','libx264','-preset','fast','-crf','18','-c:a','aac','-b:a','192k','-ar','48000','-ac','2','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart',str(out)],stdin=subprocess.PIPE)
count=0
for k,frame in enumerate(C.reader(str(graded),n=n,wh=(1080,1920))):
 frame=comp.apply(frame.copy(),k);frame[:310]=headtrack.frame(k);enc.stdin.write(np.ascontiguousarray(frame).tobytes());count+=1
enc.stdin.close();assert enc.wait()==0;assert count==n
review=W/'review/media/Why I Wear A Mouthpiece For SFC R2 - REVIEW 540p.mp4';ff(['-i',out,'-vf','scale=540:960:in_color_matrix=bt709:in_range=tv','-c:v','libx264','-preset','fast','-crf','19','-c:a','copy','-movflags','+faststart',review])
state=json.load(open(W/'execution-state.json'));state.update(checkpoint='full_candidate_rendered',master=str(out),sha256=hashlib.sha256(out.read_bytes()).hexdigest(),nativeFrames=count);(W/'execution-state.json').write_text(json.dumps(state,indent=2));print('FULL_CANDIDATE_READY',out,flush=True)
