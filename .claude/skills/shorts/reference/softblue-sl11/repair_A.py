from pathlib import Path
import json,sys
from full import R,ROOT,dump,picshots,render
import finish,renderq
with renderq.slot('Vacuum A caption and glasses repairs',pool='heavy',group='SL-11'):
 d=R/'build/A';T=json.loads((d/'timeline.json').read_text());dump(d/'shots.json',picshots('A',T));render('A');finish.checks('A')
