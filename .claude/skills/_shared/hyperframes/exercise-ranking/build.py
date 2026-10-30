"""Populated exercise ranking, proposed in RO-23 R2. Uses shared HyperFrames.

Config: id, dur, mode (images/text/corner), rows [{label,items:[{id,name}]}].
Media is composited into the returned pixel boxes by the normal RGB compositor.
The complete ranking has 11 entries. Corner mode shows the current spoken tier.
No existing tier-list template or approved render is changed.
"""
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import hfbuild as H


def prepare(config):
    c = dict(config)
    media = []
    if c['mode'] == 'corner':
        assert len(c['rows']) == 1
        rows = [dict(c['rows'][0], y=200, h=540)]
        for i, item in enumerate(rows[0]['items']):
            item = dict(item, x=80, y=305+i*200, w=660, h=174,
                        tx=310, ty=325+i*200, tw=410, px=46)
            media.append(dict(id=item['id'], box=[90, 320+i*200, 200, 130]))
            rows[0]['items'][i] = item
    else:
        assert [x['label'] for x in c['rows']] == ['Best', 'Good', 'Okay', 'Terrible']
        assert [len(x['items']) for x in c['rows']] == [1, 6, 2, 2]
        rows = []
        for row, (y,h) in zip(c['rows'], [(154,140),(310,410),(736,130),(882,130)]):
            out = dict(row,y=y,h=h,items=[])
            for i, raw in enumerate(row['items']):
                if row['label']=='Best':
                    item = dict(raw,x=266,y=y+8,w=1534,h=122,tx=865,ty=y+26,tw=910,px=52)
                    for j, key in enumerate(['workout-toe','workout-twist','workout-plank']):
                        media.append(dict(id=key,box=[280+j*184,y+20,176,100]))
                else:
                    cols=2; w=754
                    xx=266+(i%cols)*(w+18); yy=y+8+(i//cols)*132
                    item=dict(raw,x=xx,y=yy,w=w,h=114,tx=xx+230,ty=yy+18,tw=w-248,px=46)
                    media.append(dict(id=item['id'],box=[xx+10,yy+4,210,106]))
                if c['mode']=='text':
                    item.update(tx=item['x']+24,ty=item['y']+8,tw=item['w']-48,px=64)
                out['items'].append(item)
            rows.append(out)
    c['rows']=rows
    c['media']=[] if c['mode']=='text' else media
    return c


def scene(config,out):
    c=prepare(config)
    return H.make_scene(HERE/'exercise-ranking.template.htm',c,out),c


if __name__=='__main__':
    cfg=json.load(open(sys.argv[1]));out=pathlib.Path(sys.argv[2])
    for c in cfg if isinstance(cfg,list) else [cfg]:
        d,resolved=scene(c,out)
        (d/'resolved.json').write_text(json.dumps(resolved,indent=2))
        H.lint_check(d)
        if '--snap' in sys.argv:
            print(H.snapshot(d,[float(sys.argv[sys.argv.index('--snap')+1])]))
        if '--render' in sys.argv:H.render(d,out/(c['id']+'.mov'))
