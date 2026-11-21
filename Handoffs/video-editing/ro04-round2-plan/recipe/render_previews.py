from pathlib import Path
import sys,json,subprocess,hashlib
import build as B
sys.path.insert(0,str(B.P/'.claude/skills/_shared'));import buildcap
buildcap.wait('Arms Shoulders Workout R2 previews')
for g in ['OLD','A','B','C']:
 B.render(f'context/color-{g}.mp4',9,17,g,'B',False)
B.render('Arms Shoulders Workout LFC R2 - first minute.mp4',0,1789/B.FPS,'B','B')
B.render('context/overhead-crop-check.mp4',70,86,'B','B')
# Flat camera only proof of the exact first-minute picture before the unchanged graphics.
subprocess.run([B.FF,'-v','error','-ss',str(B.START),'-i',B.RAW,'-frames:v','1789','-vf',B.vf('B','B'),'-an','-c:v','h264_videotoolbox','-b:v','12M','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-y',str(B.W/'qa/picture-before-graphics.mp4')],check=True)
print('All revised preview renders complete',flush=True)
