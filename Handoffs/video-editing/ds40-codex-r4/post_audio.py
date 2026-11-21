import sys,json,subprocess,re,time
from pathlib import Path
W=Path(__file__).parent;R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');F=str(R/'Media/video_edit/bin/ffmpeg')
sys.path.insert(0,str(R/'.claude/skills/_shared'));import buildcap
while not (W/'graphics-manifest.json').exists():time.sleep(4)
buildcap.wait('Bill Maher R4 finished audio and caption alignment')
subprocess.run([sys.executable,str(R/'.claude/skills/_shared/audio/voice_chain.py'),'--in',str(W/'bill-original.wav'),'--out',str(W/'bill-finished.wav'),'--work',str(W/'audio-bill'),'--finish-only','--target','-14.1','--tp','-1.5','--oversample','4'],check=True)
def concat(a,b,out):
 subprocess.run([F,'-v','error','-y','-i',str(a),'-i',str(b),'-filter_complex','[0:a]aformat=channel_layouts=stereo[a];[1:a]aformat=channel_layouts=stereo[b];[a][b]concat=n=2:v=0:a=1[o]','-map','[o]','-c:a','pcm_s24le','-ar','48000',str(out)],check=True)
concat(W/'bill-finished.wav',W/'voice-balanced.wav',W/'mix.wav')
concat(W/'bill-original.wav',W/'lav.wav',W/'mix-untreated.wav')
sys.path.insert(0,str(R/'.claude/skills'));from _shared.cut import speech as S
bw,src=S.transcribe(str(W/'bill-original.wav'),'small',quiet=False)
(W/'bill-words.json').write_text(json.dumps({'words':bw,'source':src},indent=2))
sw=json.loads((W/'source-words.json').read_text());P=json.loads((W/'plan.json').read_text())
# The source document defines these exact sentences. Endpoint listening confirmed every word.
# Acoustic CTC will locate them on the actual mix, including quiet opening and closing words.
verified_bill=[('But let me ask you this.',0,1.36),('Have you ever seen a fat 90-year-old?',1.79,3.99),("Scary, isn't it?",8.99,9.89),('Healthy at any weight is an unchallenged lie.',15.4,19.4)]
words=[]
for text,a,b in verified_bill:
 toks=text.split()
 for j,tok in enumerate(toks):words.append({'w':tok,'t':a+(b-a)*j/len(toks),'e':a+(b-a)*(j+1)/len(toks),'source':'Verified original Bill Maher audio; acoustic CTC follows'})
off=P['opening_seconds']
for a,b in P['dialogue_ranges']:
 for x in sw:
  if a<=x['start'] and x['end']<=b:
   s=x['word'].strip()
   if s.startswith('-') and words:words[-1]['w']+=s;words[-1]['e']=off+x['end']-a;continue
   words.append({'w':s,'t':off+x['start']-a,'e':off+x['end']-a,'source':'C1730 roll sidecar'})
 off+=b-a
(W/'words-before-alignment.json').write_text(json.dumps({'words':words},indent=2))
# Use the existing CTC caption aligner, replacing only per-job input/output bindings.
code=(R/'.claude/skills/ad-edit/reference/ra13/round2/align.py').read_text()
code=code.replace("CUT = json.load(open('/Volumes/Extreme/_edit_work/ra13/cut.json'))", "CUT = json.load(open("+repr(str(W/'words-before-alignment.json'))+"))")
code=code.replace('FIX = {"apps": "abs", "app": "abs", "rip": "ripped"}','FIX = {}')
code=code.replace('w["w"].upper()', 'w["w"].upper().replace("90","NINETY")')
(W/'align.py').write_text(code)
subprocess.run([sys.executable,str(W/'align.py'),str(W/'mix.wav'),str(W/'words-aligned.json')],check=True)
subprocess.run([sys.executable,str(R/'.claude/skills/_shared/cut/junk.py'),P['source'],'--ranges',str(W/'dialogue-edl.json'),'--af','pan=mono|c0=c0','--out',str(W/'prerender-junk.json')],check=True)
subprocess.run([sys.executable,str(W/'bounded_alignment.py'),str(W/'mix.wav'),str(W/'words-aligned.json'),'premix'],check=True)
print('AUDIO AND ALIGNMENT COMPLETE',flush=True)
