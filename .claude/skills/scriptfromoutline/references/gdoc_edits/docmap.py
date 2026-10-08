import json,sys,re
def load(path):
    d=json.load(open(path))['content']
    body=d['tabs'][0]['documentTab']['body']['content']
    paras=[]
    for el in body:
        if 'paragraph' not in el: continue
        p=el['paragraph']
        runs=[]
        for r in p['elements']:
            tr=r.get('textRun')
            if tr: runs.append((r['startIndex'],r['endIndex'],tr.get('content',''),tr.get('textStyle',{}),tr))
        text=''.join(x[2] for x in runs)
        paras.append({'s':el['startIndex'],'e':el['endIndex'],'t':text,'runs':runs,'bullet':p.get('bullet'),'style':p.get('paragraphStyle',{}).get('namedStyleType')})
    return d,paras
def norm(s): return s.replace('’',"'").replace('‘',"'").replace('“','"').replace('”','"')
def fulltext(paras):
    # returns (text, base) where text index i corresponds to doc index base+i ; doc body is contiguous from paras[0].s
    base=paras[0]['s']; out=[]; pos=base
    for p in paras:
        if p['s']!=pos: out.append('\x00'*(p['s']-pos))  # non-paragraph gap (tables etc)
        out.append(p['t']); pos=p['e']
    return ''.join(out),base
if __name__=='__main__':
    d,paras=load(sys.argv[1])
    print(d['revisionId'], len(paras))
