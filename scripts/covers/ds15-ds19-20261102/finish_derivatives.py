"""Build and check both cover-first copies inside one render-queue admission."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'scripts/blotato'))
import tiktok_cover

WORK = Path('/Volumes/Extreme/_edit_work/ds15-ds19-publish')
for job, info in json.loads((WORK / 'files.json').read_text()).items():
    output = WORK / f'{job}-tiktok-cover-first.mp4'
    if output.exists():
        result = tiktok_cover.verify(info['master'], str(output), 1, info['instagram_cover'])
    else:
        result = tiktok_cover.build(info['master'], info['instagram_cover'], str(output))
    assert result['ok'], result
    (WORK / f'{job}-tiktok-verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(job, result, flush=True)
