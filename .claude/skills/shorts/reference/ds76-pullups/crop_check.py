"""Library record (path, approved grade/exercise, master sha) and every insert at its planned crop, every 4th frame tiled."""
from pathlib import Path
import subprocess, json, os, sys, hashlib
R = Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI'); W = Path(__file__).resolve().parents[1]; F = R/'Media/video_edit/bin/ffmpeg'
LIB = Path('/Volumes/Extreme/_asset_library_stage/Abs By AI - Video Asset Library/03 B-Roll - Real Footage/dan-filmed')
cat = json.load(open(R/'Media/clip-library/catalog.json')); cat = {c['id']: c for c in (cat['clips'] if isinstance(cat, dict) else cat)}
V = json.load(open(W/'records/visual-plan.json')); D = W/'evidence/crops'; D.mkdir(exist_ok=True)
lib = {}
for k in sorted({u['lib'] for u in V['assets']}):
    p = next(LIB.glob(k+'_*.mp4')); c = cat[k]
    sha = hashlib.sha256(p.read_bytes()).hexdigest()
    assert sha == c['approval']['checked_master_sha256'], (k, 'master differs from the checked one')
    lib[k] = dict(path=str(p), sha256=sha, duration=c['duration'], exercise=c.get('exercise'), approval=c['approval'], description=c['description'])
(W/'records/library.json').write_text(json.dumps(lib, indent=2))
for u in V['assets']:
    x, y, cw, ch = u['crop']; d = u['b']-u['a']
    assert u['start']+d <= lib[u['lib']]['duration']+0.02, (u['id'], 'runs past the master')
    n = round(d*30000/1001); cols = 8; rows = (n//4+cols-1)//cols
    subprocess.run([str(F), '-nostdin', '-v', 'error', '-y', '-ss', str(u['start']), '-i', lib[u['lib']]['path'], '-frames:v', str(n),
                    '-vf', f"select='not(mod(n\\,4))',crop={cw}:{ch}:{x}:{y},scale=180:-2:in_color_matrix=bt709:in_range=tv,tile={cols}x{rows}",
                    '-frames:v', '1', str(D/f"{u['id']}.jpg")], check=True)
    print(u['id'], u['lib'], round(d, 2), 's', flush=True)
