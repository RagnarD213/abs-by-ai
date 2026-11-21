from pathlib import Path
import json,hashlib,subprocess,re,numpy as np
R=Path(__file__).resolve().parents[4];W=Path('/Volumes/Expansion/_edit_work/ds16-publish');W.mkdir(parents=True,exist_ok=True)
FF=str(R/'Media/video_edit/bin/ffmpeg');FP=str(R/'Media/video_edit/bin/ffprobe')
A=Path('/Volumes/Extreme/_edit_work/revisions-20261103/muhammad/dl/ds16_v3.mp4');B=Path('/Volumes/Extreme/_edit_work/revisions-20261104/muhammad/dl/Daniel Ads DS-16 How To Lose The Last Ten Pounds Of Fat V3 HD.mp4')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def probe(p):return json.loads(subprocess.check_output([FP,'-v','error','-show_streams','-show_format','-of','json',str(p)]))
a,b=probe(A),probe(B);av,bv=[next(s for s in p['streams'] if s['codec_type']=='video') for p in [a,b]]
assert B.stat().st_size==69460867
assert all(av[k]==bv[k] for k in ['width','height','nb_frames','r_frame_rate','duration'])
stats=W/'hq-full-frame-difference.txt'
subprocess.run([FF,'-v','error','-i',str(A),'-i',str(B),'-filter_complex',f'[0:v][1:v]blend=all_mode=difference,signalstats,metadata=print:file={stats}','-an','-f','null','-'],check=True)
vals=[float(x) for x in re.findall(r'lavfi.signalstats.YAVG=([\d.]+)',stats.read_text())];assert len(vals)==1540
# Same-time, fully decoded PCM comparison, without speaker playback.
def pcm(p):return np.frombuffer(subprocess.check_output([FF,'-v','error','-i',str(p),'-vn','-ac','2','-ar','48000','-f','f32le','-']),dtype=np.float32)
x,y=pcm(A),pcm(B);n=min(len(x),len(y));x,y=x[:n],y[:n];corr=float(np.corrcoef(x,y)[0,1]);rms=float(np.sqrt(np.mean((x-y)**2)));signal=float(np.sqrt(np.mean(x*x)));snr=float(20*np.log10(signal/rms))
report={'reference':{'path':str(A),'sha256':sha(A)},'hq':{'path':str(B),'sha256':sha(B),'md5':hashlib.md5(B.read_bytes()).hexdigest(),'bytes':B.stat().st_size,'drive_id':'1-GGtoEbTEtjn433cZbpc7N4TAP_-9goh'},'format_match':True,'frames':1540,'duration':float(bv['duration']),'fps':bv['r_frame_rate'],'resolution':[bv['width'],bv['height']],'picture':{'method':'Every native1080x1920 aligned frame subtracted, luma mean measured.','mean_luma_absolute_difference_255':float(np.mean(vals)),'max_frame_mean_luma_absolute_difference_255':float(max(vals)),'frames_over_5':sum(v>5 for v in vals)},'audio':{'method':'Offline stereo48000Hz PCM aligned comparison; no audible listening.','samples_compared':n,'correlation':corr,'difference_rms':rms,'signal_to_difference_db':snr},'prior_independent_check':'revision docs/shorts-closeout-muhammad-11-4-26.summary.md','dan_hq_approval':'2026-11-04 18:06 Central Upwork: The Last Ten Pounds HQ is perfect, so that one’s done.'}
report['matches_approved_edit']=max(vals)<5 and corr>.99
(W/'hq-verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2));assert report['matches_approved_edit']
