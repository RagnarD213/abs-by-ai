from pathlib import Path
import json,re,subprocess,sys,os,hashlib
import numpy as np
W=Path(__file__).resolve().parents[1];R=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');F=R/'Media/video_edit/bin/ffmpeg';os.environ['PATH']=str(F.parent)+':'+os.environ['PATH'];sys.path.insert(0,str(R/'.claude/skills/_shared/hyperframes'));import composite as C;C.FF=str(F)
j=json.load(open(W/'round-controller.json'));assert j['productionOwner']=='01a182b7-eccb-7c82-aa31-9c48d25c0e76' and j['phase']=='complete'
old=W/'review/media/Why I Wear A Mouthpiece For SFC R2 - full 1080p.mp4';ctc=json.load(open(W/'evidence/checks/FULL-ctc-words.json'));assert ctc['video_sha256']==hashlib.sha256(old.read_bytes()).hexdigest();words=json.load(open(W/'records/full-words.json'));before=json.load(open(W/'records/FULL-captions.json'));ww={x['word_index']:x for x in ctc['words']};cues=[];n=1917;fps=30000/1001;dur=n/fps
for c in before:
 i=min(range(len(words)),key=lambda i:abs(words[i]['t0']-c['t0']));assert abs(words[i]['t0']-c['t0'])<1e-6
 count=len(c['text'].split());last=i+count-1;assert last<len(words);start=max(0,ww[i]['t']-.03);end=min(dur,ww[last]['e']+.05);cues.append(dict(t0=start,t1=end,text=c['text'],y=1436,word_indices=[i,last],original_t0=c['t0'],acoustic_onset=ww[i]['t'],ctc_score=ww[i]['score']))
for i,c in enumerate(cues):c['t1']=min(max(c['t1'],c['t0']+.35),cues[i+1]['t0']-.01 if i+1<len(cues) else dur);assert c['t1']>c['t0']
def ts(t):
 z=round(max(0,t)*100);return f'{z//360000}:{z//6000%60:02}:{z//100%60:02}.{z%100:02}'
header=(W/'records/FULL.ass').read_text().split('[Events]')[0]+'[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n'
ass=header+''.join(f'Dialogue: 0,{ts(c["t0"])},{ts(c["t1"])},Default,,0,0,0,,{{\\an8\\pos(540,1436)}}{c["text"]}\n' for c in cues)
(W/'records/FULL-aligned.ass').write_text(ass);(W/'records/FULL-aligned-captions.json').write_text(json.dumps(cues,indent=2));out=W/'review/media/Why I Wear A Mouthpiece For SFC R2 - full 1080p - aligned.mp4';assert not out.exists(),'Resume/review existing repaired output rather than overwrite'
cp=json.load(open(W/'records/context-plan.json'));meta={x['id']:x for x in json.load(open(W/'hf/graphics-meta.json'))};gg=[dict(id=g['id'],a=g['a'],b=g['b'],kind='glass',band=meta[g['id']]['band'],mov=str(W/f'hf/renders/{g["id"]}.mov'),mask=str(W/f'hf/renders/{g["id"]}_mask.mov')) for g in cp['graphics']];comp=C.Compositor(gg,wh=(1080,1920));head=C._Track(str(W/'hf/renders/T02.mov'),0,n+30,False,(1080,310))
enc=subprocess.Popen([str(F),'-nostdin','-v','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1080x1920','-framerate','30000/1001','-i','-','-i',str(old),'-map','0:v','-map','1:a:0','-frames:v',str(n),'-vf',f'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,ass={W}/records/FULL-aligned.ass','-c:v','libx264','-preset','fast','-crf','18','-c:a','copy','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-movflags','+faststart',str(out)],stdin=subprocess.PIPE)
count=0
for k,frame in enumerate(C.reader(str(W/'picture/FULL-graded.mp4'),n=n,wh=(1080,1920))):
 frame=comp.apply(frame.copy(),k);frame[:310]=head.frame(k);enc.stdin.write(np.ascontiguousarray(frame).tobytes());count+=1
enc.stdin.close();assert enc.wait()==0 and count==n
review=W/'review/media/Why I Wear A Mouthpiece For SFC R2 - REVIEW 540p - aligned.mp4';subprocess.run([str(F),'-nostdin','-v','error','-y','-i',str(out),'-vf','scale=540:960:in_color_matrix=bt709:in_range=tv','-c:v','libx264','-preset','fast','-crf','19','-c:a','copy','-movflags','+faststart',str(review)],check=True)
s=json.load(open(W/'execution-state.json'));s.update(checkpoint='caption_timing_repaired',master=str(out),review_copy=str(review),sha256=hashlib.sha256(out.read_bytes()).hexdigest(),prior_candidate=str(old),caption_timing_method='Cached local Wav2Vec2 forced alignment of exact source-confirmed transcript to delivered sound,30ms cue lead; words/chunks/layout preserved; exact originalAACstream copied');(W/'execution-state.json').write_text(json.dumps(s,indent=2));print('ALIGNED_CANDIDATE_READY',s['sha256'],flush=True)
