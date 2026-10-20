import json,sys,subprocess,time
from pathlib import Path
W=Path(__file__).parent;R=Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI');F=str(R/'Media/video_edit/bin/ffmpeg')
# Keep one slot for the dialogue renderer. This preparation follows the completed opening.
while not (W/'opening-render-stop.json').exists():time.sleep(3)
sys.path.insert(0,str(R/'.claude/skills/_shared'));import buildcap
buildcap.wait('Bill Maher R4 complete-word clip finish')
P=json.loads((W/'plan.json').read_text())
subprocess.run([F,'-y','-v','error','-ss',str(P['bill_source_start']),'-i',str(W/'bill-maher-source.f251.webm'),'-t',str(P['opening_seconds']),'-ac','2','-ar','48000','-c:a','pcm_s24le',str(W/'bill-original.wav')],check=True)
subprocess.run([sys.executable,str(W/'graphics.py')],check=True)
subprocess.run([sys.executable,str(W/'post_audio.py')],check=True)
subprocess.run([sys.executable,str(W/'render_watch_tail_key.py')],check=True)
subprocess.run([sys.executable,str(R/'.claude/skills/_shared/cut/junk.py'),P['source'],'--ranges',str(W/'dialogue-edl.json'),'--af','pan=mono|c0=c0','--out',str(W/'prerender-junk.json')],check=True)
(W/'preparation-complete.json').write_text(json.dumps({'clip_start':P['bill_source_start'],'clip_end':P['bill_source_end'],'opening_frames':588},indent=2))
print('ALL PREPARATION COMPLETE',flush=True)
