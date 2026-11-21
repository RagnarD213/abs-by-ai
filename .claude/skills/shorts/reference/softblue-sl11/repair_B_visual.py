from full import R,ROOT,FPS,picshots,render,dump,sha
import json,finish,renderq
EXPECTED='f83dff214840e22784a404f49cb6e1afff5f0474984540cb39b78c24e3251f81'
with renderq.slot('Vacuum B picture-only hand-framing repair',pool='heavy',group='SL-11'):
 d=R/'build/B';assert sha(d/'his_mix.wav')==EXPECTED
 T=json.loads((d/'timeline.json').read_text());dump(d/'shots.json',picshots('B',T))
 render('B');assert sha(d/'his_mix.wav')==EXPECTED
 finish.checks('B')
