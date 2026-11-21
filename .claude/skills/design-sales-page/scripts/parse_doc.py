import re, json, sys, html as H
from html.parser import HTMLParser
src = sys.argv[1]
h = open(src, encoding='utf-8').read()
css = re.search(r'<style[^>]*>(.*?)</style>', h, re.S).group(1)
bold, ital = set(), set()
for m in re.finditer(r'\.(c\d+)\{([^}]*)\}', css):
    if 'font-weight:700' in m.group(2): bold.add(m.group(1))
    if 'font-style:italic' in m.group(2): ital.add(m.group(1))
class P(HTMLParser):
    def __init__(s):
        super().__init__(convert_charrefs=True); s.blocks=[]; s.cur=None; s.stack=[]
    def handle_starttag(s, t, a):
        a=dict(a)
        if t in ('p','h1','h2','h3','li'):
            s.cur={'tag':t,'html':'','text':''}
        elif t=='span' and s.cur is not None:
            cl=set((a.get('class') or '').split())
            b=bool(cl&bold); i=bool(cl&ital)
            s.stack.append((b,i))
            if b: s.cur['html']+='<strong>'
            if i: s.cur['html']+='<em>'
        elif t=='img' and s.cur is not None:
            s.cur['html']+='[[IMG %s]]'%a.get('src'); s.cur['text']+='[[IMG %s]]'%a.get('src')
        elif t=='br' and s.cur is not None:
            s.cur['html']+='\n'; s.cur['text']+='\n'
    def handle_endtag(s, t):
        if t=='span' and s.cur is not None and s.stack:
            b,i=s.stack.pop()
            if i: s.cur['html']+='</em>'
            if b: s.cur['html']+='</strong>'
        elif t in ('p','h1','h2','h3','li') and s.cur is not None:
            c=s.cur; s.cur=None
            c['html']=re.sub(r'</strong><strong>','',c['html'])
            c['html']=re.sub(r'</em><em>','',c['html'])
            if c['text'].strip(): s.blocks.append(c)
    def handle_data(s, d):
        if s.cur is not None:
            e=H.escape(d, quote=False)
            s.cur['html']+=e; s.cur['text']+=d
p=P(); p.feed(h)
json.dump(p.blocks, open(sys.argv[2],'w'), ensure_ascii=False, indent=0)
for i,b in enumerate(p.blocks):
    print(i, b['tag'], repr(b['text'][:90]))
print('EMDASH count:', sum(b['text'].count('\u2014') for b in p.blocks), 'ENDASH:', sum(b['text'].count('\u2013') for b in p.blocks))
