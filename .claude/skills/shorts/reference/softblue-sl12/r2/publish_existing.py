"""Refresh a separate R2 subpath on our existing managed R1 server without restarting it.

New launchd workers hit host EMFILE. Reuse the healthy owned service and shared cache
snapshot implementation; preserve all R1 page/media and the existing login service.
"""
from pathlib import Path
import sys,json,urllib.request,importlib.util
ROOT=Path('/Users/danielrose/Projects/Claude/Projects/Abs By AI');R=Path('/Volumes/Extreme/_edit_work/SL-12/round2')
sp=importlib.util.spec_from_file_location('shared_review',ROOT/'.claude/skills/_shared/review_server.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
health=m.health(9954);assert health and Path(health['root'])==R.parent/'round1/asset-review',health
frames='--frames' in sys.argv;source=R/('A-frames-review' if frames else 'review');slug='round2-frames' if frames else 'round2';dest=Path(health['served_root'])/slug
if not frames:
    # The original review URL remains Dan's entry point. Publish the latest
    # packet in the source tree as well, so a normal cache refresh preserves it.
    parent=Path(health['root'])
    m.snapshot(source,parent/slug)
    legacy=parent/'index-r1.html'
    if not legacy.exists():
        legacy.write_bytes((parent/'index.html').read_bytes())
    (parent/'index.html').write_text('''<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Keep Your Muscle Review</title></head><body>
<p><a href="round2/">Open the current Keep Your Muscle review</a></p>
<script>location.replace('round2/'+location.search+location.hash);</script>
</body></html>''')
    m.snapshot(parent,Path(health['served_root']))
records=m.snapshot(source,dest)
(dest/'published-source.json').write_text(json.dumps(dict(owner='SL-12',round=2,source=str(source),service_port=9954,parent_source=health['root'],files=records,reason='New launchd service activation failed EMFILE; reuse owned healthy managed service without restart.'),indent=2)+'\n')
url=f'http://127.0.0.1:9954/{slug}/'
with urllib.request.urlopen(url,timeout=5) as r:assert r.status==200
print('Managed review ready:',url,'on existing owned service;',len(records),'linked files cached locally.')
