"""Review the chosen A2 design with its corrected photograph; retain B revision."""
from pathlib import Path
import shutil,json
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[4]
R=Path('/Volumes/Extreme/_edit_work/SL-12/setup/round3')
PAGE=Path('/Volumes/Extreme/_edit_work/SL-12/round1/asset-review/setup')
for label in ['A2','BX2']:
    for platform in ['instagram','youtube']:
        shutil.copyfile(R/'covers'/label/(platform+'.jpg'),PAGE/(label+'-r3-'+platform+'.jpg'))
    shutil.copyfile(R/'covers'/label/'profile.jpg',PAGE/(label+'-r3-profile.jpg'))
s='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Keep Your Muscle: A2 Photo Revision</title><style>
*{box-sizing:border-box}body{margin:0;background:#0b121a;color:#edf4fc;font:16px/1.45 system-ui}main{max-width:1150px;margin:auto;padding:18px}h1{font-size:27px;line-height:1.12;margin:6px 0 12px}h2{font-size:24px;line-height:1.18}p{max-width:800px}a{color:#8bd9ff}.hold{border-left:4px solid #f5cd4d;background:#1a2635;padding:10px 14px}.nav{position:sticky;top:0;z-index:2;background:#0b121af2;padding:12px 0;display:flex;gap:22px}article{padding:14px;background:#17212e;border:1px solid #304257;border-radius:14px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:12px;align-items:start}.pair img{width:100%;height:auto;border-radius:5px}.caption{color:#b8cbdc;font-size:13px;margin:7px 0}small{font-size:12px}section{scroll-margin-top:65px;margin-top:22px}.note{font-size:14px;color:#bdd0df}@media(min-width:900px){main{padding:28px}}
</style></head><body><main><h1>Keep Your Muscle<br>A2 Photograph Revision</h1><p>You chose A2. The updated photograph keeps the selected cyan design. Check the even press and relaxed, camera-facing expression.</p><p class="hold">Publishing stays held until the parent is confirmed public on or after December 6.</p><nav class="nav"><a href="#A">A2: Updated Photo</a><a href="#B">B: Instagram Check</a></nav>
<section id="A"><h2>A2: Your Chosen Design, Revised Photograph</h2><p class="note">The source clip had no frame combining an even rep with a relaxed expression. This photograph uses your authorized AI-assisted correction of the real lifting screenshot.</p><article><div class="pair"><div><p class="caption">Instagram profile tile</p><a href="A2-r3-instagram.jpg"><img src="A2-r3-profile.jpg" alt="A2 revised Instagram profile with balanced dumbbells and relaxed expression"><small>Open full Instagram cover</small></a></div><div><p class="caption">YouTube cover</p><a href="A2-r3-youtube.jpg"><img src="A2-r3-youtube.jpg" alt="A2 revised YouTube cover"></a></div></div></article></section>
<section id="B"><h2>B X2: Revised Instagram Still Needs Your Check</h2><p>The foods remain visible in Instagram. Your approved YouTube cover is unchanged.</p><article><div class="pair"><div><p class="caption">Revised Instagram profile tile</p><a href="BX2-r3-instagram.jpg"><img src="BX2-r3-profile.jpg" alt="B X2 food-visible Instagram profile"><small>Open full Instagram cover</small></a></div><div><p class="caption">Approved YouTube cover, unchanged</p><a href="BX2-r3-youtube.jpg"><img src="BX2-r3-youtube.jpg" alt="B X2 approved unchanged YouTube cover"></a></div></div></article></section><p>Approve the updated A2 photograph and the revised B Instagram, or give changes. Your selected design and approved video edits remain locked. No revised cover has been installed or scheduled.</p></main></body></html>'''
if not (R/'previous-review.html').exists():shutil.copyfile(PAGE/'index.html',R/'previous-review.html')
(PAGE/'index.html').write_text(s)
print('A2 photograph revision review built; no installation or scheduling.')
