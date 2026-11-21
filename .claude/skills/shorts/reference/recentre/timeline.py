import json,sys
r=json.load(open(sys.argv[1]))
def ch(o):
    a=abs(o)
    if a<35: return '.'
    if a<60: return '-'
    if a<110: return 'x' if o>0 else 'l'   # x = right of centre, l = left
    return 'R' if o>0 else 'L'
for k,v in r.items():
    if not v.get('per'): print(k,'no person'); continue
    s=''.join(ch(p['off']) for p in v['per'])
    print(f"{k}\n  {s}")
