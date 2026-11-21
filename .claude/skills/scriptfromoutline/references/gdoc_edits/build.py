import json,sys
from docmap import load,norm
def build(docpath, ops, suggest):
    d,paras=load(docpath)
    out=[]; pos=0; off=0; errs=[]
    for n,op in enumerate(ops):
        if 'sec' in op:
            c=[k for k,p in enumerate(paras) if norm(p['t']).startswith(op['sec'])]
            if len(c)!=1: errs.append(f'op{n} sec {op["sec"]!r} matches {len(c)}'); continue
            pos=c[0]; off=0
            if len(op)==1: continue
        if 'para' in op:
            k=next((k for k in range(pos,len(paras)) if norm(paras[k]['t']).strip().startswith(op['para'])),None)
            if k is None: errs.append(f'op{n} para not found {op["para"][:50]!r}'); continue
            p=paras[k]; pos=k; off=0; mode=op['mode']
            s,e=p['s'],p['e']
            if mode=='delete': out.append((s,[{"deleteContentRange":{"range":{"startIndex":s,"endIndex":e}}}]))
            elif mode=='replace':
                if suggest: out.append((s,[{"insertText":{"location":{"index":e-1},"text":op['new']}},{"deleteContentRange":{"range":{"startIndex":s,"endIndex":e-1}}}]))
                else: out.append((s,[{"deleteContentRange":{"range":{"startIndex":s,"endIndex":e-1}}},{"insertText":{"location":{"index":s},"text":op['new']}}]))
            elif mode=='append': out.append((e-1,[{"insertText":{"location":{"index":e-1},"text":op['new']}}]))
            elif mode=='before': out.append((s,[{"insertText":{"location":{"index":s},"text":op['new']}}]))
            elif mode=='delete_through':  # delete from this para through para starting with op['through'] inclusive
                k2=next((q for q in range(k,len(paras)) if norm(paras[q]['t']).strip().startswith(op['through'])),None)
                if k2 is None: errs.append(f'op{n} through not found'); continue
                out.append((s,[{"deleteContentRange":{"range":{"startIndex":s,"endIndex":paras[k2]['e']}}}])); pos=k2
        elif 'find' in op:
            f=norm(op['find']); hit=None
            for k in range(pos,len(paras)):
                t=norm(paras[k]['t']); i=t.find(f, off if k==pos else 0)
                if i>=0: hit=(k,i); break
            if not hit: errs.append(f'op{n} find not found {op["find"][:60]!r}'); continue
            k,i=hit; pos=k; off=i+len(f)
            s=paras[k]['s']+i; e=s+len(f); new=op.get('new','')
            if op.get('after'):   # pure insertion after the found text
                out.append((e,[{"insertText":{"location":{"index":e},"text":new}}]))
            else:
                r=[]
                if suggest:
                    if new: r.append({"insertText":{"location":{"index":e},"text":new}})
                    r.append({"deleteContentRange":{"range":{"startIndex":s,"endIndex":e}}})
                else:
                    r.append({"deleteContentRange":{"range":{"startIndex":s,"endIndex":e}}})
                    if new: r.append({"insertText":{"location":{"index":s},"text":new}})
                out.append((s,r))
    out.sort(key=lambda x:-x[0])
    reqs=[r for _,rs in out for r in rs]
    return reqs,errs,d['revisionId']
if __name__=='__main__':
    import importlib
    m=importlib.import_module(sys.argv[2])
    reqs,errs,rev=build(sys.argv[1],m.ops,getattr(m,'suggest',False))
    print('ERRS',errs); print('REV',rev); print('N',len(reqs))
    idx=[ (r.get('insertText') or r.get('deleteContentRange')) for r in reqs]
    json.dump(reqs,open(sys.argv[2]+'.reqs.json','w'),ensure_ascii=False,separators=(',',':'))
    if '--print' in sys.argv: print(json.dumps(reqs,ensure_ascii=False,separators=(',',':')))
