"""Soft Blue Light abdominal-layer teaching graphic. Proposed in RO-23 R1; Dan approval pending.

Config: id, dur, title, states [{at, active:[0..3], caption}], reveal:[seconds]*4.
A state may supply note for a separate 28px footer while that state is active.
Absent notes leave the historical layout unchanged.
Four separate torso diagrams distinguish the superficial, outer, inner and deep layers.
No quantitative activation or strength is implied by the animated highlight.
"""
import json, pathlib, sys
HERE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
import hfbuild as H
def scene(c,out):
    assert len(c['reveal'])==4
    assert all(0<=x<c['dur'] for x in c['reveal'])
    assert all(H.text_w(s['caption'],42)<1710 for s in c['states'])
    return H.make_scene(HERE/'ab-muscles.template.htm',c,out)
if __name__=='__main__':
    cfg=json.load(open(sys.argv[1]));out=pathlib.Path(sys.argv[2])
    for c in cfg if isinstance(cfg,list) else [cfg]:
        d=scene(c,out);H.lint_check(d)
        if '--snap' in sys.argv:H.snapshot(d,[float(sys.argv[sys.argv.index('--snap')+1])])
        if '--render' in sys.argv:H.render(d,out/(c['id']+'.mov'))
