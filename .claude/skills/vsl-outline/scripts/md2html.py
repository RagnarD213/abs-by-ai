import sys,re,html
def inl(s):
    s=html.escape(s,quote=False)
    s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s); s=re.sub(r'`(.+?)`',r'<i>\1</i>',s)
    s=re.sub(r'(?<!\w)\*(.+?)\*(?!\w)',r'<i>\1</i>',s); return s
out=['<html><body>']; lines=open(sys.argv[1]).read().split('\n'); i=0; lst=[]
def close():
    while lst: out.append('</%s>'%lst.pop())
while i<len(lines):
    l=lines[i]
    if l.startswith('|'):
        close(); rows=[]
        while i<len(lines) and lines[i].startswith('|'):
            c=[x.strip() for x in lines[i].strip('|').split('|')]
            if not all(set(x)<=set('-: ') for x in c): rows.append(c)
            i+=1
        out.append('<table border="1" cellpadding="4" style="border-collapse:collapse">')
        for k,r in enumerate(rows):
            t='th' if k==0 else 'td'; out.append('<tr>'+''.join(f'<{t}>{inl(x)}</{t}>' for x in r)+'</tr>')
        out.append('</table>'); continue
    m=re.match(r'^(#+) (.*)',l); b=re.match(r'^(\s*)[-\d]+[.)]? ?(.*)',l) if re.match(r'^\s*(- |\d+\. )',l) else None
    if m: close(); out.append(f'<h{len(m.group(1))}>{inl(m.group(2))}</h{len(m.group(1))}>')
    elif b:
        depth=len(b.group(1))//2+1; tag='ol' if re.match(r'^\s*\d',l) else 'ul'
        while len(lst)<depth: out.append(f'<{tag}>'); lst.append(tag)
        while len(lst)>depth: out.append('</%s>'%lst.pop())
        out.append(f'<li>{inl(b.group(2))}</li>')
    elif l.strip()=='---': close(); out.append('<hr>')
    elif l.strip(): close(); out.append(f'<p>{inl(l)}</p>')
    else: close()
    i+=1
close(); out.append('</body></html>'); open(sys.argv[2],'w').write('\n'.join(out))
