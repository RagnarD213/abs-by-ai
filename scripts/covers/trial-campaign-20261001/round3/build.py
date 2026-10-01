"""Two review-only revisions. Never writes into earlier rounds."""
from pathlib import Path
import ast, copy, json, hashlib, shutil
import numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFilter

ROOT = next(p for p in Path(__file__).resolve().parents if (p/'AGENTS.md').exists())
P = ROOT/'social media graphics/youtube/thumbnails/_trial-campaign-20261001'
R = P/'round3'
PH = ROOT/'photos/finalized social media photos'
source = ROOT/'scripts/covers/trial-campaign-20261001/build.py'
tree = ast.parse(source.read_text())
tree.body = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.Assign)) and not (isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id in ['ROOT','records'] for t in n.targets))]
ns = {'ROOT': ROOT, '__file__': str(source)}
exec(compile(tree, str(source), 'exec'), ns)
ADS = {a['id']: a for a in ns['ADS']}
sha = ns['sha']
for folder in ['options','phone','qa','references','sources']:
    (R/folder).mkdir(exist_ok=True)

old = json.loads((P/'round2/manifest.json').read_text())
locked = []
for row in old['outputs']:
    if row['choice'] in ['RA-R2A','10-R2A','4-R2A','3-R2A']:
        src = P/'round2'/row['path']
        assert sha(src) == row['sha256'], f'Approved image changed: {src}'
        dest = R/'references'/src.name
        shutil.copy2(src, dest)
        assert sha(dest) == row['sha256']
        locked.append(dict(choice=row['choice'], aspect=row['aspect'], source=str(src.relative_to(ROOT)), path=str(dest.relative_to(R)), sha256=sha(dest), approval='Dan approved in round 2'))
for name in ['13-R2B','13-R2A','6-R2A']:
    src = P/'round2/options'/f'{name}-16x9.jpg'
    shutil.copy2(src, R/'references'/src.name)

# Existing clean upper gray texture, feathered completely before the robot's head.
robot = ImageOps.fit(Image.open(P/'round2/generated/ad13-robot.png').convert('RGBA'), (1280,720))
shifted = Image.new('RGBA', (1280,720), (2,3,4,255))
shifted.alpha_composite(robot, (0,75))
gray = ImageOps.fit(Image.open(P/'generated/ad13-B.png').convert('RGBA'), (1280,720))
alpha = np.ones((720,1280), dtype=np.float32)
t = np.clip((np.arange(720)-100)/145, 0, 1)
alpha[:] = (1-t*t*(3-2*t))[:,None]
repair_mask = Image.fromarray((alpha*255).astype('uint8'))
plate = Image.composite(gray, shifted, repair_mask)
plate.save(R/'sources/ad13-gray-repaired-plate.png')
assert np.array_equal(np.array(plate)[245:], np.array(shifted)[245:])

records = []
def render(choice, adid, photo, waist, background, person_override=None):
    a = copy.deepcopy(ADS[adid]); a['photos'][1] = photo; a['waist'][1] = waist
    if person_override is not None: ns['CACHE'][photo] = person_override
    else: ns['CACHE'].pop(photo, None)
    im = background.copy()
    layer, person, info = ns['place_person'](a, 'B', im.size)
    im.alpha_composite(layer)
    tm, ti = ns['type_block'](a, 'B', im, person)
    assert ti['text_person_overlap'] == 0
    info.update(ti)
    dest = R/'options'/f'{choice}-16x9.jpg'
    im.convert('RGB').save(dest, quality=94, subsampling=0)
    im.convert('RGB').save(R/'qa'/f'{choice}-lossless.png')
    im.convert('RGB').resize((320,180), Image.Resampling.LANCZOS).save(R/'phone'/dest.name, quality=94)
    tm.save(R/'qa'/f'{choice}-text.png'); person.save(R/'qa'/f'{choice}-person.png')
    assert dest.stat().st_size < 2000000
    records.append(dict(info, choice=choice, path=str(dest.relative_to(R)), sha256=sha(dest), bytes=dest.stat().st_size, size=list(im.size), status='awaiting_Dan'))

render('13-R3B', 'ad13', 'photo-10', .713, plate)

age_path = R/'generated/ad6-age.png'
if age_path.exists():
    original = ns['cutout']('studio-blue-171')
    aged = Image.open(age_path).convert('RGBA').resize(original.size, Image.Resampling.LANCZOS)
    w,h = original.size
    mask = Image.new('L', original.size)
    d = ImageDraw.Draw(mask)
    # This photo's head and neck only. Shoulders and necklace stay original.
    polygon = [(.375,.058),(.646,.058),(.665,.203),(.628,.254),(.613,.284),(.573,.314),(.49,.313),(.445,.285),(.443,.258),(.408,.223),(.378,.17)]
    d.polygon([(int(x*w),int(y*h)) for x,y in polygon], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(10))
    arr = np.array(mask); arr[int(h*.326):] = 0; mask = Image.fromarray(arr)
    person = Image.composite(aged, original, mask)
    person.putalpha(original.getchannel('A'))
    assert np.array_equal(np.array(person)[int(h*.326):], np.array(original)[int(h*.326):])
    person.save(R/'sources/studio-blue-171-aged-head-original-body.png')
    mask.save(R/'sources/studio-blue-171-age-mask.png')
    render('6-R3B', 'ad6', 'studio-blue-171', .78, ns['backdrop'](ADS['ad6'],'B',(1280,720)), person)
    # Close detail for human QA, not additional concept variants.
    detail = Image.new('RGB',(1000,660),'#172128')
    for i,im in enumerate([original,person]):
        detail.paste(im.convert('RGB').crop((1200,270,2240,1650)).resize((500,660)),(i*500,0))
    detail.save(R/'qa/ad6-head-comparison.jpg',quality=95)

inputs = [PH/'studio-blue-171_FINAL_PRIMARY.jpg', PH/'_cutouts/studio-blue-171_CUTOUT.png', PH/'photo-10_FINAL_PRIMARY.jpg', P/'masks/photo-10_FINAL_PRIMARY.mask.png', P/'generated/ad13-B.png',P/'round2/generated/ad13-robot.png', P/'generated/ad6-B.png']
manifest = dict(campaign='24316364155', status='review_only_awaiting_two_decisions', generation_count=1, paid_image_api_calls=0, generation_method='codex-image.sh, ChatGPT subscription', prompt=(R/'prompts/ad6-age.txt').read_text(), inputs=[dict(path=str(p.relative_to(ROOT)),sha256=sha(p)) for p in inputs], outputs=records, locked_approvals=locked, ad13_repair=dict(method='Existing gray plate upper texture; smooth feather y100-245; unchanged robot below y245', robot_translate_y=75), age_edit=dict(source='studio-blue-171', edited_region='hair, face, neck only', original_pixels_unchanged_below_y_fraction=.326), remaining_decisions=['Confirm 13-R3B','Choose original 6-R2A or AI age edit 6-R3B'], final_exports=False, installed=False)
if age_path.exists(): manifest['generation_output'] = dict(path=str(age_path.relative_to(ROOT)),sha256=sha(age_path))
(R/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'review_images':len(records),'locked_layouts_verified':len(locked),'outputs':[(r['choice'],r['bytes']) for r in records]}))
