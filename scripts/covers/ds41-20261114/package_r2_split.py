from pathlib import Path
from PIL import Image
import shutil,json,hashlib,re
P=Path('/Users/danrrose/Projects/_edit_work/DS-41-setup/r2')
R=P.parent/'review';D=R/'round2'
snapshot=json.loads((P/'split/pre-extension-hashes.json').read_text())
# Preserve every old public file and the old source key. Only the install map extends.
for filename,digest in snapshot.items():
 if filename==str(P/'neutral-install-map.json'):continue
 assert hashlib.sha256(Path(filename).read_bytes()).hexdigest()==digest,filename
mapping=json.loads((P/'split/neutral-install-map.json').read_text())
cards=[]
for label,files in mapping.items():
 for platform in ['Instagram','YouTube']:
    src=Path(files[platform]['original']);Image.open(src).convert('RGB').save(D/f'{label}-{platform}.jpg',quality=94,subsampling=0)
 Image.open(P/'split/designed'/f'{label}-Grid.jpg').convert('RGB').save(D/f'{label}-Grid.jpg',quality=94,subsampling=0)
 prior=files['Instagram']['same_lower_image_as']
 cards.append(f'<article id="{label}"><h2>{label}</h2><p style="font-size:14px;margin-top:0">Same lower image as {prior}. Two separate real podcast frames side by side.</p><div class="pair">'+''.join(f'<figure><figcaption>{pl}</figcaption><a href="round2/{label}-{pl}.jpg" target="_blank"><img src="round2/{label}-{pl}.jpg" alt="Round 2 {label} {pl} split-frame cover" width="1080" height="1920"></a></figure>' for pl in ['Instagram','YouTube'])+f'</div><details><summary>Instagram profile grid</summary><img class="gridcrop" src="round2/{label}-Grid.jpg" alt="{label} profile grid"></details></article>')
pagefile=R/'index.html';page=pagefile.read_text()
if 'id="X5"' not in page:
 (P/'split/page-before-extension.html').write_text(page)
 original_cards={label:re.search(r'<article id="'+label+r'">.*?</article>',page,re.S).group() for label in ['X1','X2','X3','X4']}
 page=page.replace('Round 2 • Four new choices • Waiting for your pick','Round 2 • Eight choices • Waiting for your pick')
 page=page.replace('Four new covers in your requested layout: the real podcast frame above, you with a huge mound of junk food below. Two images show you ripped and two show you fat.','Four lower images, two ripped and two fat, now offered with two top-panel treatments. X1 through X4 are unchanged. X5 through X8 use the same lower images in the same order.')
 page=page.replace('<strong>The top frame shows Kevin James only.</strong>','<strong>X1 through X4 show Kevin James only.</strong>')
 page=page.replace("Kevin's image uses real source pixels.</p>","Kevin's image uses real source pixels.</p><p><strong>X5 through X8 combine two separate real frames side by side: Joe Rogan and Kevin James.</strong> The clip has no shot showing both men together. These split panels are an editorial composition, with no AI redraw.</p>")
 page=page.replace('one of X1 through X4','one of X1 through X8')
 page=page.replace('<a href="round1/index.html">Previous round, not approved</a>',''.join(f'<a href="#{k}">{k}</a>' for k in mapping)+'<a href="round1/index.html">Previous round, not approved</a>')
 page=page.replace('</section>',''.join(cards)+'</section>',1)
 page=page.replace('</details><footer>','</details><details><summary>Second real source frame for split panels</summary><p>Joe Rogan at 83.9 seconds. Both source frames keep their complete native height; only side scenery is cropped in each half. <a href="round2/joe-source-frame.png" target="_blank">Open original Joe Rogan frame</a>.</p></details><footer>',1)
 for label,body in original_cards.items():assert re.search(r'<article id="'+label+r'">.*?</article>',page,re.S).group()==body
 pagefile.write_text(page)
shutil.copy2(P/'src/joe-83.9.png',D/'joe-source-frame.png')
assert not any(x in pagefile.read_text().lower() for x in ['codex','google','gemini','nano banana'])
print('Added X5-X8 and explicit separate-frame disclosure; original X1-X4 cards/files unchanged.')
