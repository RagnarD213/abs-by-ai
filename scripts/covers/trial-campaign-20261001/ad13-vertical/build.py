"""Recompose approved 13-R3B assets into the campaign's vertical layout."""
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
ad['lines'][1] = ['HUMAN', 'TRAINERS', 'HATE THIS AI']
size = (1080, 1920)
plate_path = P/'round3/sources/ad13-gray-repaired-plate.png'
plate = Image.open(plate_path).convert('RGBA')
# Same approved plate below the headline. Use its existing upper texture above it.
im = ns['gradient'](size, (9,11,14), (24,27,31))
scene = plate.resize((1792,1008), Image.Resampling.LANCZOS)
im.alpha_composite(scene, (-120,650))
# Carry the original texture to the bottom using its empty right-hand area.
floor = plate.crop((1000,580,1280,720)).resize((1080,262), Image.Resampling.LANCZOS)
im.alpha_composite(floor, (0,1658))
layer, person, info = ns['place_person'](ad, 'B', size)
im.alpha_composite(layer)
tm, ti = ns['type_block'](ad, 'B', im, person)
assert ti['text_person_overlap'] == 0
dest = OUT/'Ad 13 | 9x16 | FINAL.jpg'
im.convert('RGB').save(dest, quality=94, subsampling=0)
assert dest.stat().st_size < 2000000
shutil.copy2(dest, P/'FINAL APPROVED'/dest.name)
manifest = dict(option='13-R3B', aspect='9x16', generated_images=0, paid_image_api_calls=0,
    method='Existing approved robot plate and original photo-10 cutout; shared campaign typography',
    size=list(size), bytes=dest.stat().st_size, sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),
    inputs=[dict(path=str(x), sha256=hashlib.sha256(x.read_bytes()).hexdigest()) for x in [plate_path, ns['PH']/'photo-10_FINAL_PRIMARY.jpg', P/'masks/photo-10_FINAL_PRIMARY.mask.png']], **info, **ti)
(OUT/'ad13-vertical-build.json').write_text(json.dumps(manifest, indent=2)+'\n')
sheet = Image.new('RGB', (1080,640), '#172128')
d = ImageDraw.Draw(sheet)
for i,name in enumerate(['Ad 13', 'Ad 3', 'Ad 10', 'RA-01']):
    f = P/'FINAL APPROVED'/f'{name} | 9x16 | FINAL.jpg'
    sheet.paste(Image.open(f).resize((270,480), Image.Resampling.LANCZOS),(i*270,40))
    d.text((i*270+12,12),name,fill='white')
sheet.paste(Image.open(P/'FINAL APPROVED/Ad 13 | 16x9 | FINAL.jpg').resize((213,120)),(12,520))
sheet.save(OUT/'ad13-vertical-comparison.jpg',quality=94)
print(json.dumps(manifest,indent=2))
