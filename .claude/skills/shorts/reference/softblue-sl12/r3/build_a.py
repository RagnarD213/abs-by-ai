"""A R3: approved Voice2, approved A1 motion, existing training/pushup assets."""
from pathlib import Path
import sys,json,math,os,hashlib,subprocess
ROOT=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI')
R=Path('/Volumes/Extreme/_edit_work/SL-12/round3');OLD=R.parent/'round1/asset-review'
sys.path.insert(0,str(Path(__file__).resolve().parents[1]));import packet as P
D=R/'build';D.mkdir(exist_ok=True);(R/'review').mkdir(exist_ok=True);P.OUT=D
FPS=P.FPS;NF=103;INTRO=NF/FPS;AI_FRAMES=61;AI_END=AI_FRAMES/FPS;CURL_END=(AI_FRAMES+61)/FPS;CAM_SKIP=round((CURL_END-INTRO)*FPS);A=347.8;NB=round((374.95-A)*FPS);N=NF+NB;DUR=N/FPS
VOICE=R.parent/'round2/audio/parent-conversational-matched.wav'
HEADER=D/'hf/renders/header-A-full-R3.mov';CARD=OLD/'hf/renders/card-A-v2.mov'
WORDS=json.loads((R.parent/'round2/audio/trial-parent-conversational/words.json').read_text())
for source,offset in [(OLD/'A-training/words.json',INTRO),(OLD/'A-movement/words.json',INTRO+366.9666-A)]:
 for w in json.loads(source.read_text()):WORDS.append(dict(w, t=round(w['t']+offset,6),e=round(w['e']+offset,6)))
(D/'words.json').write_text(json.dumps(WORDS,indent=2)+'\n');P.captions(WORDS,D/'captions.ass')
if not (D/'source-body.wav').exists():P.run([P.FF,'-v','error','-y','-ss',str(A),'-i',str(P.MASTER),'-t',str(NB/FPS),'-vn','-c:a','pcm_s16le',str(D/'source-body.wav')])
if not (D/'reference-mix.wav').exists():
 na=round(INTRO*48000);nb=round(NB/FPS*48000)
 P.run([P.FF,'-v','error','-y','-i',str(VOICE),'-i',str(D/'source-body.wav'),'-filter_complex',f'[0:a]aresample=48000,aformat=channel_layouts=stereo,apad=whole_len={na},atrim=end_sample={na},asetpts=PTS-STARTPTS[a];[1:a]atrim=end_sample={nb},asetpts=PTS-STARTPTS[b];[a][b]concat=n=2:v=0:a=1[au]','-map','[au]','-c:a','pcm_s16le',str(D/'reference-mix.wav')])
if not HEADER.exists():
 c=P.cfg_header('A',DUR);c['id']='header-A-full-R3'
 ht=D/'header.template.htm';ht.write_text((P.HF/'title-card/title-card.template.htm').read_text().replace('line-height: 1.4','line-height: 1.0').replace('id="lines"','id="lines" data-layout-allow-overlap="true"').replace('id="eyebrow"','id="eyebrow" data-layout-allow-overlap="true"').replace('height: 8px; border-radius: 3px','height: 36px; border-radius: 3px').replace('sp.textContent = w +','sp.setAttribute("data-layout-allow-overlap","true"); sp.textContent = w +'))
 P.V.build([(ht,c,())],D/'hf',render=True,snap=2)
if '--prepare' in sys.argv:print('A_PREPARED',flush=True);sys.exit(0)
MOTION=Path(sys.argv[1]);assert MOTION.exists()
out=R/'review/Keep Your Muscle - A - Weightlifting - R3.mp4'
if out.exists():raise SystemExit('Refusing to overwrite existing reviewed candidate')
ca=INTRO+167/FPS;cp=INTRO+560/FPS
font='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
g=f'[0:v]trim=start=1.5,setpts=PTS-STARTPTS,scale=in_color_matrix=bt601:in_range=tv,format=rgb24[bg];'
g+=f'[1:v]split=2[cw][ct];[cw]trim=start_frame={CAM_SKIP}:end_frame=84,setpts=PTS-STARTPTS,scale=in_color_matrix=bt709:in_range=tv,format=rgb24,crop=724:1080:646:0,scale=1080:1610:flags=lanczos,setsar=1[wide];[ct]trim=start_frame=84:end_frame=167,setpts=PTS-STARTPTS,scale=in_color_matrix=bt709:in_range=tv,format=rgb24,crop=604:900:706:0,scale=1080:1610:flags=lanczos,setsar=1[near];[wide][near]concat=n=2:v=1:a=0,setpts=PTS-STARTPTS+{CURL_END}/TB[cam];[bg][cam]overlay=0:310:eof_action=pass:format=rgb:enable=\'gte(t,{CURL_END})*lt(t,{ca})\'[base];'
g+=f'[2:v]fps=30000/1001,scale=in_color_matrix=bt709:in_range=tv,format=rgb24,scale=1080:1920:flags=lanczos,crop=1080:1610:0:310,trim=end_frame={AI_FRAMES},setpts=PTS-STARTPTS[ai];[base][ai]overlay=0:310:eof_action=pass:format=rgb:enable=\'lt(t,{AI_END})\'[aiopen];'
g+=f'[6:v]setpts=PTS-STARTPTS+{AI_END}/TB,crop=1080:1610:0:310,scale=in_color_matrix=bt709:in_range=tv,format=rgb24[curls];[aiopen][curls]overlay=0:310:eof_action=pass:format=rgb:enable=\'gte(t,{AI_END})*lt(t,{CURL_END})\'[open];'
g+=f'[3:v]setpts=PTS-STARTPTS+{ca}/TB,scale=in_color_matrix=bt601:in_range=tv,format=rgb24[card];[open][card]overlay=0:0:eof_action=pass:format=rgb:enable=\'gte(t,{ca})*lt(t,{cp})\'[training];'
g+=f'[4:v]setpts=PTS-STARTPTS+{cp}/TB,scale=in_color_matrix=bt709:in_range=tv,format=rgb24,crop=1440:1080:480:0,scale=1080:810:flags=lanczos[push];[training][push]overlay=0:310:eof_action=pass:format=rgb:enable=\'gte(t,{cp})\'[exercise];'
g+=f'[0:v]trim=start=1.5,setpts=PTS-STARTPTS,crop=1080:310:0:0,scale=in_color_matrix=bt601:in_range=tv,format=rgb24[header];[exercise][header]overlay=0:0:shortest=1:format=rgb,drawbox=x=66:y=354:w=310:h=58:color=0x132f49@0.92:t=fill:enable=\'lt(t,{AI_END})\',drawtext=fontfile=\'{font}\':text=\'AI-GENERATED\':fontsize=33:fontcolor=white:x=82:y=365:enable=\'lt(t,{AI_END})\',ass=\'{D/"captions.ass"}\',scale=out_color_matrix=bt709:out_range=tv,format=yuv420p[v]'
P.run([P.FF,'-v','error','-y','-i',str(HEADER),'-ss',str(A),'-i',str(P.MASTER),'-i',str(MOTION),'-i',str(CARD),'-ss','0.1678','-i','/Volumes/Extreme/_edit_work/ro01/assets/dan-pushups.mp4','-i',str(D/'reference-mix.wav'),'-ss',str(74/FPS),'-i',str(OLD/'A-intro-context.mp4'),'-filter_complex',g,'-map','[v]','-map','5:a','-frames:v',str(N),'-t',str(DUR),'-c:v','libx264','-preset','fast','-crf','18','-threads',os.environ.get('RENDERQ_CORES','4'),'-c:a','aac','-b:a','320k','-ar','48000','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-movflags','+faststart',str(out)])
spec=dict(frames=N,seconds=DUR,intro=INTRO,ai_end=AI_END,curls_end=CURL_END,curls_source_start=74/FPS,motion_frames=[0,49],body_source=[A,A+NB/FPS],card=[ca,cp],pushups=[cp,DUR],motion=str(MOTION),voice=str(VOICE),presenter_crop=[724,1080,646,0],near_crop=[604,900,706,0],near_at=INTRO+84/FPS,file=str(out),sha256=hashlib.sha256(out.read_bytes()).hexdigest())
(D/'A-spec.json').write_text(json.dumps(spec,indent=2)+'\n');print('COMPLETE_A_RENDERED',spec,flush=True)
