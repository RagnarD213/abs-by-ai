"""Recompose the approved Ad 10 plate and real cutout for a square thumbnail."""
from pathlib import Path
import ast
import copy
import json
import shutil
import sys

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

ad = copy.deepcopy(next(a for a in ns['ADS'] if a['id'] == 'ad10'))
ad['photos'][1] = 'studio-white-25'
ad['waist'][1] = .78
out = ROOT / 'social media graphics/youtube/thumbnails/Ad 10 My Dad Bod/trial-20261001'
out.mkdir(parents=True, exist_ok=True)
size = (1080, 1080)
image = ns['backdrop'](ad, 'B', size)
layer, person, info = ns['place_person'](ad, 'B', size)
image.alpha_composite(layer)
_, text_info = ns['type_block'](ad, 'B', image, person)
info.update(text_info)
assert info['text_person_overlap'] == 0
assert info['headline'] == 'HOW BUSY DADS GET ABS'
path = out / 'Ad 10 | 1x1 | FINAL.jpg'
image.convert('RGB').save(path, quality=94, subsampling=0)
assert path.stat().st_size < 2000000
shutil.copy2(path, P / 'FINAL APPROVED' / path.name)
record = dict(shape='1x1', output=str(path), sha256=ns['sha'](path),
              cutout_sha256=ns['sha'](ROOT / 'photos/finalized social media photos/_cutouts/studio-white-25_CUTOUT.png'),
              plate_sha256=ns['sha'](P / 'generated/ad10-B.png'), **info)
(out / 'formats-build-20261005.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
