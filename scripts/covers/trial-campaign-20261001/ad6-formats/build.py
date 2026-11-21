"""Adapt approved 6-R3B to vertical and square using its exact cutout and plate."""
from pathlib import Path
import ast, copy, json, shutil, sys
from PIL import Image

ROOT = Path(sys.argv[1]).resolve()
P = ROOT / 'social media graphics/youtube/thumbnails/_trial-campaign-20261001'
source = ROOT / 'scripts/covers/trial-campaign-20261001/build.py'
tree = ast.parse(source.read_text())
tree.body = [n for n in tree.body
             if isinstance(n, (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.Assign))
             and not (isinstance(n, ast.Assign) and any(
                 isinstance(t, ast.Name) and t.id in ['ROOT', 'records'] for t in n.targets))]
ns = {'ROOT': ROOT, '__file__': str(source)}
exec(compile(tree, str(source), 'exec'), ns)
ad = copy.deepcopy(next(a for a in ns['ADS'] if a['id'] == 'ad6'))
ad['photos'][1] = 'studio-blue-171'
ad['waist'][1] = .78
cutout = P / 'round3/sources/studio-blue-171-aged-head-original-body.png'
ns['CACHE']['studio-blue-171'] = Image.open(cutout).convert('RGBA')
out = ROOT / "social media graphics/youtube/thumbnails/Ad 6 You're Not Too Old To Get Abs/trial-20261001"
out.mkdir(parents=True, exist_ok=True)
records = []
for shape, size in [('9x16', (1080, 1920)), ('1x1', (1080, 1080))]:
    image = ns['backdrop'](ad, 'B', size)
    layer, person, info = ns['place_person'](ad, 'B', size)
    image.alpha_composite(layer)
    text, text_info = ns['type_block'](ad, 'B', image, person)
    info.update(text_info)
    assert info['text_person_overlap'] == 0
    path = out / f'Ad 6 | {shape} | FINAL.jpg'
    image.convert('RGB').save(path, quality=94, subsampling=0)
    assert path.stat().st_size < 2000000
    shutil.copy2(path, P / 'FINAL APPROVED' / path.name)
    records.append(dict(shape=shape, output=str(path), sha256=ns['sha'](path),
                        cutout_sha256=ns['sha'](cutout),
                        plate_sha256=ns['sha'](P / 'generated/ad6-B.png'), **info))
(out / 'formats-build-20261004.json').write_text(json.dumps(records, indent=2) + '\n')
print(json.dumps(records, indent=2))
