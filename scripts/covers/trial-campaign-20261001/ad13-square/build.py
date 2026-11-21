"""Recompose approved 13-R3B assets into the campaign's square layout."""
from pathlib import Path
import ast, copy, json, hashlib, shutil
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path('/Users/danielrose/Documents/Claude/Projects/Abs By AI')
P = ROOT/'social media graphics/youtube/thumbnails/_trial-campaign-20261001'
OUT = ROOT/'social media graphics/youtube/thumbnails/Ad 13 What Getting Abs Cost/trial-20261001'
OUT.mkdir(parents=True, exist_ok=True)
source = ROOT/'scripts/covers/trial-campaign-20261001/build.py'
tree = ast.parse(source.read_text())
tree.body = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.Assign)) and not (isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id in ['ROOT', 'records'] for t in n.targets))]
ns = {'ROOT': ROOT, '__file__': str(source)}
exec(compile(tree, str(source), 'exec'), ns)
ad = copy.deepcopy(next(a for a in ns['ADS'] if a['id'] == 'ad13'))
ad['photos'][1] = 'photo-10'
ad['waist'][1] = .713
ad['lines'][1] = ['HUMAN TRAINERS', 'HATE THIS AI']
size = (1080, 1080)
plate_path = P/'round3/sources/ad13-gray-repaired-plate.png'
plate = Image.open(plate_path).convert('RGBA')
# Recompose the robot below the type band without cropping Dan or any wording.
im = ns['gradient'](size, (9,11,14), (24,27,31))
scene = plate.resize((1209,680), Image.Resampling.LANCZOS)
alpha = np.asarray(scene.getchannel('A')).copy()
fade = np.clip(np.arange(scene.height)/90, 0, 1)
alpha = (alpha*fade[:,None]).astype('uint8')
scene.putalpha(Image.fromarray(alpha))
im.alpha_composite(scene, (-25,400))
layer, person, info = ns['place_person'](ad, 'B', size)
im.alpha_composite(layer)
tm, ti = ns['type_block'](ad, 'B', im, person)
assert ti['text_person_overlap'] == 0
dest = OUT/'Ad 13 | 1x1 | FINAL.jpg'
im.convert('RGB').save(dest, quality=94, subsampling=0)
assert dest.stat().st_size < 2000000
shutil.copy2(dest, P/'FINAL APPROVED'/dest.name)
manifest = dict(option='13-R3B', aspect='1x1', generated_images=0, paid_image_api_calls=0,
    method='Existing approved robot plate and original photo-10 cutout; shared campaign typography',
    size=list(size), bytes=dest.stat().st_size, sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),
    inputs=[dict(path=str(x), sha256=hashlib.sha256(x.read_bytes()).hexdigest()) for x in [plate_path, ns['PH']/'photo-10_FINAL_PRIMARY.jpg', P/'masks/photo-10_FINAL_PRIMARY.mask.png']], **info, **ti)
(OUT/'ad13-square-build.json').write_text(json.dumps(manifest, indent=2)+'\n')
im.convert('RGB').resize((320,320), Image.Resampling.LANCZOS).save(OUT/'ad13-square-phone.jpg', quality=94)
print(json.dumps(manifest,indent=2))
