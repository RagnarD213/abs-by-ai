"""DS-30 R1 finish: HyperFrames overlays (graphics-manifest.json via the shared Compositor) over base.mp4, burned captions
(DS-28/DS-31 style), approved-method voice, 1080p master + SRT + graphic stills. No AI imagery in this Short: no AI chip.
Usage: python3 finish.py [--voice voice.wav] [--name NAME]
"""
from pathlib import Path
import subprocess, json, sys, os, re, hashlib
import numpy as np
from PIL import Image
R = Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI'); W = Path(__file__).resolve().parents[1]; Q = W/'review'; Q.mkdir(exist_ok=True)
F = str(R/'Media/video_edit/bin/ffmpeg'); FPS = 30000/1001
os.environ['PATH'] = str(R/'Media/video_edit/bin') + ':' + os.environ['PATH']
sys.path.insert(0, str(R/'.claude/skills/_shared/hyperframes')); import composite as HC
import importlib.util
spec = importlib.util.spec_from_file_location('hg', R/'scripts/video/hyperframes_graphics.py'); HG = importlib.util.module_from_spec(spec); spec.loader.exec_module(HG); C = HG.module('composite')
args = sys.argv[1:]
VOICE = Path(args[args.index('--voice') + 1]) if '--voice' in args else W/'voice.wav'
NAME = args[args.index('--name') + 1] if '--name' in args else 'Self-Driving Car SFC R1'
def ff(a): subprocess.run([F, '-nostdin', '-v', 'error', '-y'] + list(map(str, a)), check=True)
TOTAL = json.load(open(W/'edl.json'))['total_frames']
man = json.load(open(W/'graphics-manifest.json'))
CO = HC.Compositor(man, wh=(1080, 1920))
comp = W/'composite.mp4'
if '--reuse-composite' not in args or not comp.exists():
    cmd = [F, '-nostdin', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1080x1920', '-framerate', '30000/1001', '-i', '-', '-an',
           '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p', '-c:v', 'libx264', '-preset', 'fast', '-crf', '17',
           '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv', str(comp)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE); still = {}
    for n, f in enumerate(C.reader(str(W/'base.mp4'), wh=(1080, 1920))):
        if CO.opaque(n): f = CO.apply(None, n)
        else: f = CO.apply(np.ascontiguousarray(f), n)
        for m in man:
            if n == round(m['b']*FPS) - 12: still[m['id']] = np.array(f)
        p.stdin.write(np.ascontiguousarray(f).astype(np.uint8).tobytes())
    p.stdin.close(); assert p.wait() == 0; assert n + 1 == TOTAL, (n + 1, TOTAL)
    for gid, f in still.items(): Image.fromarray(f.astype(np.uint8)).save(Q/f'{gid}.jpg', quality=92)

master = Q/f'{NAME} - complete Short.mp4'
ff(['-i', comp, '-i', VOICE, '-map', '0:v', '-map', '1:a', '-vf', f"ass='{W}/captions.ass'", '-c:v', 'libx264', '-preset', 'slow', '-crf', 17,
    '-c:a', 'aac', '-b:a', '256k', '-ar', 48000, '-frames:v', TOTAL, '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv', '-movflags', '+faststart', master])
ff(['-ss', 4.0, '-i', master, '-frames:v', 1, '-vf', 'scale=540:960', Q/'poster.jpg'])
def secs(x): h, m, s = x.split(':'); return int(h)*3600 + int(m)*60 + float(s)
def stamp(x): ms = round(x*1000); return f'{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}'
cues = []
for line in (W/'captions.ass').read_text().splitlines():
    if line.startswith('Dialogue:'): f_ = line.split(',', 9); cues.append((secs(f_[1]), secs(f_[2]), re.sub(r'\{[^}]*\}', '', f_[9])))
(Q/f'{NAME}.srt').write_text(''.join(f'{i+1}\n{stamp(a)} --> {stamp(b)}\n{x}\n\n' for i, (a, b, x) in enumerate(cues)))
print('FINISHED', master, hashlib.sha256(master.read_bytes()).hexdigest(), flush=True)
