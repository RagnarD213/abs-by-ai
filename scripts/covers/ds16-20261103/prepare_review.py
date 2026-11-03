#!/usr/bin/env python3
"""Register reviewed covers once, keep source provenance outside the review page."""
from pathlib import Path
import json, subprocess, hashlib, shutil
R=Path(__file__).resolve().parents[3]
O=R/'Short-form video content/covers/review/ds16-last-ten-pounds-20261103'
B=R/'.claude/skills/_shared/blind-image/blind.py'
if (O/'.blind-key.json').exists():
    raise SystemExit('Blind labels already exist; preserve them and rerun review.py only.')
for k in 'ABDEFGH':
    p=O/f'ds16/youtube/ds-16_last-ten-pounds_cover-{k}.png'
    subprocess.run(['python3',str(B),'add',str(O),'--source','codex' if k in 'ABDE' else 'google','--file',str(p),'--note',f'letter {k}'],check=True,capture_output=True)
# The photograph is a separate source category, never counted as generated Dan.
p=O/'ds16/youtube/ds-16_last-ten-pounds_cover-C.png'
h=hashlib.sha256(p.read_bytes()).hexdigest()[:12]
dest=O/'originals'/f'photograph-{h}.png';shutil.copy2(p,dest)
rp=O/'.blind-registry.json';reg=json.loads(rp.read_text());reg.append({'source':'real-photo','file':str(dest),'sha':h,'note':'letter C; original person pixels; excluded from AI model comparison'})
rp.write_text(json.dumps(reg,indent=2))
subprocess.run(['python3',str(B),'build',str(O),'--kind','cover','--video','How To Lose The Last Ten Pounds Of Fat (DS-16)','--shot','Initial Cover Choices'],check=True)
subprocess.run(['python3',str(Path(__file__).with_name('review.py'))],check=True)
