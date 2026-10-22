#!/usr/bin/env python3
"""Export Dan's picks to Short-form video content/covers/approved-sl06/: Instagram PNG as built, YouTube JPEG q88 (under 2 MB),
plus picks.json with full hashes. Usage: python3 export.py s2=C s5=D [...]; picks already exported stay."""
import sys,json,hashlib,io
from pathlib import Path
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parent))
from root import P,R
from build import COPY
OUT=P/'Short-form video content/covers/approved-sl06';OUT.mkdir(parents=True,exist_ok=True)
pj=OUT/'picks.json';picks=json.loads(pj.read_text()) if pj.exists() else {'picked_by':'Dan','covers':{}}
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
for arg in sys.argv[1:]:
 k,v=arg.split('=');slug=COPY[k][1]
 ig_src=R/'instagram'/f'{slug}_cover-{v}.png';yt_src=R/'youtube'/f'{slug}_cover-{v}.png'
 ig=OUT/f'Instagram_{slug}_cover-{v}.png';yt=OUT/f'YouTube_{slug}_cover-{v}.jpg'
 for old in OUT.glob(f'*_{slug}_cover-*'):old.unlink()
 Image.open(ig_src).convert('RGB').save(ig);Image.open(yt_src).convert('RGB').save(yt,'JPEG',quality=88)
 assert yt.stat().st_size<2_000_000 and Image.open(yt).size==(1080,1920)==Image.open(ig).size
 picks['covers'][slug]=dict(short=k,pick=v,instagram=str(ig),instagram_sha256=sha(ig),youtube=str(yt),youtube_sha256=sha(yt),youtube_bytes=yt.stat().st_size)
 print(k,v,sha(ig)[:8],sha(yt)[:8],yt.stat().st_size)
pj.write_text(json.dumps(picks,indent=1)+'\n')
