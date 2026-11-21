from pathlib import Path
from PIL import Image
import json,shutil,re
P=Path('/Users/danrrose/Projects/_edit_work/DS-41-setup')
Q=P/'r2/x3-revision';R=P/'review';O=R/'x3-revised';O.mkdir(exist_ok=True)
archive=R/'round2/index.html'
if not archive.exists():
 old=(R/'index.html').read_text()
 old=old.replace('href="round2/','href="').replace('src="round2/','src="').replace('href="round1/index.html"','href="../round1/index.html"')
 old=old.replace('<main>','<main><p style="padding:16px;background:#593025">Earlier choices. Dan selected X3 with a text revision. <a href="../">Review the revised X3 for final approval</a>.</p>',1)
 archive.write_text(old)
for pl in ['Instagram','YouTube']:
 Image.open(Q/'designed'/f'X3-Revised-{pl}.png').convert('RGB').save(O/f'X3-Revised-{pl}.jpg',quality=94,subsampling=0)
shutil.copy2(Q/'designed/X3-Revised-Grid.jpg',O/'X3-Revised-Grid.jpg')
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Kevin James Cheat SFC Setup | Revised X3 Approval</title><style>
*{box-sizing:border-box}body{margin:0;background:#101823;color:#f5f2e9;font:17px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}main{max-width:1140px;margin:auto;padding:24px 16px}h1{font-size:clamp(26px,4vw,38px);line-height:1.2;margin:12px 0}p{max-width:850px}a{color:#9ed9ff}.status{font-weight:700;color:#ffdc79}.covers{display:grid;grid-template-columns:1fr 1fr;gap:14px;padding:14px;background:#1b2636;border:1px solid #384a60;border-radius:12px;margin:24px 0}figure{margin:0;min-width:0}figcaption{font-size:15px;margin-bottom:9px}img{display:block;width:100%;height:auto;border-radius:4px}.profile{grid-column:1/-1}.profile img{max-width:300px}footer{margin:28px 0;font-size:14px;color:#b8c4d1}nav{display:flex;flex-wrap:wrap;gap:18px}@media(min-width:850px){.covers{grid-template-columns:1fr 1fr 1fr}.profile{grid-column:auto}}@media(max-width:430px){main{padding:16px 10px}.covers{padding:10px;gap:9px}}
</style><main><div class="status">X3 selected • Text revised • Final approval needed</div><h1>Why Cheat Days Make You Fat</h1><p>This is your selected Round 2 X3 with the revised headline. The Kevin James frame, his name label, your image, the food and both layouts are unchanged.</p><p><strong>Please approve these two revised cover files</strong>, Instagram and YouTube, including the headline above. The profile-grid preview shows how Instagram crops it. Reply <strong>“Approved”</strong> if both are ready.</p><p>The film is unchanged. These revised files are awaiting your final OK; nothing is installed, uploaded to publishing platforms, queued or scheduled.</p><section class="covers">'''+''.join(f'<figure><figcaption>{pl}</figcaption><a href="x3-revised/X3-Revised-{pl}.jpg" target="_blank"><img src="x3-revised/X3-Revised-{pl}.jpg" alt="Revised X3 {pl}: Why Cheat Days Make You Fat" width="1080" height="1920"></a></figure>' for pl in ['Instagram','YouTube'])+'''<figure class="profile"><figcaption>Instagram profile grid</figcaption><a href="x3-revised/X3-Revised-Grid.jpg" target="_blank"><img src="x3-revised/X3-Revised-Grid.jpg" alt="Revised X3 Instagram grid preview" width="1080" height="1440"></a></figure></section><nav><a href="round2/index.html">Earlier Round 2 choices</a><a href="round1/index.html">Earlier Round 1 choices</a></nav><footer>Kevin James Tried One Cheat Day A Week. It Wrecked His Diet.<br>X3 headline revision • November 15, 2026. No video or audio player on this page.</footer></main></html>'''
assert not any(s in page for s in ['\u2014','\u2013'])
(R/'index.html').write_text(page)
print('Prepared only revised X3 pair and grid on main page; earlier rounds archived/reachable.')
