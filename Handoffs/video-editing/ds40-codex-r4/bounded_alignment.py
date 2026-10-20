from pathlib import Path
import sys,json,subprocess,hashlib,re
W=Path(__file__).parent;F='/Users/danielrose/Documents/Claude/Projects/Abs By AI/Media/video_edit/bin/ffmpeg'
def repair(media,words_path,tag):
 media=Path(media);words_path=Path(words_path);clip=W/f'{tag}-scary-window.wav';out=W/f'{tag}-scary-aligned.json'
 subprocess.run([F,'-y','-v','error','-ss','8.0','-i',str(media),'-t','2.25','-ac','1','-ar','16000','-c:a','pcm_s16le',str(clip)],check=True)
 subprocess.run([sys.executable,str(W/'align-scary.py'),str(clip),str(out)],check=True)
 local=json.loads(out.read_text())['words'];d=json.loads(words_path.read_text());ws=d['words']
 indices=[i for i,x in enumerate(ws) if re.sub('[^a-z]','',x['w'].lower())=='scary'];assert len(indices)==1
 k=indices[0];assert [re.sub('[^a-z]','',x['w'].lower()) for x in ws[k:k+3]]==['scary','isnt','it']
 assert 8.3<=8+local[0]['t']<=9.3 and 8+local[-1]['e']<10.25
 old=ws[k:k+3]
 for j,x in enumerate(local):ws[k+j]=dict(ws[k+j],t=round(8+x['t'],3),e=round(8+x['e'],3),src='ctc_bounded_original_audio')
 d['bounded_alignment']={'phrase':"Scary, isn't it?",'source_media':str(media),'window':[8,10.25],'audio_window_sha256':hashlib.sha256(clip.read_bytes()).hexdigest(),'reason':'Whole-file CTC assigned the initial S to audience noise, stretching Scary over 5 seconds. A local acoustic pass isolates the actual phrase.','original_measurements':old,'corrected_measurements':ws[k:k+3]}
 words_path.write_text(json.dumps(d,indent=2));print('Bounded phrase timing measured on',media,flush=True)
if __name__=='__main__':repair(sys.argv[1],sys.argv[2],sys.argv[3])
