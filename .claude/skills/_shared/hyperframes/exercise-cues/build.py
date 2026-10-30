"""Shared red exercise warnings and an accurate accelerated analog second hand.
Proposed RO-23 R2; targets must be measured from the actual cropped moving source.
No automatic anatomical tracking or approval is claimed by this renderer.
"""
import json,pathlib,sys
HERE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent))
import hfbuild as H
if __name__=='__main__':
    cfg=json.load(open(sys.argv[1]));out=pathlib.Path(sys.argv[2])
    for c in cfg if isinstance(cfg,list) else [cfg]:
        assert c['type'] in ('x','arrow','clock')
        if c['type']=='arrow':assert len(c['targets'])>=2
        d=H.make_scene(HERE/'exercise-cues.template.htm',c,out)
        H.lint_check(d)
        if '--render' in sys.argv:H.render(d,out/(c['id']+'.mov'))
