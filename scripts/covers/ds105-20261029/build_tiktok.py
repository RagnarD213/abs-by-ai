"""Make the cover-first TikTok copy without changing the approved master."""
from pathlib import Path
import hashlib, json, subprocess, sys
ROOT = Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI')
sys.path.insert(0, str(ROOT/'scripts/blotato'))
import tiktok_cover as tc
OUT = Path('/Volumes/Extreme/_edit_work/ds105-publish')
OUT.mkdir(parents=True, exist_ok=True)
master = ROOT/'Short-form video content/DS-105 mouthpiece/Why I Wear A Mouthpiece For SFC R4 - final.mp4'
cover = ROOT/'Short-form video content/covers/approved-ds105/mouthpiece-instagram-approved.png'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(master) == '061deb744eb1e83cf1917727095214c8e4ea68ffebf56d9f85042d80694eebe2'
assert sha(cover) == '03ffed4da329bea1d268298394a420c9b9060b467cc871b36cf7bb2405f074dc'
dest = OUT/'mouthpiece-tiktok-cover-first.mp4'
result = tc.build(str(master), str(cover), str(dest))
def audio_hash(p):
    r = subprocess.run([tc.FFMPEG,'-v','error','-i',str(p),'-map','0:a:0','-c','copy','-f','adts','-'],capture_output=True,check=True)
    return hashlib.sha256(r.stdout).hexdigest()
result.update(path=str(dest),sha256=sha(dest),master_sha256=sha(master),audio_identical=audio_hash(master)==audio_hash(dest))
assert result['ok'] and result['audio_identical']
tc.run([tc.FFMPEG,'-v','error','-y','-i',str(dest),'-frames:v','1',str(OUT/'tiktok-frame-zero.png')])
(OUT/'tiktok-verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
