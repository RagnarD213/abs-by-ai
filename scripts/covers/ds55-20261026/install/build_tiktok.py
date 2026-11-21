"""Make the cover-first TikTok copy without changing the approved master."""
from pathlib import Path
import hashlib, json, subprocess, sys
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT/'scripts/blotato'))
import tiktok_cover as tc
OUT = Path('/Volumes/Expansion/_edit_work/ds55-publish')
OUT.mkdir(parents=True, exist_ok=True)
master = ROOT/'Short-form video content/Five Minute Exercises - DS-55/Five Minute Exercises SFC R5 - complete Short.mp4'
cover = ROOT/'Short-form video content/covers/approved-ds55/five-minute-exercises-instagram.png'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(master) == '36746f1212068e47740a8003b766973ad413f115ff6d99570d41c0d387b22e2a'
assert sha(cover) == '6687dd204410c444119bb77da699af0b29eab2b51266b54232e96dd5362b4c83'
dest = OUT/'five-minute-exercises-tiktok-cover-first.mp4'
result = tc.build(str(master), str(cover), str(dest))
def audio_hash(p):
    r = subprocess.run([tc.FFMPEG,'-v','error','-i',str(p),'-map','0:a:0','-c','copy','-f','adts','-'],capture_output=True,check=True)
    return hashlib.sha256(r.stdout).hexdigest()
result.update(path=str(dest),sha256=sha(dest),master_sha256=sha(master),audio_identical=audio_hash(master)==audio_hash(dest))
assert result['ok'] and result['audio_identical']
tc.run([tc.FFMPEG,'-v','error','-y','-i',str(dest),'-frames:v','1',str(OUT/'tiktok-frame-zero.png')])
(OUT/'tiktok-verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
