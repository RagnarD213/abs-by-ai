from pathlib import Path
import subprocess,json,random,shutil,hashlib
from PIL import Image
R=Path(__file__).resolve().parents[3];D=R/'Short-form video content/covers/review/ds27-20261102';helper=R/'.claude/skills/_shared/blind-image/blind.py'
if not (D/'.blind-key.json').exists():
 for k in 'ABDEFGH':
  source='codex' if k in 'ABDE' else 'google'
  f=D/f'ds27/instagram/ds-27_home-workouts_cover-{k}.png'
  subprocess.run(['python3',str(helper),'add',str(D),'--source',source,'--file',str(f),'--note','letter '+k],check=True,capture_output=True)
 subprocess.run(['python3',str(helper),'build',str(D),'--kind','cover','--video','Home Workouts (DS-27)','--shot','Setup Cover'],check=True,capture_output=True)
 p=D/'.blind-key.json';key=json.loads(p.read_text());items=list(key['labels'].values());f=D/'ds27/instagram/ds-27_home-workouts_cover-C.png'
 items.append({'source':'real','original':str(f),'sha':hashlib.sha256(f.read_bytes()).hexdigest()[:12],'note':'letter C; real photograph excluded from model comparison'})
 random.SystemRandom().shuffle(items);key['labels']={f'X{i}':item for i,item in enumerate(items,1)};key['real_photo_excluded_from_model_comparison']=True;p.write_text(json.dumps(key,indent=2))
 for x,item in key['labels'].items():
  Image.open(item['original']).convert('RGB').resize((941,1672),Image.Resampling.LANCZOS).save(D/'blind'/f'{x}.jpg',quality=93)
print('Eight neutral labels prepared; source key stays private')
